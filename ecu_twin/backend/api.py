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
    return {
        "inputs": symbols.INPUTS,
        "watch": symbols.WATCH,
        "flags": symbols.FLAGS,
        "routines": symbols.ROUTINES,
        "tables": symbols.TABLES,
        "rom_base": ROM_BASE,
    }


class EngineReq(BaseModel):
    gas: int = 0          # ГАЗ/педаль в % (0 = отпущен, ХХ). Обороты — ВЫХОД.
    coolant: int = 80     # темп. ОЖ в °C (ползунок, прогретый по умолчанию)
    airtemp: int = 20     # темп. воздуха в °C (ползунок)
    screw: int = 4000     # ВИНТ ХХ: базовый воздух обвода (ползунок).
    ignition: bool = False  # ЗАЖИГАНИЕ (ключ): OFF -> ЭБУ не льёт -> мотор глохнет.
    starter: bool = False   # СТАРТЕР: крутит мотор для запуска.
    ticks: int = 12       # шагов физики за кадр (плавность)


def celsius_to_raw(c):
    """°C -> сырьё датчика ($1424/$1489). Термистор: тёплый -> низкое сырьё.
    Приближённо (точная тарировка не критична — блоки прогрева пока не активны)."""
    return max(20, min(255, round(240 - c * 1.6)))


# именованные соленоиды/выходы (бит -> человеческое имя)
OUTPUTS = {
    "EGR (A9.0x10)":         {"addr": 0x00A9, "mask": 0x10},
    "Клапан мощности (A7.0x10)": {"addr": 0x00A7, "mask": 0x10},
    "Низкие об./ХХ-реле (AB.0x10)": {"addr": 0x00AB, "mask": 0x10},
}


@app.post("/api/engine")
def engine(req: EngineReq):
    """ЖИВОЙ МОТОР (плант-модель): жмёшь газ -> обороты раскручиваются сами."""
    global _engine

    def _step():
        em = engine_machine()
        return em, em.engine_plant_step(req.gas / 100.0,
                                        coolant=req.coolant,
                                        airtemp=req.airtemp,
                                        base_air=float(req.screw),
                                        ignition=req.ignition,
                                        starter=req.starter,
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
    info = m.run_chain([i.model_dump() for i in req.inputs],
                       symbols.CHAIN, iterations=req.iterations)
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


if os.path.isdir(FRONT_DIR):
    app.mount("/static", StaticFiles(directory=FRONT_DIR), name="static")
