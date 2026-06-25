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
  _DAT_0069 = _DAT_1482;
  sVar6 = _DAT_0069;
  cVar8 = '\x0f';
  DAT_0069 = (byte)((ushort)_DAT_1482 >> 8);
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
    if (bVar3 < _DAT_0076[0xf]) goto LAB_813c;
    bVar3 = _DAT_0076[0xf];
  }
  _DAT_0067 = (ushort)bVar3 << 2;
LAB_813c:
  _DAT_0074 = _DAT_0074 + 0xff;
  DAT_0072 = (char)((ushort)uVar1 >> 8);
  _DAT_006b = CONCAT11((char)((ushort)_DAT_0069 >> 8) - DAT_0072,(char)_DAT_0069);
  DAT_006d = 0;
  DAT_0073 = (char)uVar1;
  DAT_006e = DAT_0073 - DAT_0072;
  DAT_006f = 0;
  _DAT_0072 = uVar1;
  FUN_827b();
  sVar6 = _DAT_0067 + (ushort)DAT_0070 * -4;
  _DAT_006b = sVar6 * 4;
  DAT_006d = (char)((char)sVar6 << 7) >> 1;
  DAT_006f = DAT_0071 - DAT_0070;
  DAT_006e = 0;
  DAT_0072 = extraout_B;
  FUN_827b();
  DAT_0073 = extraout_B_00;
  do {
    *(char *)((short)register0x12 + -1) = -0x7f;
    *(char *)((short)register0x12 + 0x10000) = -0x7d;
    FUN_81f9();
    uVar7 = CONCAT11(DAT_0075 - DAT_0074,DAT_0072);
    if (DAT_0075 < DAT_0074) {
      bVar3 = -(DAT_0075 - DAT_0074);
      bVar4 = -DAT_0072;
      uVar7 = CONCAT11(bVar3,bVar4);
      if (bVar4 == 0) goto LAB_818c;
      sVar6 = (ushort)bVar3 * (ushort)bVar4;
      if ((char)sVar6 < '\0') {
        sVar6 = (ushort)(byte)((char)((ushort)sVar6 >> 8) + 1) << 8;
      }
      bVar3 = (char)((ushort)sVar6 >> 8) + DAT_0075;
    }
    else {
LAB_818c:
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
      if (bVar5 == 0) goto LAB_81ad;
      sVar6 = (ushort)bVar4 * (ushort)bVar5;
      if ((char)sVar6 < '\0') {
        sVar6 = (ushort)(byte)((char)((ushort)sVar6 >> 8) + 1) << 8;
      }
      bVar4 = (char)((ushort)sVar6 >> 8) + DAT_0077;
    }
    else {
LAB_81ad:
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
      if (bVar9 == 0) goto LAB_81cd;
      sVar6 = (ushort)bVar5 * (ushort)bVar9;
      if ((char)sVar6 < '\0') {
        sVar6 = (ushort)(byte)((char)((ushort)sVar6 >> 8) + 1) << 8;
      }
      cVar8 = (char)((ushort)sVar6 >> 8) + bVar4;
    }
    else {
LAB_81cd:
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


// ---- FUN_80d9 @ 80d9 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_80d9(void)

{
  undefined2 uVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  char cVar7;
  char extraout_B;
  short sVar5;
  char extraout_B_00;
  ushort uVar6;
  byte bVar8;
  byte *pbVar9;
  
  cVar7 = '\x0f';
  pbVar9 = _DAT_0078;
  do {
    if (DAT_0069 < pbVar9[1]) break;
    pbVar9 = pbVar9 + 1;
    cVar7 = cVar7 + -1;
  } while (cVar7 != '\0');
  uVar1 = *(undefined2 *)pbVar9;
  bVar2 = *_DAT_0078;
  if ((DAT_0069 < bVar2) || (bVar2 = _DAT_0078[0xf], bVar2 <= DAT_0069)) {
    _DAT_0069 = (ushort)bVar2 << 8;
  }
  cVar7 = '\x0f';
  pbVar9 = _DAT_0076;
  do {
    if ((byte)(_DAT_0067 << 2) < pbVar9[1]) break;
    pbVar9 = pbVar9 + 1;
    cVar7 = cVar7 + -1;
  } while (cVar7 != '\0');
  DAT_007a = 0xff;
  _DAT_0070 = *(undefined2 *)pbVar9;
  bVar2 = (byte)(_DAT_0067 << 2);
  if (bVar2 < *_DAT_0076) {
    bVar2 = *_DAT_0076;
  }
  else {
    if (bVar2 < _DAT_0076[0xf]) goto LAB_813c;
    bVar2 = _DAT_0076[0xf];
  }
  _DAT_0067 = (ushort)bVar2 << 2;
LAB_813c:
  _DAT_0074 = _DAT_0074 + 0xff;
  DAT_0072 = (char)((ushort)uVar1 >> 8);
  _DAT_006b = CONCAT11((char)((ushort)_DAT_0069 >> 8) - DAT_0072,(char)_DAT_0069);
  DAT_006d = 0;
  DAT_0073 = (char)uVar1;
  DAT_006e = DAT_0073 - DAT_0072;
  DAT_006f = 0;
  _DAT_0072 = uVar1;
  FUN_827b();
  sVar5 = _DAT_0067 + (ushort)DAT_0070 * -4;
  _DAT_006b = sVar5 * 4;
  DAT_006d = (char)((char)sVar5 << 7) >> 1;
  DAT_006f = DAT_0071 - DAT_0070;
  DAT_006e = 0;
  DAT_0072 = extraout_B;
  FUN_827b();
  DAT_0073 = extraout_B_00;
  do {
    *(char *)((short)register0x12 + -1) = -0x7f;
    *(char *)((short)register0x12 + 0x10000) = -0x7d;
    FUN_81f9();
    uVar6 = CONCAT11(DAT_0075 - DAT_0074,DAT_0072);
    if (DAT_0075 < DAT_0074) {
      bVar2 = -(DAT_0075 - DAT_0074);
      bVar3 = -DAT_0072;
      uVar6 = CONCAT11(bVar2,bVar3);
      if (bVar3 == 0) goto LAB_818c;
      sVar5 = (ushort)bVar2 * (ushort)bVar3;
      if ((char)sVar5 < '\0') {
        sVar5 = (ushort)(byte)((char)((ushort)sVar5 >> 8) + 1) << 8;
      }
      bVar2 = (char)((ushort)sVar5 >> 8) + DAT_0075;
    }
    else {
LAB_818c:
      sVar5 = (uVar6 >> 8) * (uVar6 & 0xff);
      if ((char)sVar5 < '\0') {
        sVar5 = (ushort)(byte)((char)((ushort)sVar5 >> 8) + 1) << 8;
      }
      bVar2 = (char)((ushort)sVar5 >> 8) + DAT_0074;
    }
    uVar6 = CONCAT11(DAT_0077 - DAT_0076,DAT_0072);
    if (DAT_0077 < DAT_0076) {
      bVar3 = -(DAT_0077 - DAT_0076);
      bVar4 = -DAT_0072;
      uVar6 = CONCAT11(bVar3,bVar4);
      if (bVar4 == 0) goto LAB_81ad;
      sVar5 = (ushort)bVar3 * (ushort)bVar4;
      if ((char)sVar5 < '\0') {
        sVar5 = (ushort)(byte)((char)((ushort)sVar5 >> 8) + 1) << 8;
      }
      bVar3 = (char)((ushort)sVar5 >> 8) + DAT_0077;
    }
    else {
LAB_81ad:
      sVar5 = (uVar6 >> 8) * (uVar6 & 0xff);
      if ((char)sVar5 < '\0') {
        sVar5 = (ushort)(byte)((char)((ushort)sVar5 >> 8) + 1) << 8;
      }
      bVar3 = (char)((ushort)sVar5 >> 8) + DAT_0076;
    }
    _DAT_0078 = (byte *)CONCAT11(bVar2,bVar3);
    uVar6 = CONCAT11(bVar3 - bVar2,DAT_0073);
    if (bVar3 < bVar2) {
      bVar4 = -(bVar3 - bVar2);
      bVar8 = -DAT_0073;
      uVar6 = CONCAT11(bVar4,bVar8);
      if (bVar8 == 0) goto LAB_81cd;
      sVar5 = (ushort)bVar4 * (ushort)bVar8;
      if ((char)sVar5 < '\0') {
        sVar5 = (ushort)(byte)((char)((ushort)sVar5 >> 8) + 1) << 8;
      }
      cVar7 = (char)((ushort)sVar5 >> 8) + bVar3;
    }
    else {
LAB_81cd:
      sVar5 = (uVar6 >> 8) * (uVar6 & 0xff);
      if ((char)sVar5 < '\0') {
        sVar5 = (ushort)(byte)((char)((ushort)sVar5 >> 8) + 1) << 8;
      }
      cVar7 = (char)((ushort)sVar5 >> 8) + bVar2;
    }
    if ((DAT_007d & 0x40) == 0) {
      return;
    }
    if ((DAT_007d & 0x20) != 0) {
      DAT_007d = DAT_007d & 0xdf;
      return;
    }
    DAT_007d = DAT_007d | 0x20;
    *(char *)register0x12 = cVar7;
    register0x12 = (BADSPACEBASE *)((short)register0x12 + -1);
  } while( true );
}


// ---- FUN_81f9 @ 81f9 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_81f9(undefined1 param_1,undefined1 param_2,byte *param_3)

{
  byte bVar1;
  byte bVar2;
  
  if ((DAT_007d & 0x40) == 0) {
    if ((DAT_007d & 0x10) != 0) {
      bVar1 = *param_3;
      if ((char)bVar1 < '\0') {
        bVar1 = bVar1 & 0x7f;
        DAT_0093 = DAT_0093 | 1;
      }
      else {
        DAT_0093 = DAT_0093 & 0xfe;
      }
      _DAT_0074 = CONCAT11(bVar1,param_3[1]) & 0xff7f;
      _DAT_0076 = *(ushort *)(param_3 + 0x10) & 0x7f7f;
      return;
    }
    _DAT_0074 = *(undefined2 *)param_3;
    _DAT_0076 = *(undefined2 *)(param_3 + 0x10);
    return;
  }
  if ((DAT_007d & 0x20) != 0) {
    bVar1 = *param_3;
    if (-1 < (char)bVar1) {
      bVar1 = 0x40;
    }
    bVar2 = param_3[1];
    if (-1 < (char)bVar2) {
      bVar2 = 0x40;
    }
    _DAT_0074 = CONCAT11(bVar1,bVar2) & 0x7f7f;
    bVar1 = param_3[0x10];
    if (-1 < (char)bVar1) {
      bVar1 = 0x40;
    }
    bVar2 = param_3[0x11];
    if (-1 < (char)bVar2) {
      bVar2 = 0x40;
    }
    _DAT_0076 = CONCAT11(bVar1,bVar2) & 0x7f7f;
    return;
  }
  bVar1 = *param_3;
  if ((char)bVar1 < '\0') {
    bVar1 = 0;
  }
  bVar2 = param_3[1];
  if ((char)bVar2 < '\0') {
    bVar2 = 0;
  }
  _DAT_0074 = CONCAT11(bVar1,bVar2);
  bVar1 = param_3[0x10];
  if ((char)bVar1 < '\0') {
    bVar1 = 0;
  }
  bVar2 = param_3[0x11];
  if ((char)bVar2 < '\0') {
    bVar2 = 0;
  }
  _DAT_0076 = CONCAT11(bVar1,bVar2);
  return;
}


// ---- FUN_827b @ 827b ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_827b(void)

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
          if (_DAT_006e <= uVar3) goto LAB_82b1;
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
              goto LAB_8297;
            }
            uVar3 = CONCAT11((char)((ushort)sVar2 >> 8) << 1 | (byte)sVar2 >> 7,
                             (byte)sVar2 << 1 | bVar1);
            if (-1 < sVar2) break;
            sVar2 = uVar3 - _DAT_006e;
LAB_82b1:
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
LAB_8297:
    uVar4 = 0xff;
  }
  DAT_006d = uVar4;
  return;
}


// ---- FUN_82b9 @ 82b9 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_82b9(void)

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


// ---- vec_IRQ @ 82ca ----

undefined1 vec_IRQ(void)

{
  undefined1 in_stack_00000003;
  
  DAT_1034 = ~DAT_102e;
  DAT_0052 = DAT_102e;
  if ((DAT_102e & 0x80) != 0) {
    DAT_0054 = DAT_0054 | 8;
    FUN_838d();
  }
  if (((DAT_0052 & 4) != 0) && ((DAT_0054 & 8) != 0)) {
    FUN_844a();
  }
  if ((DAT_0052 & 8) != 0) {
    FUN_8543();
  }
  if ((DAT_0054 & 0x80) != 0) {
    return in_stack_00000003;
  }
  do {
    if ((DAT_0054 & 0x20) == 0) {
      if ((DAT_0054 & 0x40) == 0) {
        if ((DAT_0054 & 0x10) == 0) {
          if ((DAT_0055 & 0x80) == 0) {
            return in_stack_00000003;
          }
          DAT_0054 = DAT_0054 | 0x80;
          DAT_0055 = DAT_0055 & 0x7f;
          FUN_99e1();
          FUN_99f7();
          FUN_9b5a();
          FUN_9cdc();
          FUN_9e60();
          FUN_afac();
          FUN_a04d();
          FUN_a1cc();
          FUN_a01d();
          FUN_a422();
          DAT_144a = DAT_0053;
        }
        else {
          DAT_0054 = DAT_0054 & 0xef | 0x80;
          FUN_94d2();
          FUN_957a();
        }
      }
      else {
        DAT_0054 = DAT_0054 & 0xbf | 0x80;
        FUN_85fb();
        FUN_894e();
        FUN_8a54();
        FUN_8be1();
        FUN_8c23();
        FUN_8c75();
        FUN_8cac();
        FUN_8cfa();
        FUN_91d7();
        FUN_8e17();
        FUN_918b();
        FUN_91b1();
        FUN_a9f4();
      }
    }
    else {
      DAT_0054 = DAT_0054 & 0xdf | 0x80;
      FUN_858e();
    }
    DAT_0054 = DAT_0054 & 0x7f;
  } while( true );
}


// ---- FUN_838d @ 838d ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_838d(void)

{
  _DAT_105a = (ushort)DAT_140f;
  DAT_1410 = DAT_140f;
  _DAT_105c = (ushort)DAT_143a;
  if ((DAT_004f & 0x20) == 0) {
    if (DAT_004b == '\x02') {
      DAT_00c0 = DAT_00c0 & 0xfe;
      DAT_00c0 = DAT_00c0 | 2;
    }
    else {
      if (DAT_004b != '\x05') goto LAB_83ff;
      DAT_00c0 = DAT_00c0 & 0xfd;
      DAT_00c0 = DAT_00c0 | 1;
    }
  }
  else {
    if ((DAT_004b != '\x05') && (DAT_004b != '\x02')) {
LAB_83ff:
      DAT_00c0 = DAT_00c0 & 0xfc;
      goto LAB_83f6;
    }
    DAT_00c0 = DAT_00c0 | 3;
    if ((DAT_00be & 0x20) == 0) {
      DAT_00c0 = DAT_14db ^ 3;
      goto LAB_83f6;
    }
  }
  if ((DAT_0054 & 2) == 0) {
    if ((DAT_1533 & 3) != 0) {
      if ((DAT_1533 & 1) == 0) {
        DAT_00c0 = DAT_00c0 & 0xfd;
      }
      else {
        DAT_00c0 = DAT_00c0 & 0xfe;
      }
    }
  }
  else {
    DAT_00c0 = DAT_00c0 & 0xfe;
  }
LAB_83f6:
  DAT_14db = DAT_00c0;
  DAT_00be = DAT_004f;
  DAT_0056 = 0;
  DAT_0040 = DAT_0040 & 0xfb;
  if (((DAT_0054 & 4) != 0) && (DAT_1010 = 0xc1, (DAT_0054 & 1) != 0)) {
    DAT_1010 = 0xc0;
  }
  DAT_14cc = DAT_14cb;
  _DAT_1465 = _DAT_1068;
  if ((((DAT_0053 & 2) == 0) && (0x1f < DAT_1442)) && ((0x7c < _DAT_1068 || (_DAT_1068 < 0x73)))) {
    DAT_0047 = DAT_0047 | 8;
    DAT_00d5 = DAT_00d5 | 0x80;
  }
  _DAT_14e1 = _DAT_1068;
  return;
}


// ---- FUN_844a @ 844a ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_844a(void)

{
  char cVar1;
  byte bVar2;
  ushort uVar3;
  
  cVar1 = DAT_14ef;
  DAT_004b = DAT_004b + 1;
  if ((((DAT_ffd3 & 0x10) != 0) && (DAT_14c8 != 0xff)) && ((DAT_0017 & 4) != 0)) {
    DAT_14c8 = DAT_14c8 + 8;
    if ((DAT_14c8 & 0x80) == 0) {
      if (DAT_14c8 < 0x18) {
        DAT_004b = DAT_fef9;
        DAT_14c8 = DAT_14c8 & 0x78 | DAT_fef9;
      }
      else {
        DAT_14c8 = DAT_14c8 | 0x80;
      }
    }
    uVar3 = CONCAT11(DAT_14c8,DAT_14c8) & 0xff07;
    bVar2 = (byte)(uVar3 >> 8);
    if ((byte)uVar3 == DAT_004b) {
      if (0x27 < (bVar2 & 0x78)) {
        DAT_14c8 = 0xff;
        DAT_004b = DAT_fef9;
      }
    }
    else {
      DAT_14c8 = bVar2 & 0x80 | DAT_004b;
    }
  }
  if (5 < DAT_004b) {
    DAT_004b = 0;
  }
  if (((DAT_004b != 2) && (DAT_004b != 5)) || (DAT_0054 = DAT_0054 | 0x10, DAT_0054 == 0)) {
    if ((DAT_0054 & 1) != 0) {
      _DAT_004d = 0;
    }
    if (((DAT_0091 & 4) == 0) || (DAT_0091 = DAT_0091 & 0xfb, _DAT_1042 == 0)) {
      if ((DAT_00c0 & 1) != 0) {
        _DAT_1042 = 0;
        _DAT_1058 = _DAT_004d;
      }
      if ((DAT_00c0 & 2) != 0) {
        _DAT_1044 = 0;
        _DAT_106e = _DAT_004d;
      }
      _DAT_14de = _DAT_004d;
      DAT_1036 = DAT_00c0 & 0xfc;
    }
    else {
      if ((DAT_00c0 & 1) != 0) {
        _DAT_1058 = _DAT_004d + _DAT_1058;
      }
      if ((DAT_00c0 & 2) != 0) {
        _DAT_106e = _DAT_004d + _DAT_106e;
      }
    }
  }
  DAT_007f = (DAT_0017 & 0x10) != 0;
  DAT_14ef = cVar1;
  if (!DAT_007f) {
    DAT_0080 = DAT_0080 + '\x01';
    DAT_14ef = DAT_14ef + '\x01';
    if (DAT_14ef == '\0') {
      DAT_14ef = cVar1;
    }
  }
  if ((DAT_0054 & 4) == 0) {
    DAT_0054 = DAT_0054 | 4;
    DAT_0051 = 0;
  }
  return;
}


// ---- FUN_8543 @ 8543 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8543(void)

{
  DAT_0057 = DAT_0057 + 2 ^ 1;
  if (9 < DAT_0057) {
    DAT_0057 = DAT_0057 & 1;
    DAT_0054 = DAT_0054 | 0x40;
  }
  if ((DAT_0057 & 1) != 0) {
    DAT_0054 = DAT_0054 | 0x20;
  }
  if ((DAT_0057 & 0xe) == 4) {
    DAT_0055 = DAT_0055 | 0x80;
  }
  if ((DAT_1002 & 0x20) != DAT_14bd) {
    DAT_14bc = DAT_14bc + '\x01';
  }
  DAT_14bd = DAT_1002 & 0x20;
  _DAT_14ba = _DAT_14ba + 1;
  if (0x158 < _DAT_14ba) {
    DAT_1407 = DAT_14bc;
    DAT_14bc = '\0';
    _DAT_14ba = 0;
  }
  return;
}


// ---- FUN_858e @ 858e ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_858e(void)

{
  undefined1 uVar1;
  char cVar2;
  undefined1 extraout_B;
  short sVar3;
  undefined1 extraout_B_00;
  
  uVar1 = FUN_b565();
  _DAT_1408 = CONCAT11(uVar1,extraout_B);
  if (((((DAT_0053 & 2) == 0) && (_DAT_1408 < 100)) && (_DAT_1408 = 100, (DAT_0054 & 8) != 0)) &&
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
      if ((byte)(sVar3 << 2) < 0x14) goto LAB_85e0;
    }
    DAT_0047 = DAT_0047 | 2;
    DAT_00d5 = DAT_00d5 | 0x40;
  }
LAB_85e0:
  _DAT_14e5 = _DAT_1408;
  uVar1 = FUN_802c();
  sVar3 = CONCAT11(uVar1,extraout_B_00) + _DAT_144b;
  cVar2 = (char)((ushort)sVar3 >> 8);
  _DAT_144b = CONCAT11(cVar2 >> 1 | CARRY2(CONCAT11(uVar1,extraout_B_00),_DAT_144b) << 7,
                       (char)sVar3 >> 1 | cVar2 << 7);
  return;
}


// ---- FUN_85fb @ 85fb ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_85fb(void)

{
  byte bVar1;
  byte bVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined1 uVar5;
  undefined1 uVar6;
  byte bVar7;
  char cVar8;
  char extraout_B;
  short sVar9;
  byte bVar11;
  byte extraout_B_00;
  byte bVar12;
  ushort uVar10;
  
  uVar6 = FUN_b565();
  DAT_152c = DAT_152b;
  uVar5 = DAT_1529;
  sVar9 = CONCAT11(uVar6,extraout_B) << 1;
  _DAT_1492 = sVar9;
  sVar9 = _DAT_1492;
  bVar11 = extraout_B * '\x04';
  if ((DAT_00b5 & 1) == 0) {
    _DAT_1494 = CONCAT22(CONCAT11(bVar11,bVar11),CONCAT11(bVar11,bVar11));
    DAT_00b5 = DAT_00b5 | 1;
    DAT_151b = bVar11;
    DAT_151c = bVar11;
    DAT_151d = bVar11;
    DAT_151e = bVar11;
    DAT_151f = bVar11;
    DAT_1520 = bVar11;
    DAT_1521 = bVar11;
  }
  bVar1 = DAT_1520;
  bVar7 = DAT_151e;
  bVar12 = DAT_151c;
  uVar3 = _DAT_1494;
  _DAT_1494 = CONCAT22(CONCAT11(bVar11,DAT_1494),_DAT_1495);
  uVar4 = _DAT_1494;
  DAT_152b = DAT_152a;
  DAT_1529 = DAT_1528;
  DAT_152a = uVar5;
  DAT_1528 = DAT_14bf;
  DAT_1493 = (byte)sVar9;
  DAT_1492 = (char)((ushort)sVar9 >> 8);
  if ((DAT_0053 & 2) == 0) {
    if ((2 < bVar11) && (bVar11 < 0xf2)) {
      DAT_00cb = DAT_00cb & 0xdf;
      goto LAB_866f;
    }
    DAT_00c6 = DAT_00c6 | 0x20;
    DAT_00cb = DAT_00cb | 0x20;
    DAT_00d8 = DAT_00d8 | 0x20;
    DAT_1662 = 0;
    DAT_1498 = 0xff;
    DAT_1671 = 0xff;
    cVar8 = DAT_f87e;
  }
  else {
LAB_866f:
    if ((((DAT_1492 == '\0') && (DAT_1493 < DAT_1498)) && (0x95 < (byte)(DAT_1499 + 1U))) &&
       (DAT_1498 = 0, DAT_1671 != 0)) {
      DAT_1671 = 0;
    }
    if ((((DAT_0053 & 4) != 0) && (0x27 < DAT_1442)) && ((DAT_1442 < 0x58 && (0x7c < DAT_140c)))) {
      DAT_1671 = DAT_1498;
    }
    cVar8 = bVar11 - (DAT_1498 >> 1);
    if (bVar11 < DAT_1498 >> 1) {
      cVar8 = '\0';
    }
  }
  DAT_1499 = 0;
  if ((DAT_00b5 & 0x80) == 0) {
    _DAT_1541 = CONCAT12(cVar8,CONCAT11(cVar8,cVar8));
    DAT_00b5 = DAT_00b5 | 0x80;
    DAT_149a = cVar8;
    _DAT_158d = CONCAT11(cVar8,cVar8);
  }
  bVar2 = DAT_00b5;
  _DAT_1541 = CONCAT12(DAT_149a,_DAT_1541);
  DAT_149a = cVar8;
  if ((DAT_004a & 0xf) == 0) {
    _DAT_158d = CONCAT11(cVar8,DAT_158d);
  }
  DAT_14b2 = DAT_1493;
  if (DAT_1492 != '\0') {
    DAT_14b2 = 0xff;
  }
  DAT_1497 = (byte)((uint)uVar3 >> 8);
  if (bVar11 < DAT_1497) {
    DAT_149b = 0;
    DAT_14b9 = -(bVar11 - DAT_1497);
  }
  DAT_149c = 0x80;
  DAT_1523 = DAT_1523 + 1;
  if (4 < DAT_1523) {
    DAT_1523 = 0;
    DAT_1520 = DAT_151f;
    DAT_1521 = bVar1;
    DAT_151e = DAT_151d;
    DAT_151f = bVar7;
    DAT_151c = DAT_151b;
    DAT_151d = bVar12;
    bVar7 = bVar11 - bVar12;
    if (bVar11 < bVar12) {
      DAT_149b = 0;
      if (bVar7 < 0x80) {
        bVar7 = 0x80;
      }
    }
    else {
      DAT_14b9 = 0;
      DAT_149b = bVar7;
      if (0x7f < bVar7) {
        bVar7 = 0x7f;
      }
    }
    DAT_1522 = bVar7 + 0x80;
    DAT_151b = bVar11;
  }
  if ((DAT_0054 & 8) == 0) {
    _DAT_1514 = 0;
    _DAT_1517 = 0;
    DAT_1513 = 0;
    DAT_1516 = 0;
    DAT_00b5 = DAT_00b5 & 0xf9;
    _DAT_1492 = sVar9;
    _DAT_1494 = uVar4;
    return;
  }
  if ((DAT_0053 & 1) != 0) {
    _DAT_1514 = 0;
    DAT_1513 = 0;
  }
  _DAT_1494 = uVar4;
  if (DAT_f93d <= DAT_149b) {
    if (DAT_1523 == 0) {
      DAT_1516 = 0;
      _DAT_1517 = 0;
      DAT_00b5 = DAT_00b5 & 0xfd;
      if ((bVar2 & 4) == 0) {
        DAT_14c3 = 0;
        DAT_00b5 = DAT_00b5 | 4;
        DAT_14bf = cVar8;
      }
      if (DAT_14c3 <= DAT_149b) {
        DAT_14c3 = DAT_149b;
        DAT_150e = FUN_809f();
        if (((DAT_150e == 0) || (DAT_1512 = FUN_809f(), DAT_1512 == '\0')) ||
           ((DAT_150f = FUN_809f(), DAT_150f == 0 || (DAT_1531 = FUN_809f(), DAT_1531 == '\0')))) {
          uVar10 = 0;
        }
        else {
          _DAT_005b = CONCAT21((ushort)DAT_150f * (ushort)DAT_150e,DAT_005d);
          bVar11 = FUN_8001();
          if (bVar11 < 0x10) {
            sVar9 = 4;
            bVar12 = extraout_B_00;
            do {
              bVar1 = DAT_005d >> 7;
              DAT_005d = DAT_005d << 1;
              _DAT_005b = (uint3)DAT_005d;
              bVar7 = bVar12 >> 7;
              bVar12 = bVar12 << 1 | bVar1;
              bVar11 = bVar11 << 1 | bVar7;
              sVar9 = sVar9 + -1;
            } while (sVar9 != 0);
          }
          else {
            bVar12 = 0xff;
            bVar11 = 0xff;
          }
          _DAT_005c = CONCAT11(bVar12,DAT_005d);
          _DAT_005b = CONCAT12(bVar11,_DAT_005c);
          cVar8 = FUN_8001();
          if ((cVar8 != '\0') || (uVar10 = _DAT_005c, 0x3f < (byte)(_DAT_005b >> 8))) {
            uVar10 = 0x4000;
          }
        }
        if (_DAT_1514 < uVar10) {
          _DAT_1514 = uVar10;
        }
        DAT_1513 = (undefined1)((_DAT_1514 << 2) >> 8);
        if ((short)(_DAT_1514 << 1) < 0) {
          DAT_1513 = 0xff;
        }
      }
      return;
    }
    goto LAB_8942;
  }
  DAT_00b5 = DAT_00b5 & 0xfb;
  if (DAT_1460 < DAT_f93f) {
    DAT_1516 = 0;
    _DAT_1517 = 0;
  }
  if (DAT_14b9 < DAT_f93e) {
    DAT_00b5 = bVar2 & 0xf9;
    goto LAB_8942;
  }
  DAT_1513 = 0;
  _DAT_1514 = 0;
  if ((bVar2 & 2) == 0) {
    DAT_14c3 = 0;
    DAT_00b5 = DAT_00b5 | 2;
    DAT_14bf = cVar8;
  }
  if (DAT_1460 < DAT_f93f) {
    DAT_1516 = 0;
    _DAT_1517 = 0;
    goto LAB_8942;
  }
  if (DAT_14b9 < DAT_14c3) goto LAB_8942;
  DAT_14c3 = DAT_14b9;
  DAT_1510 = FUN_809f();
  if (DAT_1510 == 0) goto LAB_892a;
  if (DAT_1453 < 0x41) {
    if (DAT_140c < DAT_f785) goto LAB_88e5;
LAB_88ec:
    DAT_1512 = FUN_809f();
    if (DAT_1512 == '\0') {
LAB_892a:
      uVar10 = 0;
    }
    else {
      DAT_1511 = FUN_809f();
      if (DAT_1511 == 0) goto LAB_892a;
      _DAT_005b = CONCAT21((ushort)DAT_1511 * (ushort)DAT_1510,DAT_005d);
      FUN_8001();
      if ((((bool)((byte)(_DAT_005b >> 8) >> 7)) ||
          (uVar10 = _DAT_005c << 2, SUB21((_DAT_005c << 1) >> 0xf,0))) ||
         (0xf < (byte)(uVar10 >> 8))) {
        uVar10 = 0x1000;
      }
    }
    if (_DAT_1517 < uVar10) {
      _DAT_1517 = uVar10;
    }
  }
  else {
    if (DAT_f784 <= DAT_140c) goto LAB_88ec;
LAB_88e5:
    _DAT_1517 = 0;
  }
  DAT_1516 = (undefined1)((_DAT_1517 << 2) >> 8);
LAB_8942:
  if ((DAT_00b5 & 6) == 0) {
    DAT_14bf = DAT_149a;
  }
  return;
}


