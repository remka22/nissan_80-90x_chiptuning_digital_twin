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

undefined1 vec_IRQ(void)

{
  undefined1 in_stack_00000003;
  
  if ((DAT_00db & 0x40) == 0) {
    DAT_00c6 = DAT_102e;
    DAT_1034 = ~(DAT_102e & 0x24);
    if ((((DAT_0040 & 8) != 0) || ((DAT_0054 & 8) != 0)) && ((DAT_1034 & 4) == 0)) {
      FUN_8741();
    }
    if ((((DAT_0040 & 8) != 0) || ((DAT_00c6 & 0x20) == 0)) || ((DAT_0054 & 8) == 0)) {
      return in_stack_00000003;
    }
    FUN_88a2();
  }
  else {
    DAT_00c6 = DAT_102e;
    DAT_1034 = ~(DAT_102e & 0x2c);
    DAT_00dc = DAT_102f;
    DAT_1035 = ~(DAT_102f & 0x1f);
    if ((((DAT_0040 & 8) != 0) || ((DAT_0054 & 8) != 0)) && ((DAT_1035 & 0x10) == 0)) {
      FUN_8741();
      if (((DAT_00c6 & 0xc) != 0) || ((DAT_00dc & 0xf) != 0)) {
        DAT_00c6 = DAT_00c6 & 0xf3;
        DAT_00dc = DAT_00dc & 0xf0;
        DAT_1598 = 0;
        DAT_1599 = 0;
        DAT_1597 = 0;
      }
      if (((DAT_102e & 0xc) != 0) || ((DAT_102f & 0xf) != 0)) {
        DAT_1034 = 0xf3;
        DAT_1035 = 0xf0;
        DAT_1598 = 0;
        DAT_1599 = 0;
        DAT_1597 = 0;
      }
    }
    if (((DAT_00c6 & 0xc) != 0) || ((DAT_00dc & 0xf) != 0)) {
      FUN_84e2();
      DAT_00c6 = DAT_00c6 & 0xf3;
      DAT_00dc = DAT_00dc & 0xf0;
    }
    if ((((DAT_0040 & 8) != 0) || ((DAT_00c6 & 0x20) == 0)) || ((DAT_0054 & 8) == 0)) {
      return in_stack_00000003;
    }
    FUN_88a2();
    if (((DAT_102e & 0xc) != 0) || ((DAT_102f & 0xf) != 0)) {
      DAT_1034 = 0xf3;
      DAT_1035 = 0xf0;
      DAT_1598 = 0;
      DAT_1599 = 0;
      DAT_1597 = 0;
    }
  }
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
            FUN_9b20();
            FUN_9b35();
            FUN_9c76();
            FUN_9d2a();
            FUN_9fe3();
            FUN_aaff();
            FUN_a597();
            if ((DAT_0040 & 8) == 0) {
              FUN_a1eb();
              FUN_c8dc();
              FUN_a560();
              FUN_a9d4();
            }
            else {
              FUN_c97b();
              FUN_c9a8();
            }
            DAT_144a = DAT_0053;
          }
          else {
            DAT_0054 = DAT_0054 & 0xef | 0x80;
            FUN_95c2();
            thunk_FUN_9623();
          }
        }
        else {
          DAT_0054 = DAT_0054 & 0xbf | 0x80;
          FUN_8e2b();
          if ((DAT_0040 & 8) == 0) {
            FUN_9266();
            FUN_9320();
            FUN_950d();
            FUN_9588();
          }
          else {
            FUN_9320();
            FUN_950d();
            FUN_c711();
            FUN_c884();
          }
        }
      }
      else {
        DAT_0054 = DAT_0054 & 0xdf | 0x80;
        FUN_8949();
        FUN_89d4();
        FUN_8a6a();
        FUN_8a8d();
        FUN_8b9c();
        FUN_8d7a();
        FUN_8d99();
        FUN_8dd6();
      }
    }
    else {
      DAT_0054 = DAT_0054 | 0x80;
      DAT_0055 = DAT_0055 & 0xbf;
      FUN_8903();
    }
    DAT_0054 = DAT_0054 & 0x7f;
    DAT_2000 = DAT_00bc;
    DAT_4000 = DAT_00b4;
    P2DATA = DAT_00d3;
    DAT_0017 = DAT_00d4;
    DAT_1002 = DAT_009c;
  } while( true );
}


// ---- vec_ICF @ 84af ----

undefined1 vec_ICF(void)

{
  undefined1 in_stack_00000003;
  
  if ((DAT_0040 & 8) == 0) {
    FUN_852c();
    DAT_0054 = DAT_0054 | 8;
    if (((DAT_102e & 0xc) != 0) || ((DAT_102f & 0xf) != 0)) {
      DAT_1034 = 0xf3;
      DAT_1035 = 0xf0;
      DAT_1598 = 0;
      DAT_1599 = 0;
      DAT_1597 = 0;
    }
  }
  return in_stack_00000003;
}


// ---- FUN_84e2 @ 84e2 ----

void FUN_84e2(void)

{
  char cVar1;
  
  cVar1 = '\0';
  do {
    cVar1 = cVar1 + '\x01';
  } while (cVar1 != '!');
  if ((DAT_2000 & 0x80) == 0) {
    DAT_00dd = DAT_00dd | 1;
  }
  DAT_1597 = DAT_1597 + 1;
  if (5 < DAT_1597) {
    DAT_1597 = 0;
    if ((DAT_00dd & 1) == 0) {
      DAT_1598 = 0;
      DAT_00dd = DAT_00dd & 0xfd;
      if (0x31 < DAT_1599) {
        DAT_00cd = DAT_00cd & 0x7f;
      }
    }
    else {
      DAT_00dd = DAT_00dd & 0xfe;
      DAT_1599 = 0;
      DAT_00dd = DAT_00dd | 2;
      if (0x31 < DAT_1598) {
        DAT_00cd = DAT_00cd | 0x80;
      }
    }
  }
  return;
}


// ---- FUN_8741 @ 8741 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8741(void)

{
  short sVar1;
  
  DAT_00d0 = 0;
  if (DAT_009f != 0) {
    DAT_00d0 = DAT_009f & DAT_00a2;
    DAT_009f = ~DAT_00d0 & DAT_009f;
    if (((DAT_fee1 & 0x20) != 0) && ((DAT_00cf == 0x3f || (DAT_00cf == 0x15)))) {
      DAT_00d0 = DAT_00d0 & 0xea;
    }
  }
  if ((DAT_00a6 & 1) != 0) {
    sVar1 = _DAT_1579;
    if ((DAT_00cf & 1) == 0) {
      sVar1 = _DAT_004d;
    }
    if ((DAT_00d0 & 1) != 0) {
      sVar1 = sVar1 + _DAT_14de;
    }
    sVar1 = CONCAT11(~(byte)((ushort)sVar1 >> 8),~(byte)sVar1);
    if ((DAT_1048 != '\0') && ((DAT_00ce & 1) != 0)) {
      sVar1 = sVar1 + _DAT_1048;
    }
    _DAT_1048 = sVar1;
    FUN_888d();
  }
  if ((DAT_00a6 & 2) != 0) {
    sVar1 = _DAT_1579;
    if ((DAT_00cf & 2) == 0) {
      sVar1 = _DAT_004d;
    }
    if ((DAT_00d0 & 2) != 0) {
      sVar1 = sVar1 + _DAT_14de;
    }
    sVar1 = CONCAT11(~(byte)((ushort)sVar1 >> 8),~(byte)sVar1);
    if ((DAT_104a != '\0') && ((DAT_00ce & 2) != 0)) {
      sVar1 = sVar1 + _DAT_104a;
    }
    _DAT_104a = sVar1;
    FUN_888d();
  }
  if ((DAT_00a6 & 4) != 0) {
    sVar1 = _DAT_1579;
    if ((DAT_00cf & 4) == 0) {
      sVar1 = _DAT_004d;
    }
    if ((DAT_00d0 & 4) != 0) {
      sVar1 = sVar1 + _DAT_14de;
    }
    sVar1 = CONCAT11(~(byte)((ushort)sVar1 >> 8),~(byte)sVar1);
    if ((DAT_104c != '\0') && ((DAT_00ce & 4) != 0)) {
      sVar1 = sVar1 + _DAT_104c;
    }
    _DAT_104c = sVar1;
    FUN_888d();
  }
  if ((DAT_00a6 & 8) != 0) {
    sVar1 = _DAT_1579;
    if ((DAT_00cf & 8) == 0) {
      sVar1 = _DAT_004d;
    }
    if ((DAT_00d0 & 8) != 0) {
      sVar1 = sVar1 + _DAT_14de;
    }
    sVar1 = CONCAT11(~(byte)((ushort)sVar1 >> 8),~(byte)sVar1);
    if ((DAT_104e != '\0') && ((DAT_00ce & 8) != 0)) {
      sVar1 = sVar1 + _DAT_104e;
    }
    _DAT_104e = sVar1;
    FUN_888d();
  }
  if ((DAT_00a6 & 0x10) != 0) {
    sVar1 = _DAT_1579;
    if ((DAT_00cf & 0x10) == 0) {
      sVar1 = _DAT_004d;
    }
    if ((DAT_00d0 & 0x10) != 0) {
      sVar1 = sVar1 + _DAT_14de;
    }
    sVar1 = CONCAT11(~(byte)((ushort)sVar1 >> 8),~(byte)sVar1);
    if ((DAT_1050 != '\0') && ((DAT_00ce & 0x10) != 0)) {
      sVar1 = sVar1 + _DAT_1050;
    }
    _DAT_1050 = sVar1;
    FUN_888d();
  }
  if ((DAT_00a6 & 0x20) != 0) {
    sVar1 = _DAT_1579;
    if ((DAT_00cf & 0x20) == 0) {
      sVar1 = _DAT_004d;
    }
    if ((DAT_00d0 & 0x20) != 0) {
      sVar1 = sVar1 + _DAT_14de;
    }
    sVar1 = CONCAT11(~(byte)((ushort)sVar1 >> 8),~(byte)sVar1);
    if ((DAT_1052 != '\0') && ((DAT_00ce & 0x20) != 0)) {
      sVar1 = sVar1 + _DAT_1052;
    }
    _DAT_1052 = sVar1;
    FUN_888d(0x20);
  }
  DAT_14b1 = (char)(_DAT_004d << 5);
  return;
}


// ---- FUN_888d @ 888d ----

void FUN_888d(byte param_1)

{
  char cVar1;
  
  DAT_00ce = ~param_1 & DAT_00ce;
  cVar1 = '\0';
  do {
    cVar1 = cVar1 + '\x01';
  } while (cVar1 != '\x05');
  DAT_1036 = 0;
  return;
}


// ---- FUN_88a2 @ 88a2 ----

void FUN_88a2(void)

{
  DAT_00d6 = DAT_00d6 + 1;
  if ((DAT_0017 & 8) != 0) {
    DAT_00d6 = DAT_fef9;
    DAT_00a0 = DAT_f92c & 0x3f;
    DAT_14c8 = DAT_14c8 | 0x80;
  }
  if (5 < DAT_00d6) {
    DAT_00d6 = 0;
  }
  if ((DAT_00d6 == 2) || (DAT_00d6 == 5)) {
    DAT_0054 = DAT_0054 | 0x10;
  }
  if ((DAT_0054 & 4) == 0) {
    DAT_0054 = DAT_0054 | 4;
    DAT_0051 = 0;
  }
  return;
}


// ---- FUN_8903 @ 8903 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8903(void)

{
  byte bVar1;
  
  if ((DAT_00db & 0x40) == 0) {
    bVar1 = DAT_1002 & 4;
  }
  else {
    bVar1 = DAT_1003 & 0x10;
  }
  if (bVar1 == 0) {
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


// ---- FUN_8949 @ 8949 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8949(void)

{
  undefined1 uVar1;
  char cVar2;
  undefined1 extraout_B;
  short sVar3;
  undefined1 extraout_B_00;
  byte bVar4;
  ushort uVar5;
  
  uVar1 = FUN_b4d4();
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
      if ((byte)(sVar3 << 1) < 0x30) goto LAB_899a;
    }
    DAT_0047 = DAT_0047 | 2;
    DAT_0048 = DAT_0048 | 0x40;
  }
LAB_899a:
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


// ---- FUN_89d4 @ 89d4 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_89d4(void)

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


// ---- FUN_8a6a @ 8a6a ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8a6a(void)

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


// ---- FUN_8a8d @ 8a8d ----

void FUN_8a8d(void)

{
  if ((DAT_0053 & 2) == 0) {
    DAT_004f = DAT_004f & 0xfe;
    FUN_8b1d();
    if (0x3b < DAT_1453) {
      return;
    }
  }
  else {
    FUN_8aae();
  }
  if (DAT_142e < 0x10) {
    FUN_8ad6();
  }
  return;
}


// ---- FUN_8aae @ 8aae ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8aae(void)

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


// ---- FUN_8ad6 @ 8ad6 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 FUN_8ad6(void)

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


// ---- FUN_8b1d @ 8b1d ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8b1d(void)

{
  char cVar1;
  byte bVar2;
  byte extraout_B;
  
  _DAT_005b = _DAT_1482;
  if (DAT_1470 != '\0') {
    DAT_1470 = DAT_1470 + -1;
    goto LAB_8b6d;
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
        if (DAT_1442 <= bVar2) goto LAB_8b67;
      }
      if ((DAT_0051 & 4) == 0) {
        DAT_0051 = DAT_0051 | 4;
        DAT_1470 = '2';
      }
      goto LAB_8b6d;
    }
  }
LAB_8b67:
  DAT_0051 = DAT_0051 & 0xfb;
  _DAT_005b = _DAT_1413;
LAB_8b6d:
  _DAT_14f2 = _DAT_005b;
  FUN_8001();
  if ((DAT_0053 & 1) == 0) {
    DAT_15b5 = (undefined1)((ushort)_DAT_148e >> 8);
  }
  else {
    DAT_15b5 = (undefined1)((ushort)_DAT_16a5 >> 8);
  }
  cVar1 = FUN_8001();
  _DAT_1411 = CONCAT11(cVar1 + CARRY1(extraout_B,DAT_142c),extraout_B + DAT_142c) + _DAT_1450;
  return;
}


// ---- FUN_8b9c @ 8b9c ----

void FUN_8b9c(void)

{
  byte extraout_B;
  byte extraout_B_00;
  byte extraout_B_01;
  byte bVar1;
  
  FUN_8be9();
  DAT_1542 = extraout_B;
  if (DAT_1407 == 0) {
    if ((DAT_1460 < DAT_ffe9) || (DAT_1413 < DAT_feea)) {
      DAT_1543 = 0;
      goto LAB_8c02;
    }
    DAT_0050 = DAT_0050 | 0x80;
    bVar1 = DAT_0050 < 0x85;
    if (!(bool)bVar1) {
      bVar1 = 0;
      FUN_8be9();
      bVar1 = bVar1 & 0xf1;
      DAT_1543 = extraout_B_00;
    }
  }
  else {
    DAT_1543 = FUN_8bde();
LAB_8c02:
    DAT_0050 = 0;
    bVar1 = 0;
  }
  if ((DAT_0053 & 1) == 0) {
    DAT_004f = DAT_004f & 0xf9;
LAB_8c1e:
    if ((DAT_004f & 8) != 0) {
LAB_8c26:
      DAT_1474 = 0;
      DAT_004f = DAT_004f & 0xf7;
    }
  }
  else {
    if ((DAT_004f & 2) != 0) {
      if ((DAT_00b5 & 1) != 0) {
        FUN_8be9(0);
        if (extraout_B_01 != 0) {
          DAT_004f = DAT_004f | 8;
          DAT_1544 = extraout_B_01;
          goto LAB_8d16;
        }
        goto LAB_8c1e;
      }
      if ((DAT_004f & 8) == 0) {
        if ((((DAT_0053 & 0x40) != 0) && ((DAT_0053 & 8) != 0)) && ((DAT_004f & 4) == 0)) {
          DAT_004f = DAT_004f | 4;
          goto LAB_8ced;
        }
        FUN_8d64();
        if ((bVar1 & 1) == 0 && (bVar1 >> 2 & 1) == 0) goto LAB_8c34;
        goto LAB_8cf7;
      }
      FUN_8d64();
      if ((bVar1 & 1) != 0 || (bVar1 >> 2 & 1) != 0) {
        bVar1 = 1;
        if ((DAT_1407 < DAT_ff85) || (((DAT_0053 & 0x40) != 0 && (bVar1 = 0, (DAT_0053 & 8) == 0))))
        {
          FUN_8d64();
          if (!(bool)(bVar1 & 1) && !(bool)(bVar1 >> 2 & 1)) goto LAB_8c26;
        }
        else if ((DAT_0053 & 0x10) != 0) {
          bVar1 = (DAT_ffaf == '\0') << 2;
          FUN_8d6a();
          if (!(bool)(bVar1 & 1) && !(bool)(bVar1 >> 2 & 1)) goto LAB_8c26;
        }
        if ((DAT_1474 == 0) && (DAT_1544 < 6)) {
          if (DAT_1544 == 0) {
            DAT_1544 = 0;
            DAT_1474 = DAT_fefa;
          }
          DAT_1544 = DAT_1544 + 3;
        }
        goto LAB_8d13;
      }
      goto LAB_8c26;
    }
    DAT_004f = DAT_004f | 2;
    if ((DAT_ff85 <= DAT_1407) &&
       ((bVar1 = 0, (DAT_0053 & 0x40) == 0 || (bVar1 = 0, (DAT_0053 & 8) != 0)))) {
LAB_8ced:
      FUN_8d64();
      if ((bool)(bVar1 & 1) || (bool)(bVar1 >> 2 & 1)) {
LAB_8cf7:
        DAT_004f = DAT_004f | 8;
        if ((DAT_ff90 < DAT_fefa) || (DAT_ff98 <= DAT_1460)) {
          DAT_1544 = 6;
        }
        DAT_1474 = 0;
LAB_8d13:
        DAT_00b0 = DAT_00b0 | 8;
        goto LAB_8d16;
      }
    }
  }
LAB_8c34:
  if (DAT_1474 == 0) {
    DAT_1544 = 0;
  }
  else {
    DAT_1544 = 3;
  }
  DAT_00b0 = DAT_00b0 & 0xf7;
LAB_8d16:
  bVar1 = DAT_1542;
  if (DAT_1542 < DAT_1543) {
    bVar1 = DAT_1543;
  }
  if (bVar1 < DAT_1544) {
    bVar1 = DAT_1544;
  }
  if (bVar1 < DAT_1545) {
    bVar1 = DAT_1545;
  }
  if (6 < bVar1) {
    bVar1 = 6;
  }
  if ((((DAT_0053 & 1) != 0) && (bVar1 == 3)) && (DAT_1544 == 3)) {
    bVar1 = 7;
  }
  if ((DAT_00d9 & 1) == 0) {
    DAT_00cf = (&DAT_8d5c)[bVar1];
  }
  else {
    DAT_00cf = DAT_166f | (&DAT_8d5c)[bVar1];
  }
  return;
}


// ---- FUN_8bde @ 8bde ----

byte FUN_8bde(byte param_1,byte param_2)

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


// ---- FUN_8be9 @ 8be9 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8be9(void)

{
  ushort in_D;
  
  if (in_D <= _DAT_140a) {
    return;
  }
  return;
}


// ---- FUN_8d64 @ 8d64 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 FUN_8d64(void)

{
  byte bVar1;
  ushort uVar2;
  
  bVar1 = FUN_809f();
  uVar2 = (ushort)bVar1;
  if ((DAT_00d2 & 0x10) != 0) {
    uVar2 = CONCAT11(CARRY1(bVar1,DAT_f693),bVar1 + DAT_f693);
  }
  return (char)(uVar2 * 2 - _DAT_140a >> 8);
}


// ---- FUN_8d6a @ 8d6a ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 FUN_8d6a(undefined1 param_1,byte param_2)

{
  ushort uVar1;
  
  uVar1 = (ushort)param_2;
  if ((DAT_00d2 & 0x10) != 0) {
    uVar1 = CONCAT11(CARRY1(param_2,DAT_f693),param_2 + DAT_f693);
  }
  return (char)(uVar1 * 2 - _DAT_140a >> 8);
}


// ---- FUN_8d7a @ 8d7a ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8d7a(void)

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


// ---- FUN_8d99 @ 8d99 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8d99(void)

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
      _DAT_004d = 1;
    }
    _DAT_15bf = _DAT_144e;
    if ((DAT_00cf & 0x3f) == 0x3f) {
      _DAT_15bf = (ushort)DAT_142c;
    }
  }
  return;
}


// ---- FUN_8dd6 @ 8dd6 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_8dd6(undefined1 param_1,undefined1 param_2)

{
  char cVar1;
  char cVar2;
  undefined2 uVar3;
  
  cVar1 = DAT_14f0;
  uVar3 = _DAT_144e;
  FUN_8e00(DAT_14f0,param_2,_DAT_144e);
  cVar2 = DAT_14f1;
  DAT_14f0 = cVar1;
  FUN_8e00(DAT_14f1,(char)uVar3,_DAT_140a << 2);
  DAT_14f1 = cVar2;
  DAT_147a = (&DAT_fa30)[(byte)(cVar2 * '\b' + DAT_14f0)];
  return;
}


// ---- FUN_8e00 @ 8e00 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

byte FUN_8e00(short param_1)

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


// ---- FUN_8e2b @ 8e2b ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_8e2b(void)

