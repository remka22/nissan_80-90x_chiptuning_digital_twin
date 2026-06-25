// ---- FUN_8000 @ 8000 ----

undefined1 FUN_8000(undefined1 param_1,undefined1 param_2)

{
  DAT_0102 = param_1;
  DAT_0103 = param_2;
  return param_1;
}


// ---- FUN_8016 @ 8016 ----

byte FUN_8016(byte param_1)

{
  return param_1 >> 4;
}


// ---- FUN_8018 @ 8018 ----

byte FUN_8018(byte param_1)

{
  return param_1 >> 3;
}


// ---- FUN_801a @ 801a ----

byte FUN_801a(byte param_1)

{
  return param_1 >> 2;
}


// ---- FUN_801f @ 801f ----

byte FUN_801f(char param_1,byte param_2)

{
  return ((((param_1 << 1 | param_2 >> 7) << 1 | (byte)(param_2 << 1) >> 7) << 1 |
          (byte)(param_2 << 2) >> 7) << 1 | (byte)(param_2 << 3) >> 7) << 1 |
         (byte)(param_2 << 4) >> 7;
}


// ---- FUN_8021 @ 8021 ----

byte FUN_8021(char param_1,byte param_2)

{
  return (((param_1 << 1 | param_2 >> 7) << 1 | (byte)(param_2 << 1) >> 7) << 1 |
         (byte)(param_2 << 2) >> 7) << 1 | (byte)(param_2 << 3) >> 7;
}


// ---- FUN_8023 @ 8023 ----

byte FUN_8023(char param_1,byte param_2)

{
  return ((param_1 << 1 | param_2 >> 7) << 1 | (byte)(param_2 << 1) >> 7) << 1 |
         (byte)(param_2 << 2) >> 7;
}


// ---- FUN_8025 @ 8025 ----

byte FUN_8025(char param_1,byte param_2)

{
  return (param_1 << 1 | param_2 >> 7) << 1 | (byte)(param_2 << 1) >> 7;
}


// ---- FUN_802b @ 802b ----

void FUN_802b(byte param_1,byte param_2)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  char cVar4;
  
  DAT_0055 = DAT_0053;
  bVar2 = param_2 + DAT_0052;
  DAT_0102 = param_1;
  param_2 = param_2 + CARRY1(param_2,DAT_0052);
  DAT_0054 = bVar2 + DAT_0053;
  bVar1 = param_2 + param_1;
  bVar3 = bVar1 + CARRY1(bVar2,DAT_0053);
  DAT_0103 = DAT_0052;
  cVar4 = bVar3 + DAT_0052;
  DAT_0052 = param_1 + (CARRY1(param_2,param_1) || CARRY1(bVar1,CARRY1(bVar2,DAT_0053))) +
             CARRY1(bVar3,DAT_0052);
  DAT_0053 = cVar4;
  return;
}


// ---- FUN_8080 @ 8080 ----

byte FUN_8080(void)

{
  byte bVar1;
  bool bVar2;
  char cVar3;
  byte bVar4;
  byte bVar5;
  byte bVar6;
  
  DAT_005a = '\x11';
  bVar4 = DAT_0052;
  bVar5 = DAT_0053;
  do {
    if ((char)DAT_0057 < '\0') {
      do {
        bVar6 = bVar5 - DAT_0058;
        cVar3 = (bVar4 - DAT_0057) - (bVar5 < DAT_0058);
        if (DAT_0057 <= bVar4 && (bVar5 < DAT_0058) <= (byte)(bVar4 - DAT_0057)) goto LAB_80c8;
        bVar2 = CARRY1(bVar6,DAT_0058);
        bVar6 = bVar6 + DAT_0058;
        cVar3 = cVar3 + DAT_0057 + bVar2;
        bVar5 = 0;
        while( true ) {
          bVar4 = DAT_0056 >> 7;
          DAT_0056 = DAT_0056 << 1 | bVar5;
          bVar2 = (bool)(DAT_0055 >> 7);
          DAT_0055 = DAT_0055 << 1 | bVar4;
          DAT_005a = DAT_005a + -1;
          if (DAT_005a == '\0') {
            if (bVar2) {
              return 0xff;
            }
            return DAT_0055;
          }
          bVar5 = DAT_0054 >> 7;
          DAT_0054 = DAT_0054 << 1 | bVar2;
          bVar5 = bVar6 << 1 | bVar5;
          bVar4 = cVar3 << 1 | bVar6 >> 7;
          if (-1 < cVar3) break;
          bVar6 = bVar5 - DAT_0058;
          cVar3 = (bVar4 - DAT_0057) - (bVar5 < DAT_0058);
LAB_80c8:
          bVar5 = 1;
        }
      } while( true );
    }
    bVar1 = DAT_0059 >> 7;
    DAT_0059 = DAT_0059 << 1;
    bVar6 = DAT_0058 >> 7;
    DAT_0058 = DAT_0058 << 1 | bVar1;
    DAT_0057 = DAT_0057 << 1 | bVar6;
    bVar1 = DAT_0056 >> 7;
    DAT_0056 = DAT_0056 << 1;
    bVar6 = DAT_0055 >> 7;
    DAT_0055 = DAT_0055 << 1 | bVar1;
    bVar1 = DAT_0054 >> 7;
    DAT_0054 = DAT_0054 << 1 | bVar6;
    bVar6 = bVar5 >> 7;
    bVar5 = bVar5 << 1 | bVar1;
    bVar2 = -1 < (char)bVar4;
    bVar4 = bVar4 << 1 | bVar6;
  } while (bVar2);
  DAT_005a = 0x11;
  return 0xff;
}


// ---- FUN_80d2 @ 80d2 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

byte FUN_80d2(byte param_1,undefined1 param_2,undefined2 param_3)

{
  char cVar1;
  byte bVar2;
  byte *pbVar3;
  
  if (0xf0 < param_1) {
    param_1 = 0xf0;
  }
  bVar2 = (char)((char)((char)(param_1 << 7) >> 1 | (param_1 >> 1) << 7) >> 1 | (param_1 >> 2) << 7)
          >> 1 | (param_1 >> 3) << 7;
  DAT_005c = (byte)param_3;
  DAT_005b = (char)((ushort)param_3 >> 8);
  _DAT_005b = (byte *)CONCAT11(DAT_005b + CARRY1(param_1 >> 4,DAT_005c),(param_1 >> 4) + DAT_005c);
  if (bVar2 != 0) {
    cVar1 = _DAT_005b[1] - *_DAT_005b;
    if (cVar1 != '\0') {
      if (_DAT_005b[1] < *_DAT_005b) {
        pbVar3 = _DAT_005b;
        cVar1 = FUN_8000(-cVar1,-bVar2);
        return cVar1 + pbVar3[1];
      }
      pbVar3 = _DAT_005b;
      cVar1 = FUN_8000();
      return cVar1 + *pbVar3;
    }
  }
  return *_DAT_005b;
}


// ---- FUN_80dd @ 80dd ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

byte FUN_80dd(byte param_1,undefined1 param_2,undefined2 param_3)

{
  char cVar1;
  byte bVar2;
  byte *pbVar3;
  
  if (0xf8 < param_1) {
    param_1 = 0xf8;
  }
  bVar2 = (char)((char)(param_1 << 7) >> 1 | (param_1 >> 1) << 7) >> 1 | (param_1 >> 2) << 7;
  DAT_005c = (byte)param_3;
  DAT_005b = (char)((ushort)param_3 >> 8);
  _DAT_005b = (byte *)CONCAT11(DAT_005b + CARRY1(param_1 >> 3,DAT_005c),(param_1 >> 3) + DAT_005c);
  if (bVar2 != 0) {
    cVar1 = _DAT_005b[1] - *_DAT_005b;
    if (cVar1 != '\0') {
      if (_DAT_005b[1] < *_DAT_005b) {
        pbVar3 = _DAT_005b;
        cVar1 = FUN_8000(-cVar1,-bVar2);
        return cVar1 + pbVar3[1];
      }
      pbVar3 = _DAT_005b;
      cVar1 = FUN_8000();
      return cVar1 + *pbVar3;
    }
  }
  return *_DAT_005b;
}


// ---- FUN_8116 @ 8116 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

char FUN_8116(char param_1,byte param_2,short param_3)

{
  bool bVar1;
  byte bVar2;
  byte bVar3;
  byte *pbVar4;
  
  bVar3 = param_1 << 1 | param_2 >> 7;
  if (0x3e < bVar3) {
    return *(char *)(param_3 + 0x7e);
  }
  DAT_0053 = 0;
  bVar3 = bVar3 * '\x02';
  DAT_005c = (byte)param_3;
  DAT_005b = (char)((ushort)param_3 >> 8);
  _DAT_005b = (byte *)CONCAT11(DAT_005b + CARRY1(bVar3,DAT_005c),bVar3 + DAT_005c);
  bVar3 = _DAT_005b[3];
  bVar1 = bVar3 < _DAT_005b[1];
  bVar2 = _DAT_005b[2] - *_DAT_005b;
  DAT_0052 = param_2 << 1;
  if (*_DAT_005b <= _DAT_005b[2] && bVar1 <= bVar2) {
    pbVar4 = _DAT_005b;
    FUN_802b();
    return *pbVar4 + DAT_0052 + CARRY1(pbVar4[1],DAT_0053);
  }
  pbVar4 = _DAT_005b;
  FUN_802b(~(bVar2 - bVar1) + (0xfe < (byte)~(bVar3 - _DAT_005b[1])));
  return (*pbVar4 - DAT_0052) - (pbVar4[1] < DAT_0053);
}


// ---- FUN_815d @ 815d ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_815d(void)

{
  bool bVar1;
  undefined2 uVar2;
  short sVar3;
  char cVar4;
  char cVar5;
  char cVar6;
  byte bVar7;
  char cVar8;
  byte bVar9;
  byte bVar10;
  byte *pbVar11;
  
  _DAT_005e = _P3SCR;
  uVar2 = _DAT_005e;
  _DAT_0060 = _DAT_0020;
  sVar3 = _DAT_0060;
  if ((char)DAT_0075 < '\0') {
    cVar8 = '\t';
  }
  else {
    cVar8 = '\x0f';
  }
  DAT_0060 = (byte)((ushort)_DAT_0020 >> 8);
  pbVar11 = _DAT_006f;
  do {
    if (DAT_0060 < pbVar11[1]) break;
    pbVar11 = pbVar11 + 1;
    cVar8 = cVar8 + -1;
  } while (cVar8 != '\0');
  if ((char)DAT_0075 < '\0') {
    cVar4 = '\t';
  }
  else {
    cVar4 = '\x0f';
  }
  DAT_0069 = *pbVar11;
  DAT_006a = pbVar11[1];
  bVar9 = *_DAT_006f;
  if (DAT_0060 < bVar9) {
LAB_81a6:
    _DAT_0060 = (ushort)bVar9 << 8;
  }
  else {
    if ((char)DAT_0075 < '\0') {
      bVar9 = _DAT_006f[9];
    }
    else {
      bVar9 = _DAT_006f[0xf];
    }
    bVar1 = bVar9 <= DAT_0060;
    _DAT_0060 = sVar3;
    if (bVar1) goto LAB_81a6;
  }
  DAT_005e = (byte)((ushort)_P3SCR >> 8);
  DAT_005f = (byte)_P3SCR;
  pbVar11 = _DAT_006d;
  if ((char)DAT_0075 < '\0') {
    cVar5 = '\t';
  }
  else {
    cVar5 = '\x0f';
  }
  do {
    if ((byte)((char)((char)DAT_005f >> 1 | DAT_005e << 7) >> 1 | (DAT_005e >> 1) << 7) < pbVar11[1]
       ) break;
    pbVar11 = pbVar11 + 1;
    cVar5 = cVar5 + -1;
  } while (cVar5 != '\0');
  if ((char)DAT_0075 < '\0') {
    cVar6 = '\t';
  }
  else {
    cVar6 = '\x0f';
  }
  DAT_0071 = (cVar6 - cVar5) * '\x10' + (cVar4 - cVar8);
  DAT_0067 = *pbVar11;
  DAT_0068 = pbVar11[1];
  bVar9 = (char)((char)DAT_005f >> 1 | DAT_005e << 7) >> 1 | (DAT_005e >> 1) << 7;
  if (bVar9 < *_DAT_006d) {
    bVar9 = *_DAT_006d;
  }
  else {
    _DAT_005e = uVar2;
    if ((char)DAT_0075 < '\0') {
      if (bVar9 < _DAT_006d[9]) goto LAB_8210;
      bVar9 = _DAT_006d[9];
    }
    else {
      if (bVar9 < _DAT_006d[0xf]) goto LAB_8210;
      bVar9 = _DAT_006d[0xf];
    }
  }
  _DAT_005e = CONCAT11((bVar9 >> 7) << 1 | (byte)(bVar9 << 1) >> 7,bVar9 << 2);
LAB_8210:
  bVar1 = CARRY1(DAT_0071,DAT_006c);
  DAT_006c = DAT_0071 + DAT_006c;
  bVar10 = DAT_006b + bVar1;
  DAT_0062 = DAT_0060 - DAT_0069;
  DAT_0063 = DAT_0061;
  DAT_0064 = 0;
  DAT_0065 = DAT_006a - DAT_0069;
  DAT_0066 = 0;
  DAT_006b = bVar10;
  FUN_8386();
  bVar7 = (DAT_005e - ((DAT_0067 >> 7) << 1 | (byte)(DAT_0067 << 1) >> 7)) -
          (DAT_005f < (byte)(DAT_0067 * '\x04'));
  bVar9 = (char)(DAT_005f + DAT_0067 * -4) >> 1;
  DAT_0062 = bVar7 >> 2;
  bVar7 = (char)(bVar9 | bVar7 * -0x80) >> 1 | (bVar7 >> 1) << 7;
  DAT_0064 = (char)(DAT_005f * -0x80) >> 1 | bVar9 << 7;
  DAT_0066 = DAT_0068 - DAT_0067;
  DAT_0065 = 0;
  DAT_0063 = bVar7;
  DAT_0069 = bVar10;
  FUN_8386();
  DAT_006a = bVar7;
  do {
    *(char *)((short)register0x12 + -1) = -0x7e;
    *(char *)((short)register0x12 + 0x10000) = 'm';
    FUN_82ef();
    bVar9 = DAT_0069;
    if (DAT_006c < DAT_006b) {
      cVar8 = -DAT_0069;
      bVar9 = 0;
      if (cVar8 == '\0') goto LAB_8276;
      *(char *)((short)register0x12 + -1) = -0x7e;
      *(char *)((short)register0x12 + 0x10000) = -0x77;
      cVar4 = FUN_8000();
      if (cVar8 < '\0') {
        cVar4 = cVar4 + '\x01';
      }
      cVar4 = cVar4 + DAT_006c;
    }
    else {
LAB_8276:
      *(char *)((short)register0x12 + -1) = -0x7e;
      *(char *)((short)register0x12 + 0x10000) = 'y';
      cVar4 = FUN_8000();
      if ((char)bVar9 < '\0') {
        cVar4 = cVar4 + '\x01';
      }
      cVar4 = cVar4 + DAT_006b;
    }
    _DAT_006f = (byte *)CONCAT11(cVar4,DAT_0070);
    bVar9 = DAT_0069;
    if (DAT_006e < DAT_006d) {
      cVar8 = -DAT_0069;
      bVar9 = 0;
      if (cVar8 == '\0') goto LAB_829b;
      *(char *)((short)register0x12 + -1) = -0x7e;
      *(char *)((short)register0x12 + 0x10000) = -0x52;
      cVar4 = FUN_8000();
      if (cVar8 < '\0') {
        cVar4 = cVar4 + '\x01';
      }
      bVar9 = cVar4 + DAT_006e;
    }
    else {
LAB_829b:
      *(char *)((short)register0x12 + -1) = -0x7e;
      *(char *)((short)register0x12 + 0x10000) = -0x62;
      cVar8 = FUN_8000();
      if ((char)bVar9 < '\0') {
        cVar8 = cVar8 + '\x01';
      }
      bVar9 = cVar8 + DAT_006d;
    }
    _DAT_006f = (byte *)CONCAT11(DAT_006f,bVar9);
    bVar7 = DAT_006a;
    if (bVar9 < DAT_006f) {
      cVar8 = -DAT_006a;
      bVar7 = 0;
      if (cVar8 == '\0') goto LAB_82bf;
      *(char *)((short)register0x12 + -1) = -0x7e;
      *(char *)((short)register0x12 + 0x10000) = -0x2f;
      cVar4 = FUN_8000();
      if (cVar8 < '\0') {
        cVar4 = cVar4 + '\x01';
      }
      cVar4 = cVar4 + DAT_0070;
    }
    else {
LAB_82bf:
      *(char *)((short)register0x12 + -1) = -0x7e;
      *(char *)((short)register0x12 + 0x10000) = -0x3e;
      cVar4 = FUN_8000();
      if ((char)bVar7 < '\0') {
        cVar4 = cVar4 + '\x01';
      }
      cVar4 = cVar4 + DAT_006f;
    }
    if ((DAT_0075 & 0x40) == 0) {
      return;
    }
    if ((DAT_0075 & 0x20) != 0) {
      DAT_0075 = DAT_0075 & 0xdf;
      return;
    }
    DAT_0075 = DAT_0075 | 0x20;
    *(char *)register0x12 = cVar4;
    register0x12 = (BADSPACEBASE *)((short)register0x12 + -1);
  } while( true );
}


// ---- FUN_82ef @ 82ef ----

void FUN_82ef(undefined1 param_1,undefined1 param_2,byte *param_3)

{
  byte bVar1;
  
  if ((DAT_0075 & 0x40) == 0) {
    if ((DAT_0075 & 0x10) != 0) {
      bVar1 = *param_3;
      if (((char)bVar1 < '\0') && (bVar1 < 0xf7)) {
        bVar1 = bVar1 & 0x7f;
        DAT_0075 = DAT_0075 | 8;
      }
      else {
        DAT_0075 = DAT_0075 & 0xf7;
      }
      DAT_006b = bVar1 + 0x80;
      DAT_006c = FUN_836c(param_3[1]);
      DAT_006d = FUN_836c(param_3[0x10]);
      DAT_006e = FUN_836c(param_3[0x11]);
      return;
    }
    DAT_006b = *param_3;
    DAT_006c = param_3[1];
    DAT_006d = param_3[0x10];
    DAT_006e = param_3[0x11];
    return;
  }
  if ((DAT_0075 & 0x20) != 0) {
    bVar1 = *param_3;
    if (-1 < (char)bVar1) {
      bVar1 = 0x40;
    }
    DAT_006b = bVar1 & 0x7f;
    bVar1 = param_3[1];
    if (-1 < (char)bVar1) {
      bVar1 = 0x40;
    }
    DAT_006c = bVar1 & 0x7f;
    bVar1 = param_3[0x10];
    if (-1 < (char)bVar1) {
      bVar1 = 0x40;
    }
    DAT_006d = bVar1 & 0x7f;
    bVar1 = param_3[0x11];
    if (-1 < (char)bVar1) {
      bVar1 = 0x40;
    }
    DAT_006e = bVar1 & 0x7f;
    return;
  }
  DAT_006b = *param_3;
  if ((char)DAT_006b < '\0') {
    DAT_006b = 0;
  }
  DAT_006c = param_3[1];
  if ((char)DAT_006c < '\0') {
    DAT_006c = 0;
  }
  DAT_006d = param_3[0x10];
  if ((char)DAT_006d < '\0') {
    DAT_006d = 0;
  }
  DAT_006e = param_3[0x11];
  if ((char)DAT_006e < '\0') {
    DAT_006e = 0;
  }
  return;
}


// ---- FUN_836c @ 836c ----

char FUN_836c(byte param_1)

{
  if (param_1 < 0xf7) {
    param_1 = param_1 & 0x7f;
  }
  return param_1 + 0x80;
}


// ---- FUN_8386 @ 8386 ----

void FUN_8386(void)