// ---- FUN_894e @ 894e ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_894e(void)

{
  char cVar1;
  char extraout_B;
  short sVar2;
  ushort uVar3;
  undefined2 *puVar4;
  undefined2 *puVar5;
  short *psVar6;
  
  _DAT_005b = -0x5955;
  cVar1 = FUN_8001();
  _DAT_158b = CONCAT11(cVar1,extraout_B);
  if ((DAT_0090 & 0x10) == 0) {
    _DAT_158b = _DAT_1589;
    _DAT_1589 = _DAT_1587;
    _DAT_1587 = _DAT_1585;
    _DAT_1585 = _DAT_1583;
    _DAT_1583 = _DAT_140a;
  }
  else {
    sVar2 = _DAT_158b << 2;
    if ((char)((ushort)sVar2 >> 8) != '\0') {
      sVar2 = 0xff;
    }
    DAT_1582 = (char)sVar2;
    DAT_0090 = DAT_0090 | 0x10;
    _DAT_1583 = _DAT_158b;
    _DAT_1585 = _DAT_158b;
    _DAT_1587 = _DAT_158b;
    _DAT_1589 = _DAT_158b;
  }
  _DAT_140a = CONCAT11(cVar1,extraout_B);
  uVar3 = _DAT_140a;
  if (cVar1 != '\0') {
    uVar3 = 0xff;
  }
  DAT_1442 = (undefined1)uVar3;
  DAT_1460 = extraout_B << 2;
  if ((DAT_004a & 0xf) == 0) {
    DAT_1582 = DAT_1581;
    DAT_1581 = DAT_1460;
  }
  sVar2 = _DAT_140a << 1;
  if ((char)((ushort)sVar2 >> 8) != '\0') {
    sVar2 = 0xff;
  }
  DAT_1544 = (undefined1)sVar2;
  if ((DAT_0090 & 0x40) != 0) {
    puVar4 = (undefined2 *)&DAT_1577;
    do {
      puVar5 = puVar4 + -1;
      *puVar4 = *puVar5;
      puVar4 = puVar5;
    } while (&DAT_1563 < puVar5);
  }
  sVar2 = _DAT_140a * 8;
  if ((DAT_0090 & 0x40) == 0) {
    DAT_0090 = DAT_0090 | 0x40;
    psVar6 = (short *)&DAT_1561;
    do {
      psVar6 = psVar6 + 1;
      *psVar6 = sVar2;
    } while (psVar6 < &DAT_1577);
  }
  else {
    _DAT_1563 = (sVar2 + _DAT_1563) * 2;
  }
  if ((DAT_0053 & 1) == 0) {
    _DAT_1455 = _DAT_140a << 3;
  }
  else {
    _DAT_005b = _DAT_1455 * 8;
    _DAT_1455 = _DAT_1455 * -7 + _DAT_140a;
  }
  if ((((DAT_0053 & 2) == 0) && (0x1f < _DAT_14e3)) &&
     ((_DAT_14e3 * 6 < _DAT_140a || (_DAT_140a <= _DAT_14e3 << 1)))) {
    DAT_0047 = DAT_0047 | 8;
    DAT_00d5 = DAT_00d5 | 0x80;
  }
  _DAT_14e3 = _DAT_140a;
  return;
}


// ---- FUN_8a54 @ 8a54 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8a54(void)

{
  undefined1 uVar1;
  byte bVar2;
  undefined1 extraout_B;
  byte *pbVar3;
  
  bVar2 = DAT_14d1;
  DAT_14d1 = bVar2;
  if (((DAT_004a & 0xf) == 0) && (DAT_14d1 = DAT_14d1 + 1, DAT_14d1 == 0)) {
    DAT_14d1 = bVar2;
  }
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
    if (DAT_f86e <= DAT_1460) {
      _DAT_1413 = 0;
      return;
    }
    for (pbVar3 = &DAT_f869; (*pbVar3 <= DAT_1494 && (pbVar3 < (byte *)0xf86b)); pbVar3 = pbVar3 + 1
        ) {
    }
    _DAT_1413 = (ushort)bRAMf85d << 8;
  }
  _DAT_150c = _DAT_1413;
  bVar2 = FUN_809f();
  if (bVar2 < DAT_150c) {
    if (DAT_f9fa <= DAT_14d1) {
      DAT_00b5 = DAT_00b5 | 0x10;
      _DAT_1413 = 0;
      return;
    }
  }
  else {
    DAT_14d1 = 0;
    DAT_00b5 = DAT_00b5 & 0xef;
  }
  DAT_14d3 = (byte)(_DAT_1413 - _DAT_1484 >> 8);
  if (_DAT_1413 < _DAT_1484) {
    if (DAT_14d3 < 0x80) {
      DAT_14d3 = 0x80;
    }
  }
  else if (0x7f < DAT_14d3) {
    DAT_14d3 = 0x7f;
  }
  _DAT_1484 = _DAT_1413;
  bVar2 = FUN_809f();
  if (_DAT_1413 <= (ushort)bVar2 << 8) {
    _DAT_1413 = (ushort)bVar2 << 8;
  }
  if (((DAT_0053 & 2) == 0) && (DAT_f886 <= DAT_1477)) {
    if (DAT_14da == 0) {
      if ((DAT_14fa == 1) && (DAT_f7be <= DAT_1460)) {
        DAT_14fa = 0xff;
      }
      if (DAT_14fa < DAT_ffb2) {
        DAT_14b8 = FUN_809f();
        DAT_1536 = DAT_14b8;
        goto LAB_8b8e;
      }
    }
    else if (DAT_14da < DAT_ffb0) {
      DAT_14b8 = FUN_809f();
      goto LAB_8b8e;
    }
  }
  DAT_14b8 = 0x40;
LAB_8b8e:
  DAT_14b7 = FUN_809f();
  if ((byte)((ushort)DAT_14b7 * (ushort)DAT_14b8 >> 8) < 0x40) {
    _DAT_14b5 = (ushort)DAT_14b7 * (ushort)DAT_14b8 * 4;
  }
  else {
    _DAT_14b5 = 0xffff;
  }
  DAT_0059 = DAT_0059 & 0xfe;
  if (_DAT_14b5 < _DAT_1413) {
    DAT_0059 = DAT_0059 | 1;
    _DAT_1413 = _DAT_14b5;
  }
  bVar2 = DAT_140c;
  if ((DAT_0051 & 2) == 0) {
    bVar2 = DAT_140c + 5;
  }
  if (bVar2 < DAT_ffd2) {
    DAT_0051 = DAT_0051 | 2;
  }
  else {
    DAT_0051 = DAT_0051 & 0xfd;
    bVar2 = DAT_14d3;
    if ((char)DAT_14d3 < '\0') {
      bVar2 = -DAT_14d3;
    }
    if (DAT_ffcf <= bVar2) {
      DAT_1480 = DAT_ff29;
    }
  }
  return;
}


// ---- FUN_8be1 @ 8be1 ----

void FUN_8be1(void)

{
  byte bVar1;
  byte *pbVar2;
  
  if ((DAT_004a == '\0') && (DAT_1477 = DAT_1477 + 1, DAT_1477 == 0)) {
    DAT_1477 = 0xff;
  }
  if ((DAT_0053 & 2) != 0) {
    DAT_1477 = 0;
  }
  pbVar2 = &DAT_ff20;
  if (DAT_ff00 <= DAT_140c) {
    pbVar2 = &DAT_fee4;
  }
  if (DAT_1477 < pbVar2[1]) {
    bVar1 = DAT_1477 - *pbVar2;
    if (DAT_1477 < *pbVar2 || bVar1 == 0) {
      DAT_1530 = DAT_fee6;
      return;
    }
    if ((!(bool)(bVar1 >> 7)) && ((byte)(bVar1 * '\x02') < DAT_fee6)) {
      DAT_1530 = ~(bVar1 * '\x02' - DAT_fee6);
      return;
    }
  }
  DAT_1530 = 0;
  return;
}


// ---- FUN_8c23 @ 8c23 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_8c23(undefined1 param_1,undefined1 param_2)

{
  char cVar1;
  byte bVar2;
  byte bVar3;
  undefined1 uVar4;
  
  bVar3 = DAT_1544;
  if ((DAT_0053 & 2) == 0) {
    if (DAT_004a != '\0') {
      return;
    }
    if (DAT_141b == '\0') {
      return;
    }
    FUN_809f(DAT_1544,DAT_141b,0xf890);
  }
  else {
    bVar2 = DAT_145d;
    FUN_809f(DAT_145d,param_2,0xfe00);
    DAT_141b = -1;
    bVar3 = 0x40;
    DAT_1417 = bVar2;
  }
  cVar1 = DAT_141b;
  _DAT_005b = (ushort)bVar3 * (ushort)DAT_1417;
  uVar4 = (undefined1)_DAT_005b;
  FUN_82b9(DAT_141b);
  _DAT_1420 = CONCAT11(cVar1,uVar4);
  return;
}


// ---- FUN_8c75 @ 8c75 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8c75(void)

{
  short sVar1;
  
  sVar1 = _DAT_1418 + _DAT_1420 + _DAT_1514;
  if (((DAT_0053 & 2) == 0) && (sVar1 = sVar1 + _DAT_1426, DAT_140a == '\0')) {
    sVar1 = sVar1 - _DAT_142f;
  }
  _DAT_142a = (sVar1 + _DAT_1428) - _DAT_1517;
  if (_DAT_142a == 0) {
    DAT_0088 = DAT_0088 | 0x80;
  }
  else {
    DAT_0088 = DAT_0088 & 0x7f;
  }
  _DAT_142a = _DAT_142a + _DAT_1422;
  if (0x3f < (byte)((ushort)_DAT_142a >> 8)) {
    _DAT_142a = 0x4000;
  }
  return;
}


// ---- FUN_8cac @ 8cac ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8cac(void)

{
  undefined1 extraout_B;
  undefined1 uStack0000;
  
  DAT_0060 = FUN_809f();
  _DAT_005b = _DAT_1413;
  uStack0000 = FUN_8001();
  _DAT_005b = _DAT_1482;
  FUN_8001(-DAT_0060);
  _DAT_1482 = CONCAT11(uStack0000,extraout_B) + _DAT_005b;
  return;
}


// ---- FUN_8cfa @ 8cfa ----

void FUN_8cfa(void)

{
  if ((DAT_004a == '\0') && (DAT_142e = DAT_142e + 1, DAT_142e == 0)) {
    DAT_142e = 0xff;
  }
  if ((DAT_0053 & 2) == 0) {
    DAT_004f = DAT_004f & 0xfe;
    FUN_8d98();
    if (0x3b < DAT_1453) {
      return;
    }
  }
  else {
    FUN_8d27();
  }
  if (DAT_142e < 0x10) {
    FUN_8d4f();
  }
  return;
}


// ---- FUN_8d27 @ 8d27 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8d27(void)

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
  _DAT_1411 = CONCAT11(cVar1 + CARRY1(extraout_B,DAT_142c),extraout_B + DAT_142c) + _DAT_14a2;
  return;
}


// ---- FUN_8d4f @ 8d4f ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 FUN_8d4f(void)

{
  byte bVar1;
  undefined1 uVar2;
  
  uVar2 = 0xfe;
  DAT_142d = FUN_809f();
  if (0xc < DAT_1442) {
    bVar1 = DAT_ff82;
    if (DAT_1442 < DAT_f78b) {
      bVar1 = (DAT_1442 - 0xc) * -5;
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


// ---- FUN_8d98 @ 8d98 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8d98(void)

{
  char cVar1;
  byte bVar2;
  byte extraout_B;
  
  _DAT_005b = _DAT_1482;
  if (DAT_1470 != '\0') {
    DAT_1470 = DAT_1470 + -1;
    goto LAB_8de8;
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
        if (DAT_1442 <= bVar2) goto LAB_8de2;
      }
      if ((DAT_0051 & 4) == 0) {
        DAT_0051 = DAT_0051 | 4;
        DAT_1470 = '\x14';
      }
      goto LAB_8de8;
    }
  }
LAB_8de2:
  DAT_0051 = DAT_0051 & 0xfb;
  _DAT_005b = _DAT_1413;
LAB_8de8:
  _DAT_14f2 = _DAT_005b;
  FUN_8001();
  if ((DAT_0053 & 1) == 0) {
    DAT_153f = (undefined1)((ushort)_DAT_148e >> 8);
  }
  else {
    DAT_153f = (undefined1)((ushort)_DAT_1645 >> 8);
  }
  cVar1 = FUN_8001();
  _DAT_1411 = CONCAT11(cVar1 + CARRY1(extraout_B,DAT_142c),extraout_B + DAT_142c) + _DAT_14a2;
  return;
}


// ---- FUN_8e17 @ 8e17 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8e17(void)

{
  char extraout_B;
  char extraout_B_00;
  byte bVar1;
  byte bVar2;
  byte bVar3;
  
  if (DAT_004a == '\0') {
    DAT_14ac = DAT_14ac + 1;
    if (DAT_14ac == 0) {
      DAT_14ac = 0xff;
    }
    if (((short)((ushort)DAT_0050 << 8) < 0) && (DAT_0050 = DAT_0050 + 1, DAT_0050 == 0)) {
      DAT_0050 = 0xff;
    }
  }
  if (DAT_1474 != 0) {
    DAT_1474 = DAT_1474 - 1;
  }
  if (((((DAT_0053 & 2) == 0) && ((DAT_0054 & 1) == 0)) && ((DAT_0054 & 8) != 0)) &&
     ((((DAT_0083 & 0x10) == 0 && ((DAT_00e5 & 0x80) != 0)) &&
      ((DAT_1407 == 0 && ((DAT_0053 & 4) != 0)))))) {
    if (DAT_14ac <= DAT_f878) goto LAB_8e6a;
    DAT_0098 = DAT_0098 | 0x10;
  }
  else {
    DAT_14ac = 0;
LAB_8e6a:
    DAT_0098 = DAT_0098 & 0xef;
  }
  if (((DAT_1407 == 0) && ((DAT_0053 & 4) != 0)) && ((DAT_0053 & 1) == 0)) {
    if ((DAT_0098 & 0x20) == 0) {
      if (DAT_004a == '\0') {
        DAT_14a8 = FUN_809f();
        bVar1 = (byte)_DAT_14a6;
        bVar3 = (byte)(_DAT_14a6 >> 8);
        if ((short)((ushort)DAT_14a8 << 8) < 0) {
          DAT_14a9 = DAT_14a8 + 0x80;
          _DAT_14a6 = CONCAT11(bVar3 + CARRY1(bVar1,DAT_14a9),bVar1 + DAT_14a9);
          if (CARRY1(bVar3,CARRY1(bVar1,DAT_14a9))) {
            _DAT_14a6 = 0xffff;
          }
        }
        else {
          DAT_14a9 = 0x80 - DAT_14a8;
          _DAT_14a6 = CONCAT11(bVar3 - (bVar1 < DAT_14a9),bVar1 - DAT_14a9);
          if (bVar3 < (bVar1 < DAT_14a9)) {
            _DAT_14a6 = 0;
          }
        }
        if ((_DAT_f873 <= _DAT_14a6) && (((DAT_00c8 & 0x20) != 0 || (DAT_f877 <= DAT_140c)))) {
          DAT_0098 = DAT_0098 | 0x20;
          goto LAB_8ee8;
        }
      }
    }
    else {
LAB_8ee8:
      if ((DAT_0098 & 0x40) == 0) {
        if (DAT_f875 <= DAT_1460) {
          DAT_0098 = DAT_0098 | 0x40;
        }
      }
      else if (DAT_1460 < DAT_f876) goto LAB_8f09;
    }
  }
  else {
    _DAT_14a6 = 0;
    DAT_0098 = DAT_0098 & 0xdf;
LAB_8f09:
    DAT_0098 = DAT_0098 & 0xbf;
  }
  if ((DAT_fa0a <= DAT_1407) || (bVar3 = DAT_1460 < DAT_ffb4, !(bool)bVar3)) {
    DAT_1533 = DAT_1533 & 0xfc;
    DAT_1561 = 0;
    DAT_1562 = 0;
    goto LAB_8faf;
  }
  bVar1 = 1;
  if ((DAT_1533 & 4) == 0) {
    DAT_1533 = DAT_1533 | 8;
    _DAT_005b = CONCAT11(DAT_fa0a,DAT_fa0b);
    _DAT_005d = CONCAT11(2,DAT_fa0c);
    DAT_0060 = DAT_1407;
    FUN_910d();
    bVar2 = bVar3 & 0xf1;
    if (extraout_B < '\0') goto LAB_8faf;
    if (extraout_B != '\0') {
      bVar1 = bVar3 & 0xf1;
      DAT_1533 = DAT_1533 & 0xf7;
      goto LAB_8f5d;
    }
  }
  else {
LAB_8f5d:
    DAT_1533 = DAT_1533 | 4;
    _DAT_005b = CONCAT11(DAT_ffb4,DAT_ff8b);
    _DAT_005d = CONCAT11(1,DAT_ffbc);
    DAT_0060 = DAT_1460;
    FUN_910d();
    bVar2 = bVar1 & 0xf1;
    if (extraout_B_00 < '\0') goto LAB_8faf;
    if (extraout_B_00 != '\0') {
      bVar2 = bVar1 & 0xf1;
      DAT_1533 = DAT_1533 & 0xfb;
    }
  }
  if ((DAT_004f & 0x40) != 0) {
    if (DAT_1407 == 0) {
      bVar3 = DAT_ffe9 < 10 | (DAT_ffe9 == 10) << 2;
      FUN_8fc5();
      if ((bool)(bVar3 & 1) || (bool)(bVar3 >> 2 & 1)) goto LAB_8faf;
    }
    DAT_004f = DAT_004f & 0xbf;
    FUN_8fcd();
    return;
  }
  if (((DAT_1407 == 0) && (FUN_8fc5(), (bVar2 & 1) != 0)) && (DAT_feea <= DAT_1413)) {
    DAT_0050 = DAT_0050 | 0x80;
    bVar3 = DAT_0050 < 0x8b;
    if (!(bool)bVar3) {
      DAT_004f = DAT_004f | 0x40;
LAB_8faf:
      FUN_90d1();
      return;
    }
  }
  else {
    DAT_0050 = 0;
    bVar3 = false;
  }
  bVar1 = DAT_004f;
  if (((DAT_0094 & 0x10) != 0) && ((DAT_0099 & 0x10) == 0)) {
    DAT_004f = DAT_004f | 8;
    FUN_90f7();
    return;
  }
  if ((DAT_0053 & 1) == 0) {
    DAT_004f = DAT_004f & 0xfd;
    if ((bVar1 & 8) == 0) goto LAB_8ff9;
    DAT_1474 = DAT_fefb;
    bVar1 = DAT_1474;
    goto LAB_8ff6;
  }
  if ((DAT_004f & 2) == 0) {
    DAT_004f = DAT_004f | 2;
    bVar3 = DAT_1407 < DAT_ff85;
    if ((!(bool)bVar3) && (((DAT_0053 & 0x40) == 0 || ((DAT_0053 & 8) != 0)))) {
LAB_9023:
      FUN_946c();
      if ((bool)(bVar3 & 1)) goto LAB_8ff9;
LAB_902b:
      DAT_004f = DAT_004f | 8;
      DAT_1474 = 0;
      goto LAB_90c5;
    }
LAB_9014:
    DAT_1474 = 0;
    bVar1 = DAT_1474;
  }
  else {
    if ((DAT_00ba & 1) != 0) {
      FUN_90d1();
      return;
    }
    if (((DAT_0053 & 0x40) != 0) && (bVar3 = false, DAT_1407 < DAT_ff85)) goto LAB_9014;
    if ((DAT_004f & 8) == 0) {
      if ((((DAT_0053 & 0x40) != 0) && ((DAT_0053 & 8) != 0)) && ((DAT_004f & 4) == 0))
      goto LAB_9023;
      FUN_946c();
      if ((bVar3 & 1) != 0) goto LAB_8ff9;
      goto LAB_902b;
    }
    if ((DAT_0053 & 0x40) == 0) {
      bVar3 = false;
      bVar2 = 1;
      if (DAT_ff85 <= DAT_1407) goto LAB_9083;
LAB_90ab:
      bVar2 = bVar2 & 0xf1;
      FUN_946c();
      bVar1 = DAT_ffdf;
      if ((bVar2 & 1) == 0) {
LAB_90c5:
        if (DAT_1474 != 0) {
          if (DAT_1474 < DAT_fefa) {
            FUN_90f7();
            return;
          }
          DAT_0054 = DAT_0054 & 0xfd;
          if ((((DAT_0098 & 0x40) == 0) && ((DAT_0098 & 0x10) == 0)) && ((DAT_00b7 & 1) == 0)) {
            DAT_00b5 = DAT_00b5 & 0xf7;
            return;
          }
        }
        DAT_0054 = DAT_0054 & 0xfd;
        _DAT_1411 = (ushort)DAT_142c;
        DAT_00b5 = DAT_00b5 | 8;
        _DAT_004d = (ushort)DAT_142c;
        DAT_1533 = DAT_1533 & 0xfc;
        DAT_1534 = 0;
        DAT_1535 = 0;
        return;
      }
    }
    else {
LAB_9083:
      FUN_946c();
      bVar1 = DAT_ffde;
      if ((bVar3 & 1) == 0) {
        if (((DAT_0053 & 0x40) == 0) || (bVar2 = bVar3 & 0xf1, (DAT_0053 & 8) != 0)) {
          bVar3 = bVar3 & 0xf1;
          if (((DAT_0053 & 0x90) == 0) || (FUN_9472(), bVar1 = DAT_ffde, !(bool)(bVar3 & 1)))
          goto LAB_90c5;
        }
        else if (((DAT_0053 & 0x90) == 0) || (FUN_9472(), bVar1 = DAT_ffdf, !(bool)(bVar2 & 1)))
        goto LAB_90ab;
      }
    }
  }
LAB_8ff6:
  DAT_1474 = bVar1;
  DAT_004f = DAT_004f & 0xf7;
LAB_8ff9:
  if (DAT_1474 == 0) {
    FUN_90f2();
    return;
  }
  FUN_90f7();
  return;
}


// ---- FUN_8fc5 @ 8fc5 ----

undefined1 FUN_8fc5(undefined1 param_1,undefined1 param_2,undefined2 param_3)

{
  return (char)((ushort)param_3 >> 8);
}


// ---- FUN_8fcd @ 8fcd ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8fcd(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  
  bVar1 = DAT_004f;
  DAT_0050 = 0;
  if (((DAT_0094 & 0x10) != 0) && ((DAT_0099 & 0x10) == 0)) {
    DAT_004f = DAT_004f | 8;
    FUN_90f7();
    return;
  }
  if ((DAT_0053 & 1) == 0) {
    DAT_004f = DAT_004f & 0xfd;
    if ((bVar1 & 8) == 0) goto LAB_8ff9;
    DAT_1474 = DAT_fefb;
    bVar1 = DAT_1474;
    goto LAB_8ff6;
  }
  if ((DAT_004f & 2) == 0) {
    DAT_004f = DAT_004f | 2;
    bVar1 = DAT_1407 < DAT_ff85;
    if ((!(bool)bVar1) && (((DAT_0053 & 0x40) == 0 || ((DAT_0053 & 8) != 0)))) {
LAB_9023:
      FUN_946c();
      if ((bool)(bVar1 & 1)) goto LAB_8ff9;
LAB_902b:
      DAT_004f = DAT_004f | 8;
      DAT_1474 = 0;
      goto LAB_90c5;
    }
LAB_9014:
    DAT_1474 = 0;
    bVar1 = DAT_1474;
  }
  else {
    if ((DAT_00ba & 1) != 0) {
      FUN_90d1();
      return;
    }
    if (((DAT_0053 & 0x40) != 0) && (DAT_1407 < DAT_ff85)) goto LAB_9014;
    bVar1 = false;
    if ((DAT_004f & 8) == 0) {
      if ((((DAT_0053 & 0x40) != 0) && ((DAT_0053 & 8) != 0)) && ((DAT_004f & 4) == 0))
      goto LAB_9023;
      FUN_946c();
      if ((bVar1 & 1) != 0) goto LAB_8ff9;
      goto LAB_902b;
    }
    if ((DAT_0053 & 0x40) == 0) {
      bVar3 = 1;
      if (DAT_ff85 <= DAT_1407) goto LAB_9083;
LAB_90ab:
      bVar3 = bVar3 & 0xf1;
      FUN_946c();
      bVar1 = DAT_ffdf;
      if ((bVar3 & 1) == 0) {
LAB_90c5:
        if (DAT_1474 != 0) {
          if (DAT_1474 < DAT_fefa) {
            FUN_90f7();
            return;
          }
          DAT_0054 = DAT_0054 & 0xfd;
          if ((((DAT_0098 & 0x40) == 0) && ((DAT_0098 & 0x10) == 0)) && ((DAT_00b7 & 1) == 0)) {
            DAT_00b5 = DAT_00b5 & 0xf7;
            return;
          }
        }
        DAT_0054 = DAT_0054 & 0xfd;
        _DAT_1411 = (ushort)DAT_142c;
        DAT_00b5 = DAT_00b5 | 8;
        _DAT_004d = (ushort)DAT_142c;
        DAT_1533 = DAT_1533 & 0xfc;
        DAT_1534 = 0;
        DAT_1535 = 0;
        return;
      }
    }
    else {
LAB_9083:
      bVar2 = 0;
      FUN_946c();
      bVar1 = DAT_ffde;
      if ((bVar2 & 1) == 0) {
        if (((DAT_0053 & 0x40) == 0) || (bVar3 = bVar2 & 0xf1, (DAT_0053 & 8) != 0)) {
          bVar2 = bVar2 & 0xf1;
          if (((DAT_0053 & 0x90) == 0) || (FUN_9472(), bVar1 = DAT_ffde, !(bool)(bVar2 & 1)))
          goto LAB_90c5;
        }
        else if (((DAT_0053 & 0x90) == 0) || (FUN_9472(), bVar1 = DAT_ffdf, !(bool)(bVar3 & 1)))
        goto LAB_90ab;
      }
    }
  }
LAB_8ff6:
  DAT_1474 = bVar1;
  DAT_004f = DAT_004f & 0xf7;
LAB_8ff9:
  if (DAT_1474 == 0) {
    FUN_90f2();
    return;
  }
  FUN_90f7();
  return;
}