{
  byte bVar1;
  bool bVar2;
  byte bVar3;
  byte bVar4;
  byte bVar5;
  undefined1 uVar6;
  byte bVar7;
  byte bVar8;
  undefined1 uVar9;
  char cVar10;
  byte extraout_B;
  short sVar11;
  ushort uVar12;
  undefined1 *puVar13;
  undefined1 *puVar14;
  short *psVar15;
  
  uVar6 = FUN_b4d4();
  sVar11 = CONCAT11(uVar6,extraout_B) << 1;
  bVar8 = (byte)sVar11;
  bVar7 = (char)((ushort)sVar11 >> 8) + CARRY1(bVar8,extraout_B & 1);
  sVar11 = CONCAT11(bVar7,bVar8 + (extraout_B & 1));
  if (1 < bVar7) {
    sVar11 = 0x1ff;
  }
  _DAT_1492 = sVar11;
  sVar11 = _DAT_1492;
  bVar7 = (byte)(sVar11 << 1);
  if ((DAT_00b0 & 1) == 0) {
    DAT_00b0 = DAT_00b0 | 1;
    DAT_1494 = bVar7;
    DAT_1495 = bVar7;
    DAT_1496 = bVar7;
    DAT_1497 = bVar7;
    DAT_1498 = bVar7;
    DAT_1499 = bVar7;
    DAT_149a = bVar7;
    DAT_149b = bVar7;
    DAT_149c = bVar7;
    DAT_149d = bVar7;
  }
  DAT_149e = DAT_149d;
  bVar5 = DAT_149b;
  bVar4 = DAT_1499;
  bVar3 = DAT_1497;
  bVar1 = DAT_1496;
  bVar8 = DAT_1495;
  DAT_149d = DAT_149c;
  DAT_149b = DAT_149a;
  DAT_149c = bVar5;
  DAT_1499 = DAT_1498;
  DAT_149a = bVar4;
  DAT_1497 = DAT_1496;
  DAT_1498 = bVar3;
  DAT_1495 = DAT_1494;
  DAT_1496 = bVar8;
  DAT_1494 = bVar7;
  DAT_1493 = (byte)sVar11;
  DAT_1492 = (char)((ushort)sVar11 >> 8);
  if ((DAT_00b9 & 0x20) == 0) {
    if (((((((DAT_0054 & 1) == 0) && ((DAT_0053 & 2) == 0)) && (99 < DAT_008f)) &&
         ((DAT_1492 == '\0' && (DAT_1493 < DAT_14a0)))) && (0x95 < (byte)(DAT_14a1 + 1U))) &&
       (DAT_14a0 = 0, DAT_16d1 != 0)) {
      DAT_16d1 = 0;
    }
    if (((DAT_0053 & 4) != 0) && ((DAT_1442 < DAT_f7b6 || ((byte)(DAT_1442 - DAT_f7b6) < DAT_143f)))
       ) {
      DAT_16d1 = DAT_14a0;
    }
    DAT_14a2 = bVar7 - (DAT_14a0 >> 1);
    if (bVar7 < DAT_14a0 >> 1) {
      DAT_14a2 = 0;
    }
  }
  else {
    DAT_14a0 = 0xff;
    DAT_16d1 = 0xff;
    DAT_14a2 = DAT_f694;
  }
  DAT_14a1 = 0;
  DAT_14b2 = DAT_1493;
  if (DAT_1492 != '\0') {
    DAT_14b2 = 0xff;
  }
  if ((DAT_00b9 & 0x20) == 0) {
    if (DAT_14a0 <= DAT_14b2) {
      bVar8 = DAT_f920;
      if ((DAT_0053 & 1) != 0) {
        bVar8 = DAT_f921;
      }
      if (bVar8 < (byte)(DAT_14b2 - DAT_14a0)) {
        DAT_0053 = DAT_0053 & 0xfe;
        goto LAB_8f21;
      }
    }
    DAT_0053 = DAT_0053 | 1;
  }
LAB_8f21:
  bVar8 = 0;
  if (((DAT_0053 & 1) != 0) || (bVar8 = DAT_14a2, DAT_158b < DAT_14a2)) {
    DAT_158b = bVar8;
  }
  bVar8 = bVar7 - bVar1;
  if (bVar7 < bVar1) {
    DAT_14a3 = 0;
    DAT_14b9 = -bVar8;
  }
  else {
    DAT_14b9 = '\0';
    DAT_14a3 = bVar8;
  }
  DAT_14a4 = 0x80;
  bVar8 = bVar7 - DAT_149e;
  if (bVar7 < DAT_149e) {
    if (bVar8 < 0x80) {
      bVar8 = 0x80;
    }
  }
  else if (0x7f < bVar8) {
    bVar8 = 0x7f;
  }
  DAT_149f = bVar8 + 0x80;
  if ((DAT_0054 & 8) == 0) {
    _DAT_1492 = sVar11;
    return;
  }
  if ((((DAT_00d5 & 0xf) == 0) && (DAT_f9ec < DAT_152e)) &&
     ((DAT_f9ed <= DAT_152e ||
      (bVar2 = CARRY1(DAT_152f,DAT_f9ef), DAT_152f = DAT_152f + DAT_f9ef, bVar2)))) {
    DAT_152f = 0xff;
  }
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_0053 & 1) != 0) {
      if ((short)((ushort)DAT_1436 << 8) < 0) {
        DAT_1436 = 0;
      }
      if (DAT_1436 < 0x40) {
        DAT_1436 = DAT_1436 + 1;
      }
      goto LAB_90b6;
    }
    if (DAT_1436 < 0x40) {
LAB_90a4:
      DAT_1436 = 0x80;
      goto LAB_90b6;
    }
    puVar13 = (undefined1 *)0xf92d;
    if (DAT_1460 < DAT_f936) {
LAB_8ff3:
      if (((char)DAT_1436 < '\0') && (DAT_009f == 0)) goto LAB_90b6;
      uVar6 = FUN_809f();
      uVar12 = CONCAT11(uVar6,0x40);
    }
    else {
      if (DAT_f939 <= DAT_1460) goto LAB_90a4;
      if (DAT_14a3 < DAT_f93a) goto LAB_8ff3;
      if ((DAT_f937 <= DAT_1460) && (puVar13 = (undefined1 *)0xf930, DAT_f938 <= DAT_1460)) {
        puVar13 = &DAT_f933;
      }
      puVar14 = puVar13;
      if ((DAT_f93b <= DAT_14a3) && (puVar14 = puVar13 + 1, DAT_f93c <= DAT_14a3)) {
        puVar14 = puVar13 + 2;
      }
      uVar6 = *puVar14;
      uVar9 = FUN_809f();
      uVar12 = CONCAT11(uVar9,uVar6);
    }
    _DAT_005b = CONCAT21((uVar12 >> 8) * (uVar12 & 0xff) * 2,DAT_005d);
    FUN_82d5();
    _DAT_14de = _DAT_005b;
    DAT_1436 = 0x80;
    if (DAT_1473 == '\0') {
      DAT_1473 = '$';
      bVar7 = DAT_00a0 & 0x3f & DAT_00a1;
      DAT_009f = ~bVar7 & DAT_00a0 & 0x3f;
      if (((DAT_fee1 & 0x20) != 0) && ((bVar7 == 0x3f || (DAT_00cf == '\x15')))) {
        bVar7 = bVar7 & 0xea;
      }
      DAT_00d0 = bVar7;
      if (bVar7 != 0) {
        _DAT_1589 = CONCAT11(~(byte)((uint3)_DAT_005b >> 0x10),~(byte)((uint3)_DAT_005b >> 8));
        psVar15 = (short *)&DAT_1048;
        bVar8 = 1;
        do {
          bVar1 = bVar7 & 1;
          bVar7 = bVar7 >> 1;
          if (bVar1 != 0) {
            if (*(char *)psVar15 == '\0') {
              DAT_00ce = bVar8 | DAT_00ce;
              sVar11 = _DAT_1589 - _DAT_1579;
              if (_DAT_1589 < _DAT_1579) {
                sVar11 = 0;
              }
            }
            else {
              sVar11 = _DAT_1589 + *psVar15;
            }
            *psVar15 = sVar11;
            FUN_888d();
          }
          bVar8 = bVar8 << 1;
          psVar15 = psVar15 + 1;
        } while (bVar7 != 0);
      }
    }
  }
  else {
    DAT_1436 = 0;
LAB_90b6:
    _DAT_14de = 0;
  }
  if (DAT_1473 != '\0') {
    DAT_1473 = DAT_1473 + -1;
  }
  if (((((DAT_0053 & 2) == 0) && ((short)((ushort)DAT_14a4 << 8) < 0)) && (DAT_009f == 0)) &&
     ((((DAT_1460 < DAT_f922 && (((bool)(DAT_14a3 >> 7) || (DAT_f92b <= (byte)(DAT_14a3 << 1))))) &&
       (DAT_14a7 = FUN_809f(), DAT_14a7 != 0)) &&
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
  bVar7 = DAT_00b0;
  DAT_1452 = (undefined1)((ushort)(_DAT_14a5 << 4) >> 8);
  if ((DAT_0053 & 2) == 0) {
    bVar8 = DAT_14a3 << 1;
    if ((char)DAT_14a3 < '\0') {
      bVar8 = 0xff;
    }
    if (DAT_f93d <= bVar8) {
      DAT_1516 = 0;
      _DAT_1517 = 0;
      DAT_00b0 = DAT_00b0 & 0xfd;
      if ((bVar7 & 4) == 0) {
        DAT_14bf = DAT_14a2;
        DAT_14c3 = 0;
        DAT_00b0 = DAT_00b0 | 4;
      }
      if (bVar8 < DAT_14c3) {
        DAT_1516 = 0;
        _DAT_1517 = 0;
        return;
      }
      DAT_14c3 = bVar8;
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
            goto LAB_91cc;
          }
        }
      }
      _DAT_1514 = 0;
LAB_91cc:
      cVar10 = (char)((ushort)_DAT_1514 >> 8);
      DAT_1513 = cVar10 << 2;
      if ((char)(cVar10 << 1) < '\0') {
        DAT_1513 = -1;
      }
      return;
    }
  }
  if ((DAT_0053 & 2) != 0) {
LAB_9262:
    DAT_00b0 = DAT_00b0 & 0xf9;
    return;
  }
  bVar8 = DAT_14b9 << 1;
  if (DAT_14b9 < '\0') {
    bVar8 = 0xff;
  }
  if (bVar8 < DAT_f93e) goto LAB_9262;
  DAT_1513 = 0;
  _DAT_1514 = 0;
  DAT_00b0 = DAT_00b0 & 0xfb;
  if ((bVar7 & 2) == 0) {
    DAT_14bf = DAT_14a2;
    DAT_14c3 = 0;
    DAT_00b0 = DAT_00b0 | 2;
  }
  if (bVar8 < DAT_14c3) {
    DAT_1513 = 0;
    _DAT_1514 = 0;
    return;
  }
  DAT_14c3 = bVar8;
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
      goto LAB_9259;
    }
  }
  _DAT_1517 = 0;
LAB_9259:
  DAT_1516 = (char)((ushort)_DAT_1517 >> 8) << 2;
  return;
}


// ---- FUN_9266 @ 9266 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9266(void)

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
    if ((DAT_0053 & 1) == 0) goto LAB_92e3;
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
LAB_92e3:
  _DAT_1455 = sVar5;
  if ((((DAT_0053 & 2) == 0) && (0x1f < _DAT_14e3)) &&
     ((_DAT_14e3 * 6 < uVar3 || (uVar3 <= _DAT_14e3 << 1)))) {
    DAT_0047 = DAT_0047 | 8;
    DAT_0048 = DAT_0048 | 0x80;
  }
  _DAT_14e3 = uVar3;
  sVar5 = uVar3 << 1;
  if ((char)((ushort)sVar5 >> 8) != '\0') {
    sVar5 = 0xff;
  }
  DAT_158e = (char)sVar5;
  return;
}


// ---- FUN_9320 @ 9320 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_9320(void)

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
  if ((DAT_00d5 == 0) && (DAT_1477 = DAT_1477 + 1, DAT_1477 == 0)) {
    DAT_1477 = 0xff;
  }
  DAT_152e = cVar3;
  if (((DAT_00d5 & 0xf) == 0) && (DAT_152e = DAT_152e + '\x01', DAT_152e == '\0')) {
    DAT_152e = cVar3;
  }
  if (DAT_1474 != '\0') {
    DAT_1474 = DAT_1474 + -1;
  }
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_0053 & 1) != 0) {
      DAT_00b0 = DAT_00b0 | 0x40;
      goto LAB_93b7;
    }
    if ((DAT_00b0 & 0x40) != 0) {
      DAT_00b0 = DAT_00b0 & 0xbf;
      FUN_809f();
      if (DAT_140c < 0x41) {
        bVar4 = DAT_ff09;
        if (DAT_ff08 <= DAT_1477) goto joined_r0x9383;
LAB_9395:
        uVar5 = CONCAT11(DAT_140c,DAT_ff0a);
LAB_9398:
        bVar4 = (byte)((ushort)bVar2 * (uVar5 & 0xff) >> 8);
      }
      else {
        bVar4 = DAT_fee5;
        if (DAT_1477 < DAT_fee4) goto LAB_9395;
joined_r0x9383:
        if ((DAT_1477 < bVar4) && ((byte)(DAT_1477 * '\x02') < DAT_ff0a)) {
          uVar5 = (ushort)(byte)~(DAT_1477 * '\x02' - DAT_ff0a);
          goto LAB_9398;
        }
        bVar4 = 0;
      }
      bVar1 = bVar4 + bVar2;
      if (CARRY1(bVar4,bVar2)) {
        bVar1 = 0xff;
      }
      goto LAB_93b8;
    }
    if (_DAT_1415 != 0) {
      bVar4 = (byte)_DAT_1415;
      bVar2 = (byte)(_DAT_1415 >> 8);
      _DAT_1415 = CONCAT11(bVar2 - (bVar4 < DAT_ffc6),bVar4 - DAT_ffc6);
      if (bVar2 < (bVar4 < DAT_ffc6)) goto LAB_93b7;
      goto LAB_93bd;
    }
  }
  else {
    DAT_1477 = 0;
LAB_93b7:
    bVar1 = 0;
LAB_93b8:
    _DAT_1415 = (ushort)bVar1 * (ushort)DAT_152f & 0xff00;
LAB_93bd:
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
      goto LAB_9424;
    }
  }
  else if (DAT_14da < DAT_ffb0) {
    uVar5 = CONCAT11(uVar7,DAT_ffb1);
    goto LAB_9424;
  }
  uVar5 = CONCAT11(uVar7,0x40);
LAB_9424:
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


// ---- FUN_950d @ 950d ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_950d(void)

{
  bool bVar1;
  byte bVar2;
  short sVar3;
  
  if ((DAT_0053 & 2) == 0) {
    if (_DAT_15bb != 0) {
      bVar1 = _DAT_15bb < _DAT_f6a5;
      _DAT_15bb = _DAT_15bb - _DAT_f6a5;
      if (bVar1) {
        _DAT_15bb = 0;
      }
      _DAT_15bd = _DAT_15bb << 2;
    }
    if (((DAT_00d5 == '\0') && (DAT_141b != 0)) &&
       (bVar1 = DAT_141b < DAT_15ba, DAT_141b = DAT_141b - DAT_15ba, bVar1)) {
      DAT_141b = 0;
    }
  }
  else {
    DAT_1417 = FUN_809f();
    DAT_15ba = FUN_809f();
    bVar2 = FUN_809f();
    _DAT_15bb = (ushort)bVar2 << 8;
    _DAT_15bd = (ushort)bVar2 << 10;
    DAT_141b = 0xff;
  }
  bVar2 = FUN_809f();
  sVar3 = (ushort)bVar2 * (ushort)DAT_141b;
  if ((SUB21((ushort)sVar3 >> 0xf,0)) || (bVar2 = (byte)((ushort)(sVar3 * 4) >> 8), sVar3 * 2 < 0))
  {
    bVar2 = 0xff;
  }
  _DAT_1420 = (ushort)bVar2 * (ushort)DAT_1417 * 4 + _DAT_15bd;
  return;
}


// ---- FUN_9588 @ 9588 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9588(void)

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


// ---- FUN_95c2 @ 95c2 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_95c2(void)

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


// ---- thunk_FUN_9623 @ 9614 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void thunk_FUN_9623(void)

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
  
  FUN_b4d4();
  DAT_1400 = extraout_B;
  if ((DAT_00d8 & 2) != 0) {
    FUN_9b0a(DAT_1668);
    FUN_9616();
    return;
  }
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
        goto LAB_9a21;
      }
      if ((DAT_fee0 & 0x10) != 0) {
        if ((((DAT_009b & 1) == 0) && (DAT_1400 < DAT_ff92)) && (DAT_009a < DAT_145d))
        goto LAB_9a24;
        if ((DAT_009b & 1) == 0) goto LAB_9767;
        if ((DAT_009b & 2) != 0) {
          if (DAT_ffa0 < DAT_1400) goto LAB_9a24;
LAB_97b4:
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
          goto LAB_97d9;
        }
        if (DAT_ffa1 < DAT_1400) goto LAB_97b4;
        goto LAB_99c9;
      }
      if (0x27 < DAT_1438) {
        DAT_1438 = 0x28;
LAB_9767:
        bVar1 = DAT_ff91;
        if (DAT_1453 < 0x3c) {
          bVar1 = DAT_fee7;
        }
        if (bVar1 <= DAT_140c) {
          if ((DAT_fee0 & 0x10) != 0) goto LAB_97b4;
          if (DAT_1400 < DAT_ff92) {
            if (DAT_ff93 <= DAT_1400) {
              DAT_1437 = 0;
              goto LAB_99c9;
            }
            DAT_1437 = DAT_1437 - 1;
          }
          else {
            DAT_1437 = DAT_1437 + 1;
          }
          if ((short)((ushort)DAT_1437 << 8) < 0) {
            if (DAT_1437 < 0xf6) goto LAB_97b4;
          }
          else if (9 < DAT_1437) {
            DAT_0051 = DAT_0051 | 0x40;
            goto LAB_97b4;
          }
        }
      }
      goto LAB_9a24;
    }
    if ((((DAT_0053 & 1) != 0) && (DAT_ffd1 <= DAT_1442)) && (3 < DAT_1407)) {
      DAT_1434 = 0;
      if ((DAT_0051 & 0x80) != 0) {
        _DAT_1431 = (ushort)DAT_ffd0 << 8;
        DAT_1438 = 0;
        goto LAB_9a3e;
      }
      DAT_1433 = DAT_1433 + 1;
      if (0x13 < DAT_1433) {
        DAT_0051 = DAT_0051 | 0x80;
      }
LAB_97d9:
      if ((DAT_0059 & 8) != 0) {
LAB_97de:
        DAT_00af = 0;
        DAT_0087 = 0;
        _DAT_147c = 0;
        goto LAB_9a21;
      }
      if ((DAT_0053 & 1) == 0) {
        DAT_0051 = DAT_0051 & 0xef;
        goto LAB_9843;
      }
      DAT_0051 = DAT_0051 | 0x10;
      if (((DAT_ffd3 & 1) != 0) && ((DAT_00bc & 0x40) != 0)) goto LAB_97de;
      if (DAT_1407 < 2) {
        if (DAT_140c < 0x73) {
          if ((DAT_ffd3 & 4) != 0) goto LAB_97de;
          goto LAB_9843;
        }
        DAT_00af = DAT_00af | 0x80;
        if ((0x80 < DAT_00af) && (DAT_0087 = DAT_0087 | 0x80, 0x87 < DAT_0087)) {
          uVar2 = FUN_9a4e((char)((ushort)(_DAT_147c << 5) >> 8) + DAT_feec);
          _DAT_1431 = CONCAT11(uVar2,extraout_B_00);
          DAT_1438 = 0;
          goto LAB_9a3e;
        }
      }
      else {
LAB_9843:
        DAT_00af = 0;
        if ((DAT_fef6 != 0) && (0x87 < DAT_0087)) {
          uVar2 = FUN_9a4e();
          _DAT_16a5 = CONCAT11(uVar2,extraout_B_01);
        }
        DAT_0087 = 0;
        _DAT_147c = 0;
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
          DAT_15b9 = DAT_1431;
          DAT_15b7 = (char)(DAT_1431 + DAT_15b8) >> 1 | CARRY1(DAT_1431,DAT_15b8) << 7;
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
        DAT_15b8 = DAT_1431;
        DAT_15b7 = (char)(DAT_1431 + DAT_15b9) >> 1 | CARRY1(DAT_1431,DAT_15b9) << 7;
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
LAB_99c9:
      bVar1 = DAT_009b;
      if ((DAT_0051 & 0x20) != 0) {
        if (DAT_1438 < DAT_ff7e) {
          if (((DAT_00d9 & 8) == 0) || (DAT_1672 != '\0')) {
            FUN_9a60();
          }
          uVar2 = FUN_9a4e((char)((ushort)_DAT_1431 >> 8));
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
          FUN_b246();
        }
        goto LAB_9a1b;
      }
      goto LAB_9a24;
    }
    DAT_1433 = 0;
    if ((DAT_0051 & 0x80) == 0) goto LAB_97d9;
    DAT_1434 = DAT_1434 + 1;
    if (0x13 < DAT_1434) {
      DAT_0051 = DAT_0051 & 0x7f;
    }
  }
  else {
LAB_9a1b:
    DAT_0051 = DAT_0051 & 0xdf;
    DAT_1437 = 0;
LAB_9a21:
    DAT_1438 = 0;
LAB_9a24:
    if ((byte)((ushort)_DAT_1431 >> 8) < 100) {
      _DAT_1431 = _DAT_1431 + 0x15;
      if ((byte)((ushort)_DAT_1431 >> 8) < 100) goto LAB_9a3e;
    }
    else {
      _DAT_1431 = _DAT_1431 + -0x15;
      if (99 < (byte)((ushort)_DAT_1431 >> 8)) goto LAB_9a3e;
    }
  }
  _DAT_1431 = 0x6400;
LAB_9a3e:
  DAT_009b = DAT_009b | 8;
  DAT_15b9 = (byte)((ushort)_DAT_1431 >> 8);
  DAT_15b8 = DAT_15b9;
  DAT_15b7 = DAT_15b9;
  return;
}


// ---- FUN_9616 @ 9616 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9616(void)

{
  undefined2 in_D;
  
  _DAT_1431 = in_D;
  DAT_15b9 = (undefined1)((ushort)in_D >> 8);
  DAT_15b8 = DAT_15b9;
  DAT_15b7 = DAT_15b9;
  return;
}


