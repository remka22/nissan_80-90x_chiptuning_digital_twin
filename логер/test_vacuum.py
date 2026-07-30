# -*- coding: utf-8 -*-
"""
Тест «в вакууме» — проверяет всю программную цепочку БЕЗ железа и БЕЗ сети:
кодирование кадра -> байт-поток -> декодер -> пересчёт в физику.

Проверяет:
  A. round-trip известных значений (адреса/порядок/16-бит/пересчёт);
  B. ресинхронизацию при мусоре и ложном 0xFF в потоке;
  C. что фейковый ЭБУ реально даёт декодируемый поток.
"""
import math
import frame
import ecu_sim


def test_a_roundtrip():
    print("=== A. round-trip известных значений ===")
    raw_in = {"rpm": 0x0271, "load": 0x64, "o2": 0x30,
              "tp": 0x0258, "alpha": 0x80, "volt": 0xB4}
    dec = frame.StreamDecoder()
    recs = dec.feed(frame.encode(raw_in))
    assert len(recs) == 1, "ждали 1 кадр, получили %d" % len(recs)
    got = recs[0]
    print("  вход :", {k: hex(v) for k, v in raw_in.items()})
    print("  выход:", {k: hex(v) for k, v in got.items()})
    ok = all(got[k] == (raw_in[k] & (0xFEFF if sz == 2 else 0xFE)) or got[k] == raw_in[k]
             for k, _a, sz, _c in frame.FIELDS)
    # точная сверка (значения выбраны без 0xFF-байт, зажатие не влияет)
    exact = got == raw_in
    phys = frame.to_phys(got)
    print("  физика:", phys)
    print("  RPM физ:", phys["rpm"], "об/мин (ожид. ~", round(0x0271*12.807), ")")
    print("  напряж :", phys["volt"], "В (ожид.", round(0xB4*0.0195, 2), ")")
    res = exact and phys["rpm"] == round(0x0271*12.807)
    print("  ИТОГ:", "OK ✓" if res else "ПРОВАЛ ✗")
    return res


def test_b_resync():
    print("\n=== B. ресинхронизация при мусоре ===")
    raw = {"rpm": 0x0400, "load": 0x50, "o2": 0x20,
           "tp": 0x0300, "alpha": 0x7F, "volt": 0xB0}
    good = frame.encode(raw)
    # поток: мусор + обрезок кадра + мусор + два целых кадра
    stream = bytes([0x13, 0x9C, 0xFF, 0x01]) + good[3:] + bytes([0x77]) + good + good
    dec = frame.StreamDecoder()
    recs = dec.feed(stream)
    print("  кадров восстановлено:", len(recs), " отброшено байт:", dec.bad)
    ok = len(recs) >= 2 and all(r == raw for r in recs[-2:])
    print("  последние 2 кадра корректны:", "да ✓" if ok else "нет ✗")
    print("  ИТОГ:", "OK ✓" if ok else "ПРОВАЛ ✗")
    return ok


def test_c_simstream():
    print("\n=== C. поток фейкового ЭБУ декодируется ===")
    dec = frame.StreamDecoder()
    got = []
    for i in range(50):
        got += dec.feed(ecu_sim.frame_bytes(i * 0.05))
    print("  сгенерено 50 кадров, декодировано:", len(got))
    # значения должны шевелиться (обороты не константа)
    rpms = [frame.to_phys(r)["rpm"] for r in got]
    moving = len(set(rpms)) > 5
    print("  обороты диапазон:", min(rpms), "..", max(rpms),
          "(меняются:", "да ✓" if moving else "нет ✗", ")")
    ok = len(got) == 50 and moving
    print("  ИТОГ:", "OK ✓" if ok else "ПРОВАЛ ✗")
    return ok


if __name__ == "__main__":
    r = [test_a_roundtrip(), test_b_resync(), test_c_simstream()]
    print("\n===== ОБЩИЙ ИТОГ:",
          "ВСЁ OK ✓" if all(r) else "ЕСТЬ ПРОВАЛЫ ✗", "=====")
    import sys
    sys.exit(0 if all(r) else 1)