// ---- FUN_90d1 @ 90d1 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_90d1(void)

{
  DAT_0054 = DAT_0054 & 0xfd;
  _DAT_1411 = (ushort)DAT_142c;
  DAT_00b5 = DAT_00b5 | 8;
  _DAT_004d = (ushort)DAT_142c;
  DAT_1533 = DAT_1533 & 0xfc;
  DAT_1534 = 0;
  DAT_1535 = 0;
  return;
}


// ---- FUN_90f2 @ 90f2 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_90f2(void)

{
  DAT_0054 = DAT_0054 & 0xfd;
  if ((((DAT_0098 & 0x40) == 0) && ((DAT_0098 & 0x10) == 0)) && ((DAT_00b7 & 1) == 0)) {
    DAT_00b5 = DAT_00b5 & 0xf7;
    return;
  }
  _DAT_1411 = (ushort)DAT_142c;
  DAT_00b5 = DAT_00b5 | 8;
  _DAT_004d = (ushort)DAT_142c;
  DAT_1533 = DAT_1533 & 0xfc;
  DAT_1534 = 0;
  DAT_1535 = 0;
  return;
}


// ---- FUN_90f7 @ 90f7 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_90f7(void)

{
  byte bVar1;
  
  bVar1 = DAT_0054;
  DAT_0054 = DAT_0054 | 2;
  if ((((DAT_0098 & 0x40) == 0) && ((DAT_0098 & 0x10) == 0)) && ((DAT_00b7 & 1) == 0)) {
    DAT_00b5 = DAT_00b5 & 0xf7;
    return;
  }
  DAT_0054 = bVar1 & 0xfd;
  _DAT_1411 = (ushort)DAT_142c;
  DAT_00b5 = DAT_00b5 | 8;
  _DAT_004d = (ushort)DAT_142c;
  DAT_1533 = DAT_1533 & 0xfc;
  DAT_1534 = 0;
  DAT_1535 = 0;
  return;
}


// ---- FUN_910d @ 910d ----

void FUN_910d(void)

{
  byte bVar1;
  
  if (DAT_1562 != 0) {
    DAT_1562 = DAT_1562 - 1;
  }
  if (DAT_1561 != 0) {
    DAT_1561 = DAT_1561 - 1;
  }
  if (DAT_1561 == DAT_005e) {
    DAT_1562 = DAT_005e << 1;
  }
  if (DAT_1561 == 0) {
    bVar1 = DAT_0060;
    if ((DAT_1533 & 2) != 0) {
      bVar1 = DAT_0060 + DAT_005d;
    }
    if (DAT_005c <= bVar1) {
      DAT_1561 = DAT_005e << 1;
    }
  }
  if (((byte)(DAT_0060 + DAT_005d) < DAT_005c) || (DAT_005b <= DAT_0060)) {
    DAT_1561 = 0;
    DAT_1562 = 0;
    DAT_1533 = DAT_1533 & 0xfc;
  }
  else {
    if (DAT_005e < DAT_1561) {
      bVar1 = DAT_1533 | 1;
    }
    else {
      bVar1 = DAT_1533 & 0xfe;
    }
    if (DAT_005e < DAT_1562) {
      DAT_1533 = bVar1 | 2;
    }
    else {
      DAT_1533 = bVar1 & 0xfd;
    }
  }
  return;
}


// ---- FUN_918b @ 918b ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_918b(void)

{
  byte bVar1;
  
  if (((DAT_ffd3 & 0x10) != 0) && ((DAT_0053 & 2) == 0)) {
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


// ---- FUN_91b1 @ 91b1 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_91b1(void)

{
  if ((DAT_0054 & 4) != 0) {
    _DAT_004d = _DAT_144e * 5;
    if (0x7f < (byte)((ushort)_DAT_004d >> 8)) {
      _DAT_004d = 0x7fff;
    }
    if ((DAT_004f & 0x10) == 0) {
      DAT_004f = DAT_004f & 0xdf;
    }
    else {
      DAT_004f = DAT_004f | 0x20;
    }
  }
  return;
}


// ---- FUN_91d7 @ 91d7 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_91d7(void)

{
  char cVar1;
  byte bVar2;
  undefined1 uVar3;
  byte bVar4;
  ushort uVar5;
  short sVar6;
  byte bVar7;
  byte *pbVar8;
  undefined2 *puVar9;
  
  bVar4 = DAT_0091;
  if ((DAT_0054 & 8) == 0) {
    return;
  }
  uVar5 = CONCAT11(DAT_0092,DAT_0092) & 0xf00f;
  DAT_005b = (byte)uVar5;
  bVar2 = (byte)(uVar5 >> 8);
  bVar7 = bVar2 >> 7;
  bVar2 = bVar2 << 1;
  if ((DAT_00b5 & 8) != 0) {
    bVar2 = bVar2 | 0x10;
  }
  DAT_0092 = bVar2 | DAT_005b;
  DAT_0091 = DAT_0091 & 0xfd;
  if ((DAT_0053 & 1) == 0) {
    if ((bVar4 & 1) == 0) {
LAB_921e:
      if ((DAT_0088 & 8) != 0) {
        uVar3 = FUN_809f();
        _DAT_155f = CONCAT11(uVar3,DAT_155f_1);
        bVar7 = bVar7 & 0xf1;
        FUN_949a();
        if (!(bool)(bVar7 & 1)) {
          DAT_0088 = DAT_0088 & 0xf7;
        }
      }
    }
    else {
      DAT_0091 = bVar4 & 0xfc;
      bVar7 = DAT_1436 < 0x40;
      if (!(bool)bVar7) {
        DAT_0088 = DAT_0088 | 8;
        goto LAB_921e;
      }
      DAT_0091 = DAT_0091 | 2;
      DAT_1526 = 0;
    }
    DAT_1436 = 0;
    if ((DAT_0053 & 1) != 0) goto LAB_9252;
    DAT_1545 = DAT_149a - DAT_1543;
    if (DAT_149a < DAT_1543) {
      DAT_1545 = 0;
    }
    if (DAT_1545 < DAT_f93a) goto LAB_9252;
    if ((DAT_0091 & 0x80) == 0) {
      pbVar8 = &DAT_f7b6;
      if ((DAT_ffc6 <= DAT_1544) && (pbVar8 = &DAT_f7b7, DAT_ffc7 <= DAT_1544)) {
        pbVar8 = &DAT_f7b8;
      }
      DAT_154b = (&DAT_f7b2)[*pbVar8 & 3];
      DAT_154a = DAT_149a;
      if ((DAT_0092 & 0x80) == 0) {
        DAT_0091 = DAT_0091 & 0xf7 | 0x50;
      }
      else {
        DAT_0091 = DAT_0091 | 0x58;
      }
      DAT_1547 = '\x01';
      DAT_1548 = 0;
      DAT_1549 = 0;
      puVar9 = (undefined2 *)&DAT_154d;
      DAT_154c = DAT_154b;
      do {
        *puVar9 = 0;
        puVar9 = puVar9 + 1;
      } while (puVar9 < (undefined2 *)0x155e);
    }
    else {
      DAT_1546 = 0;
      DAT_1547 = '\0';
      DAT_0091 = DAT_0091 & 0xdf | 0x40;
      pbVar8 = &DAT_f910;
      for (bVar4 = 0; bVar4 < 8; bVar4 = bVar4 + 1) {
        if (DAT_1541 < *pbVar8) {
          if ((DAT_0091 & 0x20) == 0) {
            DAT_0091 = DAT_0091 | 0x20;
            DAT_1546 = bVar4;
          }
          if (DAT_149a < *pbVar8) break;
          DAT_1547 = DAT_1547 + '\x01';
        }
        pbVar8 = pbVar8 + 1;
      }
    }
    DAT_0091 = DAT_0091 | 0x80;
    if ((DAT_1548 <= DAT_ffc8) && (DAT_1547 != '\0')) {
      DAT_1527 = FUN_809f();
      bVar4 = FUN_809f();
      sVar6 = (ushort)bVar4 * (ushort)DAT_1527;
      if ((SUB21((ushort)sVar6 >> 0xf,0)) ||
         (DAT_1527 = (byte)((ushort)(sVar6 * 4) >> 8), sVar6 * 2 < 0)) {
        DAT_1527 = 0xff;
      }
      bVar4 = FUN_809f();
      sVar6 = (ushort)bVar4 * (ushort)DAT_1527;
      if ((SUB21((ushort)sVar6 >> 0xf,0)) ||
         (DAT_1527 = (byte)((ushort)(sVar6 * 4) >> 8), sVar6 * 2 < 0)) {
        DAT_1527 = 0xff;
      }
      if (((DAT_0091 & 8) != 0) && ((DAT_0091 & 2) == 0)) {
        sVar6 = (ushort)DAT_1527 * (ushort)DAT_ffc9;
        if ((SUB21((ushort)sVar6 >> 0xf,0)) ||
           (DAT_1527 = (byte)((ushort)(sVar6 * 4) >> 8), sVar6 * 2 < 0)) {
          DAT_1527 = 0xff;
        }
      }
      bVar4 = FUN_809f();
      bVar7 = DAT_1527 - 9;
      if (DAT_1527 < 9) {
        bVar7 = 0;
      }
      _DAT_155f = (ushort)bVar4 * (ushort)bVar7 * 8 + 0x46;
      do {
        if (DAT_ffc8 < DAT_1548) break;
        *(short *)(&DAT_154d + (byte)(DAT_1548 << 1)) = _DAT_155f;
        DAT_1548 = DAT_1548 + 1;
        DAT_1547 = DAT_1547 + -1;
      } while (DAT_1547 != '\0');
    }
    if ((DAT_0091 & 0x10) == 0) goto LAB_93ab;
LAB_93be:
    bVar4 = DAT_1549 >> 7;
    FUN_94a9();
    cVar1 = DAT_154c;
    if (!(bool)(bVar4 & 1)) {
      DAT_1549 = DAT_1549 + 1;
      DAT_154c = DAT_154b;
      cVar1 = DAT_154c;
      if ((DAT_0091 & 0x10) != 0) {
        DAT_0091 = DAT_0091 & 0xef;
      }
    }
  }
  else {
    DAT_0091 = DAT_0091 | 1;
    DAT_0088 = DAT_0088 & 0xf7;
LAB_9252:
    bVar4 = DAT_0091;
    DAT_0091 = DAT_0091 & 0x7f;
    cVar1 = DAT_154c;
    if ((bVar4 & 0x40) != 0) {
      if (DAT_149a < DAT_154a) {
        DAT_0091 = bVar4 & 0x3d;
      }
      else {
LAB_93ab:
        cVar1 = DAT_154c + -1;
        if (((char)(DAT_154c + -1) == '\0') && (cVar1 = DAT_154c, DAT_1549 < DAT_1548))
        goto LAB_93be;
      }
    }
  }
  DAT_154c = cVar1;
  if ((DAT_0053 & 1) == 0) {
LAB_9468:
    DAT_0088 = DAT_0088 & 0xef;
  }
  else {
    bVar4 = DAT_1436 < 0x40;
    if ((bool)bVar4) {
      DAT_1436 = DAT_1436 + 1;
    }
    if ((DAT_0088 & 2) == 0) {
      if (((DAT_004f & 8) == 0) || (DAT_1474 != '\0')) goto LAB_9468;
      if ((DAT_0088 & 0x10) != 0) {
        return;
      }
      bVar4 = DAT_1407 < DAT_ff85;
      if ((bool)bVar4) {
        bVar7 = bVar4;
        if ((DAT_0053 & 0x40) == 0) {
LAB_942f:
          bVar4 = bVar7 & 0xf1;
          FUN_946c();
          if (!(bool)(bVar4 & 1)) {
            return;
          }
        }
      }
      else {
        FUN_946c();
        if (!(bool)(bVar4 & 1)) {
          if (((DAT_0053 & 0x40) == 0) || (bVar7 = bVar4 & 0xf1, (DAT_0053 & 8) != 0)) {
            bVar4 = bVar4 & 0xf1;
            if ((DAT_0053 & 0x90) == 0) {
              return;
            }
            FUN_9472();
            if ((bVar4 & 1) == 0) {
              return;
            }
          }
          else if (((DAT_0053 & 0x90) == 0) || (FUN_9472(), bVar4 = bVar7, !(bool)(bVar7 & 1)))
          goto LAB_942f;
        }
      }
      DAT_0088 = DAT_0088 | 2;
      bVar4 = bVar4 & 0xf1;
    }
    uVar3 = DAT_ffc3;
    if ((-1 < (char)DAT_1471) && (bVar4 = 1, DAT_ff0f <= DAT_1471)) {
      bVar4 = 0;
      uVar3 = DAT_ffc2;
    }
    _DAT_155f = CONCAT11(uVar3,DAT_155f_1);
    FUN_9491();
    if (!(bool)(bVar4 & 1)) {
      DAT_0088 = DAT_0088 & 0xfd;
      DAT_0088 = DAT_0088 | 0x10;
    }
  }
  return;
}


// ---- FUN_946c @ 946c ----

byte FUN_946c(void)

{
  bool bVar1;
  byte bVar2;
  char cVar3;
  byte bVar4;
  
  bVar2 = FUN_809f();
  cVar3 = '\0';
  if ((DAT_0094 & 4) != 0) {
    bVar1 = CARRY1(bVar2,DAT_f793);
    bVar2 = bVar2 + DAT_f793;
    if (bVar1) {
      cVar3 = '\x01';
    }
  }
  bVar4 = cVar3 << 1 | bVar2 >> 7;
  if ((DAT_140a <= bVar4) && ((bVar4 != DAT_140a || (DAT_140b <= (byte)(bVar2 << 1))))) {
    return ~(bVar2 << 1);
  }
  return 0;
}


// ---- FUN_9472 @ 9472 ----

byte FUN_9472(byte param_1)

{
  bool bVar1;
  char cVar2;
  byte bVar3;
  
  cVar2 = '\0';
  if ((DAT_0094 & 4) != 0) {
    bVar1 = CARRY1(param_1,DAT_f793);
    param_1 = param_1 + DAT_f793;
    if (bVar1) {
      cVar2 = '\x01';
    }
  }
  bVar3 = cVar2 << 1 | param_1 >> 7;
  if ((DAT_140a <= bVar3) && ((bVar3 != DAT_140a || (DAT_140b <= (byte)(param_1 << 1))))) {
    return ~(param_1 << 1);
  }
  return 0;
}


// ---- FUN_9491 @ 9491 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9491(void)

{
  byte bVar1;
  byte bVar3;
  short sVar2;
  
  bVar1 = FUN_809f();
  bVar3 = DAT_155f - 9;
  if (DAT_155f < 9) {
    bVar3 = 0;
  }
  sVar2 = (ushort)bVar1 * (ushort)bVar3 * 8 + 0x46;
  if ((_DAT_1042 == 0) && (_DAT_1044 == 0)) {
    _DAT_1058 = sVar2;
    _DAT_106e = sVar2;
    DAT_1036 = DAT_00c0 & 0xfc;
    DAT_0091 = DAT_0091 | 4;
    return;
  }
  return;
}


// ---- FUN_949a @ 949a ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_949a(void)

{
  ushort in_D;
  byte bVar2;
  short sVar1;
  
  bVar2 = DAT_155f - 9;
  if (DAT_155f < 9) {
    bVar2 = 0;
  }
  sVar1 = (in_D >> 8) * (ushort)bVar2 * 8 + 0x46;
  if ((_DAT_1042 == 0) && (_DAT_1044 == 0)) {
    _DAT_1058 = sVar1;
    _DAT_106e = sVar1;
    DAT_1036 = DAT_00c0 & 0xfc;
    DAT_0091 = DAT_0091 | 4;
    return;
  }
  return;
}


// ---- FUN_94a9 @ 94a9 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_94a9(void)

{
  undefined2 in_D;
  
  if ((_DAT_1042 == 0) && (_DAT_1044 == 0)) {
    _DAT_1058 = in_D;
    _DAT_106e = in_D;
    DAT_1036 = DAT_00c0 & 0xfc;
    DAT_0091 = DAT_0091 | 4;
    return;
  }
  return;
}


// ---- FUN_94d2 @ 94d2 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_94d2(void)

{
  bool bVar1;
  byte bVar2;
  byte bVar4;
  ushort uVar3;
  
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_0053 & 1) == 0) {
      DAT_14aa = 0;
      if ((DAT_00b6 & 1) != 0) {
        DAT_00b6 = DAT_00b6 & 0xfe;
        _DAT_142f = (ushort)DAT_ff84 << 2;
        goto LAB_951a;
      }
      bVar4 = (byte)_DAT_142f;
      bVar2 = (byte)((ushort)_DAT_142f >> 8);
      _DAT_142f = CONCAT11(bVar2 - (bVar4 < DAT_ff1f),bVar4 - DAT_ff1f);
      if ((bVar4 < DAT_ff1f) <= bVar2) goto LAB_951a;
    }
    else {
      DAT_00b6 = DAT_00b6 | 1;
      if ((DAT_00b5 & 8) == 0) {
        if (DAT_14aa != 0) {
          DAT_14aa = DAT_14aa - 1;
        }
      }
      else if (DAT_14aa < DAT_ffb6) {
        DAT_14aa = DAT_14aa + 1;
      }
    }
  }
  _DAT_142f = 0;
LAB_951a:
  if ((_DAT_1514 != 0) || (_DAT_1517 != 0)) {
    bVar2 = FUN_809f();
    uVar3 = (ushort)bVar2;
    _DAT_1524 = uVar3 * 2;
    if (_DAT_1514 != 0) {
      bVar1 = _DAT_1514 < _DAT_1524;
      _DAT_1514 = _DAT_1514 + uVar3 * -2;
      if (bVar1) {
        _DAT_1514 = 0;
      }
      DAT_1513 = (undefined1)((_DAT_1514 << 2) >> 8);
    }
    if (_DAT_1517 != 0) {
      bVar1 = _DAT_1517 < _DAT_1524;
      _DAT_1517 = _DAT_1517 + uVar3 * -2;
      if (bVar1) {
        _DAT_1517 = 0;
      }
      DAT_1516 = (undefined1)((_DAT_1517 << 2) >> 8);
    }
  }
  return;
}


// ---- FUN_957a @ 957a ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_957a(void)

