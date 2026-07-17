// ---- FUN_8001 @ 8001 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8001(void)

{
  ushort uVar1;
  undefined3 uVar2;
  ushort uVar3;
  ushort in_D;
  ushort uVar4;
  ushort uVar5;
  ushort uVar6;
  
  _DAT_0060 = in_D;
  uVar3 = _DAT_0060;
  uVar4 = (ushort)DAT_005c * (in_D & 0xff);
  DAT_0060 = (byte)(in_D >> 8);
  uVar1 = _DAT_005b & 0xff;
  uVar5 = DAT_0060 * uVar1 + (uVar4 >> 8);
  uVar6 = (in_D & 0xff) * (ushort)DAT_005b;
  _DAT_005c = CONCAT21(uVar6 + uVar5,(char)uVar4);
  uVar2 = _DAT_005c;
  uVar1 = (ushort)DAT_005b;
  _DAT_005b = CONCAT13(CARRY2(uVar6,uVar5),_DAT_005c);
  _DAT_005b = CONCAT22(uVar1 * DAT_0060 + _DAT_005b,(short)uVar2);
  _DAT_0060 = uVar3;
  return;
}


// ---- FUN_802c @ 802c ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 FUN_802c(short param_1)

{
  byte bVar1;
  short in_D;
  short sVar2;
  ushort *puVar3;
  
  bVar1 = (byte)((ushort)(in_D << 1) >> 8);
  if (0x3e < bVar1) {
    return (char)((ushort)*(undefined2 *)(param_1 + 0x7e) >> 8);
  }
  _DAT_005b = in_D << 9;
  puVar3 = (ushort *)(param_1 + (ushort)(byte)(bVar1 << 1));
  sVar2 = puVar3[1] - *puVar3;
  if (*puVar3 <= puVar3[1]) {
    FUN_8001();
    return (char)(*puVar3 + _DAT_005b >> 8);
  }
  FUN_8001((char)((ushort)(CONCAT11(~(byte)((ushort)sVar2 >> 8),~(byte)sVar2) + 1) >> 8));
  return (char)(*puVar3 - _DAT_005b >> 8);
}


// ---- FUN_8057 @ 8057 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

byte FUN_8057(void)

{
  byte bVar1;
  bool bVar2;
  short sVar3;
  ushort uVar4;
  byte bVar5;
  
  DAT_0063 = '\x11';
  uVar4 = _DAT_005b;
  do {
    if ((short)_DAT_0060 < 0) {
      do {
        sVar3 = uVar4 - _DAT_0060;
        if (_DAT_0060 <= uVar4) goto LAB_8097;
        sVar3 = sVar3 + _DAT_0060;
        bVar5 = 0;
        while( true ) {
          bVar1 = DAT_005f >> 7;
          DAT_005f = DAT_005f << 1 | bVar5;
          bVar2 = (bool)(DAT_005e >> 7);
          DAT_005e = DAT_005e << 1 | bVar1;
          DAT_0063 = DAT_0063 + -1;
          if (DAT_0063 == '\0') {
            if (bVar2) {
              return 0xff;
            }
            return DAT_005e;
          }
          bVar5 = DAT_005d >> 7;
          DAT_005d = DAT_005d << 1 | bVar2;
          uVar4 = CONCAT11((char)((ushort)sVar3 >> 8) << 1 | (byte)sVar3 >> 7,
                           (byte)sVar3 << 1 | bVar5);
          if (-1 < sVar3) break;
          sVar3 = uVar4 - _DAT_0060;
LAB_8097:
          bVar5 = 1;
        }
      } while( true );
    }
    bVar1 = DAT_0062 >> 7;
    DAT_0062 = DAT_0062 << 1;
    bVar5 = DAT_0061 >> 7;
    DAT_0061 = DAT_0061 << 1 | bVar1;
    DAT_0060 = DAT_0060 << 1 | bVar5;
    bVar1 = DAT_005f >> 7;
    DAT_005f = DAT_005f << 1;
    bVar5 = DAT_005e >> 7;
    DAT_005e = DAT_005e << 1 | bVar1;
    bVar1 = DAT_005d >> 7;
    DAT_005d = DAT_005d << 1 | bVar5;
    bVar2 = -1 < (short)uVar4;
    uVar4 = CONCAT11((char)(uVar4 >> 8) << 1 | (byte)uVar4 >> 7,(byte)uVar4 << 1 | bVar1);
  } while (bVar2);
  DAT_0063 = 0x11;
  return 0xff;
}


// ---- FUN_809f @ 809f ----

/* WARNING: Removing unreachable block (RAM,0x80ba) */
/* WARNING: Removing unreachable block (RAM,0x80c0) */
/* WARNING: Removing unreachable block (RAM,0x80c2) */
/* WARNING: Removing unreachable block (RAM,0x80c8) */

undefined1 FUN_809f(short param_1)

{
  byte bVar1;
  undefined2 in_D;
  
  bVar1 = (byte)((ushort)in_D >> 8);
  if (0xf0 < bVar1) {
    bVar1 = 0;
  }
  return *(undefined1 *)(param_1 + (((ushort)bVar1 << 0xc) >> 8));
}


// ---- FUN_80a9 @ 80a9 ----

/* WARNING: Removing unreachable block (RAM,0x80ba) */
/* WARNING: Removing unreachable block (RAM,0x80c0) */
/* WARNING: Removing unreachable block (RAM,0x80c2) */
/* WARNING: Removing unreachable block (RAM,0x80c8) */

undefined1 FUN_80a9(short param_1)

{
  byte bVar1;
  undefined2 in_D;
  
  bVar1 = (byte)((ushort)in_D >> 8);
  if (0xf8 < bVar1) {
    bVar1 = 0xf8;
  }
  return *(undefined1 *)(param_1 + (((ushort)bVar1 << 0xb) >> 8));
}


// ---- FUN_80cf @ 80cf ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_80cf(void)

{
  undefined2 uVar1;
  bool bVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  char cVar8;
  char extraout_B;
  short sVar6;
  char extraout_B_00;
  ushort uVar7;
  byte bVar9;
  byte *pbVar10;
  
  _DAT_0067 = _DAT_140a;
  sVar6 = _DAT_1482;
  if (((DAT_007d & 0x40) != 0) && ((DAT_00c7 & 1) != 0)) {
    sVar6 = -1;
  }
  cVar8 = '\x0f';
  DAT_0069 = (byte)((ushort)sVar6 >> 8);
  pbVar10 = _DAT_0078;
  do {
    if (DAT_0069 < pbVar10[1]) break;
    pbVar10 = pbVar10 + 1;
    cVar8 = cVar8 + -1;
  } while (cVar8 != '\0');
  uVar1 = *(undefined2 *)pbVar10;
  bVar3 = *_DAT_0078;
  if ((DAT_0069 < bVar3) ||
     (bVar3 = _DAT_0078[0xf], bVar2 = bVar3 <= DAT_0069, _DAT_0069 = sVar6, bVar2)) {
    _DAT_0069 = (ushort)bVar3 << 8;
  }
  cVar8 = '\x0f';
  pbVar10 = _DAT_0076;
  do {
    if ((byte)(_DAT_140a << 2) < pbVar10[1]) break;
    pbVar10 = pbVar10 + 1;
    cVar8 = cVar8 + -1;
  } while (cVar8 != '\0');
  DAT_007a = 0xff;
  _DAT_0070 = *(undefined2 *)pbVar10;
  bVar3 = (byte)(_DAT_140a << 2);
  if (bVar3 < *_DAT_0076) {
    bVar3 = *_DAT_0076;
  }
  else {
    if (bVar3 < _DAT_0076[0xf]) goto LAB_814b;
    bVar3 = _DAT_0076[0xf];
  }
  _DAT_0067 = (ushort)bVar3 << 2;
LAB_814b:
  _DAT_0074 = _DAT_0074 + 0xff;
  DAT_0072 = (char)((ushort)uVar1 >> 8);
  _DAT_006b = CONCAT11((char)((ushort)_DAT_0069 >> 8) - DAT_0072,(char)_DAT_0069);
  DAT_006d = 0;
  DAT_0073 = (char)uVar1;
  DAT_006e = DAT_0073 - DAT_0072;
  DAT_006f = 0;
  _DAT_0072 = uVar1;
  FUN_8297();
  sVar6 = _DAT_0067 + (ushort)DAT_0070 * -4;
  _DAT_006b = sVar6 * 4;
  DAT_006d = (char)((char)sVar6 << 7) >> 1;
  DAT_006f = DAT_0071 - DAT_0070;
  DAT_006e = 0;
  DAT_0072 = extraout_B;
  FUN_8297();
  DAT_0073 = extraout_B_00;
  do {
    *(char *)((short)register0x12 + -1) = -0x7f;
    *(char *)((short)register0x12 + 0x10000) = -0x6e;
    FUN_8208();
    uVar7 = CONCAT11(DAT_0075 - DAT_0074,DAT_0072);
    if (DAT_0075 < DAT_0074) {
      bVar3 = -(DAT_0075 - DAT_0074);
      bVar4 = -DAT_0072;
      uVar7 = CONCAT11(bVar3,bVar4);
      if (bVar4 == 0) goto LAB_819b;
      sVar6 = (ushort)bVar3 * (ushort)bVar4;
      if ((char)sVar6 < '\0') {
        sVar6 = (ushort)(byte)((char)((ushort)sVar6 >> 8) + 1) << 8;
      }
      bVar3 = (char)((ushort)sVar6 >> 8) + DAT_0075;
    }
    else {
LAB_819b:
      sVar6 = (uVar7 >> 8) * (uVar7 & 0xff);
      if ((char)sVar6 < '\0') {
        sVar6 = (ushort)(byte)((char)((ushort)sVar6 >> 8) + 1) << 8;
      }
      bVar3 = (char)((ushort)sVar6 >> 8) + DAT_0074;
    }
    uVar7 = CONCAT11(DAT_0077 - DAT_0076,DAT_0072);
    if (DAT_0077 < DAT_0076) {
      bVar4 = -(DAT_0077 - DAT_0076);
      bVar5 = -DAT_0072;
      uVar7 = CONCAT11(bVar4,bVar5);
      if (bVar5 == 0) goto LAB_81bc;
      sVar6 = (ushort)bVar4 * (ushort)bVar5;
      if ((char)sVar6 < '\0') {
        sVar6 = (ushort)(byte)((char)((ushort)sVar6 >> 8) + 1) << 8;
      }
      bVar4 = (char)((ushort)sVar6 >> 8) + DAT_0077;
    }
    else {
LAB_81bc:
      sVar6 = (uVar7 >> 8) * (uVar7 & 0xff);
      if ((char)sVar6 < '\0') {
        sVar6 = (ushort)(byte)((char)((ushort)sVar6 >> 8) + 1) << 8;
      }
      bVar4 = (char)((ushort)sVar6 >> 8) + DAT_0076;
    }
    _DAT_0078 = (byte *)CONCAT11(bVar3,bVar4);
    uVar7 = CONCAT11(bVar4 - bVar3,DAT_0073);
    if (bVar4 < bVar3) {
      bVar5 = -(bVar4 - bVar3);
      bVar9 = -DAT_0073;
      uVar7 = CONCAT11(bVar5,bVar9);
      if (bVar9 == 0) goto LAB_81dc;
      sVar6 = (ushort)bVar5 * (ushort)bVar9;
      if ((char)sVar6 < '\0') {
        sVar6 = (ushort)(byte)((char)((ushort)sVar6 >> 8) + 1) << 8;
      }
      cVar8 = (char)((ushort)sVar6 >> 8) + bVar4;
    }
    else {
LAB_81dc:
      sVar6 = (uVar7 >> 8) * (uVar7 & 0xff);
      if ((char)sVar6 < '\0') {
        sVar6 = (ushort)(byte)((char)((ushort)sVar6 >> 8) + 1) << 8;
      }
      cVar8 = (char)((ushort)sVar6 >> 8) + bVar3;
    }
    if ((DAT_007d & 0x40) == 0) {
      return;
    }
    if ((DAT_007d & 0x20) != 0) {
      DAT_007d = DAT_007d & 0xdf;
      return;
    }
    DAT_007d = DAT_007d | 0x20;
    *(char *)register0x12 = cVar8;
    register0x12 = (BADSPACEBASE *)((short)register0x12 + -1);
  } while( true );
}


// ---- FUN_8208 @ 8208 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8208(undefined1 param_1,undefined1 param_2,byte *param_3)

{
  undefined1 uVar1;
  byte bVar3;
  byte bVar4;
  ushort uVar2;
  
  if ((DAT_007d & 0x40) == 0) {
    if ((DAT_007d & 0x10) != 0) {
      bVar3 = *param_3;
      if (((char)bVar3 < '\0') && (bVar3 < 0xf7)) {
        uVar2 = CONCAT11(bVar3,DAT_007d) & 0x7fff | 8;
      }
      else {
        uVar2 = CONCAT11(bVar3,DAT_007d) & 0xfff7;
      }
      DAT_007d = (byte)uVar2;
      DAT_0074 = (char)(uVar2 >> 8) + -0x80;
      uVar1 = FUN_8285(param_3[1]);
      _DAT_0074 = CONCAT11(DAT_0074,uVar1);
      uVar1 = FUN_8285(param_3[0x10]);
      DAT_0076 = uVar1;
      uVar1 = FUN_8285(param_3[0x11]);
      _DAT_0076 = CONCAT11(DAT_0076,uVar1);
      return;
    }
    _DAT_0074 = *(undefined2 *)param_3;
    _DAT_0076 = *(undefined2 *)(param_3 + 0x10);
    return;
  }
  if ((DAT_007d & 0x20) != 0) {
    bVar3 = *param_3;
    if (-1 < (char)bVar3) {
      bVar3 = 0x40;
    }
    bVar4 = param_3[1];
    if (-1 < (char)bVar4) {
      bVar4 = 0x40;
    }
    _DAT_0074 = CONCAT11(bVar3,bVar4) & 0x7f7f;
    bVar3 = param_3[0x10];
    if (-1 < (char)bVar3) {
      bVar3 = 0x40;
    }
    bVar4 = param_3[0x11];
    if (-1 < (char)bVar4) {
      bVar4 = 0x40;
    }
    _DAT_0076 = CONCAT11(bVar3,bVar4) & 0x7f7f;
    return;
  }
  bVar3 = *param_3;
  if ((char)bVar3 < '\0') {
    bVar3 = 0;
  }
  bVar4 = param_3[1];
  if ((char)bVar4 < '\0') {
    bVar4 = 0;
  }
  _DAT_0074 = CONCAT11(bVar3,bVar4);
  bVar3 = param_3[0x10];
  if ((char)bVar3 < '\0') {
    bVar3 = 0;
  }
  bVar4 = param_3[0x11];
  if ((char)bVar4 < '\0') {
    bVar4 = 0;
  }
  _DAT_0076 = CONCAT11(bVar3,bVar4);
  return;
}


// ---- FUN_8285 @ 8285 ----

char FUN_8285(byte param_1)

{
  if (param_1 < 0xf7) {
    param_1 = param_1 & 0x7f;
  }
  return param_1 + 0x80;
}


// ---- FUN_8297 @ 8297 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8297(void)

{
  bool bVar1;
  undefined1 uVar4;
  short sVar2;
  ushort uVar3;
  byte bVar5;
  
  uVar4 = 0;
  if (_DAT_006e != 0) {
    DAT_0066 = '\t';
    uVar3 = _DAT_006b;
    do {
      if ((short)_DAT_006e < 0) {
        do {
          sVar2 = uVar3 - _DAT_006e;
          if (_DAT_006e <= uVar3) goto LAB_82cd;
          sVar2 = sVar2 + _DAT_006e;
          bVar5 = 0;
          while( true ) {
            bVar1 = (bool)(DAT_006d >> 7);
            DAT_006d = DAT_006d << 1 | bVar5;
            DAT_0066 = DAT_0066 + -1;
            if (DAT_0066 == '\0') {
              if (!bVar1) {
                return;
              }
              goto LAB_82b3;
            }
            uVar3 = CONCAT11((char)((ushort)sVar2 >> 8) << 1 | (byte)sVar2 >> 7,
                             (byte)sVar2 << 1 | bVar1);
            if (-1 < sVar2) break;
            sVar2 = uVar3 - _DAT_006e;
LAB_82cd:
            bVar5 = 1;
          }
        } while( true );
      }
      bVar5 = DAT_006f >> 7;
      DAT_006f = DAT_006f << 1;
      DAT_006e = DAT_006e << 1 | bVar5;
      bVar5 = DAT_006d >> 7;
      DAT_006d = DAT_006d << 1;
      bVar1 = -1 < (short)uVar3;
      uVar3 = CONCAT11((char)(uVar3 >> 8) << 1 | (byte)uVar3 >> 7,(byte)uVar3 << 1 | bVar5);
    } while (bVar1);
LAB_82b3:
    uVar4 = 0xff;
  }
  DAT_006d = uVar4;
  return;
}


// ---- FUN_82d5 @ 82d5 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_82d5(void)

{
  byte bVar1;
  undefined2 in_D;
  short sVar2;
  short sVar3;
  
  bVar1 = (byte)((ushort)in_D >> 8);
  sVar2 = (ushort)bVar1 * (ushort)DAT_005c;
  sVar3 = (ushort)bVar1 * (ushort)DAT_005b;
  bVar1 = (byte)sVar3;
  DAT_005c = (byte)((ushort)sVar2 >> 8);
  _DAT_005b = CONCAT21(CONCAT11((char)((ushort)sVar3 >> 8) + CARRY1(bVar1,DAT_005c),bVar1 + DAT_005c
                               ),(char)sVar2);
  return;
}


// ---- vec_IRQ @ 82e6 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 vec_IRQ(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  undefined1 in_stack_00000003;
  
  DAT_00c6 = DAT_102e;
  DAT_1034 = ~DAT_102e;
  if ((DAT_1034 & 0x20) == 0) {
    bVar3 = 0;
    bVar2 = DAT_00a6;
    do {
      bVar1 = bVar2 & 1;
      bVar2 = bVar2 >> 1;
      if (((bVar1 != 0) && (*(ushort *)(bVar3 + 0x1048) != 0)) &&
         (DAT_15b3 = bVar3, *(ushort *)(bVar3 + 0x15a7) <= *(ushort *)(bVar3 + 0x1048))) {
        *(undefined2 *)(bVar3 + 0x1048) = 0;
        bVar3 = DAT_15b3;
      }
      bVar3 = bVar3 + 2;
    } while (bVar2 != 0);
    DAT_102b = DAT_102b & 0xdf;
  }
  if ((((DAT_00c6 & 8) != 0) && ((DAT_0040 & 8) == 0)) && ((DAT_0054 & 8) != 0)) {
    FUN_876a();
    if ((DAT_0054 & 0x80) != 0) {
      return in_stack_00000003;
    }
    do {
      if ((DAT_0055 & 0x40) == 0) {
        if ((DAT_0054 & 0x20) == 0) {
          if ((DAT_0054 & 0x40) == 0) {
            if ((DAT_0054 & 0x10) == 0) {
              if ((DAT_0055 & 0x80) == 0) {
                return in_stack_00000003;
              }
              DAT_0054 = DAT_0054 | 0x80;
              DAT_0055 = DAT_0055 & 0x7f;
              FUN_99de();
              FUN_99f3();
              FUN_9b24();
              FUN_9bbe();
              FUN_a99b();
              FUN_ad88();
              if ((DAT_0040 & 8) == 0) {
                FUN_9e94();
                FUN_c4b2();
                FUN_9e5d();
                FUN_a211();
                FUN_a8b7();
              }
              else {
                FUN_c551();
                FUN_c57e();
              }
              DAT_144a = DAT_0053;
            }
            else {
              DAT_0054 = DAT_0054 & 0xef | 0x80;
              FUN_94c1();
              FUN_9513();
            }
          }
          else {
            DAT_0054 = DAT_0054 & 0xbf | 0x80;
            FUN_8dd5();
            if ((DAT_0040 & 8) == 0) {
              FUN_91a8();
              FUN_925f();
              FUN_944c();
              FUN_9487();
            }
            else {
              FUN_925f();
              FUN_944c();
              FUN_c319();
              FUN_c46c();
            }
          }
        }
        else {
          DAT_0054 = DAT_0054 & 0xdf | 0x80;
          FUN_8908();
          FUN_8990();
          FUN_8a26();
          FUN_8a49();
          FUN_8b55();
          FUN_8d2c();
          FUN_8d4b();
          FUN_8d80();
        }
      }
      else {
        DAT_0054 = DAT_0054 | 0x80;
        DAT_0055 = DAT_0055 & 0xbf;
        FUN_88d0();
      }
      DAT_0054 = DAT_0054 & 0x7f;
      DAT_2000 = DAT_00bc;
      DAT_4000 = DAT_00b4;
      P2DATA = DAT_0048;
      DAT_0017 = DAT_0049;
      DAT_1002 = DAT_009c;
    } while( true );
  }
  return in_stack_00000003;
}


// ---- vec_ICF @ 843d ----

undefined1 vec_ICF(void)

{
  undefined1 in_stack_00000003;
  
  if ((DAT_0040 & 8) == 0) {
    FUN_844f();
    DAT_0054 = DAT_0054 | 8;
  }
  return in_stack_00000003;
}


// ---- FUN_844f @ 844f ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_844f(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  char cVar4;
  char cVar5;
  byte bVar6;
  byte bVar8;
  byte bVar9;
  ushort uVar7;
  byte bVar10;
  byte bStack0000;
  
  bVar9 = DAT_1580;
  bVar8 = DAT_144d;
  if ((DAT_0054 & 8) == 0) {
    _DAT_1068 = 0;
    _DAT_106a = 0x78;
    DAT_1575 = 'x' - DAT_143a;
    DAT_143a = (DAT_140f - DAT_1575) + 0x78;
  }
  _DAT_1042 = 0xffff;
  DAT_144d = DAT_140f;
  DAT_1410 = DAT_140f;
  if ((DAT_0053 & 1) == 0) {
    DAT_143a = DAT_143a - (bVar8 - DAT_140f);
    DAT_1410 = bVar8;
  }
  _DAT_106c = (ushort)DAT_1410;
  _DAT_106e = (ushort)DAT_143a;
  DAT_15a2 = DAT_143a;
  DAT_14ce = DAT_14ce + '\x01';
  uRAM1063 = 0;
  DAT_1062 = 0;
  DAT_1582 = DAT_1582 + 1;
  if (5 < DAT_1582) {
    DAT_1582 = 0;
  }
  if ((DAT_1582 == 0) || (DAT_1582 == 3)) {
    DAT_00c2 = DAT_00c2 & 0xfe;
  }
  bStack0000 = 0;
  if (((DAT_fee1 & 4) != 0) && (((DAT_004f & 0x20) != 0 || ((DAT_00c2 & 1) != 0)))) {
    bStack0000 = 0xff;
  }
  if ((DAT_004f & 0x20) == 0) {
    bVar8 = DAT_147a >> 4;
    if ((DAT_00c2 & 0x80) == 0) {
      DAT_00c2 = DAT_00c2 | 0x80;
      DAT_147b = bVar8;
    }
    cVar4 = DAT_004b - bVar8;
    if (cVar4 < '\0') {
      cVar4 = cVar4 + '\x06';
    }
    cVar5 = (DAT_147b - bVar8) + DAT_00be;
    bVar6 = 0;
    bVar9 = 0;
    if (cVar5 != '\0') {
      if (cVar5 < '\0') {
        DAT_00be = cVar5 + '\x01';
        DAT_147b = bVar8;
        goto LAB_8589;
      }
      do {
        bVar9 = (char)bVar6 >> 1;
        bVar6 = bVar9 | 0x80;
        cVar5 = cVar5 + -1;
      } while (cVar5 != '\0');
      bVar9 = (bVar9 & 2) >> 1;
      bVar6 = bVar6 >> 2;
    }
    DAT_00be = '\0';
    bVar6 = bVar6 | 1;
    while (bVar10 = bVar9, cVar4 = cVar4 + -1, DAT_147b = bVar8, -1 < cVar4) {
      bVar9 = bVar6 >> 7;
      bVar1 = bVar6 << 1;
      bVar6 = bVar1 | bVar10;
      if ((bVar1 & 0x40) != 0) {
        bVar6 = bVar1 & 0x3f | bVar10 | 1;
      }
    }
  }
  else {
    DAT_1581 = DAT_1580;
    DAT_1580 = 0;
    DAT_00c2 = DAT_00c2 & 0x7f;
    if ((DAT_1582 == 0) || (DAT_1582 == 3)) {
      DAT_157d = bVar9 >> 2;
      DAT_1564 = DAT_157d - 1;
      _DAT_157e = (_DAT_004d + _DAT_157b) * 8;
      _DAT_1562 = (_DAT_004d + _DAT_157b) * 0x40;
      DAT_00c2 = DAT_00c2 | 1;
    }
  }
LAB_8589:
  bVar8 = DAT_1036 & 0xc0;
  DAT_00a6 = bVar8;
  DAT_1036 = bVar8;
  if (((DAT_fee1 & 4) == 0) || ((DAT_00c2 & 1) == 0)) {
    bVar9 = 0;
    do {
      bVar6 = bVar8 & 1;
      bVar8 = bVar8 >> 1;
      if ((bVar6 != 0) && (*(short *)(bVar9 + 0x1048) != 0)) {
        *(short *)(bVar9 + 0x15a7) = *(short *)(bVar9 + 0x1048);
        DAT_102b = DAT_102b | 0x20;
      }
      bVar9 = bVar9 + 2;
    } while (bVar8 != 0);
    _DAT_1042 = (ushort)bStack0000;
    FUN_86da();
  }
  DAT_00a0 = DAT_00a0 << 1;
  if ((DAT_00a0 & 0x40) != 0) {
    DAT_00a0 = DAT_00a0 | 1;
  }
  DAT_00a0 = DAT_00a0 | 0x40;
  DAT_00a3 = DAT_00a2;
  bVar8 = DAT_1036 & 0x3f;
  DAT_00a1 = bVar8 | DAT_00a2;
  DAT_0056 = 0;
  DAT_0040 = DAT_0040 & 0xfb;
  DAT_1003 = 0;
  DAT_1011 = 0xbf;
  if ((DAT_0054 & 1) != 0) {
    DAT_1011 = 0x3f;
  }
  DAT_00a2 = bVar8;
  if ((DAT_0054 & 8) != 0) {
    uVar7 = IMPCAP;
    if (((TCSR & 0x20) != 0) && (IMPCAP < 0x8000)) {
      FUN_c311();
    }
    if (uVar7 < _DAT_1478) {
      DAT_1567 = DAT_1567 - 1;
    }
    bVar1 = DAT_1567;
    DAT_1567 = DAT_1567 >> 1;
    bVar6 = DAT_1567;
    cVar4 = (char)(uVar7 - _DAT_1478 >> 8);
    bVar8 = cVar4 >> 1;
    DAT_1567 = bVar1 >> 2;
    bVar10 = DAT_1567;
    bVar9 = (char)(bVar8 | bVar1 << 7) >> 1;
    DAT_1567 = bVar1 >> 3;
    bVar2 = DAT_1567;
    bVar6 = (char)(bVar9 | bVar6 << 7) >> 1;
    DAT_1567 = bVar1 >> 4;
    bVar3 = DAT_1567;
    bVar10 = (char)(bVar6 | bVar10 << 7) >> 1;
    DAT_1567 = bVar1 >> 5;
    _DAT_1465 = CONCAT11((char)(bVar10 | bVar2 << 7) >> 1 | bVar3 << 7,
                         (char)((char)((char)((char)((char)(uVar7 - _DAT_1478) >> 1 | cVar4 << 7) >>
                                              1 | bVar8 << 7) >> 1 | bVar9 << 7) >> 1 | bVar6 << 7)
                         >> 1 | bVar10 << 7);
    if (DAT_1567 != 0) {
      _DAT_1465 = 0xffff;
    }
    if (((((DAT_009d & 2) != 0) && ((DAT_0053 & 2) == 0)) && (0x1f < DAT_1442)) &&
       ((_DAT_14e1 * 6 < _DAT_1465 || (_DAT_1465 <= _DAT_14e1 << 1)))) {
      DAT_0047 = DAT_0047 | 8;
    }
    DAT_009d = DAT_009d | 2;
    _DAT_14e1 = _DAT_1465;
  }
  _DAT_1478 = IMPCAP;
  DAT_1567 = 0;
  DAT_007f = DAT_007f & 0xcf;
  DAT_007f = DAT_1002 & 0x30 | DAT_007f;
  if ((DAT_1002 & 0x10) == 0) {
    DAT_0080 = DAT_0080 + '\x01';
  }
  if ((DAT_fee1 & 0x10) != 0) {
    _DAT_1478 = IMPCAP;
    DAT_1567 = 0;
    return;
  }
  if ((DAT_0054 & 1) != 0) {
    _DAT_1478 = IMPCAP;
    DAT_1567 = 0;
    return;
  }
  bVar8 = 0;
  if ((DAT_0017 & 4) != 0) {
    bVar8 = 0x80;
  }
  uVar7 = CONCAT11(bVar8 ^ DAT_145b,bVar8);
  if (-1 < (char)(bVar8 ^ DAT_145b)) {
    DAT_00b7 = DAT_00b7 | 0x80;
    DAT_145b = DAT_145b + 1;
    uVar7 = CONCAT11(DAT_145b,bVar8) & 0x7fff;
    bVar8 = (byte)(uVar7 >> 8);
    if ((bVar8 < 2) || (DAT_0047 = DAT_0047 | 1, bVar8 < 10)) goto LAB_86d0;
    DAT_00aa = DAT_00aa | 0x80;
    DAT_15cd = 0;
  }
  uVar7 = uVar7 & 0xff;
LAB_86d0:
  DAT_145b = (byte)uVar7 | (byte)(uVar7 >> 8);
  return;
}


// ---- FUN_86da @ 86da ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_86da(void)

{
  if ((DAT_1036 & 1) != 0) {
    if ((DAT_1541 & 1) == 0) {
      _DAT_1054 = _DAT_004d;
    }
    else {
      _DAT_1054 = _DAT_1579;
    }
  }
  if ((DAT_1036 & 2) != 0) {
    if ((DAT_1541 & 2) == 0) {
      _DAT_1056 = _DAT_004d;
    }
    else {
      _DAT_1056 = _DAT_1579;
    }
  }
  if ((DAT_1036 & 4) != 0) {
    if ((DAT_1541 & 4) == 0) {
      _DAT_1058 = _DAT_004d;
    }
    else {
      _DAT_1058 = _DAT_1579;
    }
  }
  if ((DAT_1036 & 8) != 0) {
    if ((DAT_1541 & 8) == 0) {
      _DAT_105a = _DAT_004d;
    }
    else {
      _DAT_105a = _DAT_1579;
    }
  }
  if ((DAT_1036 & 0x10) != 0) {
    if ((DAT_1541 & 0x10) == 0) {
      _DAT_105c = _DAT_004d;
    }
    else {
      _DAT_105c = _DAT_1579;
    }
  }
  if ((DAT_1036 & 0x20) != 0) {
    if ((DAT_1541 & 0x20) == 0) {
      _DAT_105e = _DAT_004d;
    }
    else {
      _DAT_105e = _DAT_1579;
    }
  }
  DAT_14b1 = (char)((ushort)(_DAT_004d << 5) >> 8);
  return;
}


