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
MODE   = 0xCA13      # РЕЖИМ РАСЧЁТА: 0 = расходомер (заводской $8057), иначе = ДАД.
                     # Одна прошивка на оба случая — переключается этим байтом.
HOOK   = 0x89D8
# 0 = считаем по давлению С ПЕРВОГО ОБОРОТА.
# Было 0x1F (≈397 об) «на прокрутке speed-density считать нечего». Для мотора
# С РАСХОДОМЕРОМ это верно, но расходомера больше нет: ниже гейта управление
# уходило заводскому коду, а тот делит накопленный расход воздуха — и получал
# показания датчика давления вместо расхода. То есть ровно на прокрутке, когда
# мотор должен схватить, наполнение считалось по мусору. Мотор не заводился.
RPMGATE = 0x00

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

# ЗАЧЕМ ДВЕ ЧАСТИ.
# Врезка 89D8 сидит ВНУТРИ обработчика прерывания по метке коленвала — там же,
# где считаются моменты искры и впрыска. У него бюджет от 25 мс на холостом до
# 4 мс на 5000 об, и не уложиться нельзя.
# Раньше вся работа делалась там: чтение АЦП (а $B209 ЗАПРЕЩАЕТ ПРЕРЫВАНИЯ и ждёт
# железку в пустом цикле!) плюс два поиска по таблицам, внутри каждого по два
# деления. При гейте 0x1F это запускалось редко и проскакивало; с гейтом 0 —
# на каждой метке, и основной цикл переставал получать время: пропадали кадры и
# управление холостым, а мотор продолжал крутиться на прерываниях.
#
# Теперь:
#   TP (в прерывании)  — только готовые числа и умножения. Ни ожиданий, ни делений.
#                        Сырьё АЦП берём из $1408, которое завод и так обновляет
#                        сам (8908-890d) — читать канал второй раз было ошибкой.
#   VECALC (в основном цикле) — тяжёлые поиски VE и Ktps, результат в $FA/$FB.
# Так устроен и заводской код: датчики читаются в цикле, в прерывании только счёт.
VE_C, KT_C = 0xFA, 0xFB          # кэш VE и Ktps (наша зона zero-page, завод её не трогает)