{
  byte bVar1;
  undefined1 uVar2;
  byte bVar3;
  byte bVar4;
  undefined1 extraout_B;
  short sVar5;
  undefined1 extraout_B_00;
  undefined1 extraout_B_01;
  undefined1 extraout_B_02;
  undefined1 extraout_B_03;
  
  uVar2 = FUN_b565();
  sVar5 = CONCAT11(uVar2,extraout_B) << 1;
  if ((char)((ushort)sVar5 >> 8) != '\0') {
    sVar5 = 0xff;
  }
  DAT_1400 = (byte)sVar5;
  if ((DAT_00d2 & 2) != 0) {
    _DAT_1431 = (ushort)DAT_16a8 << 8;
    goto LAB_9904;
  }
  if ((DAT_0097 & 4) == 0) {
    if (199 < DAT_1400) {
      if (DAT_14a5 < 0x32) goto LAB_95b3;
      DAT_0097 = DAT_0097 | 4;
LAB_98be:
      DAT_148a = 0;
      FUN_bd9e();
      goto LAB_98db;
    }
    DAT_14a5 = 0;
LAB_95b3:
    if ((DAT_0051 & 0x20) == 0) {
      if ((DAT_0053 & 2) != 0) goto LAB_98e7;
      if (0x27 < DAT_1438) {
        DAT_1438 = 0x28;
        bVar3 = DAT_ff91;
        if (DAT_1453 < 0x3c) {
          bVar3 = DAT_fee7;
        }
        if (bVar3 <= DAT_140c) {
          if (DAT_1400 < DAT_ff92) {
            if (DAT_ff93 <= DAT_1400) {
              DAT_1437 = 0;
              goto LAB_98ea;
            }
            DAT_1437 = DAT_1437 - 1;
          }
          else {
            DAT_1437 = DAT_1437 + 1;
          }
          if ((short)((ushort)DAT_1437 << 8) < 0) {
            if (DAT_1437 < 0xf6) goto LAB_9666;
          }
          else if (9 < DAT_1437) {
            DAT_0051 = DAT_0051 | 0x40;
LAB_9666:
            DAT_0051 = DAT_0051 | 0x28;
            DAT_1438 = 0;
            goto LAB_966c;
          }
        }
      }
      goto LAB_98ea;
    }
    if ((((DAT_0053 & 1) != 0) && (DAT_ffd1 <= DAT_1442)) && (3 < DAT_1407)) {
      DAT_1434 = 0;
      if ((DAT_0051 & 0x80) != 0) {
        _DAT_1431 = (ushort)DAT_ffd0 << 8;
        DAT_1438 = 0;
        DAT_0097 = DAT_0097 | 0x80;
        goto LAB_9904;
      }
      DAT_1433 = DAT_1433 + 1;
      if (0x13 < DAT_1433) {
        DAT_0051 = DAT_0051 | 0x80;
      }
LAB_966c:
      if ((DAT_0059 & 8) != 0) {
LAB_9671:
        DAT_00b4 = 0;
        DAT_0087 = 0;
        _DAT_147c = 0;
        goto LAB_98e7;
      }
      bVar3 = DAT_140c;
      if (((DAT_009b & 0x80) != 0) && (bVar3 = DAT_140c + 5, 0xfa < DAT_140c)) {
        bVar3 = 0xff;
      }
      if (bVar3 < 0x73) {
        DAT_009b = DAT_009b & 0x7f;
      }
      else {
        DAT_009b = DAT_009b | 0x80;
      }
      bVar3 = DAT_140c;
      if (((DAT_009b & 0x40) != 0) && (bVar3 = DAT_140c + 5, 0xfa < DAT_140c)) {
        bVar3 = 0xff;
      }
      if (bVar3 < DAT_f883) {
        DAT_009b = DAT_009b & 0xbf;
      }
      else {
        DAT_009b = DAT_009b | 0x40;
      }
      if ((DAT_0053 & 1) == 0) {
        DAT_0051 = DAT_0051 & 0xef;
LAB_9705:
        DAT_00b4 = 0;
        if (((DAT_fef6 != 0) && (0x87 < DAT_0087)) && (((DAT_00d3 & 8) == 0 || (DAT_16b2 != '\0'))))
        {
          uVar2 = FUN_9918();
          _DAT_1645 = CONCAT11(uVar2,extraout_B_01);
        }
        DAT_0087 = 0;
        _DAT_147c = 0;
      }
      else {
        DAT_0051 = DAT_0051 | 0x10;
        if (1 < DAT_1407) goto LAB_9705;
        if ((DAT_009b & 0x80) == 0) {
          if ((DAT_ffd3 & 4) != 0) {
            DAT_0097 = DAT_0097 | 0x80;
            goto LAB_9671;
          }
          goto LAB_9705;
        }
        if ((DAT_009b & 0x40) != 0) goto LAB_9705;
        DAT_00b4 = DAT_00b4 | 0x80;
        if ((0x80 < DAT_00b4) && (DAT_0087 = DAT_0087 | 0x80, 0x87 < DAT_0087)) {
          uVar2 = FUN_9918();
          _DAT_1431 = CONCAT11(uVar2,extraout_B_00);
          DAT_1438 = 0;
          DAT_0097 = DAT_0097 | 0x80;
          goto LAB_9904;
        }
      }
      bVar1 = DAT_148b;
      bVar3 = DAT_0051;
      if (DAT_1400 < DAT_1435) {
        if ((DAT_0097 & 0x80) == 0) {
          if ((DAT_0051 & 8) == 0) {
            _DAT_005b = DAT_fef1;
            if ((((DAT_0051 & 0x10) == 0) && (_DAT_005b = DAT_feee, (DAT_0051 & 2) == 0)) &&
               (_DAT_005b = DAT_ff06, DAT_1480 != '\0')) {
              _DAT_005b = DAT_ff0c;
            }
            uVar2 = FUN_8001();
            _DAT_1431 = CONCAT11(uVar2,extraout_B_02) + _DAT_1431;
            if ((2 < DAT_148a) && (0x31 < DAT_1438)) goto LAB_98be;
            goto LAB_98b6;
          }
          DAT_14d4 = DAT_1431;
          if ((char)DAT_0087 < '\0') {
            _DAT_147c = (ushort)DAT_1431 + _DAT_147c;
            DAT_0087 = DAT_0087 + 1;
          }
          bVar4 = DAT_fef0;
          if ((((DAT_0051 & 0x10) == 0) && (bVar4 = DAT_fee3, (DAT_0051 & 2) == 0)) &&
             (bVar4 = DAT_ff03, DAT_1480 != '\0')) {
            bVar4 = DAT_ff2e;
          }
        }
        else {
          DAT_0097 = DAT_0097 & 0x7f;
          bVar4 = DAT_f88b;
        }
        DAT_0051 = DAT_0051 & 0xf7;
        bVar4 = (byte)(((ushort)bVar4 << 0xc) >> 8);
        DAT_14c2 = -(bVar4 >> 1);
        _DAT_1431 = (ushort)bVar4 * 0x100 + _DAT_1431;
        DAT_1435 = DAT_ff95;
        if ((bVar3 & 0x40) != 0) {
          DAT_0051 = bVar3 & 0xb7;
          DAT_1435 = DAT_ffa1;
        }
        DAT_148b = 0;
        if (bVar1 < DAT_feed) {
          DAT_148a = DAT_148a + 1;
          if (2 < DAT_148a) {
            if (0x13 < DAT_1438) goto LAB_98be;
            DAT_148a = 3;
          }
        }
        else {
          DAT_148a = 0;
        }
      }
      else {
        if ((DAT_0097 & 0x80) == 0) {
          if ((DAT_0051 & 8) == 0) {
            DAT_14d5 = DAT_1431;
            if ((char)DAT_0087 < '\0') {
              _DAT_147c = (ushort)DAT_1431 + _DAT_147c;
              DAT_0087 = DAT_0087 + 1;
            }
            DAT_1435 = DAT_ff94;
            bVar3 = DAT_fef0;
            if ((((DAT_0051 & 0x10) == 0) && (bVar3 = DAT_fee2, (DAT_0051 & 2) == 0)) &&
               (bVar3 = DAT_ff00, DAT_1480 != '\0')) {
              bVar3 = DAT_ffbb;
            }
            goto LAB_97a6;
          }
          _DAT_005b = DAT_fef1;
          if ((((DAT_0051 & 0x10) == 0) && (_DAT_005b = DAT_feee, (DAT_0051 & 2) == 0)) &&
             (_DAT_005b = DAT_ff06, DAT_1480 != '\0')) {
            _DAT_005b = DAT_ff0c;
          }
          FUN_8001();
          _DAT_1431 = _DAT_1431 - _DAT_005b;
        }
        else {
          DAT_0097 = DAT_0097 & 0x7f;
          bVar3 = DAT_f88c;
LAB_97a6:
          DAT_0051 = DAT_0051 | 8;
          _DAT_005b = (ushort)bVar3 * 0x1000;
          DAT_14c2 = (byte)((ushort)_DAT_005b >> 9);
          _DAT_1431 = _DAT_1431 + (ushort)bVar3 * -0x1000;
          DAT_1438 = 0;
        }
        if (DAT_148b <= DAT_1400) {
          DAT_148b = DAT_1400;
        }
      }
LAB_98b6:
      if (DAT_1438 < DAT_ff7e) {
        if (((DAT_00d3 & 8) == 0) || (DAT_16b2 != '\0')) {
          FUN_992a();
        }
        uVar2 = FUN_9918();
        _DAT_1431 = CONCAT11(uVar2,extraout_B_03);
        goto LAB_990a;
      }
      goto LAB_98be;
    }
    DAT_1433 = 0;
    if ((DAT_0051 & 0x80) == 0) goto LAB_966c;
    DAT_1434 = DAT_1434 + 1;
    if (0x13 < DAT_1434) {
      DAT_0051 = DAT_0051 & 0x7f;
    }
LAB_9901:
    _DAT_1431 = 0x6400;
  }
  else {
LAB_98db:
    DAT_1435 = DAT_ffa0;
    DAT_0051 = DAT_0051 & 0xdf;
    DAT_1437 = 0;
LAB_98e7:
    DAT_1438 = 0;
LAB_98ea:
    if ((byte)((ushort)_DAT_1431 >> 8) < 100) {
      _DAT_1431 = _DAT_1431 + 0x15;
      if (99 < (byte)((ushort)_DAT_1431 >> 8)) goto LAB_9901;
    }
    else {
      _DAT_1431 = _DAT_1431 + -0x15;
      if ((byte)((ushort)_DAT_1431 >> 8) < 100) goto LAB_9901;
    }
  }
LAB_9904:
  DAT_14d4 = (byte)((ushort)_DAT_1431 >> 8);
  DAT_14d5 = DAT_14d4;
LAB_990a:
  DAT_14d6 = (char)(DAT_14d5 + DAT_14d4) >> 1 | CARRY1(DAT_14d5,DAT_14d4) << 7;
  return;
}


// ---- FUN_9918 @ 9918 ----

byte FUN_9918(byte param_1)

{
  if (param_1 < 0x4b) {
    param_1 = 0x4b;
  }
  else if (0x7c < param_1) {
    param_1 = 0x7d;
  }
  return param_1;
}


// ---- FUN_992a @ 992a ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_992a(void)

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
  
  if ((((_DAT_1514 == 0) && (_DAT_1517 == 0)) && ((DAT_0053 & 1) == 0)) &&
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
    uVar1 = FUN_99b8();
    _DAT_005b = CONCAT11(uVar1,extraout_B);
    uVar1 = FUN_8001((char)((ushort)DAT_fef6 >> 8));
    _DAT_007b = CONCAT11(uVar1,extraout_B_00);
    FUN_99c2();
    uVar1 = FUN_99b8();
    uVar1 = FUN_99cb((char)((ushort)(CONCAT11(uVar1,extraout_B_01) + *psVar2) >> 8));
    *psVar2 = CONCAT11(uVar1,extraout_B_02);
    FUN_99c2();
    uVar1 = FUN_99b8();
    uVar1 = FUN_99cb((char)((ushort)(CONCAT11(uVar1,extraout_B_03) + psVar2[1]) >> 8));
    psVar2[1] = CONCAT11(uVar1,extraout_B_04);
    FUN_99c2(~DAT_147f);
    uVar1 = FUN_99b8();
    uVar1 = FUN_99cb((char)((ushort)(CONCAT11(uVar1,extraout_B_05) + psVar2[8]) >> 8));
    psVar2[8] = CONCAT11(uVar1,extraout_B_06);
    FUN_99c2(DAT_147f);
    uVar1 = FUN_99b8();
    uVar1 = FUN_99cb((char)((ushort)(CONCAT11(uVar1,extraout_B_07) + psVar2[9]) >> 8));
    psVar2[9] = CONCAT11(uVar1,extraout_B_08);
    return;
  }
  return;
}


// ---- FUN_99b8 @ 99b8 ----

char FUN_99b8(char param_1,char param_2)

{
  if ((DAT_0051 & 1) != 0) {
    param_1 = -(param_1 + (param_2 != '\0'));
  }
  return param_1;
}


// ---- FUN_99c2 @ 99c2 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_99c2(void)

{
  ushort in_D;
  
  _DAT_005b = (in_D >> 8) * (in_D & 0xff);
  FUN_8001((char)((ushort)_DAT_007b >> 8));
  return;
}


// ---- FUN_99cb @ 99cb ----

byte FUN_99cb(byte param_1)

{
  byte bVar1;
  
  bVar1 = DAT_f841;
  if ((param_1 < DAT_f841) || (bVar1 = DAT_f840, DAT_f840 <= param_1)) {
    param_1 = bVar1;
  }
  return param_1;
}


// ---- FUN_99e1 @ 99e1 ----

void FUN_99e1(void)

{
  DAT_1476 = DAT_1476 + 1;
  if (DAT_1476 < 0x15) {
    DAT_0083 = DAT_0083 ^ 0x80;
    DAT_1003 = DAT_0083;
  }
  return;
}


// ---- FUN_99f7 @ 99f7 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_99f7(void)

{
  byte bVar2;
  ushort uVar1;
  byte bStack0000;
  
  P2DDR = 0xb2;
  DAT_0016 = 0xc3;
  RAMCR = 0xe5;
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
  uVar1 = (ushort)(DAT_0015 & 0xf0) << 8;
  if ((DAT_0017 & 0x20) != 0) {
    uVar1 = CONCAT11(DAT_0015 & 0xf0,1);
  }
  if ((uVar1 & 0x4000) == 0) {
    uVar1 = uVar1 | 0x10;
  }
  if (((uVar1 & 0x8000) != 0) && ((DAT_0088 & 1) == 0)) {
    uVar1 = (ushort)(byte)((byte)uVar1 | 2);
  }
  bStack0000 = (byte)uVar1;
  if (DAT_fee0 < '\0') {
    bStack0000 = bStack0000 | 0x40;
  }
  if ((P2DATA & 1) == 0) {
    bStack0000 = bStack0000 | 0x80;
  }
  if ((DAT_0053 & 0x40) == 0) {
    if ((DAT_0090 & 0x80) == 0) {
      DAT_0090 = DAT_0090 | 0x80;
      goto LAB_9a61;
    }
    if ((DAT_0015 & 0x20) == 0) {
      if ((DAT_0090 & 0x20) == 0) {
        DAT_14c0 = FUN_9b4c();
        DAT_0090 = DAT_0090 | 0x20;
      }
      if (DAT_14c0 != '\0') {
        DAT_14c0 = DAT_14c0 + -1;
        goto LAB_9aa2;
      }
      goto LAB_9aa7;
    }
    if ((DAT_0090 & 0x20) != 0) {
      DAT_14c1 = FUN_9b4c();
      DAT_0090 = DAT_0090 & 0xdf;
    }
    if (DAT_14c1 != '\0') {
      DAT_14c1 = DAT_14c1 + -1;
LAB_9aa2:
      if ((DAT_0053 & 4) != 0) goto LAB_9aa7;
    }
  }
  else {
LAB_9a61:
    if ((DAT_0015 & 0x20) == 0) {
LAB_9aa7:
      bStack0000 = bStack0000 | 4;
    }
  }
  if ((DAT_0053 & 8) == 0) {
    DAT_004f = DAT_004f & 0xfb;
  }
  else {
    DAT_004f = DAT_004f | 4;
  }
  bVar2 = bStack0000 & 0xf7;
  if ((bStack0000 & 0x80) != 0) {
    bVar2 = bVar2 | 8;
  }
  DAT_15a1 = bVar2 & 0x1f;
  uVar1 = (ushort)DAT_1002;
  if ((DAT_1002 & 4) != 0) {
    uVar1 = DAT_1002 | 0x2000;
  }
  if ((uVar1 & 8) != 0) {
    uVar1 = (ushort)(byte)((byte)(uVar1 >> 8) | 0x10) << 8;
  }
  DAT_15a2 = (char)(uVar1 >> 8);
  if ((DAT_1003 & 0x20) == 0) {
    DAT_00e5 = DAT_00e5 | 0x80;
  }
  else {
    DAT_00e5 = DAT_00e5 & 0x7f;
  }
  DAT_0053 = bStack0000;
  if ((_DAT_140a <= (ushort)DAT_1407 * (ushort)DAT_ff2a * 8) && ((bStack0000 & 4) == 0)) {
    DAT_0053 = bStack0000 | 8;
  }
  if (((ushort)DAT_1407 * (ushort)DAT_f857 * 8 < _DAT_140a) || ((DAT_0053 & 4) != 0)) {
    DAT_00c1 = DAT_00c1 & 0xfb;
  }
  else {
    DAT_00c1 = DAT_00c1 | 4;
  }
  if (((0x95 < DAT_1407) && ((DAT_0015 & 0x80) != 0)) && ((DAT_0017 & 0x20) != 0)) {
    DAT_0086 = DAT_0086 + 1;
    if (DAT_0086 < 100) goto LAB_9b48;
    DAT_0040 = DAT_0040 | 0x20;
  }
  DAT_0086 = 0;
LAB_9b48:
  DAT_004f = DAT_004f | 0x80;
  return;
}


// ---- FUN_9b4c @ 9b4c ----

void FUN_9b4c(void)

{
  byte bVar1;
  
  bVar1 = DAT_145d;
  if (0xe0 < DAT_145d) {
    bVar1 = 0xe0;
  }
  FUN_809f(bVar1 >> 1);
  return;
}


// ---- FUN_9b5a @ 9b5a ----

void FUN_9b5a(void)

{
  bool bVar1;
  bool bVar2;
  byte bVar3;
  byte bVar4;
  
  if ((DAT_0053 & 0x40) != 0) {
    return;
  }
  if ((DAT_0094 & 0x80) == 0) {
    DAT_153d = 0xc;
    DAT_0099 = DAT_0099 | 0x10;
    if ((DAT_0094 & 0x20) == 0) {
      if (DAT_1442 < 0x50) {
        DAT_1002 = DAT_0099;
        DAT_153d = 0xc;
        return;
      }
      DAT_0094 = DAT_0094 | 0x20;
    }
    if ((DAT_0053 & 2) != 0) {
      DAT_1002 = DAT_0099;
      DAT_153d = 0xc;
      return;
    }
    DAT_0094 = DAT_0094 | 0x80;
  }
  if ((DAT_1442 == 0) || ((DAT_0054 & 1) != 0)) {
    DAT_0094 = DAT_0094 & 0x7f;
    DAT_1002 = DAT_0099;
    return;
  }
  if ((DAT_00cc & 0x10) != 0) {
    DAT_1002 = DAT_0099;
    DAT_1539 = 0;
    return;
  }
  bVar3 = DAT_1002 & 0xc;
  bVar2 = bVar3 < DAT_153d;
  bVar1 = bVar3 != DAT_153d;
  DAT_153d = bVar3;
  if (bVar1) goto LAB_9c46;
  if ((DAT_1002 & 8) == 0) {
    if ((DAT_1002 & 4) == 0) {
      bVar1 = (DAT_0094 & 0x10) == 0;
      if (bVar1) {
        DAT_1539 = 0;
        DAT_153a = 10;
        DAT_0094 = DAT_0094 & 0xf3;
        DAT_0094 = DAT_0094 | 0x10;
      }
      bVar3 = !bVar1 && bVar2;
      FUN_9cb8();
    }
    else {
      bVar1 = (DAT_0094 & 8) == 0;
      if (bVar1) {
        DAT_1539 = 0;
        DAT_153a = 10;
        DAT_0094 = DAT_0094 & 0xeb;
        DAT_0094 = DAT_0094 | 8;
      }
      bVar3 = !bVar1 && bVar2;
      FUN_9cb8();
    }
    if ((bool)(bVar3 & 1)) {
LAB_9c19:
      DAT_00cc = DAT_00cc | 0x10;
LAB_9c1c:
      DAT_0094 = DAT_0094 & 0xe7 | 4;
      goto LAB_9c46;
    }
  }
  else {
    if ((DAT_1002 & 4) == 0) {
      if ((DAT_0094 & 0x1c) != 4) {
        DAT_1539 = 0;
        DAT_153a = 100;
      }
      bVar3 = 0;
      DAT_153b = DAT_f792;
      DAT_153c = '\n';
      FUN_9cc6();
      if ((bVar3 & 1) != 0) goto LAB_9c19;
      goto LAB_9c1c;
    }
    DAT_0094 = DAT_0094 & 0xe3;
    DAT_1539 = 0;
  }
  if (DAT_153b == '\0') {
LAB_9c43:
    DAT_0094 = DAT_0094 & 0xfb;
  }
  else {
    DAT_153c = DAT_153c + -1;
    if (DAT_153c == '\0') {
      DAT_153c = '\n';
      DAT_153b = DAT_153b + -1;
      if (DAT_153b == '\0') goto LAB_9c43;
    }
    DAT_0094 = DAT_0094 | 4;
  }
LAB_9c46:
  bVar3 = DAT_0095;
  if (((DAT_00c8 & 0x20) == 0) && ((DAT_00c8 & 0x40) == 0)) {
    bVar4 = DAT_140c;
    if (((DAT_0095 & 0x80) != 0) && (bVar4 = DAT_140c - 2, DAT_140c < 2)) {
      bVar4 = 0;
    }
    if (bVar4 < DAT_f794) {
      DAT_0095 = DAT_0095 | 0x80;
    }
    else {
      DAT_0095 = DAT_0095 & 0x7f;
      bVar4 = DAT_149a;
      if (((bVar3 & 0x40) != 0) && (bVar4 = DAT_149a - 10, DAT_149a < 10)) {
        bVar4 = 0;
      }
      if (bVar4 < DAT_f795) {
        DAT_0095 = DAT_0095 | 0x40;
      }
      else {
        DAT_0095 = bVar3 & 0x3f;
        bVar4 = DAT_1460;
        if (((bVar3 & 0x20) != 0) && (bVar4 = DAT_1460 - 6, DAT_1460 < 6)) {
          bVar4 = 0;
        }
        if (bVar4 < DAT_f796) {
          DAT_0095 = DAT_0095 | 0x20;
        }
        else {
          DAT_0095 = bVar3 & 0x1f;
          if ((DAT_141d != '\0') && ((DAT_00cc & 0x10) == 0)) {
            DAT_0099 = DAT_0099 & 0xef;
            DAT_1002 = DAT_0099;
            return;
          }
        }
      }
    }
  }
  DAT_0099 = DAT_0099 | 0x10;
  DAT_1002 = DAT_0099;
  return;
}


// ---- FUN_9cb8 @ 9cb8 ----

void FUN_9cb8(byte param_1)

{
  if (DAT_1539 < param_1) {
    DAT_153a = DAT_153a + -1;
    if (DAT_153a == '\0') {
      DAT_153a = '\n';
      DAT_1539 = DAT_1539 + 1;
    }
    return;
  }
  return;
}


// ---- FUN_9cc6 @ 9cc6 ----

void FUN_9cc6(byte param_1)

{
  if (DAT_1539 < param_1) {
    DAT_153a = DAT_153a + -1;
    if (DAT_153a == '\0') {
      DAT_153a = 'd';
      DAT_1539 = DAT_1539 + 1;
    }
    return;
  }
  return;
}


// ---- FUN_9cdc @ 9cdc ----

/* WARNING: Type propagation algorithm not settling */

void FUN_9cdc(void)

{
  byte bVar1;
  
  if ((DAT_004a == 0) && (DAT_1537 != '\0')) {
    DAT_1537 = DAT_1537 + -1;
  }
  if (((DAT_004a & 0xf) == 0) && (DAT_14f0 != '\0')) {
    DAT_14f0 = DAT_14f0 + -1;
  }
  if (((DAT_0054 & 8) != 0) && ((DAT_0053 & 2) == 0)) {
    bVar1 = DAT_140c;
    if (((DAT_008f & 0x80) != 0) && (bVar1 = DAT_140c + 3, 0xfc < DAT_140c)) {
      bVar1 = 0xff;
    }
    if (bVar1 < DAT_f9fe) {
      DAT_008f = DAT_008f & 0x7f;
    }
    else {
      DAT_008f = DAT_008f | 0x80;
    }
    bVar1 = DAT_140c;
    if (((DAT_0096 & 0x80) != 0) && (bVar1 = DAT_140c + 3, 0xfc < DAT_140c)) {
      bVar1 = 0xff;
    }
    if (bVar1 < DAT_f887) {
      DAT_0096 = DAT_0096 & 0x7f;
    }
    else {
      DAT_0096 = DAT_0096 | 0x80;
    }
    bVar1 = DAT_1407;
    if (((DAT_0096 & 0x40) != 0) && (bVar1 = DAT_1407 - 2, DAT_1407 < 2)) {
      bVar1 = 0;
    }
    bVar1 = bVar1 < DAT_f888;
    if ((bool)bVar1) {
      DAT_0096 = DAT_0096 | 0x40;
    }
    else {
      DAT_0096 = DAT_0096 & 0xbf;
    }
    if ((DAT_0053 & 1) == 0) {
      DAT_0096 = DAT_0096 & 0xdf;
    }
    else if ((DAT_0096 & 0x20) == 0) {
      DAT_0096 = DAT_0096 | 0x20;
      bVar1 = DAT_14cd < DAT_f889;
      if (!(bool)bVar1) {
        DAT_14f0 = DAT_f88a;
      }
    }
    if (((DAT_fee1 & 1) == 0) || ((DAT_0053 & 1) == 0)) {
      if ((DAT_008f & 4) == 0) {
        bVar1 = DAT_1460 < DAT_f85b;
        if (!(bool)bVar1) {
          DAT_008f = DAT_008f | 4;
          DAT_1537 = DAT_f788;
        }
      }
      else {
        FUN_9e3c();
        if ((bVar1 & 1) != 0) {
          DAT_008f = DAT_008f & 0xfb;
          bVar1 = bVar1 & 0xf1;
        }
      }
      if ((DAT_00cb & 0x20) != 0) goto LAB_9da4;
      bVar1 = bVar1 & 0xf1;
      if ((DAT_008f & 8) == 0) {
        if (DAT_149a < DAT_f852) {
          bVar1 = 1;
          if ((DAT_008f & 2) != 0) {
            FUN_9e54();
            goto joined_r0x9dd0;
          }
        }
        else {
          DAT_008f = DAT_008f | 10;
          DAT_1537 = DAT_f788;
        }
      }
      else {
        FUN_9e3c();
joined_r0x9dd0:
        if ((bVar1 & 1) != 0) {
          DAT_008f = DAT_008f & 0xfd;
        }
      }
    }
    else {
LAB_9da4:
      DAT_008f = DAT_008f & 0xf5;
    }
    if ((DAT_008f & 6) == 0) {
      DAT_1537 = '\0';
      if ((DAT_0053 & 0x10) == 0) {
        DAT_14f0 = '\0';
        if (-1 < (char)DAT_0084) {
          DAT_0084 = 0;
        }
        bVar1 = DAT_0084 - 1;
        if (-1 < (char)(DAT_0084 - 1)) {
          bVar1 = DAT_0084;
        }
        DAT_0084 = bVar1;
        if ((byte)-bVar1 < DAT_ff25) {
          DAT_14f0 = 0;
          DAT_1537 = 0;
          return;
        }
        goto LAB_9e34;
      }
      if (((((DAT_0096 & 0xc0) != 0xc0) || ((DAT_0053 & 0x80) == 0)) || (DAT_14f0 == '\0')) &&
         (DAT_14f0 = '\0', (DAT_008f & 0x80) == 0)) {
        if ((char)DAT_0084 < '\0') {
          DAT_0084 = 0;
        }
        bVar1 = DAT_0084 + 1;
        if ((char)(DAT_0084 + 1) < '\0') {
          bVar1 = DAT_0084;
        }
        if (DAT_ff24 <= bVar1) {
          DAT_0049 = DAT_0049 | 1;
          DAT_0017 = DAT_0049;
          DAT_0084 = bVar1;
          DAT_14f0 = 0;
          DAT_1537 = 0;
          return;
        }
        DAT_0084 = bVar1;
        DAT_14f0 = 0;
        DAT_1537 = 0;
        return;
      }
    }
  }
  DAT_0053 = DAT_0053 & 0xef;
  DAT_0084 = -DAT_ff25;
LAB_9e34:
  DAT_0049 = DAT_0049 & 0xfe;
  DAT_0017 = DAT_0049;
  return;
}


// ---- FUN_9e3c @ 9e3c ----

void FUN_9e3c(void)

{
  byte bVar1;
  
  bVar1 = DAT_149a + 0x14;
  if (0xeb < DAT_149a) {
    bVar1 = 0xff;
  }
  if (bVar1 < DAT_f852) {
    DAT_008f = DAT_008f & 0xf7;
    FUN_9e54();
    return;
  }
  if ((DAT_1537 == '\0') && (DAT_1460 < DAT_f85c)) {
    return;
  }
  return;
}


// ---- FUN_9e54 @ 9e54 ----

void FUN_9e54(void)

{
  if (DAT_1460 < DAT_f85c) {
    return;
  }
  return;
}


// ---- FUN_9e60 @ 9e60 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9e60(void)