// ---- FUN_876a @ 876a ----

void FUN_876a(void)

{
  byte bVar1;
  byte bVar2;
  byte bStack0000;
  
  DAT_004b = DAT_004b + 1;
  if ((DAT_0017 & 8) != 0) {
    DAT_004b = DAT_fef9;
    DAT_00a0 = DAT_f92c;
    DAT_14c8 = DAT_14c8 | 0x80;
  }
  if (5 < DAT_004b) {
    DAT_004b = 0;
  }
  if ((DAT_004b == 2) || (DAT_004b == 5)) {
    DAT_0054 = DAT_0054 | 0x10;
  }
  if ((DAT_0054 & 4) == 0) {
    DAT_0054 = DAT_0054 | 4;
    DAT_0051 = 0;
  }
  DAT_00a0 = DAT_00a0 & 0xbf;
  if (DAT_009f != 0) {
    bStack0000 = DAT_00a2 & DAT_009f;
    DAT_156b = '\x01';
    bVar2 = 0;
    DAT_14e0 = bStack0000;
    do {
      bVar1 = bStack0000 & 1;
      bStack0000 = bStack0000 >> 1;
      if (bVar1 != 0) {
        FUN_87d3();
      }
      DAT_156b = DAT_156b << 1;
      bVar2 = bVar2 + 1;
    } while (bVar2 < 6);
    DAT_009f = ~DAT_14e0 & DAT_009f;
  }
  return;
}


// ---- FUN_87af @ 87af ----

void FUN_87af(byte param_1)

{
  byte bVar1;
  byte bStack0000;
  
  DAT_156b = '\x01';
  bVar1 = 0;
  DAT_14e0 = param_1;
  do {
    bStack0000 = param_1 >> 1;
    if ((param_1 & 1) != 0) {
      FUN_87d3();
    }
    DAT_156b = DAT_156b << 1;
    bVar1 = bVar1 + 1;
    param_1 = bStack0000;
  } while (bVar1 < 6);
  DAT_009f = ~DAT_14e0 & DAT_009f;
  return;
}


// ---- FUN_87d3 @ 87d3 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_87d3(void)

{
  bool bVar1;
  byte bVar2;
  byte bVar3;
  short *psVar4;
  short sVar5;
  
  if ((((DAT_fee1 & 0x20) != 0) && (DAT_1544 < '\0')) && ((DAT_156b & 0x15) != 0)) {
    return;
  }
  bVar3 = 0;
  bVar2 = DAT_156b;
  while (bVar1 = (bool)(bVar2 & 1), bVar2 = bVar2 >> 1, !bVar1) {
    bVar3 = bVar3 + 2;
  }
  psVar4 = (short *)(&DAT_1054 + bVar3);
  _DAT_156c = psVar4;
  if (*(short *)(bVar3 + 0x1048) == 0) {
    _DAT_156e = _DAT_1042;
    *psVar4 = _DAT_14de + _DAT_1579;
    for (sVar5 = 0; sVar5 != 2; sVar5 = sVar5 + 1) {
    }
    DAT_1036 = DAT_00a6;
    _DAT_1042 = _DAT_156e;
    return;
  }
  _DAT_156e = *psVar4;
  *psVar4 = -1;
  *psVar4 = _DAT_156e + _DAT_14de;
  return;
}


// ---- FUN_88d0 @ 88d0 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_88d0(void)

{
  if ((DAT_1002 & 4) == 0) {
    if ((DAT_009e & 1) != 0) {
      DAT_1568 = DAT_1568 + '\x01';
      DAT_009e = DAT_009e & 0xfe;
    }
  }
  else if ((DAT_009e & 1) == 0) {
    DAT_1568 = DAT_1568 + '\x01';
    DAT_009e = DAT_009e | 1;
  }
  _DAT_1569 = _DAT_1569 + 1;
  if (0x158 < _DAT_1569) {
    DAT_1407 = DAT_1568;
    _DAT_1569 = 0;
    DAT_1568 = '\0';
  }
  return;
}


// ---- FUN_8908 @ 8908 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8908(void)

{
  undefined1 uVar1;
  char cVar2;
  undefined1 extraout_B;
  short sVar3;
  undefined1 extraout_B_00;
  byte bVar4;
  ushort uVar5;
  
  uVar1 = FUN_b209();
  _DAT_1408 = CONCAT11(uVar1,extraout_B);
  if (((((DAT_0053 & 2) == 0) && (_DAT_1408 < 100)) && (_DAT_1408 = 0x10, (DAT_0054 & 8) != 0)) &&
     (DAT_1442 != 0)) {
    DAT_007e = DAT_007e | 1;
  }
  else {
    DAT_007e = DAT_007e & 0xfe;
  }
  if (0x1f < DAT_1442) {
    if ((DAT_007e & 1) == 0) {
      sVar3 = _DAT_14e5 - _DAT_1408;
      if (_DAT_14e5 < _DAT_1408) {
        sVar3 = (byte)~(byte)sVar3 + 1;
      }
      if ((byte)(sVar3 << 1) < 0x30) goto LAB_8956;
    }
    DAT_0047 = DAT_0047 | 2;
  }
LAB_8956:
  _DAT_14e5 = _DAT_1408;
  uVar1 = FUN_802c();
  sVar3 = CONCAT11(uVar1,extraout_B_00) + _DAT_1577;
  cVar2 = (char)((ushort)sVar3 >> 8);
  uVar5 = CONCAT11(cVar2 >> 1 | CARRY2(CONCAT11(uVar1,extraout_B_00),_DAT_1577) << 7,
                   (char)sVar3 >> 1 | cVar2 << 7);
  _DAT_1577 = uVar5;
  if (uVar5 < 0x7c) {
    uVar5 = 0x7c;
  }
  else if (0xff86 < uVar5) {
    uVar5 = 0xff86;
  }
  bVar4 = (byte)(uVar5 + 0x79);
  _DAT_144b = CONCAT11((char)(uVar5 + 0x79 >> 8) - (bVar4 < DAT_1576),bVar4 - DAT_1576);
  return;
}


// ---- FUN_8990 @ 8990 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8990(void)

{
  undefined1 uVar1;
  byte bVar2;
  undefined1 extraout_B;
  
  if ((DAT_0054 & 8) == 0) {
    return;
  }
  if ((DAT_007e & 1) == 0) {
    _DAT_005b = _DAT_144b;
    FUN_8001();
    DAT_005f = 0;
    _DAT_0060 = _DAT_1455;
    if (((char)((ushort)_DAT_1455 >> 8) == '\0') && ((byte)_DAT_1455 < 0x40)) {
      _DAT_0060 = 0x40;
    }
    DAT_0062 = 0;
    uVar1 = FUN_8057();
    _DAT_1413 = CONCAT11(uVar1,extraout_B);
  }
  else {
    if (0x27 < DAT_1460) {
      _DAT_1413 = 0;
      return;
    }
    bVar2 = DAT_ff8d;
    if ((DAT_0053 & 1) == 0) {
      bVar2 = DAT_ffa2;
    }
    _DAT_1413 = (ushort)bVar2 << 8;
  }
  _DAT_150c = _DAT_1413;
  bVar2 = FUN_809f();
  if (bVar2 < DAT_150c) {
    if (DAT_f9ff <= DAT_14d1) {
      DAT_00b0 = DAT_00b0 | 0x10;
      _DAT_1413 = 0;
      return;
    }
  }
  else {
    DAT_14d1 = 0;
    DAT_00b0 = DAT_00b0 & 0xef;
  }
  if (_DAT_1413 <= _DAT_14b3) {
    _DAT_1413 = _DAT_14b3;
  }
  if (_DAT_14b5 < _DAT_1413) {
    _DAT_1413 = _DAT_14b5;
  }
  return;
}


// ---- FUN_8a26 @ 8a26 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8a26(void)

{
  undefined1 extraout_B;
  undefined1 uStack0000;
  
  _DAT_0060 = _DAT_14b7;
  _DAT_005b = _DAT_1413;
  uStack0000 = FUN_8001();
  _DAT_005b = _DAT_1482;
  FUN_8001(-DAT_0060);
  _DAT_1482 = CONCAT11(uStack0000,extraout_B) + _DAT_005b;
  return;
}


// ---- FUN_8a49 @ 8a49 ----

void FUN_8a49(void)

{
  if ((DAT_0053 & 2) == 0) {
    DAT_004f = DAT_004f & 0xfe;
    FUN_8ad9();
    if (0x3b < DAT_1453) {
      return;
    }
  }
  else {
    FUN_8a6a();
  }
  if (DAT_142e < 0x10) {
    FUN_8a92();
  }
  return;
}


// ---- FUN_8a6a @ 8a6a ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8a6a(void)

{
  char cVar1;
  byte extraout_B;
  
  if ((DAT_004f & 1) == 0) {
    DAT_142e = 0;
    DAT_004f = DAT_004f | 1;
  }
  _DAT_005b = _DAT_1413;
  FUN_8001();
  cVar1 = FUN_8001();
  _DAT_1411 = CONCAT11(cVar1 + CARRY1(extraout_B,DAT_142c),extraout_B + DAT_142c) + _DAT_1450;
  return;
}


// ---- FUN_8a92 @ 8a92 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 FUN_8a92(void)

{
  byte bVar1;
  undefined1 uVar2;
  
  uVar2 = 0xfe;
  DAT_142d = FUN_809f();
  if (0xc < DAT_1442) {
    bVar1 = DAT_ff82;
    if (DAT_1442 < 0x30) {
      bVar1 = (DAT_1442 - 0xc) * -6;
    }
    DAT_142d = (byte)((ushort)DAT_142d * (ushort)bVar1 >> 8);
  }
  if (DAT_142e < 10 || (byte)(DAT_142e - 10) == '\0') {
    bVar1 = 100;
  }
  else {
    bVar1 = (DAT_142e - 10) * -0x14 + 100;
  }
  if (_DAT_1411 <= (ushort)DAT_142d * (ushort)bVar1) {
    _DAT_1411 = (ushort)DAT_142d * (ushort)bVar1;
  }
  return uVar2;
}


// ---- FUN_8ad9 @ 8ad9 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8ad9(void)

{
  char cVar1;
  byte bVar2;
  byte extraout_B;
  
  _DAT_005b = _DAT_1482;
  if (DAT_1470 != '\0') {
    DAT_1470 = DAT_1470 + -1;
    goto LAB_8b29;
  }
  bVar2 = DAT_ff02;
  if ((DAT_0051 & 4) != 0) {
    bVar2 = DAT_ff02 - 5;
  }
  if (bVar2 < DAT_140c) {
    bVar2 = 0x3c;
    if ((DAT_0051 & 4) != 0) {
      bVar2 = 0x40;
    }
    if (DAT_1460 <= bVar2) {
      if (DAT_ff04 != 0) {
        bVar2 = DAT_ff04;
        if ((DAT_0051 & 4) == 0) {
          bVar2 = DAT_ff04 + 0x10;
        }
        if (DAT_1442 <= bVar2) goto LAB_8b23;
      }
      if ((DAT_0051 & 4) == 0) {
        DAT_0051 = DAT_0051 | 4;
        DAT_1470 = '2';
      }
      goto LAB_8b29;
    }
  }
LAB_8b23:
  DAT_0051 = DAT_0051 & 0xfb;
  _DAT_005b = _DAT_1413;
LAB_8b29:
  _DAT_14f2 = _DAT_005b;
  FUN_8001();
  cVar1 = FUN_8001();
  _DAT_1411 = CONCAT11(cVar1 + CARRY1(extraout_B,DAT_142c),extraout_B + DAT_142c) + _DAT_1450;
  return;
}


// ---- FUN_8b55 @ 8b55 ----

