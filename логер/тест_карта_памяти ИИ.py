# -*- coding: utf-8 -*-
"""Карта памяти: ТОЛЬКО ЧТЕНИЕ. Сверяем пары адресов на зеркало со сдвигом $0800."""
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
print("ЗЕРКАЛО СО СДВИГОМ $0800 — сверяем пары (только чтение):")
pairs=[(0x1C00,0x1400),(0x1C08,0x1408),(0x1D00,0x1500),(0x1E50,0x1650),(0x1EA0,0x16A0),(0x1F00,0x1700),(0x1FF0,0x17F0)]
same=0
for hi,lo in pairs:
    a=peek(hi); b=peek(lo)
    eq = (a==b)
    same += eq
    print("  $%04X = %02X   $%04X = %02X   %s"%(hi,a,lo,b,"совпало" if eq else "РАЗНОЕ"))
print()
print("МЁРТВАЯ ЗОНА — что читается (должно быть FF если там ничего):")
for a in (0x1800,0x1850,0x1900,0x1A00,0x1B00,0x1BFF):
    print("  $%04X = %02X"%(a,peek(a)))
print()
print("ЖИВЫЕ переменные мотора — блок в порядке?")
for a,n in ((0x140A,"обороты hi"),(0x1408,"расходомер hi"),(0x004C,"темп ОЖ"),(0x1411,"впрыск hi")):
    print("  $%04X %-16s = %02X"%(a,n,peek(a)))
print()
print("совпало пар: %d из %d"%(same,len(pairs)))
ser.close()
