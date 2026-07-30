# -*- coding: utf-8 -*-
"""
Билдер ДАД speed-density патча. Вшивает в бин (обычно тот, где уже логгер/дампер):
  - рутину @ C700, которая замещает расчёт Tp: Тр = КМ·Д·VE[обороты][давление];
  - VE-карту 16×16 @ C900 (256 б, номинал 0x80=1.0);
  - ось давления @ CA00 (16 б, в единицах Д=сырьё−Смещ);
  - Смещ @ CA10, КМ @ CA11.
Врезка: 89d8 JSR $8057 -> JSR C700.
$80CF переиспользуем (ось оборотов родная $FB20). Нюанс $1482 обходим temp-swap.
Гейт пуска по оборотам ($140A<31 -> родной $8057). Чек-сумма пересчитывается.

Значения VE/оси/Смещ/КМ — СТАРТОВЫЕ (номинал), тюнятся по AFR. Смещ=26 (0.5В),
КМ=128 (=×1.0, нетто 0.5 от старшего байта).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) >= 2 else os.path.join(
    HERE, "..", "j30", "J30_логгер-дамп 29.07.26 ИИ.bin")
DST = sys.argv[2] if len(sys.argv) >= 3 else os.path.join(
    HERE, "J30_логгер+дад 29.07.26 ИИ.bin")
ROM_BASE = 0x8000

ROUT = 0xC700          # рутина
VEMAP = 0xC900         # VE 16×16 (256 б)
PAXIS = 0xCA00         # ось давления (16 б, в кПа)
SMESH = 0xCA10         # Смещ (ноль датчика)
NAKL  = 0xCA11         # Наклон (рядом со Смещением) — кПа/отсчёт ×256; 125 для 0-100кПа/0.5-4.5В
KM    = 0xCA12         # КМ (масштаб)
HOOK  = 0x89D8         # JSR $8057 -> JSR ROUT
RPMGATE = 0x1F         # порог пуска (обороты raw ~31 ≈ 400об/мин)

# --- программа рутины (метка|None, токен, операнд) ---
PROG = [
    (None,"LDDe",0x140A),               # обороты
    (None,"SUBD#",RPMGATE),
    (None,"BCC","RUN"),                 # >= порога -> speed-density
    (None,"JSRe",0x8057),               # пуск -> родное деление
    (None,"RTS",None),
    # --- прочитать MAP (ch0), Д=(raw>>2)-Смещ ---
    ("RUN","LDAB#",0x00),
    (None,"JSRe",0xB209),               # D = 10-бит MAP
    (None,"LSRD",None),
    (None,"LSRD",None),                 # D>>2, B=8-бит
    (None,"SUBBe",SMESH),               # B = raw>>2 - Смещ
    (None,"BCC","DOK"),
    (None,"CLRB",None),                 # underflow -> 0
    ("DOK","STABd",0xF7),               # $F7 = Д (сырьё−Смещ)
    # --- Д в кПа: Д = (Д × наклон) >> 8 ---
    (None,"LDAAd",0xF7),
    (None,"LDABe",NAKL),
    (None,"MUL",None),                  # A = старший = Д в кПа
    (None,"STAAd",0xF7),
    # --- save $1482 и $7d, положить давление (кПа) в $1482 ---
    (None,"LDXe",0x1482),
    (None,"STXd",0xF4),                 # $F4:$F5 = old $1482
    (None,"LDAAd",0x7D),
    (None,"STAAd",0xF6),                # $F6 = old $7d
    (None,"CLRA",None),
    (None,"LDABd",0xF7),                # B = Д, A=0
    (None,"STDe",0x1482),               # $1482 = 00:Д
    (None,"LDAAd",0x7D),
    (None,"ANDA#",0x1F),
    (None,"ORAA#",0x14),
    (None,"STAAd",0x7D),                # $7d = (old&1f)|14  (бит6 сброшен)
    # --- указатели + вызов $80CF ---
    (None,"LDX#",VEMAP),
    (None,"STXd",0x74),
    (None,"LDX#",0xFB20),               # ось оборотов родная
    (None,"STXd",0x76),
    (None,"LDX#",PAXIS),
    (None,"STXd",0x78),
    (None,"JSRe",0x80CF),               # A = VE
    (None,"STAAd",0xF8),                # $F8 = VE
    # --- restore $7d и $1482 ---
    (None,"LDAAd",0xF6),
    (None,"STAAd",0x7D),
    (None,"LDXd",0xF4),
    (None,"STXe",0x1482),
    # --- Тр = старший(Д×VE) × КМ ---
    (None,"LDAAd",0xF8),                # A = VE
    (None,"LDABd",0xF7),                # B = Д
    (None,"MUL",None),                  # D=Д×VE
    (None,"ASLD",None),                 # компенсация масштаба кПа (Д×VE >>7)
    (None,"LDABe",KM),                  # B = КМ
    (None,"MUL",None),                  # A(база)×КМ -> D
    (None,"ASLD",None),                 # >>7 нетто -> A = Тр (КМ=128 -> база)
    (None,"TAB",None),                  # B = Тр
    (None,"CLRA",None),                 # A = 0
    (None,"RTS",None),                  # D = 00:Тр
]

LEN={"LDDe":3,"SUBD#":3,"BCC":2,"JSRe":3,"RTS":1,"LDAB#":2,"LSRD":1,"SUBBe":3,
     "CLRB":1,"STABd":2,"LDXe":3,"STXd":2,"LDAAd":2,"STAAd":2,"CLRA":1,"LDABd":2,
     "STDe":3,"ANDA#":2,"ORAA#":2,"LDX#":3,"JSRe":3,"LDXd":2,"STXe":3,"MUL":1,
     "LDABe":3,"ASLD":1,"TAB":1}
OP1={"RTS":0x39,"LSRD":0x04,"CLRB":0x5F,"CLRA":0x4F,"MUL":0x3D,"ASLD":0x05,"TAB":0x16}

def asm(org):
    lab={}; pc=org
    for l,op,a in PROG:
        if l: lab[l]=pc
        pc+=LEN[op]
    out=bytearray(); pc=org
    for l,op,a in PROG:
        nx=pc+LEN[op]
        if   op=="LDDe":  out+=bytes([0xFC,a>>8,a&0xFF])
        elif op=="SUBD#": out+=bytes([0x83,a>>8,a&0xFF])
        elif op=="BCC":
            r=lab[a]-nx; assert -128<=r<=127,("BCC %s %d"%(a,r)); out+=bytes([0x24,r&0xFF])
        elif op=="JSRe":  out+=bytes([0xBD,a>>8,a&0xFF])
        elif op=="LDAB#": out+=bytes([0xC6,a&0xFF])
        elif op=="SUBBe": out+=bytes([0xF0,a>>8,a&0xFF])
        elif op=="STABd": out+=bytes([0xD7,a&0xFF])
        elif op=="LDXe":  out+=bytes([0xFE,a>>8,a&0xFF])
        elif op=="STXd":  out+=bytes([0xDF,a&0xFF])
        elif op=="STXe":  out+=bytes([0xFF,a>>8,a&0xFF])
        elif op=="LDXd":  out+=bytes([0xDE,a&0xFF])
        elif op=="LDAAd": out+=bytes([0x96,a&0xFF])
        elif op=="STAAd": out+=bytes([0x97,a&0xFF])
        elif op=="LDABd": out+=bytes([0xD6,a&0xFF])
        elif op=="LDABe": out+=bytes([0xF6,a>>8,a&0xFF])
        elif op=="STDe":  out+=bytes([0xFD,a>>8,a&0xFF])
        elif op=="ANDA#": out+=bytes([0x84,a&0xFF])
        elif op=="ORAA#": out+=bytes([0x8A,a&0xFF])
        elif op=="LDX#":  out+=bytes([0xCE,a>>8,a&0xFF])
        elif op in OP1:   out+=bytes([OP1[op]])
        else: raise ValueError(op)
        pc=nx
    return out,lab

def main():
    rom=bytearray(open(SRC,"rb").read()); assert len(rom)==32768
    code,lab=asm(ROUT)
    # проверить свободное место под рутину и данные
    for a,n in [(ROUT,len(code)),(VEMAP,256),(PAXIS,16),(SMESH,1),(KM,1),(NAKL,1)]:
        off=a-ROM_BASE
        assert all(b==0x3F for b in rom[off:off+n]),"не пусто @ %04X"%a
    # проверить врезку
    ho=HOOK-ROM_BASE
    assert rom[ho]==0xBD and (rom[ho+1]<<8|rom[ho+2])==0x8057,"по 89D8 не JSR $8057"
    # вставить рутину
    rom[ROUT-ROM_BASE:ROUT-ROM_BASE+len(code)]=code
    # данные: VE номинал 0x80(=1.0), ось давления в кПа (атмо 20-110), Смещ=26, КМ=128, наклон=125
    for i in range(256): rom[VEMAP-ROM_BASE+i]=0x80
    paxis=[20,26,32,38,44,50,56,62,68,74,80,86,92,98,104,110]   # кПа
    for i,v in enumerate(paxis): rom[PAXIS-ROM_BASE+i]=v
    rom[SMESH-ROM_BASE]=26
    rom[KM-ROM_BASE]=128
    rom[NAKL-ROM_BASE]=125
    # врезка
    rom[ho+1],rom[ho+2]=ROUT>>8,ROUT&0xFF
    # чек-сумма
    s=x=0
    for i in range(len(rom)):
        if i in (0x7F7A,0x7F7B): continue
        s=(s+rom[i])&0xFF; x^=rom[i]
    rom[0x7F7A],rom[0x7F7B]=s,x
    open(DST,"wb").write(rom)
    print("Готово:",os.path.basename(DST))
    print("  рутина %d байт @ %04X..%04X"%(len(code),ROUT,ROUT+len(code)-1))
    print("  метки:",{k:"%04X"%v for k,v in lab.items()})
    print("  VE @ C900 (256, 0x80), ось @ CA00, Смещ=26 @ CA10, КМ=128 @ CA11")
    print("  врезка 89D8: JSR 8057 -> JSR %04X"%ROUT)
    print("  чек-сумма: 0x%02X/0x%02X"%(s,x))

if __name__=="__main__": main()
