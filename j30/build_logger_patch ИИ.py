# -*- coding: utf-8 -*-
"""
Билдер патча-логгера SCI-телеметрии для J30.
Берёт родной сток HN27C256G@DIP28.BIN, вставляет подпрограмму-логгер в свободный
блок ПЗУ (C600) и перенаправляет одну JSR в главном ISR на неё. Пишет новый бин.

Подпрограмма (round-robin, неблокирующая, 1 байт за вызов):
  C600  JSR $A99B        ; родной вызов, который мы замещаем (прозрачно)
  C603  init SCI (RMCR=0x0C baud, TRCSR=0x02 TE) — идемпотентно
        если TDRE занят -> выход (не блокируем ISR)
        иначе шлём следующий байт кадра [0xFF, RPMhi $140A, RPMlo $140B, load $1482]
        индекс кадра в ОЗУ $00FC (внутр. ОЗУ 6303, прошивкой не используется)

Врезка: 83F8 в стоке = JSR $A99B (BD A9 9B). Меняем операнд на C600 ->
подпрограмма сама делает JSR $9A9B, потом телеметрию. Логика мотора цела.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "HN27C256G@DIP28.BIN")          # родной сток J30 (МКПП)
DST = os.path.join(HERE, "J30_логгер_тест ИИ.bin")
ROM_BASE = 0x8000

CODE_ORG = 0xC600          # свободный блок 0x3F (C5E4..EEFF)
IDX      = 0x00FC          # байт индекса round-robin во внутр. ОЗУ
HOOK_CPU = 0x83F8          # адрес JSR $A99B в главном ISR (врезка)
ORIG_CALL = 0xA99B         # оригинальный вызов, который замещаем

# ---- мини-ассемблер (два прохода по меткам/ветвлениям) --------------------
def assemble(org):
    # (мнемоника, операнды...) ; ветвления по метке-строке
    prog = [
        ("JSR",  ORIG_CALL),        # C600: родной вызов
        # --- init SCI (идемпотентно каждый вызов) ---
        ("LDAA#", 0x0C),
        ("STAA",  0x0010),          # RMCR = скорость E/16 = кварц/64
        ("LDAA#", 0x02),
        ("STAA",  0x0011),          # TRCSR = TE (только передача)
        # --- готов ли передатчик? ---
        ("LDAA",  0x0011),
        ("BITA#", 0x20),            # TDRE
        ("BEQ",   "DONE"),          # занят -> выход (неблокирующе)
        # --- выбрать байт кадра по индексу ---
        ("LDAB",  IDX),
        ("ASLB",),                  # ×2 (записи таблицы 16-битные)
        ("LDX#",  "TABLE"),
        ("ABX",),                   # X = TABLE + idx*2
        ("LDXid", 0x00),            # X = *(TABLE[idx]) = адрес источника
        ("LDAAid",0x00),            # A = байт из источника
        ("STAA",  0x0013),          # передать в TDR
        # --- продвинуть индекс (0..3, wrap) ---
        ("LDAB",  IDX),
        ("INCB",),
        ("CMPB#", 0x04),
        ("BCS",   "SAVE"),
        ("CLRB",),
        ("SAVE:STAB", IDX),
        ("DONE:RTS",),
        # --- таблица указателей на источники ---
        ("TABLE:WORD", "SYNC"),
        ("WORD",  0x140A),          # RPM hi
        ("WORD",  0x140B),          # RPM lo
        ("WORD",  0x1482),          # нагрузка
        ("SYNC:BYTE", 0xFF),        # синхро-маркер кадра
    ]
    LEN = {
        "JSR":3, "LDAA#":2, "STAA":3, "LDAA":3, "BITA#":2, "BEQ":2, "LDAB":2,
        "ASLB":1, "LDX#":3, "ABX":1, "LDXid":2, "LDAAid":2, "INCB":1, "CMPB#":2,
        "BCS":2, "CLRB":1, "STAB":2, "RTS":1, "WORD":2, "BYTE":1,
    }
    def base_mnem(m):
        return m.split(":")[-1]
    # проход 1: адреса меток
    labels = {}
    pc = org
    for ins in prog:
        m = ins[0]
        if ":" in m and not m.endswith(":"):
            lbl = m.split(":")[0]
            labels[lbl] = pc
        pc += LEN[base_mnem(m)]
    # проход 2: байты
    out = bytearray()
    pc = org
    for ins in prog:
        m = base_mnem(ins[0])
        nxt = pc + LEN[m]
        if m == "JSR":   out += bytes([0xBD, ins[1] >> 8, ins[1] & 0xFF])
        elif m == "LDAA#": out += bytes([0x86, ins[1]])
        elif m == "STAA":  out += bytes([0xB7, ins[1] >> 8, ins[1] & 0xFF])
        elif m == "LDAA":  out += bytes([0xB6, ins[1] >> 8, ins[1] & 0xFF])
        elif m == "BITA#": out += bytes([0x85, ins[1]])
        elif m == "BEQ":
            rel = labels[ins[1]] - nxt; assert -128 <= rel <= 127
            out += bytes([0x27, rel & 0xFF])
        elif m == "BCS":
            rel = labels[ins[1]] - nxt; assert -128 <= rel <= 127
            out += bytes([0x25, rel & 0xFF])
        elif m == "LDAB":  out += bytes([0xD6, ins[1] & 0xFF])
        elif m == "STAB":  out += bytes([0xD7, ins[1] & 0xFF])
        elif m == "ASLB":  out += bytes([0x58])
        elif m == "LDX#":
            addr = labels[ins[1]]; out += bytes([0xCE, addr >> 8, addr & 0xFF])
        elif m == "ABX":   out += bytes([0x3A])
        elif m == "LDXid": out += bytes([0xEE, ins[1]])
        elif m == "LDAAid":out += bytes([0xA6, ins[1]])
        elif m == "INCB":  out += bytes([0x5C])
        elif m == "CMPB#": out += bytes([0xC1, ins[1]])
        elif m == "CLRB":  out += bytes([0x5F])
        elif m == "RTS":   out += bytes([0x39])
        elif m == "WORD":
            v = labels[ins[1]] if isinstance(ins[1], str) else ins[1]
            out += bytes([v >> 8, v & 0xFF])
        elif m == "BYTE":  out += bytes([ins[1]])
        else: raise ValueError(m)
        pc = nxt
    return out, labels


def main():
    rom = bytearray(open(SRC, "rb").read())
    assert len(rom) == 32768, "ждём 32К ПЗУ"

    # 1. проверить, что целевой блок ПЗУ реально свободен (0x3F)
    code, labels = assemble(CODE_ORG)
    off = CODE_ORG - ROM_BASE
    region = rom[off:off + len(code)]
    assert all(b == 0x3F for b in region), \
        "целевой блок C600 НЕ пустой (0x3F) — выбери другое место"

    # 2. проверить точку врезки: 83F8 должно быть JSR $9A9B (BD 9A 9B)
    hoff = HOOK_CPU - ROM_BASE
    assert rom[hoff] == 0xBD and (rom[hoff+1] << 8 | rom[hoff+2]) == ORIG_CALL, \
        "по 83F8 не JSR $9A9B — врезка невозможна без пересмотра"

    # 3. вставить код и перенаправить врезку на C600
    rom[off:off + len(code)] = code
    rom[hoff+1] = CODE_ORG >> 8
    rom[hoff+2] = CODE_ORG & 0xFF

    open(DST, "wb").write(rom)
    print("Готово:", os.path.basename(DST))
    print("  подпрограмма %d байт @ %04X..%04X" % (len(code), CODE_ORG, CODE_ORG + len(code) - 1))
    print("  метки:", {k: "%04X" % v for k, v in labels.items()})
    print("  врезка 83F8: JSR %04X -> JSR %04X" % (ORIG_CALL, CODE_ORG))
    print("  индекс кадра в ОЗУ $%04X" % IDX)


if __name__ == "__main__":
    main()
