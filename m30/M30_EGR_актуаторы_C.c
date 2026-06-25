// err c040: java.lang.NullPointerException: Cannot invoke "ghidra.program.model.pcode.Decoder.clear()" because "decoder" is null
// ==== act_c139 @ c139 ====

/* WARNING: Removing unreachable block (RAM,0xc301) */
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void act_c139(void)

{
  bool bVar1;
  byte bVar2;
  byte bVar3;
  undefined2 in_D;
  
  bVar2 = DAT_00a7;
  DAT_1554 = (byte)((ushort)in_D >> 8);
  if ((DAT_1554 < DAT_f795) || ((DAT_1554 <= DAT_1553 && (DAT_f688 <= (byte)(DAT_1553 - DAT_1554))))
     ) {
    DAT_00ca = DAT_00ca & 0xbf;
LAB_c184:
    DAT_1525 = 0;
  }
  else if (0x31 < DAT_1525) {
    DAT_00ab = DAT_00ab | 0x40;
    DAT_004a = DAT_004a | 0x40;
    DAT_00ca = DAT_00ca | 0x40;
    DAT_16b9 = 0;
    goto LAB_c184;
  }
  if ((((DAT_1413 < DAT_f782) || (DAT_f783 <= DAT_1413)) || (DAT_1460 < DAT_f784)) ||
     (DAT_f785 <= DAT_1460)) {
    DAT_00a8 = DAT_00a8 & 0xfe;
    bVar1 = false;
  }
  else {
    DAT_00a8 = DAT_00a8 | 1;
    bVar1 = true;
  }
  if ((((((DAT_1453 < DAT_f780) || (DAT_140c < DAT_f781)) ||
        (((DAT_00c8 & 0x60) != 0 || ((DAT_0088 & 0x80) == 0)))) ||
       (((DAT_009b & 1) == 0 && ((DAT_009b & 8) != 0)))) || ((DAT_00b0 & 8) != 0)) || (!bVar1)) {
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
  bVar3 = DAT_00ca;
  if (((((bVar1) || ((DAT_00c8 & 0x40) != 0)) || ((DAT_00cb & 0x20) != 0)) ||
      ((((DAT_0051 & 0x20) == 0 || (DAT_1453 < DAT_f69a)) ||
       ((DAT_1413 < DAT_f7a2 || ((DAT_f7a3 <= DAT_1413 || (DAT_1460 < DAT_f7a0)))))))) ||
     (DAT_f7a1 <= DAT_1460)) {
    DAT_00a7 = DAT_00a7 & 0xef | 0x40;
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
    DAT_00a7 = DAT_00a7 | 0x50;
    if (DAT_f7a4 <= DAT_152a) {
      _DAT_152b = (_DAT_148e * 2 + _DAT_152b * 3) * 2;
      DAT_00a7 = bVar2 | 0x70;
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
      DAT_00ca = bVar3 & 0x3f;
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


// err bed0: java.lang.NullPointerException: Cannot invoke "ghidra.program.model.pcode.Decoder.clear()" because "decoder" is null
// ==== act_a400 @ a400 ====

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */
/* WARNING: Restarted to delay deadcode elimination for space: register */

void act_a400(undefined1 param_1,undefined1 param_2,short param_3)

{
  undefined2 uVar1;
  undefined2 uVar2;
  byte bVar3;
  char cVar5;
  byte bVar6;
  ushort uVar4;
  byte bVar7;
  
  uVar1 = _DAT_14eb;
  cVar5 = DAT_0080;
  bVar3 = DAT_007f;
  DAT_007f = DAT_007f & 0xfe;
  DAT_0088 = DAT_0088 & 0xbf;
  DAT_0080 = 0;
  if ((DAT_1460 < 100) && ((bVar3 & 0x20) == 0)) {
    _DAT_1461 = (ushort)DAT_ffc5 << 8;
    DAT_00ab = DAT_00ab | 0x10;
    DAT_004a = DAT_004a | 0x10;
    DAT_007f = bVar3 & 0x7e;
    DAT_16bb = 0;
  }
  else {
    for (; cVar5 != '\0'; cVar5 = cVar5 + -1) {
      _DAT_1461 = _DAT_1461 - _DAT_ffb8;
    }
  }
  if ((DAT_00d5 & 0xf) == 0) {
    _DAT_1461 = _DAT_1461 + 0x1a;
  }
  cVar5 = (char)((ushort)_DAT_14eb >> 8);
  _DAT_14c5 = param_3;
  FUN_a473(cVar5,(char)_DAT_14eb,(ushort)DAT_145f << 8);
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
  if (-DAT_1461 == cVar5 || -cVar5 < DAT_1461) {
    if ((char)DAT_14ed < DAT_1461) {
      _DAT_1461 = (ushort)DAT_14ed << 8;
    }
  }
  else {
    _DAT_1461 = (ushort)(byte)-cVar5 << 8;
    if (DAT_145f != 0) {
      DAT_007f = DAT_007f & 0x7f;
    }
  }
  cVar5 = (DAT_1530 - DAT_14aa) + DAT_1461;
  bVar3 = 0x46 - cVar5;
  if ('F' < cVar5) {
    bVar3 = 0;
  }
  bVar7 = DAT_ff8e;
  if ((DAT_f679 <= DAT_14a3) && (DAT_f67a <= DAT_14a2)) {
    bVar7 = DAT_f67b;
  }
  bVar6 = DAT_144d;
  if (DAT_144d < bVar7) {
    bVar6 = 0;
  }
  uVar4 = (ushort)bVar6;
  if (bVar6 <= bVar3) {
    if (((DAT_0053 & 2) == 0) && ((DAT_0059 & 0x40) != 0)) {
      bVar7 = DAT_144d + DAT_ff26;
    }
    else {
      bVar7 = DAT_144d + 10;
    }
    uVar4 = CONCAT11(bVar3,bVar7);
    if (bVar3 < bVar7) goto LAB_a512;
  }
  uVar4 = uVar4 << 8;
LAB_a512:
  DAT_140f = (byte)(uVar4 >> 8);
  if (0x77 < DAT_140f) {
    DAT_140f = 0x77;
  }
  DAT_14ea = DAT_1461 + -0x80;
  return;
}