// ---- FUN_9623 @ 9623 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9623(void)

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
  
  FUN_b4d4();
  DAT_1400 = extraout_B;
  if ((DAT_00d8 & 2) != 0) {
    FUN_9b0a(DAT_1668);
    FUN_9616();
    return;
  }
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
        goto LAB_9a21;
      }
      if ((DAT_fee0 & 0x10) != 0) {
        if ((((DAT_009b & 1) == 0) && (DAT_1400 < DAT_ff92)) && (DAT_009a < DAT_145d))
        goto LAB_9a24;
        if ((DAT_009b & 1) == 0) goto LAB_9767;
        if ((DAT_009b & 2) != 0) {
          if (DAT_ffa0 < DAT_1400) goto LAB_9a24;
LAB_97b4:
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
          goto LAB_97d9;
        }
        if (DAT_ffa1 < DAT_1400) goto LAB_97b4;
        goto LAB_99c9;
      }
      if (0x27 < DAT_1438) {
        DAT_1438 = 0x28;
LAB_9767:
        bVar1 = DAT_ff91;
        if (DAT_1453 < 0x3c) {
          bVar1 = DAT_fee7;
        }
        if (bVar1 <= DAT_140c) {
          if ((DAT_fee0 & 0x10) != 0) goto LAB_97b4;
          if (DAT_1400 < DAT_ff92) {
            if (DAT_ff93 <= DAT_1400) {
              DAT_1437 = 0;
              goto LAB_99c9;
            }
            DAT_1437 = DAT_1437 - 1;
          }
          else {
            DAT_1437 = DAT_1437 + 1;
          }
          if ((short)((ushort)DAT_1437 << 8) < 0) {
            if (DAT_1437 < 0xf6) goto LAB_97b4;
          }
          else if (9 < DAT_1437) {
            DAT_0051 = DAT_0051 | 0x40;
            goto LAB_97b4;
          }
        }
      }
      goto LAB_9a24;
    }
    if ((((DAT_0053 & 1) != 0) && (DAT_ffd1 <= DAT_1442)) && (3 < DAT_1407)) {
      DAT_1434 = 0;
      if ((DAT_0051 & 0x80) != 0) {
        _DAT_1431 = (ushort)DAT_ffd0 << 8;
        DAT_1438 = 0;
        goto LAB_9a3e;
      }
      DAT_1433 = DAT_1433 + 1;
      if (0x13 < DAT_1433) {
        DAT_0051 = DAT_0051 | 0x80;
      }
LAB_97d9:
      if ((DAT_0059 & 8) != 0) {
LAB_97de:
        DAT_00af = 0;
        DAT_0087 = 0;
        _DAT_147c = 0;
        goto LAB_9a21;
      }
      if ((DAT_0053 & 1) == 0) {
        DAT_0051 = DAT_0051 & 0xef;
        goto LAB_9843;
      }
      DAT_0051 = DAT_0051 | 0x10;
      if (((DAT_ffd3 & 1) != 0) && ((DAT_00bc & 0x40) != 0)) goto LAB_97de;
      if (DAT_1407 < 2) {
        if (DAT_140c < 0x73) {
          if ((DAT_ffd3 & 4) != 0) goto LAB_97de;
          goto LAB_9843;
        }
        DAT_00af = DAT_00af | 0x80;
        if ((0x80 < DAT_00af) && (DAT_0087 = DAT_0087 | 0x80, 0x87 < DAT_0087)) {
          uVar2 = FUN_9a4e((char)((ushort)(_DAT_147c << 5) >> 8) + DAT_feec);
          _DAT_1431 = CONCAT11(uVar2,extraout_B_00);
          DAT_1438 = 0;
          goto LAB_9a3e;
        }
      }
      else {
LAB_9843:
        DAT_00af = 0;
        if ((DAT_fef6 != 0) && (0x87 < DAT_0087)) {
          uVar2 = FUN_9a4e();
          _DAT_16a5 = CONCAT11(uVar2,extraout_B_01);
        }
        DAT_0087 = 0;
        _DAT_147c = 0;
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
          DAT_15b9 = DAT_1431;
          DAT_15b7 = (char)(DAT_1431 + DAT_15b8) >> 1 | CARRY1(DAT_1431,DAT_15b8) << 7;
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
        DAT_15b8 = DAT_1431;
        DAT_15b7 = (char)(DAT_1431 + DAT_15b9) >> 1 | CARRY1(DAT_1431,DAT_15b9) << 7;
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
LAB_99c9:
      bVar1 = DAT_009b;
      if ((DAT_0051 & 0x20) != 0) {
        if (DAT_1438 < DAT_ff7e) {
          if (((DAT_00d9 & 8) == 0) || (DAT_1672 != '\0')) {
            FUN_9a60();
          }
          uVar2 = FUN_9a4e((char)((ushort)_DAT_1431 >> 8));
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
          FUN_b246();
        }
        goto LAB_9a1b;
      }
      goto LAB_9a24;
    }
    DAT_1433 = 0;
    if ((DAT_0051 & 0x80) == 0) goto LAB_97d9;
    DAT_1434 = DAT_1434 + 1;
    if (0x13 < DAT_1434) {
      DAT_0051 = DAT_0051 & 0x7f;
    }
  }
  else {
LAB_9a1b:
    DAT_0051 = DAT_0051 & 0xdf;
    DAT_1437 = 0;
LAB_9a21:
    DAT_1438 = 0;
LAB_9a24:
    if ((byte)((ushort)_DAT_1431 >> 8) < 100) {
      _DAT_1431 = _DAT_1431 + 0x15;
      if ((byte)((ushort)_DAT_1431 >> 8) < 100) goto LAB_9a3e;
    }
    else {
      _DAT_1431 = _DAT_1431 + -0x15;
      if (99 < (byte)((ushort)_DAT_1431 >> 8)) goto LAB_9a3e;
    }
  }
  _DAT_1431 = 0x6400;
LAB_9a3e:
  DAT_009b = DAT_009b | 8;
  DAT_15b9 = (byte)((ushort)_DAT_1431 >> 8);
  DAT_15b8 = DAT_15b9;
  DAT_15b7 = DAT_15b9;
  return;
}


// ---- FUN_9a4e @ 9a4e ----

byte FUN_9a4e(byte param_1)

{
  if (param_1 < 0x4b) {
    param_1 = 0x4b;
  }
  else if (0x7c < param_1) {
    param_1 = 0x7d;
  }
  return param_1;
}


// ---- FUN_9a60 @ 9a60 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9a60(void)

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
     ((((DAT_0051 & 0x80) == 0 && ((DAT_00bc & 0x40) == 0)) && ((DAT_0088 & 0x80) != 0)))) {
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
    uVar1 = FUN_9af7();
    _DAT_005b = CONCAT11(uVar1,extraout_B);
    uVar1 = FUN_8001((char)((ushort)DAT_fef6 >> 8));
    _DAT_007b = CONCAT11(uVar1,extraout_B_00);
    FUN_9b01();
    uVar1 = FUN_9af7();
    uVar1 = FUN_9b0a((char)((ushort)(CONCAT11(uVar1,extraout_B_01) + *psVar2) >> 8));
    *psVar2 = CONCAT11(uVar1,extraout_B_02);
    FUN_9b01();
    uVar1 = FUN_9af7();
    uVar1 = FUN_9b0a((char)((ushort)(CONCAT11(uVar1,extraout_B_03) + psVar2[1]) >> 8));
    psVar2[1] = CONCAT11(uVar1,extraout_B_04);
    FUN_9b01(~DAT_147f);
    uVar1 = FUN_9af7();
    uVar1 = FUN_9b0a((char)((ushort)(CONCAT11(uVar1,extraout_B_05) + psVar2[8]) >> 8));
    psVar2[8] = CONCAT11(uVar1,extraout_B_06);
    FUN_9b01(DAT_147f);
    uVar1 = FUN_9af7();
    uVar1 = FUN_9b0a((char)((ushort)(CONCAT11(uVar1,extraout_B_07) + psVar2[9]) >> 8));
    psVar2[9] = CONCAT11(uVar1,extraout_B_08);
    return;
  }
  return;
}


// ---- FUN_9af7 @ 9af7 ----

char FUN_9af7(char param_1,char param_2)

{
  if ((DAT_0051 & 1) != 0) {
    param_1 = -(param_1 + (param_2 != '\0'));
  }
  return param_1;
}


// ---- FUN_9b01 @ 9b01 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9b01(void)

{
  ushort in_D;
  
  _DAT_005b = (in_D >> 8) * (in_D & 0xff);
  FUN_8001((char)((ushort)_DAT_007b >> 8));
  return;
}


// ---- FUN_9b0a @ 9b0a ----

byte FUN_9b0a(byte param_1)

{
  byte bVar1;
  
  bVar1 = DAT_f6cf;
  if ((param_1 < DAT_f6cf) || (bVar1 = DAT_f6ce, DAT_f6ce <= param_1)) {
    param_1 = bVar1;
  }
  return param_1;
}


// ---- FUN_9b20 @ 9b20 ----

void FUN_9b20(void)

{
  DAT_1476 = DAT_1476 + 1;
  if (DAT_1476 < 0x15) {
    DAT_0017 = DAT_00d4 ^ 1;
    DAT_00d4 = DAT_0017;
  }
  return;
}


// ---- FUN_9b35 @ 9b35 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9b35(void)

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
    }
    else if (DAT_1469 == '\0') {
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
    DAT_1469 = cVar2;
    uVar3 = (ushort)(DAT_0015 & 0xf0) << 8;
    bVar1 = false;
  }
  else {
    uVar3 = CONCAT11(DAT_0015,bVar4) & 0xf0fb;
    bVar1 = false;
    if ((DAT_0015 & 0x20) == 0) {
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
  if ((uVar3 & 0x4000) != 0) {
    uVar3 = (ushort)(byte)((byte)uVar3 | 2);
  }
  DAT_1520 = (char)uVar3;
  DAT_169b = DAT_0053 & 0x17;
  DAT_169c = 0;
  if ((_DAT_140a <= (ushort)DAT_1407 * (ushort)DAT_ff2a * 8) && (!bVar1)) {
    DAT_0053 = DAT_0053 | 8;
  }
  if ((_DAT_140a <= (ushort)DAT_1407 * (ushort)DAT_ffc8 * 8) && (!bVar1)) {
    DAT_0053 = DAT_0053 | 0x80;
  }
  if (((0x7c < DAT_1407) && ((DAT_0015 & 0x80) != 0)) && ((DAT_0017 & 2) != 0)) {
    DAT_0086 = DAT_0086 + 1;
    if (DAT_0086 < 100) goto LAB_9c72;
    DAT_0040 = DAT_0040 | 0x20;
  }
  DAT_0086 = 0;
LAB_9c72:
  DAT_004f = DAT_004f | 0x80;
  return;
}


// ---- FUN_9c76 @ 9c76 ----

void FUN_9c76(void)

{
  byte bVar1;
  
  if ((DAT_00d5 == '\0') && (DAT_1538 != '\0')) {
    DAT_1538 = DAT_1538 + -1;
  }
  if ((DAT_0040 & 8) == 0) {
    if (((DAT_0054 & 8) != 0) &&
       (((DAT_0053 & 0x10) == 0 ||
        (((DAT_0053 & 2) == 0 && ((DAT_f6a7 <= DAT_1453 || (DAT_f6a8 <= DAT_1477)))))))) {
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
          if (DAT_1538 != '\0') goto LAB_9cd2;
        }
      }
      goto LAB_9ce3;
    }
LAB_9cd2:
    DAT_0053 = DAT_0053 & 0xef;
    DAT_0084 = -DAT_ffc1;
  }
  else {
LAB_9ce3:
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
      goto LAB_9d11;
    }
    if (-1 < (char)DAT_0084) {
      DAT_0084 = 0;
    }
    bVar1 = DAT_0084 - 1;
    if (-1 < (char)(DAT_0084 - 1)) {
      bVar1 = DAT_0084;
    }
    DAT_0084 = bVar1;
    if ((byte)-bVar1 < DAT_ffc1) goto LAB_9d11;
  }
  DAT_009c = DAT_009c & 0x7f;
LAB_9d11:
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