PROG = [
    # ---------- ЧАСТЬ 1: то, что зовётся из прерывания ----------
    (None,"LDAAe",MODE),(None,"BNE","DADMODE"),
    (None,"JSRe",0x8057),(None,"RTS",None),
    # Гейта по оборотам больше НЕТ: рутина стала дешёвой, душить её незачем,
    # а с гейтом мотор не заводился (ниже порога расчёт уходил заводскому коду,
    # который делит накопленный расход воздуха — а расходомера уже нет).
    # --- Д (давление) из ГОТОВОГО сырья $1408 ---
    # СМЕЩЕНИЕ ЗНАКОВОЕ (−128…+127 отсчётов): широкодиапазонные датчики показывают
    # давление уже при нуле отсчётов, беззнаковое вычитание такое не выражает.
    ("DADMODE","LDDe",0x1408),(None,"LSRD",None),(None,"LSRD",None),
    (None,"STABd",0xF7),
    (None,"LDAAe",SMESH),(None,"BMI","DADD"),
    (None,"LDAAd",0xF7),(None,"SUBAe",SMESH),(None,"BCC","DOK"),
    (None,"CLRA",None),(None,"BRA","DOK"),
    ("DADD","NEGA",None),(None,"ABA",None),(None,"BCC","DOK"),
    (None,"LDAA#",0xFF),
    ("DOK","STAAd",0xF7),
    (None,"LDAAd",0xF7),(None,"LDABe",NAKL),(None,"MUL",None),(None,"STAAd",0xF7),
    # --- Тр = ((Д×VE)>>7 × Ktps)>>7 × КМ >>7, множители ГОТОВЫЕ ---
    # Страховка на первый запуск: пока основной цикл ни разу не отработал, в кэше
    # нули, и без неё Tp вышел бы нулевым — то есть ни капли топлива.
    (None,"LDAAd",VE_C),(None,"BNE","VEOK"),(None,"LDAA#",0x80),
    ("VEOK","LDABd",0xF7),(None,"MUL",None),(None,"ASLD",None),
    (None,"LDABd",KT_C),(None,"BNE","KTOK"),(None,"LDAB#",0x80),
    ("KTOK","MUL",None),(None,"ASLD",None),
    (None,"LDABe",KM),(None,"MUL",None),(None,"ASLD",None),
    (None,"TAB",None),(None,"CLRA",None),(None,"RTS",None),

    # ---------- ЧАСТЬ 2: то, что зовётся из основного цикла ----------
    # Врезка на b0e5 (был JSR $B148 — заводской опрос датчиков). Сначала отдаём
    # управление ему, чтобы сырьё было свежим, потом считаем множители.
    ("VECALC","JSRe",0xB148),
    (None,"LDAAe",MODE),(None,"BNE","VRUN"),(None,"RTS",None),
    # давление тем же способом, что и в части 1 (нужно как ось поиска VE)
    ("VRUN","LDDe",0x1408),(None,"LSRD",None),(None,"LSRD",None),
    (None,"STABd",0xF7),
    (None,"LDAAe",SMESH),(None,"BMI","VDADD"),
    (None,"LDAAd",0xF7),(None,"SUBAe",SMESH),(None,"BCC","VDOK"),
    (None,"CLRA",None),(None,"BRA","VDOK"),
    ("VDADD","NEGA",None),(None,"ABA",None),(None,"BCC","VDOK"),
    (None,"LDAA#",0xFF),
    ("VDOK","STAAd",0xF7),
    (None,"LDAAd",0xF7),(None,"LDABe",NAKL),(None,"MUL",None),(None,"STAAd",0xF7),
    # --- поиск VE по обороты × давление ---
    (None,"LDXe",0x1482),(None,"STXd",0xF4),(None,"LDAAd",0x7D),(None,"STAAd",0xF6),
    (None,"CLRA",None),(None,"LDABd",0xF7),(None,"STDe",0x1482),
    (None,"LDAAd",0x7D),(None,"ANDA#",0x1F),(None,"ORAA#",0x14),(None,"STAAd",0x7D),
    (None,"LDXd",PTR_VE),(None,"STXd",0x74),
    (None,"LDX#",0xFB20),(None,"STXd",0x76),
    (None,"LDX#",PAXIS),(None,"STXd",0x78),
    (None,"JSRe",0x80CF),(None,"STAAd",VE_C),
    (None,"LDAAd",0xF6),(None,"STAAd",0x7D),(None,"LDXd",0xF4),(None,"STXe",0x1482),
    # --- поиск Ktps по обороты × TPS ---
    (None,"LDXe",0x1482),(None,"STXd",0xF4),(None,"LDAAd",0x7D),(None,"STAAd",0xF6),
    (None,"CLRA",None),(None,"LDABe",0x14A2),(None,"STDe",0x1482),
    (None,"LDAAd",0x7D),(None,"ANDA#",0x1F),(None,"ORAA#",0x14),(None,"STAAd",0x7D),
    (None,"LDXd",PTR_KT),(None,"STXd",0x74),
    (None,"LDX#",0xFB20),(None,"STXd",0x76),
    (None,"LDX#",TAXIS),(None,"STXd",0x78),
    (None,"JSRe",0x80CF),(None,"STAAd",KT_C),
    (None,"LDAAd",0xF6),(None,"STAAd",0x7D),(None,"LDXd",0xF4),(None,"STXe",0x1482),
    (None,"RTS",None),
]

