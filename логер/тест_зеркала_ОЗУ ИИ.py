# -*- coding: utf-8 -*-
"""Перекрёстный тест ОЗУ: одна ли это память по адресам $1Axx и $16xx.
Прошивка: v3 (poke/peek). Пишем по одному адресу — читаем по ДРУГОМУ.
Байты команд с паузой 30мс: v3 опрашивает приём раз за проход, подряд теряет."""
import serial, time, sys

PORT = "/dev/cu.usbserial-A5069RR4"; BAUD = 15625
ser = serial.Serial(PORT, BAUD, timeout=0.2)
buf = bytearray(); frames = []

def pump(sec):
    t0 = time.time()
    while time.time() - t0 < sec:
        c = ser.read(256)
        if c:
            buf.extend(c)
            i = 0
            while i < len(buf) - 5:
                if buf[i] == 0xAE and buf[i+1] == 0x17:
                    ln = buf[i+4]; end = i + 5 + ln
                    if end >= len(buf): break
                    chk = 0
                    for b in buf[i+2:end]: chk ^= b
                    if chk == buf[end]:
                        frames.append(bytes(buf[i+5:end])); i = end + 1; continue
                i += 1
            del buf[:i]
        time.sleep(0.01)

def cmd(bs):
    for b in bs:
        ser.write(bytes([b])); ser.flush(); time.sleep(0.03)

def fresh(n=2):
    k = len(frames); t0 = time.time()
    while len(frames) - k < n and time.time() - t0 < 4: pump(0.1)
    return frames[-1] if frames else None

print("слушаю 3 с...")
pump(3.0)
print("кадров: %d" % len(frames))
if not frames:
    print("КАДРОВ НЕТ — v3 не отвечает, тест невозможен"); ser.close(); sys.exit(1)
print("длина кадра: %d байт данных" % len(frames[-1]))
PEEK_IDX = len(frames[-1]) - 1          # ячейка peek ($1600) — последняя в кадре v3
print("ячейка peek = позиция %d" % PEEK_IDX)

def poke(a, v): cmd([0xC5, a >> 8, a & 0xFF, v])
def peek(a):
    cmd([0xC6, a >> 8, a & 0xFF]); f = fresh(2)
    return f[PEEK_IDX] if f else None

print()
tests = [("ПРЯМОЙ  ", 0x1A01, 0x5A, 0x1601),
         ("КОНТРОЛЬ", 0x1A02, 0xA5, 0x1602),
         ("ОБРАТНЫЙ", 0x1602, 0x33, 0x1A02)]
res = []
for name, wa, wv, ra in tests:
    poke(wa, wv); time.sleep(0.2)
    got = peek(ra)
    ok = (got == wv)
    res.append(ok)
    print("%s  пишу $%04X = %02X  →  читаю $%04X = %s   %s"
          % (name, wa, wv, ra, ("%02X" % got) if got is not None else "нет ответа",
             "СОВПАЛО" if ok else "не совпало"))

print()
print("контроль: читаю адрес, куда НЕ писали")
c = peek(0x1650); print("  $1650 = %s" % (("%02X" % c) if c is not None else "нет ответа"))
print()
if all(res): print("ВЫВОД: ЗЕРКАЛО. $1Axx и $16xx — одна и та же память.")
elif not any(res): print("ВЫВОД: зеркала НЕТ, память раздельная.")
else: print("ВЫВОД: неоднозначно, часть тестов совпала — смотреть детали.")
ser.close()