// ---- FUN_9d2a @ 9d2a ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9d2a(void)

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
  char cVar26;
  byte bVar27;
  char cVar28;
  bool bVar29;
  char *pcVar30;
  short sVar31;
  
  cVar26 = DAT_15c3;
  cVar25 = DAT_1596;
  cVar24 = DAT_1594;
  cVar23 = DAT_1593;
  cVar22 = DAT_1590;
  cVar21 = DAT_158f;
  cVar20 = DAT_1560;
  cVar19 = DAT_155d;
  cVar18 = DAT_155c;
  cVar17 = DAT_155b;
  cVar16 = DAT_155a;
  cVar15 = DAT_1559;
  cVar14 = DAT_1558;
  cVar13 = DAT_1557;
  cVar12 = DAT_1556;
  cVar11 = DAT_1555;
  cVar10 = DAT_1528;
  cVar9 = DAT_1525;
  cVar8 = DAT_1524;
  cVar7 = DAT_1521;
  cVar6 = DAT_14db;
  cVar5 = DAT_14da;
  cVar4 = DAT_14d9;
  cVar3 = DAT_14d2;
  cVar28 = DAT_14d1;
  bVar2 = DAT_0050;
  if (((short)((ushort)DAT_0081 << 8) < 0) && (DAT_0081 = DAT_0081 + 1, DAT_0081 == 0)) {
    DAT_0081 = 0xff;
  }
  if (((short)((ushort)DAT_00c5 << 8) < 0) && (DAT_00c5 = DAT_00c5 + 1, DAT_00c5 == 0)) {
    DAT_00c5 = 0xff;
  }
  DAT_155c = DAT_155c + '\x01';
  if (DAT_155c == '\0') {
    DAT_155c = cVar18;
  }
  DAT_155d = DAT_155d + '\x01';
  if (DAT_155d == '\0') {
    DAT_155d = cVar19;
  }
  DAT_1557 = DAT_1557 + '\x01';
  if (DAT_1557 == '\0') {
    DAT_1557 = cVar13;
  }
  DAT_1558 = DAT_1558 + '\x01';
  if (DAT_1558 == '\0') {
    DAT_1558 = cVar14;
  }
  DAT_1559 = DAT_1559 + '\x01';
  if (DAT_1559 == '\0') {
    DAT_1559 = cVar15;
  }
  DAT_155a = DAT_155a + '\x01';
  if (DAT_155a == '\0') {
    DAT_155a = cVar16;
  }
  DAT_155b = DAT_155b + '\x01';
  if (DAT_155b == '\0') {
    DAT_155b = cVar17;
  }
  DAT_158f = DAT_158f + '\x01';
  if (DAT_158f == '\0') {
    DAT_158f = cVar21;
  }
  DAT_1590 = DAT_1590 + '\x01';
  if (DAT_1590 == '\0') {
    DAT_1590 = cVar22;
  }
  DAT_15c3 = DAT_15c3 + '\x01';
  if (DAT_15c3 == '\0') {
    DAT_15c3 = cVar26;
  }
  if (DAT_00c0 < '\0') {
    DAT_1593 = DAT_1593 + '\x01';
    DAT_1594 = cVar24;
    if (DAT_1593 == '\0') {
      DAT_1593 = cVar23;
    }
  }
  else {
    DAT_1594 = DAT_1594 + '\x01';
    DAT_1593 = cVar23;
    if (DAT_1594 == '\0') {
      DAT_1594 = cVar24;
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
  bVar27 = DAT_00d5 + 1;
  bVar29 = (0xfe < DAT_00d5 || 9 < bVar27 >> 4) || 8 < bVar27 >> 4 && 9 < (bVar27 & 0xf);
  bVar1 = (byte)((DAT_00d5 & 0xf) + 1) >> 4 == 1 || 9 < (bVar27 & 0xf);
  if (bVar29 && bVar1) {
    bVar27 = DAT_00d5 + 0x67;
  }
  else if (bVar29) {
    bVar27 = DAT_00d5 + 0x61;
  }
  else if (bVar1) {
    bVar27 = DAT_00d5 + 7;
  }
  DAT_00d5 = bVar27;
  if (bVar27 == 0) {
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
      DAT_1524 = cVar8;
      if (DAT_1528 == '\0') {
        DAT_1528 = cVar10;
      }
    }
    else {
      DAT_1524 = DAT_1524 + '\x01';
      DAT_1528 = cVar10;
      if (DAT_1524 == '\0') {
        DAT_1524 = cVar8;
      }
    }
    if (DAT_140c < DAT_f78d) {
      DAT_1596 = '\0';
    }
    else {
      DAT_1596 = DAT_1596 + '\x01';
      if (DAT_1596 == '\0') {
        DAT_1596 = cVar25;
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
      DAT_1560 = cVar20;
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
    if ((bVar27 & 0xf) != 0) {
      return;
    }
  }
  DAT_1525 = DAT_1525 + '\x01';
  if (DAT_1525 == '\0') {
    DAT_1525 = cVar9;
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
    DAT_1555 = cVar11;
  }
  DAT_1556 = DAT_1556 + '\x01';
  if (DAT_1556 == '\0') {
    DAT_1556 = cVar12;
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
    bVar29 = CARRY1(DAT_14ab,bVar2);
    DAT_14ab = DAT_14ab + bVar2;
    if (bVar29) {
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
    DAT_14d1 = cVar28;
  }
  DAT_1539 = DAT_1539 + '\x01';
  DAT_153a = DAT_153a + '\x01';
  if ((char)(DAT_1598 + '\x01') != '\0') {
    DAT_1598 = DAT_1598 + '\x01';
  }
  if ((char)(DAT_1599 + '\x01') != '\0') {
    DAT_1599 = DAT_1599 + '\x01';
  }
  if ((DAT_0054 & 1) == 0) {
    DAT_1475 = 0;
    DAT_00d4 = DAT_00d4 | 0x80;
  }
  else {
    DAT_1475 = DAT_1475 + 1;
    if (0x3b < DAT_1475) {
      pcVar30 = &DAT_16a0;
      cVar28 = '\0';
      do {
        pcVar30 = pcVar30 + 1;
        cVar28 = cVar28 + *pcVar30;
      } while (pcVar30 != (char *)0x17ff);
      DAT_16a0 = -cVar28;
      _DAT_16e0 = 0x6997;
      DAT_00d4 = DAT_00d4 & 0x7f;
      DAT_0017 = DAT_00d4;
      RAMCR = RAMCR & 0xfe;
      TCSR = TCSR & 0xe3;
      P3SCR = P3SCR & 0xf7;
      do {
        sVar31 = 0;
        do {
          sVar31 = sVar31 + 1;
        } while (sVar31 != 0xb6e);
        DAT_1476 = 0;
        FUN_9b20();
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


// ---- FUN_9fe3 @ 9fe3 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_9fe3(void)

{
  bool bVar1;
  byte bVar2;
  ushort uVar3;
  
  bVar2 = DAT_0046;
  _DAT_16d2 = CONCAT11((byte)((ushort)_DAT_00a9 >> 8) & DAT_ff15,(byte)_DAT_00a9 & DAT_ff16);
  _DAT_16d4 = CONCAT11((byte)((ushort)_DAT_00ab >> 8) & DAT_ff17,(byte)_DAT_00ab & DAT_ff18);
  DAT_00ad = DAT_00ad & DAT_ff19;
  DAT_16d6 = DAT_00ad & 0xef;
  uVar3 = _DAT_00c8 & 0x7000;
  _DAT_16e2 = (ushort)((byte)(_DAT_00c8 >> 8) & 0x70) << 8;
  _DAT_16e4 = _DAT_00ca & 0xe828;
  DAT_16e6 = DAT_00cc & 0x80;
  _DAT_00cc = _DAT_00cc & 0x80ffff;
  _DAT_16e7 = _DAT_00cd;
  _DAT_00a9 = _DAT_16d2;
  _DAT_00ab = _DAT_16d4;
  _DAT_00c8 = _DAT_16e2;
  _DAT_00ca = _DAT_16e4;
  if (((DAT_0054 & 8) == 0) && (0xdf < DAT_1401)) {
    if (((DAT_0046 & 8) == 0) && (DAT_14e8 = DAT_14e8 + '\x01', DAT_14e8 < '\0')) {
      DAT_14e8 = '\0';
      if ((DAT_0046 & 2) == 0) {
        DAT_159a = 0;
        DAT_159b = 0;
        DAT_0046 = DAT_0046 & 0x5f | 10;
        DAT_1472 = '\0';
        DAT_1695 = 0x2a;
        _DAT_1696 = 0x104;
      }
      else {
        DAT_0046 = DAT_0046 & 0xfd | 8;
        _DAT_00a9 = 0;
        _DAT_00ab = 0;
        DAT_00ad = 0;
        _DAT_00c8 = 0;
        _DAT_00ca = 0;
        _DAT_00cc = 0;
      }
    }
    goto LAB_a186;
  }
  DAT_14e8 = '\0';
  DAT_0046 = DAT_0046 & 0xf7;
  if ((bVar2 & 2) == 0) {
    if (((DAT_0040 & 1) == 0) &&
       ((bVar2 = DAT_0054, (DAT_fee0 & 0x20) == 0 ||
        (((uVar3 == 0 && (_DAT_16e4 == 0)) && (DAT_00cc == '\0')))))) {
joined_r0xa065:
      if ((bVar2 & 8) != 0) goto LAB_a186;
    }
  }
  else {
    if ((DAT_0054 & 8) != 0) {
      if (DAT_ea14 == -1) {
LAB_a12a:
        DAT_159b = 0;
        bVar2 = DAT_0051;
        if ((DAT_0051 & 0x20) != 0) goto joined_r0xa065;
      }
      else if (DAT_1401 < 0xe0) {
        if ((bVar2 & 0x80) == 0) goto LAB_a12a;
        if ((DAT_00d5 & 0x1f) != 0) {
          DAT_14e8 = 0;
          return;
        }
        DAT_159b = DAT_159b + 1;
        if (4 < DAT_159b) {
          if (DAT_159b < 0xd) {
            bVar1 = (bool)(DAT_14e9 >> 7);
            DAT_14e9 = DAT_14e9 << 1;
            if (bVar1) goto LAB_a18b;
          }
          else if (0x13 < DAT_159b) {
            DAT_0046 = bVar2 & 0x77;
            DAT_0046 = DAT_0046 ^ 0x20;
            goto LAB_a12a;
          }
        }
      }
      else {
        DAT_159a = DAT_159a + 1;
        if ((short)((ushort)DAT_159a << 8) < 0) {
          DAT_159a = 0;
          DAT_159b = 0;
          DAT_0046 = DAT_0046 | 0x80;
          if ((bVar2 & 0x20) == 0) {
            DAT_14e9 = 0x88;
          }
          else {
            DAT_14e9 = 0xaa;
          }
        }
      }
LAB_a186:
      DAT_0083 = DAT_0083 & 0xbf;
      goto LAB_a18e;
    }
    DAT_159a = 0;
    DAT_159b = 0;
    DAT_0046 = bVar2 & 0x57;
    DAT_1472 = DAT_1472 + 1;
    if (DAT_1472 < 0x1e) {
      DAT_14e8 = 0;
      DAT_159a = 0;
      DAT_159b = 0;
      return;
    }
    while( true ) {
      while( true ) {
        DAT_1472 = '\0';
        DAT_1695 = DAT_1695 + 1;
        if (0x2a < DAT_1695) {
          DAT_1695 = 0;
          FUN_a19e();
        }
        if (DAT_1695 < 6) goto LAB_a186;
        if (DAT_1695 < 0x1a) break;
        if ((DAT_1695 < 0x1b) || ((DAT_1695 & 1) == 0)) goto LAB_a186;
        bVar1 = (bool)(DAT_146e >> 7);
        DAT_146e = DAT_146e << 1;
        if (bVar1) goto LAB_a18b;
        DAT_1695 = 0x2a;
      }
      if ((DAT_1695 & 1) != 0) {
        return;
      }
      if ((DAT_1695 >> 1 & 1) == 0) goto LAB_a186;
      bVar1 = (bool)(DAT_146f >> 7);
      DAT_146f = DAT_146f << 1;
      if (bVar1) break;
      DAT_1695 = 0x19;
    }
  }
LAB_a18b:
  DAT_0083 = DAT_0083 | 0x40;
LAB_a18e:
  uVar3 = CONCAT11(DAT_00d4,DAT_0083) & 0xbf40;
  DAT_00d4 = (char)(uVar3 >> 8) + (char)uVar3;
  DAT_0017 = DAT_00d4;
  return;
}


// ---- FUN_a19e @ a19e ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a19e(void)

{
  bool bVar1;
  ushort uVar2;
  byte bVar3;
  char cVar4;
  undefined1 *puVar5;
  
  if (((_DAT_00a9 == 0) && (_DAT_00ab == 0)) && (DAT_00ad == '\0')) {
    _DAT_1696 = 0x104;
    _DAT_146e = 0xf8f8;
  }
  else {
    do {
      uVar2 = _DAT_1696 & 0x100;
      cVar4 = (char)_DAT_1696;
      _DAT_1696 = CONCAT11((byte)(_DAT_1696 >> 9),cVar4);
      if ((uVar2 != 0) &&
         (cVar4 = cVar4 + '\x01', _DAT_1696 = CONCAT11(0x80,cVar4), cVar4 == '\x05')) {
        _DAT_1696 = 0x8000;
      }
      bVar3 = (byte)(_DAT_1696 >> 8);
    } while ((bVar3 & *(byte *)((_DAT_1696 & 0xff) + 0xa9)) == 0);
    puVar5 = &DAT_a1e3;
    while (bVar1 = (bool)(bVar3 >> 7), bVar3 = bVar3 << 1, !bVar1) {
      puVar5 = puVar5 + 1;
    }
    _DAT_146e = CONCAT11(*puVar5,(&DAT_a1e3)[_DAT_1696 & 0xff]);
  }
  return;
}


// ---- FUN_a1eb @ a1eb ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_a1eb(void)

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
  if (((DAT_00d5 & 0xf) == 0) && (DAT_1566 = DAT_1566 + 1, DAT_1566 == 0)) {
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
    goto LAB_a267;
    if ((DAT_00ae & 0x80) == 0) {
      if (((DAT_140c < DAT_f7e9) || (DAT_f7ea <= DAT_140c)) ||
         ((DAT_1407 < DAT_f6cb || (DAT_f7eb <= DAT_1407)))) goto LAB_a2bd;
      if ((DAT_149f < 0x80) || ((byte)(DAT_149f + 0x80) < DAT_f6d1)) {
LAB_a2a5:
        if ((DAT_f6cc <= DAT_14d9) || (DAT_14a2 < DAT_f6cd)) goto LAB_a2bd;
      }
      else {
        bVar8 = DAT_149e - (DAT_14a0 >> 1);
        if (DAT_149e < DAT_14a0 >> 1) {
          bVar8 = 0;
        }
        if (DAT_f6d2 <= bVar8) goto LAB_a2a5;
      }
      if ((DAT_0053 & 0x80) == 0) {
        DAT_00ae = DAT_00ae | 0x80;
      }
      goto LAB_a2bd;
    }
    DAT_1531 = DAT_1531 + 1;
    if (DAT_1531 <= DAT_f7e5) goto LAB_a2bd;
    if (DAT_f7e6 < DAT_1531) goto LAB_a267;
  }
  else {
    DAT_143d = 0;
LAB_a267:
    DAT_1531 = 0;
    DAT_00ae = DAT_00ae & 0x3f;
LAB_a2bd:
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
        if ((DAT_00ae & 0x10) == 0) goto LAB_a364;
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
LAB_a364:
  bVar3 = DAT_0088;
  DAT_15b4 = (DAT_1530 - DAT_143b) + -0x80;
  if ((DAT_007f & 8) == 0) {
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
        _DAT_16d9 = 0;
        _DAT_16db = 0;
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
    FUN_a524();
    if ((DAT_0088 & 0x20) == 0) {
      _DAT_1461 = _DAT_16d9;
      if (DAT_f7be < DAT_1460) {
        _DAT_1461 = _DAT_16db;
      }
      DAT_0088 = DAT_0088 | 0x20;
      DAT_1566 = 0;
    }
    if ((char)DAT_1566 < '\0') {
      if (0x89 < DAT_1566) goto LAB_a3a6;
    }
    else if (DAT_f7bd <= DAT_1566) {
LAB_a3a6:
      DAT_1566 = 0x80;
      psVar9 = (short *)&DAT_16d9;
      if (DAT_f7be <= DAT_1460) {
        psVar9 = (short *)&DAT_16db;
      }
      uVar5 = *psVar9 + _DAT_1461;
      *psVar9 = CONCAT11((char)((short)uVar5 >> 9),
                         (char)uVar5 >> 1 | (char)((uVar5 & 0x101) >> 8) << 7);
    }
  }
  uVar1 = _DAT_14eb;
  cVar6 = DAT_0080;
  DAT_0080 = 0;
  if ((DAT_1460 < 100) && ((DAT_007f & 0x20) == 0)) {
    _DAT_1461 = (ushort)DAT_ffc5 << 8;
    DAT_00ab = DAT_00ab | 0x10;
    DAT_004a = DAT_004a | 0x10;
    DAT_007f = DAT_007f & 0x7e;
    DAT_16bb = 0;
  }
  else {
    for (; cVar6 != '\0'; cVar6 = cVar6 + -1) {
      _DAT_1461 = _DAT_1461 - _DAT_ffb8;
    }
  }
  if ((DAT_00d5 & 0xf) == 0) {
    _DAT_1461 = _DAT_1461 + 0x1a;
  }
  cVar6 = (char)((ushort)_DAT_14eb >> 8);
  FUN_a473(cVar6,(char)_DAT_14eb,(ushort)DAT_145f << 8);
  uVar2 = _DAT_14ed;
  _DAT_14eb = uVar1;
  if ((DAT_007f & 0x40) == 0) {
    FUN_a473(DAT_14ed,(char)_DAT_14ed,(ushort)DAT_145e << 8);
    _DAT_14ed = uVar2;
    FUN_a495();
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
    if (bVar3 < bVar8) goto LAB_a512;
  }
  uVar5 = uVar5 << 8;
LAB_a512:
  DAT_140f = (byte)(uVar5 >> 8);
  if (0x77 < DAT_140f) {
    DAT_140f = 0x77;
  }
  DAT_14ea = DAT_1461 + -0x80;
  return;
}


// ---- FUN_a473 @ a473 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a473(ushort param_1)

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


// ---- FUN_a495 @ a495 ----

/* WARNING: Removing unreachable block (RAM,0xa516) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a495(void)

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


// ---- FUN_a524 @ a524 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a524(void)

{
  char cVar1;
  char extraout_B;
  char extraout_B_00;
  short sVar2;
  
  _DAT_005b = _DAT_16d9;
  if (_DAT_16d9 < 0) {
    _DAT_005b = CONCAT11(-((char)((ushort)_DAT_16d9 >> 8) + ((char)-(char)_DAT_16d9 != '\0')),
                         -(char)_DAT_16d9);
  }
  cVar1 = FUN_82d5();
  _DAT_0060 = CONCAT11(cVar1,extraout_B);
  if (_DAT_16d9 < 0) {
    _DAT_0060 = CONCAT11(-(cVar1 + (-extraout_B != '\0')),-extraout_B);
  }
  _DAT_005b = _DAT_16db;
  if (_DAT_16db < 0) {
    _DAT_005b = CONCAT11(-((char)((ushort)_DAT_16db >> 8) + ((char)-(char)_DAT_16db != '\0')),
                         -(char)_DAT_16db);
  }
  cVar1 = FUN_82d5();
  sVar2 = CONCAT11(cVar1,extraout_B_00);
  if (_DAT_16db < 0) {
    sVar2 = CONCAT11(-(cVar1 + (-extraout_B_00 != '\0')),-extraout_B_00);
  }
  _DAT_14c5 = sVar2 + _DAT_0060;
  return;
}


// ---- FUN_a560 @ a560 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a560(void)

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
      } while (puVar1 != (undefined2 *)&DAT_1640);
      if ((DAT_0040 & 4) == 0) {
        puVar1 = (undefined2 *)&DAT_1640;
        do {
          *puVar1 = 0;
          puVar1 = puVar1 + 1;
        } while (puVar1 != (undefined2 *)&DAT_16a0);
        DAT_1695 = 0x3b;
        _DAT_1696 = 0x104;
      }
      if ((DAT_0040 & 1) == 0) {
        _DAT_013e = 0xb0b2;
        FUN_b0d5();
        _DAT_013e = 0xb0b5;
        FUN_b10e();
        _DAT_013e = 0xb0b8;
        FUN_b291();
        _DAT_013e = 0xb0bc;
        FUN_b40e();
        _DAT_013e = 0xb0bf;
        FUN_b4fe();
        _DAT_013e = 0xb0c2;
        FUN_b3f6();
        _DAT_013e = 0xb0c5;
        FUN_8e2b();
        FUN_b3a0();
        return;
      }
      _DAT_013e = 0xb0cb;
      FUN_b394();
      _DAT_013e = 0xb0ce;
      FUN_b10e();
      _DAT_013e = 0xb0d1;
      FUN_b291();
      FUN_b3a0();
      return;
    }
  }
  return;
}


// ---- FUN_a597 @ a597 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a597(void)

{
  bool bVar1;
  byte bVar2;
  
  if ((DAT_0040 & 8) != 0) {
    bVar2 = DAT_f6a9;
    if ((DAT_0040 & 2) != 0) {
      return;
    }
    goto LAB_a6d1;
  }
  if ((DAT_0054 & 8) == 0) {
    return;
  }
  DAT_00bf = DAT_00bf & 0xdf;
  if ((DAT_00d9 & 0x10) != 0) {
    bVar2 = 0;
    goto LAB_a6d1;
  }
  bVar2 = DAT_166b;
  if ((DAT_00d8 & 0x10) != 0) goto LAB_a6d1;
  if ((DAT_007e & 1) == 0) {
    FUN_a6dc();
    if ((DAT_0053 & 2) != 0) {
      _DAT_146a = DAT_ffa3;
      goto LAB_a694;
    }
    if ((DAT_140c < 0xa0) || (9 < DAT_1477)) {
      FUN_a7e6();
      if ((DAT_0053 & 1) == 0) {
        FUN_a820();
LAB_a5fa:
        DAT_14be = 0;
      }
      else {
        FUN_a856();
        if (((DAT_0053 & 4) == 0) && (3 < DAT_1407)) goto LAB_a5fa;
        if (_DAT_146a < DAT_ffa3) {
          _DAT_146a = _DAT_146a + 1;
          if (DAT_143f <= DAT_1442) goto LAB_a5fa;
          _DAT_146a = DAT_ffa3;
          bVar1 = CARRY1(DAT_1445,DAT_1446);
          DAT_1445 = DAT_1445 + DAT_1446;
          if (bVar1) {
            DAT_1445 = 0xff;
          }
          DAT_1446 = 0;
        }
        DAT_00bf = DAT_00bf | 0x20;
        if (DAT_143f < DAT_1442) {
          if (2 < (byte)(DAT_1442 - DAT_143f)) {
            FUN_a8cb();
            if ((DAT_1449 == '\0') &&
               (DAT_1445 = DAT_1445 - 1, DAT_1449 = DAT_ffad, 3 < (byte)(DAT_1442 - DAT_143f))) {
              DAT_1449 = DAT_ffba;
            }
            DAT_1449 = DAT_1449 + -1;
            if (DAT_1445 == 0) {
              DAT_1445 = 1;
            }
            goto LAB_a694;
          }
        }
        else if (2 < (byte)-(DAT_1442 - DAT_143f)) {
          FUN_a888();
          goto LAB_a65c;
        }
      }
      DAT_1448 = 0;
      goto LAB_a694;
    }
LAB_a69b:
    DAT_1445 = 0xb4;
  }
  else {
LAB_a65c:
    if (DAT_1449 == '\0') {
      FUN_a8ad();
    }
    DAT_1449 = DAT_1449 + -1;
LAB_a694:
    if (0xb3 < DAT_1445) goto LAB_a69b;
    if (DAT_1445 < 0x28) {
      DAT_1445 = 0x28;
    }
  }
  FUN_a8f5();
  FUN_a915();
  if (((CARRY1(DAT_153b,DAT_1448)) ||
      (bVar2 = DAT_153b + DAT_1448 + DAT_1446, CARRY1(DAT_153b + DAT_1448,DAT_1446))) ||
     (0xb3 < bVar2)) {
    bVar2 = 0xb4;
  }
  else if (bVar2 < 0x28) {
    bVar2 = 0x28;
  }
  if ((DAT_00d8 & 0x10) != 0) {
    bVar2 = DAT_166b;
  }
LAB_a6d1:
  DAT_14cd = bVar2;
  _DAT_105a = (ushort)bVar2 << 2;
  return;
}


// ---- FUN_a6dc @ a6dc ----

/* WARNING: Removing unreachable block (RAM,0xa7cb) */
/* WARNING: Type propagation algorithm not settling */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a6dc(void)

{
  byte bVar1;
  short sVar2;
  
  if (_DAT_140a == 0) {
LAB_a706:
    DAT_1440 = 0;
  }
  else {
    sVar2 = _DAT_1440 + 1;
    DAT_1440 = (byte)((ushort)sVar2 >> 8);
    if ((short)((ushort)DAT_1440 << 8) < 0) {
      if (DAT_1440 < 0xf6) {
        DAT_0053 = DAT_0053 | 0x20;
        _DAT_1440 = sVar2;
        goto LAB_a70c;
      }
      goto LAB_a706;
    }
    if (((DAT_0053 & 2) != 0) || (0x96 < DAT_008f)) goto LAB_a706;
    DAT_1440 = DAT_1440 + 1;
  }
  _DAT_1440 = (ushort)DAT_1440 << 8;
LAB_a70c:
  FUN_809f();
  bVar1 = DAT_1401 & 0xe0;
  if (bVar1 < DAT_1551) {
    bVar1 = DAT_1401 + 10 & 0xe0;
  }
  DAT_1551 = bVar1;
  DAT_154e = 0;
  if ((((DAT_143f == '\0') || (DAT_f686 == 0)) || (DAT_143f == '\0')) ||
     (DAT_154f = DAT_154f + 1, DAT_f686 <= DAT_154f)) {
    DAT_154f = 0;
  }
  DAT_143f = 0;
  if (((DAT_00d8 & 8) != 0) && (DAT_143f = DAT_166a, 0x8f < DAT_166a)) {
    DAT_143f = 0x90;
  }
  return;
}


// ---- FUN_a7e6 @ a7e6 ----

void FUN_a7e6(void)

{
  byte bVar1;
  
  bVar1 = DAT_1442;
  if (((DAT_00b5 & 2) == 0) && (bVar1 = DAT_1442 - 0x10, DAT_1442 < 0x10)) {
    bVar1 = 0;
  }
  if (DAT_ff2d < bVar1) {
    DAT_00b5 = DAT_00b5 | 2;
    DAT_1443 = 0;
  }
  else {
    DAT_00b5 = DAT_00b5 & 0xfd;
    if ((DAT_0053 & 0x44) == 0) {
      DAT_1443 = DAT_ff9e;
      if ((DAT_0053 & 0x10) != 0) {
        DAT_1443 = DAT_f9fb;
      }
    }
    else {
      DAT_1443 = 0;
      if ((DAT_0053 & 0x10) != 0) {
        DAT_1443 = DAT_ff9f;
      }
    }
  }
  return;
}


// ---- FUN_a820 @ a820 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_a820(void)

{
  byte bVar1;
  ushort uVar2;
  bool bVar3;
  
  bVar1 = FUN_809f();
  if (DAT_158b < DAT_f684) {
    uVar2 = 0;
    bVar3 = false;
  }
  else {
    uVar2 = (ushort)DAT_f685 * (ushort)(byte)(DAT_158b - DAT_f684);
    bVar3 = false;
    if ((char)(uVar2 >> 8) != '\0') {
      uVar2 = 0xff;
      bVar3 = true;
    }
  }
  DAT_1552 = (char)uVar2;
  if (!bVar3) {
    bVar1 = (byte)((ushort)bVar1 * (uVar2 & 0xff) >> 8);
  }
  if (DAT_1446 <= bVar1) {
    DAT_1446 = bVar1;
  }
  _DAT_146a = 0;
  return;
}


// ---- FUN_a856 @ a856 ----

void FUN_a856(void)

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
    else {
      DAT_1447 = DAT_1447 + -1;
    }
  }
  return;
}


// ---- FUN_a888 @ a888 ----

void FUN_a888(void)

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


// ---- FUN_a8ad @ a8ad ----

void FUN_a8ad(void)

{
  DAT_1445 = DAT_1445 + '\x01';
  if (DAT_1445 == '\0') {
    DAT_1445 = -1;
  }
  DAT_1449 = DAT_ffad;
  if (3 < (byte)(DAT_143f - DAT_1442)) {
    DAT_1449 = DAT_ffba;
  }
  return;
}


// ---- FUN_a8cb @ a8cb ----

void FUN_a8cb(void)

{
  bool bVar1;
  
  DAT_1448 = 0;
  if ((DAT_00b5 & 4) == 0) {
    DAT_00b5 = DAT_00b5 | 4;
  }
  else if (((DAT_1471 < '\0') && (DAT_ffa6 <= (byte)-DAT_1471)) &&
          (bVar1 = CARRY1(DAT_14be >> 1,DAT_1445), DAT_1445 = (DAT_14be >> 1) + DAT_1445, bVar1)) {
    DAT_1445 = 0xff;
  }
  DAT_14be = 0;
  return;
}


// ---- FUN_a8f5 @ a8f5 ----

void FUN_a8f5(void)

{
  if (((DAT_0053 & 1) == 0) && (DAT_1445 < DAT_ffbf)) {
    if (DAT_1444 == '\0') {
      DAT_1444 = '}';
      DAT_1445 = DAT_1445 + 1;
    }
    else {
      DAT_1444 = DAT_1444 + -1;
    }
  }
  return;
}


// ---- FUN_a915 @ a915 ----

void FUN_a915(void)

{
  char cVar1;
  
  DAT_153b = DAT_1445 + DAT_1443;
  if (CARRY1(DAT_1445,DAT_1443)) {
    DAT_153b = 0xff;
  }
  if (((((DAT_0053 & 1) == 0) || ((DAT_0015 & 0x20) == 0)) || (DAT_1407 < DAT_f7f3)) ||
     ((DAT_00d2 & 0x10) != 0)) {
LAB_a95d:
    DAT_00bf = DAT_00bf & 0xaf;
    DAT_153d = 0;
    DAT_153c = 0;
    return;
  }
  cVar1 = DAT_153c;
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
    if (DAT_1442 < (byte)(DAT_143f + DAT_f7f7)) goto LAB_a95d;
    DAT_00bf = DAT_00bf & 0xbf | 0x10;
LAB_a96d:
    if ((DAT_153c == '\0') && (DAT_153d = DAT_153d + 1, cVar1 = DAT_f7f8, DAT_f6aa < DAT_153d)) {
      DAT_153d = DAT_f6aa;
      goto LAB_a98b;
    }
  }
  else {
    if ((DAT_00bf & 0x40) == 0) {
      if (((DAT_f7f9 <= DAT_1407) && ((byte)(DAT_143f + DAT_f7fa) <= DAT_1442)) &&
         ((DAT_00bf & 0x20) == 0)) goto LAB_a96d;
      DAT_00bf = DAT_00bf | 0x40;
    }
    if (DAT_153d == 0) {
      return;
    }
    if ((DAT_153c == '\0') && (DAT_153d = DAT_153d - 1, cVar1 = DAT_f7fb, DAT_153d == 0)) {
      DAT_00bf = DAT_00bf & 0xef;
      return;
    }
  }
  DAT_153c = cVar1;
  DAT_153c = DAT_153c + -1;
LAB_a98b:
  cVar1 = DAT_153b - DAT_153d;
  if (DAT_153b < DAT_153d) {
    cVar1 = '\0';
    DAT_153d = DAT_153b;
  }
  DAT_153b = cVar1;
  return;
}


// ---- FUN_a9d4 @ a9d4 ----

void FUN_a9d4(void)

{
  byte bVar1;
  byte bVar2;
  
  if (((DAT_0053 & 0x40) == 0) && ((DAT_0040 & 4) == 0)) {
    if ((DAT_0053 & 2) == 0) {
      if ((DAT_00d1 & 0x80) == 0) {
        if (DAT_1460 < 0x20) goto LAB_a9e1;
        DAT_00d1 = DAT_00d1 | 0x80;
      }
      if ((DAT_00d1 & 8) == 0) {
        if ((DAT_0040 & 8) == 0) {
          bVar1 = DAT_f67d;
          if (((DAT_00d1 & 0x40) != 0) && (bVar1 = DAT_f67d + 2, 0xfd < DAT_f67d)) {
            bVar1 = 0xff;
          }
          bVar2 = DAT_00d1 & 0xbf;
          if (DAT_140c < bVar1) {
            bVar2 = bVar2 | 0x40;
          }
          bVar1 = DAT_f67e;
          if (((bVar2 & 0x20) != 0) && (bVar1 = DAT_f67e + 10, 0xf5 < DAT_f67e)) {
            bVar1 = 0xff;
          }
          bVar2 = bVar2 & 0xdf;
          if (DAT_14a2 < bVar1) {
            bVar2 = bVar2 | 0x20;
          }
          bVar1 = DAT_f67f;
          if (((bVar2 & 0x10) != 0) && (bVar1 = DAT_f67f + 6, 0xf9 < DAT_f67f)) {
            bVar1 = 0xff;
          }
          DAT_00d1 = bVar2 & 0xef;
          if (DAT_1460 < bVar1) {
            DAT_00d1 = DAT_00d1 | 0x10;
          }
          if ((((DAT_00d1 & 0x70) != 0) || ((DAT_0059 & 8) == 0)) || ((DAT_00b6 & 0x60) != 0))
          goto LAB_aa65;
          DAT_00b4 = DAT_00b4 & 0xfd;
        }
        else {
LAB_aa65:
          DAT_00b4 = DAT_00b4 | 2;
        }
        bVar1 = DAT_2000 & 3;
        if (bVar1 == (DAT_00d2 & 3)) {
          DAT_00d2 = DAT_00d2 & 0xf3;
          DAT_00d2 = bVar1 << 2 | DAT_00d2;
        }
        else {
          DAT_00d2 = DAT_00d2 & 0xfc;
          DAT_00d2 = bVar1 | DAT_00d2;
        }
        if ((DAT_00d2 & 8) == 0) {
          if (((DAT_00d5 & 0xf) != 0) || (DAT_00c3 = DAT_00c3 + -1, DAT_00c3 != '\0'))
          goto LAB_aabb;
LAB_aaa0:
          DAT_00d1 = DAT_00d1 | 8;
          DAT_00ad = DAT_00ad | 0x10;
          DAT_004c = DAT_004c | 0x10;
          goto LAB_aaac;
        }
        DAT_00c3 = DAT_f67c;
        if ((DAT_00d2 & 4) == 0) {
          if ((DAT_00d5 == 0) && (DAT_158c = DAT_158c + -1, DAT_158c == '\0')) goto LAB_aaa0;
        }
        else {
LAB_aabb:
          DAT_158c = DAT_f691;
        }
        if ((DAT_00d2 & 8) == 0) {
          if (((DAT_00d2 & 4) != 0) || ((DAT_00b4 & 2) != 0)) goto LAB_aad6;
          DAT_1545 = 3;
LAB_aae9:
          if ((DAT_00d5 & 0xf) == 0) {
            if (DAT_158d == '\0') goto LAB_aafb;
            DAT_158d = DAT_158d + -1;
          }
          if (DAT_158d != '\0') goto LAB_aad2;
          goto LAB_aafb;
        }
        if ((DAT_00d2 & 4) != 0) {
LAB_aad6:
          DAT_1545 = 0;
          goto LAB_aae9;
        }
      }
      else {
LAB_aaac:
        DAT_00b4 = DAT_00b4 | 2;
      }
      DAT_158d = DAT_f692;
      DAT_1545 = 0;
LAB_aad2:
      DAT_00d2 = DAT_00d2 | 0x10;
      return;
    }
  }
  else {
    DAT_00d1 = DAT_00d1 & 0xf7;
  }
LAB_a9e1:
  DAT_00b4 = DAT_00b4 | 2;
  DAT_1545 = 0;
  DAT_158c = DAT_f691;
LAB_aafb:
  DAT_00d2 = DAT_00d2 & 0xef;
  return;
}


// ---- FUN_aaff @ aaff ----

/* WARNING: Removing unreachable block (RAM,0xad17) */
/* WARNING: Removing unreachable block (RAM,0xad1f) */
/* WARNING: Removing unreachable block (RAM,0xad20) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: RAM */

void FUN_aaff(void)

{
  ushort uVar1;
  byte bVar2;
  ushort uVar3;
  byte bVar4;
  
  if ((DAT_0041 & 1) == 0) {
    if ((DAT_0041 & 0x80) == 0) {
      DAT_1643 = 0;
    }
    else {
      DAT_1643 = DAT_1643 + 1;
      if (0x80 < DAT_1643) {
        DAT_0042 = DAT_0042 | 2;
        FUN_b038();
      }
    }
  }
  else if ((DAT_0041 & 0x80) == 0) {
    DAT_1643 = 0;
  }
  else {
    DAT_1643 = DAT_1643 + 1;
    if (0x80 < DAT_1643) {
      DAT_0041 = DAT_0041 & 0x7f;
    }
  }
  if (((DAT_0041 & 0x20) == 0) || ((DAT_0042 & 0x10) != 0)) {
    return;
  }
  _DAT_00a9 = CONCAT11((byte)((ushort)_DAT_00a9 >> 8) & DAT_ff15,(byte)_DAT_00a9 & DAT_ff16);
  _DAT_0048 = CONCAT11((byte)((ushort)_DAT_0048 >> 8) & DAT_ff15,(byte)_DAT_0048 & DAT_ff16);
  _DAT_00ab = CONCAT11((byte)((ushort)_DAT_00ab >> 8) & DAT_ff17,(byte)_DAT_00ab & DAT_ff18);
  _DAT_004a = CONCAT11((byte)((ushort)_DAT_004a >> 8) & DAT_ff17,(byte)_DAT_004a & DAT_ff18);
  DAT_00ad = DAT_00ad & DAT_ff19;
  DAT_004c = DAT_004c & DAT_ff19;
  DAT_1693 = DAT_ead0;
  DAT_1694 = DAT_eacf;
  if (DAT_1646 == -0x30) {
    uVar3 = 0;
    do {
      (&DAT_1651)[uVar3] = (&DAT_eac0)[uVar3];
      bVar4 = (char)uVar3 + 1;
      uVar3 = (ushort)bVar4;
    } while (bVar4 < 0x16);
  }
  else {
    if (DAT_1646 == -0x3f) {
      if ((DAT_0043 & 4) == 0) {
        _DAT_00a9 = 0;
        _DAT_00ab = 0;
        DAT_00ad = 0;
        _DAT_00c8 = 0;
        _DAT_00ca = 0;
        _DAT_00cc = 0;
        DAT_0043 = DAT_0043 | 4;
      }
    }
    else if (DAT_1646 != -0x2f) {
      bVar4 = 0;
      if ((DAT_0042 & 0x40) == 0) {
        if (((DAT_0042 & 8) != 0) && (bVar4 = 0, DAT_1647 != 0)) {
          _DAT_164d = _DAT_1465;
          FUN_ad42();
          uVar3 = 0;
          do {
            (&DAT_1651)[uVar3] = **(undefined1 **)(&DAT_ea00 + *(byte *)(uVar3 + 0x167f));
            bVar4 = (char)uVar3 + 1;
            uVar3 = (ushort)bVar4;
          } while (bVar4 < DAT_1647);
        }
      }
      else {
        bVar4 = 0;
        bVar2 = 0;
        if (DAT_1647 != 0) {
          do {
            (&DAT_1651)[bVar2] = **(undefined1 **)(bVar2 + 0x167f + (ushort)bVar2);
            bVar4 = bVar2 + 1;
            bVar2 = bVar4;
          } while ((byte)(bVar4 * '\x02') < DAT_1647);
        }
      }
      if (DAT_1646 == 'Q') {
        if (((_DAT_0048 != 0) || (_DAT_004a != 0)) || (DAT_004c != 0)) {
          DAT_1642 = 0;
          DAT_1641 = 0x80;
          bVar2 = 0;
          do {
            if ((DAT_1641 & DAT_0048) != 0) {
                    /* WARNING: Ignoring partial resolution of indirect */
              DAT_0048 = ~DAT_1641 & DAT_0048;
              bVar4 = DAT_1647;
              if ((DAT_0042 & 0x40) != 0) {
                bVar4 = DAT_1647 >> 1;
              }
              bVar4 = bVar4 + DAT_1642;
              (&DAT_1651)[bVar4] = *(undefined1 *)(bVar2 + 0xad6b);
              DAT_1642 = DAT_1642 + 1;
              if (1 < DAT_1642) goto code_r0xacfd;
            }
            bVar4 = DAT_1641 & 1;
            DAT_1641 = DAT_1641 >> 1;
            if (bVar4 != 0) {
              DAT_1641 = 0x80;
            }
            bVar2 = 1;
          } while( true );
        }
      }
      else if ((bVar4 == 0) && (DAT_1648 == '\0')) {
        return;
      }
      goto LAB_ad23;
    }
    if (((_DAT_00a9 != 0) || (_DAT_00ab != 0)) || (DAT_00ad != 0)) {
      DAT_1641 = 0x80;
      bVar4 = 0;
      DAT_1642 = 0;
      do {
        if ((DAT_1641 & DAT_00a9) != 0) {
          (&DAT_1651)[(ushort)DAT_1642 + (ushort)DAT_1642] = *(undefined1 *)(bVar4 + 0xad6b);
          uVar3 = (ushort)DAT_1642;
          uVar1 = (ushort)DAT_1642;
          (&DAT_1651 + uVar1 + uVar3)[1] = (&DAT_16a8)[bVar4];
          DAT_1642 = DAT_1642 + 1;
          if ((undefined1 *)0x1664 < &DAT_1651 + uVar1 + uVar3) goto LAB_ac2c;
        }
        bVar4 = DAT_1641 & 1;
        DAT_1641 = DAT_1641 >> 1;
        if (bVar4 != 0) {
          DAT_1641 = 0x80;
        }
        bVar4 = 1;
      } while( true );
    }
    DAT_1651 = 0x55;
    DAT_1652 = 0;
    bVar4 = 2;
  }
LAB_ad23:
  if (((DAT_0041 & 0x20) != 0) && (((TRCS & 0x20) == 0 || ((DAT_0042 & 0x20) == 0)))) {
    TRCS = TRCS | 4;
    DAT_0042 = DAT_0042 | 0x10;
  }
  _DAT_164f = CONCAT11(0xff,bVar4);
  return;
code_r0xacfd:
  bVar4 = bVar4 + 1;
  goto LAB_ad23;
LAB_ac2c:
  bVar4 = DAT_1642 * '\x02';
  goto LAB_ad23;
}


// ---- FUN_ad42 @ ad42 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_ad42(void)

{
  _DAT_1698 = 0;
  if ((DAT_009c & 0x80) != 0) {
    _DAT_1698 = 0x8000;
  }
  if ((DAT_00d4 & 0x10) != 0) {
    _DAT_1698 = _DAT_1698 | 0x4000;
  }
  if ((DAT_00bc & 0x40) != 0) {
    _DAT_1698 = _DAT_1698 | 0x40;
  }
  if ((DAT_009c & 0x40) != 0) {
    _DAT_1698 = _DAT_1698 | 1;
  }
  return;
}


// ---- vec_SCI @ ad8f ----

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
  
  bVar3 = DAT_1645;
  DAT_1595 = TRCS;
  DAT_1640 = RX;
  if (((TRCS & 4) != 0) && ((TRCS & 0x20) != 0)) {
    if ((DAT_0042 & 0x10) == 0) {
      TRCS = TRCS & 0xfb;
      DAT_0042 = DAT_0042 & 0xdf;
      FUN_b038();
      TX = DAT_1644;
    }
    else {
      DAT_1645 = DAT_1645 + 1;
      if (DAT_1650 < bVar3) {
        if ((DAT_0042 & 0x20) == 0) {
          TRCS = TRCS & 0xfb;
        }
        DAT_0042 = DAT_0042 & 0xef;
        DAT_1645 = 0;
      }
      TX = (&DAT_164f)[bVar3];
    }
  }
  if (((DAT_1595 & 0x10) == 0) || ((DAT_1595 & 0xc0) == 0)) {
    return in_stack_00000003;
  }
  if ((DAT_0041 & 1) != 0) {
    if (((DAT_1595 & 0x40) == 0) && (DAT_1640 == 0xff)) {
      if ((DAT_0041 & 0x80) == 0) {
        DAT_0041 = DAT_0041 | 0x80;
        goto LAB_adf8;
      }
      DAT_0041 = DAT_0041 & 0xfe;
      DAT_0041 = DAT_0041 | 2;
    }
    DAT_0041 = DAT_0041 & 0x7f;
    return in_stack_00000003;
  }
  bVar3 = DAT_1640;
  if ((DAT_0041 & 2) != 0) {
    if (((DAT_1595 & 0x40) != 0) || (DAT_1640 != 0xef)) {
LAB_adf8:
      DAT_0041 = DAT_0041 & 0xfd | 1;
      return in_stack_00000003;
    }
    DAT_0041 = DAT_0041 & 0xfd;
    DAT_0041 = DAT_0041 | 4;
LAB_b01e:
    bVar3 = ~bVar3;
    goto LAB_b01f;
  }
  if ((DAT_0041 & 4) == 0) {
    if ((DAT_0041 & 0x10) == 0) {
      if ((DAT_0041 & 0x20) == 0) {
        return in_stack_00000003;
      }
      if ((DAT_1595 & 0x40) == 0) {
        if (DAT_1640 == 0xff) goto LAB_ae37;
        if (DAT_1640 == 0x30) goto LAB_ae4f;
      }
    }
    else if ((DAT_1595 & 0x40) == 0) {
      if (DAT_1640 == 0xff) {
LAB_ae37:
        if ((DAT_0041 & 0x80) != 0) {
          DAT_0042 = DAT_0042 | 1;
          FUN_b038();
          bVar3 = extraout_B;
          goto LAB_b01b;
        }
        DAT_0041 = DAT_0041 | 0x80;
        goto LAB_b01e;
      }
      if (DAT_1640 == 0x30) {
LAB_ae4f:
        DAT_0042 = DAT_0042 | 2;
        FUN_b038();
        bVar3 = extraout_B_00;
        goto LAB_b01b;
      }
      if (DAT_1640 == 0xf0) {
        DAT_0041 = DAT_0041 & 0x6f;
        DAT_0041 = DAT_0041 | 0x20;
        _DAT_00d8 = _DAT_164a;
        DAT_00da = DAT_164c;
        return in_stack_00000003;
      }
      if (DAT_1640 == 10) {
        if (DAT_1648 < 5) {
          DAT_0042 = DAT_0042 & 0xb7;
          bVar3 = 10;
          goto LAB_afef;
        }
      }
      else {
        if (DAT_1646 == 0) {
          if (DAT_1640 == 0x51) {
LAB_ae9a:
            DAT_0048 = 0;
            DAT_0049 = 0;
            DAT_004a = 0;
            DAT_004b = 0;
            DAT_004c = 0;
LAB_aea9:
            DAT_0041 = DAT_0041 & 0xfb;
            DAT_0041 = DAT_0041 | 0x10;
            DAT_1646 = DAT_1640;
            goto LAB_b01b;
          }
        }
        else if (DAT_1646 != 0x51) goto LAB_aff8;
        if (DAT_1647 < 0x14) {
          if (DAT_1640 == 0xc9) {
            if ((DAT_0042 & 8) == 0) {
              DAT_0042 = DAT_0042 | 0x40;
LAB_afef:
              DAT_0041 = DAT_0041 & 0xef;
              DAT_0041 = DAT_0041 | 0xc;
              goto LAB_b01b;
            }
          }
          else if ((DAT_1640 == 0x5a) && ((DAT_0042 & 0x40) == 0)) {
            DAT_0042 = DAT_0042 | 8;
            goto LAB_afef;
          }
        }
      }
    }
LAB_aff8:
    DAT_0042 = DAT_0042 | 2;
    FUN_b038();
    bVar3 = 0xfe;
    goto LAB_b01f;
  }
  if ((DAT_1595 & 0x40) != 0) goto LAB_ae8f;
  if ((DAT_0041 & 8) == 0) {
    if (DAT_1640 == 0xff) goto LAB_ae37;
    if (DAT_1640 == 0x30) goto LAB_ae4f;
    if (DAT_1640 == 0xc9) {
      DAT_0042 = DAT_0042 | 0x40;
      DAT_0041 = DAT_0041 | 8;
    }
    else if (DAT_1640 == 0x5a) {
      DAT_0042 = DAT_0042 | 8;
      DAT_0041 = DAT_0041 | 8;
    }
    else {
      if (DAT_1640 != 10) {
        if (DAT_1640 == 0x51) goto LAB_ae9a;
        if (((DAT_1640 == 0xd1) || (DAT_1640 == 0xc1)) || (DAT_1640 == 0xd0)) goto LAB_aea9;
        goto LAB_ae8f;
      }
      DAT_0041 = DAT_0041 | 8;
      DAT_0042 = DAT_0042 & 0xb7;
    }
LAB_b01b:
    DAT_0041 = DAT_0041 & 0x7f;
    goto LAB_b01e;
  }
  if ((DAT_0042 & 0x40) == 0) {
    if ((DAT_0042 & 8) == 0) {
      if ((DAT_0042 & 0x80) != 0) {
        (&DAT_1667)[DAT_1649] = DAT_1640;
        DAT_0042 = DAT_0042 & 0x7f;
LAB_af70:
        DAT_1648 = DAT_1648 + 1;
        goto LAB_af73;
      }
      if ((0x7f < DAT_1640) && ((byte)(DAT_1640 + 0x80) < 0x18)) {
        uVar2 = *(ushort *)(&DAT_ea50 + (byte)(DAT_1640 << 1));
        bVar3 = (byte)(uVar2 >> 8);
        if (bVar3 != 0xff) {
          bVar4 = (byte)uVar2;
          if ((char)bVar4 < '\0') {
            DAT_164c = bVar3 | DAT_164c;
            bVar4 = bVar4 & 0x3f;
          }
          else if ((uVar2 & 0x40) == 0) {
            _DAT_164a = CONCAT11(bVar3 | DAT_164a,DAT_164b);
          }
          else {
            _DAT_164a = CONCAT11(DAT_164a,bVar3 | DAT_164b);
            bVar4 = bVar4 & 0x3f;
          }
          if ((bVar4 & 1) != 0) {
            DAT_0042 = DAT_0042 | 0x80;
            bVar3 = DAT_1640;
            DAT_1649 = bVar4 >> 1;
            goto LAB_b01f;
          }
          goto LAB_af70;
        }
      }
    }
    else if ((DAT_1640 < 0x28) && ((&DAT_ea00)[(byte)(DAT_1640 << 1)] != -1)) {
      *(byte *)(DAT_1647 + 0x167f) = DAT_1640 << 1;
      DAT_1647 = DAT_1647 + 1;
      goto LAB_af73;
    }
    goto LAB_ae8f;
  }
  uVar2 = (ushort)DAT_1647;
  *(byte *)(uVar2 + 0x167f) = DAT_1640;
  DAT_1647 = DAT_1647 + 1;
  if ((DAT_0043 & 1) == 0) {
    DAT_0043 = DAT_0043 | 1;
    bVar3 = DAT_1640;
    goto LAB_b01f;
  }
  DAT_0043 = DAT_0043 & 0xfe;
  puVar1 = *(undefined1 **)(uVar2 + 0x167e);
  if (puVar1 < &DAT_1400) {
    if ((puVar1 < (undefined1 *)0x40) || ((undefined1 *)0x13f < puVar1)) goto LAB_ae8f;
  }
  else if (((undefined1 *)0x17ff < puVar1) && (puVar1 < (undefined1 *)0x8000)) {
LAB_ae8f:
    DAT_0042 = DAT_0042 | 2;
    FUN_b038();
    bVar3 = 0xfe;
    goto LAB_b01f;
  }
LAB_af73:
  DAT_0041 = DAT_0041 & 0xf3;
  DAT_0041 = DAT_0041 | 0x10;
  bVar3 = DAT_1640;
LAB_b01f:
  if (((DAT_0042 & 0x10) == 0) && ((TRCS & 0x20) != 0)) {
    FUN_b038();
    TX = extraout_B_01;
    return in_stack_00000003;
  }
  TRCS = TRCS | 4;
  DAT_0042 = DAT_0042 | 0x20;
  DAT_1644 = bVar3;
  return in_stack_00000003;
}


// ---- FUN_b038 @ b038 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b038(void)

{
  if ((DAT_0042 & 3) != 0) {
    DAT_0041 = DAT_0041 & 0x41;
    DAT_0043 = DAT_0043 & 0xf9;
    if ((DAT_0042 & 1) == 0) {
      DAT_0041 = DAT_0041 | 4;
    }
    else {
      DAT_0041 = DAT_0041 | 2;
    }
    DAT_1646 = 0;
    _DAT_1647 = 0;
    _DAT_164a = 0;
    DAT_164c = 0;
    _DAT_00d8 = 0;
    DAT_00da = 0;
    DAT_0042 = DAT_0042 & 0x34;
    TRCS = TRCS & 0xfb;
  }
  return;
}


// ---- vec_RESET @ b06f ----

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
  if ((DAT_0040 & 4) == 0) {
    puVar1 = (undefined2 *)&DAT_1640;
    do {
      *puVar1 = 0;
      puVar1 = puVar1 + 1;
    } while (puVar1 != (undefined2 *)&DAT_16a0);
    DAT_1695 = 0x3b;
    _DAT_1696 = 0x104;
  }
  if ((DAT_0040 & 1) == 0) {
    _DAT_013e = 0xb0b2;
    FUN_b0d5();
    _DAT_013e = 0xb0b5;
    FUN_b10e();
    _DAT_013e = 0xb0b8;
    FUN_b291();
    _DAT_013e = 0xb0bc;
    FUN_b40e();
    _DAT_013e = 0xb0bf;
    FUN_b4fe();
    _DAT_013e = 0xb0c2;
    FUN_b3f6();
    _DAT_013e = 0xb0c5;
    FUN_8e2b();
    FUN_b3a0();
    return;
  }
  _DAT_013e = 0xb0cb;
  FUN_b394();
  _DAT_013e = 0xb0ce;
  FUN_b10e();
  _DAT_013e = 0xb0d1;
  FUN_b291();
  FUN_b3a0();
  return;
}


// ---- FUN_b0d5 @ b0d5 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b0d5(void)

{
  byte bVar1;
  byte bVar2;
  
  bVar2 = DAT_00d4;
  bVar1 = DAT_00bc;
  DAT_00bc = DAT_00bc | 0x80;
  DAT_00d4 = DAT_00d4 | 0x80;
  if ((DAT_0040 & 4) == 0) {
    DAT_00d4 = bVar2 | 0x90;
    DAT_00bc = bVar1 | 0xa0;
  }
  P2DATA = DAT_00d3;
  DAT_0017 = DAT_00d4;
  P2DDR = 0x70;
  DAT_0016 = 0xf1;
  TCSR = 0x16;
  P3SCR = 0;
  RAMCR = 0xe7;
  _DAT_001b = &DAT_1407;
  RMCR = 0xc;
  TRCS = 0x3a;
  return;
}


// ---- FUN_b10e @ b10e ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b10e(void)

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
  DAT_00d5 = 0x99;
  DAT_00d6 = 0;
  DAT_14c8 = 0;
  DAT_1582 = 5;
  DAT_1431 = 100;
  DAT_148e = 100;
  DAT_15b7 = 100;
  DAT_15b8 = 100;
  DAT_15b9 = 100;
  DAT_152b = 100;
  DAT_0051 = DAT_0051 | 0x20;
  DAT_1576 = 0x79;
  DAT_2000 = DAT_00bc;
  DAT_00b4 = 0x42;
  DAT_4000 = 0x42;
  DAT_00d2 = DAT_00d2 | 0xf;
  DAT_158c = DAT_f691;
  DAT_00c3 = DAT_f67c;
  DAT_5000 = 0;
  DAT_00b0 = DAT_00b0 | 0x80;
  DAT_142e = 0xff;
  DAT_152e = 0xff;
  DAT_152f = 0xff;
  DAT_1560 = 0xff;
  DAT_155f = 0;
  DAT_1561 = DAT_ffa0;
  DAT_00db = DAT_fee1;
  if ((DAT_0042 & 0x30) != 0) {
    TRCS = TRCS | 4;
  }
  if ((DAT_0040 & 4) != 0) {
    FUN_b25a();
    return;
  }
  DAT_0041 = DAT_0041 | 1;
  if (_DAT_16a1 == 0x55a5) {
    if (_DAT_16e0 == 0x6997) {
      cVar1 = '\0';
      pcVar3 = (char *)0x169f;
      do {
        pcVar3 = pcVar3 + 1;
        cVar1 = cVar1 + *pcVar3;
      } while (pcVar3 != (char *)0x17ff);
      if (cVar1 == '\0') {
        DAT_14a0 = DAT_16d1 + DAT_f7b7;
        if (CARRY1(DAT_16d1,DAT_f7b7)) {
          DAT_14a0 = -1;
        }
        if (DAT_fef6 != 0) {
          DAT_0057 = 9;
          _DAT_00a9 = _DAT_16d2;
          _DAT_00ab = _DAT_16d4;
          DAT_00ad = DAT_16d6;
          DAT_00b4 = 0x42;
          DAT_00bd = 0xac;
          _DAT_00c8 = _DAT_16e2;
          _DAT_00ca = _DAT_16e4;
          _DAT_00cc = _DAT_16e6;
          DAT_00d5 = 0x99;
          DAT_00d6 = 0;
          DAT_140f = 0;
          DAT_1410 = 0;
          DAT_142e = 0xff;
          DAT_1431 = 100;
          DAT_143a = 0x60;
          DAT_144d = 0;
          DAT_148e = 100;
          DAT_14c8 = 0;
          DAT_152b = 100;
          DAT_152e = 0xff;
          DAT_152f = 0xff;
          DAT_155f = 0;
          DAT_1560 = 0xff;
          DAT_1576 = 0x79;
          DAT_1582 = 5;
          DAT_15b7 = 100;
          DAT_15b8 = 100;
          DAT_15b9 = 100;
          _DAT_16e0 = 0;
          DAT_2000 = DAT_00bc;
          DAT_4000 = 0x42;
          DAT_5000 = 0;
          return;
        }
        goto FUN_b246;
      }
    }
    else {
      puVar2 = (ushort *)&DAT_1700;
      while ((*puVar2 <= (ushort)DAT_f6ce << 8 &&
             ((ushort)DAT_f6cf * 0x100 < *puVar2 || (ushort)DAT_f6cf * 0x100 - *puVar2 == 0))) {
        puVar2 = puVar2 + 1;
        if ((ushort *)0x177f < puVar2) {
          FUN_b25a();
          return;
        }
      }
    }
  }
  DAT_16d1 = 0xff;
  DAT_14a0 = -1;
  DAT_16d7 = 0;
  DAT_16d8 = 0;
  _DAT_16d2 = 0;
  _DAT_16d4 = 0;
  DAT_16d6 = 0;
  _DAT_16e2 = 0;
  _DAT_16e4 = 0;
  _DAT_16e6 = 0;
  _DAT_16d9 = 0;
  _DAT_16db = 0;
  if (_DAT_16a1 != 0x55a5) {
    _DAT_16a1 = 0x55a5;
    DAT_16a4 = DAT_ff1d;
  }
FUN_b246:
  puVar4 = (undefined2 *)&DAT_1700;
  _DAT_16a5 = 0x6400;
  _DAT_00a9 = _DAT_16d2;
  _DAT_00ab = _DAT_16d4;
  DAT_00ad = DAT_16d6;
  _DAT_00c8 = _DAT_16e2;
  _DAT_00ca = _DAT_16e4;
  _DAT_00cc = _DAT_16e6;
  do {
    *puVar4 = 0x6400;
    puVar4 = puVar4 + 1;
  } while (puVar4 != (undefined2 *)0x1780);
  _DAT_16e0 = 0;
  return;
}


// ---- FUN_b246 @ b246 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b246(void)

{
  undefined2 *puVar1;
  
  puVar1 = (undefined2 *)&DAT_1700;
  _DAT_16a5 = 0x6400;
  do {
    *puVar1 = 0x6400;
    puVar1 = puVar1 + 1;
  } while (puVar1 != (undefined2 *)0x1780);
  _DAT_16e0 = 0;
  return;
}


// ---- FUN_b25a @ b25a ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b25a(void)

{
  undefined2 *puVar1;
  
  _DAT_00a9 = _DAT_16d2;
  _DAT_00ab = _DAT_16d4;
  DAT_00ad = DAT_16d6;
  _DAT_00c8 = _DAT_16e2;
  _DAT_00ca = _DAT_16e4;
  _DAT_00cc = _DAT_16e6;
  DAT_14a0 = DAT_16d1 + DAT_f7b7;
  if (CARRY1(DAT_16d1,DAT_f7b7)) {
    DAT_14a0 = -1;
  }
  if (DAT_fef6 == 0) {
    puVar1 = (undefined2 *)&DAT_1700;
    _DAT_16a5 = 0x6400;
    do {
      *puVar1 = 0x6400;
      puVar1 = puVar1 + 1;
    } while (puVar1 != (undefined2 *)0x1780);
  }
  _DAT_16e0 = 0;
  return;
}


// ---- FUN_b291 @ b291 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b291(void)

{
  bool bVar1;
  undefined1 *puVar2;
  undefined2 *puVar3;
  undefined2 *puVar4;
  
  puVar2 = &DAT_ee00;
  if ((DAT_0040 & 8) == 0) {
    if ((DAT_00db & 0x40) != 0) {
      puVar2 = &DAT_ec00;
    }
  }
  else {
    puVar2 = &DAT_ed00;
    if ((DAT_00db & 0x40) != 0) {
      puVar2 = &DAT_eb00;
    }
  }
  DAT_1021 = *puVar2;
  puVar3 = (undefined2 *)(puVar2 + 1);
  do {
    DAT_1022 = *(undefined1 *)puVar3;
    DAT_1023 = *(undefined1 *)((short)puVar3 + 1);
    DAT_1024 = *(undefined1 *)(puVar3 + 1);
    DAT_1025 = *(undefined1 *)((short)puVar3 + 3);
    DAT_1026 = *(undefined1 *)(puVar3 + 2);
    DAT_1027 = *(undefined1 *)((short)puVar3 + 5);
    DAT_1028 = *(undefined1 *)(puVar3 + 3);
    DAT_1029 = *(undefined1 *)((short)puVar3 + 7);
    puVar3 = puVar3 + 4;
    if ((DAT_0040 & 8) == 0) {
      if ((DAT_00db & 0x40) == 0) {
        bVar1 = puVar3 == (undefined2 *)0xee81;
      }
      else {
        bVar1 = puVar3 == (undefined2 *)0xec81;
      }
    }
    else if ((DAT_00db & 0x40) == 0) {
      bVar1 = puVar3 == (undefined2 *)0xed81;
    }
    else {
      bVar1 = puVar3 == (undefined2 *)0xeb81;
    }
  } while (!bVar1);
  _DAT_1570 = (undefined2 *)&DAT_1040;
  do {
    puVar4 = puVar3;
    puVar3 = puVar4 + 1;
    *_DAT_1570 = *puVar4;
    _DAT_1570 = _DAT_1570 + 1;
    if ((DAT_0040 & 8) == 0) {
      if ((DAT_00db & 0x40) == 0) {
        bVar1 = puVar3 == (undefined2 *)0xeeb1;
      }
      else {
        bVar1 = puVar3 == (undefined2 *)0xecb1;
      }
    }
    else if ((DAT_00db & 0x40) == 0) {
      bVar1 = puVar3 == (undefined2 *)0xedb1;
    }
    else {
      bVar1 = puVar3 == (undefined2 *)0xebb1;
    }
  } while (!bVar1);
  DAT_1036 = *(undefined1 *)puVar3;
  _DAT_1012 = *(undefined2 *)((short)puVar4 + 3);
  _DAT_1010 = *(undefined2 *)((short)puVar4 + 5);
  DAT_102a = *(undefined1 *)((short)puVar4 + 7);
  DAT_102b = *(undefined1 *)(puVar4 + 4);
  DAT_102c = *(undefined1 *)((short)puVar4 + 9);
  DAT_1000 = *(undefined1 *)(puVar4 + 5);
  DAT_1001 = *(undefined1 *)((short)puVar4 + 0xb);
  DAT_1002 = *(undefined1 *)(puVar4 + 6);
  if ((DAT_0040 & 4) != 0) {
    DAT_1002 = *(undefined1 *)(puVar4 + 7);
  }
  DAT_1003 = *(undefined1 *)((short)puVar4 + 0xd);
  DAT_1033 = 0;
  DAT_1034 = 0;
  DAT_1035 = 0;
  DAT_1020 = 2;
  DAT_1005 = 0;
  return;
}


// ---- FUN_b394 @ b394 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b394(void)

{
  DAT_00bc = DAT_00bc & 0x7f;
  DAT_0040 = DAT_0040 | 8;
  DAT_00d4 = DAT_00d4 | 0x80;
  P2DATA = DAT_00d3;
  DAT_0017 = DAT_00d4;
  P2DDR = 0x70;
  DAT_0016 = 0xf1;
  TCSR = 0x16;
  P3SCR = 0;
  RAMCR = 0xe7;
  _DAT_001b = &DAT_1407;
  RMCR = 0xc;
  TRCS = 0x3a;
  return;
}


// ---- FUN_b3a0 @ b3a0 ----

void FUN_b3a0(void)

{
  do {
    DAT_1476 = 0;
    FUN_b40e();
    FUN_b4fe();
    FUN_b591();
    FUN_b5c9();
    FUN_b5f4();
    if ((DAT_0040 & 8) == 0) {
      FUN_b5fa();
      FUN_b669();
      FUN_b755();
      FUN_b800();
      FUN_bb49();
      FUN_bb70();
      FUN_bd1d();
      FUN_bd84();
      FUN_c59a();
    }
    else {
      FUN_c9a9();
    }
    P2DATA = DAT_00d3;
    DAT_0017 = DAT_00d4;
    DAT_2000 = DAT_00bc;
    DAT_00b4 = DAT_00b4 | 0x40;
    DAT_1002 = DAT_009c;
    DAT_4000 = DAT_00b4;
  } while( true );
}


// ---- FUN_b3f6 @ b3f6 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_b3f6(undefined1 param_1,undefined1 param_2)

{
  byte bVar1;
  
  bVar1 = DAT_00b1;
  FUN_809f(DAT_00b1,param_2,0xfe20);
  _DAT_004d = (ushort)bVar1 * 0x7d;
  _DAT_15bf = (ushort)bVar1 * 100;
  return;
}


// ---- FUN_b40e @ b40e ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b40e(void)

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
  
  FUN_b4d4();
  uVar1 = extraout_B;
  if (DAT_1453 != '\0') {
    _DAT_0089 = CONCAT11(DAT_008f,extraout_B);
    _DAT_008b = CONCAT11(DAT_140d,0x4b);
    DAT_140d = FUN_b4ac();
    uVar1 = extraout_B_00;
  }
  DAT_008f = uVar1;
  FUN_b4d4();
  uVar1 = extraout_B_01;
  if (DAT_1453 != '\0') {
    _DAT_0089 = CONCAT11(DAT_00d7,extraout_B_01);
    _DAT_008b = CONCAT11(DAT_140e,0x10);
    DAT_140e = FUN_b4ac();
    uVar1 = extraout_B_02;
  }
  DAT_00d7 = uVar1;
  FUN_b4d4();
  _DAT_0089 = CONCAT11(DAT_1401,extraout_B_03);
  _DAT_008b = CONCAT11(DAT_14ca,0x10);
  DAT_14ca = FUN_b4ac();
  DAT_1401 = extraout_B_04;
  FUN_b4d4();
  uVar1 = extraout_B_05;
  if (DAT_15c2 != '\0') {
    _DAT_0089 = CONCAT11(DAT_15c1,extraout_B_05);
    _DAT_008b = CONCAT11(DAT_14cb,0x10);
    DAT_14cb = FUN_b4ac();
    uVar1 = extraout_B_06;
  }
  DAT_15c1 = uVar1;
  FUN_b4d4();
  _DAT_0089 = CONCAT11(DAT_1402,extraout_B_07);
  _DAT_008b = CONCAT11(DAT_1527,0x10);
  DAT_1527 = FUN_b4ac();
  if (DAT_1526 == '\0') {
    DAT_1526 = extraout_B_08;
  }
  DAT_1402 = extraout_B_08;
  FUN_b4d4();
  DAT_1583 = extraout_B_09;
  return;
}