{
  byte bVar1;
  bool bVar2;
  char cVar3;
  byte bVar4;
  undefined1 uVar5;
  byte bVar6;
  byte bVar7;
  
  uVar5 = 0;
  if (DAT_0065 != 0 || DAT_0066 != 0) {
    DAT_005d = '\t';
    bVar7 = DAT_0062;
    bVar4 = DAT_0063;
    do {
      if ((char)DAT_0065 < '\0') {
        do {
          bVar6 = bVar4 - DAT_0066;
          cVar3 = (bVar7 - DAT_0065) - (bVar4 < DAT_0066);
          if (DAT_0065 <= bVar7 && (bVar4 < DAT_0066) <= (byte)(bVar7 - DAT_0065)) goto LAB_83c6;
          bVar2 = CARRY1(bVar6,DAT_0066);
          bVar6 = bVar6 + DAT_0066;
          cVar3 = cVar3 + DAT_0065 + bVar2;
          bVar7 = 0;
          while( true ) {
            bVar2 = (bool)(DAT_0064 >> 7);
            DAT_0064 = DAT_0064 << 1 | bVar7;
            DAT_005d = DAT_005d + -1;
            if (DAT_005d == '\0') {
              if (!bVar2) {
                return;
              }
              goto LAB_83a6;
            }
            bVar4 = bVar6 << 1 | bVar2;
            bVar7 = cVar3 << 1 | bVar6 >> 7;
            if (-1 < cVar3) break;
            bVar6 = bVar4 - DAT_0066;
            cVar3 = (bVar7 - DAT_0065) - (bVar4 < DAT_0066);
LAB_83c6:
            bVar7 = 1;
          }
        } while( true );
      }
      bVar6 = DAT_0066 >> 7;
      DAT_0066 = DAT_0066 << 1;
      DAT_0065 = DAT_0065 << 1 | bVar6;
      bVar1 = DAT_0064 >> 7;
      DAT_0064 = DAT_0064 << 1;
      bVar6 = bVar4 >> 7;
      bVar4 = bVar4 << 1 | bVar1;
      bVar2 = -1 < (char)bVar7;
      bVar7 = bVar7 << 1 | bVar6;
    } while (bVar2);
LAB_83a6:
    uVar5 = 0xff;
  }
  DAT_0064 = uVar5;
  return;
}


// ---- vec_RESET @ 83ce ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void vec_RESET(void)

{
  undefined1 uVar1;
  char cVar2;
  undefined1 *puVar3;
  
  puVar3 = (undefined1 *)0x0;
  _DAT_00fc = 0;
  _DAT_00fe = 0;
  do {
    *puVar3 = 0;
    puVar3 = puVar3 + 1;
  } while (puVar3 != &DAT_00fc);
  puVar3 = &DAT_1000;
  do {
    *puVar3 = 0;
    puVar3[1] = 0;
    puVar3 = puVar3 + 2;
  } while (puVar3 != &DAT_1400);
  _DAT_00fa = 0x83f4;
  uVar1 = FUN_8430(0xff,0xb);
  _DAT_00fa = 0x83f8;
  FUN_8430(uVar1,0xb);
  DAT_0017 = 0x36;
  DAT_0018 = 0x36;
  _DAT_00fa = 0x8400;
  uVar1 = FUN_8430();
  _DAT_00fa = 0x8404;
  uVar1 = FUN_8430(uVar1,0x60);
  _DAT_00fa = 0x8408;
  cVar2 = FUN_8430(uVar1,1);
  _DAT_00fa = 0x840e;
  uVar1 = FUN_8430(cVar2 + '\x02',200);
  _DAT_00fa = 0x8412;
  uVar1 = FUN_8430(uVar1,0);
  _DAT_00fa = 0x8416;
  uVar1 = FUN_8430(uVar1,100);
  _DAT_00fa = 0x841a;
  uVar1 = FUN_8430(uVar1,100);
  _DAT_00fa = 0x841e;
  uVar1 = FUN_8430(uVar1,0);
  _DAT_00fa = 0x8422;
  uVar1 = FUN_8430(uVar1,0x33);
  _DAT_00fa = 0x8426;
  uVar1 = FUN_8430(uVar1,0xf);
  _DAT_00fa = 0x842a;
  uVar1 = FUN_8430(uVar1,1);
  _DAT_00fa = 0x842e;
  FUN_8430(uVar1,0x58);
  FUN_8438();
  return;
}


// ---- FUN_8430 @ 8430 ----

void FUN_8430(char param_1,undefined1 param_2)

{
  DAT_0100 = param_1 + '\x01';
  DAT_0101 = param_2;
  return;
}


// ---- FUN_8438 @ 8438 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8438(void)

{
  FUN_8430();
  FUN_8430();
  if ((P1DDR & 4) == 0) {
    RX = 0x92;
  }
  else {
    RX = 0x80;
  }
  DAT_004a = 0;
  DAT_0300 = 0;
  DAT_0200 = RX;
  FUN_8430();
  DAT_101b = 0xac;
  DAT_001f = 0x20;
  DAT_101f = 0x20;
  DAT_008d = 5;
  DAT_004c = DAT_bfbe;
  DAT_0039 = 9;
  DAT_0016 = 0x99;
  DAT_0019 = 5;
  DAT_1010 = 5;
  DAT_0030 = 100;
  DAT_00cc = 100;
  DAT_1047 = 100;
  DAT_0032 = 0x20;
  DAT_002c = 0xff;
  DAT_007c = 0xff;
  DAT_00c3 = 0xff;
  DAT_0035 = DAT_bfa0;
  DAT_0094 = 0x2b;
  _DAT_0098 = 0x804;
  if (DAT_bef6 == 0) {
    FUN_84ee();
  }
  if (_DAT_1400 != -0x55ab) {
    _DAT_1400 = -0x55ab;
    DAT_1404 = 0xff;
    DAT_142a = 0;
    DAT_142b = 0;
    _DAT_1425 = 0;
    _DAT_1427 = 0;
    DAT_1429 = 0;
    FUN_84ee();
  }
  _P2DDR = _DAT_1425;
  _P2DATA = _DAT_1427;
  P4DDR = DAT_1429;
  DAT_1054 = DAT_1404 + 4;
  if (0xfb < DAT_1404) {
    DAT_1054 = -1;
  }
  FUN_8506();
  return;
}


// ---- FUN_84ee @ 84ee ----

void FUN_84ee(void)

{
  undefined1 *puVar1;
  
  puVar1 = &DAT_1500;
  DAT_1405 = 100;
  DAT_1406 = 0;
  do {
    *puVar1 = 100;
    puVar1[1] = 0;
    puVar1 = puVar1 + 2;
  } while (puVar1 != (undefined1 *)0x1700);
  return;
}


// ---- FUN_8506 @ 8506 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8506(void)

{
  undefined1 uVar1;
  
  do {
  } while ((DAT_0101 & 0x20) == 0);
  _DAT_0100 = 0x1c41;
  do {
    do {
      if (((DAT_007f < 0x32) || (RX = RX & 0xcd, DAT_0200 = RX, (DAT_0036 & 1) != 0)) ||
         (1 < DAT_000c)) {
LAB_8546:
        DAT_1000 = DAT_1000 & 0xbf;
      }
      else {
        if ((IMPCAP == '\0') && (DAT_000e < 200)) {
          DAT_009c = 0;
          goto LAB_8546;
        }
        DAT_009c = DAT_009c | 0x80;
        DAT_1000 = DAT_1000 | 0x40;
        if (0xe3 < DAT_009c) {
          P2DDR = P2DDR | 0x40;
          DAT_00fe = DAT_00fe | 2;
          DAT_1408 = 0;
        }
      }
      if ((DAT_0036 & 8) != 0) {
        DAT_009c = 0;
        DAT_00aa = 0;
        FUN_863d();
        return;
      }
      if (DAT_008a == '\0') {
        DAT_001b = 0;
        uVar1 = 0;
      }
      else {
        FUN_80d2();
        uVar1 = 4;
        DAT_001b = FUN_8000();
      }
      DAT_001a = 5;
      _DAT_0100 = CONCAT11(6,uVar1);
      DAT_00a6 = 0;
      DAT_001c = uVar1;
    } while (-1 < DAT_001f);
    if (DAT_0048 < 4) {
      if ((TRCS & 2) == 0) {
        DAT_0085 = DAT_000a;
      }
      else if ((((TRCS & 0x44) != 0) && (0x7c < DAT_0085)) && (DAT_000a <= (byte)(DAT_0085 - 0xc)))
      goto LAB_85e6;
      DAT_00aa = 0;
      DAT_1000 = DAT_1000 & 0x7f;
    }
    else {
LAB_85e6:
      DAT_00aa = DAT_00aa | 0x80;
      DAT_1000 = DAT_1000 | 0x80;
      if (0x89 < DAT_00aa) {
        P2DDR = P2DDR | 0x80;
      }
    }
    if ((OUTCMP < 3) || (0xf7 < OUTCMP)) {
      P2DDR = P2DDR | 0x20;
      DAT_1000 = DAT_1000 | 0x20;
    }
    else {
      DAT_1000 = DAT_1000 & 0xdf;
    }
  } while( true );
}


// ---- FUN_8630 @ 8630 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8630(void)

{
  undefined1 uVar1;
  char cVar2;
  undefined1 *puVar3;
  
  P1DDR = P1DDR | 4;
  puVar3 = &P4DATA;
  do {
    *puVar3 = 0;
    puVar3 = puVar3 + 1;
  } while (puVar3 != &DAT_00fc);
  puVar3 = &DAT_1000;
  do {
    *puVar3 = 0;
    puVar3[1] = 0;
    puVar3 = puVar3 + 2;
  } while (puVar3 != &DAT_1400);
  _DAT_00fa = 0x83f4;
  uVar1 = FUN_8430(0xff,0xb);
  _DAT_00fa = 0x83f8;
  FUN_8430(uVar1,0xb);
  DAT_0017 = 0x36;
  DAT_0018 = 0x36;
  _DAT_00fa = 0x8400;
  uVar1 = FUN_8430();
  _DAT_00fa = 0x8404;
  uVar1 = FUN_8430(uVar1,0x60);
  _DAT_00fa = 0x8408;
  cVar2 = FUN_8430(uVar1,1);
  _DAT_00fa = 0x840e;
  uVar1 = FUN_8430(cVar2 + '\x02',200);
  _DAT_00fa = 0x8412;
  uVar1 = FUN_8430(uVar1,0);
  _DAT_00fa = 0x8416;
  uVar1 = FUN_8430(uVar1,100);
  _DAT_00fa = 0x841a;
  uVar1 = FUN_8430(uVar1,100);
  _DAT_00fa = 0x841e;
  uVar1 = FUN_8430(uVar1,0);
  _DAT_00fa = 0x8422;
  uVar1 = FUN_8430(uVar1,0x33);
  _DAT_00fa = 0x8426;
  uVar1 = FUN_8430(uVar1,0xf);
  _DAT_00fa = 0x842a;
  uVar1 = FUN_8430(uVar1,1);
  _DAT_00fa = 0x842e;
  FUN_8430(uVar1,0x58);
  FUN_8438();
  return;
}


// ---- FUN_863d @ 863d ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_863d(void)

{
  byte bVar1;
  byte bVar2;
  char cVar3;
  byte bVar4;
  undefined1 uVar5;
  undefined1 *puVar6;
  undefined1 *puVar7;
  byte bStack0000;
  
  if (DAT_0020 < DAT_bfbc) {
    DAT_00b3 = 0;
LAB_8654:
    if ((((TRCS & 3) != 0) || ((DAT_0079 & 1) != 0)) || (DAT_bf9f <= TX)) goto LAB_8694;
    if (0x40 < DAT_007e) {
      if (0x68 < TX) goto LAB_8677;
      goto LAB_8694;
    }
    if (TX < 0x7d) goto LAB_8694;
LAB_8677:
    if ((DAT_003e & 1) != 0) {
      if (DAT_008c < DAT_bf23) goto LAB_868b;
      goto LAB_8694;
    }
    if (DAT_bf22 <= DAT_008c) goto LAB_8694;
LAB_868b:
    DAT_003e = DAT_003e | 1;
    _DAT_0100 = 0x802;
  }
  else {
    DAT_00b3 = DAT_00b3 | 0x80;
    if (DAT_00b3 < DAT_bfbd) goto LAB_8654;
LAB_8694:
    DAT_003e = DAT_003e & 0xfe;
    _DAT_0100 = 0x8c6;
  }
  if (((DAT_008c < DAT_b78e) || (DAT_b78f < DAT_008c)) ||
     ((DAT_0020 < DAT_b790 || ((DAT_b791 <= DAT_1055 || ((DAT_003e & 1) == 0)))))) {
    DAT_1009 = DAT_1009 & 0xfb;
  }
  else {
    DAT_1009 = DAT_1009 | 4;
  }
  if (((((DAT_007e < DAT_b780) || (TX < DAT_b781)) || ((DAT_00b7 & 0x80) == 0)) ||
      ((DAT_0020 < DAT_b782 || (DAT_b783 <= DAT_0020)))) ||
     ((DAT_008c < DAT_b784 || (DAT_b785 <= DAT_008c)))) {
    DAT_100a = DAT_100a & 0xfe;
  }
  else {
    DAT_100a = DAT_100a | 1;
  }
  if (DAT_008c < DAT_b901) {
    _DAT_1035 = DAT_bff2;
    if (DAT_b900 <= TX) {
      _DAT_1035 = DAT_bf94;
    }
  }
  else {
    _DAT_1035 = DAT_bff4;
    if (DAT_b900 <= TX) {
      _DAT_1035 = DAT_bff6;
    }
  }
  DAT_00a6 = 0;
  bVar2 = DAT_bee9;
  bVar1 = DAT_beeb;
  if ((DAT_004a & 1) == 0) {
    bVar2 = DAT_bee9 - 0x28;
    bVar1 = DAT_beeb - 0x10;
  }
  if ((bVar2 < DAT_0048) || (bVar1 < DAT_0020)) {
    DAT_004a = DAT_004a & 0xfe;
  }
  else {
    DAT_004a = DAT_004a | 1;
  }
  DAT_0300 = DAT_004a;
  if ((P1DDR & 0x20) != 0) {
    if ((DAT_0200 & 2) == 0) {
      P1DDR = P1DDR & 0xcf;
    }
    else {
      bVar1 = (byte)_DAT_0100;
      _DAT_0100 = CONCAT11(0xd,bVar1);
      if (bVar1 == 0) {
        if ((DAT_0200 & 1) == 0) {
          if ((P1DDR & 0x80) == 0) {
            FUN_8c24(P1DDR,0,0x1100);
            FUN_8c24();
            FUN_8c24();
            FUN_8c24();
            FUN_8c24();
            FUN_8c24();
            FUN_8c24();
            FUN_8c24();
            FUN_8c24();
            return;
          }
        }
        else if (OUTCMP < 0x21) {
          bVar1 = TCSR;
          if ((TRCS & 0x10) == 0) {
            if (0x1f < TCSR) goto LAB_8bd3;
          }
          else if (TCSR < 0xf0) {
LAB_8bd3:
            P1DDR = P1DDR | 0x10;
            goto LAB_876d;
          }
          P1DDR = P1DDR & 0xef;
        }
        else {
          bVar1 = OUTCMP;
          if ((P1DDR & 0x40) == 0) {
            P1DDR = P1DDR | 0x40;
            FUN_8c5d();
          }
        }
      }
    }
  }
LAB_876d:
  if ((TRCS & 0x40) != 0) {
    bVar1 = DAT_008c;
    if ((DAT_008c < DAT_bfb7) && (bVar1 = DAT_0020, DAT_0020 < DAT_bf21)) {
      if ((TRCS & 0x80) == 0) {
        bVar1 = DAT_0020;
        if (DAT_003f == '\0') goto LAB_8798;
      }
      else {
        bVar1 = DAT_0020;
        if ((DAT_befc <= DAT_0020) || (bVar1 = DAT_008c, DAT_bf81 <= DAT_008c)) goto LAB_8798;
      }
      DAT_003e = DAT_003e | 0x80;
    }
    else {
LAB_8798:
      DAT_003e = DAT_003e & 0x7f;
    }
  }
  DAT_0075 = DAT_0075 & 0x4f | 0x40;
  _DAT_006b = 0xbd00;
  if ((DAT_bee0 & 0x10) == 0) {
    _DAT_006d = 0xbac0;
    _DAT_006f = 0xbab0;
  }
  else {
    _DAT_006d = 0xbb00;
    _DAT_006f = 0xbaf0;
  }
  DAT_0051 = FUN_815d();
  if ((DAT_003e & 8) == 0) {
    if (1 < bVar1) goto LAB_87e7;
LAB_87de:
    bVar4 = DAT_003e & 0xf7;
    bVar1 = 0;
  }
  else {
    if (bVar1 == 0) goto LAB_87de;
LAB_87e7:
    bVar4 = DAT_003e | 8;
    bVar2 = DAT_003e & 0x80;
    DAT_003e = bVar4;
    if (bVar2 != 0) goto LAB_87de;
  }
  _DAT_005e = _P3SCR;
  DAT_0027 = bVar1;
  DAT_003e = bVar4;
  bStack0000 = FUN_80d2();
  FUN_80d2();
  bVar1 = bStack0000;
  bVar2 = FUN_8000();
  bVar1 = bVar2 << 1 | bVar1 >> 7;
  if ((((bool)(bVar2 >> 7)) || (bVar2 = bVar1 + DAT_bf8e, CARRY1(bVar1,DAT_bf8e))) ||
     ((bVar1 = DAT_bf8e + 5, (byte)(DAT_bf8e + 5) <= bVar2 && (bVar1 = bVar2, 0x60 < bVar2)))) {
    DAT_0040 = '\x18';
  }
  else {
    DAT_0040 = 'x' - bVar1;
  }
  _DAT_0100 = CONCAT11(3,DAT_0040);
  if ((TRCS & 2) == 0) {
    if ((TRCS & 1) != 0) {
      bVar1 = DAT_0020;
      if ((DAT_003e & 0x20) != 0) {
        bVar1 = DAT_0020 + 8;
      }
      if (DAT_bf70 <= bVar1) {
        bVar1 = TX;
        if ((DAT_003e & 0x20) != 0) {
          bVar1 = TX + 5;
        }
        if (DAT_bf71 <= bVar1) {
          bVar1 = DAT_bf72;
          if ((DAT_003e & 0x20) != 0) {
            bVar1 = DAT_bf72 + 0x10;
          }
          if (DAT_0048 <= bVar1) {
            DAT_003e = DAT_003e | 0x20;
            goto LAB_8913;
          }
        }
      }
      DAT_003e = DAT_003e & 0xdf | 0x40;
      bVar1 = FUN_80d2();
      if (DAT_bfd4 < TX) {
        if (TX <= (byte)(DAT_bfd4 + 0x1e)) {
          bStack0000 = bVar1;
          FUN_8000();
          cVar3 = FUN_8000();
          bVar1 = cVar3 + bStack0000;
        }
      }
      else {
        bVar1 = bVar1 + DAT_bfd9;
      }
      goto LAB_885b;
    }
    if ((((TX < DAT_bfd5) && (0x40 < DAT_007e)) && (DAT_007e < 0x55)) && (DAT_bfd4 <= TX)) {
      bVar1 = DAT_008c;
      bVar2 = DAT_0020;
      if ((DAT_0075 & 4) != 0) {
        bVar1 = DAT_008c + 10;
        bVar2 = DAT_0020 + 8;
      }
      if ((bVar2 < DAT_bfd6) && (bVar1 < DAT_bfd7)) {
        DAT_0075 = DAT_0075 & 0xfb;
        DAT_003e = DAT_003e & 0xbf;
        bVar1 = FUN_80d2();
        goto LAB_885b;
      }
    }
LAB_8913:
    puVar6 = (undefined1 *)0xbfe0;
    if ((DAT_bfdc <= DAT_008c) && (puVar6 = (undefined1 *)0xbfe3, DAT_bfdd <= DAT_008c)) {
      puVar6 = &DAT_bfe6;
    }
    puVar7 = puVar6;
    if ((DAT_bfda <= DAT_0020) && (puVar7 = puVar6 + 1, DAT_bfdb <= DAT_0020)) {
      puVar7 = puVar6 + 2;
    }
    DAT_0088 = *puVar7;
    DAT_0075 = DAT_0075 & 0x1f | 0x14;
    DAT_003e = DAT_003e & 0xbf;
    _DAT_006b = 0xbc00;
    if ((DAT_bee0 & 0x10) == 0) {
      _DAT_006d = 0xbae0;
      _DAT_006f = 0xbad0;
    }
    else {
      _DAT_006d = 0xbb20;
      _DAT_006f = 0xbb10;
    }
    cVar3 = FUN_815d();
    bStack0000 = cVar3 + 0x80;
    if ((DAT_bfd3 & 8) != 0) {
      if ((DAT_0075 & 8) == 0) {
        DAT_008b = 0;
        DAT_0088 = 0;
      }
      else {
        DAT_008b = FUN_80d2();
      }
    }
    if ((((DAT_bf10 == 0xff) || (bVar1 = bStack0000, DAT_00a7 <= DAT_bf10)) &&
        ((cVar3 = FUN_80d2(), -1 < (char)bStack0000 ||
         (bVar1 = cVar3 + bStack0000, -1 < (char)bVar1)))) &&
       (bVar1 = cVar3 + bStack0000, 0x3b < bVar1)) {
      bVar1 = 0x3c;
    }
    bStack0000 = bVar1;
    cVar3 = FUN_80d2();
    DAT_0041 = bStack0000 - cVar3;
    if (DAT_0027 == 0) goto LAB_8a01;
    if ((DAT_003e & 0x10) != 0) {
      if ((byte)(DAT_bf12 - 2) <= TX) goto LAB_89e8;
      goto LAB_89fb;
    }
    if (TX < DAT_bf12) goto LAB_8a01;
    DAT_003e = DAT_003e | 0x10;
LAB_89e8:
    DAT_0026 = DAT_bf11;
    if ((DAT_bee0 & 0x40) != 0) {
      DAT_0041 = DAT_0041 - DAT_bf13;
      goto LAB_8a01;
    }
  }
  else {
    bVar1 = FUN_80d2();
    if (DAT_0048 < 8) {
      bVar1 = DAT_0048;
      FUN_8000();
      FUN_8018();
    }
LAB_885b:
    DAT_008b = 0;
    DAT_0088 = 0;
    DAT_0041 = bVar1;
LAB_89fb:
    DAT_003e = DAT_003e & 0xef;
LAB_8a01:
    DAT_0026 = '\0';
  }
  if ((DAT_bf8a <= (byte)(DAT_0026 + DAT_0027)) &&
     (DAT_0026 = DAT_bf8a - DAT_0027, DAT_bf8a < DAT_0027)) {
    DAT_0026 = '\0';
  }
  if ((TRCS & 1) == 0) {
    bVar1 = TX;
    if ((DAT_003b & 1) == 0) {
      bVar1 = TX + 5;
    }
    if (bVar1 < DAT_bfc7) {
      if ((0x40 < DAT_007e) && (DAT_007e != 0xff)) {
        DAT_003b = DAT_003b | 1;
        goto LAB_8a45;
      }
    }
    else {
      DAT_003b = DAT_003b & 0xfe;
    }
    DAT_004a = DAT_004a & 0xfb;
  }
  else {
LAB_8a45:
    DAT_004a = DAT_004a | 4;
  }
  if ((TRCS & 2) == 0) {
    if (DAT_00b4 != '\0') {
      bVar1 = DAT_b906;
      bVar2 = DAT_b907;
      if ((RX & 0x20) == 0) {
        bVar1 = DAT_b906 - 10;
        bVar2 = DAT_b907 - 0x10;
      }
      if ((DAT_008c <= bVar1) && (cVar3 = DAT_00b4, DAT_0020 <= bVar2)) goto LAB_8ab2;
    }
LAB_8aa1:
    RX = RX & 0xdf | 0x10;
  }
  else {
    bVar1 = DAT_007e;
    if ((((char)DAT_bfd3 < '\0') && (bVar1 = DAT_00ff, (DAT_1003 & 0x40) != 0)) ||
       ((cVar3 = DAT_bf78, bVar1 < DAT_bf76 && (cVar3 = DAT_bf79, bVar1 < DAT_bf77))))
    goto LAB_8aa1;
LAB_8ab2:
    DAT_00b4 = cVar3;
    RX = RX | 0x30;
  }
  DAT_0300 = DAT_004a;
  if ((DAT_1001 & 0x40) == 0) {
    if ((TRCS & 2) != 0) {
      if (DAT_b903 <= DAT_007e) goto LAB_8ace;
      RX = RX & 0xfd;
      if (TX < 100) goto LAB_8b2a;
      goto LAB_8ae6;
    }
    if (DAT_b904 <= DAT_00a7) {
      RX = RX & 0xfd;
    }
    if (DAT_0093 == '\0') {
      if ((DAT_003e & 2) == 0) {
        if (0x3b < TX) {
          if (TX < DAT_bfcb) {
            DAT_003e = DAT_003e | 2;
            goto LAB_8b14;
          }
          bVar2 = DAT_bfb5;
          if ((TRCS & 1) != 0) goto LAB_8b2c;
        }
      }
      else {
LAB_8b14:
        if (TX < DAT_bfcc) {
          if (DAT_001d < 3) {
            uVar5 = DAT_001e;
            FUN_801a();
          }
          else {
            uVar5 = 0xff;
          }
          DAT_0052 = FUN_8000();
          bVar1 = DAT_bf1b;
          DAT_0053 = uVar5;
          cVar3 = FUN_802b();
          if (((cVar3 != '\0') || (bVar2 = DAT_bf1c + bVar1, CARRY1(DAT_bf1c,bVar1))) ||
             (199 < bVar2)) {
            bVar2 = 200;
          }
          else if (bVar2 < DAT_bf1e) {
            bVar2 = DAT_bf1e;
          }
          goto LAB_8b2c;
        }
        DAT_003e = DAT_003e & 0xfd;
      }
    }
  }
  else {
LAB_8ace:
    RX = RX | 2;
LAB_8ae6:
    DAT_0093 = '\x1e';
  }
LAB_8b2a:
  bVar2 = 200;
LAB_8b2c:
  DAT_1013 = (byte)(-bVar2 - 0x38) >> 1;
  _DAT_0100 = CONCAT11(0xb,DAT_1013);
  DAT_0200 = RX;
  FUN_8c8a();
  return;
}