/* WARNING: Removing unreachable block (RAM,0x8ce1) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_8b55(void)

{
  char cVar1;
  byte bVar2;
  undefined1 uVar3;
  byte bVar4;
  
  uVar3 = (undefined1)(_DAT_140a << 1);
  FUN_8bab((char)((ushort)(_DAT_140a << 1) >> 8),uVar3,(ushort)DAT_ffb4 * 2 + -6);
  bVar2 = DAT_1407;
  DAT_1542 = uVar3;
  if (DAT_1407 == 0) {
    if ((DAT_1460 < DAT_ffe9) || (DAT_1413 < DAT_feea)) {
      DAT_1543 = 0;
      goto LAB_8bc1;
    }
    DAT_0050 = DAT_0050 | 0x80;
    bVar2 = DAT_0050 < 0x85;
    if (!(bool)bVar2) {
      bVar2 = (byte)_DAT_140a & 1;
      bVar4 = (byte)(_DAT_140a << 1);
      FUN_8bab((char)((ushort)(_DAT_140a << 1) >> 8),bVar4,(ushort)DAT_ffe9 << 1);
      bVar2 = bVar2 & 0xf1;
      DAT_1543 = bVar4;
    }
  }
  else {
    FUN_8ba0();
    DAT_1543 = bVar2;
LAB_8bc1:
    DAT_0050 = 0;
    bVar2 = 0;
  }
  bVar4 = DAT_004f;
  if ((DAT_0053 & 1) == 0) {
    DAT_004f = DAT_004f & 0xf9;
    if ((bVar4 & 8) != 0) {
      cVar1 = DAT_fefb;
      if (DAT_1544 == 0) {
LAB_8bdb:
        cVar1 = '\0';
      }
LAB_8bdc:
      DAT_1474 = cVar1;
      DAT_004f = DAT_004f & 0xf7;
    }
LAB_8be2:
    if (DAT_1474 == '\0') {
      DAT_1544 = 0;
    }
    else {
      DAT_1544 = 0x83;
    }
    DAT_00b0 = DAT_00b0 & 0xf7;
    goto LAB_8cc0;
  }
  if ((DAT_004f & 2) == 0) {
    DAT_004f = DAT_004f | 2;
    if ((DAT_1407 < DAT_ff85) ||
       ((bVar2 = 0, (DAT_0053 & 0x40) != 0 && (bVar2 = 0, (DAT_0053 & 8) == 0)))) goto LAB_8bdb;
LAB_8c95:
    FUN_8d14();
    if ((bVar2 & 1) != 0) goto LAB_8bdb;
LAB_8c9f:
    DAT_004f = DAT_004f | 8;
    DAT_1474 = DAT_ff90 - DAT_fefa;
    if (DAT_ff90 < (byte)DAT_fefa) {
      DAT_1474 = '\0';
    }
    if (DAT_ff98 <= DAT_1460) {
      DAT_1474 = '\0';
      DAT_1544 = 0x86;
    }
  }
  else {
    if ((DAT_004f & 8) == 0) {
      if ((((DAT_0053 & 0x40) != 0) && ((DAT_0053 & 8) != 0)) && ((DAT_004f & 4) == 0)) {
        DAT_004f = DAT_004f | 4;
        goto LAB_8c95;
      }
      FUN_8d14();
      if ((bool)(bVar2 & 1)) goto LAB_8be2;
      goto LAB_8c9f;
    }
    FUN_8d14();
    cVar1 = DAT_ffde;
    if ((bool)(bVar2 & 1)) goto LAB_8bdc;
    bVar2 = 1;
    if ((DAT_1407 < DAT_ff85) || (((DAT_0053 & 0x40) != 0 && (bVar2 = 0, (DAT_0053 & 8) == 0)))) {
      FUN_8d14();
      cVar1 = DAT_ffdf;
joined_r0x8c42:
      if ((bVar2 & 1) != 0) goto LAB_8bdc;
    }
    else if ((DAT_0053 & 0x10) != 0) {
      bVar2 = 0;
      FUN_8d19();
      cVar1 = DAT_ffde;
      goto joined_r0x8c42;
    }
    if ((DAT_1474 == '\0') && (DAT_1544 != 0x86)) {
      if (DAT_1544 == 0x83) {
        DAT_1544 = 0x86;
      }
      else {
        DAT_1544 = 0x83;
        DAT_1474 = DAT_fefa;
      }
    }
  }
  DAT_00b0 = DAT_00b0 | 8;
LAB_8cc0:
  if ((char)DAT_1544 < '\0') {
    if (DAT_1544 == 0x83) {
      DAT_1541 = 0x15;
    }
    else {
      DAT_1541 = 0x3f;
    }
  }
  else {
    bVar2 = DAT_1544;
    if (DAT_1544 < DAT_1545) {
      bVar2 = DAT_1545;
    }
    DAT_1541 = 0;
    if ((((bVar2 != 0) && (DAT_1541 = 1, bVar2 != 1)) &&
        ((DAT_1541 = 9, bVar2 != 2 &&
         ((DAT_1541 = 0xb, bVar2 != 3 && (DAT_1541 = 0x1b, bVar2 != 4)))))) &&
       (DAT_1541 = 0x1f, bVar2 != 5)) {
      DAT_1541 = 0x3f;
    }
  }
  return;
}


// ---- FUN_8ba0 @ 8ba0 ----

byte FUN_8ba0(byte param_1,byte param_2)

{
  byte bVar1;
  
  bVar1 = param_1 - param_2;
  if (param_1 < param_2) {
    bVar1 = 0;
  }
  if (6 < bVar1) {
    bVar1 = 6;
  }
  return bVar1;
}


// ---- FUN_8bab @ 8bab ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8bab(undefined1 param_1,undefined1 param_2,undefined2 param_3)

{
  _DAT_005b = param_3;
  return;
}


// ---- FUN_8d14 @ 8d14 ----

byte FUN_8d14(void)

{
  char cVar1;
  
  cVar1 = FUN_809f();
  if ((DAT_140a <= (byte)-(cVar1 >> 7)) &&
     (((byte)-DAT_140a != cVar1 >> 7 || (DAT_140b <= (byte)(cVar1 << 1))))) {
    return ~(cVar1 << 1);
  }
  return 0;
}


// ---- FUN_8d19 @ 8d19 ----

byte FUN_8d19(char param_1)

{
  if ((DAT_140a <= (byte)-(param_1 >> 7)) &&
     (((byte)-DAT_140a != param_1 >> 7 || (DAT_140b <= (byte)(param_1 << 1))))) {
    return ~(param_1 << 1);
  }
  return 0;
}


// ---- FUN_8d2c @ 8d2c ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8d2c(void)

{
  byte bVar1;
  
  if ((DAT_0053 & 2) == 0) {
    bVar1 = (byte)(_DAT_1411 << 1);
    _DAT_144e = CONCAT11((char)((ushort)(_DAT_1411 << 1) >> 8) - (bVar1 < DAT_142c),bVar1 - DAT_142c
                        );
    DAT_004f = DAT_004f & 0xef;
    return;
  }
  DAT_004f = DAT_004f | 0x10;
  _DAT_144e = _DAT_1411;
  return;
}


// ---- FUN_8d4b @ 8d4b ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8d4b(void)

{
  if ((DAT_0054 & 4) != 0) {
    if ((DAT_0054 & 1) == 0) {
      _DAT_004d = _DAT_144e * 5;
      if ((DAT_004f & 0x10) == 0) {
        DAT_004f = DAT_004f & 0xdf;
      }
      else {
        DAT_004f = DAT_004f | 0x20;
      }
    }
    else {
      _DAT_004d = 0;
    }
    if (((DAT_00a0 & 0x40) != 0) && ((DAT_00c2 & 1) == 0)) {
      FUN_86da();
    }
  }
  return;
}


// ---- FUN_8d80 @ 8d80 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_8d80(undefined1 param_1,undefined1 param_2)

{
  char cVar1;
  char cVar2;
  undefined2 uVar3;
  
  cVar1 = DAT_14f0;
  uVar3 = _DAT_144e;
  FUN_8daa(DAT_14f0,param_2,_DAT_144e);
  cVar2 = DAT_14f1;
  DAT_14f0 = cVar1;
  FUN_8daa(DAT_14f1,(char)uVar3,_DAT_140a << 2);
  DAT_14f1 = cVar2;
  DAT_147a = (&DAT_fa30)[(byte)(cVar2 * '\b' + DAT_14f0)];
  return;
}


// ---- FUN_8daa @ 8daa ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

byte FUN_8daa(short param_1)

{
  byte bVar1;
  byte bVar2;
  undefined2 in_D;
  
  DAT_1405 = (byte)((ushort)in_D >> 8);
  bVar1 = DAT_1405 * '\x04';
  _DAT_1403 = CONCAT11(bVar1,bVar1 + 4);
  DAT_1406 = (byte)((ushort)param_1 >> 8);
  if (!SUB21((ushort)(param_1 << 1) >> 0xf,0)) {
    bVar2 = (byte)((ushort)(param_1 << 2) >> 8);
    if ((bVar1 <= bVar2) && (bVar2 <= (byte)(bVar1 + 4))) {
      return DAT_1405;
    }
    if (DAT_1406 < 8) {
      return DAT_1406;
    }
  }
  return 7;
}


// ---- FUN_8dd5 @ 8dd5 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8dd5(void)

{
  bool bVar1;
  byte bVar2;
  byte bVar3;
  undefined1 uVar4;
  byte bVar5;
  byte bVar6;
  undefined1 uVar7;
  char cVar8;
  byte extraout_B;
  short sVar9;
  ushort uVar10;
  undefined1 *puVar11;
  undefined1 *puVar12;
  
  uVar4 = FUN_b209();
  sVar9 = CONCAT11(uVar4,extraout_B) << 1;
  bVar6 = (byte)sVar9;
  bVar5 = (char)((ushort)sVar9 >> 8) + CARRY1(bVar6,extraout_B & 1);
  sVar9 = CONCAT11(bVar5,bVar6 + (extraout_B & 1));
  if (1 < bVar5) {
    sVar9 = 0x1ff;
  }
  _DAT_1492 = sVar9;
  sVar9 = _DAT_1492;
  bVar5 = (byte)(sVar9 << 1);
  if ((DAT_00b0 & 1) == 0) {
    DAT_00b0 = DAT_00b0 | 1;
    DAT_1494 = bVar5;
    DAT_1495 = bVar5;
    DAT_1496 = bVar5;
    DAT_1497 = bVar5;
    DAT_1498 = bVar5;
    DAT_1499 = bVar5;
    DAT_149a = bVar5;
    DAT_149b = bVar5;
    DAT_149c = bVar5;
    DAT_149d = bVar5;
  }
  bVar3 = DAT_149d;
  bVar2 = DAT_1496;
  bVar6 = DAT_1494;
  DAT_149e = DAT_149d;
  DAT_149d = DAT_149c;
  DAT_149c = DAT_149b;
  DAT_149b = DAT_149a;
  DAT_149a = DAT_1499;
  DAT_1499 = DAT_1498;
  DAT_1498 = DAT_1497;
  DAT_1496 = DAT_1495;
  DAT_1497 = bVar2;
  DAT_1494 = bVar5;
  DAT_1495 = bVar6;
  DAT_1493 = (byte)sVar9;
  DAT_1492 = (char)((ushort)sVar9 >> 8);
  if ((DAT_00b9 & 0x20) == 0) {
    if (((((DAT_0054 & 1) == 0) && ((DAT_0053 & 2) == 0)) && (99 < DAT_008f)) &&
       (((DAT_1492 == '\0' && (DAT_1493 < DAT_14a0)) &&
        ((0x95 < (byte)(DAT_14a1 + 1U) && (DAT_14a0 = 0, DAT_15e6 != 0)))))) {
      DAT_15e6 = 0;
    }
    if (((DAT_0053 & 4) != 0) && ((DAT_1442 < DAT_f7b6 || ((byte)(DAT_1442 - DAT_f7b6) < DAT_143f)))
       ) {
      DAT_15e6 = DAT_14a0;
    }
    DAT_14a2 = bVar5 - (DAT_14a0 >> 1);
    if (bVar5 < DAT_14a0 >> 1) {
      DAT_14a2 = '\0';
    }
  }
  else {
    DAT_14a0 = 0xff;
    DAT_15e6 = 0xff;
    DAT_14a2 = DAT_f691;
  }
  DAT_14a1 = 0;
  DAT_14b2 = DAT_1493;
  if (DAT_1492 != '\0') {
    DAT_14b2 = 0xff;
  }
  if ((DAT_00b9 & 0x20) == 0) {
    if (DAT_14a0 <= DAT_14b2) {
      bVar6 = DAT_f920;
      if ((DAT_0053 & 1) != 0) {
        bVar6 = DAT_f921;
      }
      if (bVar6 < (byte)(DAT_14b2 - DAT_14a0)) {
        DAT_0053 = DAT_0053 & 0xfe;
        goto LAB_8ee0;
      }
    }
    DAT_0053 = DAT_0053 | 1;
  }
LAB_8ee0:
  if (bVar5 < bVar2) {
    DAT_14a3 = 0;
    DAT_14b9 = -(bVar5 - bVar2);
  }
  else {
    DAT_14b9 = '\0';
    DAT_14a3 = bVar5 - bVar2;
  }
  DAT_14a4 = 0x80;
  bVar6 = bVar5 - bVar3;
  if (bVar5 < bVar3) {
    if (bVar6 < 0x80) {
      bVar6 = 0x80;
    }
  }
  else if (0x7f < bVar6) {
    bVar6 = 0x7f;
  }
  DAT_149f = bVar6 + 0x80;
  if ((DAT_0054 & 8) == 0) {
    _DAT_1492 = sVar9;
    return;
  }
  if ((((DAT_004a & 0xf) == 0) && (DAT_f9ec < DAT_152e)) &&
     ((DAT_f9ed <= DAT_152e ||
      (bVar1 = CARRY1(DAT_152f,DAT_f9ef), DAT_152f = DAT_152f + DAT_f9ef, bVar1)))) {
    DAT_152f = 0xff;
  }
  if ((DAT_0053 & 1) == 0) {
    if (DAT_1436 < 0x40) {
LAB_8ff8:
      DAT_1436 = 0x80;
      goto LAB_900a;
    }
    puVar11 = (undefined1 *)0xf92d;
    if (DAT_1460 < DAT_f936) {
LAB_8f98:
      if (((char)DAT_1436 < '\0') && (DAT_009f == 0)) goto LAB_900a;
      uVar4 = FUN_809f();
      uVar10 = CONCAT11(uVar4,0x40);
    }
    else {
      if (DAT_f939 <= DAT_1460) goto LAB_8ff8;
      if (DAT_14a3 < DAT_f93a) goto LAB_8f98;
      if ((DAT_f937 <= DAT_1460) && (puVar11 = (undefined1 *)0xf930, DAT_f938 <= DAT_1460)) {
        puVar11 = &DAT_f933;
      }
      puVar12 = puVar11;
      if ((DAT_f93b <= DAT_14a3) && (puVar12 = puVar11 + 1, DAT_f93c <= DAT_14a3)) {
        puVar12 = puVar11 + 2;
      }
      uVar4 = *puVar12;
      uVar7 = FUN_809f();
      uVar10 = CONCAT11(uVar7,uVar4);
    }
    _DAT_005b = CONCAT21((uVar10 >> 8) * (uVar10 & 0xff) * 2,DAT_005d);
    FUN_82d5();
    _DAT_14de = _DAT_005b;
    DAT_1436 = 0x80;
    if (DAT_1473 == '\0') {
      DAT_1473 = '$';
      DAT_009f = DAT_00a0 & 0x3f;
      bVar5 = DAT_00a1;
      if ((DAT_00a0 & 0x40) != 0) {
        bVar5 = DAT_00a3;
      }
      if ((bVar5 & DAT_009f) != 0) {
        FUN_87af();
      }
    }
  }
  else {
    if ((short)((ushort)DAT_1436 << 8) < 0) {
      DAT_1436 = 0;
    }
    if (DAT_1436 < 0x40) {
      DAT_1436 = DAT_1436 + 1;
    }
LAB_900a:
    _DAT_14de = 0;
  }
  if (DAT_1473 != '\0') {
    DAT_1473 = DAT_1473 + -1;
  }
  if ((((((short)((ushort)DAT_14a4 << 8) < 0) && (DAT_009f == 0)) && (DAT_1460 < DAT_f922)) &&
      (((bool)(DAT_14a3 >> 7) || (DAT_f92b <= (byte)(DAT_14a3 << 1))))) &&
     ((DAT_14a7 = FUN_809f(), DAT_14a7 != 0 &&
      ((DAT_14a8 = FUN_809f(), DAT_14a8 != 0 && (DAT_14a9 = FUN_809f(), DAT_14a9 != '\0')))))) {
    _DAT_005b = CONCAT21((ushort)DAT_14a7 * (ushort)DAT_14a8,DAT_005d);
    FUN_8001();
    _DAT_14a5 = _DAT_005c;
    _DAT_005b = CONCAT21(_DAT_14a5,DAT_005d);
    FUN_8001();
    _DAT_1450 = _DAT_005c;
  }
  else {
    _DAT_14a5 = 0;
    _DAT_1450 = 0;
  }
  bVar6 = DAT_00b0;
  DAT_1452 = (undefined1)((ushort)(_DAT_14a5 << 4) >> 8);
  bVar5 = DAT_14a3 << 1;
  if ((char)DAT_14a3 < '\0') {
    bVar5 = 0xff;
  }
  if (DAT_f93d <= bVar5) {
    DAT_1516 = 0;
    _DAT_1517 = 0;
    DAT_00b0 = DAT_00b0 & 0xfd;
    if ((bVar6 & 4) == 0) {
      DAT_14bf = DAT_14a2;
      DAT_14c3 = 0;
      DAT_00b0 = DAT_00b0 | 4;
    }
    if (bVar5 < DAT_14c3) {
      DAT_1516 = 0;
      _DAT_1517 = 0;
      return;
    }
    DAT_14c3 = bVar5;
    DAT_150e = FUN_809f();
    if (DAT_150e != 0) {
      DAT_1512 = FUN_809f();
      if (DAT_152f != 0xff) {
        DAT_1512 = (byte)((ushort)DAT_1512 * (ushort)DAT_152f >> 8);
      }
      if (DAT_1512 != 0) {
        DAT_150f = FUN_809f();
        if (DAT_150f != 0) {
          _DAT_005b = CONCAT21((ushort)DAT_150f * (ushort)DAT_150e,DAT_005d);
          FUN_8001();
          if ((((bool)((byte)((uint3)_DAT_005b >> 8) >> 7)) ||
              (_DAT_1514 = _DAT_005c << 2, SUB21((ushort)(_DAT_005c << 1) >> 0xf,0))) ||
             (0x3f < (byte)((ushort)_DAT_1514 >> 8))) {
            _DAT_1514 = 0x4000;
          }
          goto LAB_9116;
        }
      }
    }
    _DAT_1514 = 0;
LAB_9116:
    cVar8 = (char)((ushort)_DAT_1514 >> 8);
    DAT_1513 = cVar8 << 2;
    if ((char)(cVar8 << 1) < '\0') {
      DAT_1513 = -1;
    }
    return;
  }
  bVar5 = DAT_14b9 << 1;
  if (DAT_14b9 < '\0') {
    bVar5 = 0xff;
  }
  if (bVar5 < DAT_f93e) {
    DAT_00b0 = DAT_00b0 & 0xf9;
    return;
  }
  DAT_1513 = 0;
  _DAT_1514 = 0;
  DAT_00b0 = DAT_00b0 & 0xfb;
  if ((bVar6 & 2) == 0) {
    DAT_14bf = DAT_14a2;
    DAT_14c3 = 0;
    DAT_00b0 = DAT_00b0 | 2;
  }
  if (bVar5 < DAT_14c3) {
    DAT_1513 = 0;
    _DAT_1514 = 0;
    return;
  }
  DAT_14c3 = bVar5;
  DAT_1510 = FUN_809f();
  if ((DAT_1510 != 0) && (DAT_1512 = FUN_809f(), DAT_1512 != 0)) {
    DAT_1511 = FUN_809f();
    if (DAT_1511 != 0) {
      _DAT_005b = CONCAT21((ushort)DAT_1511 * (ushort)DAT_1510,DAT_005d);
      FUN_8001();
      if ((((bool)((byte)((uint3)_DAT_005b >> 8) >> 7)) ||
          (_DAT_1517 = _DAT_005c << 2, SUB21((ushort)(_DAT_005c << 1) >> 0xf,0))) ||
         (0xf < (byte)((ushort)_DAT_1517 >> 8))) {
        _DAT_1517 = 0x1000;
      }
      goto LAB_919b;
    }
  }
  _DAT_1517 = 0;
LAB_919b:
  DAT_1516 = (char)((ushort)_DAT_1517 >> 8) << 2;
  return;
}


// ---- FUN_91a8 @ 91a8 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_91a8(void)

{
  char cVar1;
  char cVar2;
  byte extraout_B;
  char cVar6;
  ushort uVar3;
  ushort uVar4;
  short sVar5;
  byte bVar7;
  
  _DAT_005b = 0xa6ab;
  cVar2 = FUN_8001();
  cVar1 = DAT_005d >> 7;
  DAT_005d = DAT_005d << 1;
  cVar6 = extraout_B + -cVar1;
  cVar2 = cVar2 + CARRY1(extraout_B,-cVar1);
  uVar3 = CONCAT11(cVar2,cVar6);
  _DAT_154a = _DAT_1548;
  _DAT_1548 = _DAT_1546;
  _DAT_1546 = _DAT_1534;
  _DAT_1534 = _DAT_1532;
  _DAT_1532 = _DAT_140a;
  _DAT_140a = uVar3;
  uVar4 = uVar3;
  if (cVar2 != '\0') {
    uVar4 = 0xff;
  }
  DAT_1442 = (char)uVar4;
  DAT_1460 = cVar6 * '\x04';
  sVar5 = uVar3 << 3;
  _DAT_151d = _DAT_1455;
  uVar4 = (ushort)DAT_ff05;
  if (DAT_ff05 == 0) {
    _DAT_151b = sVar5;
    if ((DAT_0053 & 1) == 0) goto LAB_9225;
    uVar4 = 8;
  }
  uVar4 = uVar4 >> 1;
  _DAT_151b = sVar5;
  do {
    bVar7 = DAT_151b;
    DAT_151b = DAT_151b >> 1;
    DAT_151c = (char)DAT_151c >> 1 | bVar7 << 7;
    bVar7 = DAT_151d;
    DAT_151d = DAT_151d >> 1;
    DAT_151e = (char)DAT_151e >> 1 | bVar7 << 7;
    bVar7 = (byte)uVar4 >> 1;
    uVar4 = (ushort)bVar7;
  } while (bVar7 != 0);
  sVar5 = (_DAT_1455 - _DAT_151d) + _DAT_151b;
LAB_9225:
  _DAT_1455 = sVar5;
  if ((((DAT_0053 & 2) == 0) && (0x1f < _DAT_14e3)) &&
     ((_DAT_14e3 * 6 < uVar3 || (uVar3 <= _DAT_14e3 << 1)))) {
    DAT_0047 = DAT_0047 | 8;
  }
  _DAT_14e3 = uVar3;
  sVar5 = uVar3 << 1;
  if ((char)((ushort)sVar5 >> 8) != '\0') {
    sVar5 = 0xff;
  }
  DAT_158c = (char)sVar5;
  return;
}


// ---- FUN_925f @ 925f ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_925f(void)

{
  byte bVar1;
  byte bVar2;
  char cVar3;
  byte bVar4;
  ushort uVar5;
  short sVar6;
  undefined1 uVar7;
  
  cVar3 = DAT_152e;
  bVar2 = DAT_00b1;
  if ((DAT_004a == 0) && (DAT_1477 = DAT_1477 + 1, DAT_1477 == 0)) {
    DAT_1477 = 0xff;
  }
  DAT_152e = cVar3;
  if (((DAT_004a & 0xf) == 0) && (DAT_152e = DAT_152e + '\x01', DAT_152e == '\0')) {
    DAT_152e = cVar3;
  }
  if (DAT_1474 != '\0') {
    DAT_1474 = DAT_1474 + -1;
  }
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_0053 & 1) != 0) {
      DAT_00b0 = DAT_00b0 | 0x40;
      goto LAB_92f6;
    }
    if ((DAT_00b0 & 0x40) != 0) {
      DAT_00b0 = DAT_00b0 & 0xbf;
      FUN_809f();
      if (DAT_140c < 0x41) {
        bVar4 = DAT_ff09;
        if (DAT_ff08 <= DAT_1477) goto joined_r0x92c2;
LAB_92d4:
        uVar5 = CONCAT11(DAT_140c,DAT_ff0a);
LAB_92d7:
        bVar4 = (byte)((ushort)bVar2 * (uVar5 & 0xff) >> 8);
      }
      else {
        bVar4 = DAT_fee5;
        if (DAT_1477 < DAT_fee4) goto LAB_92d4;
joined_r0x92c2:
        if ((DAT_1477 < bVar4) && ((byte)(DAT_1477 * '\x02') < DAT_ff0a)) {
          uVar5 = (ushort)(byte)~(DAT_1477 * '\x02' - DAT_ff0a);
          goto LAB_92d7;
        }
        bVar4 = 0;
      }
      bVar1 = bVar4 + bVar2;
      if (CARRY1(bVar4,bVar2)) {
        bVar1 = 0xff;
      }
      goto LAB_92f7;
    }
    if (_DAT_1415 != 0) {
      bVar4 = (byte)_DAT_1415;
      bVar2 = (byte)(_DAT_1415 >> 8);
      _DAT_1415 = CONCAT11(bVar2 - (bVar4 < DAT_ffc6),bVar4 - DAT_ffc6);
      if (bVar2 < (bVar4 < DAT_ffc6)) goto LAB_92f6;
      goto LAB_92fc;
    }
  }
  else {
    DAT_1477 = 0;
LAB_92f6:
    bVar1 = 0;
LAB_92f7:
    _DAT_1415 = (ushort)bVar1 * (ushort)DAT_152f & 0xff00;
LAB_92fc:
    _DAT_141e = _DAT_1415 << 2;
  }
  bVar2 = DAT_1442;
  DAT_14d3 = (byte)(_DAT_1413 - _DAT_1484 >> 8);
  if (_DAT_1413 < _DAT_1484) {
    if (DAT_14d3 < 0x80) {
      DAT_14d3 = 0x80;
    }
  }
  else if (0x7f < DAT_14d3) {
    DAT_14d3 = 0x7f;
  }
  DAT_1565 = DAT_14d3 + 0x80;
  _DAT_1484 = _DAT_1413;
  FUN_809f();
  _DAT_14b3 = (ushort)bVar2 << 8;
  sVar6 = _DAT_140a << 1;
  cVar3 = (char)((ushort)sVar6 >> 8);
  if (cVar3 != '\0') {
    sVar6 = CONCAT11(cVar3,0xff);
  }
  uVar7 = (undefined1)sVar6;
  FUN_809f();
  if (DAT_14da == 0) {
    if (DAT_14d9 < DAT_ffb2) {
      uVar5 = CONCAT11(uVar7,DAT_ffb3);
      goto LAB_9363;
    }
  }
  else if (DAT_14da < DAT_ffb0) {
    uVar5 = CONCAT11(uVar7,DAT_ffb1);
    goto LAB_9363;
  }
  uVar5 = CONCAT11(uVar7,0x40);
LAB_9363:
  _DAT_14b5 = (uVar5 >> 8) * (uVar5 & 0xff) * 4;
  if ((byte)_DAT_14b5 < DAT_ffd2) {
    DAT_0051 = DAT_0051 | 2;
  }
  else {
    DAT_0051 = DAT_0051 & 0xfd;
    if (DAT_ffcf <= (byte)_DAT_14b5) {
      DAT_1480 = DAT_ff29;
    }
  }
  if ((byte)((ushort)_DAT_14b5 >> 8) < DAT_fa0a) {
    DAT_009b = DAT_009b & 0xbf;
  }
  else {
    DAT_009b = DAT_009b | 0x40;
  }
  if ((DAT_0053 & 4) == 0) {
    if (((DAT_00b3 & 4) != 0) && (DAT_00b3 = DAT_00b3 & 0xfb, DAT_14cc < 100)) {
      DAT_1439 = DAT_ffae;
      DAT_152e = '\0';
      DAT_152f = DAT_f9ee;
    }
    DAT_14cc = 0;
  }
  else {
    DAT_00b3 = DAT_00b3 | 4;
  }
  if (DAT_149f < 0x80) {
    if (DAT_fa0c <= (byte)-(DAT_149f + 0x80)) {
      DAT_00b0 = DAT_00b0 | 0x20;
    }
  }
  else if (DAT_fa0b <= (byte)(DAT_149f + 0x80)) {
    DAT_00b0 = DAT_00b0 & 0xdf;
  }
  if ((DAT_0053 & 1) == 0) {
    if ((DAT_00b0 & 0x80) != 0) {
      DAT_00b0 = DAT_00b0 & 0x5f;
    }
  }
  else if ((DAT_00b0 & 0x80) == 0) {
    DAT_00b0 = DAT_00b0 | 0xa0;
  }
  bVar2 = 0;
  if ((DAT_00b0 & 0x20) == 0) {
    bVar2 = 8;
  }
  if (DAT_1460 < 0x24) {
    if (DAT_1460 < 0x18) {
      if (DAT_1460 < 0xc) {
        sVar6 = -0x630;
      }
      else {
        sVar6 = -0x640;
      }
    }
    else {
      sVar6 = -0x650;
    }
  }
  else {
    sVar6 = -0x660;
  }
  bVar4 = DAT_14a2 * '\x02';
  if (((bool)(DAT_14a2 >> 7)) || (0x6f < bVar4)) {
    bVar4 = 0x70;
  }
  FUN_809f(bVar4,bVar2,sVar6 + (ushort)bVar2);
  _DAT_14b7 = (ushort)bVar4 << 8;
  return;
}


// ---- FUN_944c @ 944c ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_944c(undefined1 param_1,undefined1 param_2)

{
  bool bVar1;
  byte bVar2;
  
  if ((DAT_0053 & 2) == 0) {
    if (DAT_004a != '\0') {
      return;
    }
    if (DAT_141b == 0) {
      return;
    }
    if (DAT_140c < 0x41) {
      bVar1 = DAT_141b < DAT_ffc4;
    }
    else {
      bVar1 = DAT_141b < 0x14;
    }
    if (bVar1) {
      DAT_141b = 0;
    }
  }
  else {
    bVar2 = DAT_00b1;
    FUN_809f(DAT_00b1,param_2,0xfe00);
    DAT_141b = 0xff;
    DAT_1417 = bVar2;
  }
  _DAT_1420 = (ushort)DAT_1417 * (ushort)DAT_141b * 4;
  return;
}


// ---- FUN_9487 @ 9487 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9487(void)

{
  byte bVar1;
  short sVar2;
  
  sVar2 = _DAT_1418 + _DAT_1420 + _DAT_1514;
  if ((DAT_0053 & 2) == 0) {
    sVar2 = sVar2 + _DAT_141e + _DAT_1426;
  }
  _DAT_142a = (sVar2 + _DAT_1428) - _DAT_1517;
  if (_DAT_142a == 0) {
    DAT_0088 = DAT_0088 | 0x80;
  }
  else {
    DAT_0088 = DAT_0088 & 0x7f;
  }
  _DAT_142a = _DAT_142a + _DAT_1422;
  bVar1 = (byte)((ushort)_DAT_142a >> 8);
  if (bVar1 < 0xf0) {
    if (0x3f < bVar1) {
      _DAT_142a = 0x4000;
    }
  }
  else {
    _DAT_142a = 0;
  }
  return;
}


// ---- FUN_94c1 @ 94c1 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_94c1(void)

{
  bool bVar1;
  
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_0053 & 1) == 0) {
      DAT_14aa = 0;
    }
    else if ((DAT_00b0 & 8) == 0) {
      if (DAT_14aa != 0) {
        DAT_14aa = DAT_14aa - 1;
      }
    }
    else if (DAT_14aa < DAT_ffb6) {
      DAT_14aa = DAT_14aa + 1;
    }
  }
  if (_DAT_1514 != 0) {
    bVar1 = _DAT_1514 < _DAT_f9f0;
    _DAT_1514 = _DAT_1514 - _DAT_f9f0;
    if (bVar1) {
      _DAT_1514 = 0;
    }
    DAT_1513 = (undefined1)((_DAT_1514 << 2) >> 8);
  }
  if (_DAT_1517 != 0) {
    bVar1 = _DAT_1517 < _DAT_f9f2;
    _DAT_1517 = _DAT_1517 - _DAT_f9f2;
    if (bVar1) {
      _DAT_1517 = 0;
    }
    DAT_1516 = (undefined1)((_DAT_1517 << 2) >> 8);
  }
  return;
}


// ---- FUN_9513 @ 9513 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9513(void)

{
  byte bVar1;
  undefined1 uVar2;
  byte bVar3;
  byte bVar4;
  byte extraout_B;
  undefined1 extraout_B_00;
  undefined1 extraout_B_01;
  undefined1 extraout_B_02;
  undefined1 extraout_B_03;
  
  if ((DAT_fee1 & 1) != 0) {
    _DAT_1431 = 0x6400;
    return;
  }
  FUN_b209();
  DAT_1400 = extraout_B;
  if ((DAT_0053 & 2) == 0) {
    if ((((DAT_fee0 & 0x10) != 0) && (DAT_14d6 == '\0')) && (DAT_0082 != '\0')) {
      DAT_145d = FUN_809f();
      DAT_14d6 = FUN_809f();
    }
    if (DAT_155f < DAT_1400) {
      DAT_155f = DAT_1400;
    }
    if (DAT_1400 < DAT_1560) {
      DAT_1560 = DAT_1400;
    }
    bVar1 = DAT_155f - DAT_1560;
    if (DAT_155f < DAT_1560) {
      bVar1 = 0;
    }
    DAT_1561 = (char)((ushort)bVar1 * (ushort)DAT_f7b9 >> 8) + DAT_1560;
    if (DAT_f7ba < DAT_1561) {
      DAT_1561 = DAT_f7ba;
    }
    if (DAT_1561 < DAT_f7bb) {
      DAT_1561 = DAT_f7bb;
    }
  }
  if (((DAT_fee0 & 0x10) == 0) || ((DAT_00cd & 8) == 0)) {
    if ((DAT_0051 & 0x20) == 0) {
      if ((DAT_0053 & 2) != 0) {
        DAT_009a = 0;
        goto LAB_98ed;
      }
      if ((DAT_fee0 & 0x10) != 0) {
        if ((((DAT_009b & 1) == 0) && (DAT_1400 < DAT_ff92)) && (DAT_009a < DAT_145d))
        goto LAB_98f0;
        if ((DAT_009b & 1) == 0) goto LAB_9657;
        if ((DAT_009b & 2) != 0) {
          if (DAT_ffa0 < DAT_1400) goto LAB_98f0;
LAB_96a4:
          DAT_009b = DAT_009b & 0xfc;
          DAT_1438 = 0;
          if (DAT_1400 < DAT_ffa0) {
            DAT_1435 = DAT_ffa1;
            DAT_0051 = DAT_0051 & 0xf7 | 0x20;
          }
          else {
            DAT_1435 = DAT_ffa0;
            DAT_0051 = DAT_0051 | 0x28;
          }
          goto LAB_96c9;
        }
        if (DAT_ffa1 < DAT_1400) goto LAB_96a4;
        goto LAB_989f;
      }
      if (0x27 < DAT_1438) {
        DAT_1438 = 0x28;
LAB_9657:
        bVar1 = DAT_ff91;
        if (DAT_1453 < 0x3c) {
          bVar1 = DAT_fee7;
        }
        if (bVar1 <= DAT_140c) {
          if ((DAT_fee0 & 0x10) != 0) goto LAB_96a4;
          if (DAT_1400 < DAT_ff92) {
            if (DAT_ff93 <= DAT_1400) {
              DAT_1437 = 0;
              goto LAB_989f;
            }
            DAT_1437 = DAT_1437 - 1;
          }
          else {
            DAT_1437 = DAT_1437 + 1;
          }
          if ((short)((ushort)DAT_1437 << 8) < 0) {
            if (DAT_1437 < 0xf6) goto LAB_96a4;
          }
          else if (9 < DAT_1437) {
            DAT_0051 = DAT_0051 | 0x40;
            goto LAB_96a4;
          }
        }
      }
      goto LAB_98f0;
    }
    if ((((DAT_0053 & 1) != 0) && (DAT_ffd1 <= DAT_1442)) && (3 < DAT_1407)) {
      DAT_1434 = 0;
      if ((DAT_0051 & 0x80) != 0) {
        _DAT_1431 = (ushort)DAT_ffd0 << 8;
        DAT_1438 = 0;
        goto LAB_990a;
      }
      DAT_1433 = DAT_1433 + 1;
      if (0x13 < DAT_1433) {
        DAT_0051 = DAT_0051 | 0x80;
      }
LAB_96c9:
      if ((DAT_0059 & 8) != 0) {
LAB_96ce:
        DAT_00af = 0;
        DAT_0087 = 0;
        _DAT_147c = 0;
        goto LAB_98ed;
      }
      if ((DAT_0053 & 1) == 0) {
        DAT_0051 = DAT_0051 & 0xef;
LAB_9733:
        DAT_00af = 0;
        if ((DAT_fef6 != 0) && (0x87 < DAT_0087)) {
          uVar2 = FUN_9911();
          _DAT_15c5 = CONCAT11(uVar2,extraout_B_01);
        }
        DAT_0087 = 0;
        _DAT_147c = 0;
      }
      else {
        DAT_0051 = DAT_0051 | 0x10;
        if (1 < DAT_1407) goto LAB_9733;
        if (DAT_140c < 0x73) {
          if ((DAT_ffd3 & 4) != 0) goto LAB_96ce;
          goto LAB_9733;
        }
        DAT_00af = DAT_00af | 0x80;
        if ((0x80 < DAT_00af) && (DAT_0087 = DAT_0087 | 0x80, 0x87 < DAT_0087)) {
          uVar2 = FUN_9911((char)((ushort)(_DAT_147c << 5) >> 8) + DAT_feec);
          _DAT_1431 = CONCAT11(uVar2,extraout_B_00);
          DAT_1438 = 0;
          goto LAB_990a;
        }
      }
      bVar4 = DAT_009b;
      bVar1 = DAT_0051;
      DAT_009b = DAT_009b & 0xf7;
      if (DAT_1400 < DAT_1435) {
        if ((DAT_0051 & 8) == 0) {
          if ((((DAT_0051 & 0x10) == 0) || (_DAT_005b = DAT_fef1, (bVar4 & 0x40) != 0)) &&
             ((_DAT_005b = DAT_feee, (DAT_0051 & 2) == 0 && (_DAT_005b = DAT_ff06, DAT_1480 != '\0')
              ))) {
            _DAT_005b = DAT_ff0c;
          }
          uVar2 = FUN_8001();
          _DAT_1431 = CONCAT11(uVar2,extraout_B_02) + _DAT_1431;
        }
        else {
          DAT_0051 = DAT_0051 & 0xf7;
          if ((char)DAT_0087 < '\0') {
            _DAT_147c = (ushort)DAT_1431 + _DAT_147c;
            DAT_0087 = DAT_0087 + 1;
            DAT_009b = bVar4 & 0xe7;
          }
          if (((((bVar1 & 0x10) == 0) || (bVar4 = DAT_fef0, (DAT_009b & 0x40) != 0)) &&
              (bVar4 = DAT_fee3, (bVar1 & 2) == 0)) && (bVar4 = DAT_ff03, DAT_1480 != '\0')) {
            bVar4 = DAT_ff2e;
          }
          bVar4 = (byte)(((ushort)bVar4 << 0xc) >> 8);
          DAT_14c2 = -(bVar4 >> 1);
          _DAT_1431 = (ushort)bVar4 * 0x100 + _DAT_1431;
          DAT_1435 = DAT_1561 + DAT_f7bc;
          if (CARRY1(DAT_1561,DAT_f7bc)) {
            DAT_1435 = DAT_1561;
          }
          if ((bVar1 & 0x40) != 0) {
            DAT_0051 = bVar1 & 0xb7;
            DAT_1435 = DAT_ffa1;
          }
        }
      }
      else if ((DAT_0051 & 8) == 0) {
        DAT_0051 = DAT_0051 | 8;
        if ((char)DAT_0087 < '\0') {
          _DAT_147c = (ushort)DAT_1431 + _DAT_147c;
          DAT_0087 = DAT_0087 + 1;
        }
        DAT_1435 = DAT_1561 - DAT_f7bc;
        if (DAT_1561 < DAT_f7bc) {
          DAT_1435 = DAT_1561;
        }
        if ((((bVar1 & 0x10) == 0) || (bVar3 = DAT_fef0, (bVar4 & 0x40) != 0)) &&
           ((bVar3 = DAT_fee2, (bVar1 & 2) == 0 && (bVar3 = DAT_ff00, DAT_1480 != '\0')))) {
          bVar3 = DAT_ffbb;
        }
        _DAT_005b = (ushort)bVar3 * 0x1000;
        DAT_14c2 = (byte)((ushort)_DAT_005b >> 9);
        _DAT_1431 = _DAT_1431 + (ushort)bVar3 * -0x1000;
        DAT_1438 = 0;
      }
      else {
        if (((((DAT_0051 & 0x10) == 0) || (_DAT_005b = DAT_fef1, (bVar4 & 0x40) != 0)) &&
            (_DAT_005b = DAT_feee, (DAT_0051 & 2) == 0)) && (_DAT_005b = DAT_ff06, DAT_1480 != '\0')
           ) {
          _DAT_005b = DAT_ff0c;
        }
        FUN_8001();
        _DAT_1431 = _DAT_1431 - _DAT_005b;
      }
LAB_989f:
      bVar1 = DAT_009b;
      if ((DAT_0051 & 0x20) != 0) {
        if (DAT_1438 < DAT_ff7e) {
          FUN_9923();
          uVar2 = FUN_9911((char)((ushort)_DAT_1431 >> 8));
          _DAT_1431 = CONCAT11(uVar2,extraout_B_03);
          return;
        }
        if ((DAT_0051 & 8) == 0) {
          DAT_009b = DAT_009b & 0xfd | 1;
        }
        else {
          DAT_009b = DAT_009b | 3;
          if (DAT_00af < 0x8a) {
            if (DAT_f7a4 <= DAT_152a) {
              DAT_009b = bVar1 | 0x23;
            }
          }
          else {
            DAT_009b = bVar1 | 0x13;
          }
        }
        if ((DAT_0040 & 0x80) == 0) {
          FUN_afba();
        }
        goto LAB_98e7;
      }
      goto LAB_98f0;
    }
    DAT_1433 = 0;
    if ((DAT_0051 & 0x80) == 0) goto LAB_96c9;
    DAT_1434 = DAT_1434 + 1;
    if (0x13 < DAT_1434) {
      DAT_0051 = DAT_0051 & 0x7f;
    }
  }
  else {
LAB_98e7:
    DAT_0051 = DAT_0051 & 0xdf;
    DAT_1437 = 0;
LAB_98ed:
    DAT_1438 = 0;
LAB_98f0:
    if ((byte)((ushort)_DAT_1431 >> 8) < 100) {
      _DAT_1431 = _DAT_1431 + 0x15;
      if ((byte)((ushort)_DAT_1431 >> 8) < 100) goto LAB_990a;
    }
    else {
      _DAT_1431 = _DAT_1431 + -0x15;
      if (99 < (byte)((ushort)_DAT_1431 >> 8)) goto LAB_990a;
    }
  }
  _DAT_1431 = 0x6400;
LAB_990a:
  DAT_009b = DAT_009b | 8;
  return;
}


// ---- FUN_9911 @ 9911 ----

byte FUN_9911(byte param_1)

{
  if (param_1 < 0x4b) {
    param_1 = 0x4b;
  }
  else if (0x7c < param_1) {
    param_1 = 0x7d;
  }
  return param_1;
}


// ---- FUN_9923 @ 9923 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9923(void)

{
  undefined1 uVar1;
  undefined1 extraout_B;
  undefined1 extraout_B_00;
  undefined1 extraout_B_01;
  undefined1 extraout_B_02;
  undefined1 extraout_B_03;
  undefined1 extraout_B_04;
  undefined1 extraout_B_05;
  undefined1 extraout_B_06;
  undefined1 extraout_B_07;
  undefined1 extraout_B_08;
  short *psVar2;
  
  if (((((DAT_0040 & 0x80) == 0) && ((DAT_007e & 1) == 0)) && ((DAT_0053 & 1) == 0)) &&
     (((DAT_0051 & 0x80) == 0 && ((DAT_0088 & 0x80) != 0)))) {
    if ((byte)(DAT_147e + 1) < 0x10) {
      DAT_147e = DAT_147e + 1;
      return;
    }
    DAT_147e = 0;
    DAT_0051 = DAT_0051 & 0xfe;
    if (CONCAT11((char)((ushort)_DAT_1431 >> 8) + DAT_14c2,(char)_DAT_1431) < 0x6400) {
      DAT_0051 = DAT_0051 | 1;
    }
    psVar2 = _DAT_1486;
    uVar1 = FUN_99b5();
    _DAT_005b = CONCAT11(uVar1,extraout_B);
    uVar1 = FUN_8001((char)((ushort)DAT_fef6 >> 8));
    _DAT_007b = CONCAT11(uVar1,extraout_B_00);
    FUN_99bf();
    uVar1 = FUN_99b5();
    uVar1 = FUN_99c8((char)((ushort)(CONCAT11(uVar1,extraout_B_01) + *psVar2) >> 8));
    *psVar2 = CONCAT11(uVar1,extraout_B_02);
    FUN_99bf();
    uVar1 = FUN_99b5();
    uVar1 = FUN_99c8((char)((ushort)(CONCAT11(uVar1,extraout_B_03) + psVar2[1]) >> 8));
    psVar2[1] = CONCAT11(uVar1,extraout_B_04);
    FUN_99bf(~DAT_147f);
    uVar1 = FUN_99b5();
    uVar1 = FUN_99c8((char)((ushort)(CONCAT11(uVar1,extraout_B_05) + psVar2[8]) >> 8));
    psVar2[8] = CONCAT11(uVar1,extraout_B_06);
    FUN_99bf(DAT_147f);
    uVar1 = FUN_99b5();
    uVar1 = FUN_99c8((char)((ushort)(CONCAT11(uVar1,extraout_B_07) + psVar2[9]) >> 8));
    psVar2[9] = CONCAT11(uVar1,extraout_B_08);
    return;
  }
  return;
}


// ---- FUN_99b5 @ 99b5 ----

char FUN_99b5(char param_1,char param_2)

{
  if ((DAT_0051 & 1) != 0) {
    param_1 = -(param_1 + (param_2 != '\0'));
  }
  return param_1;
}


// ---- FUN_99bf @ 99bf ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_99bf(void)

{
  ushort in_D;
  
  _DAT_005b = (in_D >> 8) * (in_D & 0xff);
  FUN_8001((char)((ushort)_DAT_007b >> 8));
  return;
}


// ---- FUN_99c8 @ 99c8 ----

byte FUN_99c8(byte param_1)

{
  byte bVar1;
  
  bVar1 = DAT_f6cf;
  if ((param_1 < DAT_f6cf) || (bVar1 = DAT_f6ce, DAT_f6ce <= param_1)) {
    param_1 = bVar1;
  }
  return param_1;
}


// ---- FUN_99de @ 99de ----

void FUN_99de(void)

{
  DAT_1476 = DAT_1476 + 1;
  if (DAT_1476 < 0x15) {
    DAT_0017 = DAT_0049 ^ 1;
    DAT_0049 = DAT_0017;
  }
  return;
}


// ---- FUN_99f3 @ 99f3 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_99f3(void)

{
  bool bVar1;
  char cVar2;
  byte bVar4;
  ushort uVar3;
  
  P2DDR = 0x70;
  DAT_0016 = 0xf1;
  RAMCR = 0xe7;
  if ((DAT_0088 & 1) == 0) {
    if (0x4f < DAT_1442) {
      DAT_0088 = DAT_0088 | 1;
    }
  }
  else if (DAT_1442 < 0x10) {
    DAT_0088 = DAT_0088 & 0xfe;
  }
  if ((DAT_0015 & 0x10) == 0) {
    DAT_0054 = DAT_0054 | 1;
  }
  else {
    DAT_0054 = DAT_0054 & 0xfe;
  }
  bVar4 = DAT_0053 & 5;
  if ((DAT_00b9 & 0x20) != 0) {
    if ((DAT_0017 & 2) == 0) {
      bVar4 = 0;
    }
    else {
      bVar4 = bVar4 | 1;
    }
  }
  if ((DAT_fee0 & 0x80) == 0) {
    if ((DAT_0015 & 0x20) == 0) {
      if (DAT_1469 == '\0') {
        cVar2 = '\x7f';
      }
      else {
        if (DAT_1469 < '\0') {
          DAT_1469 = '\0';
        }
        cVar2 = DAT_1469 + '\x01';
        if ((char)(DAT_1469 + '\x01') < '\0') {
          cVar2 = DAT_1469;
        }
      }
    }
    else if (DAT_1469 == '\0') {
      cVar2 = -0x80;
    }
    else {
      if (-1 < DAT_1469) {
        DAT_1469 = '\0';
      }
      cVar2 = DAT_1469 + -1;
      if (-1 < (char)(DAT_1469 + -1)) {
        cVar2 = DAT_1469;
      }
    }
    DAT_1469 = cVar2;
    uVar3 = (ushort)(DAT_0015 & 0xf0) << 8;
    bVar1 = false;
  }
  else {
    uVar3 = CONCAT11(DAT_0015,bVar4) & 0xf0fb;
    bVar1 = false;
    if ((DAT_0015 & 0x20) != 0) {
      uVar3 = uVar3 | 4;
      bVar1 = true;
    }
  }
  if ((uVar3 & 0x4000) == 0) {
    uVar3 = uVar3 | 0x10;
  }
  if (((uVar3 & 0x8000) != 0) && ((DAT_0088 & 1) == 0)) {
    uVar3 = (ushort)(byte)((byte)uVar3 | 2);
  }
  DAT_0053 = (byte)uVar3;
  if ((char)DAT_fee0 < '\0') {
    DAT_0053 = DAT_0053 | 0x40;
  }
  uVar3 = CONCAT11(DAT_2000,DAT_1520) & 0xfffc;
  if ((DAT_2000 & 0x20) == 0) {
    uVar3 = uVar3 | 1;
  }
  if ((uVar3 & 0x4000) == 0) {
    uVar3 = (ushort)(byte)((byte)uVar3 | 2);
  }
  DAT_1520 = (char)uVar3;
  if ((_DAT_140a <= (ushort)DAT_1407 * (ushort)DAT_ff2a * 8) && (!bVar1)) {
    DAT_0053 = DAT_0053 | 8;
  }
  if ((_DAT_140a <= (ushort)DAT_1407 * (ushort)DAT_ffc8 * 8) && (!bVar1)) {
    DAT_0053 = DAT_0053 | 0x80;
  }
  if (((0x7c < DAT_1407) && ((DAT_0015 & 0x80) != 0)) && ((DAT_0017 & 2) != 0)) {
    DAT_0086 = DAT_0086 + 1;
    if (DAT_0086 < 100) goto LAB_9b0b;
    DAT_0040 = DAT_0040 | 0x20;
  }
  DAT_0086 = 0;
LAB_9b0b:
  DAT_004f = DAT_004f | 0x80;
  if ((DAT_0053 & 1) == 0) {
    if (DAT_155e <= DAT_14a2) {
      DAT_155e = DAT_14a2;
    }
  }
  else {
    DAT_155e = 0;
  }
  return;
}


// ---- FUN_9b24 @ 9b24 ----

void FUN_9b24(void)

{
  byte bVar1;
  
  if ((DAT_004a == '\0') && (DAT_1538 != '\0')) {
    DAT_1538 = DAT_1538 + -1;
  }
  if ((DAT_0040 & 8) == 0) {
    if ((DAT_0054 & 8) != 0) {
      if ((DAT_00b9 & 0x20) == 0) {
        bVar1 = DAT_fa0d;
        if (((DAT_00bf & 0x80) != 0) && (bVar1 = DAT_fa0d - 0x14, DAT_fa0d < 0x14)) {
          bVar1 = 0;
        }
        if (DAT_14a2 < bVar1) {
          DAT_00bf = DAT_00bf & 0x7f;
          DAT_1538 = '\0';
        }
        else {
          if ((DAT_00bf & 0x80) == 0) {
            DAT_00bf = DAT_00bf | 0x80;
            DAT_1538 = DAT_fa0e;
          }
          if (DAT_1538 != '\0') goto LAB_9b66;
        }
      }
      goto LAB_9b77;
    }
LAB_9b66:
    DAT_0053 = DAT_0053 & 0xef;
    DAT_0084 = -DAT_ffc1;
  }
  else {
LAB_9b77:
    if ((DAT_0053 & 0x10) != 0) {
      if ((char)DAT_0084 < '\0') {
        DAT_0084 = 0;
      }
      bVar1 = DAT_0084 + 1;
      if ((char)(DAT_0084 + 1) < '\0') {
        bVar1 = DAT_0084;
      }
      DAT_0084 = bVar1;
      if (DAT_ffc0 <= bVar1) {
        DAT_009c = DAT_009c | 0x80;
      }
      goto LAB_9ba5;
    }
    if (-1 < (char)DAT_0084) {
      DAT_0084 = 0;
    }
    bVar1 = DAT_0084 - 1;
    if (-1 < (char)(DAT_0084 - 1)) {
      bVar1 = DAT_0084;
    }
    DAT_0084 = bVar1;
    if ((byte)-bVar1 < DAT_ffc1) goto LAB_9ba5;
  }
  DAT_009c = DAT_009c & 0x7f;
LAB_9ba5:
  if ((DAT_00b4 & 4) == 0) {
    if (99 < DAT_140c) {
      DAT_00b4 = DAT_00b4 | 4;
    }
  }
  else if (DAT_140c < 0x50) {
    DAT_00b4 = DAT_00b4 & 0xfb;
  }
  return;
}


// ---- FUN_9bbe @ 9bbe ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9bbe(void)

{
  bool bVar1;
  byte bVar2;
  char cVar3;
  char cVar4;
  char cVar5;
  char cVar6;
  char cVar7;
  char cVar8;
  char cVar9;
  char cVar10;
  char cVar11;
  char cVar12;
  char cVar13;
  char cVar14;
  char cVar15;
  char cVar16;
  char cVar17;
  char cVar18;
  char cVar19;
  char cVar20;
  char cVar21;
  char cVar22;
  char cVar23;
  char cVar24;
  char cVar25;
  byte bVar26;
  char cVar27;
  bool bVar28;
  char *pcVar29;
  short sVar30;
  
  cVar25 = DAT_158e;
  cVar24 = DAT_158d;
  cVar23 = DAT_158b;
  cVar22 = DAT_158a;
  cVar21 = DAT_1560;
  cVar20 = DAT_155d;
  cVar19 = DAT_155c;
  cVar18 = DAT_155b;
  cVar17 = DAT_155a;
  cVar16 = DAT_1559;
  cVar15 = DAT_1558;
  cVar14 = DAT_1557;
  cVar13 = DAT_1556;
  cVar12 = DAT_1555;
  cVar11 = DAT_1528;
  cVar10 = DAT_1525;
  cVar9 = DAT_1524;
  cVar8 = DAT_1522;
  cVar7 = DAT_1521;
  cVar6 = DAT_14db;
  cVar5 = DAT_14da;
  cVar4 = DAT_14d9;
  cVar3 = DAT_14d2;
  cVar27 = DAT_14d1;
  bVar2 = DAT_0050;
  if (((short)((ushort)DAT_0081 << 8) < 0) && (DAT_0081 = DAT_0081 + 1, DAT_0081 == 0)) {
    DAT_0081 = 0xff;
  }
  if (((short)((ushort)DAT_00c5 << 8) < 0) && (DAT_00c5 = DAT_00c5 + 1, DAT_00c5 == 0)) {
    DAT_00c5 = 0xff;
  }
  DAT_155c = DAT_155c + '\x01';
  if (DAT_155c == '\0') {
    DAT_155c = cVar19;
  }
  DAT_155d = DAT_155d + '\x01';
  if (DAT_155d == '\0') {
    DAT_155d = cVar20;
  }
  DAT_1557 = DAT_1557 + '\x01';
  if (DAT_1557 == '\0') {
    DAT_1557 = cVar14;
  }
  DAT_1558 = DAT_1558 + '\x01';
  if (DAT_1558 == '\0') {
    DAT_1558 = cVar15;
  }
  DAT_1559 = DAT_1559 + '\x01';
  if (DAT_1559 == '\0') {
    DAT_1559 = cVar16;
  }
  DAT_155a = DAT_155a + '\x01';
  if (DAT_155a == '\0') {
    DAT_155a = cVar17;
  }
  DAT_155b = DAT_155b + '\x01';
  if (DAT_155b == '\0') {
    DAT_155b = cVar18;
  }
  DAT_158a = DAT_158a + '\x01';
  if (DAT_158a == '\0') {
    DAT_158a = cVar22;
  }
  DAT_158b = DAT_158b + '\x01';
  if (DAT_158b == '\0') {
    DAT_158b = cVar23;
  }
  if (DAT_00c0 < '\0') {
    DAT_158d = DAT_158d + '\x01';
    DAT_158e = cVar25;
    if (DAT_158d == '\0') {
      DAT_158d = cVar24;
    }
  }
  else {
    DAT_158e = DAT_158e + '\x01';
    DAT_158d = cVar24;
    if (DAT_158e == '\0') {
      DAT_158e = cVar25;
    }
  }
  if ((DAT_0053 & 1) == 0) {
    DAT_14da = '\0';
    DAT_14d9 = DAT_14d9 + '\x01';
    if (DAT_14d9 == '\0') {
      DAT_14d9 = cVar4;
    }
  }
  else {
    DAT_14d9 = '\0';
    DAT_14da = DAT_14da + '\x01';
    if (DAT_14da == '\0') {
      DAT_14da = cVar5;
    }
  }
  if (DAT_1587 != '\0') {
    DAT_1587 = DAT_1587 + -1;
  }
  if (DAT_1588 != '\0') {
    DAT_1588 = DAT_1588 + -1;
  }
  bVar26 = DAT_004a + 1;
  bVar28 = (0xfe < DAT_004a || 9 < bVar26 >> 4) || 8 < bVar26 >> 4 && 9 < (bVar26 & 0xf);
  bVar1 = (byte)((DAT_004a & 0xf) + 1) >> 4 == 1 || 9 < (bVar26 & 0xf);
  if (bVar28 && bVar1) {
    bVar26 = DAT_004a + 0x67;
  }
  else if (bVar28) {
    bVar26 = DAT_004a + 0x61;
  }
  else if (bVar1) {
    bVar26 = DAT_004a + 7;
  }
  DAT_004a = bVar26;
  if (bVar26 == 0) {
    DAT_009a = DAT_009a + '\x01';
    if (DAT_009a == '\0') {
      DAT_009a = -1;
    }
    if ((0x38 < DAT_00bd) && (DAT_0065 = DAT_0065 + 1, 2 < DAT_0065)) {
      DAT_0065 = 0;
      DAT_00bd = DAT_00bd - 1;
    }
    if ((DAT_00a7 & 4) == 0) {
      DAT_1528 = DAT_1528 + '\x01';
      DAT_1524 = cVar9;
      if (DAT_1528 == '\0') {
        DAT_1528 = cVar11;
      }
    }
    else {
      DAT_1524 = DAT_1524 + '\x01';
      DAT_1528 = cVar11;
      if (DAT_1524 == '\0') {
        DAT_1524 = cVar9;
      }
    }
    if (DAT_140c < DAT_f78d) {
      DAT_1522 = '\0';
    }
    else {
      DAT_1522 = DAT_1522 + '\x01';
      if (DAT_1522 == '\0') {
        DAT_1522 = cVar8;
      }
    }
    if (((short)((ushort)DAT_00af << 8) < 0) && (DAT_00af = DAT_00af + 1, DAT_00af == 0)) {
      DAT_00af = 0xff;
    }
    if (DAT_1481 != '\0') {
      DAT_1481 = DAT_1481 + -1;
    }
    if (DAT_1467 != '\0') {
      DAT_1467 = DAT_1467 + -1;
    }
    if (DAT_155f != '\0') {
      DAT_155f = DAT_155f + -1;
    }
    DAT_1560 = DAT_1560 + '\x01';
    if (DAT_1560 == '\0') {
      DAT_1560 = cVar21;
    }
    DAT_142e = DAT_142e + '\x01';
    if (DAT_142e == '\0') {
      DAT_142e = -1;
    }
    DAT_0050 = bVar2;
    if (((short)((ushort)DAT_0050 << 8) < 0) && (DAT_0050 = DAT_0050 + 1, DAT_0050 == 0)) {
      DAT_0050 = bVar2;
    }
  }
  else {
    DAT_0050 = bVar2;
    if ((bVar26 & 0xf) != 0) {
      return;
    }
  }
  DAT_1525 = DAT_1525 + '\x01';
  if (DAT_1525 == '\0') {
    DAT_1525 = cVar10;
  }
  if ((DAT_1523 != '\0') && (DAT_1523 = DAT_1523 + '\x01', DAT_1523 == '\0')) {
    DAT_1523 = -1;
  }
  DAT_1471 = (char)_DAT_1457 - (char)_DAT_140a;
  _DAT_1457 = _DAT_140a;
  if (DAT_1480 != '\0') {
    DAT_1480 = DAT_1480 + -1;
  }
  DAT_14d2 = cVar3;
  if ((DAT_14d2 != '\0') && (DAT_14d2 = DAT_14d2 + '\x01', DAT_14d2 == '\0')) {
    DAT_14d2 = cVar3;
  }
  if (((short)((ushort)DAT_0099 << 8) < 0) && (DAT_0099 = DAT_0099 + 1, DAT_0099 == 0)) {
    DAT_0099 = 0xff;
  }
  DAT_152a = DAT_152a + '\x01';
  if (DAT_152a == '\0') {
    DAT_152a = -1;
  }
  DAT_1521 = cVar7;
  if (((DAT_00a8 & 1) != 0) && (DAT_1521 = DAT_1521 + '\x01', DAT_1521 == '\0')) {
    DAT_1521 = cVar7;
  }
  DAT_1555 = DAT_1555 + '\x01';
  if (DAT_1555 == '\0') {
    DAT_1555 = cVar12;
  }
  DAT_1556 = DAT_1556 + '\x01';
  if (DAT_1556 == '\0') {
    DAT_1556 = cVar13;
  }
  DAT_1454 = DAT_1454 + '\x01';
  if (DAT_1454 == '\0') {
    DAT_1454 = -1;
  }
  if (DAT_14ab != 0xff) {
    bVar2 = DAT_fa05;
    if (DAT_1460 < DAT_fa06) {
      bVar2 = DAT_fa04;
    }
    bVar28 = CARRY1(DAT_14ab,bVar2);
    DAT_14ab = DAT_14ab + bVar2;
    if (bVar28) {
      DAT_14ab = 0xff;
    }
  }
  if (DAT_1439 != '\0') {
    DAT_1439 = DAT_1439 + -1;
  }
  DAT_14db = DAT_14db + '\x01';
  if (DAT_14db == '\0') {
    DAT_14db = cVar6;
  }
  DAT_1438 = DAT_1438 + '\x01';
  if (DAT_1438 == '\0') {
    DAT_1438 = -1;
  }
  if (((short)((ushort)DAT_14c9 << 8) < 0) && (DAT_14c9 = DAT_14c9 + 1, DAT_14c9 == 0)) {
    DAT_14c9 = 0xff;
  }
  if (((short)((ushort)DAT_14c4 << 8) < 0) && (DAT_14c4 = DAT_14c4 + 1, DAT_14c4 == 0)) {
    DAT_14c4 = 0xff;
  }
  if (((short)((ushort)DAT_0085 << 8) < 0) && (DAT_0085 = DAT_0085 + 1, DAT_0085 == 0)) {
    DAT_0085 = 0xff;
  }
  DAT_14d1 = DAT_14d1 + '\x01';
  if (DAT_14d1 == '\0') {
    DAT_14d1 = cVar27;
  }
  DAT_1539 = DAT_1539 + '\x01';
  DAT_153a = DAT_153a + '\x01';
  if ((DAT_0054 & 1) == 0) {
    DAT_1475 = 0;
    DAT_0049 = DAT_0049 | 0x80;
  }
  else {
    DAT_1475 = DAT_1475 + 1;
    if (0x3b < DAT_1475) {
      pcVar29 = &DAT_15c0;
      cVar27 = '\0';
      do {
        pcVar29 = pcVar29 + 1;
        cVar27 = cVar27 + *pcVar29;
      } while (pcVar29 != (char *)0x17ff);
      DAT_15c0 = -cVar27;
      _DAT_15f5 = 0x6997;
      DAT_0049 = DAT_0049 & 0x7f;
      DAT_0017 = DAT_0049;
      RAMCR = RAMCR & 0xfe;
      TCSR = TCSR & 0xe3;
      P3SCR = P3SCR & 0xf7;
      do {
        sVar30 = 0;
        do {
          sVar30 = sVar30 + 1;
        } while (sVar30 != 0xb6e);
        DAT_1476 = 0;
        FUN_99de();
      } while ((DAT_0015 & 0x10) == 0);
      vec_RESET();
      return;
    }
  }
  if (((DAT_0044 & 8) == 0) && (0x77 < DAT_1442)) {
    DAT_0044 = DAT_0044 | 10;
  }
  if (((DAT_0044 & 4) == 0) && (((DAT_fee0 & 1) != 0 || (9 < DAT_1407)))) {
    DAT_0044 = DAT_0044 | 4;
  }
  if ((DAT_0054 & 8) != 0) {
    DAT_0044 = DAT_0044 | 3;
  }
  if (0xa4 < DAT_140c) {
    DAT_0044 = DAT_0044 & 0xfe;
  }
  return;
}


// ---- FUN_9e5d @ 9e5d ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9e5d(void)

{
  undefined2 *puVar1;
  
  if ((DAT_0054 & 8) != 0) {
    if (_DAT_140a == 0) {
      DAT_14c8 = DAT_14c8 & 0x7f;
    }
    DAT_0056 = DAT_0056 + 1;
    if ((99 < DAT_0056) && (DAT_14c4 = 0, 0x95 < DAT_0056)) {
      if ((DAT_0054 & 1) == 0) {
        DAT_0044 = DAT_0044 & 0xf0;
      }
      DAT_0040 = DAT_0040 | 6;
      puVar1 = (undefined2 *)&DAT_0048;
      do {
        *puVar1 = 0;
        puVar1 = puVar1 + 1;
      } while (puVar1 != (undefined2 *)0x140);
      puVar1 = (undefined2 *)&DAT_1400;
      do {
        *puVar1 = 0;
        puVar1 = puVar1 + 1;
      } while (puVar1 != (undefined2 *)&DAT_15c0);
      if ((DAT_0040 & 1) == 0) {
        _DAT_013e = 0xae3e;
        FUN_ae5e();
        _DAT_013e = 0xae41;
        FUN_ae98();
        _DAT_013e = 0xae44;
        FUN_b00d();
        _DAT_013e = 0xae48;
        FUN_b148();
        _DAT_013e = 0xae4b;
        FUN_b264();
        _DAT_013e = 0xae4e;
        FUN_b138();
        FUN_b0e2();
        return;
      }
      _DAT_013e = 0xae54;
      FUN_b0d6();
      _DAT_013e = 0xae57;
      FUN_ae98();
      _DAT_013e = 0xae5a;
      FUN_b00d();
      FUN_b0e2();
      return;
    }
  }
  return;
}


// ---- FUN_9e94 @ 9e94 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_9e94(void)

{
  undefined2 uVar1;
  undefined2 uVar2;
  byte bVar3;
  short sVar4;
  ushort uVar5;
  char cVar6;
  byte bVar7;
  byte bVar8;
  short *psVar9;
  
  bVar8 = DAT_1566;
  bVar3 = DAT_00ae;
  DAT_1566 = bVar8;
  if (((DAT_004a & 0xf) == 0) && (DAT_1566 = DAT_1566 + 1, DAT_1566 == 0)) {
    DAT_1566 = bVar8;
  }
  DAT_1530 = DAT_143b;
  DAT_00ae = DAT_00ae & 0xe7;
  if ((bVar3 & 0x20) != 0) {
    DAT_00ae = DAT_00ae | 0x10;
  }
  bVar3 = DAT_1460;
  if (0x6f < DAT_1460) {
    bVar3 = 0x70;
  }
  FUN_809f();
  bVar8 = DAT_143d;
  if ((DAT_0053 & 4) == 0) {
    DAT_143d = DAT_143d + 1;
    if (DAT_143d == 0) {
      DAT_143d = bVar8;
    }
    if (((((DAT_143d < DAT_f6ca) || (DAT_1460 < DAT_f7e7)) || (DAT_f7e8 <= DAT_1460)) ||
        ((DAT_1471 < '\0' && (DAT_f6d0 <= (byte)-DAT_1471)))) || ((DAT_0053 & 1) != 0))
    goto LAB_9f10;
    if ((DAT_00ae & 0x80) == 0) {
      if (((DAT_140c < DAT_f7e9) || (DAT_f7ea <= DAT_140c)) ||
         ((DAT_1407 < DAT_f6cb || (DAT_f7eb <= DAT_1407)))) goto LAB_9f66;
      if ((DAT_149f < 0x80) || ((byte)(DAT_149f + 0x80) < DAT_f6d1)) {
LAB_9f4e:
        if ((DAT_f6cc <= DAT_14d9) || (DAT_14a2 < DAT_f6cd)) goto LAB_9f66;
      }
      else {
        bVar8 = DAT_149e - (DAT_14a0 >> 1);
        if (DAT_149e < DAT_14a0 >> 1) {
          bVar8 = 0;
        }
        if (DAT_f6d2 <= bVar8) goto LAB_9f4e;
      }
      if ((DAT_0053 & 0x80) == 0) {
        DAT_00ae = DAT_00ae | 0x80;
      }
      goto LAB_9f66;
    }
    DAT_1531 = DAT_1531 + 1;
    if (DAT_1531 <= DAT_f7e5) goto LAB_9f66;
    if (DAT_f7e6 < DAT_1531) goto LAB_9f10;
  }
  else {
    DAT_143d = 0;
LAB_9f10:
    DAT_1531 = 0;
    DAT_00ae = DAT_00ae & 0x3f;
LAB_9f66:
    DAT_00ae = DAT_00ae | 8;
  }
  bVar8 = DAT_00ae;
  _DAT_154c = _DAT_140a - _DAT_154a;
  DAT_143c = bVar3;
  if (_DAT_140a < _DAT_154a) {
    DAT_00ae = DAT_00ae | 0x20;
    if (((bVar8 & 8) == 0) && ((bVar8 & 0x40) != 0)) {
      bVar3 = DAT_1530 * '\x02';
      if (0x6f < bVar3) {
        bVar3 = 0x70;
      }
      FUN_809f();
      _DAT_005b = (ushort)bVar3 * (ushort)DAT_143c;
      sVar4 = -_DAT_154c;
      cVar6 = (char)((ushort)sVar4 >> 8);
      if (cVar6 != '\0') {
        sVar4 = CONCAT11(cVar6,0xff);
      }
      FUN_82d5();
      sVar4 = CONCAT11((char)sVar4,(char)sVar4) << 3;
      cVar6 = (char)((ushort)sVar4 >> 8);
      if ((cVar6 != '\0') || (DAT_f7e2 <= (byte)sVar4)) {
        sVar4 = CONCAT11(cVar6,DAT_f7e2);
      }
      DAT_1530 = (char)sVar4 + DAT_1530;
    }
  }
  else {
    if (_DAT_154c != 0) {
      DAT_00ae = DAT_00ae & 0xdf;
    }
    if ((DAT_00ae & 8) == 0) {
      if ((DAT_00ae & 0x40) == 0) {
        if ((DAT_00ae & 0x10) == 0) goto LAB_a00d;
        DAT_00ae = DAT_00ae | 0x40;
      }
      bVar3 = DAT_1530 * '\x02';
      if (0x6f < bVar3) {
        bVar3 = 0x70;
      }
      FUN_809f();
      _DAT_005b = (ushort)bVar3 * (ushort)DAT_143c;
      cVar6 = (char)((ushort)_DAT_154c >> 8);
      sVar4 = _DAT_154c;
      if (cVar6 != '\0') {
        sVar4 = CONCAT11(cVar6,0xff);
      }
      FUN_82d5();
      sVar4 = CONCAT11((char)sVar4,(char)sVar4) << 3;
      cVar6 = (char)((ushort)sVar4 >> 8);
      if ((cVar6 != '\0') || (DAT_f7e3 <= (byte)sVar4)) {
        sVar4 = CONCAT11(cVar6,DAT_f7e3);
      }
      DAT_1530 = DAT_1530 - (char)sVar4;
    }
  }
LAB_a00d:
  bVar3 = DAT_0088;
  DAT_1589 = (DAT_1530 - DAT_143b) + -0x80;
  if ((DAT_007d & 8) == 0) {
    bVar8 = DAT_1460;
    if ((DAT_1460 < DAT_feff) || (bVar8 = DAT_1413, DAT_1413 < DAT_ff74)) {
      DAT_007f = DAT_007f & 0xfe;
    }
    else {
      DAT_007f = DAT_007f | 1;
    }
    if ((DAT_0088 & 0x20) != 0) {
      DAT_0088 = DAT_0088 & 0xdf;
      if (bVar8 < 0x7d) {
        _DAT_15ee = 0;
        _DAT_15f0 = 0;
        _DAT_14c5 = 0;
        DAT_007f = DAT_007f & 0xfe;
        DAT_0088 = bVar3 & 0x9f;
      }
      else {
        DAT_0088 = DAT_0088 | 0x40;
      }
    }
  }
  else {
    DAT_007f = DAT_007f & 0xfe;
    FUN_a1d5();
    if ((DAT_0088 & 0x20) == 0) {
      _DAT_1461 = _DAT_15ee;
      if (DAT_f7be < DAT_1460) {
        _DAT_1461 = _DAT_15f0;
      }
      DAT_0088 = DAT_0088 | 0x20;
      DAT_1566 = 0;
    }
    if ((char)DAT_1566 < '\0') {
      if (0x89 < DAT_1566) goto LAB_a04f;
    }
    else if (DAT_f7bd <= DAT_1566) {
LAB_a04f:
      DAT_1566 = 0x80;
      psVar9 = (short *)&DAT_15ee;
      if (DAT_f7be <= DAT_1460) {
        psVar9 = (short *)&DAT_15f0;
      }
      uVar5 = *psVar9 + _DAT_1461;
      *psVar9 = CONCAT11((char)((short)uVar5 >> 9),
                         (char)uVar5 >> 1 | (char)((uVar5 & 0x101) >> 8) << 7);
    }
  }
  uVar1 = _DAT_14eb;
  cVar6 = DAT_0080;
  DAT_0080 = 0;
  if (((((DAT_0053 & 2) == 0) && (0x7c < DAT_008f)) && (DAT_1460 < 100)) && ((DAT_007f & 0x20) == 0)
     ) {
    _DAT_1461 = (ushort)DAT_ffc5 << 8;
    DAT_00ab = DAT_00ab | 0x10;
    DAT_007f = DAT_007f & 0x7e;
    DAT_15d5 = 0;
  }
  else {
    for (; cVar6 != '\0'; cVar6 = cVar6 + -1) {
      _DAT_1461 = _DAT_1461 - _DAT_ffb8;
    }
  }
  if ((DAT_004a & 0xf) == 0) {
    _DAT_1461 = _DAT_1461 + 0x1a;
  }
  cVar6 = (char)((ushort)_DAT_14eb >> 8);
  FUN_a124(cVar6,(char)_DAT_14eb,(ushort)DAT_145f << 8);
  uVar2 = _DAT_14ed;
  _DAT_14eb = uVar1;
  if ((DAT_007f & 0x40) == 0) {
    FUN_a124(DAT_14ed,(char)_DAT_14ed,(ushort)DAT_145e << 8);
    _DAT_14ed = uVar2;
    FUN_a146();
    return;
  }
  if ((DAT_007f & 1) != 0) {
    _DAT_1461 = _DAT_14c5;
  }
  if (-DAT_1461 == cVar6 || -cVar6 < DAT_1461) {
    if ((char)DAT_14ed < DAT_1461) {
      _DAT_1461 = (ushort)DAT_14ed << 8;
    }
  }
  else {
    _DAT_1461 = (ushort)(byte)-cVar6 << 8;
    if (DAT_145f != 0) {
      DAT_007f = DAT_007f & 0x7f;
    }
  }
  cVar6 = (DAT_1530 - DAT_14aa) + DAT_1461;
  bVar3 = 0x46 - cVar6;
  if ('F' < cVar6) {
    bVar3 = 0;
  }
  bVar8 = DAT_ff8e;
  if ((DAT_f679 <= DAT_14a3) && (DAT_f67a <= DAT_14a2)) {
    bVar8 = DAT_f67b;
  }
  bVar7 = DAT_144d;
  if (DAT_144d < bVar8) {
    bVar7 = 0;
  }
  uVar5 = (ushort)bVar7;
  if (bVar7 <= bVar3) {
    if (((DAT_0053 & 2) == 0) && ((DAT_0059 & 0x40) != 0)) {
      bVar8 = DAT_144d + DAT_ff26;
    }
    else {
      bVar8 = DAT_144d + 10;
    }
    uVar5 = CONCAT11(bVar3,bVar8);
    if (bVar3 < bVar8) goto LAB_a1c3;
  }
  uVar5 = uVar5 << 8;
LAB_a1c3:
  DAT_140f = (byte)(uVar5 >> 8);
  if (0x77 < DAT_140f) {
    DAT_140f = 0x77;
  }
  DAT_14ea = DAT_1461 + -0x80;
  return;
}


// ---- FUN_a124 @ a124 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a124(ushort param_1)

{
  ushort in_D;
  
  _DAT_005b = in_D;
  if (param_1 != in_D) {
    if (param_1 < in_D) {
      _DAT_005b = in_D;
      if (_DAT_fa01 <= in_D) {
        _DAT_005b = in_D - _DAT_fa01;
      }
    }
    else {
      _DAT_005b = in_D;
      if (!CARRY2(in_D,_DAT_fa01)) {
        _DAT_005b = in_D + _DAT_fa01;
      }
    }
  }
  return;
}


// ---- FUN_a146 @ a146 ----

/* WARNING: Removing unreachable block (RAM,0xa1c7) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a146(void)

{
  if ((DAT_007f & 1) != 0) {
    _DAT_1461 = _DAT_14c5;
  }
  if (-DAT_1461 == DAT_14eb || -DAT_14eb < DAT_1461) {
    if ((char)DAT_14ed < DAT_1461) {
      _DAT_1461 = (ushort)DAT_14ed << 8;
    }
  }
  else {
    _DAT_1461 = (ushort)(byte)-DAT_14eb << 8;
    if (DAT_145f != '\0') {
      DAT_007f = DAT_007f & 0x7f;
    }
  }
  DAT_140f = 0;
  DAT_14ea = DAT_1461 + -0x80;
  return;
}


// ---- FUN_a1d5 @ a1d5 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a1d5(void)

{
  char cVar1;
  char extraout_B;
  char extraout_B_00;
  short sVar2;
  
  _DAT_005b = _DAT_15ee;
  if (_DAT_15ee < 0) {
    _DAT_005b = CONCAT11(-((char)((ushort)_DAT_15ee >> 8) + ((char)-(char)_DAT_15ee != '\0')),
                         -(char)_DAT_15ee);
  }
  cVar1 = FUN_82d5();
  _DAT_0060 = CONCAT11(cVar1,extraout_B);
  if (_DAT_15ee < 0) {
    _DAT_0060 = CONCAT11(-(cVar1 + (-extraout_B != '\0')),-extraout_B);
  }
  _DAT_005b = _DAT_15f0;
  if (_DAT_15f0 < 0) {
    _DAT_005b = CONCAT11(-((char)((ushort)_DAT_15f0 >> 8) + ((char)-(char)_DAT_15f0 != '\0')),
                         -(char)_DAT_15f0);
  }
  cVar1 = FUN_82d5();
  sVar2 = CONCAT11(cVar1,extraout_B_00);
  if (_DAT_15f0 < 0) {
    sVar2 = CONCAT11(-(cVar1 + (-extraout_B_00 != '\0')),-extraout_B_00);
  }
  _DAT_14c5 = sVar2 + _DAT_0060;
  return;
}


// ---- FUN_a211 @ a211 ----

/* WARNING: Removing unreachable block (RAM,0xa4c5) */
/* WARNING: Removing unreachable block (RAM,0xa4cc) */
/* WARNING: Removing unreachable block (RAM,0xa4c3) */
/* WARNING: Removing unreachable block (RAM,0xa51b) */
/* WARNING: Removing unreachable block (RAM,0xa525) */
/* WARNING: Removing unreachable block (RAM,0xa528) */
/* WARNING: Removing unreachable block (RAM,0xa52a) */
/* WARNING: Removing unreachable block (RAM,0xa52f) */
/* WARNING: Removing unreachable block (RAM,0xa520) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a211(void)

{
  bool bVar1;
  byte bVar2;
  char cVar3;
  byte bVar4;
  short sVar5;
  byte bStack0000;
  
  if ((DAT_00b5 & 0x20) == 0) {
    DAT_1445 = FUN_809f();
    sVar5 = 0x3333;
    do {
      if ((byte)((ushort)sVar5 >> 8) == DAT_15c7) goto LAB_a231;
      sVar5 = sVar5 << 1;
    } while (sVar5 != 0);
    DAT_15c7 = 0x33;
LAB_a231:
    DAT_00b5 = DAT_00b5 | 10;
  }
  FUN_a583();
  FUN_a679();
  if ((0x8f < DAT_140c) && (DAT_1477 < 10)) {
    DAT_154e = DAT_ff0e;
  }
  if ((((DAT_143f == '\0') || (DAT_f686 == 0)) || (DAT_143f == DAT_154e)) ||
     (DAT_154f = DAT_154f + 1, DAT_f686 <= DAT_154f)) {
    DAT_154f = 0;
  }
  DAT_143f = 0;
  DAT_14bd = FUN_809f();
  if (DAT_004a == 0) {
    bVar2 = FUN_809f();
    if ((DAT_00b5 & 0x20) == 0) {
      DAT_00b5 = DAT_00b5 | 0x20;
      DAT_14bb = bVar2;
    }
    if (bVar2 != DAT_14bb) {
      if (bVar2 < DAT_14bb) {
        DAT_14bb = DAT_14bb - 1;
      }
      else {
        DAT_14bb = DAT_14bb + 1;
      }
    }
  }
  if ((DAT_008f < 0x70) && ((DAT_004a & 1) != 0)) {
    return;
  }
  if (DAT_1401 < 0xe0) {
    if ((DAT_0053 & 2) == 0) {
      if ((DAT_0054 & 8) != 0) {
        if ((DAT_0053 & 1) == 0) {
          FUN_a6bb();
LAB_a30a:
          DAT_00bf = DAT_00bf & 0xf7;
LAB_a30d:
          DAT_00bf = DAT_00bf & 0xdf;
          DAT_14be = 0;
LAB_a313:
          DAT_1448 = 0;
          DAT_14c0 = 0;
          DAT_00b5 = DAT_00b5 & 0xfe;
          if (DAT_14c1 != 0) {
LAB_a322:
            DAT_14c1 = 0;
            FUN_a562();
          }
        }
        else {
          FUN_a6f9();
          if ((((DAT_0058 & 0x10) != 0) || ((DAT_0053 & 4) == 0)) &&
             (((DAT_0058 & 0x40) != 0 || (DAT_f69b < DAT_1407)))) goto LAB_a30a;
          if ((DAT_00bf & 8) == 0) {
            bVar2 = FUN_809f();
            _DAT_15b4 = (ushort)bVar2 * 10;
            DAT_00bf = DAT_00bf | 8;
          }
          if (_DAT_146a < _DAT_15b4) {
            _DAT_146a = _DAT_146a + 1;
            if (DAT_1442 < DAT_143f) {
              _DAT_146a = _DAT_15b4;
              DAT_1445 = DAT_1445 + DAT_1446;
              DAT_1446 = 0;
              goto LAB_a387;
            }
            goto LAB_a30d;
          }
LAB_a387:
          DAT_00bf = DAT_00bf | 0x20;
          if ((DAT_00c0 & 0x80) == 0) {
            if ((DAT_00c0 & 0x40) != 0) {
              DAT_00c0 = DAT_00c0 & 0xbf;
              bVar1 = DAT_1445 < DAT_f696;
              DAT_1445 = DAT_1445 - DAT_f696;
              if (bVar1) {
                DAT_1445 = 0;
              }
            }
          }
          else if ((DAT_00c0 & 0x40) == 0) {
            DAT_00c0 = DAT_00c0 | 0x40;
            bVar1 = CARRY1(DAT_1445,DAT_f695);
            DAT_1445 = DAT_1445 + DAT_f695;
            if (bVar1) {
              DAT_1445 = 0xff;
            }
          }
          if (DAT_1442 <= DAT_143f) {
            if ((byte)-(DAT_1442 - DAT_143f) < 3) goto LAB_a313;
            FUN_a729();
            DAT_00ba = DAT_00ba & 0x7f;
            if (DAT_14c1 == 0) {
              if (DAT_1449 == '\0') {
                FUN_a74e();
              }
              DAT_1449 = DAT_1449 + -1;
              goto LAB_a43f;
            }
            goto LAB_a322;
          }
          if ((byte)(DAT_1442 - DAT_143f) < 3) goto LAB_a313;
          if (((byte)(DAT_1442 - DAT_143f) < 0x38) || (DAT_14c0 = DAT_14c0 + 1, DAT_14c0 < 100)) {
            FUN_a770();
            if (DAT_1449 == '\0') goto LAB_a40c;
          }
          else {
            DAT_14c0 = 100;
LAB_a40c:
            if (DAT_1445 == 0) {
              if ((DAT_14ba == '\0') || ((byte)(DAT_1442 - DAT_143f) < DAT_f6a0)) goto LAB_a43f;
              DAT_14c1 = DAT_14c1 + 1;
            }
            else {
              DAT_1445 = DAT_1445 - 1;
            }
            DAT_1449 = '\0';
          }
          DAT_1449 = DAT_1449 + -1;
        }
LAB_a43f:
        FUN_a796();
        bStack0000 = DAT_1445;
        if (DAT_14bb < DAT_fee8) {
          cVar3 = ('\x01' - (2 < DAT_fee8)) - ((byte)(2 - DAT_fee8) < DAT_14bb);
          sVar5 = CONCAT11(cVar3,(2 - DAT_fee8) - DAT_14bb);
        }
        else {
          sVar5 = (ushort)(byte)(0x81 - DAT_14bb) << 1;
          cVar3 = (char)((ushort)sVar5 >> 8);
        }
        bVar2 = (byte)sVar5;
        if (cVar3 != '\0') {
          bVar2 = 0xff;
        }
        if (bVar2 <= DAT_1445) {
          DAT_1445 = bVar2;
        }
        FUN_a7dd();
        if (((CARRY1(DAT_153b,DAT_14bb)) ||
            (bVar2 = DAT_153b + DAT_14bb + DAT_1448, CARRY1(DAT_153b + DAT_14bb,DAT_1448))) ||
           (bVar4 = bVar2 + DAT_1446, CARRY1(bVar2,DAT_1446))) {
          bVar4 = 0xff;
        }
        if (DAT_fee8 < bVar4) {
          bVar2 = DAT_14bb;
          if (DAT_14bb < DAT_fee8) {
            bVar2 = DAT_fee8;
          }
          bVar4 = ((byte)(bVar4 - bVar2) >> 1) + bVar2;
        }
        if (0x80 < bVar4) {
          bVar4 = 0x81;
        }
        if (bVar4 < DAT_14bd) {
          bVar4 = DAT_14bd;
        }
        if (bVar4 < DAT_14c1) {
          DAT_14c1 = bVar4;
        }
        goto LAB_a4ce;
      }
    }
    else {
      _DAT_146a = (ushort)DAT_f77f * 10;
      _DAT_15b4 = _DAT_146a;
    }
    DAT_00bf = DAT_00bf & 0xdf;
  }
LAB_a4ce:
  cVar3 = DAT_15c4;
  if (DAT_15c4 == '\x01') {
    DAT_14ba = 0;
    if ((DAT_004a & 0x1f) != 0) {
      return;
    }
  }
  DAT_14ba = 0;
  DAT_15c4 = cVar3;
  if (cVar3 == '\0') {
    if ((DAT_00b5 & 2) != 0) {
      DAT_00b5 = DAT_00b5 | 8;
      goto LAB_a54d;
    }
  }
  else {
    if ((DAT_00b5 & 8) == 0) {
      if ((DAT_00b5 & 2) == 0) {
        if ((DAT_00b5 & 0x10) == 0) {
          DAT_00b5 = DAT_00b5 | 0x10;
        }
        else {
          bVar2 = DAT_15c7 & 1;
          DAT_15c7 = DAT_15c7 >> 1;
          if (bVar2 != 0) {
            DAT_15c7 = DAT_15c7 | 0x80;
          }
          DAT_15c4 = cVar3 + -1;
          if ((char)(cVar3 + -1) == '\0') {
            DAT_15c4 = cVar3;
          }
        }
      }
      else {
        DAT_00b5 = DAT_00b5 & 0xfd;
      }
      goto LAB_a54d;
    }
    DAT_00b5 = DAT_00b5 & 0xf7;
  }
  DAT_00b5 = DAT_00b5 | 2;
  bVar2 = 0x33;
  do {
    if (bVar2 == DAT_15c7) break;
    bVar1 = -1 < (char)bVar2;
    bVar2 = bVar2 << 1;
  } while (bVar1);
LAB_a54d:
  DAT_00bc = DAT_00bc & 0xf0;
  if ((DAT_00c0 & 0x80) == 0) {
    DAT_00c0 = DAT_00c0 & 0xbf;
  }
  else {
    DAT_00c0 = DAT_00c0 | 0x40;
  }
  DAT_004a = DAT_004a;
  DAT_0053 = DAT_0053;
  DAT_0054 = DAT_0054;
  DAT_0058 = DAT_0058;
  DAT_008f = DAT_008f;
  DAT_00ba = DAT_00ba;
  DAT_00bf = DAT_00bf;
  DAT_1401 = DAT_1401;
  DAT_1407 = DAT_1407;
  DAT_140c = DAT_140c;
  DAT_143f = DAT_143f;
  DAT_1442 = DAT_1442;
  DAT_1445 = DAT_1445;
  DAT_1446 = DAT_1446;
  DAT_1448 = DAT_1448;
  DAT_1449 = DAT_1449;
  DAT_1460 = DAT_1460;
  _DAT_146a = _DAT_146a;
  DAT_1477 = DAT_1477;
  DAT_14bb = DAT_14bb;
  DAT_14bd = DAT_14bd;
  DAT_14be = DAT_14be;
  DAT_14c0 = DAT_14c0;
  DAT_14c1 = DAT_14c1;
  DAT_153b = DAT_153b;
  DAT_154e = DAT_154e;
  DAT_154f = DAT_154f;
  _DAT_15b4 = _DAT_15b4;
  DAT_f686 = DAT_f686;
  DAT_f695 = DAT_f695;
  DAT_f696 = DAT_f696;
  DAT_f69b = DAT_f69b;
  DAT_f6a0 = DAT_f6a0;
  DAT_f77f = DAT_f77f;
  DAT_fee8 = DAT_fee8;
  DAT_ff0e = DAT_ff0e;
  DAT_ff1d = DAT_ff1d;
  DAT_ffad = DAT_ffad;
  DAT_ffba = DAT_ffba;
  return;
}


// ---- FUN_a562 @ a562 ----

void FUN_a562(void)

{
  DAT_1445 = DAT_fb8c;
  DAT_14ba = DAT_fb8c + DAT_14bb + DAT_1443;
  DAT_15c4 = DAT_14ba;
  if (0x80 < DAT_14ba) {
    DAT_14ba = 0x81;
    DAT_15c4 = 0x80;
  }
  if (DAT_14ba == 0) {
    DAT_15c4 = 1;
  }
  return;
}


// ---- FUN_a679 @ a679 ----

void FUN_a679(void)

{
  byte bVar1;
  
  DAT_1443 = '\0';
  bVar1 = DAT_ff2d;
  if ((DAT_00b5 & 0x40) != 0) {
    bVar1 = DAT_ff2d - 4;
  }
  if (bVar1 < DAT_1460) {
    DAT_00b5 = DAT_00b5 | 0x40;
  }
  else {
    DAT_00b5 = DAT_00b5 & 0xbf;
    if ((DAT_1520 & 1) != 0) {
      DAT_1443 = DAT_f682;
    }
    if ((DAT_0053 & 0x10) == 0) {
      if ((DAT_0053 & 0x44) == 0) {
        DAT_1443 = DAT_1443 + DAT_ff9e;
      }
    }
    else if ((DAT_0053 & 0x44) == 0) {
      DAT_1443 = DAT_1443 + DAT_f9fb;
    }
    else {
      DAT_1443 = DAT_1443 + DAT_ff9f;
    }
  }
  return;
}


// ---- FUN_a6bb @ a6bb ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a6bb(void)

{
  byte bVar1;
  ushort uVar2;
  
  bVar1 = FUN_809f();
  if (DAT_155e < DAT_f684) {
    uVar2 = 0;
  }
  else {
    uVar2 = (ushort)DAT_f685 * (ushort)(byte)(DAT_155e - DAT_f684);
    if ((char)(uVar2 >> 8) != '\0') {
      DAT_1552 = 0xff;
      goto LAB_a6eb;
    }
  }
  DAT_1552 = (undefined1)uVar2;
  bVar1 = (byte)((ushort)bVar1 * (uVar2 & 0xff) >> 8);
LAB_a6eb:
  if (DAT_1446 <= bVar1) {
    DAT_1446 = bVar1;
  }
  _DAT_146a = 0;
  bVar1 = DAT_140c;
  if ((DAT_00b5 & 0x80) != 0) {
    bVar1 = DAT_140c + 5;
  }
  if (bVar1 < 0x62) {
    DAT_1446 = 0;
    DAT_00b5 = DAT_00b5 & 0x7f;
  }
  else {
    DAT_00b5 = DAT_00b5 | 0x80;
  }
  if (DAT_1446 != 0) {
    if (DAT_1447 == '\0') {
      DAT_1447 = DAT_ffab;
      DAT_1446 = DAT_1446 - 1;
    }
    DAT_1447 = DAT_1447 + -1;
  }
  return;
}


// ---- FUN_a6f9 @ a6f9 ----

void FUN_a6f9(void)

{
  byte bVar1;
  
  bVar1 = DAT_140c;
  if ((DAT_00b5 & 0x80) != 0) {
    bVar1 = DAT_140c + 5;
  }
  if (bVar1 < 0x62) {
    DAT_1446 = '\0';
    DAT_00b5 = DAT_00b5 & 0x7f;
  }
  else {
    DAT_00b5 = DAT_00b5 | 0x80;
  }
  if (DAT_1446 != '\0') {
    if (DAT_1447 == '\0') {
      DAT_1447 = DAT_ffab;
      DAT_1446 = DAT_1446 + -1;
    }
    DAT_1447 = DAT_1447 + -1;
  }
  return;
}


// ---- FUN_a729 @ a729 ----

void FUN_a729(void)

{
  ushort in_D;
  ushort uVar1;
  short sVar2;
  
  uVar1 = (in_D >> 10) * (in_D >> 10);
  if ((char)(uVar1 >> 8) != '\0') {
    uVar1 = 0xff;
  }
  sVar2 = (ushort)DAT_ffac * (uVar1 & 0xff);
  if (((SUB21((ushort)sVar2 >> 0xf,0)) ||
      (DAT_1448 = (byte)((ushort)(sVar2 * 4) >> 8), SUB21((ushort)(sVar2 * 2) >> 0xf,0))) ||
     (0x3f < DAT_1448)) {
    DAT_1448 = 0x40;
  }
  if (DAT_14be <= DAT_1448) {
    DAT_14be = DAT_1448;
  }
  return;
}


// ---- FUN_a74e @ a74e ----

void FUN_a74e(void)

{
  DAT_1445 = DAT_1445 + 1;
  if (DAT_f69c < DAT_1445) {
    DAT_1445 = DAT_f69c;
  }
  DAT_1449 = DAT_ffad;
  if (3 < (byte)(DAT_143f - DAT_1442)) {
    DAT_1449 = DAT_ffba;
  }
  return;
}


// ---- FUN_a770 @ a770 ----

void FUN_a770(void)

{
  DAT_1448 = 0;
  if ((DAT_00b5 & 4) == 0) {
    DAT_00b5 = DAT_00b5 | 4;
  }
  else if ((DAT_1471 < '\0') && (DAT_ffa6 <= (byte)-DAT_1471)) {
    DAT_1445 = (DAT_14be >> 1) + DAT_1445;
  }
  DAT_14be = 0;
  return;
}


// ---- FUN_a796 @ a796 ----

void FUN_a796(void)

{
  if ((DAT_00bf & 0x20) == 0) {
    if (DAT_1445 < DAT_ffbf) {
      if (DAT_1444 == '\0') {
        DAT_1445 = DAT_1445 + 1;
        DAT_1444 = 0x7d;
        return;
      }
      DAT_1444 = DAT_1444 + -1;
      return;
    }
    if (DAT_f69d < DAT_1445) {
      if (DAT_14d0 == '\0') {
        DAT_1445 = DAT_1445 - 1;
        DAT_14d0 = DAT_f69e;
        return;
      }
      DAT_14d0 = DAT_14d0 + -1;
      return;
    }
  }
  DAT_14d0 = DAT_f69e;
  DAT_1444 = 0x7d;
  return;
}


// ---- FUN_a7dd @ a7dd ----

void FUN_a7dd(void)

{
  byte bVar1;
  byte bVar2;
  
  bVar2 = DAT_1445 + DAT_1443;
  if (CARRY1(DAT_1445,DAT_1443)) {
    bVar2 = 0xff;
  }
  DAT_153b = bVar2;
  DAT_153e = DAT_ffbf + DAT_ff9e;
  if (CARRY1(DAT_ffbf,DAT_ff9e)) {
    DAT_153e = 0xff;
  }
  if ((((DAT_0053 & 1) == 0) || ((DAT_0015 & 0x20) != 0)) || (DAT_1407 < DAT_f7f3)) {
LAB_a82d:
    DAT_00bf = DAT_00bf & 0xaf;
    DAT_153d = 0;
    DAT_153c = 0;
    return;
  }
  if ((DAT_00bf & 0x10) == 0) {
    if (DAT_1407 < DAT_f7f4) {
      return;
    }
    if (DAT_140c < DAT_f7f5) {
      return;
    }
    if (DAT_f7f6 <= DAT_140c) {
      return;
    }
    if (CARRY1(DAT_143f,DAT_f7f7)) {
      return;
    }
    if (DAT_1442 <= (byte)(DAT_143f + DAT_f7f7)) goto LAB_a82d;
    DAT_00bf = DAT_00bf & 0xbf | 0x10;
  }
  else {
    if ((DAT_00bf & 0x40) != 0) {
LAB_a88a:
      if (DAT_153d == 0) {
        return;
      }
      if (DAT_153c == '\0') {
        DAT_153d = DAT_153d - 1;
        if (DAT_153d == 0) {
          DAT_00bf = DAT_00bf & 0xef;
          return;
        }
        DAT_153c = DAT_f7fb;
      }
      DAT_153c = DAT_153c + -1;
      if (DAT_153d <= bVar2) {
        DAT_153b = bVar2 - DAT_153d;
        return;
      }
      DAT_153b = 0;
      DAT_153d = bVar2;
      return;
    }
    if (((DAT_1407 < DAT_f7f9) || (DAT_1442 <= (byte)(DAT_143f + DAT_f7fa))) ||
       ((DAT_00bf & 0x20) != 0)) {
      DAT_00bf = DAT_00bf | 0x40;
      goto LAB_a88a;
    }
  }
  if (DAT_153c == '\0') {
    DAT_153d = DAT_153d + 1;
    bVar1 = DAT_153e;
    if (DAT_153e < DAT_153d) goto LAB_a85b;
    DAT_153c = DAT_f7f8;
  }
  DAT_153c = DAT_153c + -1;
  bVar1 = DAT_153d;
LAB_a85b:
  DAT_153d = bVar1;
  DAT_153b = bVar2 - DAT_153d;
  if (bVar2 < DAT_153d) {
    DAT_153b = '\0';
    DAT_153d = bVar2;
  }
  return;
}


// ---- FUN_a8b7 @ a8b7 ----

void FUN_a8b7(void)

{
  byte bVar1;
  byte bVar2;
  
  if (((DAT_0053 & 0x40) != 0) || ((DAT_0040 & 4) != 0)) {
    DAT_00c1 = DAT_00c1 & 0xf7;
    goto LAB_a994;
  }
  if ((DAT_0053 & 2) != 0) goto LAB_a994;
  if ((DAT_00c1 & 0x80) == 0) {
    if (DAT_1460 < 0x14) goto LAB_a994;
    DAT_00c1 = DAT_00c1 | 0x80;
  }
  bVar1 = DAT_00c1;
  if ((DAT_00b6 & 0x60) == 0) {
    bVar2 = DAT_f67d;
    if (((DAT_00c1 & 0x40) == 0) && (bVar2 = DAT_f67d + 2, 0xfd < DAT_f67d)) {
      bVar2 = 0xff;
    }
    if (DAT_140c < bVar2) {
      DAT_00c1 = DAT_00c1 & 0xbf;
      goto LAB_a947;
    }
    bVar2 = DAT_f67e;
    if (((DAT_00c1 & 0x20) == 0) && (bVar2 = DAT_f67e + 10, 0xf5 < DAT_f67e)) {
      bVar2 = 0xff;
    }
    if (DAT_14a2 < bVar2) {
      DAT_00c1 = DAT_00c1 & 0xdf | 0x40;
      goto LAB_a947;
    }
    bVar2 = DAT_f67f;
    if (((DAT_00c1 & 0x10) == 0) && (bVar2 = DAT_f67f + 6, 0xf9 < DAT_f67f)) {
      bVar2 = 0xff;
    }
    if (DAT_1460 < bVar2) {
      DAT_00c1 = DAT_00c1 & 0xef | 0x60;
      goto LAB_a947;
    }
    DAT_00c1 = DAT_00c1 | 0x70;
    if (((DAT_141d == '\0') || ((DAT_0040 & 8) != 0)) || ((bVar1 & 8) != 0)) goto LAB_a947;
    DAT_00b4 = DAT_00b4 & 0xfd;
  }
  else {
LAB_a947:
    DAT_00b4 = DAT_00b4 | 2;
  }
  if ((DAT_00c1 & 8) == 0) {
    if ((DAT_2000 & 1) != 0) {
      if ((DAT_00c1 & 4) != 0) {
        DAT_00c3 = DAT_f67c;
        DAT_1545 = 0;
        return;
      }
      DAT_00c1 = DAT_00c1 | 4;
      return;
    }
    if ((DAT_00c1 & 4) != 0) {
      DAT_00c1 = DAT_00c1 & 0xfb;
      return;
    }
    if (((DAT_004a & 0xf) != 0) || (DAT_00c3 = DAT_00c3 + -1, DAT_00c3 != '\0')) {
      if ((DAT_00b4 & 2) != 0) {
        DAT_1545 = 0;
        return;
      }
      DAT_1545 = 3;
      return;
    }
    DAT_00c1 = DAT_00c1 | 8;
    DAT_00c3 = DAT_f67c;
  }
LAB_a994:
  DAT_00b4 = DAT_00b4 | 2;
  DAT_1545 = 0;
  return;
}


// ---- FUN_a99b @ a99b ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a99b(void)

{
  bool bVar1;
  byte bVar2;
  byte bVar3;
  short sVar4;
  char cVar5;
  ushort uVar6;
  
  bVar3 = DAT_0047;
  bVar2 = DAT_0046;
  _DAT_15e7 = CONCAT11((byte)((ushort)_DAT_00a9 >> 8) & DAT_ff15,(byte)_DAT_00a9 & DAT_ff16);
  _DAT_15e9 = CONCAT11((byte)((ushort)_DAT_00ab >> 8) & DAT_ff17,(byte)_DAT_00ab & DAT_ff18);
  DAT_00ad = DAT_00ad & DAT_ff19;
  DAT_15eb = DAT_00ad & 0xef;
  _DAT_15f7 = CONCAT11((byte)((ushort)_DAT_00c8 >> 8) & DAT_ff15,(byte)_DAT_00c8 & DAT_ff16);
  _DAT_15f9 = CONCAT11((byte)((ushort)_DAT_00ca >> 8) & DAT_ff17,(byte)_DAT_00ca & DAT_ff18);
  DAT_15fc = (undefined1)_DAT_00cc;
  DAT_15fb = (byte)((ushort)_DAT_00cc >> 8) & DAT_ff19;
  _DAT_00cc = CONCAT11(DAT_15fb,DAT_15fc);
  _DAT_00a9 = _DAT_15e7;
  _DAT_00ab = _DAT_15e9;
  _DAT_00c8 = _DAT_15f7;
  _DAT_00ca = _DAT_15f9;
  if ((DAT_0040 & 0x20) == 0) {
    if ((DAT_0046 & 8) == 0) {
      if (DAT_1401 < 0xe0) {
        DAT_14e8 = 0;
        if ((DAT_0046 & 0x40) != 0) {
          DAT_143e = DAT_143e + '\x01';
          if (DAT_143e < '\0') {
            DAT_143e = -0x80;
          }
          DAT_1472 = DAT_1472 + 1;
          if (DAT_1472 < 0x1e) {
            DAT_14e8 = 0;
            return;
          }
          goto LAB_abd6;
        }
        if ((DAT_0046 & 0x20) != 0) {
          DAT_14dd = DAT_0040;
          if ((DAT_0053 & 3) != DAT_15e1) {
            DAT_0083 = DAT_0083 ^ 0x40;
            DAT_15e1 = DAT_0053 & 3;
          }
          if (((DAT_0053 & 2) != 0) || (DAT_1407 < 10)) {
            DAT_0083 = DAT_0083 & 0xdf;
            goto LAB_ac26;
          }
LAB_ac0f:
          DAT_0083 = DAT_0083 | 0x20;
          goto LAB_ac26;
        }
        if ((DAT_0046 & 0x10) == 0) {
          if ((DAT_0051 & 0x20) == 0) {
            DAT_0083 = DAT_0083 & 0x9f;
          }
          else {
            if ((DAT_0051 & 8) == 0) {
              DAT_0083 = DAT_0083 | 0x60;
            }
            else {
              DAT_0083 = DAT_0083 & 0x9f;
            }
            if (DAT_1431 < 0x6a) {
              if (DAT_1431 < 0x5f) {
                DAT_0083 = DAT_0083 & 0xbf;
              }
            }
            else {
              DAT_0083 = DAT_0083 | 0x40;
            }
          }
          if ((DAT_0040 & 8) == 0) {
            if ((DAT_0046 & 0x80) == 0) {
              if ((DAT_0054 & 8) == 0) goto LAB_ac26;
              if (((DAT_fee0 & 0x20) != 0) &&
                 (((_DAT_15f7 != 0 || (_DAT_15f9 != 0)) || (DAT_15fb != 0)))) goto LAB_ac0a;
            }
            else if ((DAT_0054 & 8) != 0) goto LAB_ac26;
LAB_ac14:
            DAT_0083 = DAT_0083 & 0xbf;
          }
          else {
            DAT_0083 = DAT_0083 & 0xdf;
LAB_ac0a:
            DAT_0083 = DAT_0083 | 0x40;
          }
          goto LAB_ac26;
        }
        if ((DAT_004a & 0x1f) != 0) {
          DAT_14e8 = 0;
          return;
        }
        if (((DAT_0047 & 8) == 0) || (DAT_0047 = DAT_0047 & 0x6e, (bVar3 & 0x40) != 0)) {
LAB_ac8d:
          bVar2 = DAT_0047;
          if ((DAT_0047 & 4) != 0) {
            DAT_0047 = DAT_0047 & 0x7f | 0x40;
            if (DAT_15e2 == 0) {
              DAT_15e4 = 0xdb;
            }
            if (DAT_15e2 < 0x30) {
              FUN_ad05();
            }
            else {
              DAT_0047 = bVar2 & 0x3b;
              DAT_15e2 = 0;
            }
          }
        }
        else {
          if (DAT_15e2 == 0) {
            DAT_15e4 = 0xff;
          }
          if (0x2f < DAT_15e2) {
            DAT_0047 = bVar3 & 0x66;
            DAT_15e2 = 0;
            goto LAB_ac8d;
          }
          FUN_ad05();
        }
        bVar2 = DAT_0047;
        if (((DAT_0047 & 0x10) == 0) && ((DAT_0047 & 2) != 0)) {
          DAT_0047 = DAT_0047 | 0x80;
          if (DAT_15e3 == 0) {
            DAT_15e5 = 0xe7;
          }
          if (DAT_15e3 < 0x30) {
            FUN_ad05();
            goto LAB_ac26;
          }
          DAT_0047 = bVar2 & 0xfd | 0x80;
          DAT_15e3 = 0;
        }
        if ((DAT_0047 & 1) != 0) {
          DAT_0047 = DAT_0047 | 0x90;
          if (DAT_15e3 == 0) {
            DAT_15e5 = 0xaa;
          }
          if (DAT_15e3 < 0x30) {
            FUN_ad05();
            goto LAB_ac26;
          }
        }
        DAT_0047 = DAT_0047 & 0xee;
        DAT_0083 = DAT_0083 & 0xdf;
        DAT_15e3 = 0;
        goto LAB_ac26;
      }
      if (((DAT_004a & 0xf) != 0) || (DAT_14e8 = DAT_14e8 + 1, DAT_14e8 < 10)) goto LAB_ac23;
      DAT_14e8 = 0;
      DAT_0046 = DAT_0046 | 8;
      if ((bVar2 & 0x80) == 0) {
        if ((bVar2 & 0x40) == 0) {
          if ((bVar2 & 0x20) == 0) {
            if ((bVar2 & 0x10) == 0) {
              DAT_0046 = bVar2 | 0x88;
              DAT_14e9 = 0x98;
            }
            else {
              DAT_0046 = bVar2 & 0xef | 8;
              DAT_14e9 = 0xc0;
            }
          }
          else {
            DAT_0046 = DAT_0046 ^ 0x30;
            DAT_14e9 = 0x55;
            DAT_15e2 = 0;
            DAT_15e3 = 0;
          }
        }
        else {
          DAT_0046 = DAT_0046 ^ 0x60;
          DAT_14e9 = 0x54;
          if (DAT_143e < '\0') {
            _DAT_00a9 = 0;
            _DAT_00ab = 0;
            DAT_00ad = 0;
            DAT_15ed = 0;
            _DAT_00c8 = 0;
            _DAT_00ca = 0;
            _DAT_00cc = 0;
          }
          DAT_143e = '\0';
        }
      }
      else {
        DAT_0046 = DAT_0046 ^ 0xc0;
        DAT_14e9 = 0x50;
        DAT_1472 = '\0';
        DAT_1468 = 0x2b;
        _DAT_146c = 0x804;
      }
    }
    if ((DAT_004a & 0x1f) != 0) {
      return;
    }
    DAT_14e7 = DAT_14e7 + 1;
    if (4 < DAT_14e7) {
      if (DAT_14e7 == 5) {
LAB_ac1e:
        DAT_0083 = DAT_0083 | 0x60;
        goto LAB_ac26;
      }
      if (DAT_14e7 < 0xe) {
        bVar1 = (bool)(DAT_14e9 >> 7);
        DAT_14e9 = DAT_14e9 << 1;
        if (bVar1) goto LAB_ac1e;
      }
      else if ((DAT_14e7 != 0xe) && (0xf < DAT_14e7)) {
        DAT_14e7 = 0;
        DAT_0046 = DAT_0046 & 0xf7;
        DAT_15e1 = DAT_0053 & 3;
        DAT_0047 = DAT_0047 & 0xf0;
        goto LAB_ac26;
      }
    }
  }
  else if (DAT_140a == '\0') {
    if ((DAT_0040 & 0x10) != 0) goto LAB_ac1e;
  }
  else if ((DAT_0053 & 1) == 0) {
    if (DAT_1472 != '\0') {
      DAT_1468 = 0x2b;
      _DAT_146c = 0x804;
    }
LAB_abd6:
    DAT_1472 = '\0';
    DAT_1468 = DAT_1468 + 1;
    if (0x2b < DAT_1468) {
      DAT_1468 = 0;
      FUN_ad35();
    }
    sVar4 = _DAT_146e;
    if (0xf < DAT_1468) {
      cVar5 = DAT_146f;
      if (DAT_1468 < 0x1a) {
        if ((DAT_1468 & 1) != 0) {
          DAT_146f = DAT_146f << 1;
          if (cVar5 < '\0') goto LAB_ac0a;
        }
      }
      else if ((0x21 < DAT_1468) && ((DAT_1468 & 1) != 0)) {
        DAT_146e = DAT_146e << 1;
        if (sVar4 < 0) goto LAB_ac0f;
      }
    }
  }
  else {
    if (DAT_1472 != -1) {
      DAT_1472 = -1;
      DAT_1468 = 0x31;
    }
    DAT_1468 = DAT_1468 + 1;
    if (DAT_1468 < 0x32) {
      if (DAT_1468 == 0x1d) {
        _DAT_146e = CONCAT11(DAT_146f,DAT_146f);
      }
      else if (DAT_1468 != 0x31) {
        if (DAT_1468 < 0xb) goto LAB_ac23;
        if ((DAT_1468 != 0x1f) && (DAT_1468 != 0xb)) {
          if (!(bool)(DAT_1468 & 1)) goto LAB_ac14;
          bVar1 = (bool)(DAT_146e & 1);
          DAT_146e = DAT_146e >> 1;
          if (bVar1) goto LAB_aa6b;
        }
        goto LAB_ac1e;
      }
LAB_aa6b:
      DAT_0083 = DAT_0083 & 0xdf | 0x40;
      goto LAB_ac26;
    }
    _DAT_146e = CONCAT11(DAT_ff7c,DAT_ff2f);
    DAT_1468 = 0;
  }
LAB_ac23:
  DAT_0083 = DAT_0083 & 0x9f;
LAB_ac26:
  uVar6 = CONCAT11(DAT_0049,DAT_0083) & 0x9f60;
  DAT_0049 = (char)(uVar6 >> 8) + (char)uVar6;
  DAT_0017 = DAT_0049;
  return;
}


// ---- FUN_ad05 @ ad05 ----

void FUN_ad05(byte param_1,char param_2)

{
  char cVar1;
  
  cVar1 = param_2;
  if (((param_1 & 8) == 0) && (cVar1 = param_2 * '\x02', param_2 < '\0')) {
    cVar1 = cVar1 + '\x01';
    if ((DAT_0047 & 0x80) != 0) {
      DAT_0083 = DAT_0083 | 0x20;
      goto LAB_ad2e;
    }
    DAT_0083 = DAT_0083 | 0x40;
  }
  else {
    if ((DAT_0047 & 0x80) != 0) {
      DAT_0083 = DAT_0083 & 0xdf;
LAB_ad2e:
      DAT_15e3 = DAT_15e3 + '\x01';
      DAT_15e5 = cVar1;
      return;
    }
    DAT_0083 = DAT_0083 & 0xbf;
  }
  DAT_15e2 = DAT_15e2 + '\x01';
  DAT_15e4 = cVar1;
  return;
}


// ---- FUN_ad35 @ ad35 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_ad35(void)

{
  bool bVar1;
  byte bVar2;
  char cVar3;
  undefined1 *puVar4;
  
  if (((_DAT_00a9 == 0) && (_DAT_00ab == 0)) && ((DAT_00ad & 0xfe) == 0)) {
    _DAT_146c = 0x804;
    _DAT_146e = 0xf8f8;
  }
  else {
    do {
      cVar3 = (char)_DAT_146c;
      bVar2 = (byte)(_DAT_146c >> 9);
      _DAT_146c = CONCAT11(bVar2,cVar3);
      if ((bVar2 == 4) &&
         (cVar3 = cVar3 + '\x01', _DAT_146c = CONCAT11(0x80,cVar3), cVar3 == '\x05')) {
        _DAT_146c = 0x8000;
      }
      bVar2 = (byte)(_DAT_146c >> 8);
    } while ((bVar2 & *(byte *)((_DAT_146c & 0xff) + 0xa9)) == 0);
    puVar4 = (undefined1 *)0xad7e;
    while (bVar1 = (bool)(bVar2 >> 7), bVar2 = bVar2 << 1, !bVar1) {
      puVar4 = puVar4 + 1;
    }
    _DAT_146e = CONCAT11(*puVar4,(&DAT_ad83)[_DAT_146c & 0xff]);
  }
  return;
}


// ---- FUN_ad88 @ ad88 ----

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_ad88(void)

{
  if ((DAT_0040 & 0x80) != 0) {
    if ((DAT_00c4 & 1) != 0) {
                    /* WARNING: Bad instruction - Truncating control flow here */
      halt_baddata();
    }
    if ((TRCS & 8) == 0) {
      _DAT_159e = 0x8300;
      _DAT_15a0 = 0;
      TRCS = TRCS | 0x1a;
    }
  }
  return;
}