// ---- FUN_b4ac @ b4ac ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

byte FUN_b4ac(void)

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


// ---- FUN_b4d4 @ b4d4 ----

undefined1 FUN_b4d4(undefined1 param_1,char param_2)

{
  short sVar1;
  char cVar2;
  ushort uVar3;
  
  DAT_1006 = param_2 + ' ';
  uVar3 = CONCAT11(param_2,param_2) & 0xff03;
  cVar2 = (char)(uVar3 >> 8);
  do {
  } while (-1 < (char)(param_2 + ' '));
  sVar1 = *(short *)((byte)((char)uVar3 << 1) + 0x1007);
  if ((cVar2 != '\0') && (cVar2 != '\x06')) {
    return (char)((ushort)sVar1 >> 8);
  }
  return (char)((ushort)(sVar1 << 6) >> 8);
}


// ---- FUN_b4fe @ b4fe ----

void FUN_b4fe(undefined1 param_1,undefined1 param_2)

{
  byte bVar1;
  undefined1 uVar2;
  
  if ((DAT_00d8 & 1) == 0) {
    bVar1 = DAT_00bd;
    if ((2 < DAT_00d7) && (DAT_00d7 < 0xf2)) {
      if (DAT_00d7 == DAT_1489) {
        if (DAT_15c1 != DAT_1425) {
          DAT_1425 = DAT_15c1;
          DAT_1424 = FUN_80a9();
        }
        if (((DAT_0015 & 0x80) == 0) || (0x6f < DAT_008f)) {
          if (DAT_1453 == '\0') {
            DAT_1453 = DAT_140c;
          }
          if (DAT_0082 == '\0') {
            DAT_0082 = DAT_00b1;
          }
          if (DAT_15c2 == '\0') {
            DAT_15c2 = DAT_1424;
          }
        }
        return;
      }
      DAT_1489 = DAT_00d7;
      bVar1 = DAT_00d7;
    }
    uVar2 = FUN_80a9(bVar1,param_2,0xfb30);
    DAT_140c = FUN_b532(DAT_140c,uVar2);
  }
  else {
    DAT_1489 = 0;
    DAT_140c = DAT_1667;
  }
  FUN_b53c();
  return;
}


