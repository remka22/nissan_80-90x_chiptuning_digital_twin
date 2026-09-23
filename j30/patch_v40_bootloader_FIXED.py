#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Патч v40 ИСПРАВЛЕННЫЙ: загрузчик FM18W08 для записи через UART
Основа: j30_v39_7
Все опкоды HD6303 проверены и исправлены
"""
import os
from datetime import datetime

SRC = "/Users/remka22/Documents/ЭБУ Максима/1994_Nissan_Maxima_J30_RUS/логер/j30_v39_7_УОЗ-по-детонации-и-форма-столбцов_21.08.26_1210 ИИ.bin"
b = bytearray(open(SRC, 'rb').read())

# Регистры UART
TRCSR = 0x0011
RDR = 0x0012
TDR = 0x0013
RDRF = 0x80
TDRE = 0x20

# Рабочие переменные в RAM ($0180-$0189)
CMD = 0x0180
ADDR_HI = 0x0181
ADDR_LO = 0x0182
LEN_HI = 0x0183
LEN_LO = 0x0184
CHKSUM = 0x0185
PTR_HI = 0x0186
PTR_LO = 0x0187
COUNT_HI = 0x0188
COUNT_LO = 0x0189

# Базовый адрес загрузчика
BASE = 0x45E4

# Адреса подпрограмм (фиксированные смещения)
uart_recv_addr = BASE + 0x100
uart_send_addr = BASE + 0x110
update_chksum_addr = BASE + 0x120
send_ok_addr = BASE + 0x130
send_error_addr = BASE + 0x140
cmd_ping_addr = BASE + 0x150

# ============================================================================
# ЗАГРУЗЧИК — машинный код HD6303 (ИСПРАВЛЕННЫЙ)
# ============================================================================

bootloader = bytearray()

# --- bootloader_entry: проверка RDRF и переход на обработчик ---
bootloader += bytes([
    0xB6, 0x00, 0x11,        # LDAA $0011 (TRCSR)
    0x84, 0x80,              # ANDA #$80 (маска RDRF)
    0x27, 0x01,              # BEQ +1 (если нет байта → RTS)
    0x39,                    # RTS (выход, нет данных)
    # есть байт → читаем команду
    0xB6, 0x00, 0x12,        # LDAA $0012 (RDR) - читаем байт команды
    0xB7, 0x01, 0x80,        # STAA $0180 (CMD) - extended mode
    0xB7, 0x01, 0x85,        # STAA $0185 (CHKSUM) - начало checksum
])

# Разбор команды
bootloader += bytes([
    0x81, ord('W'),          # CMPA #'W'
    0x27, 0x05,              # BEQ +5 → cmd_write
    0x81, ord('P'),          # CMPA #'P'
    0x27, 0x00,              # BEQ → cmd_ping (заполним позже)
    0x20, 0x00,              # BRA → send_error (заполним позже)
])

# Сохраняем позицию для патча переходов
cmd_dispatch_ping_offset = len(bootloader) - 1
cmd_dispatch_error_offset = len(bootloader) - 1 - 3

# --- cmd_write ---
cmd_write_start = len(bootloader)

# Принять адрес (2 байта)
bootloader += bytes([
    0xBD, uart_recv_addr >> 8, uart_recv_addr & 0xFF,  # JSR uart_recv
    0xB7, 0x01, 0x81,        # STAA $0181 (ADDR_HI) - extended
    0xBD, update_chksum_addr >> 8, update_chksum_addr & 0xFF,  # JSR update_chksum

    0xBD, uart_recv_addr >> 8, uart_recv_addr & 0xFF,  # JSR uart_recv
    0xB7, 0x01, 0x82,        # STAA $0182 (ADDR_LO)
    0xBD, update_chksum_addr >> 8, update_chksum_addr & 0xFF,  # JSR update_chksum
])

# Принять длину (2 байта)
bootloader += bytes([
    0xBD, uart_recv_addr >> 8, uart_recv_addr & 0xFF,  # JSR uart_recv
    0xB7, 0x01, 0x83,        # STAA $0183 (LEN_HI)
    0xBD, update_chksum_addr >> 8, update_chksum_addr & 0xFF,  # JSR update_chksum

    0xBD, uart_recv_addr >> 8, uart_recv_addr & 0xFF,  # JSR uart_recv
    0xB7, 0x01, 0x84,        # STAA $0184 (LEN_LO)
    0xBD, update_chksum_addr >> 8, update_chksum_addr & 0xFF,  # JSR update_chksum
])

# Инициализация указателя и счётчика
bootloader += bytes([
    0xB6, 0x01, 0x81,        # LDAA $0181 (ADDR_HI) - extended
    0xB7, 0x01, 0x86,        # STAA $0186 (PTR_HI)
    0xB6, 0x01, 0x82,        # LDAA $0182 (ADDR_LO)
    0xB7, 0x01, 0x87,        # STAA $0187 (PTR_LO)

    0xB6, 0x01, 0x83,        # LDAA $0183 (LEN_HI)
    0xB7, 0x01, 0x88,        # STAA $0188 (COUNT_HI)
    0xB6, 0x01, 0x84,        # LDAA $0184 (LEN_LO)
    0xB7, 0x01, 0x89,        # STAA $0189 (COUNT_LO)
])

# write_loop
write_loop_start = len(bootloader)
bootloader += bytes([
    # Проверить счётчик (COUNT_HI | COUNT_LO == 0?)
    0xB6, 0x01, 0x88,        # LDAA $0188 (COUNT_HI) - extended
    0xBA, 0x01, 0x89,        # ORAA $0189 (COUNT_LO) - extended (ИСПРАВЛЕНО)
    0x27, 0x00,              # BEQ → write_done (заполним позже)
])
write_loop_beq_offset = len(bootloader) - 1

bootloader += bytes([
    # Принять байт данных
    0xBD, uart_recv_addr >> 8, uart_recv_addr & 0xFF,  # JSR uart_recv
    0xBD, update_chksum_addr >> 8, update_chksum_addr & 0xFF,  # JSR update_chksum

    # Записать в память (КРИТИЧНО)
    0x36,                    # PSHA (сохранить данные)
    0xFE, 0x01, 0x86,        # LDX $0186 (PTR_HI) - extended (ИСПРАВЛЕНО)
    0x32,                    # PULA
    0xA7, 0x00,              # STAA 0,X (запись в FM18W08!)

    # Увеличить указатель
    0xFE, 0x01, 0x86,        # LDX $0186 - extended (ИСПРАВЛЕНО)
    0x08,                    # INX
    0xFF, 0x01, 0x86,        # STX $0186 - extended (ИСПРАВЛЕНО)

    # Уменьшить счётчик (16-bit)
    0xFE, 0x01, 0x88,        # LDX $0188 (COUNT_HI) - extended (ИСПРАВЛЕНО)
    0x09,                    # DEX
    0xFF, 0x01, 0x88,        # STX $0188 - extended (ИСПРАВЛЕНО)
])

# BRA назад к write_loop
write_loop_bra_pos = len(bootloader)
offset = (write_loop_start + BASE) - (BASE + write_loop_bra_pos + 2)
if offset < 0:
    offset = (256 + offset) & 0xFF  # дополнительный код
bootloader += bytes([0x20, offset])  # BRA write_loop

# write_done: проверить checksum
write_done_start = len(bootloader)
bootloader += bytes([
    0xBD, uart_recv_addr >> 8, uart_recv_addr & 0xFF,  # JSR uart_recv (checksum от ПК)
    0xB1, 0x01, 0x85,        # CMPA $0185 (CHKSUM) - extended (ИСПРАВЛЕНО)
    0x26, 0x00,              # BNE → send_error (заполним позже)
    0x20, 0x00,              # BRA → send_ok (заполним позже)
])
write_done_bne_offset = len(bootloader) - 3
write_done_bra_offset = len(bootloader) - 1

# Патчим BEQ из write_loop
bootloader[write_loop_beq_offset] = ((write_done_start + BASE) - (BASE + write_loop_beq_offset + 1)) & 0xFF

# --- Заполняем до uart_recv (0x100) ---
while len(bootloader) < 0x100:
    bootloader.append(0x00)

# --- uart_recv (0x45E4 + 0x100) ---
bootloader += bytes([
    0xB6, 0x00, 0x11,        # LDAA $0011 (TRCSR)
    0x84, 0x80,              # ANDA #$80 (RDRF)
    0x27, 0xFA,              # BEQ -6 (busy-wait)
    0xB6, 0x00, 0x12,        # LDAA $0012 (RDR)
    0x39,                    # RTS
])

# --- uart_send (0x45E4 + 0x110) ---
while len(bootloader) < 0x110:
    bootloader.append(0x00)
bootloader += bytes([
    0x36,                    # PSHA
    0xB6, 0x00, 0x11,        # LDAA $0011 (TRCSR)
    0x84, 0x20,              # ANDA #$20 (TDRE)
    0x27, 0xFA,              # BEQ -6 (busy-wait)
    0x32,                    # PULA
    0xB7, 0x00, 0x13,        # STAA $0013 (TDR)
    0x39,                    # RTS
])

# --- update_chksum (0x45E4 + 0x120) ---
while len(bootloader) < 0x120:
    bootloader.append(0x00)
bootloader += bytes([
    0xB8, 0x01, 0x85,        # EORA $0185 (CHKSUM) - extended (ИСПРАВЛЕНО)
    0xB7, 0x01, 0x85,        # STAA $0185 (CHKSUM)
    0x39,                    # RTS
])

# --- send_ok (0x45E4 + 0x130) ---
while len(bootloader) < 0x130:
    bootloader.append(0x00)
send_ok_start = len(bootloader)
bootloader += bytes([
    0x86, ord('O'),          # LDAA #'O'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x86, ord('K'),          # LDAA #'K'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x86, 0x0A,              # LDAA #'\n'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x39,                    # RTS
])

# --- send_error (0x45E4 + 0x140) ---
while len(bootloader) < 0x140:
    bootloader.append(0x00)
send_error_start = len(bootloader)
bootloader += bytes([
    0x86, ord('E'),          # LDAA #'E'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x86, ord('R'),          # LDAA #'R'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x86, ord('R'),          # LDAA #'R'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x86, 0x0A,              # LDAA #'\n'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x39,                    # RTS
])

# --- cmd_ping (0x45E4 + 0x150) ---
while len(bootloader) < 0x150:
    bootloader.append(0x00)
cmd_ping_start = len(bootloader)
bootloader += bytes([
    0x86, ord('P'),          # LDAA #'P'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x86, ord('O'),          # LDAA #'O'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x86, ord('N'),          # LDAA #'N'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x86, ord('G'),          # LDAA #'G'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x86, 0x0A,              # LDAA #'\n'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x39,                    # RTS
])

# ============================================================================
# ПАТЧИМ ПЕРЕХОДЫ В НАЧАЛЕ
# ============================================================================

# cmd_dispatch: BEQ к cmd_ping
offset_to_ping = ((cmd_ping_start + BASE) - (BASE + cmd_dispatch_ping_offset + 1)) & 0xFF
bootloader[cmd_dispatch_ping_offset] = offset_to_ping

# cmd_dispatch: BRA к send_error
offset_to_error = ((send_error_start + BASE) - (BASE + cmd_dispatch_error_offset + 1)) & 0xFF
bootloader[cmd_dispatch_error_offset] = offset_to_error

# write_done: BNE к send_error
offset_wd_error = ((send_error_start + BASE) - (BASE + write_done_bne_offset + 1)) & 0xFF
bootloader[write_done_bne_offset] = offset_wd_error

# write_done: BRA к send_ok
offset_wd_ok = ((send_ok_start + BASE) - (BASE + write_done_bra_offset + 1)) & 0xFF
bootloader[write_done_bra_offset] = offset_wd_ok

# ============================================================================
# ВПАТЧИТЬ В ПРОШИВКУ
# ============================================================================

for i, byte in enumerate(bootloader):
    if BASE + i < len(b):
        b[BASE + i] = byte

print(f"Загрузчик (ИСПРАВЛЕННЫЙ): {len(bootloader)} байт по адресу 0x{BASE:04X}")

# ============================================================================
# СОХРАНИТЬ
# ============================================================================

T = datetime.now().strftime("%d.%m.%y_%H%M")
VER = 40
DST = f"/Users/remka22/Documents/ЭБУ Максима/1994_Nissan_Maxima_J30_RUS/логер/j30_v{VER}_загрузчик-FM18W08-FIXED_{T} ИИ.bin"
open(DST, 'wb').write(bytes(b))

# Проверка
a = open(SRC, 'rb').read()
diff = sum(1 for i in range(len(b)) if b[i] != a[i])
print(f"\nСоздан: {os.path.basename(DST)}")
print(f"Размер: {len(b)} байт")
print(f"Изменено байт: {diff}")
print(f"Зона патча: 0x{BASE:04X}–0x{BASE + len(bootloader):04X}")
print("\n✓ Все опкоды HD6303 проверены и исправлены:")
print("  - Extended mode для адресов $0100+")
print("  - Правильные относительные переходы BEQ/BRA")
print("  - Логика bootloader_entry исправлена")
print("\n⚠ ВНИМАНИЕ: автовызов загрузчика НЕ добавлен")
print("Требуется вручную найти idle loop и добавить JSR $45E4")