// ---- vec_SCI @ adaa ----

/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 vec_SCI(void)

{
  undefined1 in_stack_00000003;
  
  if ((DAT_0040 & 0x80) == 0) {
    return in_stack_00000003;
  }
  if ((DAT_00c4 & 1) != 0) {
                    /* WARNING: Bad instruction - Truncating control flow here */
    halt_baddata();
  }
  if ((DAT_001e & 0x50) != 0) {
    DAT_00c4 = DAT_00c4 | 2;
  }
  if ((DAT_001e & 0x80) == 0) {
    return in_stack_00000003;
  }
  DAT_159f = RX + DAT_159f;
  DAT_159e = DAT_159e - 1;
  if (DAT_159e == 0) {
    if (((DAT_00c4 & 2) != 0) || (DAT_159f != '\0')) goto LAB_ae07;
  }
  else {
    if (DAT_159e < 0x82) {
      if (0x80 < DAT_159e) {
        _DAT_15a0 = &LAB_1600 + (ushort)RX * 0x200;
        return in_stack_00000003;
      }
      *_DAT_15a0 = RX;
      _DAT_15a0 = _DAT_15a0 + 1;
      return in_stack_00000003;
    }
    if (RX == 1) {
      return in_stack_00000003;
    }
    if (RX != 4) {
LAB_ae07:
      DAT_00c4 = DAT_00c4 & 0xfd;
      TX = 0x15;
      DAT_159e = 0x83;
      DAT_159f = 0;
      return in_stack_00000003;
    }
    DAT_00c4 = DAT_00c4 | 1;
  }
  TX = 6;
  DAT_159e = 0x83;
  return in_stack_00000003;
}