LEN={"BNE":2,"LDAAe":3,"LDDe":3,"SUBD#":3,"BCC":2,"JSRe":3,"RTS":1,"LDAB#":2,"LSRD":1,"SUBBe":3,
     "CLRB":1,"STABd":2,"LDXe":3,"STXd":2,"LDAAd":2,"STAAd":2,"CLRA":1,"LDABd":2,
     "STDe":3,"ANDA#":2,"ORAA#":2,"LDX#":3,"LDXd":2,"STXe":3,"MUL":1,
     "LDABe":3,"ASLD":1,"TAB":1,
     # добавлено под ЗНАКОВОЕ смещение ДАД (см. блок «Д (давление)»)
     "BMI":2,"BRA":2,"SUBAe":3,"NEGA":1,"ABA":1,"LDAA#":2,"LDAB#":2}
OP1={"RTS":0x39,"LSRD":0x04,"CLRB":0x5F,"CLRA":0x4F,"MUL":0x3D,"ASLD":0x05,"TAB":0x16,
     "NEGA":0x40,"ABA":0x1B}


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
        elif op=="BNE":
            r=lab[a]-nx; assert -128<=r<=127,("BNE %s %d"%(a,r)); out+=bytes([0x26,r&0xFF])
        elif op=="JSRe":  out+=bytes([0xBD,a>>8,a&0xFF])
        elif op=="LDAB#": out+=bytes([0xC6,a&0xFF])
        elif op=="SUBBe": out+=bytes([0xF0,a>>8,a&0xFF])
        elif op=="STABd": out+=bytes([0xD7,a&0xFF])
        elif op=="LDXe":  out+=bytes([0xFE,a>>8,a&0xFF])
        elif op=="STXd":  out+=bytes([0xDF,a&0xFF])
        elif op=="STXe":  out+=bytes([0xFF,a>>8,a&0xFF])
        elif op=="LDXd":  out+=bytes([0xDE,a&0xFF])
        elif op=="LDAAe": out+=bytes([0xB6,a>>8,a&0xFF])
        elif op=="LDAAd": out+=bytes([0x96,a&0xFF])
        elif op=="STAAd": out+=bytes([0x97,a&0xFF])
        elif op=="LDABd": out+=bytes([0xD6,a&0xFF])
        elif op=="LDABe": out+=bytes([0xF6,a>>8,a&0xFF])
        elif op=="STDe":  out+=bytes([0xFD,a>>8,a&0xFF])
        elif op=="BMI":
            r=lab[a]-nx; assert -128<=r<=127,("BMI %s %d"%(a,r)); out+=bytes([0x2B,r&0xFF])
        elif op=="BRA":
            r=lab[a]-nx; assert -128<=r<=127,("BRA %s %d"%(a,r)); out+=bytes([0x20,r&0xFF])
        elif op=="SUBAe": out+=bytes([0xB0,a>>8,a&0xFF])
        elif op=="LDAA#": out+=bytes([0x86,a&0xFF])
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
    for a,n in [(ROUT,len(code)),(VEMAP,256),(PAXIS,16),(SMESH,1),(KM,1),(NAKL,1),(KTPS,256),(TAXIS,16),(SPAN,1),(MODE,1)]:
        assert all(b==0x3F for b in rom[off(a):off(a)+n]),"не пусто @ %04X"%a
    # врезка
    ho=off(HOOK)
    assert rom[ho]==0xBD and (rom[ho+1]<<8|rom[ho+2])==0x8057,"по 89D8 не JSR 8057"
    rom[off(ROUT):off(ROUT)+len(code)]=code
    # данные ДАД (номинал)
    # VE — ПОСТРОЕНА ПО ЛОГАМ ПОЛЬЗОВАТЕЛЯ, не выдумана.
    #
    # Формула блока при всех единицах вырождается в Tp = Д, поэтому нужный
    # коэффициент = реальное_наполнение / давление. Обе величины взяты из логов:
    #   холостой   : Tp 23 при 50 кПа   -> 0.46
    #   полный газ : Tp 84…91 при 107 кПа (72 замера, газ >= 80%) -> 0.79…0.85
    # Между ними — линейно по давлению. Главный наклон именно ПО ДАВЛЕНИЮ:
    # разница вдвое, тогда как по оборотам всего ±4%.
    #
    # ⚠ Прошлая версия делала наклон по ОБОРОТАМ и плоско по давлению — это было
    # неверно и давало на холостом вдвое бедно (Tp 11 против нужных 23).
    #
    # Форма по оборотам — из тех же замеров, нормирована на пик 3500 об.
    # Вне 2500…5000 данных нет, поэтому края держим на ближайшем известном.
    PAXIS_VAL=[20,26,32,38,44,50,56,62,68,74,80,86,92,98,104,110]
    VE_LO,P_LO = 0.46, 50.0        # холостой
    VE_HI,P_HI = 0.83, 107.0       # полный газ (среднее по кривой)
    SHAPE=[(2500,0.966),(3000,0.966),(3500,1.000),(4000,0.977),(4500,0.945),(5000,0.928)]
    def shape(rpm):
        if rpm<=SHAPE[0][0]: return SHAPE[0][1]
        if rpm>=SHAPE[-1][0]: return SHAPE[-1][1]
        for i in range(len(SHAPE)-1):
            (r0,v0),(r1,v1)=SHAPE[i],SHAPE[i+1]
            if r0<=rpm<=r1: return v0+(v1-v0)*(rpm-r0)/(r1-r0)
        return 1.0
    rax=[rom[off(0xFB20)+i] for i in range(16)]      # ось оборотов ИЗ ПЗУ
    k=(VE_HI-VE_LO)/(P_HI-P_LO)
    for r in range(16):
        s = shape(rax[r] * 51.2)                     # обороты = значение оси × 51.2
        for c in range(16):
            ve = (VE_LO + (PAXIS_VAL[c]-P_LO)*k) * s
            rom[off(VEMAP)+r*16+c] = max(1, min(255, round(ve*128)))
    for i,v in enumerate([20,26,32,38,44,50,56,62,68,74,80,86,92,98,104,110]): rom[off(PAXIS)+i]=v
    rom[off(SMESH)]=26; rom[off(KM)]=128; rom[off(NAKL)]=125
    # данные Ktps: карта 0x80 (=1.0, без поправки), ось TPS из января
    for i in range(256): rom[off(KTPS)+i]=0x80
    for i,v in enumerate(TAXIS_VAL): rom[off(TAXIS)+i]=v
    rom[off(SPAN)]=172        # span полного газа в $14A2 (=344 в $1492)
    rom[off(MODE)]=0          # ПО УМОЛЧАНИЮ РАСХОДОМЕР: без датчика давления ДАД
                              # считал бы мусор. Ставить 1 после установки датчика.
    # врезка адреса — прерывание зовёт часть 1
    rom[ho+1],rom[ho+2]=ROUT>>8,ROUT&0xFF
    # ВТОРАЯ ВРЕЗКА: основной цикл (b0e5: JSR $B148) -> наша часть 2, а она в начале
    # сама зовёт $B148. Порядок заводских вызовов сохраняется, а тяжёлые поиски VE
    # и Ktps уезжают из прерывания сюда, где ждать можно сколько угодно.
    ho2=off(0xB0E5)
    assert rom[ho2]==0xBD and (rom[ho2+1]<<8|rom[ho2+2])==0xB148,"по B0E5 не JSR B148"
    va=lab["VECALC"]
    rom[ho2+1],rom[ho2+2]=va>>8,va&0xFF
    print("  врезка в основной цикл: B0E5 -> VECALC @ %04X"%va)
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
    print("  режим @ %04X = %d (0 расходомер / 1 ДАД)"%(MODE,rom[off(MODE)]))
    print("  чек-сумма: %02X/%02X"%(s,x))


if __name__=="__main__": main()
