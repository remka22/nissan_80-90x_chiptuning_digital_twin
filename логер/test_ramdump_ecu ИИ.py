# -*- coding: utf-8 -*-
"""
Тест подпрограммы-ДАМПЕРА ОЗУ на двойнике (ЭБУ-сторона).
Вкалываем в ОЗУ узор mem[addr]=addr&0xFF, гоняем подпрограмму C603 (логику дампа
мимо родного JSR), собираем SCI-поток НАШИМ ЖЕ декодером ramframe и сверяем, что
восстановленный образ ОЗУ совпал с вколотым. Если контрольные суммы блоков
верны — декодер их примет, и покрытие будет полным.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ecu_twin", "backend"))
from emulator.machine import Machine
import ramframe

BIN = os.path.join(HERE, "..", "j30", "J30_дамп_озу_тест ИИ.bin")
DUMP_LOGIC = 0xC603            # вход в логику дампа МИМО родного JSR $A99B
# два диапазона дампа: внутренний ОЗУ 6303 + внешний ОЗУ HD63140
RANGES = [(0x0040, 0x0100), (0x1400, 0x1800)]
STATE = {0xFA, 0xFB, 0xFC, 0xFD}    # свои рабочие байты — в дампе «живые», не сверяем


def main():
    m = Machine(BIN)
    m.boot(80_000)
    b = m.bus
    # вколоть узнаваемый узор: байт = младший байт адреса (оба диапазона)
    for lo, hi in RANGES:
        for a in range(lo, hi):
            b.mem[a] = a & 0xFF
    # состояние подпрограммы в 0 (иначе ptr!=0 и обход стартует не туда)
    for s in STATE:
        b.mem[s] = 0
    b.sci_tx = []

    # полный обход: (192+1024)/16=76 блоков × 22 = 1672; берём с запасом
    calls = 1800
    for _ in range(calls):
        r = m.call_routine(DUMP_LOGIC)
        if r["crashed"] or not r["reached_return"]:
            print("ПРОВАЛ: подпрограмма сорвалась:", r)
            sys.exit(1)

    print("вызовов:", calls, " передано байт:", len(b.sci_tx))

    dec = ramframe.RamDecoder()
    dec.feed(bytes(b.sci_tx))
    print("адресов в образе:", len(dec.image), " отброшено байт:", dec.bad)

    total = covered = mism = 0
    bad = []
    for lo, hi in RANGES:
        for a in range(lo, hi):
            total += 1
            if a in dec.image:
                covered += 1
                if dec.image[a] != (a & 0xFF) and a not in STATE:
                    mism += 1
                    bad.append(a)
    print("покрыто: %d из %d (внутр. $40-$FF + внешн. $1400-$17FF)" % (covered, total))
    print("несовпадений (кроме своих $FA-$FD):", mism)
    if bad:
        print("  плохие адреса:", ["$%04X" % a for a in bad[:8]])
    # показать, что свои байты состояния реально попали в дамп
    print("  свои байты в дампе: " + " ".join(
        "$%02X=%s" % (s, hex(dec.image.get(s, -1))) for s in sorted(STATE)))

    ok = (covered == total) and (mism == 0)
    print("\n===== ИТОГ:",
          "OK ✓ (ЭБУ дампит ОБА диапазона ОЗУ, декодер собрал верно)" if ok
          else "ПРОВАЛ ✗", "=====")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
