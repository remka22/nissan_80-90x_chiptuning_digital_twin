# -*- coding: utf-8 -*-
"""
FastAPI-бэкенд двойника ЭБУ.
REST:
  GET  /api/meta             — список входов/наблюдаемых/рутин/таблиц
  POST /api/run              — прогнать рутину с входами, вернуть наблюдаемые
  POST /api/sweep            — свип одного входа, вернуть таблицу
  GET  /api/disasm?addr=...  — короткий дизасм вокруг адреса (для контекста)
Статика фронта — из ../frontend.
"""
import os
import json
import threading
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

from emulator import Machine, symbols

ROM_PATH = os.environ.get("ECU_ROM", "/data/rom.bin")
ROM_BASE = int(os.environ.get("ECU_ROM_BASE", "0x8000"), 0)
FRONT_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
PCN_PATH = os.path.join(FRONT_DIR, "pcn_data.json")
BCN_PATH = os.path.join(FRONT_DIR, "bcn_data.json")
DAD_PATH = os.path.join(FRONT_DIR, "dad_data.json")


_edit_lock = threading.Lock()   # правки таблиц — строго по одной, иначе затирают друг друга


def _atomic_write(path, data):
    """Пишем через временный файл + подмену — иначе быстрые правки подряд бьют JSON."""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=0)
    os.replace(tmp, path)

app = FastAPI(title="ЭБУ-двойник M30 (SIL)")


@app.middleware("http")
async def no_cache(request, call_next):
    """Фронт не кэшировать — чтобы правки JS/HTML всегда подхватывались."""
    resp = await call_next(request)
    p = request.url.path
    if p == "/" or p.startswith("/static") or p.endswith((".js", ".css", ".html")):
        resp.headers["Cache-Control"] = "no-store, must-revalidate"
        resp.headers["Pragma"] = "no-cache"
    return resp

_machine = None
_engine = None
_engine_lock = threading.Lock()   # мотор — один синглтон, шагаем по одному запросу


def machine():
    global _machine
    if _machine is None:
        _machine = Machine(ROM_PATH, rom_base=ROM_BASE)
    return _machine


def active_profile():
    """Определить вариант прошивки (M30/J30) по reset-вектору загруженного ROM."""
    reset = machine().peek16(0xFFFE)
    name, prof = symbols.resolve(reset)
    return name, prof


def engine_machine():
    """Отдельный заведённый экземпляр для живого мотора (крутится постоянно)."""
    global _engine
    if _engine is None:
        _engine = Machine(ROM_PATH, rom_base=ROM_BASE)
        _engine.start_engine()
    return _engine


# ---------- модели запросов ----------
class VarIn(BaseModel):
    addr: int
    size: int = 8
    value: int


class WatchIn(BaseModel):
    name: str
    addr: int
    size: int = 8


class RunReq(BaseModel):
    routine_addr: int
    inputs: List[VarIn] = []
    watch: List[WatchIn] = []
    max_steps: int = 200000
    trace: bool = False
    iterations: int = 8


class SweepReq(BaseModel):
    routine_addr: int
    sweep_addr: int
    sweep_size: int = 16
    start: int
    stop: int
    step: int = 1
    inputs: List[VarIn] = []          # базовые (постоянные) входы
    watch: List[WatchIn] = []
    max_steps: int = 200000
    iterations: int = 8


# ---------- эндпоинты ----------
class StateReq(BaseModel):
    inputs: List[VarIn] = []
    iterations: int = 6


@app.get("/api/meta")
def meta():
    name, prof = active_profile()
    return {
        "inputs": symbols.INPUTS,
        "watch": symbols.WATCH,
        "flags": symbols.FLAGS,
        "routines": prof["routines"],      # точки входа выбранного варианта
        "tables": symbols.TABLES,
        "rom_base": ROM_BASE,
        "variant": name,                    # M30 / J30 / UNKNOWN
        "variant_desc": prof.get("desc", ""),
        "engine_plant": prof.get("engine_plant", False),
    }


class EngineReq(BaseModel):
    gas: int = 0          # ГАЗ/педаль в % (0 = отпущен, ХХ). Обороты — ВЫХОД.
    coolant: int = 80     # темп. ОЖ в °C (ползунок, прогретый по умолчанию)
    airtemp: int = 20     # темп. воздуха в °C (ползунок)
    screw: int = 6800     # ВИНТ ХХ: базовый воздух обвода (ползунок).
    ignition: bool = False  # ЗАЖИГАНИЕ (ключ): OFF -> ЭБУ не льёт -> мотор глохнет.
    starter: bool = False   # СТАРТЕР: крутит мотор для запуска.
    load: int = 0         # ДОРОЖНАЯ НАГРУЗКА в % (0 = нейтраль, 100 = тяжело/в гору)
    ticks: int = 12       # шагов физики за кадр (плавность)


