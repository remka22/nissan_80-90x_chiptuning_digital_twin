#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Компилятор загрузчика FM18W08 для HD6303
Переводит ассемблер в машинный код и патчит прошивку
"""

# Опкоды HD6303 (неполный набор, только используемые)
opcodes = {
    'LDAA_IMM': 0x86,    # LDAA #imm
    'LDAA_DIR': 0x96,    # LDAA addr
    'LDAA_EXT': 0xB6,    # LDAA addr16
    'LDAA_IDX': 0xA6,    # LDAA 0,X
    'STAA_DIR': 0x97,    # STAA addr
    'STAA_EXT': 0xB7,    # STAA addr16
    'STAA_IDX': 0xA7,    # STAA 0,X
    'LDX_IMM':  0xCE,    # LDX #imm16
    'LDX_DIR':  0xDE,    # LDX addr
    'STX_DIR':  0xDF,    # STX addr
    'INX':      0x08,    # INX
    'DEX':      0x09,    # DEX
    'ANDA_IMM': 0x84,    # ANDA #imm
    'EORA_DIR': 0x98,    # EORA addr
    'ORAA_DIR': 0x9A,    # ORAA addr
    'CMPA_IMM': 0x81,    # CMPA #imm
    'CMPA_DIR': 0x91,    # CMPA addr
    'BEQ':      0x27,    # BEQ rel
    'BNE':      0x26,    # BNE rel
    'BRA':      0x20,    # BRA rel
    'JSR':      0xBD,    # JSR addr16
    'RTS':      0x39,    # RTS
    'JMP_EXT':  0x7E,    # JMP addr16
    'JMP_IDX':  0x6E,    # JMP [$addr]
    'PSHA':     0x36,    # PSHA
    'PULA':     0x32,    # PULA
    'CLR_DIR':  0x7F,    # CLR addr
}

# Адреса регистров и переменных
TRCSR   = 0x0011
RDR     = 0x0012
TDR     = 0x0013
RDRF    = 0x80
TDRE    = 0x20

WORK    = 0x0180
CMD     = WORK + 0
ADDR_HI = WORK + 1
ADDR_LO = WORK + 2
LEN_HI  = WORK + 3
LEN_LO  = WORK + 4
CHKSUM  = WORK + 5
PTR_HI  = WORK + 6
PTR_LO  = WORK + 7
COUNT_HI= WORK + 8
COUNT_LO= WORK + 9

# Упрощённая компиляция основных функций в машинный код
# Полная компиляция требует полноценного ассемблера, делаю ключевые части

def compile_bootloader():
    """
    Компилирует загрузчик в машинный код
    Упрощённая версия — только критические функции
    """
    code = bytearray()

    # bootloader_entry: проверка RDRF
    code += bytes([
        opcodes['LDAA_EXT'], 0x00, 0x11,        # LDAA TRCSR ($0011)
        opcodes['ANDA_IMM'], RDRF,              # ANDA #$80
        opcodes['BEQ'], 0x03,                   # BEQ +3 (пропустить RTS)
        opcodes['JMP_EXT'], 0x45, 0xF0,         # JMP cmd_parser (заглушка)
        opcodes['RTS'],                         # RTS
    ])

    return bytes(code)

# Основной патч — вызов загрузчика из главного цикла
def patch_firmware(src_bin, dst_bin):
    """
    Патчит прошивку: добавляет загрузчик и вызов из главного цикла
    """
    with open(src_bin, 'rb') as f:
        firmware = bytearray(f.read())

    # ВНИМАНИЕ: это заглушка для демонстрации структуры
    # Полная компиляция требует as6303 или ручной трансляции всех 250 байт

    print("ПРЕДУПРЕЖДЕНИЕ: автоматическая компиляция HD6303 ASM не реализована")
    print("Требуется:")
    print("1. Установить ассемблер as6303 или ASL")
    print("2. Скомпилировать bootloader_fm18w08.asm -> bootloader.bin")
    print("3. Впатчить вручную:")
    print("   - Загрузчик по адресу 0x45E4")
    print("   - Вызов JSR $45E4 в главный цикл (найти idle loop)")
    print("   - Пересчитать checksum")

    return None

if __name__ == '__main__':
    print("Компилятор загрузчика FM18W08 для J30")
    print("=" * 60)

    src = "логер/j30_v39_7_УОЗ-по-детонации-и-форма-столбцов_21.08.26_1210 ИИ.bin"
    dst = "логер/j30_v40_загрузчик-FM18W08_21.08.26_xxxx ИИ.bin"

    result = patch_firmware(src, dst)

    if result is None:
        print("\nДля завершения патча требуется:")
        print("1. Скомпилировать j30/bootloader_fm18w08.asm")
        print("2. Найти idle loop в v39_7 (адрес основного цикла)")
        print("3. Впатчить вызов загрузчика")
        print("4. Пересчитать контрольную сумму")