{
  bool bVar1;
  bool bVar2;
  char cVar3;
  char cVar4;
  char cVar5;
  char cVar6;
  byte bVar7;
  byte bVar8;
  byte bVar9;
  byte *pbVar10;
  short sVar11;
  
  cVar6 = DAT_14fa;
  cVar5 = DAT_14da;
  cVar4 = DAT_14d9;
  cVar3 = DAT_14d2;
  if (((short)((ushort)DAT_14d0 << 8) < 0) && (DAT_14d0 = DAT_14d0 + 1, DAT_14d0 == 0)) {
    DAT_14d0 = 0xff;
  }
  if (((short)((ushort)DAT_0081 << 8) < 0) && (DAT_0081 = DAT_0081 + 1, DAT_0081 == 0)) {
    DAT_0081 = 0xff;
  }
  if ((DAT_0053 & 1) == 0) {
    DAT_14da = '\0';
    DAT_14d9 = DAT_14d9 + '\x01';
    if (DAT_14d9 == '\0') {
      DAT_14d9 = cVar4;
    }
    DAT_14fa = DAT_14fa + '\x01';
    if (DAT_14fa == '\0') {
      DAT_14fa = cVar6;
    }
  }
  else {
    DAT_14d9 = '\0';
    DAT_14fa = '\0';
    DAT_14da = DAT_14da + '\x01';
    if (DAT_14da == '\0') {
      DAT_14da = cVar5;
    }
  }
  bVar7 = DAT_004a + 1;
  bVar1 = (0xfe < DAT_004a || 9 < bVar7 >> 4) || 8 < bVar7 >> 4 && 9 < (bVar7 & 0xf);
  bVar2 = (byte)((DAT_004a & 0xf) + 1) >> 4 == 1 || 9 < (bVar7 & 0xf);
  if (bVar1 && bVar2) {
    bVar7 = DAT_004a + 0x67;
  }
  else if (bVar1) {
    bVar7 = DAT_004a + 0x61;
  }
  else if (bVar2) {
    bVar7 = DAT_004a + 7;
  }
  DAT_004a = bVar7;
  if (bVar7 == 0) {
    DAT_009a = DAT_009a + '\x01';
    if (DAT_009a == '\0') {
      DAT_009a = -1;
    }
    if ((0x3d < DAT_00bf) && (DAT_0065 = DAT_0065 + 1, 2 < DAT_0065)) {
      DAT_0065 = 0;
      DAT_00bf = DAT_00bf - 1;
    }
    if (((short)((ushort)DAT_0082 << 8) < 0) && (DAT_0082 = DAT_0082 + 1, DAT_0082 == 0)) {
      DAT_0082 = 0xff;
    }
    if (((short)((ushort)DAT_00b4 << 8) < 0) && (DAT_00b4 = DAT_00b4 + 1, DAT_00b4 == 0)) {
      DAT_00b4 = 0xff;
    }
    if (DAT_1481 != '\0') {
      DAT_1481 = DAT_1481 + -1;
    }
    if (DAT_159b != '\0') {
      DAT_159b = DAT_159b + -1;
    }
    if (((DAT_00c2 & 0x80) != 0) && (DAT_159a < DAT_f87d)) {
      DAT_159a = DAT_159a + 1;
    }
  }
  else if ((bVar7 & 0xf) != 0) {
    return;
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
  DAT_1454 = DAT_1454 + '\x01';
  if (DAT_1454 == '\0') {
    DAT_1454 = -1;
  }
  if ((DAT_14ab != 0xff) &&
     (bVar1 = CARRY1(DAT_14ab,DAT_f85a), DAT_14ab = DAT_14ab + DAT_f85a, bVar1)) {
    DAT_14ab = 0xff;
  }
  DAT_1439 = DAT_1439 + '\x01';
  if (DAT_1439 == '\0') {
    DAT_1439 = -1;
  }
  DAT_1450 = DAT_1450 + '\x01';
  if (DAT_1450 == '\0') {
    DAT_1450 = -1;
  }
  DAT_1591 = DAT_1591 + '\x01';
  if (DAT_1591 == '\0') {
    DAT_1591 = -1;
  }
  DAT_1526 = DAT_1526 + '\x01';
  if (DAT_1526 == '\0') {
    DAT_1526 = -1;
  }
  DAT_1438 = DAT_1438 + '\x01';
  if (DAT_1438 == '\0') {
    DAT_1438 = -1;
  }
  if (DAT_159c != '\0') {
    DAT_159c = DAT_159c + -1;
  }
  DAT_14a5 = DAT_14a5 + '\x01';
  if (DAT_14a5 == '\0') {
    DAT_14a5 = -1;
  }
  if (((short)((ushort)DAT_1473 << 8) < 0) && ((byte)(DAT_1473 + 1) != 0)) {
    DAT_1473 = DAT_1473 + 1;
  }
  if (((short)((ushort)DAT_0085 << 8) < 0) && ((byte)(DAT_0085 + 1) != 0)) {
    DAT_0085 = DAT_0085 + 1;
  }
  if ((DAT_0054 & 1) == 0) {
    DAT_1475 = 0;
    DAT_0049 = DAT_0049 | 0x80;
    DAT_0017 = DAT_0049;
  }
  else {
    DAT_1475 = DAT_1475 + 1;
    if (0x3b < DAT_1475) {
      pbVar10 = (byte *)0x1641;
      bVar9 = 0;
      bVar8 = 0;
      _DAT_1642 = 0;
      DAT_1647 = 0;
      do {
        pbVar10 = pbVar10 + 1;
        bVar1 = CARRY1(bVar9,*pbVar10);
        bVar9 = bVar9 + *pbVar10;
        bVar8 = bVar8 + bVar1;
      } while (pbVar10 != (byte *)0x177f);
      _DAT_1640 = CONCAT11(~bVar8,~bVar9) + 1;
      DAT_0049 = DAT_0049 & 0x7f;
      DAT_0017 = DAT_0049;
      RAMCR = RAMCR & 0xfe;
      TCSR = TCSR & 0xe3;
      P3SCR = P3SCR & 0xf7;
      do {
        sVar11 = 0;
        do {
          sVar11 = sVar11 + 1;
        } while (sVar11 != 0xb6e);
        DAT_0083 = DAT_0083 ^ 0x80;
      } while ((DAT_0015 & 0x10) == 0);
      DAT_1003 = DAT_0083;
      vec_RESET();
      return;
    }
  }
  if (((DAT_0044 & 8) == 0) && (0x77 < DAT_1442)) {
    DAT_0044 = DAT_0044 | 10;
  }
  if (((DAT_0044 & 4) == 0) && (9 < DAT_1407)) {
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


// ---- FUN_a01d @ a01d ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a01d(void)

{
  undefined2 *puVar1;
  
  if ((DAT_0054 & 8) != 0) {
    if (_DAT_140a == 0) {
      DAT_14c8 = 0;
    }
    DAT_0056 = DAT_0056 + 1;
    if (0x95 < DAT_0056) {
      _DAT_1058 = 0;
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
      } while (puVar1 != (undefined2 *)&DAT_1640);
      _DAT_013e = 0xb1fa;
      FUN_b20d();
      _DAT_013e = 0xb1fd;
      FUN_b23c();
      _DAT_013e = 0xb200;
      FUN_b343();
      _DAT_013e = 0xb204;
      FUN_b4d8();
      _DAT_013e = 0xb207;
      FUN_b59b();
      _DAT_013e = 0xb20a;
      FUN_b4bd();
      FUN_b497();
      return;
    }
  }
  return;
}


// ---- FUN_a04d @ a04d ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a04d(void)

{
  byte bVar1;
  ushort uVar2;
  byte extraout_B;
  byte extraout_B_00;
  
  DAT_1595 = DAT_143b;
  if ((byte)(DAT_1580 + 1) != 0) {
    DAT_1580 = DAT_1580 + 1;
  }
  bVar1 = DAT_00c1 & 0xd7;
  if ((DAT_00c1 & 0x10) != 0) {
    bVar1 = bVar1 | 8;
  }
  if ((DAT_0053 & 4) == 0) {
    if ((((DAT_1580 < DAT_f842) || ((DAT_0053 & 1) != 0)) || (DAT_1460 < DAT_f849)) ||
       ((DAT_f84a <= DAT_1460 ||
        ((DAT_1582 <= DAT_1581 && (DAT_f84d <= (byte)(DAT_1581 - DAT_1582))))))) goto LAB_a0ad;
    DAT_00c1 = bVar1;
    if ((bVar1 & 0x80) == 0) {
      if ((((DAT_f843 <= DAT_140c) && (DAT_140c < DAT_f844)) &&
          ((DAT_f845 <= DAT_1407 && ((DAT_1407 < DAT_f846 && ((bVar1 & 4) == 0)))))) &&
         (((DAT_14d9 < DAT_f847 && (DAT_f848 <= DAT_149a)) ||
          (((DAT_151d <= DAT_151b && (DAT_f84e <= (byte)(DAT_151b - DAT_151d))) &&
           (DAT_158e < DAT_f84f)))))) {
        DAT_00c1 = bVar1 | 0x80;
      }
      goto LAB_a103;
    }
    DAT_1592 = DAT_1592 + 1;
    if (DAT_1592 <= DAT_f84c) goto LAB_a103;
    if (DAT_f84b < DAT_1592) goto LAB_a0ad;
  }
  else {
    DAT_1580 = 0;
LAB_a0ad:
    DAT_1593 = 0;
    DAT_1594 = '\0';
    DAT_1592 = 0;
    DAT_00c1 = bVar1 & 0x3f;
LAB_a103:
    DAT_00c1 = DAT_00c1 | 0x20;
  }
  uVar2 = _DAT_140a - _DAT_158b;
  if (_DAT_140a < _DAT_158b) {
    bVar1 = DAT_00c1 | 0x10;
    if (((DAT_00c1 & 0x20) == 0) && ((DAT_00c1 & 0x40) != 0)) {
      if ((short)uVar2 < -0x80) {
        uVar2 = 0xff80;
      }
      DAT_1594 = (char)uVar2;
      DAT_00c1 = bVar1;
      FUN_a192();
      DAT_1593 = extraout_B_00;
      if (DAT_f850 < extraout_B_00) {
        DAT_1593 = DAT_f850;
      }
      DAT_1595 = DAT_1593 + DAT_1595;
      bVar1 = DAT_00c1;
    }
  }
  else {
    if (uVar2 != 0) {
      DAT_00c1 = DAT_00c1 & 0xef;
    }
    bVar1 = DAT_00c1;
    if ((DAT_00c1 & 0x20) == 0) {
      if ((DAT_00c1 & 0x40) == 0) {
        if ((DAT_00c1 & 8) == 0) goto LAB_a185;
        DAT_00c1 = DAT_00c1 | 0x40;
      }
      if (0x7f < uVar2) {
        uVar2 = 0x7f;
      }
      DAT_1594 = (char)uVar2;
      FUN_a192();
      bVar1 = extraout_B;
      if (0x80 < extraout_B) {
        bVar1 = 0x80;
      }
      DAT_1593 = -bVar1;
      if ((short)((ushort)(byte)(DAT_1593 - DAT_f851) << 8) < 0 != SBORROW1(DAT_1593,DAT_f851)) {
        DAT_1593 = DAT_f851;
      }
      DAT_1595 = DAT_1593 + DAT_1595;
      bVar1 = DAT_00c1;
    }
  }
LAB_a185:
  DAT_00c1 = bVar1;
  _DAT_1596 = CONCAT11(DAT_1594 + -0x80,DAT_1593 + 0x80);
  return;
}


// ---- FUN_a192 @ a192 ----

void FUN_a192(undefined1 param_1,byte param_2)

{
  short sVar1;
  byte bStack0000;
  
  bStack0000 = param_2;
  DAT_158f = FUN_809f();
  sVar1 = (ushort)DAT_158f * (ushort)bStack0000 * 0x10;
  if ((char)((ushort)sVar1 >> 8) != '\0') {
    sVar1 = 0xff;
  }
  bStack0000 = (byte)sVar1;
  DAT_1590 = FUN_809f();
  return;
}


// ---- FUN_a1cc @ a1cc ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_a1cc(void)

{
  undefined2 uVar1;
  undefined2 uVar2;
  char cVar3;
  byte bVar4;
  ushort uVar5;
  char cVar6;
  byte bVar7;
  short *psVar8;
  
  if (((DAT_004a & 0xf) == 0) && ((byte)(DAT_152f + 1) != 0)) {
    DAT_152f = DAT_152f + 1;
  }
  if ((DAT_0053 & 1) != 0) {
    DAT_007d = DAT_007d & 0xf7;
  }
  if ((DAT_007d & 8) == 0) {
    DAT_152f = 0;
    if ((DAT_1460 < DAT_feff) || (DAT_1413 < DAT_ff74)) {
      DAT_007f = DAT_007f & 0xef;
    }
    else {
      DAT_007f = DAT_007f | 0x10;
    }
    DAT_0088 = DAT_0088 & 0xdf;
  }
  else {
    DAT_007f = DAT_007f & 0xef;
    if ((DAT_0088 & 0x20) == 0) {
      _DAT_1461 = _DAT_1463;
      if (DAT_fa14 < DAT_1460) {
        _DAT_1461 = _DAT_152d;
      }
      DAT_0088 = DAT_0088 | 0x20;
      DAT_152f = 0;
    }
    if ((char)DAT_152f < '\0') {
      if (0x89 < DAT_152f) goto LAB_a217;
    }
    else if (DAT_fa13 <= DAT_152f) {
LAB_a217:
      DAT_152f = 0x80;
      psVar8 = (short *)&DAT_1463;
      if (DAT_fa14 < DAT_1460) {
        psVar8 = (short *)&DAT_152d;
      }
      uVar5 = *psVar8 + _DAT_1461;
      *psVar8 = CONCAT11((char)((short)uVar5 >> 9),
                         (char)uVar5 >> 1 | (char)((uVar5 & 0x101) >> 8) << 7);
      FUN_a3e6();
    }
  }
  uVar1 = _DAT_14eb;
  cVar6 = DAT_0080;
  DAT_0080 = 0;
  if (((((DAT_0053 & 2) == 0) && (0x7c < DAT_1404)) && (DAT_1460 != 0)) && (DAT_1460 < 100)) {
    if ((DAT_007f & 0x20) == 0) {
      _DAT_1461 = (ushort)DAT_ffc5 << 8;
      DAT_00ca = DAT_00ca | 0x10;
      DAT_00c5 = DAT_00c5 | 0x10;
      DAT_00d7 = DAT_00d7 | 0x10;
      DAT_007f = DAT_007f & 0x6f;
      DAT_165b = 0;
      goto LAB_a306;
    }
    DAT_00ca = DAT_00ca & 0xef;
  }
  for (; cVar6 != '\0'; cVar6 = cVar6 + -1) {
    _DAT_1461 = _DAT_1461 - _DAT_ffb8;
  }
  if ((DAT_004a & 0xf) == 0) {
    _DAT_1461 = _DAT_1461 + 0x1a;
  }
  if (((DAT_007d & 8) != 0) && (DAT_fa14 < DAT_1460)) {
    if ((DAT_007f & 0x80) == 0) {
      if (DAT_f932 < DAT_152d) {
        DAT_007f = DAT_007f | 0x80;
      }
    }
    else if (DAT_152d <= DAT_f931) {
      DAT_007f = DAT_007f & 0x7f;
    }
  }
  if ((DAT_0093 & 8) == 0) {
LAB_a306:
    FUN_a322((char)((ushort)_DAT_14eb >> 8),(char)_DAT_14eb,(ushort)DAT_145f << 8);
    uVar2 = _DAT_14ed;
    _DAT_14eb = uVar1;
    FUN_a322((char)((ushort)_DAT_14ed >> 8),(char)_DAT_14ed,(ushort)DAT_145e << 8);
    _DAT_14ed = uVar2;
    FUN_a344();
    return;
  }
  DAT_0093 = DAT_0093 & 0xf7;
  cVar6 = (char)((ushort)_DAT_1461 >> 8);
  DAT_1461 = cVar6 + DAT_14f6;
  if (SCARRY1(cVar6,DAT_14f6)) {
    if (DAT_1461 < '\0') {
      DAT_1462 = 0xff;
      DAT_1461 = '\x7f';
    }
    else {
      DAT_1462 = 0;
      DAT_1461 = -0x80;
    }
  }
  _DAT_1463 = 0;
  _DAT_152d = 0;
  _DAT_14c5 = 0;
  cVar6 = DAT_1595 - DAT_14aa;
  if (DAT_1595 < DAT_14aa) {
    DAT_14aa = DAT_1595;
    cVar6 = '\0';
  }
  cVar6 = cVar6 + DAT_1461;
  if (((DAT_0054 & 8) != 0) && ((DAT_00d2 & 4) != 0)) {
    bVar4 = DAT_16a9;
    if ((char)DAT_16a9 < '\0') {
      if (DAT_16a9 < 0xf6) {
        bVar4 = 0xf6;
      }
    }
    else if (10 < DAT_16a9) {
      bVar4 = 10;
    }
    cVar6 = bVar4 + cVar6;
  }
  if ((DAT_fee1 & 0x10) == 0) {
    cVar3 = 'F';
  }
  else {
    cVar3 = 'n';
  }
  bVar4 = cVar3 - cVar6;
  if (cVar3 < cVar6) {
    bVar4 = 0;
  }
  bVar7 = DAT_1410 - DAT_ff8e;
  if (DAT_1410 < DAT_ff8e) {
    bVar7 = 0;
  }
  uVar5 = (ushort)bVar7;
  if (bVar7 <= bVar4) {
    if (((DAT_0053 & 2) == 0) && ((DAT_0053 & 1) != 0)) {
      bVar7 = DAT_1410 + DAT_ff26;
    }
    else {
      bVar7 = DAT_1410 + 10;
    }
    uVar5 = CONCAT11(bVar4,bVar7);
    if (bVar4 < bVar7) goto LAB_a3d4;
  }
  uVar5 = uVar5 << 8;
LAB_a3d4:
  DAT_140f = (byte)(uVar5 >> 8);
  if (0x77 < DAT_140f) {
    DAT_140f = 0x77;
  }
  DAT_14ea = DAT_1461 + -0x80;
  return;
}


// ---- FUN_a322 @ a322 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a322(ushort param_1)

{
  ushort in_D;
  
  _DAT_005b = in_D;
  if (param_1 != in_D) {
    if (param_1 < in_D) {
      _DAT_005b = in_D;
      if (_DAT_f9fc <= in_D) {
        _DAT_005b = in_D - _DAT_f9fc;
      }
    }
    else {
      _DAT_005b = in_D;
      if (!CARRY2(in_D,_DAT_f9fc)) {
        _DAT_005b = in_D + _DAT_f9fc;
      }
    }
  }
  return;
}


// ---- FUN_a344 @ a344 ----

/* WARNING: Removing unreachable block (RAM,0xa3d8) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a344(void)

{
  if ((DAT_007f & 0x10) != 0) {
    _DAT_1461 = _DAT_14c5;
  }
  if (-DAT_1461 == DAT_14eb || -DAT_14eb < DAT_1461) {
    if ((char)DAT_14ed < DAT_1461) {
      _DAT_1461 = (ushort)DAT_14ed << 8;
    }
  }
  else {
    _DAT_1461 = (ushort)(byte)-DAT_14eb << 8;
  }
  if (DAT_1595 < DAT_14aa) {
    DAT_14aa = DAT_1595;
  }
  DAT_140f = 0;
  DAT_14ea = DAT_1461 + -0x80;
  return;
}


// ---- FUN_a3e6 @ a3e6 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a3e6(void)

{
  char cVar1;
  char extraout_B;
  char extraout_B_00;
  short sVar2;
  
  _DAT_005b = _DAT_1463;
  if (_DAT_1463 < 0) {
    _DAT_005b = CONCAT11(-((char)((ushort)_DAT_1463 >> 8) + ((char)-(char)_DAT_1463 != '\0')),
                         -(char)_DAT_1463);
  }
  cVar1 = FUN_82b9();
  _DAT_0060 = CONCAT11(cVar1,extraout_B);
  if (_DAT_1463 < 0) {
    _DAT_0060 = CONCAT11(-(cVar1 + (-extraout_B != '\0')),-extraout_B);
  }
  _DAT_005b = _DAT_152d;
  if (_DAT_152d < 0) {
    _DAT_005b = CONCAT11(-((char)((ushort)_DAT_152d >> 8) + ((char)-(char)_DAT_152d != '\0')),
                         -(char)_DAT_152d);
  }
  cVar1 = FUN_82b9();
  sVar2 = CONCAT11(cVar1,extraout_B_00);
  if (_DAT_152d < 0) {
    sVar2 = CONCAT11(-(cVar1 + (-extraout_B_00 != '\0')),-extraout_B_00);
  }
  _DAT_14c5 = sVar2 + _DAT_0060;
  return;
}


// ---- FUN_a422 @ a422 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a422(void)

{
  bool bVar1;
  byte bVar2;
  byte bVar3;
  byte bVar4;
  
  if ((DAT_0054 & 8) == 0) {
    return;
  }
  if ((DAT_008f & 0x40) == 0) {
    DAT_008f = DAT_008f | 0x40;
    DAT_1445 = FUN_809f();
  }
  DAT_1598 = 0;
  bVar2 = DAT_16ab;
  if (((DAT_00d2 & 0x10) != 0) || (((DAT_00d3 & 0x10) != 0 && (bVar2 = 0, DAT_16b3 == '\0'))))
  goto LAB_a5f5;
  if ((DAT_0053 & 2) == 0) {
    if (DAT_157a == '\0') {
      DAT_1579 = DAT_1579 + '\x01';
      if (DAT_1579 == '\0') {
        DAT_1579 = -1;
      }
      DAT_157a = '\n';
    }
    DAT_157a = DAT_157a + -1;
  }
  else {
    DAT_1579 = '\0';
    DAT_157a = '\n';
  }
  if ((DAT_007e & 1) == 0) {
    FUN_a600();
    if ((DAT_0053 & 2) == 0) {
      FUN_a732();
      DAT_1599 = FUN_809f();
      if ((DAT_0053 & 1) == 0) {
        FUN_a77e();
LAB_a4aa:
        _DAT_146a = 0;
        DAT_0096 = DAT_0096 & 0xef;
LAB_a4b3:
        DAT_008f = DAT_008f & 0xfe;
        DAT_14be = 0;
        DAT_157e = 0;
        FUN_a8b4();
      }
      else {
        FUN_a78b();
        if (((DAT_0053 & 4) == 0) && (DAT_f7bc <= DAT_1407)) goto LAB_a4aa;
        if ((DAT_0096 & 0x10) == 0) {
          DAT_0096 = DAT_0096 | 0x10;
          bVar2 = FUN_809f();
          _DAT_14f7 = (ushort)bVar2 * 10;
        }
        if (_DAT_146a < _DAT_14f7) {
          _DAT_146a = _DAT_146a + 1;
          bVar2 = DAT_143f + DAT_f882;
          if (CARRY1(DAT_143f,DAT_f882)) {
            bVar2 = 0xff;
          }
          if (DAT_1442 <= bVar2) {
            _DAT_146a = _DAT_14f7;
            bVar1 = CARRY1(DAT_1445,DAT_1446);
            DAT_1445 = DAT_1445 + DAT_1446;
            if (bVar1) {
              DAT_1445 = 0xff;
            }
            DAT_1446 = 0;
            goto LAB_a51d;
          }
          goto LAB_a4b3;
        }
LAB_a51d:
        DAT_008f = DAT_008f | 1;
        DAT_157f = 0;
        FUN_a990();
        FUN_a87c();
        if (DAT_143f < DAT_1442) {
          if (2 < (byte)(DAT_1442 - DAT_143f)) {
            FUN_a80c();
            if (DAT_1449 == '\0') {
              if (DAT_1445 != 0) {
                DAT_1445 = DAT_1445 - 1;
              }
              DAT_1449 = DAT_ffad;
              if ((DAT_f7b9 <= (byte)(DAT_1442 - DAT_143f)) &&
                 (DAT_1449 = DAT_ffba, DAT_f7ba <= (byte)(DAT_1442 - DAT_143f))) {
                DAT_1449 = DAT_f7bb;
              }
            }
            DAT_1449 = DAT_1449 + -1;
            goto LAB_a58a;
          }
        }
        else if (2 < (byte)-(DAT_1442 - DAT_143f)) {
          FUN_a7bd();
          goto LAB_a549;
        }
      }
      DAT_1448 = 0;
      goto LAB_a58a;
    }
    DAT_008f = DAT_008f & 0xfe;
    bVar2 = DAT_f853;
  }
  else {
LAB_a549:
    if (DAT_1449 == '\0') {
      FUN_a7ed();
    }
    DAT_1449 = DAT_1449 + -1;
LAB_a58a:
    bVar2 = 0;
    bVar3 = DAT_fa04;
    if ((DAT_008f & 1) != 0) {
      bVar2 = DAT_fa05;
      bVar3 = DAT_1599;
    }
    if (bVar3 < DAT_1445) {
      DAT_1445 = bVar3;
    }
    if (DAT_1445 < bVar2) {
      DAT_1445 = bVar2;
    }
    FUN_a836();
    FUN_a8c1();
    bVar3 = DAT_157b + DAT_1448;
    bVar2 = DAT_fa04;
    if (((((!CARRY1(DAT_157b,DAT_1448)) && (bVar3 < DAT_fa04)) &&
         (bVar4 = bVar3 + DAT_1446, !CARRY1(bVar3,DAT_1446))) &&
        ((bVar4 < DAT_fa04 && (bVar3 = bVar4 + DAT_157e, !CARRY1(bVar4,DAT_157e))))) &&
       ((bVar3 < DAT_fa04 && (bVar2 = bVar3, bVar3 < DAT_fa05)))) {
      bVar2 = DAT_fa05;
    }
    if ((bVar2 < DAT_157f) && (bVar2 = DAT_157f, DAT_fa04 < DAT_157f)) {
      bVar2 = DAT_fa04;
    }
  }
  if ((DAT_00d2 & 0x10) != 0) {
    bVar2 = DAT_16ab;
  }
LAB_a5f5:
  DAT_14cd = bVar2;
  _DAT_1060 = (ushort)bVar2 << 2;
  return;
}


// ---- FUN_a600 @ a600 ----

/* WARNING: Removing unreachable block (RAM,0xa71e) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a600(void)

{
  byte bVar1;
  short sVar2;
  
  if (_DAT_140a == 0) {
LAB_a62b:
    DAT_1440 = 0;
  }
  else {
    sVar2 = _DAT_1440 + 1;
    DAT_1440 = (byte)((ushort)sVar2 >> 8);
    if ((short)((ushort)DAT_1440 << 8) < 0) {
      if (DAT_1440 < 0xf6) {
        DAT_0053 = DAT_0053 | 0x20;
        _DAT_1440 = sVar2;
        goto LAB_a631;
      }
      goto LAB_a62b;
    }
    if (((DAT_0053 & 2) != 0) || (0x96 < DAT_1404)) goto LAB_a62b;
    DAT_1440 = DAT_1440 + 1;
  }
  _DAT_1440 = (ushort)DAT_1440 << 8;
LAB_a631:
  FUN_809f();
  if ((((DAT_0053 & 0x10) != 0) || ((DAT_008f & 0x80) != 0)) && ((DAT_0053 & 0x44) != 0)) {
    bVar1 = DAT_140c;
    if (((DAT_0064 & 0x80) != 0) && (bVar1 = DAT_140c + 5, 0xfa < DAT_140c)) {
      bVar1 = 0xff;
    }
    if (bVar1 < DAT_f87a) {
      DAT_0064 = DAT_0064 & 0x7f;
    }
    else {
      DAT_0064 = DAT_0064 | 0x80;
    }
  }
  bVar1 = DAT_1401 & 0xe0;
  if (bVar1 < DAT_1469) {
    bVar1 = DAT_1401 + 10 & 0xe0;
  }
  DAT_1469 = bVar1;
  DAT_143f = 0;
  return;
}


// ---- FUN_a732 @ a732 ----

void FUN_a732(void)

{
  bool bVar1;
  byte bVar2;
  
  bVar2 = DAT_1442;
  if (((DAT_00ba & 2) == 0) && (bVar2 = DAT_1442 - 0x10, DAT_1442 < 0x10)) {
    bVar2 = 0;
  }
  if (DAT_f783 < bVar2) {
    bVar2 = 0;
    DAT_00ba = DAT_00ba | 2;
  }
  else {
    DAT_00ba = DAT_00ba & 0xfd;
    if (((DAT_0053 & 0x44) == 0) || (bVar2 = 0, (DAT_0053 & 0x10) != 0)) {
      bVar2 = FUN_809f();
    }
    if (((DAT_0053 & 0x80) != 0) &&
       (bVar1 = CARRY1(bVar2,DAT_f781), bVar2 = bVar2 + DAT_f781, bVar1)) {
      bVar2 = 0xff;
    }
  }
  DAT_1443 = bVar2;
  return;
}


// ---- FUN_a77e @ a77e ----

void FUN_a77e(undefined1 param_1,undefined1 param_2)

{
  DAT_1446 = FUN_80a9(DAT_1544,param_2,0xf7c0);
  return;
}


// ---- FUN_a78b @ a78b ----

void FUN_a78b(void)

{
  byte bVar1;
  
  bVar1 = DAT_140c;
  if ((DAT_00ba & 0x80) != 0) {
    bVar1 = DAT_140c + 5;
  }
  if (bVar1 < 0x62) {
    DAT_1446 = '\0';
    DAT_00ba = DAT_00ba & 0x7f;
  }
  else {
    DAT_00ba = DAT_00ba | 0x80;
  }
  if (DAT_1446 != '\0') {
    if (DAT_1447 == '\0') {
      DAT_1447 = DAT_ffab;
      DAT_1446 = DAT_1446 + -1;
    }
    else {
      DAT_1447 = DAT_1447 + -1;
    }
  }
  return;
}


// ---- FUN_a7bd @ a7bd ----

void FUN_a7bd(void)

{
  ushort in_D;
  ushort uVar1;
  short sVar2;
  
  DAT_005b = DAT_1599 - DAT_1445;
  if (DAT_1599 < DAT_1445) {
    DAT_005b = 0;
  }
  uVar1 = (in_D >> 10) * (in_D >> 10);
  if ((char)(uVar1 >> 8) != '\0') {
    uVar1 = 0xff;
  }
  sVar2 = (ushort)DAT_ffac * (uVar1 & 0xff);
  if (((SUB21((ushort)sVar2 >> 0xf,0)) ||
      (DAT_1448 = (byte)((ushort)(sVar2 * 4) >> 8), SUB21((ushort)(sVar2 * 2) >> 0xf,0))) ||
     (DAT_005b <= DAT_1448)) {
    DAT_1448 = DAT_005b;
  }
  if (DAT_14be <= DAT_1448) {
    DAT_14be = DAT_1448;
  }
  return;
}


// ---- FUN_a7ed @ a7ed ----

void FUN_a7ed(void)

{
  DAT_1445 = DAT_1445 + '\x01';
  if (DAT_1445 == '\0') {
    DAT_1445 = -1;
  }
  DAT_1449 = DAT_ffad;
  if (DAT_f7b9 <= (byte)(DAT_143f - DAT_1442)) {
    DAT_1449 = DAT_ffba;
  }
  return;
}


// ---- FUN_a80c @ a80c ----

void FUN_a80c(void)

{
  bool bVar1;
  
  DAT_1448 = 0;
  if ((DAT_00ba & 4) == 0) {
    DAT_00ba = DAT_00ba | 4;
  }
  else if (((DAT_1471 < '\0') && (DAT_ffa6 <= (byte)-DAT_1471)) &&
          (bVar1 = CARRY1(DAT_14be >> 1,DAT_1445), DAT_1445 = (DAT_14be >> 1) + DAT_1445, bVar1)) {
    DAT_1445 = 0xff;
  }
  DAT_14be = 0;
  return;
}


// ---- FUN_a836 @ a836 ----

void FUN_a836(void)

{
  DAT_14f9 = FUN_809f();
  if ((DAT_008f & 1) == 0) {
    if (DAT_1445 < DAT_ffbd) {
      if (DAT_1444 == '\0') {
        DAT_1444 = DAT_f854;
        DAT_1445 = DAT_1445 + 1;
        return;
      }
    }
    else {
      if (DAT_1445 <= DAT_14f9) goto LAB_a854;
      if (DAT_1444 == '\0') {
        DAT_1444 = DAT_f7bd;
        DAT_1445 = DAT_1445 - 1;
        return;
      }
    }
    DAT_1444 = DAT_1444 + -1;
  }
  else {
LAB_a854:
    DAT_1444 = '\0';
  }
  return;
}


// ---- FUN_a87c @ a87c ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a87c(void)

{
  char cVar1;
  char extraout_B;
  
  if (_DAT_1563 + 0x10 < _DAT_1577) {
    _DAT_005b = _DAT_1563 - _DAT_1577;
    if (_DAT_1563 < _DAT_1577) {
      _DAT_005b = CONCAT11(~(byte)((ushort)_DAT_005b >> 8) + (0xfe < (byte)~(byte)_DAT_005b),
                           ~(byte)_DAT_005b + 1);
    }
    _DAT_005b = _DAT_005b << 3;
    cVar1 = FUN_82b9();
    if ((cVar1 != '\0') || (DAT_157e = DAT_005d, extraout_B != '\0')) {
      DAT_157e = 0xff;
    }
  }
  else {
    DAT_157e = 0;
  }
  return;
}


// ---- FUN_a8b4 @ a8b4 ----

void FUN_a8b4(undefined1 param_1,undefined1 param_2)

{
  DAT_157f = FUN_809f(DAT_1544,param_2,0xfb80);
  return;
}


// ---- FUN_a8c1 @ a8c1 ----

void FUN_a8c1(void)

{
  byte bVar1;
  
  bVar1 = DAT_1445 + DAT_1443;
  if (CARRY1(DAT_1445,DAT_1443)) {
    bVar1 = 0xff;
  }
  DAT_157b = bVar1;
  if (((((DAT_0053 & 1) == 0) || ((DAT_0015 & 0x20) == 0)) || (DAT_1407 < DAT_f9f4)) ||
     ((DAT_0094 & 4) != 0)) {
LAB_a909:
    DAT_008f = DAT_008f & 0xcf;
    DAT_157d = 0;
    DAT_157c = 0;
    return;
  }
  if ((DAT_008f & 0x10) == 0) {
    if (DAT_1407 < DAT_f9f5) {
      return;
    }
    if (DAT_140c < DAT_f9f6) {
      return;
    }
    if (DAT_f9f7 <= DAT_140c) {
      return;
    }
    if (CARRY1(DAT_143f,DAT_f9f8)) {
      return;
    }
    if (DAT_1442 <= (byte)(DAT_143f + DAT_f9f8)) goto LAB_a909;
    DAT_008f = DAT_008f & 0xdf | 0x10;
  }
  else {
    if ((DAT_008f & 0x20) != 0) {
LAB_a963:
      if (DAT_157d == 0) {
        return;
      }
      if (DAT_157c == '\0') {
        DAT_157d = DAT_157d - 1;
        if (DAT_157d == 0) {
          DAT_008f = DAT_008f & 0xef;
          return;
        }
        DAT_157c = DAT_fa03;
      }
      DAT_157c = DAT_157c + -1;
      if (DAT_157d <= bVar1) {
        DAT_157b = bVar1 - DAT_157d;
        return;
      }
      DAT_157b = 0;
      DAT_157d = bVar1;
      return;
    }
    if (((DAT_1407 < DAT_fa01) || (DAT_1442 <= (byte)(DAT_143f + DAT_fa02))) ||
       ((DAT_008f & 1) != 0)) {
      DAT_008f = DAT_008f | 0x20;
      goto LAB_a963;
    }
  }
  if (DAT_157c == '\0') {
    DAT_157d = DAT_157d + 1;
    if (DAT_f9f9 < DAT_157d) {
      DAT_157d = DAT_f9f9;
      goto LAB_a937;
    }
    DAT_157c = DAT_fa00;
  }
  DAT_157c = DAT_157c + -1;
LAB_a937:
  DAT_157b = bVar1 - DAT_157d;
  if (bVar1 < DAT_157d) {
    DAT_157b = '\0';
    DAT_157d = bVar1;
  }
  return;
}


// ---- FUN_a990 @ a990 ----

void FUN_a990(void)

{
  byte bVar1;
  
  if (DAT_1401 < 0xe0) {
    bVar1 = DAT_143f - DAT_1442;
    if (DAT_143f < DAT_1442) {
      bVar1 = -bVar1;
      if (0xf < bVar1) {
        bVar1 = 0xf;
      }
      DAT_151a = (&DAT_f990)[bVar1];
      bVar1 = FUN_809f();
      if (DAT_151a < bVar1) {
        bVar1 = DAT_151a;
      }
      DAT_1598 = -bVar1;
    }
    else {
      if (0xf < bVar1) {
        bVar1 = 0xf;
      }
      DAT_1519 = (&DAT_f980)[bVar1];
      DAT_1598 = FUN_809f();
      if (DAT_1519 < DAT_1598) {
        DAT_1598 = DAT_1519;
      }
    }
  }
  else {
    DAT_1598 = 0;
  }
  return;
}


// ---- FUN_a9f4 @ a9f4 ----

/* WARNING: Removing unreachable block (RAM,0xac36) */
/* WARNING: Removing unreachable block (RAM,0xac3e) */
/* WARNING: Removing unreachable block (RAM,0xac3f) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: RAM */

void FUN_a9f4(void)

{
  ushort uVar1;
  byte bVar2;
  ushort uVar3;
  byte extraout_B;
  byte bVar4;
  
  if ((DAT_0041 & 1) == 0) {
    if ((DAT_0041 & 0x80) == 0) {
      DAT_1683 = 0;
    }
    else {
      DAT_1683 = DAT_1683 + 1;
      if (0x80 < DAT_1683) {
        DAT_0042 = DAT_0042 | 2;
        FUN_af72();
      }
    }
  }
  else if ((DAT_0041 & 0x80) == 0) {
    DAT_1683 = 0;
  }
  else {
    DAT_1683 = DAT_1683 + 1;
    if (0x80 < DAT_1683) {
      DAT_0041 = DAT_0041 & 0x7f;
    }
  }
  if (((DAT_0041 & 0x20) == 0) || ((DAT_0042 & 0x10) != 0)) {
    return;
  }
  _DAT_00c3 = CONCAT11((byte)((ushort)_DAT_00c3 >> 8) & DAT_f924,(byte)_DAT_00c3 & DAT_f925);
  _DAT_00d5 = CONCAT11((byte)((ushort)_DAT_00d5 >> 8) & DAT_f924,(byte)_DAT_00d5 & DAT_f925);
  _DAT_00c5 = CONCAT11((byte)((ushort)_DAT_00c5 >> 8) & DAT_f926,(byte)_DAT_00c5 & DAT_f927);
  _DAT_00d7 = CONCAT11((byte)((ushort)_DAT_00d7 >> 8) & DAT_f926,(byte)_DAT_00d7 & DAT_f927);
  DAT_00c7 = DAT_00c7 & DAT_f928;
  DAT_00d9 = DAT_00d9 & DAT_f928;
  DAT_16d3 = DAT_f7a7;
  DAT_16d4 = DAT_f7a6;
  if (DAT_1686 == -0x30) {
    uVar3 = 0;
    do {
      (&DAT_1691)[uVar3] = (&DAT_f797)[uVar3];
      bVar4 = (char)uVar3 + 1;
      uVar3 = (ushort)bVar4;
    } while (bVar4 < 0x16);
    goto LAB_ac42;
  }
  if (DAT_1686 == -0x3f) {
    if ((DAT_0043 & 4) == 0) {
      _DAT_00c3 = 0;
      _DAT_00c5 = 0;
      DAT_00c7 = 0;
      _DAT_00de = 0;
      _DAT_00e0 = 0;
      _DAT_00e2 = 0;
      DAT_00e4 = 0;
      DAT_0043 = DAT_0043 | 4;
    }
  }
  else if (DAT_1686 != -0x2f) {
    if ((DAT_0043 & 8) == 0) {
      bVar4 = 0;
      if ((DAT_0042 & 0x40) == 0) {
        if (((DAT_0042 & 8) != 0) && (bVar4 = 0, DAT_1687 != 0)) {
          _DAT_168d = _DAT_1465;
          FUN_ac61();
          bVar4 = extraout_B;
          do {
            (&DAT_1691)[bVar4] = **(undefined1 **)(&DAT_f600 + *(byte *)(bVar4 + 0x16bf));
            bVar4 = bVar4 + 1;
          } while (bVar4 < DAT_1687);
        }
      }
      else {
        bVar4 = 0;
        bVar2 = 0;
        if (DAT_1687 != 0) {
          do {
            (&DAT_1691)[bVar2] = **(undefined1 **)(bVar2 + 0x16bf + (ushort)bVar2);
            bVar4 = bVar2 + 1;
            bVar2 = bVar4;
          } while ((byte)(bVar4 * '\x02') < DAT_1687);
        }
      }
      if (DAT_1686 == 'Q') {
        if (((_DAT_00d5 != 0) || (_DAT_00d7 != 0)) || (DAT_00d9 != 0)) {
          DAT_1682 = 0;
          DAT_1681 = 0x80;
          bVar2 = 0;
          do {
            if ((DAT_1681 & DAT_00d5) != 0) {
                    /* WARNING: Ignoring partial resolution of indirect */
              DAT_00d5 = ~DAT_1681 & DAT_00d5;
              bVar4 = DAT_1687;
              if ((DAT_0042 & 0x40) != 0) {
                bVar4 = DAT_1687 >> 1;
              }
              bVar4 = bVar4 + DAT_1682;
              (&DAT_1691)[bVar4] = *(undefined1 *)(bVar2 + 0xac83);
              DAT_1682 = DAT_1682 + 1;
              if (1 < DAT_1682) goto code_r0xac1c;
            }
            bVar4 = DAT_1681 & 1;
            DAT_1681 = DAT_1681 >> 1;
            if (bVar4 != 0) {
              DAT_1681 = 0x80;
            }
            bVar2 = 1;
          } while( true );
        }
      }
      else if ((bVar4 == 0) && (DAT_1688 == '\0')) {
        return;
      }
    }
    else {
      if ((DAT_0040 & 0x20) == 0) {
        return;
      }
      DAT_1691 = 0x55;
      if ((DAT_0040 & 0x10) != 0) {
        DAT_1691 = 0xaa;
      }
      bVar4 = 1;
    }
    goto LAB_ac42;
  }
  if (((_DAT_00c3 != 0) || (_DAT_00c5 != 0)) || (DAT_00c7 != 0)) {
    DAT_1681 = 0x80;
    bVar4 = 0;
    DAT_1682 = 0;
    do {
      if (((DAT_1681 & DAT_00c3) != 0) && ((byte)(&DAT_1648)[bVar4] < 0x32)) {
        (&DAT_1691)[(ushort)DAT_1682 + (ushort)DAT_1682] = *(undefined1 *)(bVar4 + 0xac83);
        uVar3 = (ushort)DAT_1682;
        uVar1 = (ushort)DAT_1682;
        (&DAT_1691 + uVar1 + uVar3)[1] = (&DAT_1648)[bVar4];
        DAT_1682 = DAT_1682 + 1;
        if ((undefined1 *)0x16a4 < &DAT_1691 + uVar1 + uVar3) goto LAB_ab2e;
      }
      bVar4 = DAT_1681 & 1;
      DAT_1681 = DAT_1681 >> 1;
      if (bVar4 != 0) {
        DAT_1681 = 0x80;
      }
      bVar4 = 1;
    } while( true );
  }
LAB_ab36:
  DAT_1691 = 0x55;
  DAT_1692 = 0;
  bVar4 = 2;
LAB_ac42:
  if (((DAT_0041 & 0x20) != 0) && (((TRCS & 0x20) == 0 || ((DAT_0042 & 0x20) == 0)))) {
    TRCS = TRCS | 4;
    DAT_0042 = DAT_0042 | 0x10;
  }
  _DAT_168f = CONCAT11(0xff,bVar4);
  return;
code_r0xac1c:
  bVar4 = bVar4 + 1;
  goto LAB_ac42;
LAB_ab2e:
  if (DAT_1682 != 0) {
    bVar4 = DAT_1682 * '\x02';
    goto LAB_ac42;
  }
  goto LAB_ab36;
}


// ---- FUN_ac61 @ ac61 ----

void FUN_ac61(void)

{
  DAT_00db = 0;
  DAT_00dc = 0;
  DAT_00dd = 0;
  if ((DAT_0049 & 1) != 0) {
    DAT_00db = 0x80;
  }
  if ((DAT_0099 & 2) != 0) {
    DAT_00db = DAT_00db | 0x40;
  }
  if ((DAT_0099 & 0x10) == 0) {
    DAT_00dc = 2;
  }
  return;
}


// ---- vec_SCI @ aca7 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 vec_SCI(void)

{
  undefined1 *puVar1;
  ushort uVar2;
  byte bVar3;
  byte extraout_B;
  byte extraout_B_00;
  byte bVar4;
  undefined1 extraout_B_01;
  undefined1 in_stack_00000003;
  
  bVar3 = DAT_1685;
  DAT_00da = TRCS;
  DAT_1680 = RX;
  if (((TRCS & 4) != 0) && ((TRCS & 0x20) != 0)) {
    if ((DAT_0042 & 0x10) == 0) {
      TRCS = TRCS & 0xfb;
      DAT_0042 = DAT_0042 & 0xdf;
      FUN_af72();
      TX = DAT_1684;
    }
    else {
      DAT_1685 = DAT_1685 + 1;
      if (DAT_1690 < bVar3) {
        if ((DAT_0042 & 0x20) == 0) {
          TRCS = TRCS & 0xfb;
        }
        DAT_0042 = DAT_0042 & 0xef;
        DAT_1685 = 0;
      }
      TX = (&DAT_168f)[bVar3];
    }
  }
  if (((DAT_00da & 0x10) == 0) || ((DAT_00da & 0xc0) == 0)) {
    return in_stack_00000003;
  }
  if ((DAT_0041 & 1) != 0) {
    if (((DAT_00da & 0x40) == 0) && (DAT_1680 == 0xff)) {
      if ((DAT_0041 & 0x80) == 0) {
        DAT_0041 = DAT_0041 | 0x80;
        goto LAB_ad0e;
      }
      DAT_0041 = DAT_0041 & 0xfe;
      DAT_0041 = DAT_0041 | 2;
    }
    DAT_0041 = DAT_0041 & 0x7f;
    return in_stack_00000003;
  }
  bVar3 = DAT_1680;
  if ((DAT_0041 & 2) != 0) {
    if (((DAT_00da & 0x40) != 0) || (DAT_1680 != 0xef)) {
LAB_ad0e:
      DAT_0041 = DAT_0041 & 0xfd | 1;
      return in_stack_00000003;
    }
    DAT_0041 = DAT_0041 & 0xfd;
    DAT_0041 = DAT_0041 | 4;
LAB_af58:
    bVar3 = ~bVar3;
    goto LAB_af59;
  }
  if ((DAT_0041 & 4) == 0) {
    if ((DAT_0041 & 0x10) == 0) {
      if ((DAT_0041 & 0x20) == 0) {
        return in_stack_00000003;
      }
      if ((DAT_00da & 0x40) == 0) {
        if (DAT_1680 == 0xff) goto LAB_ad4d;
        if (DAT_1680 == 0x30) goto LAB_ad65;
      }
    }
    else if ((DAT_00da & 0x40) == 0) {
      if (DAT_1680 == 0xff) {
LAB_ad4d:
        if ((DAT_0041 & 0x80) != 0) {
          DAT_0042 = DAT_0042 | 1;
          FUN_af72();
          bVar3 = extraout_B;
          goto LAB_af55;
        }
        DAT_0041 = DAT_0041 | 0x80;
        goto LAB_af58;
      }
      if (DAT_1680 == 0x30) {
LAB_ad65:
        DAT_0042 = DAT_0042 | 2;
        FUN_af72();
        bVar3 = extraout_B_00;
        goto LAB_af55;
      }
      if (DAT_1680 == 0xf0) {
        DAT_0041 = DAT_0041 & 0x6f;
        DAT_0041 = DAT_0041 | 0x20;
        _DAT_00d2 = _DAT_168a;
        DAT_00d4 = DAT_168c;
        return in_stack_00000003;
      }
      if (DAT_1680 == 10) {
        if (DAT_1688 < 5) {
          DAT_0042 = DAT_0042 & 0xb7;
          bVar3 = 10;
          goto LAB_af29;
        }
      }
      else {
        if (DAT_1686 == 0) {
          if (DAT_1680 == 0x51) {
LAB_adbd:
            DAT_1686 = DAT_1680;
            DAT_00d5 = 0;
            DAT_00d6 = 0;
            DAT_00d7 = 0;
            DAT_00d8 = 0;
            DAT_00d9 = 0;
            DAT_0041 = DAT_0041 & 0xfb;
            DAT_0041 = DAT_0041 | 0x10;
            goto LAB_af55;
          }
        }
        else if (DAT_1686 != 0x51) goto LAB_af32;
        if (DAT_1687 < 0x14) {
          if (DAT_1680 == 0xc9) {
            if ((DAT_0042 & 8) == 0) {
              DAT_0042 = DAT_0042 | 0x40;
LAB_af29:
              DAT_0041 = DAT_0041 & 0xef;
              DAT_0041 = DAT_0041 | 0xc;
              goto LAB_af55;
            }
          }
          else if ((DAT_1680 == 0x5a) && ((DAT_0042 & 0x40) == 0)) {
            DAT_0042 = DAT_0042 | 8;
            goto LAB_af29;
          }
        }
      }
    }
LAB_af32:
    DAT_0042 = DAT_0042 | 2;
    FUN_af72();
    bVar3 = 0xfe;
    goto LAB_af59;
  }
  if ((DAT_00da & 0x40) != 0) goto LAB_adb2;
  if ((DAT_0041 & 8) == 0) {
    if (DAT_1680 == 0xff) goto LAB_ad4d;
    if (DAT_1680 == 0x30) goto LAB_ad65;
    if (DAT_1680 == 0xc9) {
      DAT_0042 = DAT_0042 | 0x40;
      DAT_0041 = DAT_0041 | 8;
    }
    else if (DAT_1680 == 0x5a) {
      DAT_0042 = DAT_0042 | 8;
      DAT_0041 = DAT_0041 | 8;
    }
    else if (DAT_1680 == 10) {
      DAT_0041 = DAT_0041 | 8;
      DAT_0042 = DAT_0042 & 0xb7;
    }
    else {
      if (DAT_1680 != 0x10) {
        if ((((DAT_1680 == 0x51) || (DAT_1680 == 0xd1)) || (DAT_1680 == 0xc1)) || (DAT_1680 == 0xd0)
           ) goto LAB_adbd;
        goto LAB_adb2;
      }
      DAT_0043 = DAT_0043 | 8;
      DAT_0041 = DAT_0041 | 8;
    }
LAB_af55:
    DAT_0041 = DAT_0041 & 0x7f;
    goto LAB_af58;
  }
  if ((DAT_0043 & 8) != 0) {
    if (DAT_1680 == 1) {
      DAT_0040 = DAT_0040 | 0x80;
    }
    else {
      if (DAT_1680 != 2) goto LAB_adb2;
      DAT_0040 = DAT_0040 | 0x40;
    }
    goto LAB_aeae;
  }
  if ((DAT_0042 & 0x40) == 0) {
    if ((DAT_0042 & 8) == 0) {
      if ((DAT_0042 & 0x80) != 0) {
        (&DAT_16a7)[DAT_1689] = DAT_1680;
        DAT_0042 = DAT_0042 & 0x7f;
LAB_aeab:
        DAT_1688 = DAT_1688 + 1;
        goto LAB_aeae;
      }
      if ((0x7f < DAT_1680) && ((byte)(DAT_1680 + 0x80) < 0x18)) {
        uVar2 = *(ushort *)(&DAT_f650 + (byte)(DAT_1680 << 1));
        bVar3 = (byte)(uVar2 >> 8);
        if (bVar3 != 0xff) {
          bVar4 = (byte)uVar2;
          if ((char)bVar4 < '\0') {
            DAT_168c = bVar3 | DAT_168c;
            bVar4 = bVar4 & 0x3f;
          }
          else if ((uVar2 & 0x40) == 0) {
            _DAT_168a = CONCAT11(bVar3 | DAT_168a,DAT_168b);
          }
          else {
            _DAT_168a = CONCAT11(DAT_168a,bVar3 | DAT_168b);
            bVar4 = bVar4 & 0x3f;
          }
          if ((bVar4 & 1) != 0) {
            DAT_0042 = DAT_0042 | 0x80;
            bVar3 = DAT_1680;
            DAT_1689 = bVar4 >> 1;
            goto LAB_af59;
          }
          goto LAB_aeab;
        }
      }
    }
    else if ((DAT_1680 < 0x28) && ((&DAT_f600)[(byte)(DAT_1680 << 1)] != -1)) {
      *(byte *)(DAT_1687 + 0x16bf) = DAT_1680 << 1;
      DAT_1687 = DAT_1687 + 1;
      goto LAB_aeae;
    }
    goto LAB_adb2;
  }
  uVar2 = (ushort)DAT_1687;
  *(byte *)(uVar2 + 0x16bf) = DAT_1680;
  DAT_1687 = DAT_1687 + 1;
  if ((DAT_0043 & 1) == 0) {
    DAT_0043 = DAT_0043 | 1;
    bVar3 = DAT_1680;
    goto LAB_af59;
  }
  DAT_0043 = DAT_0043 & 0xfe;
  puVar1 = *(undefined1 **)(uVar2 + 0x16be);
  if (puVar1 < (undefined1 *)0x8000) {
    if (puVar1 < &DAT_1400) {
      if ((puVar1 < &DAT_0040) || ((undefined1 *)0x13f < puVar1)) goto LAB_adb2;
    }
    else if ((undefined1 *)0x17ff < puVar1) {
LAB_adb2:
      DAT_0042 = DAT_0042 | 2;
      FUN_af72();
      bVar3 = 0xfe;
      goto LAB_af59;
    }
  }
LAB_aeae:
  DAT_0041 = DAT_0041 & 0xf3;
  DAT_0041 = DAT_0041 | 0x10;
  bVar3 = DAT_1680;
LAB_af59:
  if (((DAT_0042 & 0x10) == 0) && ((TRCS & 0x20) != 0)) {
    FUN_af72();
    TX = extraout_B_01;
    return in_stack_00000003;
  }
  TRCS = TRCS | 4;
  DAT_0042 = DAT_0042 | 0x20;
  DAT_1684 = bVar3;
  return in_stack_00000003;
}


// ---- FUN_af72 @ af72 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_af72(void)

{
  if ((DAT_0042 & 3) != 0) {
    DAT_0041 = DAT_0041 & 0x41;
    DAT_0043 = DAT_0043 & 0xf1;
    if ((DAT_0042 & 1) == 0) {
      DAT_0041 = DAT_0041 | 4;
    }
    else {
      DAT_0041 = DAT_0041 | 2;
    }
    DAT_1686 = 0;
    _DAT_1687 = 0;
    _DAT_168a = 0;
    DAT_168c = 0;
    _DAT_00d2 = 0;
    DAT_00d4 = 0;
    DAT_0042 = DAT_0042 & 0x34;
    TRCS = TRCS & 0xfb;
    DAT_0040 = DAT_0040 & 0xf;
  }
  return;
}


// ---- FUN_afac @ afac ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_afac(void)

{
  bool bVar1;
  byte bVar2;
  ushort uVar3;
  
  _DAT_1672 = CONCAT11((byte)((ushort)_DAT_00c3 >> 8) & DAT_f924,(byte)_DAT_00c3 & DAT_f925);
  _DAT_1674 = CONCAT11((byte)((ushort)_DAT_00c5 >> 8) & DAT_f926,(byte)_DAT_00c5 & DAT_f927);
  DAT_1676 = DAT_00c7 & DAT_f928;
  _DAT_1677 = CONCAT11((byte)((ushort)_DAT_00de >> 8) & DAT_f924,(byte)_DAT_00de & DAT_f925);
  _DAT_1679 = CONCAT11((byte)((ushort)_DAT_00e0 >> 8) & DAT_f926,(byte)_DAT_00e0 & DAT_f927);
  DAT_167b = DAT_00e2 & DAT_f928;
  _DAT_00e2 = CONCAT12(DAT_167b,_DAT_00e3);
  _DAT_167c = _DAT_00e3;
  _DAT_00c3 = _DAT_1672;
  _DAT_00c5 = _DAT_1674;
  DAT_00c7 = DAT_1676;
  _DAT_00de = _DAT_1677;
  _DAT_00e0 = _DAT_1679;
  if ((DAT_0054 & 8) == 0) {
    if (DAT_1401 < 0xe0) {
      DAT_0046 = DAT_0046 & 0xf7;
      goto LAB_b00b;
    }
    if (((DAT_0046 & 8) == 0) && (DAT_14e8 = DAT_14e8 + '\x01', DAT_14e8 < '\0')) {
      DAT_14e8 = '\0';
      if ((DAT_0046 & 2) == 0) {
        DAT_159f = 0;
        DAT_15a0 = 0;
        DAT_0046 = DAT_0046 & 0x3f | 10;
        DAT_1472 = '\0';
        DAT_1468 = 0;
        _DAT_146e = 0x104;
      }
      else {
        DAT_0046 = DAT_0046 & 0xfd | 8;
        _DAT_00c3 = 0;
        _DAT_00c5 = 0;
        DAT_00c7 = 0;
        _DAT_00de = 0;
        _DAT_00e0 = 0;
        _DAT_00e2 = 0;
      }
    }
    goto LAB_b14e;
  }
LAB_b00b:
  bVar2 = DAT_0046;
  DAT_14e8 = '\0';
  if ((DAT_0046 & 2) == 0) {
    bVar2 = DAT_0054;
    if (((DAT_fee0 & 0x20) != 0) && (((_DAT_1677 != 0 || (_DAT_1679 != 0)) || (DAT_167b != 0))))
    goto LAB_b153;
joined_r0xb02c:
    if ((bVar2 & 8) == 0) goto LAB_b153;
  }
  else if ((DAT_0054 & 8) == 0) {
    DAT_159f = 0;
    DAT_15a0 = 0;
    DAT_0046 = DAT_0046 & 0x3f;
    DAT_1472 = DAT_1472 + 1;
    if (DAT_1472 < 0x1e) {
      DAT_14e8 = 0;
      DAT_159f = 0;
      DAT_15a0 = 0;
      return;
    }
    DAT_1472 = '\0';
    if (DAT_1468 == 0) {
      FUN_b16b();
    }
    DAT_1468 = DAT_1468 + 1;
    if (0x2a < DAT_1468) {
      DAT_1468 = 0;
    }
    if (5 < DAT_1468) {
      if (DAT_1468 < 0x1a) {
        if ((DAT_1468 & 1) != 0) {
          return;
        }
        if ((DAT_1468 >> 1 & 1) != 0) {
          bVar1 = (bool)(DAT_147b >> 7);
          DAT_147b = DAT_147b << 1;
          if (!bVar1) {
            DAT_1468 = 0x1a;
            return;
          }
LAB_b153:
          DAT_0083 = DAT_0083 | 0x10;
          goto LAB_b156;
        }
      }
      else if ((0x1a < DAT_1468) && ((DAT_1468 & 1) != 0)) {
        bVar1 = (bool)(DAT_147a >> 7);
        DAT_147a = DAT_147a << 1;
        if (!bVar1) {
          DAT_1468 = 0;
          return;
        }
        goto LAB_b153;
      }
    }
  }
  else if (DAT_f614 == -1) {
LAB_b0f4:
    DAT_15a0 = 0;
    bVar2 = DAT_004c;
    if ((DAT_0046 & 0x40) == 0) {
      bVar2 = DAT_0051;
    }
    if ((bVar2 & 0x20) != 0) goto joined_r0xb02c;
  }
  else if (DAT_1401 < 0xe0) {
    if ((DAT_0046 & 0x80) == 0) goto LAB_b0f4;
    if ((DAT_004a & 0x1f) != 0) {
      DAT_14e8 = 0;
      return;
    }
    DAT_15a0 = DAT_15a0 + 1;
    if (4 < DAT_15a0) {
      if (DAT_15a0 < 0xd) {
        bVar1 = (bool)(DAT_14e9 >> 7);
        DAT_14e9 = DAT_14e9 << 1;
        if (bVar1) goto LAB_b153;
      }
      else if (0x18 < DAT_15a0) {
        DAT_0046 = DAT_0046 & 0x7f;
        DAT_0046 = DAT_0046 ^ 0x40;
        goto LAB_b0f4;
      }
    }
  }
  else {
    DAT_159f = DAT_159f + 1;
    if ((short)((ushort)DAT_159f << 8) < 0) {
      DAT_159f = 0;
      DAT_15a0 = 0;
      DAT_0046 = DAT_0046 | 0x80;
      if ((bVar2 & 0x40) == 0) {
        DAT_14e9 = 0x88;
      }
      else {
        DAT_14e9 = 0xaa;
      }
    }
  }
LAB_b14e:
  DAT_0083 = DAT_0083 & 0xef;
LAB_b156:
  uVar3 = CONCAT11(DAT_1003,DAT_0083) & 0xef10;
  DAT_1647 = DAT_0046;
  DAT_1003 = (char)(uVar3 >> 8) + (char)uVar3;
  return;
}


// ---- FUN_b16b @ b16b ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b16b(void)

{
  bool bVar1;
  byte bVar2;
  byte bVar3;
  ushort uVar4;
  char cVar6;
  byte bVar7;
  ushort uVar5;
  undefined *puVar8;
  byte bStack_1;
  
  uVar5 = _DAT_146e;
  if (((_DAT_00c3 != 0) || (_DAT_00c5 != 0)) || (DAT_00c7 != '\0')) {
    do {
      uVar4 = CONCAT11((byte)(uVar5 >> 9),(char)uVar5);
      if (((uVar5 & 0x100) != 0) &&
         (cVar6 = (char)uVar5 + '\x01', uVar4 = CONCAT11(0x80,cVar6), cVar6 == '\x05')) {
        uVar4 = 0x8000;
      }
      bVar3 = (byte)(uVar4 >> 8);
      uVar5 = uVar4;
      if ((bVar3 & *(byte *)((uVar4 & 0xff) + 0xc3)) != 0) {
        uVar5 = CONCAT11(bVar3,(char)_bStack_1);
        bVar7 = (char)uVar4 << 3;
        bVar2 = bVar3;
        while (bVar1 = (bool)(bVar2 >> 7), bVar2 = bVar2 << 1, !bVar1) {
          bVar7 = bVar7 + 1;
        }
        _bStack_1 = uVar5;
        if ((byte)(&DAT_1648)[bVar7] < 0x32) {
          puVar8 = &DAT_b1d0;
          while (bVar1 = (bool)(bVar3 >> 7), bVar3 = bVar3 << 1, !bVar1) {
            puVar8 = puVar8 + 1;
          }
          _DAT_146e = uVar5;
          _DAT_147a = CONCAT11(*puVar8,(&DAT_b1d0)[uVar4 & 0xff]);
          return;
        }
      }
    } while (uVar5 != _DAT_146e);
  }
  _DAT_146e = 0x104;
  _DAT_147a = 0xf8f8;
  return;
}


// ---- vec_RESET @ b1d8 ----

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
  } while (puVar1 != (undefined2 *)&DAT_1640);
  _DAT_013e = 0xb1fa;
  FUN_b20d();
  _DAT_013e = 0xb1fd;
  FUN_b23c();
  _DAT_013e = 0xb200;
  FUN_b343();
  _DAT_013e = 0xb204;
  FUN_b4d8();
  _DAT_013e = 0xb207;
  FUN_b59b();
  _DAT_013e = 0xb20a;
  FUN_b4bd();
  FUN_b497();
  return;
}