// ---- vec_RESET @ ae17 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void vec_RESET(void)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)&DAT_0040;
  do {
    *puVar1 = 0;
    puVar1 = puVar1 + 1;
  } while (puVar1 != (undefined2 *)0x140);
  puVar1 = (undefined2 *)&DAT_1400;
  do {
    *puVar1 = 0;
    puVar1 = puVar1 + 1;
  } while (puVar1 != (undefined2 *)&DAT_15c0);
  if ((DAT_0040 & 1) == 0) {
    _DAT_013e = 0xae3e;
    FUN_ae5e();
    _DAT_013e = 0xae41;
    FUN_ae98();
    _DAT_013e = 0xae44;
    FUN_b00d();
    _DAT_013e = 0xae48;
    FUN_b148();
    _DAT_013e = 0xae4b;
    FUN_b264();
    _DAT_013e = 0xae4e;
    FUN_b138();
    FUN_b0e2();
    return;
  }
  _DAT_013e = 0xae54;
  FUN_b0d6();
  _DAT_013e = 0xae57;
  FUN_ae98();
  _DAT_013e = 0xae5a;
  FUN_b00d();
  FUN_b0e2();
  return;
}


// ---- FUN_ae5e @ ae5e ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_ae5e(void)

{
  byte bVar1;
  
  bVar1 = DAT_0049;
  DAT_00bc = DAT_00bc | 0x80;
  DAT_0049 = DAT_0049 | 0x80;
  if ((DAT_0040 & 4) == 0) {
    DAT_0049 = bVar1 | 0x90;
  }
  P2DATA = DAT_0048;
  DAT_0017 = DAT_0049;
  P2DDR = 0x70;
  DAT_0016 = 0xf1;
  TCSR = 0x16;
  P3SCR = 0;
  RAMCR = 0xe7;
  _DAT_001b = &DAT_1407;
  RMCR = 0xc;
  TRCS = 0;
  DAT_001e = 4;
  return;
}


