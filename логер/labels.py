# -*- coding: utf-8 -*-
"""
Таблица меток «адрес ОЗУ -> смысл» для J30. Навешивается на сырой дамп ОЗУ,
чтобы известные адреса показывались осмысленно, а неизвестные — как raw.

conf: high  — доказано трассировкой кода;
      med   — выведено, но не добито до конца;
      addr  — адрес точен (по коду), но физический смысл ещё не подтверждён.

size: 1 или 2 (16-бит big-endian);  ch: канал АЦП, если это датчик-вход.
Пополняется по мере разбора (это НЕ финальный список).
"""

# ключ = адрес; поля: name, size, conf, ch(опц.), note(опц.)
LABELS = {
    # --- ВХОДЫ АЦП (закрытый список каналов, по коду b148..b1e0 / 8908 / 9523) ---
    0x1408: {"name": "MAF расход (нагрузка)", "size": 2, "conf": "high", "ch": 0},
    0x1400: {"name": "O2 лямбда (сырой)",     "size": 1, "conf": "high", "ch": 3},
    0x008F: {"name": "напряжение борта",       "size": 1, "conf": "high", "ch": 1},
    0x140D: {"name": "напряжение (сглаж.)",    "size": 1, "conf": "high", "ch": 1},
    0x004C: {"name": "АЦП кан.2 (сырой)",      "size": 1, "conf": "addr", "ch": 2},
    0x140E: {"name": "АЦП кан.2 (сглаж.)",     "size": 1, "conf": "addr", "ch": 2},
    0x1402: {"name": "АЦП кан.4 (темп ОЖ?)",   "size": 1, "conf": "addr", "ch": 4},
    0x1527: {"name": "АЦП кан.4 сглаж (темп?)","size": 1, "conf": "addr", "ch": 4},
    0x1401: {"name": "АЦП кан.5 (сырой)",      "size": 1, "conf": "addr", "ch": 5},
    0x14CA: {"name": "АЦП кан.5 (сглаж.)",     "size": 1, "conf": "addr", "ch": 5},
    0x1574: {"name": "АЦП кан.8 (сырой)",      "size": 1, "conf": "addr", "ch": 8},
    0x1573: {"name": "АЦП кан.8 (сглаж.)",     "size": 1, "conf": "addr", "ch": 8},
    0x1583: {"name": "АЦП кан.7",              "size": 1, "conf": "addr", "ch": 7},

    # --- ПРОИЗВОДНЫЕ (вычислены из датчиков + таблиц ПЗУ) ---
    0x140A: {"name": "обороты", "size": 2, "conf": "high",
             "note": "×12.807 об/мин"},
    0x1482: {"name": "нагрузка (индекс карт)", "size": 1, "conf": "high"},
    0x1413: {"name": "Tp база впрыска", "size": 2, "conf": "high"},
    0x1411: {"name": "импульс впрыска", "size": 2, "conf": "high"},
    0x1437: {"name": "ALPHA (замкнутый цикл)", "size": 1, "conf": "high"},
    0x00B1: {"name": "температура ОЖ (индекс)", "size": 1, "conf": "med",
             "note": "индексирует прогревочные таблицы F700/F720/F740"},
    0x004D: {"name": "длит. впрыска (HD63140)", "size": 2, "conf": "med",
             "note": "×0.005 мс"},
}


def label_for(addr):
    return LABELS.get(addr)


def summary():
    hi = sum(1 for v in LABELS.values() if v["conf"] == "high")
    print("Меток: %d (доказано: %d, адрес-без-смысла: %d, выведено: %d)" % (
        len(LABELS), hi,
        sum(1 for v in LABELS.values() if v["conf"] == "addr"),
        sum(1 for v in LABELS.values() if v["conf"] == "med")))


if __name__ == "__main__":
    summary()
    for a in sorted(LABELS):
        v = LABELS[a]
        print("  $%04X  %-28s %s%s" % (
            a, v["name"], v["conf"],
            "  (кан.%d)" % v["ch"] if "ch" in v else ""))
