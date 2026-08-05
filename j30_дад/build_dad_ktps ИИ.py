# -*- coding: utf-8 -*-
"""
ДАД speed-density + ПОПРАВКА ПО ДРОССЕЛЮ (Ktps). Расширение build_dad_patch:
  Наполнение Тр = КМ · Д · VE[обороты×давление] · Ktps[обороты×TPS%]
  (VE и Ktps ПЕРЕМНОЖАЮТСЯ — как в январе поправки по дросселю и давлению).

Рутина @ C700: два lookup через штатный $80CF.
  1) VE   @ C900, ось давл @ CA00 (kPa), Смещ CA10, наклон CA11, КМ CA12  (как ДАД).
  2) Ktps @ CB00 (16×16, 0x80=1.0), ось TPS @ CC00 (в единицах $14A2 = открытие от закрытого).
Индекс Ktps: обороты $140A × открытие дросселя $14A2 (не сырой АЦП — от выученного нуля).
Ось TPS = январская шкала дросселя (неравномерная, гуще на малом газу), пересчитанная в
$14A2 (полный газ ≈ 172 = span 344/2). В редакторе показывается в % (январские значения).

Врезка 89D8: JSR $8057 -> JSR C700. База — бин с K412 (последний). Чек-сумма пересчитывается.
TPS-патч тарировки НЕ нужен (используем $14A2 от обучения + span).
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) >= 2 else os.path.join(HERE, "..", "логер", "J30_v8plus2_k412_l095_02.08.26 ИИ.bin")
DST = sys.argv[2] if len(sys.argv) >= 3 else os.path.join(HERE, "..", "логер", "J30_дад+ktps_k412_02.08.26 ИИ.bin")
ROM_BASE = 0x8000

ROUT   = 0xC700
VEMAP  = 0xC900
PAXIS  = 0xCA00
SMESH  = 0xCA10
NAKL   = 0xCA11
KM     = 0xCA12
KTPS   = 0xCB00      # карта Ktps 16×16
TAXIS  = 0xCC00      # ось TPS (в единицах $14A2)
SPAN   = 0xCC10      # span дросселя закрыт→полный, в $14A2 (172 = 344 в $1492); справочно/для осей
HOOK   = 0x89D8
RPMGATE = 0x1F

# УКАЗАТЕЛИ КАРТ в zero-page — общие с build_targeted_patch (живой тюнинг).
# Рутина берёт базу карты НЕ константой, а из указателя: тогда панель может увести
# карту на тень $1600 и править её на ходу. Значения в указатели кладёт живой патч
# (MYPTR/MYINIT ставят ПЗУ, команда CB переключает). Адреса ОБЯЗАНЫ совпадать с
# PTR_VE/PTR_KT в build_targeted_patch ИИ.py — там стоит встречная проверка.
PTR_VE = 0x00D3        # указатель карты VE   ($C9 = ПЗУ, $16 = тень)
PTR_KT = 0x00D5        # указатель карты Ktps ($CB = ПЗУ, $16 = тень)

# январская ось дросселя, % (thr из pcn/dad): гуще на низах
THR_PCT = [0, 2, 4, 6, 8, 10, 14, 18, 23, 29, 37, 46, 56, 66, 80, 100]
# в единицах $14A2 (полный газ 100% = 172): %×1.72, монотонно
TAXIS_VAL = [min(255, round(p * 172 / 100)) for p in THR_PCT]

PROG = [
    (None,"LDDe",0x140A),(None,"SUBD#",RPMGATE),(None,"BCC","RUN"),
    (None,"JSRe",0x8057),(None,"RTS",None),
    # --- Д (давление) из MAF-канала ---
    ("RUN","LDAB#",0x00),(None,"JSRe",0xB209),(None,"LSRD",None),(None,"LSRD",None),
    (None,"SUBBe",SMESH),(None,"BCC","DOK"),(None,"CLRB",None),
    ("DOK","STABd",0xF7),
    (None,"LDAAd",0xF7),(None,"LDABe",NAKL),(None,"MUL",None),(None,"STAAd",0xF7),  # Д в kPa → $F7
    # --- lookup VE по обороты × давление ---
    (None,"LDXe",0x1482),(None,"STXd",0xF4),(None,"LDAAd",0x7D),(None,"STAAd",0xF6),
    (None,"CLRA",None),(None,"LDABd",0xF7),(None,"STDe",0x1482),
    (None,"LDAAd",0x7D),(None,"ANDA#",0x1F),(None,"ORAA#",0x14),(None,"STAAd",0x7D),
    (None,"LDXd",PTR_VE),(None,"STXd",0x74),   # база VE — ИЗ УКАЗАТЕЛЯ (ПЗУ или тень)
    (None,"LDX#",0xFB20),(None,"STXd",0x76),
    (None,"LDX#",PAXIS),(None,"STXd",0x78),
    (None,"JSRe",0x80CF),(None,"STAAd",0xF8),  # $F8 = VE
    (None,"LDAAd",0xF6),(None,"STAAd",0x7D),(None,"LDXd",0xF4),(None,"STXe",0x1482),
    # --- lookup Ktps по обороты × TPS ($14A2) ---
    (None,"LDXe",0x1482),(None,"STXd",0xF4),(None,"LDAAd",0x7D),(None,"STAAd",0xF6),
    (None,"CLRA",None),(None,"LDABe",0x14A2),(None,"STDe",0x1482),   # $1482 = 00:$14A2
    (None,"LDAAd",0x7D),(None,"ANDA#",0x1F),(None,"ORAA#",0x14),(None,"STAAd",0x7D),
    (None,"LDXd",PTR_KT),(None,"STXd",0x74),   # база Ktps — ИЗ УКАЗАТЕЛЯ (ПЗУ или тень)
    (None,"LDX#",0xFB20),(None,"STXd",0x76),
    (None,"LDX#",TAXIS),(None,"STXd",0x78),
    (None,"JSRe",0x80CF),(None,"STAAd",0xF9),  # $F9 = Ktps
    (None,"LDAAd",0xF6),(None,"STAAd",0x7D),(None,"LDXd",0xF4),(None,"STXe",0x1482),
    # --- Тр = ((Д×VE)>>7 × Ktps)>>7 × КМ >>7 ---
    (None,"LDAAd",0xF8),(None,"LDABd",0xF7),(None,"MUL",None),(None,"ASLD",None),   # A=Д×VE
    (None,"LDABd",0xF9),(None,"MUL",None),(None,"ASLD",None),                       # × Ktps
    (None,"LDABe",KM),(None,"MUL",None),(None,"ASLD",None),                         # × КМ
    (None,"TAB",None),(None,"CLRA",None),(None,"RTS",None),
]

LEN={"LDDe":3,"SUBD#":3,"BCC":2,"JSRe":3,"RTS":1,"LDAB#":2,"LSRD":1,"SUBBe":3,
     "CLRB":1,"STABd":2,"LDXe":3,"STXd":2,"LDAAd":2,"STAAd":2,"CLRA":1,"LDABd":2,
     "STDe":3,"ANDA#":2,"ORAA#":2,"LDX#":3,"LDXd":2,"STXe":3,"MUL":1,
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
    off=lambda a:a-ROM_BASE
    code,lab=asm(ROUT)
    # свободно под рутину и данные
    for a,n in [(ROUT,len(code)),(VEMAP,256),(PAXIS,16),(SMESH,1),(KM,1),(NAKL,1),(KTPS,256),(TAXIS,16),(SPAN,1)]:
        assert all(b==0x3F for b in rom[off(a):off(a)+n]),"не пусто @ %04X"%a
    # врезка
    ho=off(HOOK)
    assert rom[ho]==0xBD and (rom[ho+1]<<8|rom[ho+2])==0x8057,"по 89D8 не JSR 8057"
    rom[off(ROUT):off(ROUT)+len(code)]=code
    # данные ДАД (номинал)
    for i in range(256): rom[off(VEMAP)+i]=0x80
    for i,v in enumerate([20,26,32,38,44,50,56,62,68,74,80,86,92,98,104,110]): rom[off(PAXIS)+i]=v
    rom[off(SMESH)]=26; rom[off(KM)]=128; rom[off(NAKL)]=125
    # данные Ktps: карта 0x80 (=1.0, без поправки), ось TPS из января
    for i in range(256): rom[off(KTPS)+i]=0x80
    for i,v in enumerate(TAXIS_VAL): rom[off(TAXIS)+i]=v
    rom[off(SPAN)]=172        # span полного газа в $14A2 (=344 в $1492)
    # врезка адреса
    rom[ho+1],rom[ho+2]=ROUT>>8,ROUT&0xFF
    # чек-сумма
    s=x=0
    for i in range(len(rom)):
        if i in (0x7F7A,0x7F7B): continue
        s=(s+rom[i])&0xFF; x^=rom[i]
    rom[0x7F7A],rom[0x7F7B]=s,x
    open(DST,"wb").write(rom)
    print("Готово:",os.path.basename(DST))
    print("  рутина %d байт @ C700..%04X"%(len(code),ROUT+len(code)-1))
    print("  VE @ C900, ось давл @ CA00 | Ktps @ CB00, ось TPS @ CC00")
    print("  ось TPS в $14A2:",TAXIS_VAL)
    print("  чек-сумма: %02X/%02X"%(s,x))


if __name__=="__main__": main()