// ---- FUN_8c24 @ 8c24 ----

void FUN_8c24(undefined1 param_1,undefined1 param_2,byte *param_3)

{
  byte bVar1;
  char cVar2;
  
  bVar1 = 0xaa;
  do {
    cVar2 = '\0';
    do {
      param_3[-1] = ~bVar1;
      param_3 = param_3 + -2;
      cVar2 = cVar2 + '\x02';
      *param_3 = bVar1;
    } while (cVar2 != '\0');
    DAT_0200 = 0x90;
    cVar2 = '\0';
    do {
      if ((bVar1 != *param_3) || ((byte)~bVar1 != param_3[1])) {
        P1DDR = 0xb0;
        goto LAB_8c1f;
      }
      param_3 = param_3 + 2;
      cVar2 = cVar2 + '\x02';
    } while (cVar2 != '\0');
    if (bVar1 == 0x55) {
      if (param_3 != &DAT_0100) {
        return;
      }
      P1DDR = 0xa0;
LAB_8c1f:
      FUN_8630();
      return;
    }
    bVar1 = ~bVar1;
  } while( true );
}


// ---- FUN_8c5d @ 8c5d ----

void FUN_8c5d(void)

{
  byte *pbVar1;
  
  pbVar1 = (byte *)0x7fff;
  DAT_0086 = 0;
  DAT_0087 = '\0';
  do {
    pbVar1 = pbVar1 + 1;
    DAT_0086 = DAT_0086 ^ *pbVar1;
    DAT_0087 = DAT_0087 + *pbVar1;
    DAT_00a6 = 0;
  } while (pbVar1 != (byte *)0xbfff);
  if ((DAT_0086 == DAT_bf7a) && (DAT_0087 == DAT_bf7b)) {
    P1DDR = P1DDR & 0xef;
  }
  else {
    P1DDR = P1DDR | 0x10;
  }
  return;
}


// ---- FUN_8c8a @ 8c8a ----