// ---- FUN_ae98 @ ae98 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_ae98(void)

{
  char cVar1;
  ushort *puVar2;
  char *pcVar3;
  undefined2 *puVar4;
  
  DAT_1445 = DAT_ffbe;
  DAT_00bd = 0xac;
  DAT_007f = DAT_007f | 0x30;
  DAT_140f = 0;
  DAT_144d = 0;
  DAT_1410 = 0;
  DAT_143a = 0x60;
  DAT_004f = DAT_004f | 0x20;
  DAT_0057 = 9;
  DAT_004a = 0x99;
  DAT_004b = 0;
  DAT_14c8 = 0;
  DAT_1582 = 5;
  DAT_1431 = 100;
  DAT_148e = 100;
  DAT_1580 = 100;
  DAT_152b = 100;
  DAT_0051 = DAT_0051 | 0x20;
  DAT_1576 = 0x79;
  DAT_2000 = DAT_00bc;
  DAT_00b4 = 0x42;
  DAT_4000 = 0x42;
  DAT_00c1 = DAT_00c1 | 4;
  DAT_5000 = 0;
  DAT_00b0 = DAT_00b0 | 0x80;
  DAT_142e = 0xff;
  DAT_152e = 0xff;
  DAT_152f = 0xff;
  DAT_1560 = 0xff;
  DAT_155f = 0;
  DAT_1561 = DAT_ffa0;
  DAT_1468 = 0x2b;
  _DAT_146c = 0x804;
  if ((DAT_0040 & 4) != 0) {
    FUN_afce();
    return;
  }
  if (_DAT_15c1 == 0x55a5) {
    if (_DAT_15f5 == 0x6997) {
      cVar1 = '\0';
      pcVar3 = (char *)0x15bf;
      do {
        pcVar3 = pcVar3 + 1;
        cVar1 = cVar1 + *pcVar3;
      } while (pcVar3 != (char *)0x17ff);
      if (cVar1 == '\0') {
        if ((_DAT_15fb & 0x20) != 0) {
          DAT_009b = DAT_009b | 0x10;
        }
        DAT_14a0 = DAT_15e6 + DAT_f7b7;
        if (CARRY1(DAT_15e6,DAT_f7b7)) {
          DAT_14a0 = -1;
        }
        if (DAT_fef6 != 0) {
          DAT_004a = 0x99;
          DAT_004b = 0;
          DAT_0057 = 9;
          _DAT_00a9 = _DAT_15e7;
          _DAT_00ab = _DAT_15e9;
          DAT_00ad = DAT_15eb;
          DAT_00b4 = 0x42;
          DAT_00bd = 0xac;
          _DAT_00c8 = _DAT_15f7;
          _DAT_00ca = _DAT_15f9;
          _DAT_00cc = _DAT_15fb;
          DAT_140f = 0;
          DAT_1410 = 0;
          DAT_142e = 0xff;
          DAT_1431 = 100;
          DAT_143a = 0x60;
          DAT_144d = 0;
          DAT_1468 = 0x2b;
          _DAT_146c = 0x804;
          DAT_148e = 100;
          DAT_14c8 = 0;
          DAT_152b = 100;
          DAT_152e = 0xff;
          DAT_152f = 0xff;
          DAT_155f = 0;
          DAT_1560 = 0xff;
          DAT_1576 = 0x79;
          DAT_1580 = 100;
          DAT_1582 = 5;
          _DAT_15f5 = 0;
          DAT_2000 = DAT_00bc;
          DAT_4000 = 0x42;
          DAT_5000 = 0;
          return;
        }
        goto FUN_afba;
      }
    }
    else {
      puVar2 = (ushort *)&DAT_1700;
      while ((*puVar2 <= (ushort)DAT_f6ce << 8 &&
             ((ushort)DAT_f6cf * 0x100 < *puVar2 || (ushort)DAT_f6cf * 0x100 - *puVar2 == 0))) {
        puVar2 = puVar2 + 1;
        if ((ushort *)0x177f < puVar2) {
          FUN_afce();
          return;
        }
      }
    }
  }
  DAT_15e6 = 0xff;
  DAT_14a0 = -1;
  DAT_15ec = 0;
  DAT_15ed = 0;
  _DAT_15e7 = 0;
  _DAT_15e9 = 0;
  DAT_15eb = 0;
  _DAT_15f7 = 0;
  _DAT_15f9 = 0;
  _DAT_15fb = 0;
  _DAT_15ee = 0;
  _DAT_15f0 = 0;
  if (_DAT_15c1 != 0x55a5) {
    _DAT_15c1 = 0x55a5;
    DAT_15c4 = DAT_ff1d;
  }
FUN_afba:
  puVar4 = (undefined2 *)&DAT_1700;
  _DAT_15c5 = 0x6400;
  _DAT_00a9 = _DAT_15e7;
  _DAT_00ab = _DAT_15e9;
  DAT_00ad = DAT_15eb;
  _DAT_00c8 = _DAT_15f7;
  _DAT_00ca = _DAT_15f9;
  _DAT_00cc = _DAT_15fb;
  do {
    *puVar4 = 0x6400;
    puVar4 = puVar4 + 1;
  } while (puVar4 != (undefined2 *)0x1780);
  _DAT_15f5 = 0;
  return;
}


// ---- FUN_afba @ afba ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_afba(void)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)&DAT_1700;
  _DAT_15c5 = 0x6400;
  do {
    *puVar1 = 0x6400;
    puVar1 = puVar1 + 1;
  } while (puVar1 != (undefined2 *)0x1780);
  _DAT_15f5 = 0;
  return;
}


// ---- FUN_afce @ afce ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_afce(void)

{
  undefined2 *puVar1;
  
  _DAT_00a9 = _DAT_15e7;
  _DAT_00ab = _DAT_15e9;
  DAT_00ad = DAT_15eb;
  _DAT_00c8 = _DAT_15f7;
  _DAT_00ca = _DAT_15f9;
  _DAT_00cc = _DAT_15fb;
  if ((_DAT_15fb & 0x20) != 0) {
    DAT_009b = DAT_009b | 0x10;
  }
  DAT_14a0 = DAT_15e6 + DAT_f7b7;
  if (CARRY1(DAT_15e6,DAT_f7b7)) {
    DAT_14a0 = -1;
  }
  if (DAT_fef6 == 0) {
    puVar1 = (undefined2 *)&DAT_1700;
    _DAT_15c5 = 0x6400;
    do {
      *puVar1 = 0x6400;
      puVar1 = puVar1 + 1;
    } while (puVar1 != (undefined2 *)0x1780);
  }
  _DAT_15f5 = 0;
  return;
}


// ---- FUN_b00d @ b00d ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b00d(void)

{
  bool bVar1;
  char *pcVar2;
  char *pcVar3;
  
  pcVar2 = &DAT_f400;
  if ((DAT_0040 & 8) != 0) {
    pcVar2 = s__________________________________c5e4 + 0x2d1c;
  }
  DAT_1021 = *pcVar2;
  pcVar2 = pcVar2 + 1;
  do {
    DAT_1022 = *pcVar2;
    DAT_1023 = pcVar2[1];
    DAT_1024 = pcVar2[2];
    DAT_1025 = pcVar2[3];
    DAT_1026 = pcVar2[4];
    DAT_1027 = pcVar2[5];
    DAT_1028 = pcVar2[6];
    DAT_1029 = pcVar2[7];
    pcVar2 = pcVar2 + 8;
    if ((DAT_0040 & 8) == 0) {
      bVar1 = pcVar2 == (char *)0xf481;
    }
    else {
      bVar1 = pcVar2 == (char *)0xf381;
    }
  } while (!bVar1);
  _DAT_1570 = (undefined2 *)&DAT_1040;
  do {
    pcVar3 = pcVar2;
    pcVar2 = pcVar3 + 2;
    *_DAT_1570 = *(undefined2 *)pcVar3;
    _DAT_1570 = _DAT_1570 + 1;
    if ((DAT_0040 & 8) == 0) {
      bVar1 = pcVar2 == (char *)0xf4b1;
    }
    else {
      bVar1 = pcVar2 == (char *)0xf3b1;
    }
  } while (!bVar1);
  DAT_1036 = *pcVar2;
  _DAT_1012 = *(undefined2 *)(pcVar3 + 3);
  _DAT_1010 = *(undefined2 *)(pcVar3 + 5);
  DAT_102a = pcVar3[7];
  DAT_102b = pcVar3[8];
  DAT_102c = pcVar3[9];
  DAT_1000 = pcVar3[10];
  DAT_1001 = pcVar3[0xb];
  DAT_1002 = pcVar3[0xc];
  if ((DAT_0040 & 4) != 0) {
    DAT_1002 = pcVar3[0xe];
  }
  DAT_1003 = pcVar3[0xd];
  DAT_1033 = 0;
  DAT_1034 = 0;
  DAT_1035 = 0;
  DAT_1020 = 2;
  DAT_1005 = 0;
  return;
}


// ---- FUN_b0d6 @ b0d6 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b0d6(void)

{
  DAT_00bc = DAT_00bc & 0x7f;
  DAT_0040 = DAT_0040 | 8;
  DAT_0049 = DAT_0049 | 0x80;
  P2DATA = DAT_0048;
  DAT_0017 = DAT_0049;
  P2DDR = 0x70;
  DAT_0016 = 0xf1;
  TCSR = 0x16;
  P3SCR = 0;
  RAMCR = 0xe7;
  _DAT_001b = &DAT_1407;
  RMCR = 0xc;
  TRCS = 0;
  DAT_001e = 4;
  return;
}


// ---- FUN_b0e2 @ b0e2 ----

void FUN_b0e2(void)

{
  do {
    DAT_1476 = 0;
    FUN_b148();
    FUN_b264();
    FUN_b2cb();
    FUN_b239();
    FUN_b36a();
    FUN_b9b5();
    if ((DAT_0040 & 8) == 0) {
      FUN_b307();
      FUN_b39c();
      FUN_b443();
      FUN_b4e4();
      FUN_b808();
      FUN_bb23();
      FUN_bb7c();
      FUN_c1ab();
    }
    else {
      FUN_c5b6();
    }
    P2DATA = DAT_0048;
    DAT_0017 = DAT_0049;
    DAT_2000 = DAT_00bc;
    DAT_00b4 = DAT_00b4 | 0x40;
    DAT_1002 = DAT_009c;
    DAT_4000 = DAT_00b4;
  } while( true );
}


// ---- FUN_b138 @ b138 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_b138(undefined1 param_1,undefined1 param_2)

{
  byte bVar1;
  
  bVar1 = DAT_00b1;
  FUN_809f(DAT_00b1,param_2,0xfe20);
  _DAT_004d = (ushort)bVar1 * 0x7d;
  return;
}


// ---- FUN_b148 @ b148 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b148(void)

{
  undefined1 uVar1;
  undefined1 extraout_B;
  undefined1 extraout_B_00;
  undefined1 extraout_B_01;
  undefined1 extraout_B_02;
  undefined1 extraout_B_03;
  undefined1 extraout_B_04;
  undefined1 extraout_B_05;
  undefined1 extraout_B_06;
  undefined1 extraout_B_07;
  char extraout_B_08;
  undefined1 extraout_B_09;
  
  FUN_b209();
  uVar1 = extraout_B;
  if (DAT_1453 != '\0') {
    _DAT_0089 = CONCAT11(DAT_008f,extraout_B);
    _DAT_008b = CONCAT11(DAT_140d,0x4b);
    DAT_140d = FUN_b1e1();
    uVar1 = extraout_B_00;
  }
  DAT_008f = uVar1;
  FUN_b209();
  uVar1 = extraout_B_01;
  if (DAT_1453 != '\0') {
    _DAT_0089 = CONCAT11(DAT_004c,extraout_B_01);
    _DAT_008b = CONCAT11(DAT_140e,0x10);
    DAT_140e = FUN_b1e1();
    uVar1 = extraout_B_02;
  }
  DAT_004c = uVar1;
  FUN_b209();
  _DAT_0089 = CONCAT11(DAT_1401,extraout_B_03);
  _DAT_008b = CONCAT11(DAT_14ca,0x10);
  DAT_14ca = FUN_b1e1();
  DAT_1401 = extraout_B_04;
  FUN_b209();
  _DAT_0089 = CONCAT11(DAT_1574,extraout_B_05);
  _DAT_008b = CONCAT11(DAT_1573,0x10);
  DAT_1573 = FUN_b1e1();
  DAT_1574 = extraout_B_06;
  FUN_b209();
  _DAT_0089 = CONCAT11(DAT_1402,extraout_B_07);
  _DAT_008b = CONCAT11(DAT_1527,0x10);
  DAT_1527 = FUN_b1e1();
  if (DAT_1526 == '\0') {
    DAT_1526 = extraout_B_08;
  }
  DAT_1402 = extraout_B_08;
  FUN_b209();
  DAT_1583 = extraout_B_09;
  return;
}


// ---- FUN_b1e1 @ b1e1 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

byte FUN_b1e1(void)

{
  byte bVar1;
  byte bVar2;
  
  bVar1 = (byte)((ushort)_DAT_0089 >> 8);
  if (bVar1 != 0) {
    bVar2 = bVar1 - (byte)_DAT_0089;
    if (bVar1 < (byte)_DAT_0089) {
      bVar2 = -bVar2;
    }
    if (bVar2 <= DAT_008c) {
      if ((-1 < (short)((ushort)DAT_008b << 8)) && ((byte)(DAT_008b + 1) < 0x14)) {
        return DAT_008b + 1;
      }
      return 0x80;
    }
    if ((short)((ushort)DAT_008b << 8) < 0) {
      return DAT_008b + 1;
    }
  }
  return 0;
}


// ---- FUN_b209 @ b209 ----

byte FUN_b209(undefined1 param_1,byte param_2)

{
  byte bVar1;
  
  DAT_1006 = param_2 + 0x20;
  do {
  } while (-1 < (char)(param_2 + 0x20));
  if ((param_2 != 0) && (param_2 != 6)) {
    return param_2;
  }
  bVar1 = *(byte *)((byte)((param_2 & 3) << 1) + 0x1007);
  return (bVar1 >> 7) << 1 | (byte)(bVar1 << 1) >> 7;
}


// ---- FUN_b239 @ b239 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b239(void)

{
  char cVar1;
  byte bVar2;
  
  if (DAT_008f < 0xb0) {
    cVar1 = (char)((ushort)(byte)(0xaf - DAT_008f) * (ushort)DAT_ff87 >> 8);
  }
  else {
    cVar1 = -(char)((ushort)(byte)-(0xaf - DAT_008f) * (ushort)DAT_ff87 >> 8);
  }
  DAT_142c = cVar1 + DAT_ff88;
  bVar2 = (byte)((ushort)DAT_142c << 2);
  _DAT_1579 = CONCAT11((char)(((ushort)DAT_142c << 2) >> 8) + CARRY1(bVar2,DAT_142c),
                       bVar2 + DAT_142c);
  _DAT_157b = (ushort)DAT_142c * 10;
  return;
}


// ---- FUN_b264 @ b264 ----

void FUN_b264(undefined1 param_1,undefined1 param_2)

{
  byte bVar1;
  undefined1 uVar2;
  
  bVar1 = DAT_00bd;
  if ((2 < DAT_004c) && (DAT_004c < 0xf2)) {
    if (DAT_004c == DAT_1489) {
      if (((DAT_0015 & 0x80) == 0) || (0x6f < DAT_008f)) {
        if (DAT_1453 == '\0') {
          DAT_1453 = DAT_140c;
        }
        if (DAT_0082 == '\0') {
          DAT_0082 = DAT_00b1;
        }
      }
      return;
    }
    DAT_1489 = DAT_004c;
    bVar1 = DAT_004c;
  }
  uVar2 = FUN_80a9(bVar1,param_2,0xfb30);
  DAT_140c = FUN_b28b(DAT_140c,uVar2);
  FUN_b295();
  return;
}


// ---- FUN_b28b @ b28b ----

byte FUN_b28b(byte param_1,byte param_2)

{
  byte bVar1;
  
  bVar1 = param_2;
  if ((param_1 < param_2) || (bVar1 = param_2 + 2, (byte)(param_2 + 2) <= param_1)) {
    param_1 = bVar1;
  }
  return param_1;
}


// ---- FUN_b295 @ b295 ----

void FUN_b295(void)

{
  byte bVar1;
  undefined2 in_D;
  byte bVar2;
  
  bVar2 = (byte)((ushort)in_D >> 8);
  bVar1 = bVar2 - 10;
  if (bVar2 < 10) {
    bVar1 = 0;
  }
  else if (0x9f < bVar1) {
    bVar1 = 0x9f;
  }
  DAT_00b1 = (char)((ushort)bVar1 * 0x19a + 0x80 >> 8);
  if (((DAT_0015 & 0x80) == 0) || (0x6f < DAT_008f)) {
    if (DAT_1453 == '\0') {
      DAT_1453 = DAT_140c;
    }
    if (DAT_0082 == '\0') {
      DAT_0082 = DAT_00b1;
    }
  }
  return;
}


// ---- FUN_b307 @ b307 ----

void FUN_b307(void)

{
  byte bVar1;
  
  if ((DAT_0054 & 8) != 0) {
    if (DAT_1413 < DAT_ffbc) {
      DAT_0099 = 0;
    }
    else {
      DAT_0099 = DAT_0099 | 0x80;
      if (DAT_ffbd <= DAT_0099) goto LAB_b363;
    }
    if ((((DAT_0053 & 3) == 0) && ((DAT_007e & 1) == 0)) && (DAT_140c < DAT_f9fa)) {
      if (DAT_1453 < 0x41) {
        if (DAT_140c < DAT_f9f9) goto LAB_b363;
      }
      else if (DAT_140c < 0x69) goto LAB_b363;
      bVar1 = DAT_ff23;
      if ((DAT_0059 & 1) == 0) {
        bVar1 = DAT_ff22;
      }
      if (DAT_1460 < bVar1) {
        DAT_0059 = DAT_0059 | 1;
        DAT_009c = DAT_009c & 0xbf;
        return;
      }
    }
  }
LAB_b363:
  DAT_0059 = DAT_0059 & 0xfe;
  DAT_009c = DAT_009c | 0x40;
  return;
}


// ---- FUN_b36a @ b36a ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b36a(void)

{
  byte extraout_B;
  
  if ((DAT_fee1 & 1) != 0) {
    _DAT_006b = (ushort)DAT_1574 * 0xaf;
    DAT_006e = DAT_008f;
    DAT_006d = 0;
    DAT_006f = 0;
    FUN_8297();
    if (extraout_B < 0x6f) {
      DAT_1576 = extraout_B + 10;
      return;
    }
    if (0x82 < extraout_B) {
      DAT_1576 = extraout_B - 10;
      return;
    }
  }
  DAT_1576 = 0x79;
  return;
}


// ---- FUN_b39c @ b39c ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b39c(void)

