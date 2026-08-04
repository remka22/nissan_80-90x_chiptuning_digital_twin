# -*- coding: utf-8 -*-
"""Есть ли вообще ОЗУ по адресу: пишем и читаем ТОТ ЖЕ адрес (как старый промер),
но с контролем — сначала проверяем, что механизм poke вообще работает (на заведомо живом $16xx)."""
import serial, time
PORT="/dev/cu.usbserial-A5069RR4"; BAUD=15625
ser=serial.Serial(PORT,BAUD,timeout=0.2); buf=bytearray(); frames=[]
def pump(sec):
    t0=time.time()
    while time.time()-t0<sec:
        c=ser.read(256)
        if c:
            buf.extend(c); i=0
            while i<len(buf)-5:
                if buf[i]==0xAE and buf[i+1]==0x17:
                    ln=buf[i+4]; end=i+5+ln
                    if end>=len(buf): break
                    chk=0
                    for b in buf[i+2:end]: chk^=b
                    if chk==buf[end]: frames.append(bytes(buf[i+5:end])); i=end+1; continue
                i+=1
            del buf[:i]
        time.sleep(0.01)
def cmd(bs):
    for b in bs: ser.write(bytes([b])); ser.flush(); time.sleep(0.03)
pump(2.0)
IDX=len(frames[-1])-1
def fresh(n=2):
    k=len(frames); t0=time.time()
    while len(frames)-k<n and time.time()-t0<4: pump(0.1)
    return frames[-1][IDX] if frames else None
def poke(a,v): cmd([0xC5,a>>8,a&0xFF,v])
def peek(a):
    cmd([0xC6,a>>8,a&0xFF]); return fresh(2)

print("=== КОНТРОЛЬ: работает ли poke вообще (пишем в заведомо живой $16A0) ===")
for v in (0x5A,0xA5):
    poke(0x16A0,v); time.sleep(0.2); g=peek(0x16A0)
    print("  пишу $16A0 = %02X → читаю = %s  %s"%(v,("%02X"%g) if g is not None else "нет",
          "OK" if g==v else "НЕ ЗАПИСАЛОСЬ"))
print()
print("=== ПРОВЕРКА: есть ли память выше $17FF (пишем и читаем ТОТ ЖЕ адрес) ===")
for a in (0x1800,0x1900,0x1A00,0x1AB0,0x1F00):
    r=[]
    for v in (0x5A,0xA5):
        poke(a,v); time.sleep(0.2); g=peek(a); r.append(g)
    ok = (r[0]==0x5A and r[1]==0xA5)
    print("  $%04X: записал 5A→прочитал %s, записал A5→прочитал %s   %s"
          %(a,("%02X"%r[0]) if r[0] is not None else "нет",("%02X"%r[1]) if r[1] is not None else "нет",
            "ПАМЯТЬ ЕСТЬ" if ok else "ПАМЯТИ НЕТ"))
print()
print("=== для сравнения: заведомо живое ОЗУ \$1400-\$17FF ===")
for a in (0x1650,0x1700,0x17F0):
    g=peek(a); print("  $%04X читается как %s"%(a,("%02X"%g) if g is not None else "нет"))
ser.close()