// ---- FUN_b532 @ b532 ----

byte FUN_b532(byte param_1,byte param_2)

{
  byte bVar1;
  
  bVar1 = param_2;
  if ((param_1 < param_2) || (bVar1 = param_2 + 2, (byte)(param_2 + 2) <= param_1)) {
    param_1 = bVar1;
  }
  return param_1;
}


// ---- FUN_b53c @ b53c ----

void FUN_b53c(void)

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
  if (DAT_15c1 != DAT_1425) {
    DAT_1425 = DAT_15c1;
    DAT_1424 = FUN_80a9();
  }
  if (((DAT_0015 & 0x80) == 0) || (0x6f < DAT_008f)) {
    if (DAT_1453 == '\0') {
      DAT_1453 = DAT_140c;
    }
    if (DAT_0082 == '\0') {
      DAT_0082 = DAT_00b1;
    }
    if (DAT_15c2 == '\0') {
      DAT_15c2 = DAT_1424;
    }
  }
  return;
}


// ---- FUN_b591 @ b591 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void FUN_b591(void)

{
  byte bVar1;
  byte bVar2;
  short sVar3;
  ushort uVar4;
  byte bStack0000;
  
  bVar2 = DAT_00b1;
  if ((DAT_0051 & 0x20) == 0) {
    FUN_809f();
    bVar1 = DAT_158e;
    sVar3 = (ushort)bVar2 * 400;
    if ((short)((ushort)bVar2 * 200) < 0) {
      sVar3 = CONCAT11(0xff,(char)sVar3);
    }
    DAT_15b6 = (undefined1)((ushort)sVar3 >> 8);
    bStack0000 = bVar2;
    FUN_809f(DAT_158e,(char)sVar3,0xf5a0);
    uVar4 = (ushort)bVar1 * (ushort)bStack0000;
  }
  else {
    uVar4 = 0;
  }
  _DAT_1418 = (uVar4 >> 8) << 10;
  return;
}


// ---- FUN_b5c9 @ b5c9 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b5c9(void)

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


// ---- FUN_b5f4 @ b5f4 ----

void FUN_b5f4(void)

{
  DAT_1576 = 0x79;
  return;
}


// ---- FUN_b5fa @ b5fa ----

void FUN_b5fa(void)

{
  byte bVar1;
  
  if ((DAT_00d9 & 0x20) == 0) {
    if ((DAT_0054 & 8) != 0) {
      if (DAT_1413 < DAT_ffbc) {
        DAT_0099 = 0;
      }
      else {
        DAT_0099 = DAT_0099 | 0x80;
        if (DAT_ffbd <= DAT_0099) goto LAB_b662;
      }
      if ((((DAT_0053 & 3) == 0) && ((DAT_007e & 1) == 0)) && (DAT_140c < DAT_f9fa)) {
        if (DAT_1453 < 0x41) {
          if (DAT_140c < DAT_f9f9) goto LAB_b662;
        }
        else if (DAT_140c < 0x69) goto LAB_b662;
        bVar1 = DAT_ff23;
        if ((DAT_0059 & 1) == 0) {
          bVar1 = DAT_ff22;
        }
        if (DAT_1460 < bVar1) goto LAB_b65a;
      }
    }
  }
  else if (DAT_1674 == '\0') {
LAB_b65a:
    DAT_0059 = DAT_0059 | 1;
    DAT_009c = DAT_009c & 0xbf;
    return;
  }
LAB_b662:
  DAT_0059 = DAT_0059 & 0xfe;
  DAT_009c = DAT_009c | 0x40;
  return;
}


// ---- FUN_b669 @ b669 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b669(void)

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
          FUN_b6d2();
          FUN_b6d2();
          FUN_b6d2();
          FUN_b6d2();
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
                goto LAB_b714;
              }
              pbVar4 = pbVar4 + 2;
              cVar2 = cVar2 + '\x02';
            } while (cVar2 != '\0');
            if (bVar1 == 0x55) {
              if (pbVar4 != (byte *)0x140) {
                return;
              }
              DAT_0040 = 0xa0;
LAB_b714:
              _DAT_0041 = 0;
              DAT_0043 = 0;
              puVar3 = (undefined2 *)&DAT_0048;
              do {
                *puVar3 = 0;
                puVar3 = puVar3 + 1;
              } while (puVar3 != (undefined2 *)0x140);
              puVar3 = (undefined2 *)&DAT_1400;
              do {
                *puVar3 = 0;
                puVar3 = puVar3 + 1;
              } while (puVar3 != (undefined2 *)&DAT_1640);
              if ((DAT_0040 & 4) == 0) {
                puVar3 = (undefined2 *)&DAT_1640;
                do {
                  *puVar3 = 0;
                  puVar3 = puVar3 + 1;
                } while (puVar3 != (undefined2 *)&DAT_16a0);
                DAT_1695 = 0x3b;
                _DAT_1696 = 0x104;
              }
              if ((DAT_0040 & 1) == 0) {
                _DAT_013e = 0xb0b2;
                FUN_b0d5();
                _DAT_013e = 0xb0b5;
                FUN_b10e();
                _DAT_013e = 0xb0b8;
                FUN_b291();
                _DAT_013e = 0xb0bc;
                FUN_b40e();
                _DAT_013e = 0xb0bf;
                FUN_b4fe();
                _DAT_013e = 0xb0c2;
                FUN_b3f6();
                _DAT_013e = 0xb0c5;
                FUN_8e2b();
                FUN_b3a0();
                return;
              }
              _DAT_013e = 0xb0cb;
              FUN_b394();
              _DAT_013e = 0xb0ce;
              FUN_b10e();
              _DAT_013e = 0xb0d1;
              FUN_b291();
              FUN_b3a0();
              return;
            }
            bVar1 = ~bVar1;
          } while( true );
        }
      }
      else {
        if (DAT_00d7 < 0x21) {
          _RMCR = 0x420;
          if ((byte)(((P2DATA & 0xc) >> 3) + ((P2DATA & 0xc) >> 2 & 1)) == '\x01') {
            DAT_00d3 = DAT_00d3 & 0xef;
          }
          else {
            DAT_00d3 = DAT_00d3 | 0x10;
          }
          P2DATA = DAT_00d3;
          return;
        }
        if ((DAT_0040 & 0x40) == 0) {
          DAT_0040 = DAT_0040 | 0x40;
          FUN_b720();
          return;
        }
      }
    }
  }
  return;
}


