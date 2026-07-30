# -*- coding: utf-8 -*-
"""
Формат кадра телеметрии J30 — ЕДИНЫЙ источник правды.
Используется и «фейковым ЭБУ» (кодирование), и демоном (декодирование),
чтобы они не разошлись.

Поток байт от ЭБУ (SCI):
    [SYNC=0xFF] [payload...] [checksum]  [SYNC] [payload...] [checksum] ...
  - payload = поля из FIELDS по порядку (1 или 2 байта каждое, старший первым);
  - все байты payload и checksum ЗАЖАТЫ до <=0xFE (0xFF зарезервирован под SYNC),
    поэтому 0xFF в потоке = ВСЕГДА начало кадра -> надёжная синхронизация;
  - checksum = XOR всех байт payload (тоже зажат) — отсев ложных срабатываний.

Цена зажатия: значение 0xFF байта -> 0xFE (для 8-бит датчика незаметно; для
16-бит оборотов максимум ~13 об/мин погрешности на редкой границе). Для первого
«просто увидеть что прилетает» — приемлемо.
"""

SYNC = 0xFF

# (ключ, адрес в ОЗУ ЭБУ, размер байт, тип пересчёта в физику)
# Пересчёт — те же коэффициенты, что в редакторе (CONV).
FIELDS = [
    ("rpm",   0x140A, 2, "rpm"),    # обороты (16-бит)
    ("load",  0x1482, 1, "raw"),    # нагрузка (ось карт)
    ("o2",    0x1400, 1, "raw"),    # лямбда (сырой АЦП)
    ("tp",    0x1413, 2, "raw"),    # база впрыска Tp
    ("alpha", 0x1437, 1, "raw"),    # ALPHA (замкнутый цикл)
    ("volt",  0x008F, 1, "volt"),   # напряжение борта (оценка)
]

PAYLOAD_LEN = sum(sz for _, _, sz, _ in FIELDS)
FRAME_LEN = 1 + PAYLOAD_LEN + 1        # SYNC + payload + checksum


def _clamp(b):
    """Зажать байт до <=0xFE (0xFF только под SYNC)."""
    b &= 0xFF
    return 0xFE if b == 0xFF else b


def encode(raw):
    """raw: dict {ключ: сырое_целое} -> bytes одного кадра."""
    payload = bytearray()
    for key, _addr, sz, _conv in FIELDS:
        v = int(raw.get(key, 0)) & (0xFFFF if sz == 2 else 0xFF)
        if sz == 2:
            payload.append(_clamp(v >> 8))
            payload.append(_clamp(v & 0xFF))
        else:
            payload.append(_clamp(v))
    chk = 0
    for b in payload:
        chk ^= b
    return bytes([SYNC]) + bytes(payload) + bytes([_clamp(chk)])


class StreamDecoder:
    """Кормим байтами (feed) -> отдаёт список готовых записей {ключ: сырое}.
    Сам ресинхронизируется по SYNC и проверяет контрольную сумму."""

    def __init__(self):
        self.buf = bytearray()
        self.bad = 0        # счётчик отброшенных байт (диагностика)

    def feed(self, data):
        self.buf.extend(data)
        out = []
        while True:
            # выкинуть мусор до первого SYNC
            si = self.buf.find(SYNC)
            if si < 0:
                self.bad += len(self.buf)
                self.buf.clear()
                break
            if si > 0:
                self.bad += si
                del self.buf[:si]
            # достаточно ли байт на полный кадр?
            if len(self.buf) < FRAME_LEN:
                break
            payload = self.buf[1:1 + PAYLOAD_LEN]
            chk = self.buf[1 + PAYLOAD_LEN]
            calc = 0
            for b in payload:
                calc ^= b
            if _clamp(calc) != chk:
                # ложный SYNC — сдвинуться на 1 байт и искать заново
                self.bad += 1
                del self.buf[0]
                continue
            out.append(self._split(payload))
            del self.buf[:FRAME_LEN]
        return out

    @staticmethod
    def _split(payload):
        rec = {}
        i = 0
        for key, _addr, sz, _conv in FIELDS:
            if sz == 2:
                rec[key] = (payload[i] << 8) | payload[i + 1]
                i += 2
            else:
                rec[key] = payload[i]
                i += 1
        return rec


# --- пересчёт сырое -> физика (коэффициенты из редактора) --------------------
def to_phys(raw):
    phys = {}
    for key, _addr, _sz, conv in FIELDS:
        v = raw.get(key, 0)
        if conv == "rpm":
            phys[key] = round(v * 12.807)
        elif conv == "volt":
            phys[key] = round(v * 0.0195, 2)
        else:
            phys[key] = v
    return phys


UNITS = {"rpm": "об/мин", "load": "ед", "o2": "АЦП", "tp": "ед",
         "alpha": "ед", "volt": "В~"}