/* WARNING: Removing unreachable block (RAM,0x8fb5) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8c8a(void)

{
  bool bVar1;
  undefined2 uVar2;
  short sVar3;
  byte bVar4;
  byte bVar5;
  undefined1 uVar6;
  byte bVar7;
  char cVar8;
  byte *pbVar9;
  char *pcVar10;
  byte bStack0000;
  
  if (DAT_0048 == 0) {
    DAT_00a1 = DAT_00a1 | 0x80;
    if (DAT_00a1 < 0x94) goto LAB_8ce2;
LAB_8cd7:
    P2DDR = P2DDR | 0x80;
    DAT_1407 = 0;
  }
  else {
    DAT_00a1 = 0;
    if (0x2f < DAT_0048) {
      _DAT_0052 = _P3SCR;
      bVar4 = DAT_0092;
      FUN_802b();
      DAT_1008 = (char)(DAT_0054 >> 1 | bVar4 << 7) >> 1 | (bVar4 >> 1) << 7;
      bVar7 = DAT_1008;
      if (bVar4 >> 2 != 0) {
        bVar7 = 0xff;
      }
      if ((bVar7 < 0x50) || (0x80 < bVar7)) {
        DAT_00aa = DAT_00aa | 0x80;
        DAT_1000 = DAT_1000 | 0x80;
        if (0x89 < DAT_00aa) goto LAB_8cd7;
        goto LAB_8ced;
      }
    }
LAB_8ce2:
    DAT_00aa = 0;
    DAT_1000 = DAT_1000 & 0x7f;
  }
LAB_8ced:
  if ((TRCS & 2) == 0) {
    if ((TIMER < 3) || (0xf7 < TIMER)) {
      P3DDR = P3DDR | 0x40;
      DAT_1003 = DAT_1003 | 0x40;
      DAT_1417 = 0;
    }
    else {
      DAT_1003 = DAT_1003 & 0xbf;
    }
    if ((OUTCMP < 3) || (0xf7 < OUTCMP)) {
      P2DDR = P2DDR | 0x20;
      DAT_1000 = DAT_1000 | 0x20;
      DAT_1409 = 0;
    }
    else {
      DAT_1000 = DAT_1000 & 0xdf;
    }
    if ((DAT_1057 < 3) || (0xf0 < DAT_1057)) {
      P3DDR = P3DDR | 0x20;
      DAT_1003 = DAT_1003 | 0x20;
      DAT_1418 = 0;
    }
    else {
      DAT_1003 = DAT_1003 & 0xdf;
    }
    if ((((DAT_1000 & 0x20) == 0) && (DAT_b799 <= TX)) && (DAT_b79b <= DAT_1058)) {
      P2DATA = P2DATA | 8;
      DAT_1415 = 0;
    }
  }
  if ((((RX & 2) == 0) && ((DAT_0036 & 1) == 0)) && ((DAT_0048 != 0 && ((DAT_0200 & 4) != 0)))) {
    DAT_100f = DAT_100f | 0x80;
    if (DAT_100f == 0x85) {
      P1DATA = P1DATA | 0x40;
      DAT_1001 = DAT_1001 | 0x40;
      DAT_00fe = DAT_00fe | 4;
      DAT_140d = 0;
      goto LAB_8dc2;
    }
  }
  else {
LAB_8dc2:
    DAT_100f = 0;
  }
  if ((DAT_0048 < 0x30) || ((DAT_0079 & 1) == 0)) {
LAB_8de4:
    DAT_009c = 0;
  }
  else {
    DAT_009c = DAT_009c | 0x80;
    if (0xe3 < DAT_009c) {
      P2DDR = P2DDR | 0x40;
      DAT_1408 = 0;
      goto LAB_8de4;
    }
  }
  if ((0x2f < DAT_0048) && ((DAT_100a & 8) == 0)) {
    DAT_142a = DAT_142a + 1;
    DAT_100a = DAT_100a | 8;
  }
  if ((TRCS & 1) != 0) {
    DAT_142a = 0;
    DAT_100a = DAT_100a | 8;
  }
  if (4 < DAT_142a) {
    P1DATA = P1DATA | 0x20;
    DAT_140e = 0;
  }
  if (DAT_000c < 2) {
    if ((DAT_0020 < DAT_b79d) || (DAT_008c < DAT_b79e)) goto LAB_8e58;
    if ((DAT_100a & 0x10) == 0) {
      if (DAT_103f == 0) {
        DAT_103f = 1;
      }
      if (DAT_b79f <= DAT_103f) {
        DAT_142b = DAT_142b + 1;
        DAT_100a = DAT_100a | 0x10;
      }
    }
  }
  else {
    DAT_142b = 0;
LAB_8e58:
    DAT_103f = 0;
  }
  if (4 < DAT_142b) {
    P2DDR = P2DDR | 0x10;
    DAT_140a = 0;
    DAT_142b = 0;
  }
  if ((((((DAT_1000 & 0x60) == 0) && ((DAT_1003 & 0x20) == 0)) && (DAT_b78c <= DAT_007e)) &&
      ((DAT_b78d <= TX && (DAT_1042 < DAT_b794)))) && ((P2DATA & 8) == 0)) {
    if ((DAT_1009 & 4) == 0) {
      if ((DAT_1040 < DAT_b796) || (DAT_b797 <= DAT_1044)) goto LAB_8ef2;
      goto LAB_8ef9;
    }
    DAT_1044 = 0;
    if ((DAT_1040 < DAT_b792) || (DAT_1058 <= DAT_b795)) {
LAB_8edd:
      DAT_1041 = 0;
    }
    else if ((DAT_b793 <= DAT_1041) && ((DAT_1009 & 2) == 0)) {
      DAT_1009 = DAT_1009 | 2;
      DAT_1045 = DAT_1045 + 1;
      if (DAT_b798 <= DAT_1045) {
        P2DATA = P2DATA | 0x40;
        DAT_1412 = 0;
        DAT_1045 = 0;
        goto LAB_8edd;
      }
    }
  }
  else {
LAB_8ef2:
    DAT_1040 = 0;
    DAT_1044 = 0;
LAB_8ef9:
    DAT_1041 = 0;
    DAT_1009 = DAT_1009 & 0xfd;
  }
  if (((((P2DATA & 0x20) == 0) && ((P2DDR & 0x40) == 0)) && ((DAT_0032 & 0x20) != 0)) &&
     (((DAT_b7a0 <= DAT_008c && (DAT_008c < DAT_b7a1)) &&
      ((DAT_b7a2 <= DAT_0020 && (DAT_0020 < DAT_b7a3)))))) {
    if (DAT_b7a4 <= DAT_1046) {
      bVar4 = DAT_00cc + DAT_1047 + CARRY1(DAT_00cd,DAT_1048);
      bVar7 = (char)(DAT_00cd + DAT_1048) >> 1 | bVar4 * -0x80;
      bVar4 = (bVar4 >> 1) + DAT_1047 + CARRY1(bVar7,DAT_1048);
      DAT_1047 = bVar4 >> 1;
      DAT_1048 = (char)(bVar7 + DAT_1048) >> 1 | bVar4 * -0x80;
    }
  }
  else {
    DAT_1009 = DAT_1009 & 0xef;
    DAT_1046 = 0;
  }
  if ((((DAT_1047 < DAT_b7a5) &&
       (bVar4 = (DAT_1047 - DAT_1405) - (DAT_1048 < DAT_1406),
       DAT_1405 <= DAT_1047 && (DAT_1048 < DAT_1406) <= (byte)(DAT_1047 - DAT_1405))) &&
      (DAT_1049 = bVar4, DAT_b7a6 <= bVar4)) ||
     (((DAT_100b & 0x10) != 0 && ((DAT_1047 < DAT_b7a7 || ((DAT_100b & 0x20) != 0)))))) {
    P3DDR = P3DDR | 8;
    DAT_1419 = 0;
  }
  bStack0000 = 0;
  if ((TRCS & 2) == 0) {
    DAT_00fd = DAT_00fd & 0xfb;
  }
  else if ((DAT_00fd & 4) == 0) {
    DAT_00fd = DAT_00fd | 4;
    bVar4 = 0;
    do {
      pbVar9 = &DAT_b90b;
      bVar7 = FUN_9014();
      if ((bVar7 & *pbVar9) != 0) {
        pbVar9 = &DAT_1407;
        bVar5 = bVar7;
        do {
          bVar1 = (bool)(bVar5 >> 7);
          bVar5 = bVar5 << 1;
        } while (!bVar1);
        bStack0000 = bVar4;
        FUN_9014();
        *pbVar9 = *pbVar9 + 1;
        bVar4 = bStack0000;
        if (0x31 < *pbVar9) {
          *pbVar9 = 0;
          pbVar9 = &P2DDR;
          bVar7 = FUN_9014();
          *pbVar9 = ~bVar7 & *pbVar9;
          bVar4 = bStack0000;
          bStack0000 = bVar7;
        }
      }
    } while ((7 < bVar7 >> 1) || (bVar4 = bVar4 + 1, bVar4 < 5));
  }
  _DAT_006b = &DAT_1500;
  _DAT_006d = &DAT_bbb0;
  _DAT_006f = &DAT_bba0;
  _DAT_005e = _P3SCR;
  uVar2 = _DAT_005e;
  _DAT_0060 = _DAT_0020;
  sVar3 = _DAT_0060;
  pcVar10 = (char *)&DAT_bba0;
  cVar8 = '\x0f';
  DAT_0060 = (byte)((ushort)_DAT_0020 >> 8);
  do {
    if (DAT_0060 < (byte)pcVar10[1]) break;
    pcVar10 = pcVar10 + 1;
    cVar8 = cVar8 + -1;
  } while (cVar8 != '\0');
  DAT_0071 = '\x0f' - cVar8;
  DAT_0069 = *pcVar10;
  DAT_006a = pcVar10[1];
  bVar4 = DAT_bba0;
  if ((DAT_0060 < DAT_bba0) ||
     (bVar1 = DAT_bbaf <= DAT_0060, bVar4 = DAT_bbaf, _DAT_0060 = sVar3, bVar1)) {
    _DAT_0060 = (ushort)bVar4 << 8;
  }
  pbVar9 = &DAT_bbb0;
  DAT_005f = (byte)_P3SCR;
  bVar4 = DAT_005f;
  _DAT_005e = uVar2;
  FUN_801a();
  cVar8 = '\x0f';
  do {
    if (bVar4 < pbVar9[1]) break;
    pbVar9 = pbVar9 + 1;
    cVar8 = cVar8 + -1;
  } while (cVar8 != '\0');
  cVar8 = '\x10';
  FUN_8000();
  DAT_0071 = cVar8 + DAT_0071;
  DAT_0067 = *pbVar9;
  DAT_0068 = pbVar9[1];
  bVar4 = DAT_005f;
  pbVar9 = _DAT_006d;
  FUN_801a();
  if (bVar4 < *pbVar9) {
    bVar4 = *pbVar9;
LAB_90ab:
    uVar6 = FUN_8025(0);
    _DAT_005e = CONCAT11(uVar6,bVar4);
  }
  else if (pbVar9[0xf] <= bVar4) {
    bVar4 = pbVar9[0xf];
    goto LAB_90ab;
  }
  cVar8 = (DAT_006b - (DAT_0071 >> 7)) + CARRY1(DAT_0071 * '\x02',DAT_006c);
  _DAT_006b = (byte *)CONCAT11(cVar8,DAT_0071 * '\x02' + DAT_006c);
  DAT_0062 = DAT_0060 - DAT_0069;
  DAT_0063 = DAT_0061;
  DAT_0064 = '\0';
  DAT_0065 = DAT_006a - DAT_0069;
  DAT_0066 = 0;
  pbVar9 = _DAT_006b;
  FUN_8386();
  bVar4 = pbVar9[3] - pbVar9[1];
  DAT_00ce = cVar8;
  if ((pbVar9[2] < *pbVar9 || (byte)(pbVar9[2] - *pbVar9) < (pbVar9[3] < pbVar9[1])) &&
     (bVar4 = -bVar4, DAT_0064 != '\0')) {
    DAT_0064 = -DAT_0064;
    cVar8 = FUN_91ae();
    DAT_00c9 = bVar4 + pbVar9[3];
    DAT_00c8 = cVar8 + pbVar9[2] + CARRY1(bVar4,pbVar9[3]);
  }
  else {
    cVar8 = FUN_91ae();
    DAT_00c9 = bVar4 + pbVar9[1];
    DAT_00c8 = cVar8 + *pbVar9 + CARRY1(bVar4,pbVar9[1]);
  }
  DAT_0064 = DAT_00ce;
  bVar4 = pbVar9[0x23] - pbVar9[0x21];
  if ((pbVar9[0x22] < pbVar9[0x20] ||
       (byte)(pbVar9[0x22] - pbVar9[0x20]) < (pbVar9[0x23] < pbVar9[0x21])) &&
     (bVar4 = -bVar4, DAT_00ce != '\0')) {
    DAT_0064 = -DAT_00ce;
    cVar8 = FUN_91ae();
    DAT_00cb = bVar4 + pbVar9[0x23];
    DAT_00ca = cVar8 + pbVar9[0x22] + CARRY1(bVar4,pbVar9[0x23]);
  }
  else {
    cVar8 = FUN_91ae();
    DAT_00cb = bVar4 + pbVar9[0x21];
    DAT_00ca = cVar8 + pbVar9[0x20] + CARRY1(bVar4,pbVar9[0x21]);
  }
  bVar7 = DAT_0067;
  cVar8 = FUN_8025(0);
  bVar5 = (DAT_005e - cVar8) - (DAT_005f < bVar7);
  bVar4 = (char)(DAT_005f - bVar7) >> 1;
  DAT_0062 = bVar5 >> 2;
  bVar5 = (char)(bVar4 | bVar5 * -0x80) >> 1 | (bVar5 >> 1) << 7;
  DAT_0064 = (char)((DAT_005f - bVar7) * -0x80) >> 1 | bVar4 << 7;
  DAT_0066 = DAT_0068 - DAT_0067;
  DAT_0065 = 0;
  DAT_0063 = bVar5;
  FUN_8386();
  bVar4 = DAT_00cb - DAT_00c9;
  DAT_00cf = bVar5;
  if ((DAT_00ca < DAT_00c8 || (byte)(DAT_00ca - DAT_00c8) < (DAT_00cb < DAT_00c9)) &&
     (bVar4 = -bVar4, DAT_0064 != 0)) {
    DAT_0064 = -DAT_0064;
    cVar8 = FUN_91ae();
    DAT_00cd = bVar4 + DAT_00cb;
    DAT_00cc = cVar8 + DAT_00ca + CARRY1(bVar4,DAT_00cb);
  }
  else {
    cVar8 = FUN_91ae();
    DAT_00cd = bVar4 + DAT_00c9;
    DAT_00cc = cVar8 + DAT_00c8 + CARRY1(bVar4,DAT_00c9);
  }
  if (DAT_00cc < 0x7d) {
    if (0x4a < DAT_00cc) goto LAB_919b;
    DAT_00cc = 0x4b;
  }
  else {
    DAT_00cc = 0x7d;
  }
  DAT_00cd = '\0';
LAB_919b:
  DAT_00b1 = DAT_00ce;
  DAT_00bc = DAT_00cf;
  _DAT_00ba = pbVar9;
  FUN_863d();
  return;
}


// ---- FUN_9014 @ 9014 ----

void FUN_9014(undefined1 param_1,char param_2)

{
  for (; param_2 != '\0'; param_2 = param_2 + -1) {
  }
  return;
}


// ---- FUN_91ae @ 91ae ----

char FUN_91ae(byte param_1,char param_2)

{
  char cVar1;
  byte bVar2;
  
  DAT_00c6 = param_1;
  DAT_00c7 = FUN_8000();
  if (param_2 < '\0') {
    DAT_00c7 = DAT_00c7 + 1;
  }
  bVar2 = DAT_00c6;
  cVar1 = FUN_8000(DAT_0064,DAT_00c6);
  return cVar1 + CARRY1(bVar2,DAT_00c7);
}


// ---- FUN_953a @ 953a ----

undefined1 FUN_953a(undefined1 param_1)

{
  DAT_0100 = 0x14;
  DAT_0101 = param_1;
  FUN_9553();
  FUN_9553();
  DAT_0100 = 0x16;
  return DAT_0101;
}


// ---- FUN_9553 @ 9553 ----

void FUN_9553(void)

{
  return;
}


// ---- FUN_9557 @ 9557 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9557(void)

{
  if ((DAT_0036 & 8) != 0) {
    if (_P3SCR == 0) {
      DAT_1010 = 0;
    }
    DAT_0038 = DAT_0038 + 1;
    if ((99 < DAT_0038) && (DAT_00a1 = 0, 0x95 < DAT_0038)) {
      _DAT_0100 = 0x600;
      if ((DAT_0036 & 1) == 0) {
        P3DATA = P3DATA & 0xf0;
      }
      FUN_8630();
      return;
    }
  }
  FUN_9655();
  return;
}


// ---- FUN_9593 @ 9593 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9593(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  char cStack0000;
  
  if ((TRCS & 2) == 0) {
    if ((((IMPCAP != '\0') || (7 < DAT_000e)) || (_IMPCAP = 8, (DAT_0036 & 8) == 0)) ||
       (DAT_0048 == 0)) goto LAB_95bc;
    DAT_0079 = DAT_0079 | 1;
  }
  else {
LAB_95bc:
    DAT_0079 = DAT_0079 & 0xfe;
  }
  if ((0x1f < DAT_0048) && ((DAT_0036 & 8) != 0)) {
    if ((DAT_0079 & 1) == 0) {
      bVar2 = DAT_102d - DAT_000e;
      bVar1 = (DAT_102c - IMPCAP) - (DAT_102d < DAT_000e);
      if (DAT_102c < IMPCAP || (byte)(DAT_102c - IMPCAP) < (DAT_102d < DAT_000e)) {
        bVar3 = ~bVar2;
        bVar2 = bVar3 + 1;
        bVar1 = ~bVar1 + (0xfe < bVar3);
      }
      if ((byte)((char)bVar2 >> 1 | bVar1 << 7) < 0x18) goto LAB_95f4;
    }
    DAT_00fe = DAT_00fe | 2;
  }
LAB_95f4:
  _DAT_102c = _IMPCAP;
  bVar1 = DAT_000e - 8;
  cStack0000 = IMPCAP - (DAT_000e < 8);
  if (IMPCAP < (DAT_000e < 8)) {
    cStack0000 = '\0';
    bVar1 = 0;
  }
  FUN_8021(cStack0000);
  DAT_1015 = FUN_8116();
  _DAT_1017 = _DAT_007a;
  bVar2 = DAT_bee6 >> 1;
  DAT_1016 = bVar1;
  do {
    bVar1 = DAT_1015;
    DAT_1015 = DAT_1015 >> 1;
    DAT_1016 = (char)DAT_1016 >> 1 | bVar1 << 7;
    bVar1 = DAT_1017;
    DAT_1017 = DAT_1017 >> 1;
    DAT_1018 = (char)DAT_1018 >> 1 | bVar1 << 7;
    bVar2 = bVar2 >> 1;
  } while (bVar2 != 0);
  DAT_0073 = (DAT_007b - DAT_1018) + DAT_1016;
  DAT_0072 = ((DAT_007a - DAT_1017) - (DAT_007b < DAT_1018)) + DAT_1015 +
             CARRY1(DAT_007b - DAT_1018,DAT_1016);
  _DAT_007a = CONCAT11(DAT_0072,DAT_0073);
  FUN_941a();
  return;
}


// ---- FUN_9655 @ 9655 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9655(void)

{
  char cVar1;
  char cVar2;
  char cVar3;
  char cVar4;
  byte bVar5;
  byte bVar6;
  byte bVar7;
  char cVar8;
  bool bVar9;
  
  DAT_00a6 = DAT_00a6 + 1;
  if (DAT_008c < 0x50) {
    if (DAT_00a6 < 0x15) goto LAB_9669;
  }
  else {
    DAT_00a6 = 0;
LAB_9669:
    RX = RX ^ 1;
    DAT_0200 = RX;
  }
  DAT_0100 = 0xd;
  _DAT_104e = _DAT_104c;
  _DAT_104c = _P3SCR;
  _P3SCR = CONCAT11(DAT_0101,DAT_0101);
  DAT_0048 = 0;
  if (DAT_0101 != 0) {
    DAT_0048 = 0xff;
  }
  bVar6 = DAT_0101;
  FUN_801a();
  bVar7 = RMCR;
  DAT_008c = bVar6;
  bVar5 = FUN_8023();
  _DAT_1024 = _DAT_0080;
  bVar6 = DAT_bf05;
  DAT_1022 = bVar5;
  DAT_1023 = bVar7;
  if (DAT_bf05 == 0) {
    if ((TRCS & 1) != 0) {
      bVar6 = 8;
      goto LAB_96c7;
    }
  }
  else {
LAB_96c7:
    bVar6 = bVar6 >> 1;
    do {
      bVar7 = DAT_1022;
      DAT_1022 = DAT_1022 >> 1;
      DAT_1023 = (char)DAT_1023 >> 1 | bVar7 << 7;
      bVar7 = DAT_1024;
      DAT_1024 = DAT_1024 >> 1;
      DAT_1025 = (char)DAT_1025 >> 1 | bVar7 << 7;
      bVar6 = bVar6 >> 1;
    } while (bVar6 != 0);
    bVar7 = (DAT_0081 - DAT_1025) + DAT_1023;
    bVar5 = ((DAT_0080 - DAT_1024) - (DAT_0081 < DAT_1025)) + DAT_1022 +
            CARRY1(DAT_0081 - DAT_1025,DAT_1023);
  }
  _DAT_0080 = CONCAT11(bVar5,bVar7);
  if ((TRCS & 2) == 0) {
    if ((DAT_102a != 0) || (0x1f < DAT_102b)) {
      bVar6 = (DAT_102a << 1 | DAT_102b >> 7) + DAT_102a + CARRY1(DAT_102b * '\x02',DAT_102b);
      bVar7 = bVar6 >> 1;
      if ((bVar7 < P3SCR ||
           (byte)(bVar7 - P3SCR) < ((byte)((char)(DAT_102b * '\x03') >> 1 | bVar6 * -0x80) < RMCR))
         || (P3SCR <= DAT_102a >> 1 &&
             ((byte)((char)DAT_102b >> 1 | DAT_102a << 7) < RMCR) <= (byte)((DAT_102a >> 1) - P3SCR)
            )) {
        DAT_00fe = DAT_00fe | 8;
      }
    }
  }
  _DAT_102a = _P3SCR;
  if ((DAT_00b7 & 1) == 0) {
    if (0x4f < DAT_0048) {
      DAT_00b7 = DAT_00b7 | 1;
    }
  }
  else if (DAT_0048 < 0x10) {
    DAT_00b7 = DAT_00b7 & 0xfe;
  }
  if ((DAT_0200 & 0x10) == 0) {
    DAT_0036 = DAT_0036 | 1;
  }
  else {
    DAT_0036 = DAT_0036 & 0xfe;
  }
  TRCS = DAT_0200 & 3;
  if ((DAT_0200 & 0x40) != 0) {
    TRCS = TRCS | 0x10;
  }
  if ((DAT_0200 & 0x80) == 0) {
    TRCS = TRCS | 4;
  }
  if ((char)DAT_bee0 < '\0') {
    TRCS = TRCS | 0x40;
  }
  if ((DAT_00b7 & 1) != 0) {
    TRCS = TRCS & 0xfd;
  }
  DAT_0100 = 0xf;
  DAT_000c = DAT_0101;
  bVar6 = DAT_bf2a;
  FUN_8000();
  bVar7 = FUN_8018();
  if ((P3SCR <= bVar7) && (((bVar7 != P3SCR || (RMCR <= bVar6)) && ((TRCS & 4) == 0)))) {
    TRCS = TRCS | 8;
  }
  bVar6 = DAT_b902;
  FUN_8000();
  bVar7 = FUN_8018();
  cVar2 = DAT_1021;
  cVar8 = DAT_1020;
  if (((P3SCR <= bVar7) && ((bVar7 != P3SCR || (RMCR <= bVar6)))) && ((TRCS & 4) == 0)) {
    TRCS = TRCS | 0x80;
  }
  if (((DAT_000c < 0x7d) || ((DAT_0200 & 2) == 0)) || ((DAT_0200 & 1) == 0)) {
LAB_97e3:
    DAT_1033 = 0;
  }
  else {
    DAT_1033 = DAT_1033 + 1;
    if (99 < DAT_1033) {
      P1DDR = P1DDR | 0x20;
      goto LAB_97e3;
    }
  }
  if (DAT_00c3 != '\0') {
    DAT_00c3 = DAT_00c3 + -1;
  }
  if (DAT_0022 != '\0') {
    bVar9 = DAT_0023 < DAT_bfc6;
    DAT_0023 = DAT_0023 - DAT_bfc6;
    DAT_0022 = DAT_0022 - bVar9;
  }
  if (DAT_00a3 != '\0') {
    DAT_00a3 = DAT_00a3 + -1;
  }
  if ((DAT_009c < '\0') && (DAT_009c = DAT_009c + '\x01', DAT_009c == '\0')) {
    DAT_009c = -1;
  }
  if ((TRCS & 1) == 0) {
    DAT_1020 = '\0';
    DAT_1021 = DAT_1021 + '\x01';
    if (DAT_1021 == '\0') {
      DAT_1021 = cVar2;
    }
  }
  else {
    DAT_1021 = '\0';
    DAT_1020 = DAT_1020 + '\x01';
    if (DAT_1020 == '\0') {
      DAT_1020 = cVar8;
    }
  }
  FUN_9c01();
  cVar4 = DAT_1046;
  cVar3 = DAT_1044;
  cVar2 = DAT_1041;
  cVar8 = DAT_1040;
  if (DAT_0016 == 0) {
    if (DAT_00b4 != '\0') {
      DAT_00b4 = DAT_00b4 + -1;
    }
    if (DAT_0093 != '\0') {
      DAT_0093 = DAT_0093 + -1;
    }
    DAT_002c = DAT_002c + '\x01';
    if (DAT_002c == '\0') {
      DAT_002c = -1;
    }
    DAT_00a7 = DAT_00a7 + '\x01';
    if (DAT_00a7 == '\0') {
      DAT_00a7 = -1;
    }
    if ((DAT_002f < '\0') && (DAT_002f = DAT_002f + '\x01', DAT_002f == '\0')) {
      DAT_002f = -1;
    }
    if ((DAT_0084 < '\0') && (DAT_0084 = DAT_0084 + '\x01', DAT_0084 == '\0')) {
      DAT_0084 = -1;
    }
    if ((DAT_009f < '\0') && (DAT_009f = DAT_009f + '\x01', DAT_009f == '\0')) {
      DAT_009f = -1;
    }
    if ((DAT_103f != '\0') && (DAT_103f = DAT_103f + '\x01', DAT_103f == '\0')) {
      DAT_103f = -1;
    }
    DAT_100d = DAT_100d + '\x01';
    if (DAT_100d == '\0') {
      DAT_100d = -1;
    }
    if ((0x38 < DAT_101b) && (DAT_101c = DAT_101c + 1, 2 < DAT_101c)) {
      DAT_101c = 0;
      DAT_101b = DAT_101b - 1;
    }
    if (TX < 0x41) {
      bVar9 = DAT_0025 < DAT_bfc4;
      cVar1 = -DAT_bfc4;
    }
    else {
      bVar9 = DAT_0025 < 0x14;
      cVar1 = -0x14;
    }
    DAT_0025 = DAT_0025 + cVar1;
    if (bVar9) {
      DAT_0025 = 0;
    }
    if ((DAT_1009 & 4) == 0) {
      DAT_1044 = DAT_1044 + '\x01';
      DAT_1041 = cVar2;
      if (DAT_1044 == '\0') {
        DAT_1044 = cVar3;
      }
    }
    else {
      DAT_1041 = DAT_1041 + '\x01';
      DAT_1044 = cVar3;
      if (DAT_1041 == '\0') {
        DAT_1041 = cVar2;
      }
    }
    DAT_1040 = cVar8;
    if (((DAT_1009 & 4) != 0) && (DAT_1040 = DAT_1040 + '\x01', DAT_1040 == '\0')) {
      DAT_1040 = cVar8;
    }
LAB_98e3:
    DAT_009e = DAT_0083 - RMCR;
    _DAT_0082 = _P3SCR;
    DAT_007f = DAT_007f + '\x01';
    if (DAT_007f == '\0') {
      DAT_007f = -1;
    }
    DAT_00ab = DAT_00ab + '\x01';
    if (DAT_00ab == '\0') {
      DAT_00ab = -1;
    }
    if ((DAT_00b3 < '\0') && (DAT_00b3 = DAT_00b3 + '\x01', DAT_00b3 == '\0')) {
      DAT_00b3 = -1;
    }
    if (DAT_003f != '\0') {
      DAT_003f = DAT_003f + -1;
    }
    if (((DAT_100a & 1) != 0) && (DAT_103e = DAT_103e + '\x01', DAT_103e == '\0')) {
      DAT_103e = -1;
    }
    DAT_1046 = DAT_1046 + '\x01';
    if (DAT_1046 == '\0') {
      DAT_1046 = cVar4;
    }
    DAT_003d = DAT_003d + '\x01';
    if (DAT_003d == '\0') {
      DAT_003d = -1;
    }
    if (DAT_003c != '\0') {
      DAT_003c = DAT_003c + -1;
    }
    if ((DAT_100f < '\0') && (DAT_100f = DAT_100f + '\x01', DAT_100f == '\0')) {
      DAT_100f = -1;
    }
    if ((DAT_00a1 < '\0') && (DAT_00a1 = DAT_00a1 + '\x01', DAT_00a1 == '\0')) {
      DAT_00a1 = -1;
    }
    if ((DAT_00aa < '\0') && (DAT_00aa = DAT_00aa + '\x01', DAT_00aa == '\0')) {
      DAT_00aa = -1;
    }
    if ((OUTCMP < 3) || (0xf7 < OUTCMP)) {
LAB_996f:
      TX = FUN_80dd();
      if (DAT_007e == 0) {
        DAT_007e = TX;
      }
      bVar6 = TX - 10;
      if (TX < 10) {
        bVar6 = 0;
      }
      else if (0x9f < bVar6) {
        bVar6 = 0x9f;
      }
      bVar7 = 0xcd;
      cVar8 = FUN_8000(bVar6);
      DAT_008a = (cVar8 << 1 | bVar7 >> 7) + (0x7f < (byte)(bVar7 << 1));
      if (DAT_1038 == '\0') {
        DAT_1038 = DAT_008a;
        DAT_1037 = FUN_80d2();
        DAT_100e = FUN_80d2();
      }
    }
    else if (OUTCMP != DAT_00bd) {
      DAT_00bd = OUTCMP;
      goto LAB_996f;
    }
    if ((DAT_0036 & 1) == 0) {
      DAT_00a5 = 0;
      RX = RX & 0xbf | 0x80;
    }
    else {
      DAT_00a5 = DAT_00a5 + 1;
      if (DAT_00a5 < 0x3c) {
        if ((0x31 < DAT_00a5) && (P3DATA == 0xf)) {
          RX = RX | 0x40;
        }
      }
      else {
        RX = RX & 0x3f;
      }
    }
    _DAT_008f = CONCAT11(DAT_008f + (0xe5 < DAT_0090),DAT_0090 + 0x1a);
    if (((P3DATA & 8) == 0) && (0x77 < DAT_0048)) {
      P3DATA = P3DATA | 10;
    }
    if (((P3DATA & 4) == 0) && (((DAT_bee0 & 1) != 0 || (9 < DAT_000c)))) {
      P3DATA = P3DATA | 4;
    }
    if ((DAT_0036 & 8) != 0) {
      P3DATA = P3DATA | 3;
    }
    if (0xa4 < TX) {
      P3DATA = P3DATA & 0xfe;
    }
  }
  else {
    DAT_1040 = cVar8;
    if ((DAT_0016 & 0xf) == 0) goto LAB_98e3;
  }
  DAT_104a = DAT_0041;
  bVar6 = DAT_0095 & 0xe7;
  if ((DAT_0095 & 0x20) != 0) {
    bVar6 = bVar6 | 0x10;
  }
  DAT_0095 = bVar6;
  if ((bVar6 & 0x80) == 0) {
    if (((((((TRCS & 4) == 0) && (DAT_b7e9 <= TX)) && (TX <= DAT_b7ea)) &&
         ((DAT_000c < DAT_b7eb && (DAT_0020 < DAT_b7ec)))) &&
        ((-1 < (char)DAT_007d && ((DAT_b7e4 <= DAT_007d && (DAT_b7e7 <= DAT_008c)))))) &&
       (DAT_008c <= DAT_b7e8)) {
      DAT_0095 = bVar6 | 0x80;
    }
LAB_9a91:
    DAT_0095 = DAT_0095 | 8;
  }
  else {
    DAT_104b = DAT_104b + 1;
    if (DAT_104b <= DAT_b7e5) goto LAB_9a91;
    if (DAT_b7e6 < DAT_104b) {
      DAT_104b = 0;
      DAT_0095 = bVar6 & 0x3f;
      goto LAB_9a91;
    }
  }
  bVar6 = RMCR - DAT_104f;
  cVar8 = (P3SCR - DAT_104e) - (RMCR < DAT_104f);
  _DAT_1050 = CONCAT11(cVar8,bVar6);
  if (P3SCR < DAT_104e || (byte)(P3SCR - DAT_104e) < (RMCR < DAT_104f)) {
    bVar7 = DAT_0095 | 0x20;
    if (((DAT_0095 & 8) == 0) && ((DAT_0095 & 0x40) != 0)) {
      bVar5 = -bVar6;
      if ((bool)-cVar8 != (bVar6 != 0)) {
        bVar5 = 0xff;
      }
      DAT_0095 = bVar7;
      FUN_8000();
      cVar8 = FUN_801a();
      if ((cVar8 != '\0') || (DAT_b7e2 <= bVar5)) {
        bVar5 = DAT_b7e2;
      }
      DAT_104a = bVar5 + DAT_104a;
      bVar7 = DAT_0095;
    }
  }
  else {
    if (_DAT_1050 != 0) {
      DAT_0095 = DAT_0095 & 0xdf;
    }
    bVar7 = DAT_0095;
    if ((DAT_0095 & 8) == 0) {
      if ((DAT_0095 & 0x40) == 0) {
        if ((DAT_0095 & 0x10) == 0) goto LAB_9b22;
        DAT_0095 = DAT_0095 | 0x40;
      }
      if (cVar8 != '\0') {
        bVar6 = 0xff;
      }
      FUN_8000();
      cVar8 = FUN_801a();
      if ((cVar8 != '\0') || (DAT_b7e3 <= bVar6)) {
        bVar6 = DAT_b7e3;
      }
      DAT_104a = DAT_104a - bVar6;
      bVar7 = DAT_0095;
    }
  }
LAB_9b22:
  DAT_0095 = bVar7;
  cVar8 = DAT_008e;
  bVar6 = TX;
  if ((DAT_0089 & 0x40) != 0) {
    bVar6 = TX + 4;
  }
  if (bVar6 < 0x7d) {
    _DAT_00c1 = 0;
    DAT_0089 = DAT_0089 & 0xbf;
  }
  else {
    DAT_0089 = DAT_0089 | 0x40;
  }
  if ((DAT_bfd3 & 8) != 0) {
    if ((DAT_0075 & 8) == 0) {
      if ((DAT_0089 & 0x20) != 0) {
        _DAT_00c1 = _DAT_008f;
        DAT_0089 = DAT_0089 & 0xdf;
      }
    }
    else if ((DAT_0089 & 0x20) == 0) {
      DAT_0089 = DAT_0089 | 0x20;
      _DAT_008f = _DAT_00c1;
    }
  }
  DAT_008e = 0;
  if ((DAT_008d & 4) == 0) {
    _DAT_008f = (ushort)DAT_bfc5 << 8;
    P2DATA = P2DATA | 0x10;
    DAT_1414 = 0;
  }
  else {
    for (; cVar8 != '\0'; cVar8 = cVar8 + -1) {
      _DAT_008f = CONCAT11((DAT_008f - DAT_bfb8) - (DAT_0090 < DAT_bfb9),DAT_0090 - DAT_bfb9);
    }
  }
  if (_DAT_008f < 0) {
    bVar6 = -DAT_0088;
    if ((byte)(bVar6 - DAT_008f) != 0 &&
        (short)((ushort)(byte)(bVar6 - DAT_008f) << 8) < 0 == SBORROW1(bVar6,DAT_008f)) {
      _DAT_008f = (ushort)bVar6 << 8;
    }
  }
  else if (DAT_008b <= DAT_008f) {
    _DAT_008f = (ushort)DAT_008b << 8;
  }
  cVar8 = (DAT_104a - DAT_00bf) + DAT_008f;
  DAT_0017 = 0x46 - cVar8;
  if ('F' < cVar8) {
    DAT_0017 = 0;
  }
  bVar6 = DAT_0018 - DAT_bf8e;
  if (DAT_0018 < DAT_bf8e) {
    bVar6 = 0;
  }
  if (bVar6 <= DAT_0017) {
    if (((TRCS & 2) != 0) || (cVar8 = DAT_bf26, (DAT_003e & 0x40) == 0)) {
      cVar8 = '\n';
    }
    bVar6 = cVar8 + DAT_0018;
    if (DAT_0017 < (byte)(cVar8 + DAT_0018)) goto LAB_9be9;
  }
  DAT_0017 = bVar6;
LAB_9be9:
  if (0x77 < DAT_0017) {
    DAT_0017 = 0x77;
  }
  DAT_001f = DAT_001f | 0x80;
  DAT_1031 = DAT_008f + -0x80;
  FUN_a5de();
  return;
}


// ---- FUN_9c01 @ 9c01 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9c01(void)

{
  bool bVar1;
  byte bVar2;
  byte bVar3;
  
  DAT_1425 = P2DDR & DAT_b90b;
  DAT_1426 = P1DATA & DAT_b90c;
  _P2DDR = CONCAT11(DAT_1425,DAT_1426);
  DAT_1427 = P2DATA & DAT_b90d;
  DAT_1428 = P3DDR & DAT_b90e;
  _P2DATA = CONCAT11(DAT_1427,DAT_1428);
  DAT_1429 = P4DDR & DAT_b90f;
  P4DDR = DAT_1429;
  if ((P1DDR & 0x20) == 0) {
    if ((DAT_00fd & 8) == 0) {
      if (TCSR < 0xe0) {
        DAT_102f = 0;
        if ((DAT_00fd & 0x40) == 0) {
          if ((DAT_00fd & 0x20) != 0) {
            DAT_1027 = P1DDR;
            if ((TRCS & 3) != DAT_1420) {
              DAT_00a2 = DAT_00a2 ^ 0x10;
              DAT_1420 = TRCS & 3;
            }
            if (((TRCS & 2) != 0) || (DAT_000c < 10)) {
              DAT_00a2 = DAT_00a2 & 0xf7;
              DAT_0100 = 0x19;
              DAT_0101 = DAT_00a2;
              DAT_1027 = P1DDR;
              DAT_102f = 0;
              return;
            }
            goto LAB_9e4c;
          }
          if ((DAT_00fd & 0x10) != 0) {
            if ((DAT_0016 & 0x1f) != 0) {
              DAT_102f = 0;
              return;
            }
            bVar3 = DAT_00fe;
            if (((DAT_00fe & 8) != 0) && (bVar3 = DAT_00fe & 0x6e, (DAT_00fe & 0x40) == 0)) {
              if (DAT_1421 == 0) {
                DAT_1423 = 0xff;
              }
              if (DAT_1421 < 0x30) {
                DAT_00fe = DAT_00fe & 0x6e;
                FUN_9f5e();
                goto LAB_9f01;
              }
              DAT_1421 = 0;
              bVar3 = DAT_00fe & 0x66;
            }
            DAT_00fe = bVar3;
            if ((DAT_00fe & 4) != 0) {
              if (DAT_1421 == 0) {
                DAT_1423 = 0xdb;
              }
              if (DAT_1421 < 0x30) {
                DAT_00fe = DAT_00fe & 0x7f | 0x40;
                FUN_9f5e();
              }
              else {
                DAT_00fe = DAT_00fe & 0x3b;
                DAT_1421 = 0;
              }
            }
LAB_9f01:
            if (((DAT_00fe & 0x10) == 0) && ((DAT_00fe & 2) != 0)) {
              if (DAT_1422 == 0) {
                DAT_1424 = 0xe7;
              }
              if (DAT_1422 < 0x30) {
                DAT_00fe = DAT_00fe | 0x80;
                FUN_9f5e();
                DAT_0100 = 0x19;
                DAT_0101 = DAT_00a2;
                return;
              }
              DAT_00fe = DAT_00fe & 0xfd | 0x80;
              DAT_1422 = 0;
            }
            if ((DAT_00fe & 1) != 0) {
              DAT_00fe = DAT_00fe | 0x90;
              if (DAT_1422 == 0) {
                DAT_1424 = 0xaa;
              }
              if (DAT_1422 < 0x30) {
                FUN_9f5e();
                DAT_0100 = 0x19;
                DAT_0101 = DAT_00a2;
                return;
              }
            }
            DAT_00a2 = DAT_00a2 & 0xf7;
            DAT_00fe = DAT_00fe & 0xee;
            DAT_0100 = 0x19;
            DAT_0101 = DAT_00a2;
            DAT_1422 = 0;
            return;
          }
          if ((DAT_0032 & 0x20) == 0) {
            DAT_00a2 = DAT_00a2 & 0xe7;
          }
          else {
            if ((DAT_0032 & 8) == 0) {
              DAT_00a2 = DAT_00a2 | 0x18;
            }
            else {
              DAT_00a2 = DAT_00a2 & 0xe7;
            }
            if (DAT_0030 < 0x6a) {
              if (DAT_0030 < 0x5f) {
                DAT_00a2 = DAT_00a2 & 0xef;
              }
            }
            else {
              DAT_00a2 = DAT_00a2 | 0x10;
            }
          }
          if ((DAT_00fd & 0x80) != 0) {
            if ((DAT_0036 & 8) != 0) {
              DAT_0100 = 0x19;
              DAT_0101 = DAT_00a2;
              DAT_102f = 0;
              return;
            }
LAB_9e52:
            DAT_00a2 = DAT_00a2 & 0xef;
            DAT_0100 = 0x19;
            DAT_0101 = DAT_00a2;
            return;
          }
          if ((DAT_0036 & 8) == 0) {
            DAT_0100 = 0x19;
            DAT_0101 = DAT_00a2;
            DAT_102f = 0;
            return;
          }
          if (((((DAT_1425 & 0x50) == 0) && ((DAT_1426 & 0x20) == 0)) && ((DAT_1427 & 0xe0) == 0))
             && ((DAT_1428 & 8) == 0)) goto LAB_9e52;
          goto LAB_9e46;
        }
        DAT_0044 = DAT_0044 + '\x01';
        if (DAT_0044 < '\0') {
          DAT_0044 = -0x80;
        }
        DAT_00a0 = DAT_00a0 + 1;
        if (DAT_00a0 < 0x1e) {
          DAT_102f = 0;
          return;
        }
        goto LAB_9e14;
      }
      if (((DAT_0016 & 0xf) != 0) || (DAT_102f = DAT_102f + 1, DAT_102f < 10)) goto LAB_9e64;
      DAT_102f = 0;
      bVar3 = DAT_00fd | 8;
      if ((DAT_00fd & 0x80) == 0) {
        if ((DAT_00fd & 0x40) == 0) {
          if ((DAT_00fd & 0x20) == 0) {
            if ((DAT_00fd & 0x10) == 0) {
              DAT_00fd = DAT_00fd | 0x88;
              DAT_1030 = 0x98;
            }
            else {
              DAT_00fd = DAT_00fd & 0xef | 8;
              DAT_1030 = 0xc0;
            }
          }
          else {
            DAT_00fd = bVar3 ^ 0x30;
            DAT_1030 = 0x55;
            DAT_1421 = 0;
            DAT_1422 = 0;
          }
        }
        else {
          DAT_00fd = bVar3 ^ 0x60;
          DAT_1030 = 0x54;
          if (DAT_0044 < '\0') {
            _P2DDR = 0;
            _P2DATA = 0;
            P4DDR = 0;
            DAT_142b = 0;
          }
          DAT_0044 = '\0';
        }
      }
      else {
        DAT_00fd = bVar3 ^ 0xc0;
        DAT_1030 = 0x50;
        DAT_00a0 = '\0';
        DAT_0094 = 0x2b;
        _DAT_0098 = 0x804;
      }
    }
    if ((DAT_0016 & 0x1f) != 0) {
      return;
    }
    DAT_102e = DAT_102e + 1;
    if (4 < DAT_102e) {
      if (DAT_102e == 5) {
LAB_9e5e:
        DAT_00a2 = DAT_00a2 | 0x18;
        DAT_0100 = 0x19;
        DAT_0101 = DAT_00a2;
        return;
      }
      if (DAT_102e < 0xe) {
        bVar1 = (bool)(DAT_1030 >> 7);
        DAT_1030 = DAT_1030 << 1;
        if (bVar1) goto LAB_9e5e;
      }
      else if ((DAT_102e != 0xe) && (0xf < DAT_102e)) {
        DAT_00fd = DAT_00fd & 0xf7;
        DAT_00fe = DAT_00fe & 0xf0;
        DAT_0100 = 0x19;
        DAT_0101 = DAT_00a2;
        DAT_102e = 0;
        DAT_1420 = TRCS & 3;
        return;
      }
    }
  }
  else {
    if (P3SCR == '\0') {
      if ((P1DDR & 0x10) != 0) goto LAB_9e5e;
      goto LAB_9e64;
    }
    if ((TRCS & 1) != 0) {
      if (DAT_00a0 != -1) {
        DAT_00a0 = -1;
        DAT_0094 = 0x31;
      }
      DAT_0094 = DAT_0094 + 1;
      if (0x31 < DAT_0094) {
        DAT_009a = DAT_bf7c;
        DAT_009b = DAT_bf2f;
        DAT_0094 = 0;
        goto LAB_9e64;
      }
      if (DAT_0094 == 0x1d) {
        DAT_009a = DAT_009b;
LAB_9cb0:
        DAT_00a2 = DAT_00a2 & 0xf7 | 0x10;
        DAT_0100 = 0x19;
        DAT_0101 = DAT_00a2;
        return;
      }
      if (DAT_0094 == 0x31) goto LAB_9cb0;
      if (DAT_0094 < 0xb) goto LAB_9e64;
      if ((DAT_0094 != 0x1f) && (DAT_0094 != 0xb)) {
        if (!(bool)(DAT_0094 & 1)) goto LAB_9e52;
        bVar1 = (bool)(DAT_009a & 1);
        DAT_009a = DAT_009a >> 1;
        if (bVar1) goto LAB_9cb0;
      }
      goto LAB_9e5e;
    }
    if (DAT_00a0 != '\0') {
      DAT_0094 = 0x2b;
      _DAT_0098 = 0x804;
    }
LAB_9e14:
    DAT_00a0 = '\0';
    DAT_0094 = DAT_0094 + 1;
    if (0x2b < DAT_0094) {
      DAT_0094 = 0;
      FUN_9f98();
    }
    bVar2 = DAT_009b;
    bVar3 = DAT_009a;
    if (0xf < DAT_0094) {
      if (DAT_0094 < 0x1a) {
        if ((!(bool)(DAT_0094 & 1)) && (DAT_009b = DAT_009b << 1, (char)bVar2 < '\0')) {
LAB_9e46:
          DAT_00a2 = DAT_00a2 | 0x10;
          DAT_0100 = 0x19;
          DAT_0101 = DAT_00a2;
          return;
        }
      }
      else if ((0x21 < DAT_0094) &&
              (((DAT_0094 & 1) != 0 && (DAT_009a = DAT_009a << 1, (char)bVar3 < '\0')))) {
LAB_9e4c:
        DAT_00a2 = DAT_00a2 | 8;
        DAT_0100 = 0x19;
        DAT_0101 = DAT_00a2;
        return;
      }
    }
  }
LAB_9e64:
  DAT_0101 = DAT_00a2 & 0xe7;
  DAT_0100 = 0x19;
  DAT_00a2 = DAT_00a2 & 0xe7;
  return;
}


// ---- FUN_9f5e @ 9f5e ----

void FUN_9f5e(byte param_1,char param_2)

{
  char cVar1;
  
  cVar1 = param_2;
  if ((param_1 & 8) == 0) {
    cVar1 = param_2 * '\x02';
    if (param_2 < '\0') {
      cVar1 = cVar1 + '\x01';
      if ((DAT_00fe & 0x80) != 0) {
        DAT_00a2 = DAT_00a2 | 8;
        goto LAB_9f8f;
      }
      DAT_00a2 = DAT_00a2 | 0x10;
      goto LAB_9f82;
    }
  }
  if ((DAT_00fe & 0x80) != 0) {
    DAT_00a2 = DAT_00a2 & 0xf7;
LAB_9f8f:
    DAT_1422 = DAT_1422 + '\x01';
    DAT_1424 = cVar1;
    return;
  }
  DAT_00a2 = DAT_00a2 & 0xef;
LAB_9f82:
  DAT_1421 = DAT_1421 + '\x01';
  DAT_1423 = cVar1;
  return;
}


// ---- FUN_9f98 @ 9f98 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9f98(void)

{
  bool bVar1;
  byte bVar2;
  char cVar3;
  byte *pbVar4;
  undefined1 *puVar5;
  
  if (((_P2DDR == 0) && (_P2DATA == 0)) && ((P4DDR & 0xfe) == 0)) {
    _DAT_0098 = 0x804;
    DAT_009a = 0xf8;
    DAT_009b = 0xf8;
  }
  else {
    bVar2 = DAT_0098;
    cVar3 = DAT_0099;
    do {
      if ((bVar2 >> 1 == 4) && (cVar3 = cVar3 + '\x01', cVar3 == '\x05')) {
        cVar3 = '\0';
      }
      pbVar4 = &P2DDR;
      bVar2 = FUN_9014();
    } while ((bVar2 & *pbVar4) == 0);
    _DAT_0098 = CONCAT11(bVar2,cVar3);
    puVar5 = &DAT_9fec;
    bVar2 = FUN_9014();
    DAT_009b = *puVar5;
    puVar5 = (undefined1 *)0x9fe7;
    while (bVar1 = (bool)(bVar2 >> 7), bVar2 = bVar2 << 1, !bVar1) {
      puVar5 = puVar5 + 1;
    }
    DAT_009a = *puVar5;
  }
  return;
}


// ---- FUN_9ff1 @ 9ff1 ----

/* WARNING: Removing unreachable block (RAM,0xa157) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9ff1(void)

{
  bool bVar1;
  bool bVar2;
  char cVar3;
  byte bVar4;
  byte bVar5;
  undefined1 uVar6;
  byte bVar7;
  
  bVar5 = DAT_1059;
  DAT_1059 = bVar5;
  if (((DAT_0016 & 0xf) == 0) && (DAT_1059 = DAT_1059 + 1, DAT_1059 == 0)) {
    DAT_1059 = bVar5;
  }
  if ((DAT_0079 & 1) == 0) {
    _DAT_0052 = _DAT_0072;
    FUN_8023();
    FUN_802b();
    DAT_0056 = 0;
    bVar5 = DAT_0081;
    if ((DAT_0080 == '\0') && (DAT_0081 < 0x40)) {
      bVar5 = 0x40;
    }
    DAT_0057 = DAT_0080;
    DAT_0059 = 0;
    DAT_0058 = bVar5;
    DAT_105a = FUN_8080();
LAB_a04b:
    _DAT_0020 = CONCAT11(DAT_105a,bVar5);
    DAT_007d = (DAT_105a - DAT_00b8) - (bVar5 < DAT_00b9);
    if (DAT_105a < DAT_00b8 || (byte)(DAT_105a - DAT_00b8) < (bVar5 < DAT_00b9)) {
      if (DAT_007d < 0x80) {
        DAT_007d = 0x80;
      }
    }
    else if (0x7f < DAT_007d) {
      DAT_007d = 0x7f;
    }
    DAT_105d = DAT_007d + 0x80;
    _DAT_00b8 = _DAT_0020;
    bVar5 = DAT_00c0;
    bVar4 = FUN_80d2();
    if (bVar4 < DAT_105a) {
      if (DAT_b909 <= DAT_1059) {
        bVar5 = DAT_00c0 | 0x10;
      }
    }
    else {
      DAT_1059 = 0;
      bVar5 = DAT_00c0;
    }
    bVar4 = DAT_bf16;
    if ((DAT_bf14 < DAT_007c) && (bVar4 = DAT_bf17, DAT_bf15 < DAT_007c)) {
      bVar4 = 0x40;
    }
    DAT_00c0 = bVar5;
    FUN_80d2();
    FUN_8000();
    FUN_8025();
    FUN_8000();
    bVar5 = FUN_8025();
    if ((DAT_0020 <= bVar5) && ((bVar5 != DAT_0020 || (DAT_0021 < bVar4)))) {
      _DAT_0020 = CONCAT11(bVar5,bVar4);
    }
    FUN_80d2();
    FUN_8000();
    bVar5 = FUN_8025();
    if (bVar5 <= DAT_0020) {
      _DAT_0020 = (ushort)bVar5 << 8;
    }
  }
  else {
    if (DAT_008c < 0x28) {
      DAT_105a = DAT_bf8d;
      if ((TRCS & 1) == 0) {
        DAT_105a = DAT_bfa2;
      }
      bVar5 = 0;
      goto LAB_a04b;
    }
    _DAT_0020 = 0;
  }
  if ((TRCS & 2) == 0) {
    _DAT_0052 = _DAT_0020;
    if (DAT_009d == '\0') {
      if ((((TRCS & 1) != 0) || (DAT_0020 < DAT_b905)) && ((TRCS & 4) == 0)) {
        bVar5 = DAT_bf02;
        if ((DAT_0032 & 4) != 0) {
          bVar5 = DAT_bf02 - 5;
        }
        if (bVar5 < TX) {
          bVar5 = 0x3c;
          if ((DAT_0032 & 4) != 0) {
            bVar5 = 0x40;
          }
          if (DAT_008c <= bVar5) {
            if (DAT_bf04 != 0) {
              bVar5 = DAT_bf04;
              if ((DAT_0032 & 4) == 0) {
                bVar5 = DAT_bf04 + 0x10;
              }
              if (DAT_0048 <= bVar5) goto code_r0xa225;
            }
            if (DAT_bf01 != 0) {
              bVar5 = DAT_bf01;
              if ((DAT_0032 & 4) == 0) {
                bVar5 = DAT_bf01 + 2;
              }
              if (DAT_000c <= bVar5) goto code_r0xa225;
            }
            if ((DAT_0032 & 4) == 0) {
              DAT_0032 = DAT_0032 | 4;
              DAT_009d = '\x14';
            }
            goto LAB_a212;
          }
        }
      }
code_r0xa225:
      DAT_0032 = DAT_0032 & 0xfb;
    }
    else {
      DAT_009d = DAT_009d + -1;
LAB_a212:
      if (DAT_0020 <= DAT_00b5 && (DAT_00b6 < DAT_0021) <= (byte)(DAT_00b5 - DAT_0020)) {
        _DAT_0052 = _DAT_00b5;
      }
    }
    FUN_802b();
    cVar3 = DAT_00cd;
    if ((TRCS & 1) != 0) {
      cVar3 = DAT_1406;
    }
    bVar5 = cVar3 + DAT_0031;
    cVar3 = FUN_802b();
    DAT_001e = bVar5 + DAT_002a;
    DAT_001d = cVar3 + CARRY1(bVar5,DAT_002a);
    if (DAT_007e < 0x3c) goto LAB_a151;
  }
  else {
    if ((DAT_001f & 1) == 0) {
      DAT_002c = 0;
      DAT_001f = DAT_001f | 1;
    }
    _DAT_0052 = _DAT_0020;
    FUN_802b();
    bVar5 = 0;
    cVar3 = FUN_802b();
    DAT_001e = bVar5 + DAT_002a;
    DAT_001d = cVar3 + CARRY1(bVar5,DAT_002a);
LAB_a151:
    if (DAT_002c < 0x10) {
      DAT_002b = FUN_80d2();
      if (0xc < DAT_0048) {
        if (DAT_0048 < 0x30) {
          FUN_8000();
        }
        DAT_002b = FUN_8000();
      }
      cVar3 = DAT_002c - 10;
      if (DAT_002c < 10 || cVar3 == '\0') {
        bVar5 = 100;
      }
      else {
        FUN_8000();
        bVar5 = 100 - cVar3;
      }
      bVar4 = FUN_8000();
      if ((DAT_001d < bVar4) || ((bVar4 == DAT_001d && (DAT_001e < bVar5)))) {
        DAT_001d = bVar4;
        DAT_001e = bVar5;
      }
    }
  }
  if (((DAT_bfd3 & 0x10) == 0) || ((TRCS & 2) != 0)) {
LAB_a2c5:
    DAT_001f = DAT_001f | 0x10;
    DAT_0076 = DAT_001d;
    DAT_0077 = DAT_001e;
  }
  else {
    bVar5 = DAT_bef8;
    if ((DAT_001f & 0x10) == 0) {
      bVar5 = DAT_bef8 - 5;
    }
    if (TX <= bVar5) goto LAB_a2c5;
    DAT_0077 = DAT_001e * '\x02' - DAT_002a;
    DAT_0076 = (DAT_001d << 1 | DAT_001e >> 7) - ((byte)(DAT_001e * '\x02') < DAT_002a);
    _DAT_0052 = CONCAT11(DAT_0076,DAT_0077);
    bVar5 = RMCR;
    cVar3 = FUN_802b();
    if (cVar3 != '\0') goto LAB_a2c5;
    if ((DAT_001f & 0x10) == 0) {
      if ((6 < bVar5) || ((5 < bVar5 && (0x96 < DAT_0054)))) goto LAB_a2c5;
    }
    else if ((5 < bVar5) || ((4 < bVar5 && (0x1f < DAT_0054)))) goto LAB_a2c5;
    DAT_001f = DAT_001f & 0xef;
  }
  bVar5 = (char)((char)DAT_0077 >> 1 | DAT_0076 << 7) >> 1 | (DAT_0076 >> 1) << 7;
  DAT_001c = bVar5 + DAT_0077;
  DAT_001b = (DAT_0076 >> 2) + DAT_0076 + CARRY1(bVar5,DAT_0077);
  if (0x7f < DAT_001b) {
    DAT_001b = 0x7f;
    DAT_001c = 0xff;
  }
  _DAT_0052 = 0;
  for (; bVar5 = DAT_001b < 3, 3 < DAT_001b; DAT_001b = DAT_001b >> 1) {
    _DAT_0052 = _DAT_0052 + 1;
    DAT_001c = (char)DAT_001c >> 1 | DAT_001b << 7;
  }
  if ((DAT_001f & 0x10) == 0) {
    DAT_001f = DAT_001f & 0xdf;
  }
  else {
    DAT_001f = DAT_001f | 0x20;
  }
  DAT_001a = DAT_0053;
  if ((DAT_bfd3 & 0x20) != 0) {
    if ((DAT_00b7 & 0x40) == 0) {
      if (((DAT_001f & 0x20) != 0) || ((DAT_101f & 0x20) == 0)) goto LAB_a381;
      DAT_00b7 = DAT_00b7 | 0x40;
    }
    DAT_0100 = 0x1f;
    if ((DAT_0101 & 0x40) == 0) {
      DAT_0100 = 6;
      DAT_0101 = DAT_103c;
      bVar5 = DAT_0019 < 3;
      if ((bool)bVar5) {
        RX = RX & 0xfb | 8;
      }
      else {
        RX = RX & 0xf7 | 4;
      }
      FUN_a5b0();
      DAT_00b7 = DAT_00b7 & 0xbf;
      bVar5 = bVar5 & 0xe1;
      DAT_101f = DAT_101f & 0xdf;
    }
  }
LAB_a381:
  if ((TRCS & 1) == 0) {
    if ((DAT_00b7 & 8) == 0) {
      bVar5 = DAT_0037 < 0x40;
      if (!(bool)bVar5) {
        DAT_00b7 = DAT_00b7 | 8;
        goto LAB_a39a;
      }
    }
    else {
LAB_a39a:
      uVar6 = DAT_bfc1;
      DAT_1039 = FUN_a5c4();
      bVar5 = bVar5 & 0xf1;
      DAT_103a = uVar6;
      FUN_a56f();
      if (!(bool)(bVar5 & 1)) {
        DAT_00b7 = DAT_00b7 & 0xf7;
      }
    }
    DAT_0037 = 0;
    bVar5 = false;
    if ((DAT_00c3 == '\0') && (bVar5 = true, DAT_bfea <= DAT_008c)) {
      bVar5 = DAT_00b8 < DAT_bfc9;
      if (((bool)bVar5) && (-1 < (char)DAT_007d)) {
        bVar5 = true;
        if ((DAT_00b7 & 4) == 0) {
          DAT_1034 = DAT_bfc0;
          bVar5 = DAT_bfc8;
          if ((DAT_bfeb <= DAT_008c) &&
             (DAT_1034 = DAT_bfed, bVar5 = DAT_bfef, DAT_bfec <= DAT_008c)) {
            DAT_1034 = DAT_bfee;
            bVar5 = DAT_bff0;
          }
          bVar5 = bVar5 < DAT_007d;
          if (!(bool)bVar5) goto LAB_a428;
          DAT_00b7 = DAT_00b7 | 4;
        }
        uVar6 = DAT_1034;
        DAT_1039 = FUN_a5c4();
        bVar5 = bVar5 & 0xf1;
        DAT_103a = uVar6;
        FUN_a56f();
        if (!(bool)(bVar5 & 1)) {
          DAT_00b7 = DAT_00b7 & 0xfb | 0x20;
          bVar5 = bVar5 & 0xe1;
          DAT_101e = DAT_101d;
          DAT_00c3 = DAT_bff1;
        }
        goto LAB_a4b4;
      }
    }
LAB_a428:
    DAT_00b7 = DAT_00b7 & 0xfb;
LAB_a4b4:
    bVar5 = bVar5 & 0xf1;
    DAT_00b7 = DAT_00b7 & 0xef;
  }
  else {
    bVar1 = DAT_0037 < 0x40;
    bVar2 = !bVar1;
    if (bVar2) {
      DAT_00c3 = '\0';
    }
    else {
      DAT_0037 = DAT_0037 + 1;
      DAT_00c3 = 'd';
    }
    bVar5 = !bVar2 && bVar1;
    if ((DAT_00b7 & 2) == 0) {
      if (((DAT_001f & 8) == 0) || (DAT_00a3 != '\0')) goto LAB_a4b4;
      if ((DAT_00b7 & 0x10) == 0) {
        bVar5 = DAT_000c < DAT_bf85;
        if ((((bool)bVar5) || (FUN_b096(), (bool)(bVar5 & 1))) ||
           ((bVar5 = bVar5 & 0xf1, bVar4 = TRCS, bVar7 = bVar5, (TRCS & 0x40) != 0 &&
            (((TRCS & 8) == 0 && (bVar4 = FUN_b096(), bVar7 = bVar5, (bool)(bVar5 & 1))))))) {
LAB_a485:
          bVar5 = bVar5 & 0xf1;
          DAT_00b7 = DAT_00b7 | 2;
          goto LAB_a48b;
        }
        bVar5 = bVar7 & 0xf1;
        if ((bVar4 & 0x10) != 0) {
          bVar5 = bVar7 & 0xf1;
          FUN_b09b();
          if ((bVar5 & 1) != 0) goto LAB_a485;
        }
      }
    }
    else {
LAB_a48b:
      uVar6 = DAT_bfc3;
      if ((-1 < (char)DAT_009e) && (bVar5 = 1, DAT_bf0f <= DAT_009e)) {
        bVar5 = 0;
        uVar6 = DAT_bfc2;
      }
      DAT_1039 = FUN_a5c4();
      bVar5 = bVar5 & 0xf1;
      DAT_103a = uVar6;
      FUN_a56f();
      if (!(bool)(bVar5 & 1)) {
        bVar5 = bVar5 & 0xf1;
        DAT_00b7 = DAT_00b7 & 0xfd | 0x10;
      }
    }
  }
  bVar5 = bVar5 & 0xf1;
  if ((DAT_00b7 & 0x20) != 0) {
    uVar6 = DAT_bf99;
    DAT_1039 = FUN_a5c4();
    bVar5 = bVar5 & 0xf1;
    DAT_103a = uVar6;
    FUN_a56f();
    if (!(bool)(bVar5 & 1)) {
      DAT_00b7 = DAT_00b7 & 0xdf;
    }
  }
  bVar5 = TX;
  if ((DAT_0032 & 2) == 0) {
    bVar5 = TX + 5;
  }
  if (bVar5 < DAT_bfd2) {
    DAT_0032 = DAT_0032 | 2;
  }
  else {
    DAT_0032 = DAT_0032 & 0xfd;
    bVar5 = DAT_007d;
    if ((char)DAT_007d < '\0') {
      bVar5 = -DAT_007d;
    }
    if (DAT_bfcf <= bVar5) {
      DAT_003c = DAT_bf29;
    }
  }
  bVar5 = DAT_000c;
  if ((DAT_100b & 0x40) != 0) {
    bVar5 = DAT_000c + 4;
  }
  if (bVar5 < DAT_b90a) {
    DAT_100b = DAT_100b & 0xbf;
  }
  else {
    DAT_100b = DAT_100b | 0x40;
  }
  if (DAT_0020 < DAT_bfca) {
    if ((DAT_1012 & 1) != 0) {
      DAT_1026 = DAT_1026 + 1;
      if (DAT_1026 == 0) {
        DAT_1026 = 0xff;
      }
      if (9 < DAT_1026) {
        if (DAT_1026 < 100) {
          bVar5 = DAT_1012 | 2;
          goto LAB_a569;
        }
        DAT_1012 = DAT_1012 & 0xfe;
      }
    }
    bVar5 = DAT_1012 & 0xfd;
  }
  else {
    DAT_1026 = 0;
    if ((char)DAT_007d < '\0') {
      bVar5 = DAT_1012 & 0xf9;
      if (DAT_bfcd <= (byte)-DAT_007d) {
        bVar5 = bVar5 | 1;
      }
    }
    else {
      bVar5 = DAT_1012 & 0xfe;
      if ((((DAT_1012 & 2) != 0) && (DAT_bfce <= DAT_007d)) && ((DAT_1012 & 4) == 0)) {
        bVar5 = bVar5 | 4;
        DAT_003f = DAT_bfae;
      }
    }
  }
LAB_a569:
  DAT_1012 = bVar5;
  FUN_941a();
  return;
}


// ---- FUN_a56f @ a56f ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a56f(void)

{
  _DAT_0100 = CONCAT11(0x1f,DAT_0101);
  if ((DAT_0101 & 0x40) != 0) {
    return;
  }
  RX = RX & 0xf3;
  if ((DAT_00b7 & 0x20) != 0) {
    RX = DAT_101e & 0xc | RX;
  }
  DAT_0200 = RX;
  _DAT_0100 = 0x404;
  return;
}


// ---- FUN_a5b0 @ a5b0 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a5b0(void)

{
  DAT_0200 = RX;
  _DAT_0100 = 0x404;
  return;
}


// ---- FUN_a5c4 @ a5c4 ----

char FUN_a5c4(undefined1 param_1,byte param_2)

{
  undefined1 uVar1;
  char cVar2;
  byte bVar3;
  byte bStack0000;
  
  bStack0000 = param_2;
  uVar1 = FUN_80d2();
  bVar3 = bStack0000 - 9;
  if (bStack0000 < 9) {
    bVar3 = 0;
  }
  FUN_8000(uVar1,bVar3);
  cVar2 = FUN_8016();
  return cVar2 + (0xdc < bVar3);
}


// ---- FUN_a5de @ a5de ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a5de(void)

{
  bool bVar1;
  bool bVar2;
  char cVar3;
  byte bVar4;
  byte bVar5;
  short sVar6;
  
  if ((DAT_0036 & 8) == 0) {
    FUN_941a();
    return;
  }
  if ((DAT_bee0 & 2) == 0) {
    sVar6 = _DAT_0046 + 1;
    DAT_0047 = (byte)sVar6;
    DAT_0046 = (byte)((ushort)sVar6 >> 8);
    _DAT_0046 = sVar6;
    if (DAT_0046 == 0) {
      bVar2 = DAT_0047 < 0x65;
      if (bVar2) {
        if (((TRCS & 2) != 0) || (0x95 < DAT_000a)) goto LAB_a8a2;
LAB_a8b2:
        if (((((DAT_bee0 & 4) != 0) && ((TRCS & 4) != 0)) || ((TRCS & 0x10) == 0)) &&
           ((((TRCS & 0x40) == 0 || ((TRCS & 4) != 0)) || (DAT_000c == 0)))) {
          if ((TRCS & 2) == 0) {
            if (4 < DAT_00ab) {
              if ((DAT_00ac & 1) == 0) {
                bVar5 = FUN_80d2();
                DAT_00ad = bVar5 + 5;
                if (0xfa < bVar5) {
                  DAT_00ad = 0xff;
                }
                DAT_00ac = DAT_00ac | 1;
              }
              else if (DAT_00ad <= DAT_00ab) {
                bVar5 = TX;
                if ((DAT_00ac & 2) != 0) {
                  bVar5 = TX + 5;
                }
                if (DAT_b908 <= bVar5) {
                  if ((TRCS & 1) != 0) {
                    bVar5 = DAT_bf25;
                    if (-1 < (char)(DAT_00ac | 2)) {
                      bVar5 = DAT_bf24;
                    }
                    if (bVar5 <= DAT_0048) {
                      DAT_00ac = DAT_00ac | 0x82;
                      goto LAB_a940;
                    }
                  }
                  DAT_00ac = DAT_00ac & 0x7f | 2;
                  _DAT_0100 = 0xa63;
                  goto LAB_a943;
                }
              }
            }
          }
          else {
            DAT_00ac = DAT_00ac & 0xfe;
            DAT_00ab = 0;
          }
        }
      }
    }
    else {
      bVar2 = DAT_0047 < 0x30;
      bVar5 = DAT_0046 + 0x8b;
      bVar1 = 0x74 < DAT_0046;
      if (bVar1 && bVar2 <= bVar5) {
LAB_a8a2:
        _DAT_0046 = 0;
        goto LAB_a8b2;
      }
    }
LAB_a940:
    _DAT_0100 = 0xa01;
LAB_a943:
    FUN_9ff1();
    return;
  }
  if ((DAT_0079 & 1) == 0) {
    if ((TRCS & 2) != 0) {
      _DAT_0096 = DAT_bfa3;
      goto LAB_a829;
    }
    if ((TX < 0xa0) || (9 < DAT_00a7)) {
      DAT_0049 = DAT_bf9e;
      if ((TRCS & 0x44) != 0) {
        DAT_0049 = 0;
      }
      if ((TRCS & 1) == 0) {
        DAT_004d = FUN_80d2();
        _DAT_0096 = 0;
      }
      else {
        sVar6 = _DAT_0046 + 1;
        DAT_0046 = (byte)((ushort)sVar6 >> 8);
        if (sVar6 < 0) {
          if (0xf5 < DAT_0046) goto LAB_a66a;
          TRCS = TRCS | 0x20;
          _DAT_0046 = sVar6;
        }
        else {
          if (((TRCS & 2) == 0) && (DAT_000a < 0x97)) {
            DAT_0046 = DAT_0046 + 1;
          }
          else {
LAB_a66a:
            DAT_0046 = 0;
          }
          _DAT_0046 = (ushort)DAT_0046 << 8;
        }
        if (DAT_0016 == '\0') {
          bVar5 = FUN_80d2();
          if (DAT_00a7 < DAT_bef3) {
LAB_a6a1:
            bVar4 = FUN_8000();
          }
          else {
            if (DAT_00a7 < DAT_bef4) {
              bVar4 = DAT_00a7 - DAT_bef3;
              FUN_8000();
              if (bVar4 < DAT_bef5) goto LAB_a6a1;
            }
            bVar4 = 0;
          }
          DAT_105c = bVar4 + bVar5;
          if (CARRY1(bVar4,bVar5)) {
            DAT_105c = 0xff;
          }
        }
        DAT_0045 = DAT_105c;
        if ((TRCS & 0x40) == 0) {
          if ((TRCS & 4) == 0) {
            if (DAT_bf9a <= DAT_105c) {
              DAT_0045 = DAT_bf9a;
            }
          }
          else if (DAT_105c < DAT_bf9b) {
            DAT_0045 = DAT_bf9b;
          }
        }
        if ((TRCS & 0x10) != 0) {
          if ((TRCS & 0x44) == 0) {
            if (DAT_0045 < DAT_bf9c) {
              DAT_0045 = DAT_bf9c;
            }
          }
          else if (DAT_0045 < DAT_bf9d) {
            DAT_0045 = DAT_bf9d;
          }
        }
        if (((TRCS & 0x20) != 0) && (DAT_0045 < 0x40)) {
          DAT_0045 = 0x40;
        }
        bVar5 = TCSR;
        if (0xdf < TCSR) {
          bVar5 = 0x20;
        }
        bVar5 = ((bVar5 & 0xe0) >> 4) + DAT_be6c;
        if (DAT_0045 < bVar5) {
          DAT_0045 = bVar5;
        }
        bVar5 = TX;
        if ((DAT_1005 & 0x80) != 0) {
          bVar5 = TX + 5;
        }
        if (bVar5 < 0x62) {
          DAT_004d = 0;
          DAT_1005 = DAT_1005 & 0x7f;
        }
        else {
          DAT_1005 = DAT_1005 | 0x80;
        }
        if (DAT_004d != 0) {
          if (DAT_004e == '\0') {
            DAT_004e = DAT_bfab;
            DAT_004d = DAT_004d - 1;
          }
          else {
            DAT_004e = DAT_004e + -1;
          }
        }
        if (((TRCS & 4) != 0) || (DAT_000c < 4)) {
          if ((DAT_0096 <= DAT_bfa3._0_1_) &&
             ((DAT_0096 < DAT_bfa3._0_1_ || (DAT_0097 < (byte)DAT_bfa3)))) {
            _DAT_0096 = _DAT_0096 + 1;
            if (DAT_0045 <= DAT_0048) goto LAB_a63f;
            _DAT_0096 = DAT_bfa3;
            bVar2 = CARRY1(DAT_004c,DAT_004d);
            DAT_004c = DAT_004c + DAT_004d;
            if (bVar2) {
              DAT_004c = 0xff;
            }
            DAT_004d = 0;
          }
          if (DAT_0045 < DAT_0048) {
            if (2 < (byte)(DAT_0048 - DAT_0045)) {
              DAT_004f = 0;
              if ((DAT_1005 & 4) == 0) {
                DAT_1005 = DAT_1005 | 4;
              }
              else if (((DAT_009e < '\0') && (DAT_bfa6 <= (byte)-DAT_009e)) &&
                      (bVar2 = CARRY1(DAT_1007 >> 1,DAT_004c), DAT_004c = (DAT_1007 >> 1) + DAT_004c
                      , bVar2)) {
                DAT_004c = 0xff;
              }
              DAT_1007 = 0;
              if (DAT_0050 == '\0') {
                DAT_004c = DAT_004c - 1;
                if ((byte)(DAT_0048 - DAT_0045) < 4) {
                  DAT_0050 = '\x19';
                }
                else {
                  DAT_0050 = '\x06';
                }
              }
              DAT_0050 = DAT_0050 + -1;
              if (DAT_004c == 0) {
                DAT_004c = 1;
              }
              goto LAB_a829;
            }
          }
          else if (1 < (byte)-(DAT_0048 - DAT_0045) && (byte)(DAT_0048 - DAT_0045) != -2) {
            bVar5 = 0;
            cVar3 = FUN_8000();
            if (cVar3 != '\0') {
              bVar5 = 0xff;
            }
            bVar4 = FUN_8000();
            if ((((bool)(bVar4 >> 7)) ||
                (DAT_004f = (bVar4 << 1 | bVar5 >> 7) << 1 | (byte)(bVar5 << 1) >> 7,
                (bool)((byte)(bVar4 << 1) >> 7))) || (0x3f < DAT_004f)) {
              DAT_004f = 0x40;
            }
            if (DAT_1007 <= DAT_004f) {
              DAT_1007 = DAT_004f;
            }
            goto LAB_a7bd;
          }
          DAT_004f = 0;
          goto LAB_a829;
        }
      }
LAB_a63f:
      DAT_1007 = 0;
      DAT_004f = 0;
      goto LAB_a829;
    }
  }
  else {
LAB_a7bd:
    if (DAT_0050 == '\0') {
      DAT_004c = DAT_004c + 1;
      if (DAT_004c == 0) {
        DAT_004c = 0xff;
      }
      if ((byte)(DAT_0045 - DAT_0048) < 4) {
        DAT_0050 = '\x19';
      }
      else {
        DAT_0050 = '\x06';
      }
    }
    DAT_0050 = DAT_0050 + -1;
LAB_a829:
    if (DAT_004c < 0xb4) {
      if (DAT_004c < 0x28) {
        DAT_004c = 0x28;
      }
      bVar5 = DAT_004c;
      if (((TRCS & 1) == 0) && (DAT_004c < DAT_bfbf)) {
        if (DAT_004b == '\0') {
          DAT_004b = '}';
          DAT_004c = DAT_004c + 1;
        }
        else {
          DAT_004b = DAT_004b + -1;
        }
      }
      bVar4 = bVar5 + DAT_004f;
      if (((CARRY1(bVar5,DAT_004f)) || (CARRY1(bVar4,DAT_0049))) ||
         (bVar5 = bVar4 + DAT_0049 + DAT_004d, 0xb3 < bVar5)) {
        bVar5 = 0xb4;
      }
      else if (bVar5 < 0x28) {
        bVar5 = 0x28;
      }
      goto LAB_a872;
    }
  }
  bVar5 = 0xb4;
  DAT_004c = 0xb4;
LAB_a872:
  DAT_1011 = (byte)(-bVar5 - 0x38) >> 1;
  _DAT_0100 = CONCAT11(10,DAT_1011);
  FUN_9ff1();
  return;
}


// ---- FUN_a949 @ a949 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a949(void)

{
  bool bVar1;
  char cVar2;
  byte bVar3;
  byte bVar4;
  
  P4DATA = FUN_953a();
  bVar4 = DAT_100c;
  if ((DAT_bee0 & 8) == 0) {
LAB_a982:
    DAT_100c = bVar4;
    if ((DAT_0032 & 0x20) == 0) {
      if ((TRCS & 2) != 0) {
        DAT_100d = 0;
        goto LAB_ad0e;
      }
      if ((DAT_bee0 & 8) == 0) {
        if (0x27 < DAT_003d) {
          DAT_003d = 0x28;
          goto LAB_aa3d;
        }
      }
      else {
        if ((DAT_100b & 1) == 0) {
          bVar4 = DAT_100e;
          if ((DAT_000a < 0x96) && (bVar4 = DAT_100e + 0x78, 0x87 < DAT_100e)) {
            bVar4 = 0xff;
          }
          if ((DAT_100d < bVar4) || ((P4DATA < DAT_bf92 && (DAT_100d < DAT_1037)))) goto LAB_ad11;
        }
        if ((DAT_100b & 1) != 0) {
          if ((DAT_100b & 2) != 0) {
            if (DAT_bfa0 < P4DATA) goto LAB_ad11;
LAB_aa84:
            DAT_0032 = DAT_0032 | 0x28;
            DAT_100b = DAT_100b & 0xfc;
            DAT_003d = 0;
            goto LAB_aa93;
          }
          if (DAT_bfa0 < P4DATA) goto LAB_aa84;
          goto LAB_ac7a;
        }
LAB_aa3d:
        bVar4 = DAT_bf91;
        if (DAT_007e < 0x3c) {
          bVar4 = DAT_bee7;
        }
        if (bVar4 <= TX) {
          if ((DAT_bee0 & 8) != 0) goto LAB_aa84;
          if (P4DATA < DAT_bf92) {
            if (DAT_bf93 <= P4DATA) {
              DAT_003a = 0;
              goto LAB_ac7a;
            }
            DAT_003a = DAT_003a - 1;
          }
          else {
            DAT_003a = DAT_003a + 1;
          }
          if ((char)DAT_003a < '\0') {
            if (DAT_003a < 0xf6) goto LAB_aa84;
          }
          else if (9 < DAT_003a) {
            DAT_0032 = DAT_0032 | 0x40;
            goto LAB_aa84;
          }
        }
      }
      goto LAB_ad11;
    }
    if ((((TRCS & 1) == 0) || (DAT_0048 < DAT_bfd1)) || (DAT_000c < 4)) {
      DAT_0033 = 0;
      if ((DAT_0032 & 0x80) == 0) goto LAB_aa93;
      DAT_0034 = DAT_0034 + 1;
      if (0x13 < DAT_0034) {
        DAT_0032 = DAT_0032 & 0x7f;
      }
      goto LAB_ad2b;
    }
    DAT_0034 = 0;
    if ((DAT_0032 & 0x80) == 0) {
      DAT_0033 = DAT_0033 + 1;
      if (0x13 < DAT_0033) {
        DAT_0032 = DAT_0032 | 0x80;
      }
LAB_aa93:
      if ((DAT_003e & 8) != 0) {
LAB_aa99:
        DAT_0084 = 0;
        DAT_00b2 = 0;
        DAT_00ae = '\0';
        DAT_00af = 0;
        goto LAB_ad0e;
      }
      if ((TRCS & 1) == 0) {
        DAT_0032 = DAT_0032 & 0xef;
        goto LAB_ab02;
      }
      DAT_0032 = DAT_0032 | 0x10;
      if (((DAT_bfd3 & 1) != 0) && ((RX & 0x20) != 0)) goto LAB_aa99;
      if (DAT_000c < 2) {
        if (TX < 0x73) {
          if ((DAT_bfd3 & 4) != 0) goto LAB_aa99;
          goto LAB_ab02;
        }
        DAT_0084 = DAT_0084 | 0x80;
        if ((0x80 < DAT_0084) && (DAT_00b2 = DAT_00b2 | 0x80, 0x87 < DAT_00b2)) {
          bVar4 = DAT_00af;
          cVar2 = FUN_801f(DAT_00ae);
          DAT_0030 = FUN_ad3f(cVar2 + DAT_beec);
          DAT_003d = 0;
          goto LAB_ad2e;
        }
      }
      else {
LAB_ab02:
        DAT_0084 = 0;
        if ((DAT_bef6 != 0) && (0x87 < DAT_00b2)) {
          bVar4 = DAT_00af;
          cVar2 = FUN_801f();
          cVar2 = ((char)bVar4 >> 1 | cVar2 << 7) + DAT_1406;
          DAT_1405 = FUN_ad3f();
          DAT_1406 = cVar2;
        }
        DAT_00b2 = 0;
        DAT_00ae = '\0';
        DAT_00af = 0;
      }
      if (P4DATA < DAT_0035) {
        if ((DAT_0032 & 8) == 0) {
          if ((((DAT_0032 & 0x10) == 0) || (_DAT_0052 = DAT_bef1, (DAT_100b & 0x40) != 0)) &&
             ((_DAT_0052 = DAT_beee, (DAT_0032 & 2) == 0 && (_DAT_0052 = DAT_bf06, DAT_003c != '\0')
              ))) {
            _DAT_0052 = DAT_bf0c;
          }
          bVar4 = DAT_001e;
          cVar2 = FUN_802b();
          bVar1 = CARRY1(bVar4,DAT_0031);
          DAT_0031 = bVar4 + DAT_0031;
          DAT_0030 = cVar2 + DAT_0030 + bVar1;
        }
        else {
          DAT_0032 = DAT_0032 & 0xf7;
          if ((char)DAT_00b2 < '\0') {
            bVar1 = CARRY1(DAT_0030,DAT_00af);
            DAT_00af = DAT_0030 + DAT_00af;
            DAT_00ae = DAT_00ae + bVar1;
            DAT_00b2 = DAT_00b2 + 1;
          }
          bVar3 = 0;
          bVar4 = FUN_8016();
          DAT_1014 = -(bVar4 >> 1);
          bVar1 = CARRY1(bVar3,DAT_0031);
          DAT_0031 = bVar3 + DAT_0031;
          DAT_0030 = bVar4 + DAT_0030 + bVar1;
          DAT_0035 = DAT_1036;
          if ((DAT_0032 & 0x40) != 0) {
            DAT_0032 = DAT_0032 & 0xbf;
            DAT_0035 = DAT_bfa1;
          }
        }
      }
      else if ((DAT_0032 & 8) == 0) {
        DAT_0032 = DAT_0032 | 8;
        if ((char)DAT_00b2 < '\0') {
          bVar1 = CARRY1(DAT_0030,DAT_00af);
          DAT_00af = DAT_0030 + DAT_00af;
          DAT_00ae = DAT_00ae + bVar1;
          DAT_00b2 = DAT_00b2 + 1;
        }
        DAT_0035 = DAT_1035;
        bVar3 = 0;
        bVar4 = FUN_8016();
        _DAT_0052 = CONCAT11(bVar4,bVar3);
        DAT_1014 = bVar4 >> 1;
        bVar1 = DAT_0031 < bVar3;
        DAT_0031 = DAT_0031 - bVar3;
        DAT_0030 = (DAT_0030 - bVar4) - bVar1;
        DAT_003d = 0;
      }
      else {
        if (((((DAT_0032 & 0x10) == 0) || (_DAT_0052 = DAT_bef1, (DAT_100b & 0x40) != 0)) &&
            (_DAT_0052 = DAT_beee, (DAT_0032 & 2) == 0)) && (_DAT_0052 = DAT_bf06, DAT_003c != '\0')
           ) {
          _DAT_0052 = DAT_bf0c;
        }
        FUN_802b();
        bVar1 = DAT_0031 < DAT_0053;
        DAT_0031 = DAT_0031 - DAT_0053;
        DAT_0030 = (DAT_0030 - DAT_0052) - bVar1;
      }
LAB_ac7a:
      if (P4DATA < DAT_0035) {
        if ((DAT_100a & 1) == 0) {
          DAT_100a = DAT_100a & 0xfd;
          goto LAB_aca5;
        }
        if ((DAT_100a & 2) != 0) goto LAB_aca8;
        if (DAT_b787 <= DAT_103e) {
          DAT_103d = DAT_103d + 1;
          DAT_100a = DAT_100a | 2;
          goto LAB_aca8;
        }
      }
      else {
LAB_aca5:
        DAT_103e = 0;
LAB_aca8:
        if (DAT_b78a <= DAT_103d) {
          P2DATA = P2DATA | 0x20;
          DAT_1413 = 0;
          DAT_103d = 0;
        }
      }
      if ((DAT_0032 & 0x20) != 0) {
        if (DAT_003d < DAT_bf7e) {
          FUN_ad51();
          DAT_0030 = FUN_ad3f(DAT_0030);
          goto LAB_ad38;
        }
        if ((DAT_0032 & 8) == 0) {
          bVar4 = DAT_100b & 0xfd | 1;
        }
        else {
          bVar4 = DAT_100b | 3;
          if ((char)DAT_00b2 < '\0') {
            bVar4 = DAT_100b | 0x13;
          }
          else if (DAT_b7a4 <= bVar4) {
            bVar4 = DAT_100b | 0x23;
          }
        }
        DAT_100b = bVar4;
        FUN_84ee();
        goto LAB_ad00;
      }
      goto LAB_ad11;
    }
    bVar4 = 0;
    DAT_003d = 0;
    DAT_0030 = DAT_bfd0;
  }
  else {
    if ((DAT_100b & 4) == 0) {
      if (P4DATA < 200) {
        bVar4 = 0;
      }
      else {
        bVar4 = DAT_100c + 1;
        if (4 < (byte)(DAT_100c + 1)) {
          DAT_100b = DAT_100b | 4;
          P2DATA = P2DATA | 0x20;
          DAT_1413 = 0;
          goto LAB_ad00;
        }
      }
      goto LAB_a982;
    }
LAB_ad00:
    DAT_0035 = DAT_bfa0;
    DAT_0032 = DAT_0032 & 0xdf;
    DAT_003a = 0;
LAB_ad0e:
    DAT_003d = 0;
LAB_ad11:
    if (DAT_0030 < 100) {
      bVar4 = DAT_0031 + 0x15;
      DAT_0030 = DAT_0030 + (0xea < DAT_0031);
      if (99 < DAT_0030) {
LAB_ad2b:
        bVar4 = 0;
        DAT_0030 = 100;
      }
    }
    else {
      bVar4 = DAT_0031 - 0x15;
      DAT_0030 = DAT_0030 - (DAT_0031 < 0x15);
      if (DAT_0030 < 100) goto LAB_ad2b;
    }
  }
LAB_ad2e:
  DAT_100b = DAT_100b | 8;
  DAT_0031 = bVar4;
LAB_ad38:
  FUN_ae89();
  return;
}


// ---- FUN_ad3f @ ad3f ----

byte FUN_ad3f(byte param_1)

{
  if (param_1 < 0x4b) {
    param_1 = 0x4b;
  }
  else if (0x7c < param_1) {
    param_1 = 0x7d;
  }
  return param_1;
}


// ---- FUN_ad51 @ ad51 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_ad51(void)

{
  bool bVar1;
  byte bVar2;
  char cVar3;
  undefined1 uVar4;
  byte bVar5;
  char cVar6;
  char *pcVar7;
  
  if (((((TRCS & 1) != 0) || ((DAT_0032 & 0x80) != 0)) || ((RX & 0x20) != 0)) ||
     ((DAT_00b7 & 0x80) == 0)) {
    return;
  }
  if ((byte)(DAT_00b0 + 1) < 0x10) {
    DAT_00b0 = DAT_00b0 + 1;
    return;
  }
  DAT_00b0 = 0;
  DAT_0052 = DAT_0030 + DAT_1014 + 0x9c;
  if ((byte)(DAT_0030 + DAT_1014) < 100) {
    DAT_0053 = -DAT_0031;
    DAT_0052 = -(DAT_0052 + (DAT_0053 != '\0'));
    uVar4 = (undefined1)DAT_bef6;
    pcVar7 = _DAT_00ba;
    DAT_00c4 = FUN_802b(DAT_bef6._0_1_);
    bVar5 = ~DAT_00bc;
    DAT_00c5 = uVar4;
    cVar3 = FUN_ae67(~DAT_00b1);
    bVar5 = -bVar5;
    cVar6 = bVar5 + pcVar7[1];
    cVar3 = FUN_ae76((*pcVar7 - (cVar3 + (bVar5 != 0))) + CARRY1(bVar5,pcVar7[1]));
    *pcVar7 = cVar3;
    pcVar7[1] = cVar6;
    bVar5 = ~DAT_00bc;
    cVar3 = FUN_ae67(DAT_00b1);
    bVar5 = -bVar5;
    cVar6 = bVar5 + pcVar7[3];
    cVar3 = FUN_ae76((pcVar7[2] - (cVar3 + (bVar5 != 0))) + CARRY1(bVar5,pcVar7[3]));
    pcVar7[2] = cVar3;
    pcVar7[3] = cVar6;
    bVar5 = DAT_00bc;
    cVar3 = FUN_ae67(~DAT_00b1);
    bVar5 = -bVar5;
    cVar6 = bVar5 + pcVar7[0x21];
    cVar3 = FUN_ae76((pcVar7[0x20] - (cVar3 + (bVar5 != 0))) + CARRY1(bVar5,pcVar7[0x21]));
    pcVar7[0x20] = cVar3;
    pcVar7[0x21] = cVar6;
    bVar5 = DAT_00bc;
    cVar3 = FUN_ae67(DAT_00b1);
    bVar5 = -bVar5;
    cVar6 = bVar5 + pcVar7[0x23];
    cVar3 = FUN_ae76((pcVar7[0x22] - (cVar3 + (bVar5 != 0))) + CARRY1(bVar5,pcVar7[0x23]));
    pcVar7[0x22] = cVar3;
    pcVar7[0x23] = cVar6;
    return;
  }
  DAT_0053 = DAT_0031;
  uVar4 = (undefined1)DAT_bef6;
  pcVar7 = _DAT_00ba;
  DAT_00c4 = FUN_802b();
  bVar5 = ~DAT_00bc;
  DAT_00c5 = uVar4;
  FUN_ae67();
  cVar6 = bVar5 + pcVar7[1];
  cVar3 = FUN_ae76();
  *pcVar7 = cVar3;
  pcVar7[1] = cVar6;
  bVar5 = ~DAT_00bc;
  FUN_ae67();
  cVar6 = bVar5 + pcVar7[3];
  cVar3 = FUN_ae76();
  pcVar7[2] = cVar3;
  pcVar7[3] = cVar6;
  bVar5 = DAT_00bc;
  FUN_ae67();
  cVar6 = bVar5 + pcVar7[0x21];
  cVar3 = FUN_ae76();
  pcVar7[0x20] = cVar3;
  pcVar7[0x21] = cVar6;
  bVar5 = DAT_00bc;
  bVar2 = FUN_ae67();
  bVar1 = CARRY1(bVar5,pcVar7[0x23]);
  cVar6 = bVar5 + pcVar7[0x23];
  bVar5 = bVar2 + pcVar7[0x22];
  cVar3 = bVar5 + bVar1;
  if (CARRY1(bVar2,pcVar7[0x22]) || CARRY1(bVar5,bVar1)) {
    cVar3 = -1;
  }
  cVar3 = FUN_ae76(cVar3);
  pcVar7[0x22] = cVar3;
  pcVar7[0x23] = cVar6;
  return;
}


// ---- FUN_ae67 @ ae67 ----

void FUN_ae67(undefined1 param_1,undefined1 param_2)

{
  DAT_0052 = FUN_8000();
  DAT_0053 = param_2;
  FUN_802b(DAT_00c4,DAT_00c5);
  return;
}


// ---- FUN_ae76 @ ae76 ----

byte FUN_ae76(byte param_1)

{
  if (param_1 < 0x7d) {
    if (param_1 < 0x4b) {
      param_1 = 0x4b;
    }
  }
  else {
    param_1 = 0x7d;
  }
  return param_1;
}


// ---- FUN_ae89 @ ae89 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_ae89(void)

{
  char cVar1;
  undefined1 uVar2;
  byte bVar3;
  undefined1 uVar4;
  char cVar5;
  byte bVar6;
  byte bVar7;
  
  if (DAT_000a < 0xb0) {
    cVar1 = FUN_8000();
  }
  else {
    cVar1 = FUN_8000();
    cVar1 = -cVar1;
  }
  DAT_002a = cVar1 + DAT_bf88;
  if ((DAT_0032 & 0x20) == 0) {
    uVar2 = FUN_80d2();
    if (0x28 < DAT_008c) {
      if (DAT_008c < 0x2e) {
        FUN_8000();
      }
      uVar2 = FUN_8000(uVar2);
    }
    uVar4 = 0;
    uVar2 = FUN_801a(uVar2);
  }
  else {
    uVar2 = 0;
    uVar4 = 0;
  }
  _DAT_0028 = CONCAT11(uVar2,uVar4);
  if ((TRCS & 2) != 0) {
    DAT_0024 = FUN_80d2();
    DAT_0025 = -1;
  }
  if (DAT_0025 != '\0') {
    bVar6 = DAT_0024;
    FUN_8000();
    cVar1 = FUN_801a();
    _DAT_0028 = CONCAT11(cVar1 + DAT_0028 + CARRY1(bVar6,DAT_0029),bVar6 + DAT_0029);
  }
  if ((TRCS & 2) != 0) {
    DAT_00a7 = 0;
LAB_b16f:
    if (DAT_0026 != '\0') {
      bVar6 = 0;
      cVar1 = FUN_8018();
      _DAT_0028 = CONCAT11(cVar1 + DAT_0028 + CARRY1(bVar6,DAT_0029),bVar6 + DAT_0029);
    }
    if (_DAT_0028 == 0) {
      DAT_00b7 = DAT_00b7 | 0x80;
    }
    else {
      DAT_00b7 = DAT_00b7 & 0x7f;
    }
    bVar7 = 0;
    cVar1 = FUN_8018();
    bVar6 = cVar1 + DAT_0028 + CARRY1(bVar7,DAT_0029);
    _DAT_0028 = CONCAT11(bVar6,bVar7 + DAT_0029);
    if (0x3f < bVar6) {
      _DAT_0028 = 0x4000;
    }
LAB_b1a6:
    if ((DAT_00b5 < DAT_0020 || (byte)(DAT_00b5 - DAT_0020) < (DAT_00b6 < DAT_0021)) ||
       (0x3f < DAT_008c)) {
      _DAT_00b5 = _DAT_0020;
    }
    else {
      DAT_0057 = DAT_bf0b;
      if (((DAT_008c < 0x30) && (DAT_0057 = DAT_bf0a, DAT_008c < DAT_bfa8)) &&
         (DAT_0057 = DAT_bf08, DAT_bfa9 <= DAT_008c)) {
        DAT_0057 = DAT_bf09;
      }
      bVar6 = 0;
      _DAT_0052 = _DAT_0020;
      cVar1 = FUN_802b();
      _DAT_0052 = _DAT_00b5;
      FUN_802b(-DAT_0057,0);
      _DAT_00b5 = CONCAT11(cVar1 + DAT_0052 + CARRY1(bVar6,DAT_0053),bVar6 + DAT_0053);
    }
    FUN_941a();
    return;
  }
  bVar6 = DAT_001f & 0xfe;
  if ((DAT_001f & 0x40) == 0) {
    if ((DAT_bfb4 <= DAT_008c) || (DAT_bfa5 < DAT_000c)) {
LAB_af62:
      bVar6 = bVar6 | 0x40;
LAB_af68:
      DAT_001f = bVar6;
      FUN_b112();
      return;
    }
    if (DAT_008c < DAT_bf8b) {
      _DAT_0042 = 0;
    }
    else {
      _DAT_0042 = _DAT_0042 + 1;
      if (_DAT_0042 == 0x200) goto LAB_af62;
    }
    DAT_001f = bVar6;
    if (DAT_000c == 0) {
      if ((DAT_008c < DAT_bfe9) || (DAT_0020 < DAT_beea)) goto LAB_af8f;
      DAT_002f = DAT_002f | 0x80;
      if (0x84 < DAT_002f) goto LAB_af62;
    }
  }
  else {
    if (DAT_bf8b <= (byte)(DAT_008c + 10)) goto LAB_af68;
    if (DAT_000c == 0) {
      if (DAT_bfe9 <= (byte)(DAT_008c + 10)) goto LAB_af68;
    }
    else if (DAT_bfa5 <= (byte)(DAT_000c + 10)) goto LAB_af68;
    DAT_001f = DAT_001f & 0xbe;
    _DAT_0042 = 0;
LAB_af8f:
    DAT_002f = 0;
  }
  if ((TRCS & 1) == 0) {
    DAT_007c = -1;
    DAT_00bf = 0;
    if ((DAT_001f & 2) == 0) {
      cVar5 = DAT_002e - DAT_bf1f;
      cVar1 = DAT_002d - (DAT_002e < DAT_bf1f);
      if (DAT_002d < (DAT_002e < DAT_bf1f)) {
        cVar1 = '\0';
        cVar5 = '\0';
      }
      _DAT_002d = CONCAT11(cVar1,cVar5);
      DAT_001f = DAT_001f & 0xfb;
      goto LAB_b021;
    }
    DAT_001f = DAT_001f & 0xf9;
    bVar6 = FUN_80d2();
    if (TX < 0x41) {
      if (0x3b < DAT_00a7) {
        if (DAT_00a7 < 0x6e) {
          cVar1 = -0x3c;
          goto LAB_afdd;
        }
        goto LAB_aff2;
      }
LAB_afeb:
      bVar7 = FUN_8000();
    }
    else {
      if (DAT_00a7 < DAT_bee4) goto LAB_afeb;
      if (DAT_00a7 < DAT_bee5) {
        cVar1 = -DAT_bee4;
LAB_afdd:
        if ((byte)((DAT_00a7 + cVar1) * '\x02') < 0x66) goto LAB_afeb;
      }
LAB_aff2:
      bVar7 = 0;
    }
    bVar3 = bVar7 + bVar6;
    if (CARRY1(bVar7,bVar6)) {
      bVar3 = 0xff;
    }
    _DAT_0022 = (ushort)bVar3 << 8;
    if (DAT_008c < DAT_bf86) {
      uVar2 = DAT_bf84;
      uVar4 = FUN_8025(0);
      _DAT_002d = CONCAT11(uVar4,uVar2);
    }
    bVar6 = DAT_00a3;
    if ((DAT_001f & 8) != 0) {
      DAT_00a3 = DAT_befb;
      bVar6 = DAT_00a3;
    }
  }
  else {
    _DAT_002d = 0;
    _DAT_0022 = 0;
    DAT_007c = DAT_007c + '\x01';
    if (DAT_007c == '\0') {
      DAT_007c = -1;
    }
    if ((DAT_001f & 2) == 0) {
      DAT_001f = DAT_001f | 2;
      DAT_007c = '\0';
      if ((DAT_bf85 <= DAT_000c) && (((TRCS & 0x40) == 0 || ((TRCS & 8) != 0)))) {
LAB_b078:
        bVar6 = DAT_000c < DAT_bf85;
        FUN_b096();
        if (!(bool)(bVar6 & 1)) {
LAB_b07f:
          DAT_001f = DAT_001f | 8;
          DAT_00a3 = DAT_bf90;
          if (DAT_bf98 <= DAT_008c) {
            DAT_00a3 = 0;
          }
          goto LAB_b107;
        }
      }
    }
    else {
      bVar7 = DAT_000c < DAT_bf85;
      if (!(bool)bVar7) {
        if ((DAT_001f & 8) == 0) {
          if ((((TRCS & 0x40) != 0) && ((TRCS & 8) != 0)) && ((DAT_001f & 4) == 0)) {
            DAT_001f = DAT_001f | 4;
            goto LAB_b078;
          }
          bVar6 = 0;
          FUN_b096();
          if ((bVar6 & 1) != 0) goto LAB_b021;
          goto LAB_b07f;
        }
        FUN_b096();
        bVar6 = DAT_bfde;
        if ((bVar7 & 1) == 0) {
          bVar7 = bVar7 & 0xf1;
          if (((TRCS & 0x40) == 0) || ((TRCS & 8) != 0)) {
            if (((TRCS & 0x10) == 0) || (FUN_b09b(), bVar6 = DAT_bfde, !(bool)(bVar7 & 1)))
            goto LAB_b107;
          }
          else {
            FUN_b096();
            bVar6 = DAT_bfdf;
            if ((bVar7 & 1) == 0) {
LAB_b107:
              if (DAT_00a3 == 0) {
                _DAT_0028 = 0;
                if (DAT_00bf < DAT_bfb6) {
                  DAT_00bf = DAT_00bf + 1;
                }
                DAT_0036 = DAT_0036 & 0xfd;
                goto LAB_b1a6;
              }
              if (DAT_00a3 < DAT_befa) {
                FUN_b12b();
                return;
              }
              DAT_0036 = DAT_0036 & 0xfd;
              if (DAT_00bf != 0) {
                DAT_00bf = DAT_00bf - 1;
              }
              if (DAT_0022 != '\0') {
                bVar6 = 0;
                cVar1 = FUN_801a();
                _DAT_0028 = CONCAT11(cVar1 + DAT_0028 + CARRY1(bVar6,DAT_0029),bVar6 + DAT_0029);
              }
              bVar6 = 0;
              cVar1 = FUN_8018();
              bVar7 = bVar6 + DAT_0029;
              cVar1 = cVar1 + DAT_0028 + CARRY1(bVar6,DAT_0029);
              _DAT_0028 = CONCAT11(cVar1,bVar7);
              if (P3SCR == '\0') {
                _DAT_0028 = CONCAT11((cVar1 - DAT_002d) - (bVar7 < DAT_002e),bVar7 - DAT_002e);
              }
              goto LAB_b16f;
            }
          }
        }
        goto LAB_b01b;
      }
    }
    DAT_00a3 = 0;
    bVar6 = DAT_00a3;
  }
LAB_b01b:
  DAT_00a3 = bVar6;
  DAT_001f = DAT_001f & 0xf7;
LAB_b021:
  if ((DAT_00c0 & 0x10) != 0) {
    FUN_b112();
    return;
  }
  if (DAT_00a3 == 0) {
    FUN_b132();
    return;
  }
  FUN_b12b();
  return;
}


// ---- FUN_b096 @ b096 ----

byte FUN_b096(void)

{
  char cVar1;
  
  cVar1 = FUN_80d2();
  if ((P3SCR <= (byte)-(cVar1 >> 7)) &&
     (((byte)-P3SCR != cVar1 >> 7 || (RMCR <= (byte)(cVar1 << 1))))) {
    return ~(cVar1 << 1);
  }
  return 0;
}


// ---- FUN_b09b @ b09b ----

byte FUN_b09b(char param_1)

{
  if ((P3SCR <= (byte)-(param_1 >> 7)) &&
     (((byte)-P3SCR != param_1 >> 7 || (RMCR <= (byte)(param_1 << 1))))) {
    return ~(param_1 << 1);
  }
  return 0;
}


// ---- FUN_b12b @ b12b ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b12b(void)

{
  char cVar1;
  byte bVar2;
  byte bVar3;
  
  DAT_0036 = DAT_0036 | 2;
  if (DAT_00bf != '\0') {
    DAT_00bf = DAT_00bf + -1;
  }
  if (DAT_0022 != '\0') {
    bVar2 = 0;
    cVar1 = FUN_801a();
    _DAT_0028 = CONCAT11(cVar1 + DAT_0028 + CARRY1(bVar2,DAT_0029),bVar2 + DAT_0029);
  }
  bVar2 = 0;
  cVar1 = FUN_8018();
  bVar3 = bVar2 + DAT_0029;
  cVar1 = cVar1 + DAT_0028 + CARRY1(bVar2,DAT_0029);
  _DAT_0028 = CONCAT11(cVar1,bVar3);
  if (P3SCR == '\0') {
    _DAT_0028 = CONCAT11((cVar1 - DAT_002d) - (bVar3 < DAT_002e),bVar3 - DAT_002e);
  }
  if (DAT_0026 != '\0') {
    bVar2 = 0;
    cVar1 = FUN_8018();
    _DAT_0028 = CONCAT11(cVar1 + DAT_0028 + CARRY1(bVar2,DAT_0029),bVar2 + DAT_0029);
  }
  if (_DAT_0028 == 0) {
    DAT_00b7 = DAT_00b7 | 0x80;
  }
  else {
    DAT_00b7 = DAT_00b7 & 0x7f;
  }
  bVar3 = 0;
  cVar1 = FUN_8018();
  bVar2 = cVar1 + DAT_0028 + CARRY1(bVar3,DAT_0029);
  _DAT_0028 = CONCAT11(bVar2,bVar3 + DAT_0029);
  if (0x3f < bVar2) {
    _DAT_0028 = 0x4000;
  }
  if ((DAT_00b5 < DAT_0020 || (byte)(DAT_00b5 - DAT_0020) < (DAT_00b6 < DAT_0021)) ||
     (0x3f < DAT_008c)) {
    _DAT_00b5 = _DAT_0020;
  }
  else {
    DAT_0057 = DAT_bf0b;
    if (((DAT_008c < 0x30) && (DAT_0057 = DAT_bf0a, DAT_008c < DAT_bfa8)) &&
       (DAT_0057 = DAT_bf08, DAT_bfa9 <= DAT_008c)) {
      DAT_0057 = DAT_bf09;
    }
    bVar2 = 0;
    _DAT_0052 = _DAT_0020;
    cVar1 = FUN_802b();
    _DAT_0052 = _DAT_00b5;
    FUN_802b(-DAT_0057,0);
    _DAT_00b5 = CONCAT11(cVar1 + DAT_0052 + CARRY1(bVar2,DAT_0053),bVar2 + DAT_0053);
  }
  FUN_941a();
  return;
}


// ---- FUN_b132 @ b132 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b132(void)

{
  char cVar1;
  byte bVar2;
  byte bVar3;
  
  DAT_0036 = DAT_0036 & 0xfd;
  if (DAT_00bf != '\0') {
    DAT_00bf = DAT_00bf + -1;
  }
  if (DAT_0022 != '\0') {
    bVar2 = 0;
    cVar1 = FUN_801a();
    _DAT_0028 = CONCAT11(cVar1 + DAT_0028 + CARRY1(bVar2,DAT_0029),bVar2 + DAT_0029);
  }
  bVar2 = 0;
  cVar1 = FUN_8018();
  bVar3 = bVar2 + DAT_0029;
  cVar1 = cVar1 + DAT_0028 + CARRY1(bVar2,DAT_0029);
  _DAT_0028 = CONCAT11(cVar1,bVar3);
  if (P3SCR == '\0') {
    _DAT_0028 = CONCAT11((cVar1 - DAT_002d) - (bVar3 < DAT_002e),bVar3 - DAT_002e);
  }
  if (DAT_0026 != '\0') {
    bVar2 = 0;
    cVar1 = FUN_8018();
    _DAT_0028 = CONCAT11(cVar1 + DAT_0028 + CARRY1(bVar2,DAT_0029),bVar2 + DAT_0029);
  }
  if (_DAT_0028 == 0) {
    DAT_00b7 = DAT_00b7 | 0x80;
  }
  else {
    DAT_00b7 = DAT_00b7 & 0x7f;
  }
  bVar3 = 0;
  cVar1 = FUN_8018();
  bVar2 = cVar1 + DAT_0028 + CARRY1(bVar3,DAT_0029);
  _DAT_0028 = CONCAT11(bVar2,bVar3 + DAT_0029);
  if (0x3f < bVar2) {
    _DAT_0028 = 0x4000;
  }
  if ((DAT_00b5 < DAT_0020 || (byte)(DAT_00b5 - DAT_0020) < (DAT_00b6 < DAT_0021)) ||
     (0x3f < DAT_008c)) {
    _DAT_00b5 = _DAT_0020;
  }
  else {
    DAT_0057 = DAT_bf0b;
    if (((DAT_008c < 0x30) && (DAT_0057 = DAT_bf0a, DAT_008c < DAT_bfa8)) &&
       (DAT_0057 = DAT_bf08, DAT_bfa9 <= DAT_008c)) {
      DAT_0057 = DAT_bf09;
    }
    bVar2 = 0;
    _DAT_0052 = _DAT_0020;
    cVar1 = FUN_802b();
    _DAT_0052 = _DAT_00b5;
    FUN_802b(-DAT_0057,0);
    _DAT_00b5 = CONCAT11(cVar1 + DAT_0052 + CARRY1(bVar2,DAT_0053),bVar2 + DAT_0053);
  }
  FUN_941a();
  return;
}


// ---- vec_SWI @ b200 ----

undefined1 vec_SWI(void)

{
  undefined1 in_stack_00000003;
  
  P1DDR = P1DDR | 0x20;
  return in_stack_00000003;
}