// ---- FUN_b20d @ b20d ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b20d(void)

{
  byte bVar1;
  
  bVar1 = 0;
  if ((DAT_0040 & 4) == 0) {
    bVar1 = DAT_0049;
  }
  P2DATA = 0;
  DAT_0017 = bVar1 | 0x80;
  DAT_0049 = bVar1 | 0x80;
  DAT_0048 = 0;
  P2DDR = 0xb2;
  DAT_0016 = 0xc3;
  TCSR = 0;
  P3SCR = 0;
  RAMCR = 0xe5;
  _DAT_001b = 0;
  RMCR = 0xc;
  TRCS = 0x3a;
  return;
}


// ---- FUN_b23c @ b23c ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b23c(void)

{
  short sVar1;
  byte *pbVar2;
  undefined2 *puVar3;
  
  DAT_00bf = 0xb0;
  DAT_007f = DAT_007f | 0xa1;
  DAT_0093 = DAT_0093 | 0x60;
  DAT_140f = 0x5e;
  DAT_1410 = 0x5e;
  DAT_144d = 0x5e;
  DAT_004f = DAT_004f | 0x20;
  DAT_00be = DAT_00be | 0x20;
  DAT_0057 = 9;
  DAT_004a = 0x99;
  DAT_1526 = 0xff;
  DAT_004b = 5;
  DAT_14c8 = 5;
  DAT_1431 = 100;
  DAT_148e = 100;
  DAT_14d4 = 100;
  DAT_14d5 = 100;
  DAT_14d6 = 100;
  DAT_0051 = DAT_0051 | 0x20;
  DAT_142e = ~DAT_142e;
  DAT_1452 = ~DAT_1452;
  DAT_14da = ~DAT_14da;
  DAT_1435 = DAT_ffa0;
  _DAT_146e = 0x104;
  if ((DAT_0042 & 0x30) != 0) {
    TRCS = TRCS | 4;
  }
  if ((DAT_0040 & 4) == 0) {
    if ((DAT_0040 & 0x80) == 0) {
      DAT_0041 = DAT_0041 | 1;
      if (_DAT_1642 != 0x55aa) {
        sVar1 = 0;
        pbVar2 = (byte *)0x1641;
        do {
          pbVar2 = pbVar2 + 1;
          sVar1 = CONCAT11((char)((ushort)sVar1 >> 8) + CARRY1((byte)sVar1,*pbVar2),
                           (byte)sVar1 + *pbVar2);
        } while (pbVar2 != (byte *)0x177f);
        if (sVar1 + _DAT_1640 != 0) goto LAB_b2cb;
      }
      goto LAB_b2f8;
    }
LAB_b2cb:
    DAT_1671 = 0xff;
    DAT_1498 = -1;
    _DAT_1672 = 0;
    _DAT_1674 = 0;
    DAT_1676 = 0;
  }
  else {
LAB_b2f8:
    _DAT_1642 = 0;
    DAT_0046 = DAT_1647 & 0x3b;
    _DAT_00c3 = _DAT_1672;
    _DAT_00c5 = _DAT_1674;
    DAT_00c7 = DAT_1676;
    DAT_1498 = DAT_1671 + 4;
    if (0xfb < DAT_1671) {
      DAT_1498 = -1;
    }
    if (DAT_fef6 != 0) goto LAB_b324;
  }
  puVar3 = (undefined2 *)&DAT_1700;
  _DAT_1645 = 0x6400;
  _DAT_00c3 = _DAT_1672;
  _DAT_00c5 = _DAT_1674;
  DAT_00c7 = DAT_1676;
  do {
    *puVar3 = 0x6400;
    puVar3 = puVar3 + 1;
  } while (puVar3 != (undefined2 *)0x1780);
LAB_b324:
  if ((DAT_0040 & 4) != 0) {
    _DAT_00d2 = _DAT_168a;
    DAT_00d4 = DAT_168c;
    return;
  }
  puVar3 = (undefined2 *)&DAT_1680;
  do {
    *puVar3 = 0;
    puVar3 = puVar3 + 1;
  } while (puVar3 < &DAT_1700);
  return;
}