{
  byte bVar1;
  char cVar2;
  undefined2 *puVar3;
  byte *pbVar4;
  
  if ((DAT_0040 & 0x20) != 0) {
    if ((DAT_0015 & 0x80) == 0) {
      DAT_0040 = DAT_0040 & 0xcf;
    }
    else if (DAT_140a == '\0') {
      if ((DAT_0017 & 2) == 0) {
        if ((DAT_0040 & 0x80) == 0) {
          FUN_b3f6();
          FUN_b3f6();
          FUN_b3f6();
          FUN_b3f6();
          DAT_15e8 = DAT_00aa;
          pbVar4 = (byte *)0x140;
          bVar1 = 0xaa;
          do {
            cVar2 = '\0';
            do {
              pbVar4[-1] = ~bVar1;
              pbVar4 = pbVar4 + -2;
              cVar2 = cVar2 + '\x02';
              *pbVar4 = bVar1;
              if (pbVar4 == &DAT_0040) break;
            } while (cVar2 != '\0');
            DAT_0017 = 0x80;
            cVar2 = '\0';
            do {
              if ((bVar1 != *pbVar4) || ((byte)~bVar1 != pbVar4[1])) {
                DAT_0040 = 0xb0;
                goto LAB_b438;
              }
              pbVar4 = pbVar4 + 2;
              cVar2 = cVar2 + '\x02';
            } while (cVar2 != '\0');
            if (bVar1 == 0x55) {
              if (pbVar4 != (byte *)0x140) {
                return;
              }
              DAT_0040 = 0xa0;
LAB_b438:
              DAT_0041 = DAT_15e8;
              puVar3 = (undefined2 *)&DAT_0048;
              do {
                *puVar3 = 0;
                puVar3 = puVar3 + 1;
              } while (puVar3 != (undefined2 *)0x140);
              puVar3 = (undefined2 *)&DAT_1400;
              do {
                *puVar3 = 0;
                puVar3 = puVar3 + 1;
              } while (puVar3 != (undefined2 *)&DAT_15c0);
              if ((DAT_0040 & 1) != 0) {
                _DAT_013e = 0xae54;
                FUN_b0d6();
                _DAT_013e = 0xae57;
                FUN_ae98();
                _DAT_013e = 0xae5a;
                FUN_b00d();
                FUN_b0e2();
                return;
              }
              _DAT_013e = 0xae3e;
              FUN_ae5e();
              _DAT_013e = 0xae41;
              FUN_ae98();
              _DAT_013e = 0xae44;
              FUN_b00d();
              _DAT_013e = 0xae48;
              FUN_b148();
              _DAT_013e = 0xae4b;
              FUN_b264();
              _DAT_013e = 0xae4e;
              FUN_b138();
              FUN_b0e2();
              return;
            }
            bVar1 = ~bVar1;
          } while( true );
        }
      }
      else if (DAT_004c < 0x21) {
        if ((DAT_0053 & 0x10) == 0) {
          if (DAT_1401 < 0x20) goto LAB_b3d0;
        }
        else if (0xef < DAT_1401) {
LAB_b3d0:
          DAT_0040 = DAT_0040 & 0xef;
          return;
        }
        DAT_0040 = DAT_0040 | 0x10;
        return;
      }
    }
  }
  return;
}


// ---- FUN_b3f6 @ b3f6 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b3f6(undefined1 param_1,undefined1 param_2,byte *param_3)

{
  byte bVar1;
  char cVar2;
  undefined2 *puVar3;
  
  bVar1 = 0xaa;
  do {
    cVar2 = '\0';
    do {
      param_3[-1] = ~bVar1;
      param_3 = param_3 + -2;
      cVar2 = cVar2 + '\x02';
      *param_3 = bVar1;
      if (param_3 == &DAT_0040) break;
    } while (cVar2 != '\0');
    DAT_0017 = 0x80;
    cVar2 = '\0';
    do {
      if ((bVar1 != *param_3) || ((byte)~bVar1 != param_3[1])) {
        DAT_0040 = 0xb0;
        goto LAB_b438;
      }
      param_3 = param_3 + 2;
      cVar2 = cVar2 + '\x02';
    } while (cVar2 != '\0');
    if (bVar1 == 0x55) {
      if (param_3 != (byte *)0x140) {
        return;
      }
      DAT_0040 = 0xa0;
LAB_b438:
      DAT_0041 = DAT_15e8;
      puVar3 = (undefined2 *)&DAT_0048;
      do {
        *puVar3 = 0;
        puVar3 = puVar3 + 1;
      } while (puVar3 != (undefined2 *)0x140);
      puVar3 = (undefined2 *)&DAT_1400;
      do {
        *puVar3 = 0;
        puVar3 = puVar3 + 1;
      } while (puVar3 != (undefined2 *)&DAT_15c0);
      if ((DAT_0040 & 1) == 0) {
        _DAT_013e = 0xae3e;
        FUN_ae5e();
        _DAT_013e = 0xae41;
        FUN_ae98();
        _DAT_013e = 0xae44;
        FUN_b00d();
        _DAT_013e = 0xae48;
        FUN_b148();
        _DAT_013e = 0xae4b;
        FUN_b264();
        _DAT_013e = 0xae4e;
        FUN_b138();
        FUN_b0e2();
        return;
      }
      _DAT_013e = 0xae54;
      FUN_b0d6();
      _DAT_013e = 0xae57;
      FUN_ae98();
      _DAT_013e = 0xae5a;
      FUN_b00d();
      FUN_b0e2();
      return;
    }
    bVar1 = ~bVar1;
  } while( true );
}


// ---- FUN_b443 @ b443 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b443(void)

{
  bool bVar1;
  byte bVar2;
  byte extraout_B;
  
  bVar2 = FUN_809f();
  if (((DAT_00c7 & 1) != 0) && (bVar1 = bVar2 < 10, bVar2 = bVar2 - 10, bVar1)) {
    bVar2 = 0;
  }
  if (DAT_14a2 < bVar2) {
    DAT_00c7 = DAT_00c7 & 0xfe;
    if ((DAT_ffb7 <= DAT_1460) || (DAT_ff21 <= DAT_1413)) goto LAB_b490;
    if ((DAT_0053 & 0x80) == 0) {
      if (DAT_1439 != '\0') goto LAB_b495;
      goto LAB_b490;
    }
    if ((DAT_fefc <= DAT_1413) || (DAT_ff81 <= DAT_1460)) goto LAB_b490;
LAB_b495:
    DAT_0059 = DAT_0059 | 0x80;
  }
  else {
    DAT_00c7 = DAT_00c7 | 1;
LAB_b490:
    DAT_0059 = DAT_0059 & 0x7f;
  }
  DAT_007d = DAT_007d & 0x4f;
  DAT_007d = DAT_007d | 0x40;
  _DAT_0074 = 0xfd00;
  _DAT_0076 = 0xfb00;
  _DAT_0078 = 0xfaf0;
  DAT_141a = FUN_80cf();
  _DAT_1422 = (ushort)(byte)(DAT_141a + 0x40) << 0xb;
  if ((DAT_0059 & 8) == 0) {
    if (1 < extraout_B) goto LAB_b4d1;
  }
  else if (extraout_B != 0) {
LAB_b4d1:
    if ((DAT_0059 & 0x80) == 0) {
      DAT_0059 = DAT_0059 | 8;
      DAT_141d = extraout_B;
      goto LAB_b4d9;
    }
  }
  DAT_0059 = DAT_0059 & 0xf7;
  DAT_141d = 0;
LAB_b4d9:
  _DAT_1426 = (ushort)DAT_141d << 0xb;
  return;
}


// ---- FUN_b4e4 @ b4e4 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_b4e4(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  char cVar5;
  short sVar6;
  ushort uVar7;
  char *pcVar8;
  char *pcVar9;
  byte bStack0000;
  byte bVar4;
  
  bVar2 = DAT_008f;
  FUN_809f();
  uVar7 = _DAT_0067;
  bStack0000 = bVar2;
  FUN_80a9();
  bVar1 = DAT_1442;
  bVar2 = DAT_00b1;
  sVar6 = (uVar7 & 0x3f) * 4 * (ushort)bStack0000;
  if (((SUB21((ushort)sVar6 >> 0xf,0)) ||
      (bVar4 = (byte)((ushort)(sVar6 * 2) >> 8), bVar3 = bVar4 + DAT_ff8e, CARRY1(bVar4,DAT_ff8e)))
     || ((bVar4 = DAT_ff8e + 5, (byte)(DAT_ff8e + 5) <= bVar3 && (bVar4 = bVar3, 0x60 < bVar3)))) {
    DAT_143a = '\x18';
  }
  else {
    DAT_143a = 'x' - bVar4;
  }
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_0053 & 1) == 0) {
      if ((((DAT_140c < DAT_ffd5) && (0x40 < DAT_1453)) && (DAT_1453 < 0x55)) &&
         (DAT_ffd4 <= DAT_140c)) {
        sVar6 = CONCAT11(DAT_1460,DAT_1482);
        if ((DAT_007d & 4) != 0) {
          sVar6 = sVar6 + 0xa08;
        }
        if (((byte)sVar6 < DAT_ffd6) && ((byte)((ushort)sVar6 >> 8) < DAT_ffd7)) {
          DAT_007d = DAT_007d & 0xfb;
          FUN_809f(DAT_1442,(byte)sVar6,0xff60);
          DAT_0059 = DAT_0059 & 0xbf;
          DAT_143b = bVar1;
          goto LAB_b535;
        }
      }
LAB_b6ed:
      pcVar8 = (char *)0xffe0;
      if ((DAT_007f & 0x80) != 0) {
        pcVar8 = (char *)0xf9e3;
      }
      pcVar9 = pcVar8;
      if ((DAT_ffdc <= DAT_1460) && (pcVar9 = pcVar8 + 3, DAT_ffdd <= DAT_1460)) {
        pcVar9 = pcVar8 + 6;
      }
      pcVar8 = pcVar9;
      if ((DAT_ffda <= DAT_1482) && (pcVar8 = pcVar9 + 1, DAT_ffdb <= DAT_1482)) {
        pcVar8 = pcVar9 + 2;
      }
      cVar5 = *pcVar8;
      DAT_007d = DAT_007d & 0x1f;
      DAT_007d = DAT_007d | 0x14;
      DAT_0059 = DAT_0059 & 0xbf;
      _DAT_0074 = 0xfc00;
      _DAT_0076 = 0xfb20;
      _DAT_0078 = 0xfb10;
      DAT_145f = cVar5;
      FUN_80cf();
      bStack0000 = cVar5 + 0x80;
      if ((DAT_007d & 8) == 0) {
        if ((DAT_007d & 1) != 0) {
          if ((DAT_feff <= DAT_1460) && (DAT_ff74 <= DAT_1482)) goto LAB_b757;
          DAT_145e = '\0';
          DAT_145f = '\0';
        }
      }
      else {
LAB_b757:
        DAT_007d = DAT_007d | 1;
        cVar5 = DAT_1460 << 1;
        if ((char)DAT_1460 < '\0') {
          cVar5 = -1;
        }
        FUN_809f();
        DAT_145e = cVar5;
      }
      bVar2 = DAT_158c;
      if ((DAT_ff10 == 0xff) || (bVar1 = bStack0000, DAT_1477 <= DAT_ff10)) {
        FUN_809f();
        bVar1 = DAT_00b1;
        FUN_809f();
        cVar5 = bVar1 - bVar2;
        if (bVar1 < bVar2) {
          cVar5 = '\0';
        }
        if (((-1 < (char)bStack0000) ||
            (bVar1 = cVar5 + bStack0000, -1 < (char)(cVar5 + bStack0000))) &&
           (bVar1 = cVar5 + bStack0000, 0x3b < (byte)(cVar5 + bStack0000))) {
          bVar1 = 0x3c;
        }
      }
      bStack0000 = bVar1;
      bVar2 = DAT_00b1;
      FUN_809f();
      bStack0000 = bStack0000 - bVar2;
      if (DAT_141d == 0) {
LAB_b7f6:
        DAT_141c = 0;
      }
      else {
        if (DAT_141d < DAT_ff12) {
          DAT_0059 = DAT_0059 & 0xef;
          goto LAB_b7f6;
        }
        DAT_0059 = DAT_0059 | 0x10;
        if ((DAT_fee0 & 0x40) != 0) {
          bStack0000 = bStack0000 - DAT_ff13;
          goto LAB_b7f6;
        }
        DAT_141c = DAT_ff11;
        if (DAT_ff8a <= (byte)(DAT_ff11 + DAT_141d)) {
          DAT_141c = DAT_ff8a;
        }
      }
      DAT_143b = bStack0000;
      goto LAB_b7fd;
    }
    uVar7 = CONCAT11(DAT_140c,DAT_1482);
    if ((DAT_0059 & 0x20) != 0) {
      uVar7 = uVar7 + 0x508;
    }
    if ((DAT_ff70 <= (byte)uVar7) && (DAT_ff71 <= (byte)(uVar7 >> 8))) {
      if ((DAT_0059 & 0x20) != 0) {
        uVar7 = uVar7 & 0xff;
      }
      if (DAT_1442 <= (byte)uVar7) {
        DAT_0059 = DAT_0059 | 0x20;
        goto LAB_b6ed;
      }
    }
    DAT_0059 = DAT_0059 & 0xdf;
    if ((DAT_0053 & 4) == 0) {
      FUN_809f();
      if ((DAT_0059 & 0x40) == 0) {
LAB_b5c0:
        DAT_0059 = DAT_0059 & 0xfb;
      }
      else if ((DAT_0059 & 4) != 0) {
        if (bVar1 < DAT_142f) {
          if (DAT_14ce <= DAT_142f) {
            DAT_142f = DAT_142f - DAT_14ce;
          }
        }
        else {
          if (bVar1 == DAT_142f) goto LAB_b5c0;
          DAT_142f = DAT_142f + DAT_14ce;
        }
      }
      DAT_1430 = 0;
    }
    else {
      FUN_809f();
      if ((DAT_0059 & 0x40) == 0) {
LAB_b603:
        DAT_0059 = DAT_0059 | 4;
      }
      else if ((DAT_0059 & 4) == 0) {
        if (bVar1 < DAT_1430) {
          if (DAT_14ce <= DAT_1430) {
            DAT_1430 = DAT_1430 - DAT_14ce;
          }
        }
        else {
          if (bVar1 == DAT_1430) goto LAB_b603;
          DAT_1430 = DAT_1430 + DAT_14ce;
        }
      }
      DAT_142f = 0;
    }
    bStack0000 = 0;
    DAT_14ce = 0;
    DAT_0059 = DAT_0059 | 0x40;
    if (((DAT_00b9 & 0x20) == 0) && ((DAT_00bf & 0x20) != 0)) {
      sVar6 = DAT_143f - _DAT_140a;
      if (sVar6 != 0) {
        if (DAT_143f < _DAT_140a) {
          sVar6 = CONCAT11(-((char)((ushort)sVar6 >> 8) + ((char)-(char)sVar6 != '\0')),-(char)sVar6
                          ) << 4;
          cVar5 = (char)((ushort)sVar6 >> 8);
          if (cVar5 != '\0') {
            sVar6 = CONCAT11(cVar5,0xff);
          }
          FUN_809f();
          DAT_151a = (char)sVar6;
          FUN_809f();
        }
        else {
          sVar6 = sVar6 * 0x10;
          cVar5 = (char)((ushort)sVar6 >> 8);
          if (cVar5 != '\0') {
            sVar6 = CONCAT11(cVar5,0xff);
          }
          FUN_809f();
          DAT_1519 = (char)sVar6;
          FUN_809f();
        }
      }
    }
    DAT_143b = DAT_ffd9;
    if ((DAT_ffd4 < DAT_140c) &&
       (bVar2 = (DAT_ffd4 + 0x1e) - DAT_140c, DAT_143b = 0, DAT_140c <= (byte)(DAT_ffd4 + 0x1e))) {
      DAT_143b = (byte)((ushort)DAT_ffd9 * ((CONCAT11(8,bVar2) >> 8) * (ushort)bVar2 & 0xff) >> 8);
    }
  }
  else {
    FUN_809f();
    DAT_143b = bVar2;
    if (DAT_1442 < 8) {
      DAT_143b = bVar2 * DAT_1442 * '\b';
    }
  }
LAB_b535:
  DAT_145e = '\0';
  DAT_145f = '\0';
  DAT_141c = 0;
LAB_b7fd:
  _DAT_1428 = (ushort)DAT_141c << 0xb;
  return;
}


// ---- FUN_b808 @ b808 ----

