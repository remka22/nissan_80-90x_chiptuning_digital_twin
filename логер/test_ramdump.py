# -*- coding: utf-8 -*-
"""
Вакуум-тест протокола полного дампа ОЗУ (без железа, без сети).
A. блок кодируется/декодируется, произвольные байты (0xFF) проходят;
B. ресинхронизация при мусоре и ложной синхре в данных;
C. полный обход указателя покрывает ВЕСЬ диапазон ОЗУ.
"""
import ramframe
import ram_sim


def test_a():
    print("=== A. блок round-trip + произвольные байты ===")
    data = bytes([0xFF, 0x00, 0xAE, 0x17, 0x55, 0xFF])   # спец-байты внутри!
    dec = ramframe.RamDecoder()
    blocks = dec.feed(ramframe.encode_block(0x1400, data))
    ok = (len(blocks) == 1 and blocks[0][1] == data
          and all(dec.image[0x1400 + k] == data[k] for k in range(len(data))))
    print("  данные с 0xFF и 0xAE17 внутри восстановлены:", "да ✓" if ok else "нет ✗")
    return ok


def test_b():
    print("\n=== B. ресинхронизация при мусоре/ложной синхре ===")
    good = ramframe.encode_block(0x1480, bytes([1, 2, 3, 0xAE, 0x17, 9]))
    stream = bytes([0x00, 0xAE, 0x17, 0x99]) + good[4:] + bytes([0x42]) + good + good
    dec = ramframe.RamDecoder()
    blocks = dec.feed(stream)
    ok = len(blocks) >= 2 and all(b[0] == 0x1480 for b in blocks[-2:])
    print("  блоков восстановлено:", len(blocks), " отброшено:", dec.bad)
    print("  последние 2 корректны:", "да ✓" if ok else "нет ✗")
    return ok


def test_c():
    print("\n=== C. полный обход покрывает ОБА диапазона ОЗУ ===")
    dec = ramframe.RamDecoder()
    nblk = 2 * len(ram_sim._starts) + 2      # два полных обхода
    for i in range(nblk):
        dec.feed(ram_sim.next_block(i * 0.05))
    total = sum(hi - lo for lo, hi in ram_sim.RANGES)
    covered = sum(1 for lo, hi in ram_sim.RANGES
                  for a in range(lo, hi) if a in dec.image)
    print("  покрыто адресов: %d из %d (внутр.+внешн.)" % (covered, total))
    print("  внутр. напряжение $008F =", hex(dec.image.get(0x008F, -1)))
    ok = covered == total and 0x008F in dec.image
    print("  оба диапазона + внутренний байт:", "да ✓" if ok else "нет ✗")
    return ok


if __name__ == "__main__":
    import sys
    r = [test_a(), test_b(), test_c()]
    print("\n===== ИТОГ:", "ВСЁ OK ✓" if all(r) else "ЕСТЬ ПРОВАЛЫ ✗", "=====")
    sys.exit(0 if all(r) else 1)