// ---- FUN_b343 @ b343 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b343(void)

{
  undefined2 uVar1;
  undefined2 *puVar2;
  byte *pbVar3;
  
  DAT_1021 = 0;
  puVar2 = &DAT_b3d3;
  do {
    _DAT_1022 = *puVar2;
    _DAT_1024 = puVar2[1];
    _DAT_1026 = puVar2[2];
    _DAT_1028 = puVar2[3];
    puVar2 = puVar2 + 4;
  } while (puVar2 != (undefined2 *)0xb453);
  _DAT_005b = (undefined2 *)&DAT_1040;
  pbVar3 = (byte *)0xb453;
  do {
    uVar1 = *(undefined2 *)pbVar3;
    pbVar3 = pbVar3 + 2;
    *_DAT_005b = uVar1;
    _DAT_005b = _DAT_005b + 1;
  } while (pbVar3 != (byte *)0xb483);
  do {
    *(byte *)(*pbVar3 + 0x1000) = pbVar3[10];
    pbVar3 = pbVar3 + 1;
  } while (pbVar3 != (byte *)0xb48d);
  DAT_102a = 0;
  DAT_1033 = 0;
  DAT_102b = 0x8c;
  DAT_1034 = 0;
  DAT_102c = 0;
  DAT_1035 = 0;
  DAT_1020 = 2;
  DAT_14bd = DAT_1002 & 0x20;
  return;
}


// ---- FUN_b497 @ b497 ----

void FUN_b497(void)

{
  do {
    DAT_1476 = 0;
    FUN_b4d8();
    FUN_b59b();
    FUN_b5e8();
    FUN_b584();
    FUN_b60d();
    FUN_b63b();
    FUN_b6e5();
    FUN_b84d();
    FUN_bb78();
    FUN_bbe7();
    FUN_bd58();
  } while( true );
}


// ---- FUN_b4bd @ b4bd ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_b4bd(undefined1 param_1,undefined1 param_2)

{
  byte bVar1;
  
  bVar1 = DAT_145d;
  FUN_809f(DAT_145d,param_2,0xfe20);
  _DAT_004d = (ushort)bVar1 * 0x7d;
  _DAT_1058 = _DAT_004d;
  _DAT_106e = _DAT_004d;
  return;
}


// ---- FUN_b4d8 @ b4d8 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b4d8(void)

{
  undefined1 extraout_B;
  undefined1 extraout_B_00;
  undefined1 extraout_B_01;
  undefined1 extraout_B_02;
  undefined1 extraout_B_03;
  undefined1 extraout_B_04;
  
  FUN_b54f();
  _DAT_0089 = CONCAT11(DAT_1404,extraout_B);
  _DAT_008b = CONCAT11(DAT_140d,0x4b);
  DAT_140d = FUN_b527();
  DAT_1404 = extraout_B_00;
  FUN_b54f();
  _DAT_0089 = CONCAT11(DAT_1405,extraout_B_01);
  _DAT_008b = CONCAT11(DAT_140e,0x10);
  DAT_140e = FUN_b527();
  DAT_1405 = extraout_B_02;
  FUN_b54f();
  _DAT_0089 = CONCAT11(DAT_1401,extraout_B_03);
  _DAT_008b = CONCAT11(DAT_14ca,0x10);
  DAT_14ca = FUN_b527();
  DAT_1401 = extraout_B_04;
  return;
}


// ---- FUN_b527 @ b527 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

byte FUN_b527(void)

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


// ---- FUN_b54f @ b54f ----

void FUN_b54f(undefined1 param_1,byte param_2)

{
  DAT_1006 = param_2 | 0x20;
  do {
  } while (-1 < (char)(param_2 | 0x20));
  return;
}


// ---- FUN_b565 @ b565 ----

byte FUN_b565(undefined1 param_1,byte param_2)

{
  byte bVar1;
  
  DAT_1006 = param_2 | 0x20;
  do {
  } while (-1 < (char)(param_2 | 0x20));
  bVar1 = *(byte *)((byte)((param_2 & 3) << 1) + 0x1007);
  return (bVar1 >> 7) << 1 | (byte)(bVar1 << 1) >> 7;
}


// ---- FUN_b584 @ b584 ----

void FUN_b584(void)

{
  char cVar1;
  
  if (DAT_1404 < 0xb0) {
    cVar1 = (char)((ushort)(byte)(0xaf - DAT_1404) * (ushort)DAT_ff87 >> 8);
  }
  else {
    cVar1 = -(char)((ushort)(byte)-(0xaf - DAT_1404) * (ushort)DAT_ff87 >> 8);
  }
  DAT_142c = cVar1 + DAT_ff88;
  return;
}


// ---- FUN_b59b @ b59b ----

void FUN_b59b(void)

{
  byte bVar1;
  
  if ((DAT_00d2 & 1) == 0) {
    if ((2 < DAT_1405) && (DAT_1405 < 0xf2)) {
      if (DAT_1405 == DAT_1489) {
        return;
      }
      DAT_1489 = DAT_1405;
    }
    DAT_140c = FUN_80a9();
    if (DAT_1453 == 0) {
      DAT_1453 = DAT_140c;
    }
  }
  else {
    DAT_1489 = 0;
    DAT_140c = DAT_16a7;
  }
  bVar1 = DAT_140c - 10;
  if (DAT_140c < 10) {
    bVar1 = 0;
  }
  else if (0x9f < bVar1) {
    bVar1 = 0x9f;
  }
  DAT_145d = (char)((ushort)bVar1 * 0x19a + 0x80 >> 8);
  return;
}


// ---- FUN_b5e8 @ b5e8 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_b5e8(void)

{
  byte bVar1;
  byte bVar2;
  byte bVar3;
  undefined2 uVar4;
  byte bStack0000;
  
  bVar1 = DAT_1453;
  bVar3 = DAT_145d;
  uVar4 = 0xfeb0;
  if (DAT_1453 < 0x41) {
    uVar4 = 0xff30;
  }
  FUN_809f(DAT_145d,DAT_1453,uVar4);
  bVar2 = DAT_1544;
  bStack0000 = bVar3;
  FUN_809f(DAT_1544,bVar1,0xf8a0);
  _DAT_1418 = (ushort)bVar2 * (ushort)bStack0000 * 4;
  return;
}


// ---- FUN_b60d @ b60d ----

void FUN_b60d(void)

{
  byte bVar1;
  byte bVar2;
  
  if ((DAT_0054 & 8) != 0) {
    bVar1 = DAT_fee9;
    bVar2 = DAT_feeb;
    if ((DAT_0049 & 0x40) == 0) {
      bVar1 = DAT_fee9 - 0x28;
      bVar2 = DAT_feeb - 0x10;
    }
    if ((DAT_1442 <= bVar1) && (DAT_1413 <= bVar2)) {
      DAT_0049 = DAT_0049 | 0x40;
      DAT_0017 = DAT_0049;
      return;
    }
  }
  DAT_0049 = DAT_0049 & 0xbf;
  DAT_0017 = DAT_0049;
  return;
}


// ---- FUN_b63b @ b63b ----

/* WARNING: Instruction at (RAM,0xb696) overlaps instruction at (RAM,0xb695)
    */
/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b63b(void)

{
  byte bVar1;
  char cVar2;
  byte *pbVar3;
  undefined2 *puVar4;
  
  if (((((_DAT_0041 & 0x2000) == 0) || ((DAT_0043 & 8) == 0)) || ((DAT_0040 & 0x20) != 0)) ||
     ((DAT_0040 & 0xc0) == 0)) {
    return;
  }
  if ((DAT_0040 & 0x80) == 0) {
    pbVar3 = (byte *)0x7fff;
    DAT_145a = '\0';
    DAT_1459 = 0;
    do {
      pbVar3 = pbVar3 + 1;
      DAT_1459 = DAT_1459 ^ *pbVar3;
      DAT_145a = DAT_145a + *pbVar3;
      DAT_1476 = 0;
    } while (pbVar3 != (byte *)((short)&RST_VECTOR + 1));
    if ((DAT_1459 == DAT_ff7a) && (DAT_145a == DAT_ff7b)) {
      DAT_0040 = DAT_0040 | 0x20;
      return;
    }
    DAT_0040 = DAT_0040 | 0x30;
    return;
  }
  FUN_b66d();
  FUN_b66d();
  FUN_b66d();
  FUN_b66d();
  pbVar3 = (byte *)0x140;
  bVar1 = 0xaa;
  while( true ) {
    cVar2 = '\0';
    do {
      pbVar3[-1] = ~bVar1;
      pbVar3 = pbVar3 + -2;
      *pbVar3 = bVar1;
      cVar2 = cVar2 + '\x02';
    } while (cVar2 != '\0');
    cVar2 = '\0';
    DAT_1003 = 0;
    do {
      if (bVar1 != *pbVar3) {
        DAT_0040 = 0xb0;
        goto LAB_b6a8;
      }
      if ((byte)~bVar1 != pbVar3[1]) {
                    /* WARNING: Bad instruction - Truncating control flow here */
        halt_baddata();
      }
      pbVar3 = pbVar3 + 2;
      cVar2 = cVar2 + '\x02';
    } while (cVar2 != '\0');
    if (bVar1 == 0x55) break;
    bVar1 = ~bVar1;
  }
  if (pbVar3 != (byte *)0x140) {
    return;
  }
  DAT_0040 = 0xa0;
LAB_b6a8:
  _DAT_0041 = 0x2000;
  DAT_0043 = 8;
  puVar4 = (undefined2 *)&DAT_0044;
  do {
    *puVar4 = 0;
    puVar4 = puVar4 + 1;
  } while (puVar4 != (undefined2 *)0x140);
  puVar4 = (undefined2 *)&DAT_1400;
  do {
    *puVar4 = 0;
    puVar4 = puVar4 + 1;
  } while (puVar4 != (undefined2 *)&DAT_1640);
  _DAT_013e = 0xb1fa;
  FUN_b20d();
  _DAT_013e = 0xb1fd;
  FUN_b23c();
  _DAT_013e = 0xb200;
  FUN_b343();
  _DAT_013e = 0xb204;
  FUN_b4d8();
  _DAT_013e = 0xb207;
  FUN_b59b();
  _DAT_013e = 0xb20a;
  FUN_b4bd();
  FUN_b497();
  return;
}


// ---- FUN_b66d @ b66d ----

/* WARNING: Instruction at (RAM,0xb696) overlaps instruction at (RAM,0xb695)
    */
/* WARNING: Control flow encountered bad instruction data */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b66d(undefined1 param_1,undefined1 param_2,byte *param_3)

{
  byte bVar1;
  char cVar2;
  undefined2 *puVar3;
  
  bVar1 = 0xaa;
  while( true ) {
    cVar2 = '\0';
    do {
      param_3[-1] = ~bVar1;
      param_3 = param_3 + -2;
      *param_3 = bVar1;
      cVar2 = cVar2 + '\x02';
    } while (cVar2 != '\0');
    cVar2 = '\0';
    DAT_1003 = 0;
    do {
      if (bVar1 != *param_3) {
        DAT_0040 = 0xb0;
        goto LAB_b6a8;
      }
      if ((byte)~bVar1 != param_3[1]) {
                    /* WARNING: Bad instruction - Truncating control flow here */
        halt_baddata();
      }
      param_3 = param_3 + 2;
      cVar2 = cVar2 + '\x02';
    } while (cVar2 != '\0');
    if (bVar1 == 0x55) break;
    bVar1 = ~bVar1;
  }
  if (param_3 != (byte *)0x140) {
    return;
  }
  DAT_0040 = 0xa0;
LAB_b6a8:
  _DAT_0041 = 0x2000;
  DAT_0043 = 8;
  puVar3 = (undefined2 *)&DAT_0044;
  do {
    *puVar3 = 0;
    puVar3 = puVar3 + 1;
  } while (puVar3 != (undefined2 *)0x140);
  puVar3 = (undefined2 *)&DAT_1400;
  do {
    *puVar3 = 0;
    puVar3 = puVar3 + 1;
  } while (puVar3 != (undefined2 *)&DAT_1640);
  _DAT_013e = 0xb1fa;
  FUN_b20d();
  _DAT_013e = 0xb1fd;
  FUN_b23c();
  _DAT_013e = 0xb200;
  FUN_b343();
  _DAT_013e = 0xb204;
  FUN_b4d8();
  _DAT_013e = 0xb207;
  FUN_b59b();
  _DAT_013e = 0xb20a;
  FUN_b4bd();
  FUN_b497();
  return;
}


// ---- FUN_b6e5 @ b6e5 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b6e5(void)