// ---- FUN_b6d2 @ b6d2 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b6d2(undefined1 param_1,undefined1 param_2,byte *param_3)

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
        goto LAB_b714;
      }
      param_3 = param_3 + 2;
      cVar2 = cVar2 + '\x02';
    } while (cVar2 != '\0');
    if (bVar1 == 0x55) {
      if (param_3 != (byte *)0x140) {
        return;
      }
      DAT_0040 = 0xa0;
LAB_b714:
      _DAT_0041 = 0;
      DAT_0043 = 0;
      puVar3 = (undefined2 *)&DAT_0048;
      do {
        *puVar3 = 0;
        puVar3 = puVar3 + 1;
      } while (puVar3 != (undefined2 *)0x140);
      puVar3 = (undefined2 *)&DAT_1400;
      do {
        *puVar3 = 0;
        puVar3 = puVar3 + 1;
      } while (puVar3 != (undefined2 *)&DAT_1640);
      if ((DAT_0040 & 4) == 0) {
        puVar3 = (undefined2 *)&DAT_1640;
        do {
          *puVar3 = 0;
          puVar3 = puVar3 + 1;
        } while (puVar3 != (undefined2 *)&DAT_16a0);
        DAT_1695 = 0x3b;
        _DAT_1696 = 0x104;
      }
      if ((DAT_0040 & 1) == 0) {
        _DAT_013e = 0xb0b2;
        FUN_b0d5();
        _DAT_013e = 0xb0b5;
        FUN_b10e();
        _DAT_013e = 0xb0b8;
        FUN_b291();
        _DAT_013e = 0xb0bc;
        FUN_b40e();
        _DAT_013e = 0xb0bf;
        FUN_b4fe();
        _DAT_013e = 0xb0c2;
        FUN_b3f6();
        _DAT_013e = 0xb0c5;
        FUN_8e2b();
        FUN_b3a0();
        return;
      }
      _DAT_013e = 0xb0cb;
      FUN_b394();
      _DAT_013e = 0xb0ce;
      FUN_b10e();
      _DAT_013e = 0xb0d1;
      FUN_b291();
      FUN_b3a0();
      return;
    }
    bVar1 = ~bVar1;
  } while( true );
}


// ---- FUN_b720 @ b720 ----

void FUN_b720(void)

{
  byte bVar1;
  byte *pbVar2;
  
  pbVar2 = (byte *)0x7fff;
  bVar1 = 0;
  DAT_145a = '\0';
  do {
    pbVar2 = pbVar2 + 1;
    bVar1 = bVar1 ^ *pbVar2;
    DAT_145a = DAT_145a + *pbVar2;
    DAT_1476 = 0;
  } while (pbVar2 != (byte *)((short)&RST_VECTOR + 1));
  DAT_1459 = bVar1;
  if ((bVar1 == DAT_ff7a) && (DAT_145a == DAT_ff7b)) {
    DAT_0040 = DAT_0040 & 0xef;
    return;
  }
  DAT_0040 = DAT_0040 | 0x10;
  DAT_1459 = -2 - DAT_145a;
  DAT_145a = bVar1;
  return;
}


// ---- FUN_b755 @ b755 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b755(void)

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
    if ((DAT_ffb7 <= DAT_1460) || (DAT_ff21 <= DAT_1413)) goto LAB_b7a2;
    if ((DAT_0053 & 0x80) == 0) {
      if (DAT_1439 != '\0') goto LAB_b7a7;
      goto LAB_b7a2;
    }
    if ((DAT_fefc <= DAT_1413) || (DAT_ff81 <= DAT_1460)) goto LAB_b7a2;
LAB_b7a7:
    DAT_0059 = DAT_0059 | 0x80;
  }
  else {
    DAT_00c7 = DAT_00c7 | 1;
LAB_b7a2:
    DAT_0059 = DAT_0059 & 0x7f;
  }
  DAT_007d = DAT_007d & 0x4f;
  DAT_007d = DAT_007d | 0x40;
  if ((DAT_0053 & 0x80) == 0) {
    _DAT_0074 = 0xfd00;
  }
  else {
    _DAT_0074 = 0xf400;
  }
  _DAT_0076 = 0xfb00;
  _DAT_0078 = 0xfaf0;
  DAT_141a = FUN_80cf();
  _DAT_1422 = (ushort)(byte)(DAT_141a + 0x40) << 0xb;
  if ((DAT_0059 & 8) == 0) {
    if (1 < extraout_B) goto LAB_b7ed;
  }
  else if (extraout_B != 0) {
LAB_b7ed:
    if ((DAT_0059 & 0x80) == 0) {
      DAT_0059 = DAT_0059 | 8;
      DAT_141d = extraout_B;
      goto LAB_b7f5;
    }
  }
  DAT_0059 = DAT_0059 & 0xf7;
  DAT_141d = 0;
LAB_b7f5:
  _DAT_1426 = (ushort)DAT_141d << 0xb;
  return;
}


// ---- FUN_b800 @ b800 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_b800(void)

{
  byte bVar1;
  byte bVar2;
  char cVar3;
  short sVar4;
  undefined1 *puVar5;
  undefined1 *puVar6;
  byte bStack0000;
  
  bStack0000 = FUN_809f();
  bVar1 = FUN_80a9();
  if (((SUB21((ushort)bVar1 * (ushort)bStack0000 >> 0xf,0)) ||
      (bVar1 = (byte)((ushort)bVar1 * (ushort)bStack0000 * 2 >> 8), bVar2 = bVar1 + DAT_ff8e,
      CARRY1(bVar1,DAT_ff8e))) ||
     ((bVar1 = DAT_ff8e + 5, (byte)(DAT_ff8e + 5) <= bVar2 && (bVar1 = bVar2, 0x60 < bVar2)))) {
    DAT_143a = '\x18';
  }
  else {
    DAT_143a = 'x' - bVar1;
  }
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_0053 & 1) == 0) {
      if ((((DAT_140c < DAT_ffd5) && (0x40 < DAT_1453)) && (DAT_1453 < 0x55)) &&
         (DAT_ffd4 <= DAT_140c)) {
        sVar4 = CONCAT11(DAT_1460,DAT_1482);
        if ((DAT_007d & 4) != 0) {
          sVar4 = sVar4 + 0xa08;
        }
        if (((byte)sVar4 < DAT_ffd6) && ((byte)((ushort)sVar4 >> 8) < DAT_ffd7)) {
          DAT_007d = DAT_007d & 0xfb;
          FUN_809f();
          DAT_0059 = DAT_0059 & 0xbf;
          goto LAB_b851;
        }
      }
LAB_ba13:
      puVar5 = (undefined1 *)0xffe0;
      if ((DAT_007f & 0x80) != 0) {
        puVar5 = (undefined1 *)0xf9e3;
      }
      puVar6 = puVar5;
      if ((DAT_ffdc <= DAT_1460) && (puVar6 = puVar5 + 3, DAT_ffdd <= DAT_1460)) {
        puVar6 = puVar5 + 6;
      }
      puVar5 = puVar6;
      if ((DAT_ffda <= DAT_1482) && (puVar5 = puVar6 + 1, DAT_ffdb <= DAT_1482)) {
        puVar5 = puVar6 + 2;
      }
      DAT_146c = *puVar5;
      DAT_007d = DAT_007d & 0x1f;
      DAT_007d = DAT_007d | 0x14;
      DAT_0059 = DAT_0059 & 0xbf;
      _DAT_0074 = 0xfc00;
      _DAT_0076 = 0xfb20;
      _DAT_0078 = 0xfb10;
      cVar3 = FUN_80cf();
      bStack0000 = cVar3 + -0x80;
      if ((DAT_007d & 8) == 0) {
        if ((DAT_007d & 1) != 0) {
          if ((DAT_feff <= DAT_1460) && (DAT_ff74 <= DAT_1482)) goto LAB_ba7d;
          DAT_146d = 0;
          DAT_146c = 0;
        }
      }
      else {
LAB_ba7d:
        DAT_007d = DAT_007d | 1;
        DAT_146d = FUN_809f();
      }
      sVar4 = CONCAT11(bStack0000,DAT_ff10);
      if ((DAT_ff10 == 0xff) || (DAT_1477 <= DAT_ff10)) {
        bVar1 = FUN_809f();
        bVar2 = FUN_809f();
        cVar3 = bVar2 - bVar1;
        if (bVar2 < bVar1) {
          cVar3 = '\0';
        }
        if ((char)bStack0000 < '\0') {
          sVar4 = (ushort)(byte)(cVar3 + bStack0000) << 8;
          if (sVar4 < 0) goto LAB_bac9;
        }
        else {
          sVar4 = (ushort)(byte)(cVar3 + bStack0000) << 8;
        }
        if (0x3b < (byte)((ushort)sVar4 >> 8)) {
          sVar4 = 0x3c00;
        }
      }
LAB_bac9:
      bStack0000 = (byte)((ushort)sVar4 >> 8);
      cVar3 = FUN_809f();
      bStack0000 = bStack0000 - cVar3;
      if (DAT_141d == 0) {
LAB_bb1c:
        DAT_141c = 0;
      }
      else {
        bVar1 = DAT_140c;
        if ((DAT_0059 & 0x10) != 0) {
          bVar1 = DAT_140c + 2;
        }
        if (bVar1 < DAT_ff12) {
          DAT_0059 = DAT_0059 & 0xef;
          goto LAB_bb1c;
        }
        DAT_0059 = DAT_0059 | 0x10;
        if ((DAT_fee0 & 0x40) != 0) {
          bStack0000 = bStack0000 - DAT_ff13;
          goto LAB_bb1c;
        }
        DAT_141c = DAT_ff11;
        if ((DAT_ff8a <= (byte)(DAT_ff11 + DAT_141d)) &&
           (DAT_141c = DAT_ff8a - DAT_141d, DAT_ff8a < DAT_141d)) {
          DAT_141c = 0;
        }
      }
      DAT_143b = bStack0000;
      goto LAB_bb23;
    }
    sVar4 = CONCAT11(DAT_140c,DAT_1482);
    if ((DAT_0059 & 0x20) != 0) {
      sVar4 = sVar4 + 0x508;
    }
    if ((DAT_ff70 <= (byte)sVar4) && (DAT_ff71 <= (byte)((ushort)sVar4 >> 8))) {
      bVar1 = DAT_ff72;
      if ((DAT_0059 & 0x20) != 0) {
        bVar1 = DAT_ff72 + 0x10;
      }
      if (DAT_1442 <= bVar1) {
        DAT_0059 = DAT_0059 | 0x20;
        goto LAB_ba13;
      }
    }
    DAT_0059 = DAT_0059 & 0xdf;
    if ((DAT_0053 & 4) == 0) {
      bVar1 = FUN_809f();
      if ((DAT_0059 & 0x40) == 0) {
LAB_b8dc:
        DAT_0059 = DAT_0059 & 0xfb;
      }
      else if ((DAT_0059 & 4) != 0) {
        if (bVar1 < DAT_142f) {
          if (DAT_14ce <= DAT_142f) {
            DAT_142f = DAT_142f - DAT_14ce;
          }
        }
        else {
          if (bVar1 == DAT_142f) goto LAB_b8dc;
          DAT_142f = DAT_142f + DAT_14ce;
        }
      }
      DAT_1430 = 0;
    }
    else {
      bVar1 = FUN_809f();
      if ((DAT_0059 & 0x40) == 0) {
LAB_b91f:
        DAT_0059 = DAT_0059 | 4;
      }
      else if ((DAT_0059 & 4) == 0) {
        if (bVar1 < DAT_1430) {
          if (DAT_14ce <= DAT_1430) {
            DAT_1430 = DAT_1430 - DAT_14ce;
          }
        }
        else {
          if (bVar1 == DAT_1430) goto LAB_b91f;
          DAT_1430 = DAT_1430 + DAT_14ce;
        }
      }
      DAT_142f = 0;
    }
    DAT_14ce = 0;
    DAT_0059 = DAT_0059 | 0x40;
    if (((((DAT_00d9 & 0x10) == 0) || (DAT_1673 != '\0')) && ((DAT_00b9 & 0x20) == 0)) &&
       ((DAT_00bf & 0x20) != 0)) {
      bStack0000 = 0;
      if (DAT_143f != _DAT_140a) {
        if (DAT_143f < _DAT_140a) {
          DAT_151a = FUN_809f();
          FUN_809f();
        }
        else {
          DAT_1519 = FUN_809f();
          FUN_809f();
        }
      }
    }
  }
  else {
    FUN_809f();
  }
LAB_b851:
  DAT_146d = 0;
  DAT_146c = 0;
  DAT_141c = 0;
  DAT_143b = '\0';
LAB_bb23:
  _DAT_1428 = (ushort)DAT_141c << 0xb;
  DAT_145f = DAT_146c;
  DAT_145e = DAT_146d;
  if ((DAT_007d & 8) == 0) {
    DAT_007f = DAT_007f & 0xf7;
  }
  else {
    DAT_007f = DAT_007f | 8;
  }
  return;
}


// ---- FUN_bb49 @ bb49 ----

void FUN_bb49(void)

{
  if ((DAT_00d9 & 2) == 0) {
    if (((DAT_0054 & 8) == 0) && (((DAT_0040 & 4) != 0 || (0x31 < DAT_1454)))) goto LAB_bb6c;
  }
  else if (DAT_1670 == '\0') {
LAB_bb6c:
    DAT_00bc = DAT_00bc & 0xdf;
    return;
  }
  DAT_00bc = DAT_00bc | 0x20;
  return;
}


// ---- FUN_bb70 @ bb70 ----