def celsius_to_raw(c):
    """°C -> сырьё датчика ($1424/$1489). Термистор: тёплый -> низкое сырьё.
    Приближённо (точная тарировка не критична — блоки прогрева пока не активны)."""
    return max(20, min(255, round(240 - c * 1.6)))


# именованные соленоиды/выходы (бит -> имя). Активность сверена опытом по режимам:
# $A7.0x10/0x80/0x04 и $A8.0x01 вспыхивают на РЕЗКОМ газу (обогащение разгона);
# $A9.0x10 (EGR) пока не срабатывает; $AB.0x10 постоянно; $AE/$59/$9B меняются вне ХХ.
OUTPUTS = {
    # обогащение разгона (резкое открытие газа) — подтверждено: клапан мощности
    "Клапан мощности (обогащ. разгона A7.0x10)": {"addr": 0x00A7, "mask": 0x10},
    "Обогащ. разгона (A7.0x80)":  {"addr": 0x00A7, "mask": 0x80},
    "Обогащ. разгона (A7.0x04)":  {"addr": 0x00A7, "mask": 0x04},
    "Соленоид резк. газа (A8.0x01)": {"addr": 0x00A8, "mask": 0x01},
    # EGR
    "EGR (A9.0x10)":             {"addr": 0x00A9, "mask": 0x10},
    # реле/режимы
    "Низкие об./ХХ-реле (AB.0x10)": {"addr": 0x00AB, "mask": 0x10},
    # выходы/флаги, которые меняются по режимам — назначение ещё опознаём по поведению
    "Выход AE.0x10 (опознать)":  {"addr": 0x00AE, "mask": 0x10},
    "Выход AE.0x20 (опознать)":  {"addr": 0x00AE, "mask": 0x20},
    "Флаг 59.0x08 (опознать)":   {"addr": 0x0059, "mask": 0x08},
    "Флаг 9B.0x08 (опознать)":   {"addr": 0x009B, "mask": 0x08},
    "Флаг D4.0x01 (опознать)":   {"addr": 0x00D4, "mask": 0x01},
}


@app.post("/api/engine")
def engine(req: EngineReq):
    """ЖИВОЙ МОТОР (плант-модель): жмёшь газ -> обороты раскручиваются сами."""
    global _engine

    name, prof = active_profile()
    if not prof.get("engine_plant", False):
        # Полный «живой мотор» завязан на M30-адреса планировщика/главного цикла
        # (0x83CE, 0x82A1 и т.д.). Для J30 эти адреса другие — engine_plant пока
        # не перепривязан. Рутинный уровень (/api/run, /api/sweep) для J30 работает.
        return {"state": None, "outputs": {},
                "notice": f"Живой мотор для варианта {name} ещё не привязан "
                          f"(нужны адреса планировщика/главного цикла J30). "
                          f"Рутины (/api/run, /api/sweep) работают."}

    def _step():
        em = engine_machine()
        return em, em.engine_plant_step(req.gas / 100.0,
                                        coolant=req.coolant,
                                        airtemp=req.airtemp,
                                        base_air=float(req.screw),
                                        ignition=req.ignition,
                                        starter=req.starter,
                                        road_load=req.load / 100.0,
                                        ticks=max(1, req.ticks))

    with _engine_lock:                 # сериализуем доступ — без гонки потоков
        try:
            em, st = _step()
        except Exception:
            # прошивка крэшнулась (прыжок в мусор) -> пересоздаём, панель не виснет
            _engine = None
            em, st = _step()
        outputs = {}
        for name, d in OUTPUTS.items():
            byte = em.peek8(d["addr"])
            outputs[name] = bool(byte & d["mask"])
    return {"state": st, "outputs": outputs}


@app.post("/api/state")
def state(req: StateReq):
    """Прогнать мини-цикл с входами и вернуть ВСЕ наблюдаемые + флаги (для панели)."""
    m = machine()
    _, prof = active_profile()
    info = m.run_chain([i.model_dump() for i in req.inputs],
                       prof["chain"], iterations=req.iterations)
    watch = {name: m.get_var(d["addr"], d.get("size", 8))
             for name, d in symbols.WATCH.items()}
    flags = {}
    for name, d in symbols.FLAGS.items():
        byte = m.peek8(d["addr"])
        flags[name] = {"on": bool(byte & d["mask"]), "byte": byte}
    return {"watch": watch, "flags": flags, "chain": info,
            "io_writes": [{"addr": a, "val": v} for a, v in m.bus.io_writes]}