{
  bool bVar1;
  byte bVar2;
  byte extraout_B;
  
  bVar2 = FUN_809f();
  if (((DAT_00c2 & 8) != 0) && (bVar1 = bVar2 < 10, bVar2 = bVar2 - 10, bVar1)) {
    bVar2 = 0;
  }
  if (DAT_149a < bVar2) {
    DAT_00c2 = DAT_00c2 & 0xf7;
  }
  else {
    DAT_00c2 = DAT_00c2 | 8;
  }
  bVar2 = DAT_ffa8;
  if (((DAT_00c2 & 4) != 0) && (bVar2 = DAT_ffa8 - 2, DAT_ffa8 < 2)) {
    bVar2 = 0;
  }
  if (DAT_140c < bVar2) {
LAB_b72d:
    DAT_00c2 = DAT_00c2 & 0xfb;
  }
  else {
    bVar2 = DAT_ffa7;
    if (((DAT_00c2 & 4) == 0) && (bVar2 = DAT_ffa7 - 2, DAT_ffa7 < 2)) {
      bVar2 = 0;
    }
    if (bVar2 <= DAT_140c) goto LAB_b72d;
    DAT_00c2 = DAT_00c2 | 4;
  }
  if ((DAT_00c2 & 0xc) == 0xc) {
    DAT_0059 = DAT_0059 | 4;
  }
  else {
    DAT_0059 = DAT_0059 & 0xfb;
  }
  if ((DAT_0053 & 0x40) != 0) {
    if ((DAT_0053 & 1) == 0) {
      if ((DAT_0059 & 0x40) != 0) {
        DAT_0059 = DAT_0059 & 0xbf;
        if (DAT_1450 < 6) {
          DAT_1439 = 0;
        }
        else {
          DAT_1439 = 0xff;
        }
      }
      if ((((DAT_0059 & 4) == 0) && (DAT_140a == '\0')) && ((DAT_0059 & 1) == 0)) {
        if (DAT_1439 < DAT_ffae) {
          DAT_0059 = DAT_0059 | 0x80;
          goto LAB_b7a2;
        }
      }
      else {
        DAT_14ab = 0xff;
      }
    }
    else if ((DAT_0059 & 0x40) == 0) {
      DAT_1450 = 0;
      DAT_0059 = DAT_0059 | 0x40;
    }
    else if ((char)DAT_1450 < '\0') {
      DAT_1450 = 200;
    }
    DAT_0059 = DAT_0059 & 0x7f;
  }
LAB_b7a2:
  _DAT_0069 = _DAT_1482;
  if ((DAT_0059 & 4) != 0) {
    _DAT_0069 = 0xffff;
  }
  _DAT_0067 = _DAT_140a;
  DAT_007d = DAT_007d & 0x4f;
  DAT_007d = DAT_007d | 0x40;
  _DAT_0074 = 0xfd00;
  if ((DAT_007f & 0x80) == 0) {
    _DAT_0074 = 0xf500;
  }
  _DAT_0076 = 0xfb00;
  _DAT_0078 = 0xfaf0;
  DAT_141a = FUN_80d9();
  _DAT_1422 = (ushort)(byte)(DAT_141a + 0x40) << 0xb;
  if ((DAT_0059 & 8) == 0) {
    if (extraout_B < 2) goto LAB_b7eb;
LAB_b806:
    if ((DAT_0053 & 0x40) == 0) {
      if ((((DAT_0059 & 4) == 0) && (DAT_1460 < DAT_ffb7)) && ((DAT_0059 & 1) == 0)) {
        if (DAT_1439 < DAT_ffae) {
          DAT_0059 = DAT_0059 | 0x80;
          goto LAB_b7f6;
        }
      }
      else {
        DAT_14ab = 0xff;
      }
      DAT_0059 = DAT_0059 & 0x7f;
    }
    if ((DAT_0059 & 0x80) == 0) {
      DAT_0059 = DAT_0059 | 8;
      DAT_141d = extraout_B;
      if (DAT_14ab != 0xff) {
        DAT_141d = (byte)((ushort)extraout_B * (ushort)DAT_14ab >> 8);
      }
      goto LAB_b842;
    }
  }
  else {
    if (extraout_B != 0) goto LAB_b806;
LAB_b7eb:
    if ((DAT_0053 & 0x40) == 0) {
      DAT_0059 = DAT_0059 & 0x7f;
      DAT_1439 = 0;
    }
  }
LAB_b7f6:
  DAT_0059 = DAT_0059 & 0xf7;
  DAT_14ab = DAT_f9ff;
  DAT_141d = 0;
LAB_b842:
  _DAT_1426 = (ushort)DAT_141d << 0xb;
  return;
}


// ---- FUN_b84d @ b84d ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_b84d(void)

{
  bool bVar1;
  byte bVar2;
  byte bVar3;
  byte bVar5;
  char cVar6;
  ushort uVar7;
  short sVar8;
  undefined1 *puVar9;
  undefined1 *puVar10;
  byte bStack0000;
  byte bVar4;
  
  bVar2 = DAT_1404;
  FUN_809f();
  bVar3 = DAT_1460;
  bStack0000 = bVar2;
  FUN_80a9();
  bVar5 = DAT_145d;
  bVar2 = DAT_1442;
  if (((SUB21((ushort)bVar3 * (ushort)bStack0000 >> 0xf,0)) ||
      (bVar4 = (byte)((ushort)bVar3 * (ushort)bStack0000 * 2 >> 8), bVar3 = bVar4 + DAT_ff8e,
      CARRY1(bVar4,DAT_ff8e))) ||
     ((bVar4 = DAT_ff8e + 5, (byte)(DAT_ff8e + 5) <= bVar3 && (bVar4 = bVar3, 0x60 < bVar3)))) {
    DAT_143a = '\x18';
  }
  else {
    DAT_143a = 'x' - bVar4;
  }
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_0053 & 1) == 0) {
      DAT_159a = '\0';
      sVar8 = CONCAT11(DAT_143a,DAT_140c);
      if ((((DAT_140c < DAT_ffd5) && (sVar8 = CONCAT11(DAT_1453,DAT_140c), 0x40 < DAT_1453)) &&
          (DAT_1453 < 0x55)) && (DAT_ffd4 <= DAT_140c)) {
        sVar8 = CONCAT11(DAT_1460,DAT_1482);
        if ((DAT_007d & 4) != 0) {
          sVar8 = sVar8 + 0xa08;
        }
        if (((byte)sVar8 < DAT_ffd6) && ((byte)((ushort)sVar8 >> 8) < DAT_ffd7)) {
          DAT_007d = DAT_007d & 0xfb;
          FUN_809f(DAT_1442,(byte)sVar8,0xff60);
          DAT_143b = bVar2;
          goto LAB_b8a0;
        }
      }
LAB_b9c2:
      DAT_159a = '\0';
      DAT_007d = DAT_007d & 0x1f;
      DAT_007d = DAT_007d | 0x14;
      _DAT_0074 = 0xfc00;
      DAT_0093 = DAT_0093 & 0xbf;
      if ((DAT_007f & 0x80) != 0) {
        _DAT_0074 = 0xf400;
        DAT_0093 = DAT_0093 | 0x40;
      }
      _DAT_0076 = 0xfb20;
      _DAT_0078 = 0xfb10;
      bVar5 = (byte)((ushort)sVar8 >> 8);
      FUN_80cf();
      bVar2 = DAT_1544;
      if ((DAT_0093 & 0x40) == 0) {
        if ((DAT_0093 & 0x20) != 0) {
          DAT_0093 = DAT_0093 & 0xdf;
LAB_ba03:
          DAT_14f6 = DAT_14f5 - bVar5;
          DAT_0093 = DAT_0093 | 0x10;
        }
      }
      else if ((DAT_0093 & 0x20) == 0) {
        DAT_0093 = DAT_0093 | 0x20;
        goto LAB_ba03;
      }
      DAT_14f4 = bVar5;
      DAT_14f5 = bVar5;
      bStack0000 = bVar5;
      if (((DAT_0093 & 1) == 0) && ((DAT_007f & 0x10) == 0)) {
        DAT_159e = 0;
        DAT_159d = 0;
      }
      else {
        FUN_809f();
        puVar9 = (undefined1 *)0xffe0;
        if ((DAT_0093 & 0x40) != 0) {
          puVar9 = (undefined1 *)0xf918;
        }
        puVar10 = puVar9;
        if ((DAT_ffdc <= DAT_1460) && (puVar10 = puVar9 + 3, DAT_ffdd <= DAT_1460)) {
          puVar10 = puVar9 + 6;
        }
        puVar9 = puVar10;
        if ((DAT_ffda <= DAT_1482) && (puVar9 = puVar10 + 1, DAT_ffdb <= DAT_1482)) {
          puVar9 = puVar10 + 2;
        }
        DAT_159e = *puVar9;
        DAT_159d = bVar2;
      }
      bVar2 = DAT_145d;
      if ((DAT_ff10 == 0xff) || (DAT_1477 <= DAT_ff10)) {
        FUN_809f();
        bVar5 = DAT_1544;
        FUN_809f();
        cVar6 = bVar2 - bVar5;
        if (bVar2 < bVar5) {
          cVar6 = '\0';
        }
        bStack0000 = cVar6 + bStack0000;
        if (0x3b < bStack0000) {
          bStack0000 = 0x3c;
        }
      }
      bVar2 = DAT_145d;
      FUN_809f();
      bVar1 = bStack0000 < bVar2;
      bStack0000 = bStack0000 - bVar2;
      if (bVar1) {
        bStack0000 = 0;
      }
      if (DAT_141d == 0) {
LAB_bb3c:
        DAT_141c = 0;
      }
      else {
        if (DAT_ff12 <= DAT_141d) {
          DAT_00c2 = DAT_00c2 | 0x10;
          if ((DAT_fee0 & 0x40) == 0) goto LAB_bad3;
          bVar1 = bStack0000 < DAT_ff13;
          bStack0000 = bStack0000 - DAT_ff13;
          if (bVar1) {
            bStack0000 = 0;
          }
          goto LAB_bb3c;
        }
        DAT_00c2 = DAT_00c2 & 0xef;
        if ((DAT_fee0 & 0x40) != 0) goto LAB_bb3c;
LAB_bad3:
        bVar2 = DAT_140c;
        if (((DAT_00c2 & 0x20) != 0) && (bVar2 = DAT_140c + 2, 0xfd < DAT_140c)) {
          bVar2 = 0xff;
        }
        if (bVar2 < DAT_f880) {
          DAT_00c2 = DAT_00c2 & 0xdf;
        }
        else {
          DAT_00c2 = DAT_00c2 | 0x20;
        }
        bVar2 = DAT_00c2;
        DAT_141c = DAT_1407;
        if (((DAT_00c2 & 0x40) != 0) && (DAT_141c = DAT_1407 + 5, 0xfa < DAT_1407)) {
          DAT_141c = 0xff;
        }
        if (DAT_141c < DAT_f87f) {
          DAT_00c2 = DAT_00c2 & 0xbf;
          if ((bVar2 & 0x20) == 0) goto LAB_bb11;
        }
        else {
          DAT_00c2 = DAT_00c2 | 0x40;
LAB_bb11:
          if ((DAT_00c2 & 0x10) == 0) goto LAB_bb3c;
        }
        if ((DAT_ff7d <= (byte)(DAT_141c + DAT_141d)) &&
           (DAT_141c = DAT_ff7d - DAT_141d, DAT_ff7d < DAT_141d)) {
          DAT_141c = 0;
        }
      }
      _DAT_145e = CONCAT11(DAT_159d,DAT_159e);
      cVar6 = -1;
      if ((DAT_0093 & 0x10) != 0) {
        cVar6 = '\0';
        DAT_0093 = DAT_0093 & 0xef;
      }
      if ((DAT_0093 & 1) == 0) {
        DAT_007d = DAT_007d & 0xf7;
      }
      else {
        DAT_007d = DAT_007d | 8;
      }
      DAT_143b = bStack0000;
      if (cVar6 == '\0') {
        DAT_0093 = DAT_0093 | 8;
      }
      goto LAB_bb6d;
    }
    if (((DAT_0053 & 4) == 0) || (((DAT_0053 & 0x10) == 0 && ((DAT_008f & 0x80) == 0)))) {
LAB_b8e5:
      DAT_00c2 = DAT_00c2 & 0x7f;
      DAT_159a = '\0';
      uVar7 = CONCAT11(DAT_140c,DAT_1482);
      if ((DAT_0059 & 0x20) != 0) {
        uVar7 = uVar7 + 0x508;
      }
      if ((DAT_ff70 <= (byte)uVar7) && (bVar5 = (byte)(uVar7 >> 8), DAT_ff71 <= bVar5)) {
        if ((DAT_0059 & 0x20) != 0) {
          uVar7 = uVar7 & 0xff;
        }
        sVar8 = CONCAT11(bVar5,(byte)uVar7);
        if (DAT_1442 <= (byte)uVar7) {
          DAT_0059 = DAT_0059 | 0x20;
          goto LAB_b9c2;
        }
      }
    }
    else {
      bVar5 = DAT_140c;
      if (((DAT_00c2 & 0x80) != 0) && (bVar5 = DAT_140c + 5, 0xfa < DAT_140c)) {
        bVar5 = 0xff;
      }
      if (bVar5 < DAT_f87c) goto LAB_b8e5;
      DAT_00c2 = DAT_00c2 | 0x80;
    }
    DAT_0059 = DAT_0059 & 0xdf;
    FUN_809f();
    DAT_14cb = bVar2;
    if (DAT_14cc != 0) {
      if (bVar2 < DAT_14cc) {
        if ((1 < (byte)-(bVar2 - DAT_14cc)) && (DAT_14cb = DAT_14cc, DAT_14cc != 0)) {
          DAT_14cb = DAT_14cc - 1;
        }
      }
      else if ((1 < (byte)(bVar2 - DAT_14cc)) &&
              (DAT_14cb = DAT_14cc + 1, (byte)(DAT_14cc + 1) == 0)) {
        DAT_14cb = 0xff;
      }
    }
    DAT_143b = DAT_14cb + DAT_1598;
    if ((DAT_00c2 & 0x80) == 0) {
      if (DAT_ffd4 < DAT_140c) {
        bVar2 = (DAT_ffd4 + 0x1e) - DAT_140c;
        if (DAT_140c <= (byte)(DAT_ffd4 + 0x1e)) {
          DAT_143b = (char)((ushort)DAT_ffd9 * ((CONCAT11(8,bVar2) >> 8) * (ushort)bVar2 & 0xff) >>
                           8) + DAT_143b;
        }
      }
      else {
        DAT_143b = DAT_143b + DAT_ffd9;
      }
    }
    else {
      DAT_143b = DAT_143b + DAT_159a;
    }
  }
  else {
    FUN_809f();
    DAT_143b = bVar5;
    if (DAT_1442 < 8) {
      DAT_143b = bVar5 * DAT_1442 * '\b';
    }
  }
LAB_b8a0:
  DAT_0093 = DAT_0093 & 0xfe;
  DAT_159d = 0;
  DAT_159e = 0;
  DAT_141c = 0;
LAB_bb6d:
  _DAT_1428 = (ushort)DAT_141c << 0xb;
  return;
}


// ---- FUN_bb78 @ bb78 ----

void FUN_bb78(void)

{
  if ((DAT_00d3 & 2) == 0) {
    if (((DAT_0054 & 8) != 0) || (((DAT_0040 & 4) == 0 && (DAT_1454 < 0x32)))) goto LAB_bb9a;
  }
  else if (DAT_16b0 != '\0') {
LAB_bb9a:
    DAT_0099 = DAT_0099 | 2;
    goto LAB_bb9d;
  }
  DAT_0099 = DAT_0099 & 0xfd;
LAB_bb9d:
  if (DAT_f872 <= DAT_140c) {
    if ((DAT_0053 & 2) == 0) {
      if ((DAT_1442 != '\0') && (DAT_159b == '\0')) {
        if ((DAT_0053 & 1) == 0) {
          DAT_159c = '\x14';
        }
        else if (DAT_159c == '\0') {
          DAT_0049 = DAT_0049 | 2;
          DAT_0017 = DAT_0049;
          DAT_1002 = DAT_0099;
          return;
        }
      }
    }
    else {
      DAT_159b = '\0';
      if (DAT_f870 <= DAT_140c) {
        DAT_159b = DAT_f871;
      }
    }
  }
  DAT_0049 = DAT_0049 & 0xfd;
  DAT_0017 = DAT_0049;
  DAT_1002 = DAT_0099;
  return;
}


// ---- FUN_bbe7 @ bbe7 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_bbe7(void)

{
  bool bVar1;
  ushort uVar2;
  byte bVar3;
  ushort uVar4;
  char cVar5;
  byte bVar6;
  byte *pbVar7;
  byte bStack_1;
  
  bVar6 = DAT_145b;
  bVar3 = DAT_00d6;
  if ((DAT_0054 & 8) == 0) {
    if (DAT_1442 < 4) {
      if ((DAT_0053 & 2) == 0) {
        DAT_148c = DAT_1404;
      }
      else if ((((DAT_0053 & 0x44) != 0) && (0x7c < DAT_148c)) &&
              (DAT_1404 <= (byte)(DAT_148c - 0xc))) goto LAB_bc3d;
LAB_bc54:
      DAT_00c8 = DAT_00c8 & 0x7f;
LAB_bc5a:
      DAT_0085 = 0;
    }
    else {
LAB_bc3d:
      DAT_0085 = DAT_0085 | 0x80;
      DAT_00c8 = DAT_00c8 | 0x80;
      if (0x89 < DAT_0085) goto LAB_bc49;
    }
  }
  else {
    if (DAT_1442 != 0) {
      DAT_1473 = 0;
      if ((DAT_1442 < 0x30) || ((0x72 < _DAT_1465 && (_DAT_1465 < 0x7e)))) goto LAB_bc54;
      goto LAB_bc3d;
    }
    DAT_1473 = DAT_1473 | 0x80;
    if (DAT_1473 < 0x94) {
      DAT_00c8 = DAT_00c8 | 0x80;
      goto LAB_bc5a;
    }
LAB_bc49:
    DAT_00c3 = DAT_00c3 | 0x80;
    DAT_00d5 = DAT_00d5 | 0x80;
    DAT_1648 = 0;
  }
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_1405 < 3) || (0xf1 < DAT_1405)) {
      DAT_00c3 = DAT_00c3 | 0x20;
      DAT_00c8 = DAT_00c8 | 0x20;
      DAT_00d5 = DAT_00d5 | 0x20;
      DAT_164a = 0;
    }
    else {
      DAT_00c8 = DAT_00c8 & 0xdf;
    }
  }
  if ((DAT_0054 & 8) == 0) {
    if (0x31 < DAT_1454) {
      if ((DAT_0054 & 1) == 0) {
        if (399 < _DAT_1408) {
          DAT_0081 = DAT_0081 | 0x80;
          if (0xe3 < DAT_0081) {
            DAT_00c8 = DAT_00c8 | 0x40;
            DAT_0047 = DAT_0047 | 2;
            DAT_00d5 = DAT_00d5 | 0x40;
            goto LAB_bcc8;
          }
          goto LAB_bcdf;
        }
        DAT_0081 = 0;
      }
      DAT_00c8 = DAT_00c8 & 0xbf;
    }
  }
  else if (0x2f < DAT_1442) {
    if ((DAT_007e & 1) == 0) {
      DAT_0081 = 0;
      DAT_00c8 = DAT_00c8 & 0xbf;
    }
    else {
      DAT_0081 = DAT_0081 | 0x80;
      if (0xe3 < DAT_0081) {
LAB_bcc8:
        DAT_00c3 = DAT_00c3 | 0x40;
        DAT_00c8 = DAT_00c8 | 0x40;
        DAT_00d5 = DAT_00d5 | 0x40;
        DAT_1649 = 0;
        DAT_0081 = 0;
      }
    }
  }
LAB_bcdf:
  if ((DAT_00cc & 0x10) != 0) {
    DAT_00c7 = DAT_00c7 | 0x10;
    DAT_00d9 = DAT_00d9 | 0x10;
    DAT_166b = 0;
  }
  if ((P2DATA & 0x40) != 0) {
    DAT_0047 = DAT_0047 | 1;
    DAT_00d6 = DAT_00d6 | 0x80;
    DAT_145b = DAT_145b + 1;
    if (DAT_145b == 0) {
      DAT_145b = bVar6;
    }
    if (9 < DAT_145b) {
      DAT_00c4 = DAT_00c4 | 0x80;
      DAT_00d6 = bVar3 | 0x80;
      DAT_1650 = 0;
      goto LAB_bd15;
    }
  }
  DAT_00c9 = DAT_00c9 & 0x7f;
LAB_bd15:
  if ((DAT_0053 & 2) == 0) {
    DAT_0046 = DAT_0046 & 0xfb;
  }
  else if ((DAT_0046 & 4) == 0) {
    DAT_0046 = DAT_0046 | 4;
    uVar4 = 0x8000;
    do {
      bVar3 = (byte)(uVar4 >> 8);
      if ((bVar3 & (&DAT_f924)[uVar4 & 0xff]) != 0) {
        cVar5 = (char)uVar4;
        uVar4 = CONCAT11(bVar3,(char)_bStack_1);
        bVar6 = cVar5 << 3;
        while (bVar1 = (bool)(bVar3 >> 7), bVar3 = bVar3 << 1, !bVar1) {
          bVar6 = bVar6 + 1;
        }
        pbVar7 = &DAT_1648 + bVar6;
        if ((byte *)0x166c < pbVar7) {
          return;
        }
        *pbVar7 = *pbVar7 + 1;
        _bStack_1 = uVar4;
        if (*pbVar7 == 0) {
          *pbVar7 = ~*pbVar7;
        }
      }
      uVar2 = uVar4 & 0x100;
      cVar5 = (char)uVar4;
      uVar4 = CONCAT11((byte)(uVar4 >> 9),cVar5);
      if ((uVar2 != 0) && (bVar3 = cVar5 + 1, uVar4 = CONCAT11(0x80,bVar3), 4 < bVar3)) {
        return;
      }
    } while( true );
  }
  return;
}


// ---- FUN_bd58 @ bd58 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_bd58(void)

{
  undefined1 uVar1;
  undefined1 extraout_B;
  undefined2 uVar2;
  
  if ((((DAT_00d3 & 8) != 0) && (DAT_16b2 == '\0')) && ((DAT_0043 & 2) == 0)) {
    DAT_0043 = DAT_0043 | 2;
    FUN_bd97();
  }
  _DAT_0074 = &DAT_1700;
  _DAT_0076 = 0xfba8;
  uVar2 = 0xfba0;
  _DAT_0078 = 0xfba0;
  FUN_bdb1();
  uVar1 = FUN_99cb();
  _DAT_148e = CONCAT11(uVar1,extraout_B);
  _DAT_1486 = uVar2;
  DAT_147f = DAT_1490;
  DAT_1488 = DAT_1491;
  return;
}


// ---- FUN_bd97 @ bd97 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_bd97(void)

{
  undefined2 *puVar1;
  
  _DAT_147c = 0;
  DAT_0087 = 0;
  puVar1 = (undefined2 *)&DAT_1700;
  _DAT_1645 = 0x6400;
  do {
    *puVar1 = 0x6400;
    puVar1 = puVar1 + 1;
  } while (puVar1 != (undefined2 *)0x1780);
  return;
}


// ---- FUN_bd9e @ bd9e ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_bd9e(void)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)&DAT_1700;
  _DAT_1645 = 0x6400;
  do {
    *puVar1 = 0x6400;
    puVar1 = puVar1 + 1;
  } while (puVar1 != (undefined2 *)0x1780);
  return;
}


// ---- FUN_bdb1 @ bdb1 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 FUN_bdb1(void)

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
    if (bVar6 < _DAT_0076[7]) goto LAB_be1f;
    bVar6 = _DAT_0076[7];
  }
  _DAT_0067 = (ushort)bVar6 << 2;
LAB_be1f:
  puVar8 = (ushort *)((short)_DAT_0074 + 0x7e);
  DAT_0072 = (char)((ushort)uVar1 >> 8);
  _DAT_006b = CONCAT11((char)((ushort)_DAT_0069 >> 8) - DAT_0072,(char)_DAT_0069);
  DAT_006d = '\0';
  DAT_0073 = (char)uVar1;
  DAT_006e = DAT_0073 - DAT_0072;
  DAT_006f = 0;
  _DAT_0072 = uVar1;
  _DAT_0074 = puVar8;
  FUN_827b();
  DAT_1490 = extraout_B;
  if ((puVar8[1] < *puVar8) && (DAT_006d != '\0')) {
    DAT_006d = -DAT_006d;
    uVar3 = FUN_bec9();
    _DAT_008b = CONCAT11(uVar3,extraout_B_01) + puVar8[1];
  }
  else {
    uVar3 = FUN_bec9();
    _DAT_008b = CONCAT11(uVar3,extraout_B_00) + *puVar8;
  }
  DAT_006d = DAT_1490;
  if ((puVar8[9] < puVar8[8]) && (DAT_1490 != '\0')) {
    DAT_006d = -DAT_1490;
    uVar3 = FUN_bec9();
    _DAT_008d = CONCAT11(uVar3,extraout_B_03) + puVar8[9];
  }
  else {
    uVar3 = FUN_bec9();
    _DAT_008d = CONCAT11(uVar3,extraout_B_02) + puVar8[8];
  }
  sVar4 = _DAT_0067 + (ushort)DAT_0070 * -4;
  _DAT_006b = sVar4 * 4;
  DAT_006d = (char)((char)sVar4 << 7) >> 1;
  DAT_006f = DAT_0071 - DAT_0070;
  DAT_006e = 0;
  FUN_827b();
  DAT_1491 = extraout_B_04;
  if ((_DAT_008d < _DAT_008b) && (DAT_006d != '\0')) {
    DAT_006d = -DAT_006d;
    uVar3 = FUN_bec9();
    uVar3 = (undefined1)(CONCAT11(uVar3,extraout_B_06) + _DAT_008d >> 8);
  }
  else {
    uVar3 = FUN_bec9();
    uVar3 = (undefined1)(CONCAT11(uVar3,extraout_B_05) + _DAT_008b >> 8);
  }
  return uVar3;
}


// ---- FUN_bec9 @ bec9 ----

char FUN_bec9(void)

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


// ---- vec_ICF @ bede ----

undefined1 vec_ICF(void)

{
  undefined1 in_stack_00000003;
  
  return in_stack_00000003;
}


// ---- vec_OCF @ bedf ----

undefined1 vec_OCF(void)

{
  undefined1 in_stack_00000003;
  
  return in_stack_00000003;
}


// ---- vec_TOF @ bee0 ----

undefined1 vec_TOF(void)

{
  undefined1 in_stack_00000003;
  
  return in_stack_00000003;
}


// ---- vec_SWI @ bee1 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 vec_SWI(void)

{
  short sVar1;
  undefined1 in_stack_00000003;
  
  _DAT_1642 = 0;
  if ((DAT_0015 & 0x10) != 0) {
    _DAT_1642 = 0x55aa;
  }
  sVar1 = 500;
  do {
    sVar1 = sVar1 + -1;
  } while (sVar1 != 0);
  return in_stack_00000003;
}