/* WARNING: Removing unreachable block (RAM,0xbc86) */
/* WARNING: Removing unreachable block (RAM,0xbc94) */
/* WARNING: Removing unreachable block (RAM,0xbc9c) */
/* WARNING: Removing unreachable block (RAM,0xbc9e) */
/* WARNING: Removing unreachable block (RAM,0xbc8f) */
/* WARNING: Removing unreachable block (RAM,0xbca1) */
/* WARNING: Removing unreachable block (RAM,0xbca6) */
/* WARNING: Removing unreachable block (RAM,0xbcae) */
/* WARNING: Removing unreachable block (RAM,0xbcb1) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_bb70(void)

{
  byte bVar1;
  
  if ((DAT_fee1 & 2) == 0) {
    if (((DAT_0054 & 8) == 0) && (((DAT_0040 & 4) != 0 || (0x31 < DAT_1454)))) {
      DAT_00d4 = DAT_00d4 & 0xef;
      return;
    }
    DAT_00d4 = DAT_00d4 | 0x10;
    return;
  }
  DAT_00a5 = DAT_008f - DAT_1583;
  if (DAT_008f < DAT_1583) {
    DAT_00a5 = 0;
  }
  if ((DAT_0054 & 8) == 0) {
    if (((DAT_0040 & 4) == 0) && (DAT_1454 < 0x32)) goto LAB_bbf9;
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
        else if ((DAT_0053 & 1) == 0) goto LAB_bbf9;
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
        goto LAB_bcd3;
      }
    }
    else if (DAT_140c < 100) {
      DAT_1467 = '\0';
    }
    else {
      DAT_1467 = '\x1e';
    }
LAB_bbf9:
    DAT_1584 = DAT_008f - DAT_f678;
    bVar1 = 100;
  }
LAB_bcd3:
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
    if (((DAT_0040 & 4) != 0) || (0x31 < DAT_1454)) goto LAB_bd19;
  }
  else if ((DAT_00b7 & 0x40) == 0) {
    if (DAT_f9fc <= DAT_1453) {
      if ((DAT_0053 & 2) != 0) goto LAB_bd0c;
      if (DAT_1477 < DAT_f9fd) {
        return;
      }
    }
LAB_bd19:
    DAT_00d4 = DAT_00d4 & 0xef;
    return;
  }
LAB_bd0c:
  DAT_00d4 = DAT_00d4 | 0x10;
  return;
}


// ---- FUN_bd1d @ bd1d ----

void FUN_bd1d(void)

{
  char cVar1;
  byte bVar2;
  byte bVar3;
  
  cVar1 = DAT_1481;
  if ((DAT_00d9 & 4) == 0) {
    if ((DAT_0054 & 8) == 0) {
      DAT_00bc = DAT_00bc & 0xbf;
      return;
    }
    if ((DAT_0053 & 2) == 0) {
      if (DAT_1481 != '\0') {
        bVar2 = DAT_ffc2;
        bVar3 = DAT_ffc3;
        if ((DAT_00bc & 0x40) == 0) {
          bVar2 = DAT_ffc2 - 10;
          if (DAT_ffc2 < 10) {
            bVar2 = 0;
          }
          bVar3 = DAT_ffc3 - 0x10;
          if (DAT_ffc3 < 0x10) {
            bVar3 = 0;
          }
        }
        if ((DAT_1460 <= bVar2) && (DAT_1413 <= bVar3)) goto LAB_bd80;
      }
    }
    else if (((DAT_00b9 & 0x40) == 0) &&
            ((cVar1 = DAT_ff78, DAT_ff76 <= DAT_15c2 || (cVar1 = DAT_ff79, DAT_ff77 <= DAT_15c2))))
    goto LAB_bd80;
  }
  else if (DAT_1671 != '\0') {
LAB_bd80:
    DAT_1481 = cVar1;
    DAT_00bc = DAT_00bc | 0x40;
    return;
  }
  DAT_00bc = DAT_00bc & 0xbf;
  return;
}


// ---- FUN_bd84 @ bd84 ----

/* WARNING: Removing unreachable block (RAM,0xc301) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_bd84(void)

{
  bool bVar1;
  byte bVar2;
  byte bVar3;
  short sVar4;
  
  if ((DAT_0054 & 8) == 0) {
    if (DAT_1442 < 4) {
      if ((DAT_0053 & 2) == 0) {
        DAT_14ac = DAT_008f;
      }
      else if ((((DAT_0053 & 0x44) != 0) && (0x7c < DAT_14ac)) &&
              (DAT_008f <= (byte)(DAT_14ac - 0xc))) goto LAB_bde9;
      goto LAB_be00;
    }
LAB_bde9:
    DAT_0085 = DAT_0085 | 0x80;
    DAT_00b6 = DAT_00b6 | 0x80;
    if (0x89 < DAT_0085) {
LAB_bdf5:
      DAT_00a9 = DAT_00a9 | 0x80;
      DAT_0048 = DAT_0048 | 0x80;
      DAT_16a8 = 0;
    }
  }
  else {
    if (DAT_1442 == 0) {
      DAT_14c4 = DAT_14c4 | 0x80;
      if (0x93 < DAT_14c4) goto LAB_bdf5;
    }
    else {
      DAT_14c4 = 0;
      if (0x2f < DAT_1442) {
        _DAT_005b = CONCAT21(_DAT_140a,DAT_005d);
        FUN_8001();
        sVar4 = _DAT_005c << 2;
        DAT_145c = (undefined1)sVar4;
        if ((char)((ushort)sVar4 >> 8) != '\0') {
          sVar4 = 0xff;
        }
        if (((byte)sVar4 < 0x50) || (0x80 < (byte)sVar4)) goto LAB_bde9;
      }
    }
LAB_be00:
    DAT_0085 = 0;
    DAT_00b6 = DAT_00b6 & 0x7f;
  }
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_15c1 < 3) || (0xf1 < DAT_15c1)) {
      DAT_00b9 = DAT_00b9 | 0x40;
      if (99 < DAT_15c3) {
        DAT_00ac = DAT_00ac | 0x40;
        DAT_16c1 = 0;
        goto LAB_be2e;
      }
    }
    else {
      DAT_00b9 = DAT_00b9 & 0xbf;
      DAT_15c3 = 0;
    }
  }
  else {
LAB_be2e:
    DAT_15c3 = 0;
  }
  if ((DAT_0053 & 2) == 0) {
    if ((DAT_00d7 < 3) || (0xf1 < DAT_00d7)) {
      DAT_00b6 = DAT_00b6 | 0x20;
      DAT_155d = 0;
      if (99 < DAT_155c) {
        DAT_00a9 = DAT_00a9 | 0x20;
        DAT_0048 = DAT_0048 | 0x20;
        DAT_00c8 = DAT_00c8 | 0x20;
        DAT_16aa = 0;
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
          DAT_004b = DAT_004b | 0x20;
          DAT_16c2 = 0;
        }
        goto LAB_bec2;
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
LAB_bec2:
  if (((DAT_00c8 & 0x20) == 0) && ((DAT_0053 & 2) == 0)) {
    if ((DAT_140c < DAT_f68b) || (DAT_1402 < DAT_f68d)) {
      DAT_1557 = 0;
    }
    else if (99 < DAT_1557) {
      DAT_00ca = DAT_00ca | 8;
      DAT_00ab = DAT_00ab | 8;
      DAT_004a = DAT_004a | 8;
      DAT_16bc = 0;
    }
    if ((DAT_140c < DAT_f68c) && (DAT_1402 < DAT_f68e)) {
      if (99 < DAT_1558) {
        DAT_00ca = DAT_00ca | 8;
        DAT_00ab = DAT_00ab | 8;
        DAT_004a = DAT_004a | 8;
        DAT_16bc = 0;
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
  if (((((DAT_fee1 & 2) == 0) || ((DAT_0054 & 1) != 0)) || ((DAT_00d4 & 0x10) != 0)) ||
     (DAT_1442 == 0)) {
LAB_bf84:
    DAT_14c9 = 0;
  }
  else {
    bVar3 = DAT_1584 - DAT_00a5;
    if (DAT_1584 < DAT_00a5) {
      bVar3 = -bVar3;
    }
    if (bVar3 < DAT_f677) goto LAB_bf84;
    bVar3 = DAT_14c9 & 0x7f;
    DAT_14c9 = DAT_14c9 | 0x80;
    if (DAT_f6c3 <= bVar3) {
      DAT_00aa = DAT_00aa | 0x40;
      DAT_00b7 = DAT_00b7 | 0x40;
      DAT_0047 = DAT_0047 | 4;
      DAT_0049 = DAT_0049 | 0x40;
      DAT_16b1 = 0;
      goto LAB_bf84;
    }
  }
  if ((DAT_0054 & 8) == 0) {
    DAT_1590 = 0;
    if (((DAT_1454 < 0x32) || ((DAT_0054 & 1) != 0)) || (1 < DAT_1407)) {
      DAT_158f = 0;
    }
    else if (_DAT_1408 < 400) {
      DAT_00b6 = DAT_00b6 & 0xbf;
      if (99 < DAT_158f) {
        DAT_00cd = DAT_00cd & 0xfe;
      }
    }
    else {
      DAT_158f = 0;
      DAT_0081 = DAT_0081 | 0x80;
      if (DAT_0081 < 0xe4) goto LAB_c023;
      DAT_0047 = DAT_0047 | 2;
      DAT_0048 = DAT_0048 | 0x40;
      DAT_00cd = DAT_00cd | 1;
      DAT_00b6 = DAT_00b6 | 0x40;
    }
    DAT_0081 = 0;
  }
  else {
    DAT_158f = 0;
    if ((DAT_1442 < 0x30) || ((DAT_0053 & 2) != 0)) {
      DAT_1590 = 0;
    }
    else if (_DAT_1408 < 100) {
      DAT_1590 = 0;
      DAT_00c5 = DAT_00c5 | 0x80;
      if (DAT_00c5 < 0xe4) goto LAB_c023;
      DAT_00cd = DAT_00cd | 2;
      DAT_00b6 = DAT_00b6 | 0x40;
    }
    else {
      if ((DAT_00b6 & 0x40) != 0) {
        DAT_00b6 = DAT_00b6 & 0xbf;
        FUN_b246();
      }
      if (99 < DAT_1590) {
        DAT_00cd = DAT_00cd & 0xfd;
      }
    }
    DAT_00c5 = 0;
  }
LAB_c023:
  if (((DAT_00cd & 1) == 0) && ((DAT_00cd & 2) == 0)) {
    DAT_00c8 = DAT_00c8 & 0xbf;
  }
  else {
    DAT_00a9 = DAT_00a9 | 0x40;
    DAT_0048 = DAT_0048 | 0x40;
    DAT_00c8 = DAT_00c8 | 0x40;
    DAT_16a9 = 0;
  }
  if (DAT_1407 < 2) {
    if ((((((DAT_0053 & 4) != 0) || ((DAT_00c8 & 0x60) != 0)) || (DAT_1460 < DAT_f79e)) ||
        ((DAT_f695 <= DAT_1460 || (DAT_1413 < DAT_f79d)))) ||
       ((DAT_f696 <= DAT_1413 || (DAT_140c < DAT_f697)))) goto LAB_c094;
    if (DAT_1523 == 0) {
      DAT_1523 = 1;
    }
    if (0x32 < DAT_1523) {
      DAT_00a9 = DAT_00a9 | 0x10;
      DAT_0048 = DAT_0048 | 0x10;
      DAT_00c8 = DAT_00c8 | 0x10;
      DAT_16ab = 0;
      DAT_1523 = 0;
    }
  }
  else {
    DAT_00c8 = DAT_00c8 & 0xef;
LAB_c094:
    DAT_1523 = 0;
  }
  if ((DAT_1460 < DAT_f78e) || (DAT_f78f <= DAT_1460)) {
LAB_c0d9:
    DAT_00a7 = DAT_00a7 & 0xfb;
  }
  else {
    if ((DAT_0053 & 0x10) != 0) {
      if ((DAT_f6a3 <= DAT_1413) && (DAT_1413 < DAT_f6a4)) goto LAB_c0c2;
      goto LAB_c0d9;
    }
    if ((DAT_1413 < DAT_f790) || (DAT_f698 <= DAT_1413)) goto LAB_c0d9;
LAB_c0c2:
    if (((DAT_14a2 < DAT_f68f) || (DAT_f690 <= DAT_14a2)) || ((DAT_0059 & 1) == 0)) goto LAB_c0d9;
    DAT_00a7 = DAT_00a7 | 4;
  }
  if ((((((DAT_00c8 & 0x60) == 0) && ((DAT_00cb & 0x20) == 0)) &&
       (((DAT_00ca & 8) == 0 && ((DAT_f78c <= DAT_1453 && (DAT_f78d <= DAT_140c)))))) &&
      (DAT_f699 <= DAT_1596)) && (DAT_1526 < DAT_f794)) {
    if ((DAT_00a7 & 4) == 0) {
      if ((DAT_1524 < DAT_f796) || (DAT_f797 <= DAT_1528)) goto LAB_c17b;
      goto LAB_c184;
    }
    DAT_1528 = 0;
    if ((DAT_00a7 & 0x80) == 0) {
      DAT_1553 = DAT_1402;
      DAT_00a7 = DAT_00a7 | 0x80;
    }
    if (DAT_1524 < DAT_f792) goto LAB_c184;
    if ((DAT_00a7 & 0x40) == 0) {
      DAT_00a7 = DAT_00a7 | 0x40;
      DAT_1554 = DAT_1402;
    }
    if ((DAT_1402 < DAT_f795) ||
       ((DAT_1554 <= DAT_1553 && (DAT_f688 <= (byte)(DAT_1553 - DAT_1554))))) {
      DAT_00ca = DAT_00ca & 0xbf;
      goto LAB_c184;
    }
    if (0x31 < DAT_1525) {
      DAT_00ab = DAT_00ab | 0x40;
      DAT_004a = DAT_004a | 0x40;
      DAT_00ca = DAT_00ca | 0x40;
      DAT_16b9 = 0;
      goto LAB_c184;
    }
  }
  else {
LAB_c17b:
    DAT_1524 = 0;
    DAT_1528 = 0;
    DAT_00a7 = DAT_00a7 & 0x3f;
LAB_c184:
    DAT_1525 = 0;
  }
  bVar3 = DAT_00a7;
  if ((((DAT_1413 < DAT_f782) || (DAT_f783 <= DAT_1413)) || (DAT_1460 < DAT_f784)) ||
     (DAT_f785 <= DAT_1460)) {
    DAT_00a8 = DAT_00a8 & 0xfe;
    bVar1 = false;
  }
  else {
    DAT_00a8 = DAT_00a8 | 1;
    bVar1 = true;
  }
  if ((((DAT_1453 < DAT_f780) || (DAT_140c < DAT_f781)) ||
      (((DAT_00c8 & 0x60) != 0 || ((DAT_0088 & 0x80) == 0)))) ||
     ((((DAT_009b & 1) == 0 && ((DAT_009b & 8) != 0)) || (((DAT_00b0 & 8) != 0 || (!bVar1)))))) {
    DAT_1521 = 0;
LAB_c200:
    DAT_1555 = 0;
  }
  else {
    if (DAT_1521 < DAT_f689) goto LAB_c200;
    if ((DAT_1400 < DAT_f68a) || (DAT_1435 <= DAT_1400)) {
      DAT_00cd = DAT_00cd & 0xfb;
      goto LAB_c200;
    }
    if (99 < DAT_1555) {
      DAT_00cd = DAT_00cd | 4;
      goto LAB_c200;
    }
  }
  if (DAT_1400 < 200) {
    DAT_00cd = DAT_00cd & 0xf7;
LAB_c219:
    DAT_1556 = 0;
  }
  else if (0x31 < DAT_1556) {
    DAT_00cd = DAT_00cd | 8;
    goto LAB_c219;
  }
  if (((DAT_00cd & 4) == 0) && ((DAT_00cd & 8) == 0)) {
    DAT_00ca = DAT_00ca & 0xdf;
    bVar1 = false;
  }
  else {
    DAT_00ab = DAT_00ab | 0x20;
    DAT_004a = DAT_004a | 0x20;
    DAT_00ca = DAT_00ca | 0x20;
    bVar1 = true;
    DAT_16ba = 0;
  }
  bVar2 = DAT_00ca;
  if (((((bVar1) || ((DAT_00c8 & 0x40) != 0)) || ((DAT_00cb & 0x20) != 0)) ||
      ((((DAT_0051 & 0x20) == 0 || (DAT_1453 < DAT_f69a)) ||
       ((DAT_1413 < DAT_f7a2 || ((DAT_f7a3 <= DAT_1413 || (DAT_1460 < DAT_f7a0)))))))) ||
     (DAT_f7a1 <= DAT_1460)) {
    DAT_00a7 = DAT_00a7 & 0xef;
    DAT_152a = 0;
LAB_c2ba:
    if ((DAT_00a7 & 0x20) != 0) {
      if ((DAT_009b & 0x10) == 0) {
        DAT_00cd = DAT_00cd & 0xdf;
      }
      else if (DAT_152b < DAT_f7a7) {
        DAT_00cd = DAT_00cd | 0x20;
      }
    }
  }
  else {
    DAT_00a7 = DAT_00a7 | 0x10;
    if (DAT_f7a4 <= DAT_152a) {
      _DAT_152b = (_DAT_148e * 2 + _DAT_152b * 3) * 2;
      DAT_00a7 = bVar3 | 0x30;
    }
    if ((DAT_00a7 & 0x20) != 0) {
      if ((byte)(_DAT_152b >> 8) < DAT_f7a5) {
        DAT_152d = (byte)(_DAT_152b - _DAT_16a5 >> 8);
        if (_DAT_152b < _DAT_16a5) {
          DAT_152d = 0;
        }
        if (DAT_152d < DAT_f7a6) {
          if (DAT_152d < DAT_f69b) {
            DAT_00cd = DAT_00cd & 0xef;
          }
        }
        else {
          DAT_00cd = DAT_00cd | 0x10;
        }
      }
      goto LAB_c2ba;
    }
  }
  if (((DAT_00cd & 0x10) == 0) && ((DAT_00cd & 0x20) == 0)) {
    DAT_00cb = DAT_00cb & 0xf7;
  }
  else {
    DAT_00ac = DAT_00ac | 8;
    DAT_004b = DAT_004b | 8;
    DAT_00cb = DAT_00cb | 8;
    DAT_16c4 = 0;
  }
  DAT_00ca = DAT_00ca & 0x7f;
  if ((DAT_00db & 0x40) != 0) {
    if ((((((DAT_00d9 & 1) == 0) && ((DAT_0040 & 8) == 0)) && (DAT_f69c <= DAT_008f)) &&
        (((DAT_f69d <= DAT_158e && (DAT_158e < DAT_f69e)) &&
         (((DAT_0053 & 1) != 0 && ((_DAT_f69f <= _DAT_144e && (_DAT_144e < _DAT_f6a1)))))))) &&
       (((DAT_004f & 0x20) == 0 && (DAT_00cf == '\0')))) {
      _DAT_102b = _DAT_102b | 0xc0f;
    }
    else {
      DAT_1598 = 0;
      DAT_1599 = 0;
      DAT_1597 = 0;
      DAT_00dd = DAT_00dd & 0xfe;
      _DAT_102b = _DAT_102b & 0xf3f0;
    }
    if ((DAT_00cd & 0x80) == 0) {
      DAT_00cc = DAT_00cc & 0x7f;
    }
    else {
      DAT_00ad = DAT_00ad | 0x80;
      DAT_00cc = DAT_00cc | 0x80;
      DAT_004c = DAT_004c | 0x80;
    }
  }
  if (((DAT_0053 & 2) != 0) || ((DAT_004f & 0x80) == 0)) goto LAB_c3f6;
  if ((DAT_0058 & 0x20) == 0) {
    if ((DAT_0053 & 4) == 0) {
      DAT_0058 = DAT_0058 & 0xef | 0x20;
    }
    else if (((DAT_0053 & 1) == 0) && (0x1d < DAT_1407)) {
      if (0x31 < DAT_1539) {
        DAT_0058 = DAT_0058 | 0x10;
      }
      goto LAB_c3bf;
    }
    DAT_1539 = 0;
  }
LAB_c3bf:
  if ((DAT_0058 & 0x80) == 0) {
    if (DAT_1407 == 0) {
      if (((((DAT_0053 & 5) == 0) && ((DAT_0058 & 0x10) == 0)) && (0x27 < DAT_1460)) &&
         (0x2f < DAT_1413)) {
        if (0x31 < DAT_153a) {
          DAT_0058 = DAT_0058 | 0x40;
        }
        goto LAB_c3f6;
      }
    }
    else {
      DAT_0058 = DAT_0058 & 0xbf | 0x80;
    }
    DAT_153a = 0;
  }
LAB_c3f6:
  if ((DAT_0053 & 2) == 0) {
    DAT_0046 = DAT_0046 & 0xfb;
  }
  else if ((DAT_0046 & 4) == 0) {
    DAT_0046 = DAT_0046 | 4;
    if (((DAT_ff15 & 0x80) != 0) && (DAT_16a8 = DAT_16a8 + 1, 0x31 < DAT_16a8)) {
      DAT_16a8 = 0;
      DAT_00a9 = DAT_00a9 & 0x7f;
    }
    if (((DAT_ff15 & 0x40) != 0) && (DAT_16a9 = DAT_16a9 + 1, 0x31 < DAT_16a9)) {
      DAT_16a9 = 0;
      DAT_00a9 = DAT_00a9 & 0xbf;
      DAT_00c8 = DAT_00c8 & 0xbf;
      DAT_00cd = DAT_00cd & 0xfc;
    }
    if (((DAT_ff15 & 0x20) != 0) && (DAT_16aa = DAT_16aa + 1, 0x31 < DAT_16aa)) {
      DAT_16aa = 0;
      DAT_00a9 = DAT_00a9 & 0xdf;
      DAT_00c8 = DAT_00c8 & 0xdf;
    }
    if (((DAT_ff15 & 0x10) != 0) && (DAT_16ab = DAT_16ab + 1, 0x31 < DAT_16ab)) {
      DAT_16ab = 0;
      DAT_00a9 = DAT_00a9 & 0xef;
      DAT_00c8 = DAT_00c8 & 0xef;
    }
    if (((DAT_ff16 & 0x80) != 0) && (DAT_16b0 = DAT_16b0 + 1, 0x31 < DAT_16b0)) {
      DAT_16b0 = 0;
      DAT_00aa = DAT_00aa & 0x7f;
    }
    if (((DAT_ff16 & 0x40) != 0) && (DAT_16b1 = DAT_16b1 + 1, 0x31 < DAT_16b1)) {
      DAT_16b1 = 0;
      DAT_00aa = DAT_00aa & 0xbf;
    }
    if (((DAT_ff17 & 0x80) != 0) && (DAT_16b8 = DAT_16b8 + 1, 0x31 < DAT_16b8)) {
      DAT_16b8 = 0;
      DAT_00ab = DAT_00ab & 0x7f;
    }
    if (((DAT_ff17 & 0x40) != 0) && (DAT_16b9 = DAT_16b9 + 1, 0x31 < DAT_16b9)) {
      DAT_16b9 = 0;
      DAT_00ab = DAT_00ab & 0xbf;
      DAT_00ca = bVar2 & 0x3f;
    }
    if (((DAT_ff17 & 0x20) != 0) && (DAT_16ba = DAT_16ba + 1, 0x31 < DAT_16ba)) {
      DAT_16ba = 0;
      DAT_00ab = DAT_00ab & 0xdf;
      DAT_00ca = DAT_00ca & 0xdf;
      DAT_00cd = DAT_00cd & 0xf3;
    }
    if (((DAT_ff17 & 0x10) != 0) && (DAT_16bb = DAT_16bb + 1, 0x31 < DAT_16bb)) {
      DAT_16bb = 0;
      DAT_00ab = DAT_00ab & 0xef;
    }
    if (((DAT_ff17 & 8) != 0) && (DAT_16bc = DAT_16bc + 1, 0x31 < DAT_16bc)) {
      DAT_16bc = 0;
      DAT_00ab = DAT_00ab & 0xf7;
      DAT_00ca = DAT_00ca & 0xf7;
    }
    if (((DAT_ff18 & 0x40) != 0) && (DAT_16c1 = DAT_16c1 + 1, 0x31 < DAT_16c1)) {
      DAT_16c1 = 0;
      DAT_00ac = DAT_00ac & 0xbf;
    }
    if (((DAT_ff18 & 0x20) != 0) && (DAT_16c2 = DAT_16c2 + 1, 0x31 < DAT_16c2)) {
      DAT_16c2 = 0;
      DAT_00ac = DAT_00ac & 0xdf;
      DAT_00cb = DAT_00cb & 0xdf;
    }
    if (((DAT_ff18 & 0x10) != 0) && (DAT_16c4 = DAT_16c4 + 1, 0x31 < DAT_16c4)) {
      DAT_16c4 = 0;
      DAT_00ac = DAT_00ac & 0xf7;
      DAT_00cb = DAT_00cb & 0xf7;
      DAT_00cd = DAT_00cd & 0xcf;
      DAT_00ce = DAT_00ce & 0xcf;
    }
    if (((DAT_ff19 & 0x80) != 0) && (DAT_16c8 = DAT_16c8 + 1, 0x31 < DAT_16c8)) {
      DAT_16c8 = 0;
      DAT_00ad = DAT_00ad & 0x7f;
      DAT_00cc = DAT_00cc & 0x7f;
      DAT_00ce = DAT_00ce & 0x7f;
    }
    return;
  }
  return;
}


// ---- FUN_c59a @ c59a ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_c59a(void)

{
  undefined1 uVar1;
  undefined1 extraout_B;
  undefined2 uVar2;
  
  if ((((DAT_00d9 & 8) != 0) && (DAT_1672 == '\0')) && ((DAT_0043 & 2) == 0)) {
    DAT_0043 = DAT_0043 | 2;
    FUN_b246();
  }
  _DAT_0074 = &DAT_1700;
  _DAT_0076 = 0xfba8;
  uVar2 = 0xfba0;
  _DAT_0078 = 0xfba0;
  FUN_c5d9();
  uVar1 = FUN_9b0a();
  _DAT_148e = CONCAT11(uVar1,extraout_B);
  _DAT_1486 = uVar2;
  DAT_147f = DAT_1490;
  DAT_1488 = DAT_1491;
  return;
}


// ---- FUN_c5d9 @ c5d9 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined1 FUN_c5d9(void)

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
    if (bVar6 < _DAT_0076[7]) goto LAB_c647;
    bVar6 = _DAT_0076[7];
  }
  _DAT_0067 = (ushort)bVar6 << 2;
LAB_c647:
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
    uVar3 = FUN_c6f1();
    _DAT_008b = CONCAT11(uVar3,extraout_B_01) + puVar8[1];
  }
  else {
    uVar3 = FUN_c6f1();
    _DAT_008b = CONCAT11(uVar3,extraout_B_00) + *puVar8;
  }
  DAT_006d = DAT_1490;
  if ((puVar8[9] < puVar8[8]) && (DAT_1490 != '\0')) {
    DAT_006d = -DAT_1490;
    uVar3 = FUN_c6f1();
    _DAT_008d = CONCAT11(uVar3,extraout_B_03) + puVar8[9];
  }
  else {
    uVar3 = FUN_c6f1();
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
    uVar3 = FUN_c6f1();
    uVar3 = (undefined1)(CONCAT11(uVar3,extraout_B_06) + _DAT_008d >> 8);
  }
  else {
    uVar3 = FUN_c6f1();
    uVar3 = (undefined1)(CONCAT11(uVar3,extraout_B_05) + _DAT_008b >> 8);
  }
  return uVar3;
}


// ---- FUN_c6f1 @ c6f1 ----

char FUN_c6f1(void)

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


// ---- vec_TOF @ c706 ----

undefined1 vec_TOF(void)

{
  undefined1 in_stack_00000003;
  
  FUN_c709();
  return in_stack_00000003;
}


// ---- FUN_c709 @ c709 ----

undefined1 FUN_c709(void)

{
  DAT_1567 = DAT_1567 + '\x01';
  return (char)((ushort)TIMER >> 8);
}


// ---- FUN_c884 @ c884 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_c884(void)

{
  if ((DAT_0054 & 1) == 0) {
    if ((DAT_00bb & 0x40) == 0) {
      if ((DAT_0040 & 2) != 0) goto LAB_c8c8;
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
    if ((DAT_00db & 0x40) == 0) {
      DAT_1011 = 0xff;
    }
    else {
      DAT_1011 = 0xef;
    }
  }
  else {
LAB_c8c8:
    DAT_1003 = 0;
    if ((DAT_00db & 0x40) == 0) {
      DAT_1011 = 0x7f;
    }
    else {
      DAT_1011 = 0x6f;
    }
  }
  return;
}


// ---- FUN_c8dc @ c8dc ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_c8dc(void)

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
       ((((DAT_0053 & 4) != 0 && (0x7c < DAT_14ac)) && (DAT_008f <= (byte)(DAT_14ac - 0xc))))) {
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
LAB_c95b:
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
        goto LAB_c95b;
      }
    }
    DAT_14d4 = '\0';
  }
  _DAT_14d7 = 0;
  return;
}


// ---- FUN_c97b @ c97b ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_c97b(void)

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
        } while (puVar1 != (undefined2 *)&DAT_1640);
        if ((DAT_0040 & 4) == 0) {
          puVar1 = (undefined2 *)&DAT_1640;
          do {
            *puVar1 = 0;
            puVar1 = puVar1 + 1;
          } while (puVar1 != (undefined2 *)&DAT_16a0);
          DAT_1695 = 0x3b;
          _DAT_1696 = 0x104;
        }
        if ((DAT_0040 & 1) == 0) {
          _DAT_013e = 0xb0b2;
          FUN_b0d5();
          _DAT_013e = 0xb0b5;
          FUN_b10e();
          _DAT_013e = 0xb0b8;
          FUN_b291();
          _DAT_013e = 0xb0bc;
          FUN_b40e();
          _DAT_013e = 0xb0bf;
          FUN_b4fe();
          _DAT_013e = 0xb0c2;
          FUN_b3f6();
          _DAT_013e = 0xb0c5;
          FUN_8e2b();
          FUN_b3a0();
          return;
        }
        _DAT_013e = 0xb0cb;
        FUN_b394();
        _DAT_013e = 0xb0ce;
        FUN_b10e();
        _DAT_013e = 0xb0d1;
        FUN_b291();
        FUN_b3a0();
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


// ---- FUN_c9a8 @ c9a8 ----

void FUN_c9a8(void)

{
  return;
}


// ---- FUN_c9a9 @ c9a9 ----

void FUN_c9a9(void)

{
  if (((DAT_0040 & 2) == 0) || ((DAT_00bb & 0x40) != 0)) {
    DAT_00d4 = DAT_00d4 | 0x10;
    DAT_009c = DAT_009c | 0x40;
    DAT_00bc = DAT_00bc | 0x20;
  }
  else {
    DAT_00d4 = DAT_00d4 & 0xef;
    DAT_009c = DAT_009c & 0xbf;
    DAT_00bc = DAT_00bc & 0xdf;
  }
  return;
}


// ---- vec_NMI @ c9c8 ----

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void vec_NMI(void)

{
  DAT_0017 = DAT_0017 ^ 1;
  _DAT_16a1 = 0;
  vec_RESET();
  return;
}


// ---- vec_SWI @ c9d3 ----

void vec_SWI(void)

{
  do {
                    /* WARNING: Do nothing block with infinite loop */
  } while( true );
}


