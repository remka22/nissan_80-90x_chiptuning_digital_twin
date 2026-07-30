# -*- coding: utf-8 -*-
"""
ТЕСТ МЕТОДА РАСШИФРОВКИ на двойнике.

Двойник даёт И дамп ОЗУ, И правильный ответ (мы знаем: $140A=обороты,
$1482=нагрузка). Прогоняем метод корреляции ВСЛЕПУЮ по снимкам ОЗУ и
проверяем, вычислит ли он верные адреса сам.

Сетка режимов: обороты и MAF варьируем НЕЗАВИСИМО (полная сетка), чтобы
корреляция могла их разделить.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ecu_twin", "backend"))
from emulator.machine import Machine
import decode

# бин можно передать аргументом (для сверки J30 vs M30); по умолчанию — J30
BIN = (sys.argv[1] if len(sys.argv) > 1
       else os.path.join(HERE, "..", "j30", "HN27C256G@DIP28.BIN"))
RAM_LO, RAM_HI = 0x1400, 0x1600          # окно снимка ОЗУ (512 байт)

# опоры (истина, которую метод НЕ видит — только для сверки в конце)
TRUTH = {"обороты": 0x140A, "нагрузка": 0x1482}


def capture():
    m = Machine(BIN)
    m.start_engine()
    periods = [250, 350, 500, 700]        # меньше период = выше обороты
    mafs    = [0x0080, 0x0140, 0x0220, 0x0320]
    snaps, rpm_ref, maf_ref = [], [], []
    for p in periods:
        for maf in mafs:
            m.engine_run(rpm_period=p, maf_adc=maf, cycles=4)
            snaps.append(bytes(m.bus.mem[RAM_LO:RAM_HI]))
            rpm_ref.append(1_000_000.0 / p)   # прокси оборотов (~1/период)
            maf_ref.append(float(maf))
    return snaps, rpm_ref, maf_ref


def report(name, ranked, truth_addr, topn=6):
    print("\n--- опора: %s (истина = $%04X) ---" % (name, truth_addr))
    hit_rank = None
    for rank, (addr, ar, r) in enumerate(ranked[:topn], 1):
        mark = "  <== ИСТИНА" if addr == truth_addr else ""
        print("  %d. $%04X  |r|=%.3f%s" % (rank, addr, ar, mark))
    for rank, (addr, ar, r) in enumerate(ranked, 1):
        if addr == truth_addr:
            hit_rank = rank
            break
    ok = hit_rank is not None and hit_rank <= 3
    print("  истина на месте %s -> %s" %
          (hit_rank, "OK ✓ (в топ-3)" if ok else "мимо ✗"))
    return ok


def main():
    print("Снимаю ОЗУ двойника под 16 режимами (обороты × MAF независимо)...")
    snaps, rpm_ref, maf_ref = capture()
    const, vary = decode.classify(snaps, RAM_LO)
    print("Снимков: %d | окно $%04X..$%04X | меняются %d байт, константы %d"
          % (len(snaps), RAM_LO, RAM_HI - 1, len(vary), len(const)))

    # обороты — 16-битные, ищем СЛОВНЫМ режимом
    print("\n=== ОБОРОТЫ (словный режим, 16-бит) ===")
    r_rpm_w = decode.rank_words(snaps, rpm_ref, RAM_LO)
    ok_rpm = report("обороты", r_rpm_w, TRUTH["обороты"])

    # нагрузка — 1 байт, байтовый режим
    print("\n=== НАГРУЗКА (байтовый режим) ===")
    r_maf_b = decode.rank_bytes(snaps, maf_ref, RAM_LO)
    ok_load = report("нагрузка", r_maf_b, TRUTH["нагрузка"])

    print("\n===== ИТОГ МЕТОДА:",
          "РАБОТАЕТ ✓ (сам нашёл верные адреса)" if (ok_rpm and ok_load)
          else "требует доработки ✗", "=====")
    sys.exit(0 if (ok_rpm and ok_load) else 1)


if __name__ == "__main__":
    main()
