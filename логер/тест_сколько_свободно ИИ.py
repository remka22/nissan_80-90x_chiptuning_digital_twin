# -*- coding: utf-8 -*-
"""Сколько байт ОЗУ реально свободно: ставим метки, ждём, читаем.
Уцелела метка = завод туда не пишет. Затёрлась = занято."""
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
pump(2.0); IDX=len(frames[-1])-1
def peek(a):
    cmd([0xC6,a>>8,a&0xFF]); k=len(frames); t0=time.time()
    while len(frames)-k<2 and time.time()-t0<4: pump(0.1)
    return frames[-1][IDX]
def poke(a,v): cmd([0xC5,a>>8,a&0xFF,v])

# метки: адрес -> уникальное значение
probe=[]
for a in range(0x1600,0x1700,0x10): probe.append(a)     # буфер загрузчика, 16 точек
for a in range(0x1780,0x1800,0x10): probe.append(a)     # хвост после таблицы обучения, 8 точек
marks={a:(0x40+i) for i,a in enumerate(probe)}

print("ставлю %d меток..."%len(probe))
for a,v in marks.items(): poke(a,v)
print("жду 12 секунд с работающим блоком...")
time.sleep(12)
print()
ok=[]; bad=[]
for a,v in marks.items():
    g=peek(a)
    (ok if g==v else bad).append((a,v,g))
    print("  $%04X: ставил %02X → сейчас %02X   %s"%(a,v,g,"цело" if g==v else "ЗАТЁРТО"))
print()
print("уцелело %d из %d"%(len(ok),len(marks)))
if bad: print("затёрты:", ", ".join("$%04X"%a for a,_,_ in bad))
ser.close()