@app.post("/api/run")
def run(req: RunReq):
    m = machine()
    info = m.run(
        req.routine_addr,
        [i.model_dump() for i in req.inputs],
        [w.model_dump() for w in req.watch],
        max_steps=req.max_steps,
        trace=req.trace,
        iterations=req.iterations,
    )
    if info.get("trace"):
        info["trace"] = [{"pc": pc, "op": op} for pc, op in info["trace"]]
    return info


@app.post("/api/sweep")
def sweep(req: SweepReq):
    m = machine()
    vals = list(range(req.start, req.stop + 1, max(1, req.step)))
    rows = m.sweep(
        req.routine_addr,
        req.sweep_addr,
        req.sweep_size,
        vals,
        [i.model_dump() for i in req.inputs],
        [w.model_dump() for w in req.watch],
        max_steps=req.max_steps,
        iterations=req.iterations,
    )
    return {"rows": rows, "count": len(rows)}


@app.get("/api/disasm")
def disasm(addr: int, n: int = 12):
    """Очень короткий дизасм для контекста (используем дизассемблер проекта если есть)."""
    m = machine()
    out = []
    p = addr
    for _ in range(n):
        b = m.peek8(p)
        out.append({"addr": p, "byte": b})
        p += 1
    return {"bytes": out}


# ---------- статика фронта ----------
@app.get("/")
def index():
    return FileResponse(os.path.join(FRONT_DIR, "index.html"))


@app.get("/mixmap")
def mixmap():
    """Редактор таблицы ЦН y30: слайс по дросселю + 3D всей таблицы."""
    return FileResponse(os.path.join(FRONT_DIR, "mixmap.html"))


@app.get("/editor")
def editor():
    """Редактор данных прошивки J30 (все данные интерпретированно/сырьём, сравнение,
    скачивание дампа с пересчётом чек-суммы). Автономная страница (ROM вшит)."""
    return FileResponse(os.path.join(FRONT_DIR, "editor.html"))


@app.get("/api/pcn")
def get_pcn():
    """Отдать таблицу ЦН из pcn_data.json — читаем с диска каждый раз, чтобы правки были видны сразу."""
    with open(PCN_PATH, encoding="utf-8") as f:
        return json.load(f)


@app.get("/api/bcn")
def get_bcn():
    """Отдать таблицу БЦН из bcn_data.json (синий=сток, зелёный=факт из логов, красный=достроено)."""
    with open(BCN_PATH, encoding="utf-8") as f:
        return json.load(f)


@app.get("/api/dad")
def get_dad():
    """Отдать ПЦН по давлению (ДАД): зелёный=измерено логами, красный=достроено/экстраполяция."""
    with open(DAD_PATH, encoding="utf-8") as f:
        return json.load(f)


class DadEdit(BaseModel):
    pi: int      # индекс давления (строка)
    xi: int      # индекс оборотов (столбец)
    val: float


@app.post("/api/dad")
def set_dad(e: DadEdit):
    """Записать одну ячейку ПЦН-ДАД обратно в dad_data.json (правка мышью из UI)."""
    with _edit_lock:                      # читаем-меняем-пишем без гонки
        with open(DAD_PATH, encoding="utf-8") as f:
            d = json.load(f)
        d["z"][e.pi][e.xi] = e.val
        if "hand" not in d:               # отметка «правил руками» — отдельный слой/цвет
            d["hand"] = [[False] * len(d["z"][0]) for _ in range(len(d["z"]))]
        d["hand"][e.pi][e.xi] = True
        _atomic_write(DAD_PATH, d)
    return {"ok": True, "pi": e.pi, "xi": e.xi, "val": e.val}


class PcnEdit(BaseModel):
    ti: int              # индекс дросселя (строка)
    xi: int              # индекс оборотов (столбец)
    val: float
    arr: str = "z"       # какой слой правим: z / zred / z5k / zbase


@app.post("/api/pcn")
def set_pcn(e: PcnEdit):
    """Записать одну ячейку выбранного слоя обратно в pcn_data.json (правка из UI)."""
    arr = e.arr if e.arr in ("z", "zred", "z5k", "zbase", "zsurf") else "z"
    with _edit_lock:                      # читаем-меняем-пишем без гонки
        with open(PCN_PATH, encoding="utf-8") as f:
            d = json.load(f)
        d[arr][e.ti][e.xi] = e.val
        if "hand" not in d:               # отметка «правил руками» — отдельный слой/цвет
            d["hand"] = [[False] * len(d["z"][0]) for _ in range(len(d["z"]))]
        d["hand"][e.ti][e.xi] = True
        _atomic_write(PCN_PATH, d)
    return {"ok": True, "ti": e.ti, "xi": e.xi, "val": e.val, "arr": arr}


if os.path.isdir(FRONT_DIR):
    app.mount("/static", StaticFiles(directory=FRONT_DIR), name="static")