/* WARNING: Removing unreachable block (RAM,0xb91e) */
/* WARNING: Removing unreachable block (RAM,0xb92c) */
/* WARNING: Removing unreachable block (RAM,0xb934) */
/* WARNING: Removing unreachable block (RAM,0xb936) */
/* WARNING: Removing unreachable block (RAM,0xb927) */
/* WARNING: Removing unreachable block (RAM,0xb939) */
/* WARNING: Removing unreachable block (RAM,0xb93e) */
/* WARNING: Removing unreachable block (RAM,0xb946) */
/* WARNING: Removing unreachable block (RAM,0xb949) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b808(void)

{
  byte bVar1;
  
  if ((DAT_fee1 & 2) == 0) {
    if (((DAT_0054 & 8) == 0) && (((DAT_0040 & 4) != 0 || (0x31 < DAT_1454)))) {
      DAT_0049 = DAT_0049 & 0xef;
      return;
    }
    DAT_0049 = DAT_0049 | 0x10;
    return;
  }
  DAT_00a5 = DAT_008f - DAT_1583;
  if (DAT_008f < DAT_1583) {
    DAT_00a5 = 0;
  }
  if ((DAT_0054 & 8) == 0) {
    if (((DAT_0040 & 4) == 0) && (DAT_1454 < 0x32)) goto LAB_b891;
    bVar1 = 0;
  }
  else {
    if (DAT_140c < DAT_ffcc) {
      if (((DAT_0059 & 2) != 0) && (DAT_140c <= DAT_ffcb)) {
        DAT_0059 = DAT_0059 & 0xfd;
      }
    }
    else {
      DAT_0059 = DAT_0059 | 2;
    }
    if ((DAT_0053 & 2) == 0) {
      if ((DAT_1467 == '\0') && (0x3b < DAT_140c)) {
        if ((DAT_0059 & 2) == 0) {
          if ((byte)((ushort)_DAT_1411 >> 8) < 3) {
            bVar1 = (byte)(_DAT_1411 << 2);
          }
          else {
            bVar1 = 0xff;
          }
          _DAT_005b = (ushort)DAT_1460 * (ushort)bVar1;
          FUN_8001();
        }
        else if ((DAT_0053 & 1) == 0) goto LAB_b891;
        DAT_1584 = '\0';
        if (DAT_00a5 == 0) {
          DAT_1586 = 0;
          DAT_1587 = '\0';
        }
        else {
          if (DAT_00a5 < 6) {
            DAT_1586 = 0;
          }
          else {
            bVar1 = (byte)((ushort)DAT_00a5 * (ushort)DAT_f675 >> 8);
            if (99 < bVar1) {
              bVar1 = 100;
            }
            DAT_1586 = -bVar1;
          }
          if (DAT_1587 == '\0') {
            if (DAT_1585 != 0) {
              DAT_1585 = DAT_1585 - 1;
            }
            DAT_1587 = DAT_f676;
          }
        }
        if ((short)((ushort)DAT_1586 << 8) < 0) {
          bVar1 = DAT_1585 + DAT_1586;
          if (DAT_1585 < (byte)-DAT_1586) {
            bVar1 = 0;
          }
        }
        else {
          bVar1 = DAT_1586 + DAT_1585;
          if ((CARRY1(DAT_1586,DAT_1585)) || (99 < bVar1)) {
            bVar1 = 100;
          }
        }
        goto LAB_b96b;
      }
    }
    else if (DAT_140c < 100) {
      DAT_1467 = '\0';
    }
    else {
      DAT_1467 = '\x1e';
    }
LAB_b891:
    DAT_1584 = DAT_008f - DAT_f678;
    bVar1 = 100;
  }
LAB_b96b:
  DAT_1585 = bVar1;
  if (bVar1 == 0) {
    DAT_5000 = -0x80;
  }
  else {
    DAT_5000 = bVar1 - 1;
    if (DAT_5000 == 'c') {
      DAT_5000 = 'd';
    }
  }
  if ((DAT_0054 & 8) == 0) {
    if (((DAT_0040 & 4) != 0) || (0x31 < DAT_1454)) goto LAB_b9b1;
  }
  else if ((DAT_00b7 & 0x40) == 0) {
    if (DAT_f9fc <= DAT_1453) {
      if ((DAT_0053 & 2) != 0) goto LAB_b9a4;
      if (DAT_1477 < DAT_f9fd) {
        return;
      }
    }
LAB_b9b1:
    DAT_0049 = DAT_0049 & 0xef;
    return;
  }
LAB_b9a4:
  DAT_0049 = DAT_0049 | 0x10;
  return;
}


// ---- FUN_b9b5 @ b9b5 ----

void FUN_b9b5(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  byte *pbVar4;
  byte *pbVar5;
  
  bVar1 = DAT_00c0;
  if ((DAT_0040 & 8) == 0) {
    if ((DAT_0054 & 8) != 0) goto LAB_b9cf;
  }
  else if ((DAT_0040 & 2) == 0) {
LAB_b9cf:
    if ((DAT_0053 & 2) == 0) {
      if ((DAT_00b6 & 0x20) != 0) {
        DAT_00c0 = DAT_00c0 | 0x80;
        goto LAB_bb17;
      }
      DAT_00c0 = DAT_00c0 & 0xc0;
      bVar3 = DAT_00c0;
      bVar2 = DAT_1407;
      if ((bVar1 & 1) != 0) {
        bVar2 = DAT_1407 + 4;
      }
      if (DAT_f697 <= bVar2) {
        DAT_00c0 = DAT_00c0 | 1;
        bVar2 = DAT_1407;
        if ((bVar1 & 2) != 0) {
          bVar2 = DAT_1407 + 4;
        }
        if (DAT_f698 <= bVar2) {
          DAT_00c0 = bVar3 | 3;
        }
      }
      bVar3 = DAT_00c0;
      if (((DAT_2000 & 2) == 0) && ((DAT_0053 & 0x10) != 0)) {
        DAT_00ce = DAT_00ce | 1;
        bVar2 = DAT_140c;
        if ((bVar1 & 4) != 0) {
          bVar2 = DAT_140c + 2;
        }
        if (bVar2 < DAT_f699) goto LAB_bab6;
        DAT_00c0 = DAT_00c0 | 4;
        bVar2 = DAT_140c;
        if ((bVar1 & 8) != 0) {
          bVar2 = DAT_140c + 2;
        }
        if ((byte)(bVar2 - 5) < DAT_f699) goto LAB_bab6;
        DAT_00c0 = bVar3 | 0xc;
        bVar2 = DAT_140c;
        if ((bVar1 & 0x10) != 0) {
          bVar2 = DAT_140c + 2;
        }
        if ((byte)(bVar2 - 10) < DAT_f699) goto LAB_bab6;
        DAT_00c0 = bVar3 | 0x1c;
        bVar2 = DAT_140c;
        if ((bVar1 & 0x20) != 0) {
          bVar2 = DAT_140c + 2;
        }
        if ((byte)(bVar2 - 0xf) < DAT_f699) goto LAB_bab6;
LAB_baaf:
        DAT_00c0 = bVar3 | 0x3c;
        bVar3 = 3;
      }
      else {
        DAT_00ce = DAT_00ce & 0xfe;
        bVar2 = DAT_140c;
        if ((bVar1 & 4) != 0) {
          bVar2 = DAT_140c + 2;
        }
        if (DAT_f69a <= bVar2) {
          DAT_00c0 = DAT_00c0 | 4;
          bVar2 = DAT_140c;
          if ((bVar1 & 8) != 0) {
            bVar2 = DAT_140c + 2;
          }
          if (DAT_f69a <= (byte)(bVar2 - 5)) {
            DAT_00c0 = bVar3 | 0xc;
            bVar2 = DAT_140c;
            if ((bVar1 & 0x10) != 0) {
              bVar2 = DAT_140c + 2;
            }
            if (DAT_f69a <= (byte)(bVar2 - 10)) {
              DAT_00c0 = bVar3 | 0x1c;
              bVar2 = DAT_140c;
              if ((bVar1 & 0x20) != 0) {
                bVar2 = DAT_140c + 2;
              }
              if (DAT_f69a <= (byte)(bVar2 - 0xf)) goto LAB_baaf;
            }
          }
        }
LAB_bab6:
        pbVar4 = (byte *)0xf7ed;
        if ((DAT_00ce & 1) != 0) {
          pbVar4 = &DAT_f7f0;
        }
        pbVar5 = pbVar4;
        if (((DAT_00c0 & 1) != 0) && (pbVar5 = pbVar4 + 1, (DAT_00c0 & 2) != 0)) {
          pbVar5 = pbVar4 + 2;
        }
        bVar1 = *pbVar5;
        bVar3 = bVar1;
        if ((((DAT_00c0 & 4) != 0) && (bVar3 = bVar1 >> 2, (DAT_00c0 & 8) != 0)) &&
           (bVar3 = bVar1 >> 4, (DAT_00c0 & 0x10) != 0)) {
          bVar3 = bVar1 >> 6;
        }
      }
      if (((bool)(bVar3 & 1)) || ((bool)(bVar3 >> 1 & 1))) {
        DAT_00c0 = DAT_00c0 | 0x80;
      }
      else {
        DAT_00c0 = DAT_00c0 & 0x7f;
      }
      if ((char)DAT_00c0 < '\0') {
        if (DAT_158d < DAT_f693) {
          DAT_158e = 0;
          return;
        }
        if ((bVar3 & 2) == 0) {
          DAT_00bc = DAT_00bc & 0xef;
          DAT_00bc = DAT_00bc | 0x20;
          DAT_158e = 0;
          return;
        }
LAB_bb17:
        DAT_00bc = DAT_00bc | 0x30;
        DAT_158e = 0;
        return;
      }
      if (DAT_158e < DAT_f694) {
        DAT_158d = 0;
        return;
      }
      goto LAB_bb03;
    }
  }
  DAT_00c0 = DAT_00c0 & 0x7f;
LAB_bb03:
  DAT_00bc = DAT_00bc & 0xcf;
  DAT_158d = 0;
  return;
}


// ---- FUN_bb23 @ bb23 ----

void FUN_bb23(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  
  if ((((DAT_0054 & 8) != 0) && ((DAT_0053 & 2) == 0)) && ((DAT_0053 & 1) == 0)) {
    bVar2 = DAT_140c;
    if ((DAT_00bc & 0x40) != 0) {
      bVar2 = DAT_140c + 5;
    }
    if ((DAT_fa07 <= bVar2) && (7 < DAT_1460)) {
      bVar2 = DAT_1460;
      bVar3 = DAT_1413;
      if ((DAT_00bc & 0x40) != 0) {
        bVar2 = DAT_1460 - 4;
        if (DAT_1460 < 4) goto LAB_bb78;
        bVar3 = DAT_1413 + 8;
      }
      bVar1 = DAT_f9e1;
      if (DAT_f9e2 <= bVar2) {
        if ((DAT_00bc & 0x40) != 0) {
          bVar2 = bVar2 + 8;
        }
        bVar1 = DAT_fa08;
        if (bVar2 < DAT_fa09) goto LAB_bb78;
      }
      if (bVar1 <= bVar3) {
        DAT_00bc = DAT_00bc | 0x40;
        return;
      }
    }
  }
LAB_bb78:
  DAT_00bc = DAT_00bc & 0xbf;
  return;
}


// ---- FUN_bb7c @ bb7c ----

/* WARNING: Removing unreachable block (RAM,0xc0cb) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_bb7c(void)

{
  bool bVar1;
  byte bVar2;
  byte bVar3;
  short sVar4;
  ushort uVar5;
  byte bVar7;
  ushort uVar6;
  byte *pbVar8;
  undefined1 uStack0000;
  byte bStack_1;
  
  if ((DAT_0054 & 8) == 0) {
    if (DAT_1442 < 4) {
      if ((DAT_0053 & 2) == 0) {
        DAT_14ac = DAT_008f;
      }
      else if ((((DAT_0053 & 0x44) != 0) && (0x7c < DAT_14ac)) &&
              (DAT_008f <= (byte)(DAT_14ac - 0xc))) goto LAB_bbe1;
      goto LAB_bbf5;
    }
LAB_bbe1:
    DAT_0085 = DAT_0085 | 0x80;
    DAT_00b6 = DAT_00b6 | 0x80;
    if (0x89 < DAT_0085) {
LAB_bbed:
      DAT_00a9 = DAT_00a9 | 0x80;
      DAT_15c8 = 0;
    }
  }
  else {
    if (DAT_1442 == 0) {
      DAT_14c4 = DAT_14c4 | 0x80;
      if (0x93 < DAT_14c4) goto LAB_bbed;
    }
    else {
      DAT_14c4 = 0;
      if (0x2f < DAT_1442) {
        _DAT_005b = CONCAT21(_DAT_140a,DAT_005d);
        _bStack_1 = 0xbbcc;
        FUN_8001();
        sVar4 = _DAT_005c << 2;
        DAT_145c = (undefined1)sVar4;
        if ((char)((ushort)sVar4 >> 8) != '\0') {
          sVar4 = 0xff;
        }
        if (((byte)sVar4 < 0x50) || (0x80 < (byte)sVar4)) goto LAB_bbe1;
      }
    }
LAB_bbf5:
    DAT_0085 = 0;
    DAT_00b6 = DAT_00b6 & 0x7f;
  }
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_004c < 3) || (0xf1 < DAT_004c)) {
      DAT_00b6 = DAT_00b6 | 0x20;
      DAT_155d = 0;
      if (99 < DAT_155c) {
        DAT_00a9 = DAT_00a9 | 0x20;
        DAT_00c8 = DAT_00c8 | 0x20;
        DAT_15ca = 0;
      }
    }
    else {
      DAT_00b6 = DAT_00b6 & 0xdf;
      DAT_155c = 0;
      if (99 < DAT_155d) {
        DAT_00c8 = DAT_00c8 & 0xdf;
      }
    }
  }
  else {
    DAT_155c = 0;
    DAT_155d = 0;
  }
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_1494 < 3) || (0xf0 < DAT_1494)) {
      DAT_155b = 0;
      DAT_00b9 = DAT_00b9 | 0x20;
      if (((DAT_0053 & 4) == 0) && (1 < DAT_1407)) {
        if (99 < DAT_155a) {
          DAT_00cb = DAT_00cb | 0x20;
          DAT_00ac = DAT_00ac | 0x20;
          DAT_15d9 = 0;
        }
        goto LAB_bc86;
      }
    }
    else {
      DAT_00b9 = DAT_00b9 & 0xdf;
      if (99 < DAT_155b) {
        DAT_00cb = DAT_00cb & 0xdf;
      }
    }
    DAT_155a = 0;
  }
  else {
    DAT_155a = 0;
    DAT_155b = 0;
  }
LAB_bc86:
  if (((DAT_00c8 & 0x20) == 0) && ((DAT_0053 & 2) == 0)) {
    if ((DAT_140c < DAT_f68b) || (DAT_1402 < DAT_f68d)) {
      DAT_1557 = 0;
    }
    else if (99 < DAT_1557) {
      DAT_00ca = DAT_00ca | 8;
      DAT_00ab = DAT_00ab | 8;
      DAT_15d6 = 0;
    }
    if ((DAT_140c < DAT_f68c) && (DAT_1402 < DAT_f68e)) {
      if (99 < DAT_1558) {
        DAT_00ca = DAT_00ca | 8;
        DAT_00ab = DAT_00ab | 8;
        DAT_15d6 = 0;
      }
    }
    else {
      DAT_1558 = 0;
    }
  }
  else {
    DAT_1557 = 0;
    DAT_1558 = 0;
  }
  if ((DAT_1402 < DAT_f68e) || (DAT_f68d <= DAT_1402)) {
    DAT_1559 = 0;
  }
  else if (99 < DAT_1559) {
    DAT_00ca = DAT_00ca & 0xf7;
  }
  if (((((DAT_fee1 & 2) == 0) || ((DAT_0054 & 1) != 0)) || ((DAT_0049 & 0x10) != 0)) ||
     (DAT_1442 == 0)) {
LAB_bd3c:
    DAT_14c9 = 0;
  }
  else {
    bVar2 = DAT_1584 - DAT_00a5;
    if (DAT_1584 < DAT_00a5) {
      bVar2 = -bVar2;
    }
    if (bVar2 < DAT_f677) goto LAB_bd3c;
    bVar2 = DAT_14c9 & 0x7f;
    DAT_14c9 = DAT_14c9 | 0x80;
    if (DAT_f6c3 <= bVar2) {
      DAT_00aa = DAT_00aa | 0x40;
      DAT_00b7 = DAT_00b7 | 0x40;
      DAT_0047 = DAT_0047 | 4;
      DAT_15ce = 0;
      goto LAB_bd3c;
    }
  }
  if ((DAT_0054 & 8) == 0) {
    DAT_158b = 0;
    if (((DAT_1454 < 0x32) || ((DAT_0054 & 1) != 0)) || (1 < DAT_1407)) {
      DAT_158a = 0;
    }
    else if (_DAT_1408 < 400) {
      DAT_00b6 = DAT_00b6 & 0xbf;
      if (99 < DAT_158a) {
        DAT_00cd = DAT_00cd & 0xfe;
      }
    }
    else {
      DAT_158a = 0;
      DAT_0081 = DAT_0081 | 0x80;
      if (DAT_0081 < 0xe4) goto LAB_bdd8;
      DAT_0047 = DAT_0047 | 2;
      DAT_00cd = DAT_00cd | 1;
      DAT_00b6 = DAT_00b6 | 0x40;
    }
    DAT_0081 = 0;
  }
  else {
    DAT_158a = 0;
    if ((DAT_1442 < 0x30) || ((DAT_0053 & 2) != 0)) {
      DAT_158b = 0;
    }
    else if (_DAT_1408 < 100) {
      DAT_158b = 0;
      DAT_00c5 = DAT_00c5 | 0x80;
      if (DAT_00c5 < 0xe4) goto LAB_bdd8;
      DAT_00cd = DAT_00cd | 2;
      DAT_00b6 = DAT_00b6 | 0x40;
    }
    else {
      if ((DAT_00b6 & 0x40) != 0) {
        DAT_00b6 = DAT_00b6 & 0xbf;
        _bStack_1 = 0xbdb2;
        FUN_afba();
      }
      if (99 < DAT_158b) {
        DAT_00cd = DAT_00cd & 0xfd;
      }
    }
    DAT_00c5 = 0;
  }
LAB_bdd8:
  if (((DAT_00cd & 1) == 0) && ((DAT_00cd & 2) == 0)) {
    DAT_00c8 = DAT_00c8 & 0xbf;
  }
  else {
    DAT_00a9 = DAT_00a9 | 0x40;
    DAT_00c8 = DAT_00c8 | 0x40;
    DAT_15c9 = 0;
  }
  if ((0x2f < DAT_1442) && ((DAT_00a8 & 8) == 0)) {
    DAT_15ec = DAT_15ec + 1;
    DAT_00a8 = DAT_00a8 | 8;
  }
  if ((DAT_0053 & 1) != 0) {
    DAT_15ec = 0;
    DAT_00c9 = DAT_00c9 & 0xdf;
    DAT_00a8 = DAT_00a8 | 8;
  }
  if (1 < DAT_15ec) {
    DAT_00aa = DAT_00aa | 0x20;
    DAT_00c9 = DAT_00c9 | 0x20;
    DAT_15cf = 0;
  }
  if (DAT_1407 < 2) {
    if (((((DAT_0053 & 4) != 0) || ((DAT_00c8 & 0x60) != 0)) || (DAT_1460 < DAT_f79e)) ||
       (((DAT_f7ad <= DAT_1460 || (DAT_1413 < DAT_f79d)) ||
        ((DAT_f7ae <= DAT_1413 || (DAT_140c < DAT_f7af)))))) goto LAB_be73;
    if (DAT_1523 == 0) {
      DAT_1523 = 1;
    }
    if (0x32 < DAT_1523) {
      DAT_00a9 = DAT_00a9 | 0x10;
      DAT_00c8 = DAT_00c8 | 0x10;
      DAT_15cb = 0;
      DAT_1523 = 0;
    }
  }
  else {
    DAT_00c8 = DAT_00c8 & 0xef;
LAB_be73:
    DAT_1523 = 0;
  }
  if ((((DAT_0053 & 0x10) == 0) && (DAT_f78e <= DAT_1460)) &&
     (((DAT_1460 < DAT_f78f &&
       (((DAT_f790 <= DAT_1413 && (DAT_1413 < DAT_f786)) && (DAT_f68f <= DAT_14a2)))) &&
      ((DAT_14a2 < DAT_f690 && ((DAT_0059 & 1) != 0)))))) {
    DAT_00a7 = DAT_00a7 | 4;
  }
  else {
    DAT_00a7 = DAT_00a7 & 0xfb;
  }
  if ((((DAT_0053 & 0x10) == 0) && ((DAT_00c8 & 0x60) == 0)) &&
     (((DAT_00cb & 0x20) == 0 &&
      (((((DAT_00ca & 8) == 0 && (DAT_f78c <= DAT_1453)) && (DAT_f78d <= DAT_140c)) &&
       ((DAT_f69f <= DAT_1522 && (DAT_1526 < DAT_f794)))))))) {
    if ((DAT_00a7 & 4) == 0) {
      if ((DAT_1524 < DAT_f796) || (DAT_f797 <= DAT_1528)) goto LAB_bf4b;
      goto LAB_bf54;
    }
    DAT_1528 = 0;
    if ((DAT_00a7 & 0x80) == 0) {
      DAT_1553 = DAT_1402;
      DAT_00a7 = DAT_00a7 | 0x80;
    }
    if (DAT_1524 < DAT_f792) goto LAB_bf54;
    if ((DAT_00a7 & 0x40) == 0) {
      DAT_00a7 = DAT_00a7 | 0x40;
      DAT_1554 = DAT_1402;
    }
    if ((DAT_1402 < DAT_f795) ||
       ((DAT_1554 <= DAT_1553 && (DAT_f688 <= (byte)(DAT_1553 - DAT_1554))))) {
      DAT_00ca = DAT_00ca & 0xbf;
      goto LAB_bf54;
    }
    if (0x31 < DAT_1525) {
      DAT_00ab = DAT_00ab | 0x40;
      DAT_00ca = DAT_00ca | 0x40;
      DAT_15d3 = 0;
      goto LAB_bf54;
    }
  }
  else {
LAB_bf4b:
    DAT_1524 = 0;
    DAT_1528 = 0;
    DAT_00a7 = DAT_00a7 & 0x3f;
LAB_bf54:
    DAT_1525 = 0;
  }
  bVar2 = DAT_00a7;
  if ((((DAT_1413 < DAT_f782) || (DAT_f783 <= DAT_1413)) || (DAT_1460 < DAT_f784)) ||
     (DAT_f785 <= DAT_1460)) {
    DAT_00a8 = DAT_00a8 & 0xfe;
  }
  else {
    DAT_00a8 = DAT_00a8 | 1;
  }
  if ((((((DAT_1453 < DAT_f780) || (DAT_140c < DAT_f781)) ||
        (((DAT_00c8 & 0x60) != 0 || ((DAT_0088 & 0x80) == 0)))) ||
       (((DAT_009b & 1) == 0 && ((DAT_009b & 8) != 0)))) || ((DAT_00b0 & 8) != 0)) ||
     ((DAT_00a8 & 1) == 0)) {
    DAT_1521 = 0;
LAB_bfd0:
    DAT_1555 = 0;
  }
  else {
    if (DAT_1521 < DAT_f689) goto LAB_bfd0;
    if ((DAT_1400 < DAT_f68a) || (DAT_1435 <= DAT_1400)) {
      DAT_00cd = DAT_00cd & 0xfb;
      goto LAB_bfd0;
    }
    if (99 < DAT_1555) {
      DAT_00cd = DAT_00cd | 4;
      goto LAB_bfd0;
    }
  }
  if (DAT_1400 < 200) {
    DAT_00cd = DAT_00cd & 0xf7;
LAB_bfe9:
    DAT_1556 = 0;
  }
  else if (0x31 < DAT_1556) {
    DAT_00cd = DAT_00cd | 8;
    goto LAB_bfe9;
  }
  if (((DAT_00cd & 4) == 0) && ((DAT_00cd & 8) == 0)) {
    DAT_00ca = DAT_00ca & 0xdf;
  }
  else {
    DAT_00ab = DAT_00ab | 0x20;
    DAT_00ca = DAT_00ca | 0x20;
    DAT_15d4 = 0;
  }
  if ((((((DAT_00ca & 0x20) == 0) && ((DAT_00c8 & 0x40) == 0)) && ((DAT_00cb & 0x20) == 0)) &&
      ((((DAT_0051 & 0x20) != 0 && (DAT_f6a3 <= DAT_1453)) &&
       ((DAT_f7a2 <= DAT_1413 && ((DAT_1413 < DAT_f7a3 && (DAT_f7a0 <= DAT_1460)))))))) &&
     (DAT_1460 < DAT_f7a1)) {
    DAT_00a7 = DAT_00a7 | 0x10;
    if (DAT_f7a4 <= DAT_152a) {
      _DAT_152b = (_DAT_148e * 2 + _DAT_152b * 3) * 2;
      DAT_00a7 = bVar2 | 0x30;
    }
    if ((DAT_00a7 & 0x20) != 0) {
      if ((byte)(_DAT_152b >> 8) < DAT_f7a5) {
        DAT_152d = (byte)(_DAT_152b - _DAT_15c5 >> 8);
        if (_DAT_152b < _DAT_15c5) {
          DAT_152d = 0;
        }
        if (DAT_152d < DAT_f7a6) {
          if (DAT_152d < DAT_f692) {
            DAT_00cd = DAT_00cd & 0xef;
          }
        }
        else {
          DAT_00cd = DAT_00cd | 0x10;
        }
      }
      goto LAB_c087;
    }
  }
  else {
    DAT_00a7 = DAT_00a7 & 0xef;
    DAT_152a = 0;
LAB_c087:
    if ((DAT_00a7 & 0x20) != 0) {
      if ((DAT_009b & 0x10) == 0) {
        DAT_00cd = DAT_00cd & 0xdf;
      }
      else if (DAT_152b < DAT_f7a7) {
        DAT_00cd = DAT_00cd | 0x20;
      }
    }
  }
  if (((DAT_00cd & 0x10) == 0) && ((DAT_00cd & 0x20) == 0)) {
    DAT_00cb = DAT_00cb & 0xf7;
  }
  else {
    DAT_00ac = DAT_00ac | 8;
    DAT_00cb = DAT_00cb | 8;
    DAT_15db = 0;
  }
  DAT_00ca = DAT_00ca & 0x7f;
  if ((DAT_00c1 & 8) != 0) {
    DAT_00ad = DAT_00ad | 0x10;
  }
  if (((DAT_0053 & 2) != 0) || ((DAT_004f & 0x80) == 0)) goto LAB_c14d;
  if ((DAT_0058 & 0x20) == 0) {
    if ((DAT_0053 & 4) == 0) {
      DAT_0058 = DAT_0058 & 0xef | 0x20;
    }
    else if (((DAT_0053 & 1) == 0) && (0x1d < DAT_1407)) {
      if (0x31 < DAT_1539) {
        DAT_0058 = DAT_0058 | 0x10;
      }
      goto LAB_c116;
    }
    DAT_1539 = 0;
  }
LAB_c116:
  if ((DAT_0058 & 0x80) == 0) {
    if (DAT_1407 == 0) {
      if (((((DAT_0053 & 5) == 0) && ((DAT_0058 & 0x10) == 0)) && (0x27 < DAT_1460)) &&
         (0x2f < DAT_1413)) {
        if (0x31 < DAT_153a) {
          DAT_0058 = DAT_0058 | 0x40;
        }
        goto LAB_c14d;
      }
    }
    else {
      DAT_0058 = DAT_0058 & 0xbf | 0x80;
    }
    DAT_153a = 0;
  }
LAB_c14d:
  if ((DAT_0053 & 2) == 0) {
    DAT_0046 = DAT_0046 & 0xfb;
  }
  else if ((DAT_0046 & 4) == 0) {
    DAT_0046 = DAT_0046 | 4;
    uVar5 = 0x8000;
    do {
      bVar2 = (byte)(uVar5 >> 8);
      uVar6 = uVar5;
      if ((bVar2 & *(byte *)((uVar5 & 0xff) - 0xeb)) != 0) {
        uStack0000 = (undefined1)_bStack_1;
        bVar7 = (char)uVar5 * '\x05';
        _bStack_1 = CONCAT11(bVar2,uStack0000);
        bVar3 = bVar2;
        while (bVar1 = (bool)(bVar3 >> 7), bVar3 = bVar3 << 1, !bVar1) {
          bVar7 = bVar7 + 1;
        }
        pbVar8 = &DAT_15c8 + bVar7;
        *pbVar8 = *pbVar8 + 1;
        uVar6 = _bStack_1;
        if (0x31 < *pbVar8) {
          *pbVar8 = 0;
          pbVar8 = (byte *)((uVar5 & 0xff) + 0xa9);
          bVar2 = ~bVar2;
          _bStack_1 = CONCAT11(bVar2,uStack0000);
          *pbVar8 = bVar2 & *pbVar8;
          pbVar8 = (byte *)((uVar5 & 0xff) + 200);
          *pbVar8 = bVar2 & *pbVar8;
          uVar6 = uVar5;
        }
      }
      bVar2 = (byte)(uVar6 >> 9);
      uVar5 = CONCAT11(bVar2,(char)uVar6);
    } while ((7 < bVar2) || (bVar2 = (char)uVar6 + 1, uVar5 = CONCAT11(0x80,bVar2), bVar2 < 5));
  }
  return;
}


// ---- FUN_c1ab @ c1ab ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_c1ab(void)

{
  undefined1 uVar1;
  undefined1 extraout_B;
  undefined2 uVar2;
  
  if ((DAT_0040 & 0x80) != 0) {
    _DAT_148e = 0x6400;
    return;
  }
  _DAT_0074 = &DAT_1700;
  _DAT_0076 = 0xfba8;
  uVar2 = 0xfba0;
  _DAT_0078 = 0xfba0;
  FUN_c1e1();
  uVar1 = FUN_99c8();
  _DAT_148e = CONCAT11(uVar1,extraout_B);
  _DAT_1486 = uVar2;
  DAT_147f = DAT_1490;
  DAT_1488 = DAT_1491;
  return;
}


// ---- FUN_c1e1 @ c1e1 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 FUN_c1e1(void)

{
  undefined2 uVar1;
  bool bVar2;
  undefined1 uVar3;
  char cVar5;
  byte bVar6;
  char extraout_B;
  undefined1 extraout_B_00;
  undefined1 extraout_B_01;
  undefined1 extraout_B_02;
  undefined1 extraout_B_03;
  short sVar4;
  undefined1 extraout_B_04;
  undefined1 extraout_B_05;
  undefined1 extraout_B_06;
  byte *pbVar7;
  ushort *puVar8;
  
  _DAT_0067 = _DAT_140a;
  _DAT_0069 = _DAT_1413;
  sVar4 = _DAT_0069;
  cVar5 = '\a';
  DAT_0069 = (byte)((ushort)_DAT_1413 >> 8);
  pbVar7 = _DAT_0078;
  do {
    if (DAT_0069 < pbVar7[1]) break;
    pbVar7 = pbVar7 + 1;
    cVar5 = cVar5 + -1;
  } while (cVar5 != '\0');
  uVar1 = *(undefined2 *)pbVar7;
  bVar6 = *_DAT_0078;
  if ((DAT_0069 < bVar6) ||
     (bVar6 = _DAT_0078[7], bVar2 = bVar6 <= DAT_0069, _DAT_0069 = sVar4, bVar2)) {
    _DAT_0069 = (ushort)bVar6 << 8;
  }
  cVar5 = '\a';
  pbVar7 = _DAT_0076;
  do {
    if ((byte)(_DAT_140a << 2) < pbVar7[1]) break;
    pbVar7 = pbVar7 + 1;
    cVar5 = cVar5 + -1;
  } while (cVar5 != '\0');
  DAT_007a = 0x7e;
  _DAT_0070 = *(undefined2 *)pbVar7;
  bVar6 = (byte)(_DAT_140a << 2);
  if (bVar6 < *_DAT_0076) {
    bVar6 = *_DAT_0076;
  }
  else {
    if (bVar6 < _DAT_0076[7]) goto LAB_c24f;
    bVar6 = _DAT_0076[7];
  }
  _DAT_0067 = (ushort)bVar6 << 2;
LAB_c24f:
  puVar8 = (ushort *)((short)_DAT_0074 + 0x7e);
  DAT_0072 = (char)((ushort)uVar1 >> 8);
  _DAT_006b = CONCAT11((char)((ushort)_DAT_0069 >> 8) - DAT_0072,(char)_DAT_0069);
  DAT_006d = '\0';
  DAT_0073 = (char)uVar1;
  DAT_006e = DAT_0073 - DAT_0072;
  DAT_006f = 0;
  _DAT_0072 = uVar1;
  _DAT_0074 = puVar8;
  FUN_8297();
  DAT_1490 = extraout_B;
  if ((puVar8[1] < *puVar8) && (DAT_006d != '\0')) {
    DAT_006d = -DAT_006d;
    uVar3 = FUN_c2f9();
    _DAT_008b = CONCAT11(uVar3,extraout_B_01) + puVar8[1];
  }
  else {
    uVar3 = FUN_c2f9();
    _DAT_008b = CONCAT11(uVar3,extraout_B_00) + *puVar8;
  }
  DAT_006d = DAT_1490;
  if ((puVar8[9] < puVar8[8]) && (DAT_1490 != '\0')) {
    DAT_006d = -DAT_1490;
    uVar3 = FUN_c2f9();
    _DAT_008d = CONCAT11(uVar3,extraout_B_03) + puVar8[9];
  }
  else {
    uVar3 = FUN_c2f9();
    _DAT_008d = CONCAT11(uVar3,extraout_B_02) + puVar8[8];
  }
  sVar4 = _DAT_0067 + (ushort)DAT_0070 * -4;
  _DAT_006b = sVar4 * 4;
  DAT_006d = (char)((char)sVar4 << 7) >> 1;
  DAT_006f = DAT_0071 - DAT_0070;
  DAT_006e = 0;
  FUN_8297();
  DAT_1491 = extraout_B_04;
  if ((_DAT_008d < _DAT_008b) && (DAT_006d != '\0')) {
    DAT_006d = -DAT_006d;
    uVar3 = FUN_c2f9();
    uVar3 = (undefined1)(CONCAT11(uVar3,extraout_B_06) + _DAT_008d >> 8);
  }
  else {
    uVar3 = FUN_c2f9();
    uVar3 = (undefined1)(CONCAT11(uVar3,extraout_B_05) + _DAT_008b >> 8);
  }
  return uVar3;
}


// ---- FUN_c2f9 @ c2f9 ----

char FUN_c2f9(void)

{
  ushort in_D;
  short sVar1;
  
  DAT_0089 = (byte)(in_D >> 8);
  sVar1 = (ushort)DAT_006d * (in_D & 0xff);
  if ((char)sVar1 < '\0') {
    sVar1 = (ushort)(byte)((char)((ushort)sVar1 >> 8) + 1) << 8;
  }
  DAT_008a = (byte)((ushort)sVar1 >> 8);
  sVar1 = (ushort)DAT_006d * (ushort)DAT_0089;
  return (char)((ushort)sVar1 >> 8) + CARRY1((byte)sVar1,DAT_008a);
}


// ---- vec_TOF @ c30e ----

undefined1 vec_TOF(void)

{
  undefined1 in_stack_00000003;
  
  FUN_c311();
  return in_stack_00000003;
}


// ---- FUN_c311 @ c311 ----

undefined1 FUN_c311(void)

{
  DAT_1567 = DAT_1567 + '\x01';
  return (char)((ushort)TIMER >> 8);
}


// ---- FUN_c46c @ c46c ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_c46c(void)

{
  if ((DAT_0054 & 1) == 0) {
    if ((DAT_00bb & 0x40) == 0) {
      if ((DAT_0040 & 2) != 0) goto LAB_c4a7;
      _DAT_106c = 0xb3b;
      _DAT_106e = 500;
      if ((DAT_0053 & 1) == 0) {
        _DAT_106c = 0x271;
        _DAT_106e = 0x177;
      }
    }
    else {
      _DAT_106c = 0x186a;
      _DAT_106e = 0x271;
    }
    DAT_1011 = 0xbf;
  }
  else {
LAB_c4a7:
    DAT_1003 = 0;
    DAT_1011 = 0x3f;
  }
  return;
}


// ---- FUN_c4b2 @ c4b2 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_c4b2(void)

{
  bool bVar1;
  bool bVar2;
  byte bVar3;
  byte bVar5;
  short sVar4;
  bool bVar6;
  
  if ((DAT_fee1 & 8) == 0) {
    return;
  }
  DAT_14dd = DAT_0040;
  if (((DAT_0054 & 8) == 0) || (DAT_1442 == 0)) {
    if (((DAT_0053 & 2) != 0) &&
       ((((DAT_0053 & 0x44) != 0 && (0x7c < DAT_14ac)) && (DAT_008f <= (byte)(DAT_14ac - 0xc))))) {
      bVar6 = 0xfe < DAT_14d8;
      bVar3 = DAT_14d8 + 1;
      bVar1 = (bVar6 || 9 < bVar3 >> 4) || 8 < bVar3 >> 4 && 9 < (bVar3 & 0xf);
      bVar2 = (byte)((DAT_14d8 & 0xf) + 1) >> 4 == 1 || 9 < (bVar3 & 0xf);
      if (bVar1 && bVar2) {
        bVar6 = 0x99 < bVar3;
        bVar3 = DAT_14d8 + 0x67;
      }
      else if (bVar1) {
        bVar6 = 0x9f < bVar3;
        bVar3 = DAT_14d8 + 0x61;
      }
      else if (bVar2) {
        bVar6 = 0xf9 < bVar3;
        bVar3 = DAT_14d8 + 7;
      }
      bVar5 = DAT_14d7 + bVar6;
      _DAT_14d7 = CONCAT11(bVar5,bVar3);
      if (bVar5 < 3) {
        DAT_14dd = DAT_0040;
        return;
      }
LAB_c531:
      DAT_14dd = DAT_0040;
      if ((DAT_0054 & 8) == 0) {
        DAT_0054 = DAT_0054 | 8;
        DAT_0056 = 0x96;
      }
      DAT_0040 = DAT_0040 | 1;
      DAT_14d4 = 0;
      return;
    }
  }
  else {
    if (0x2f < DAT_1442) {
      _DAT_005b = CONCAT21(_DAT_1465,DAT_005d);
      FUN_8001();
      sVar4 = _DAT_005c << 2;
      if ((char)((ushort)sVar4 >> 8) != '\0') {
        sVar4 = 0xff;
      }
      if (((byte)sVar4 < 0x50) || (0x80 < (byte)sVar4)) {
        DAT_14d4 = DAT_14d4 + 1;
        if (DAT_14d4 < 0x6e) {
          _DAT_14d7 = 0;
          return;
        }
        goto LAB_c531;
      }
    }
    DAT_14d4 = '\0';
  }
  _DAT_14d7 = 0;
  return;
}


// ---- FUN_c551 @ c551 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_c551(void)

{
  undefined2 *puVar1;
  
  if (((DAT_0040 & 2) == 0) || (DAT_14d4 = 0, (DAT_00bb & 0x40) != 0)) {
    if ((DAT_1408 == '\0') && (DAT_1409 < 0x65)) {
      DAT_14d4 = DAT_14d4 + 1;
      if (0x95 < DAT_14d4) {
        DAT_0040 = DAT_0040 | 6;
        puVar1 = (undefined2 *)&DAT_0048;
        do {
          *puVar1 = 0;
          puVar1 = puVar1 + 1;
        } while (puVar1 != (undefined2 *)0x140);
        puVar1 = (undefined2 *)&DAT_1400;
        do {
          *puVar1 = 0;
          puVar1 = puVar1 + 1;
        } while (puVar1 != (undefined2 *)&DAT_15c0);
        if ((DAT_0040 & 1) == 0) {
          _DAT_013e = 0xae3e;
          FUN_ae5e();
          _DAT_013e = 0xae41;
          FUN_ae98();
          _DAT_013e = 0xae44;
          FUN_b00d();
          _DAT_013e = 0xae48;
          FUN_b148();
          _DAT_013e = 0xae4b;
          FUN_b264();
          _DAT_013e = 0xae4e;
          FUN_b138();
          FUN_b0e2();
          return;
        }
        _DAT_013e = 0xae54;
        FUN_b0d6();
        _DAT_013e = 0xae57;
        FUN_ae98();
        _DAT_013e = 0xae5a;
        FUN_b00d();
        FUN_b0e2();
        return;
      }
    }
    else {
      DAT_14d4 = 0;
      DAT_0040 = DAT_0040 & 0xfd;
    }
  }
  return;
}


// ---- FUN_c57e @ c57e ----

/* WARNING: Removing unreachable block (RAM,0xa4c5) */
/* WARNING: Removing unreachable block (RAM,0xa4cc) */
/* WARNING: Removing unreachable block (RAM,0xa4c3) */
/* WARNING: Removing unreachable block (RAM,0xa51b) */
/* WARNING: Removing unreachable block (RAM,0xa525) */
/* WARNING: Removing unreachable block (RAM,0xa528) */
/* WARNING: Removing unreachable block (RAM,0xa52a) */
/* WARNING: Removing unreachable block (RAM,0xa52f) */
/* WARNING: Removing unreachable block (RAM,0xa520) */

void FUN_c57e(void)

{
  bool bVar1;
  char cVar2;
  byte bVar3;
  byte bVar4;
  
  if (((DAT_0040 & 2) == 0) || ((DAT_0054 & 1) == 0)) {
    DAT_1448 = 0;
    DAT_1446 = 0;
    DAT_14bd = 0;
    FUN_a679();
    DAT_14bb = FUN_809f();
    if (DAT_14bb < DAT_fee8) {
      DAT_1445 = DAT_fee8 - DAT_14bb;
    }
    else {
      DAT_1445 = '\0';
    }
    FUN_a7dd();
    if (((CARRY1(DAT_153b,DAT_14bb)) ||
        (bVar3 = DAT_153b + DAT_14bb + DAT_1448, CARRY1(DAT_153b + DAT_14bb,DAT_1448))) ||
       (bVar4 = bVar3 + DAT_1446, CARRY1(bVar3,DAT_1446))) {
      bVar4 = 0xff;
    }
    if (DAT_fee8 < bVar4) {
      bVar3 = DAT_14bb;
      if (DAT_14bb < DAT_fee8) {
        bVar3 = DAT_fee8;
      }
      bVar4 = ((byte)(bVar4 - bVar3) >> 1) + bVar3;
    }
    if (0x80 < bVar4) {
      bVar4 = 0x81;
    }
    if (bVar4 < DAT_14bd) {
      bVar4 = DAT_14bd;
    }
    if (bVar4 < DAT_14c1) {
      DAT_14c1 = bVar4;
    }
  }
  DAT_14ba = 0;
  if ((DAT_15c4 == '\x01') && ((DAT_004a & 0x1f) != 0)) {
    return;
  }
  cVar2 = DAT_15c4;
  if (DAT_15c4 == '\0') {
    if ((DAT_00b5 & 2) != 0) {
      DAT_00b5 = DAT_00b5 | 8;
      goto LAB_a54d;
    }
  }
  else {
    if ((DAT_00b5 & 8) == 0) {
      if ((DAT_00b5 & 2) == 0) {
        if ((DAT_00b5 & 0x10) == 0) {
          DAT_00b5 = DAT_00b5 | 0x10;
        }
        else {
          bVar3 = DAT_15c7 & 1;
          DAT_15c7 = DAT_15c7 >> 1;
          if (bVar3 != 0) {
            DAT_15c7 = DAT_15c7 | 0x80;
          }
          cVar2 = DAT_15c4 + -1;
          if ((char)(DAT_15c4 + -1) == '\0') {
            cVar2 = DAT_15c4;
          }
        }
      }
      else {
        DAT_00b5 = DAT_00b5 & 0xfd;
      }
      goto LAB_a54d;
    }
    DAT_00b5 = DAT_00b5 & 0xf7;
  }
  DAT_00b5 = DAT_00b5 | 2;
  bVar3 = 0x33;
  do {
    if (bVar3 == DAT_15c7) break;
    bVar1 = -1 < (char)bVar3;
    bVar3 = bVar3 << 1;
  } while (bVar1);
LAB_a54d:
  DAT_15c4 = cVar2;
  DAT_00bc = DAT_00bc & 0xf0;
  if ((DAT_00c0 & 0x80) == 0) {
    DAT_00c0 = DAT_00c0 & 0xbf;
  }
  else {
    DAT_00c0 = DAT_00c0 | 0x40;
  }
  return;
}


// ---- FUN_c5b6 @ c5b6 ----

void FUN_c5b6(void)

{
  if (((DAT_0040 & 2) == 0) || ((DAT_00bb & 0x40) != 0)) {
    DAT_0049 = DAT_0049 | 0x10;
    DAT_009c = DAT_009c | 0x40;
  }
  else {
    DAT_0049 = DAT_0049 & 0xef;
    DAT_009c = DAT_009c & 0xbf;
  }
  DAT_00bc = DAT_00bc & 0xbf;
  return;
}


// ---- vec_NMI @ c5d2 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void vec_NMI(void)

{
  DAT_0017 = DAT_0017 ^ 1;
  _DAT_15c1 = 0;
  vec_RESET();
  return;
}


// ---- vec_SWI @ c5dd ----

void vec_SWI(void)

{
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}


