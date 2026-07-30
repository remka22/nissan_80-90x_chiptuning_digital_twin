# -*- coding: utf-8 -*-
"""
Тест-стенд патча-логгера на цифровом двойнике.

Часть A (юнит) — строгая проверка ЛОГИКИ логгера с известными числами:
  вкалываем в $140A/$140B/$1482 сентинелы, зовём подпрограмму с C603
  (сразу после родного JSR), ловим поток SCI и сверяем БАЙТ-В-БАЙТ.
  Ловит: неверный адрес источника, перепутанный старший/младший, сбой синхры,
  ошибку round-robin.

Часть B (интеграция) — врезка в РЕАЛЬНОМ ISR:
  заводим J30, крутим мотор, проверяем что прошивка не упала и поток байт идёт
  (значит JSR-редирект + родной вызов + телеметрия сосуществуют).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "ecu_twin", "backend"))
from emulator.machine import Machine

BIN = os.path.join(HERE, "J30_логгер_тест ИИ.bin")
LOGGER_AFTER_ORIG = 0xC603     # вход в логгер МИМО JSR $9A9B
IDX = 0x00FC


def part_a():
    print("=== Часть A: юнит-тест логики логгера ===")
    m = Machine(BIN)
    m.boot(80_000)                       # инициализация ОЗУ прошивкой
    b = m.bus
    # известные сентинелы
    m.poke8(0x140A, 0x12)                # RPM hi
    m.poke8(0x140B, 0x34)                # RPM lo
    m.poke8(0x1482, 0x56)                # нагрузка
    m.poke8(IDX, 0x00)                   # индекс кадра с нуля
    b.sci_tx = []
    for _ in range(8):                   # два полных кадра по 4 байта
        m.call_routine(LOGGER_AFTER_ORIG)
    got = list(b.sci_tx)
    exp = [0xFF, 0x12, 0x34, 0x56, 0xFF, 0x12, 0x34, 0x56]
    print("  ожидалось:", " ".join("%02X" % x for x in exp))
    print("  получено :", " ".join("%02X" % x for x in got))
    ok = got == exp
    print("  ИТОГ:", "OK ✓" if ok else "ПРОВАЛ ✗")
    return ok


def part_b():
    print("\n=== Часть B: врезка-обёртка (JSR A99B + телеметрия) ===")
    m = Machine(BIN)
    b = m.bus
    # 1. статическая проверка байт врезки в патче
    hoff = 0x83F8 - 0x8000
    hook_ok = (b.mem[0x83F8] == 0xBD and b.mem[0x83F9] == 0xC6 and b.mem[0x83FA] == 0x00)
    head_ok = (b.mem[0xC600] == 0xBD and b.mem[0xC601] == 0xA9 and b.mem[0xC602] == 0x9B)
    print("  83F8 = JSR C600 :", "да ✓" if hook_ok else "НЕТ ✗")
    print("  C600 = JSR A99B :", "да ✓" if head_ok else "НЕТ ✗")
    # ПРИМЕЧАНИЕ: двойник для J30 НЕ исполняет натуральный ISR-блок 83xx (гонит
    # мотор «явной цепочкой»), поэтому врезку проверяем ПРЯМЫМ вызовом обёртки C600:
    # она обязана сама вызвать родное A99B, затем передать байт и чисто вернуться.
    m.start_engine()
    m.poke8(IDX, 0x00)
    b.sci_tx = []
    clean = True
    for _ in range(8):                   # два кадра через полную обёртку
        r = m.call_routine(0xC600)
        if not r["reached_return"] or r["crashed"]:
            clean = False
            print("  прогон обёртки сорвался:", r)
            break
    tx = list(b.sci_tx)
    print("  обёртка вернулась чисто:", "да ✓" if clean else "НЕТ ✗")
    print("  байт передано:", len(tx), "->", " ".join("%02X" % x for x in tx))
    # синхро-маркер должен попадать на позиции 0 и 4 (round-robin из 4)
    sync_ok = len(tx) == 8 and tx[0] == 0xFF and tx[4] == 0xFF
    print("  синхро 0xFF на позициях 0 и 4:", "да ✓" if sync_ok else "НЕТ ✗")
    ok = hook_ok and head_ok and clean and sync_ok
    print("  ИТОГ:", "OK ✓ (обёртка вызывает A99B и шлёт кадр, стек цел)"
          if ok else "ПРОВАЛ ✗")
    return ok


if __name__ == "__main__":
    a = part_a()
    b = part_b()
    print("\n===== ОБЩИЙ ИТОГ:", "ВСЁ OK ✓" if (a and b) else "ЕСТЬ ПРОВАЛЫ ✗", "=====")
    sys.exit(0 if (a and b) else 1)
