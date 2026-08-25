#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Патч v40: загрузчик FM18W08 для записи через UART
Основа: j30_v39_7
"""
import os
from datetime import datetime

SRC = "/Users/remka22/Documents/ЭБУ Максима/1994_Nissan_Maxima_J30_RUS/логер/j30_v39_7_УОЗ-по-детонации-и-форма-столбцов_21.08.26_1210 ИИ.bin"
b = bytearray(open(SRC, 'rb').read())

# Регистры и адреса
TRCSR = 0x0011
RDR = 0x0012
TDR = 0x0013
RDRF = 0x80
TDRE = 0x20

# Рабочие переменные в RAM
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

# Адреса подпрограмм (будут внутри загрузчика)
BASE = 0x45E4
uart_recv_addr = BASE + 0x80
uart_send_addr = BASE + 0xA0
update_chksum_addr = BASE + 0xC0
send_ok_addr = BASE + 0xD0
send_error_addr = BASE + 0xE0

# ============================================================================
# ЗАГРУЗЧИК — машинный код HD6303
# ============================================================================

bootloader = bytearray()

# --- bootloader_entry: проверка RDRF ---
bootloader += bytes([
    0xB6, 0x00, 0x11,        # LDAA $0011 (TRCSR)
    0x84, 0x80,              # ANDA #$80 (RDRF)
    0x27, 0x01,              # BEQ +1 (нет байта -> RTS)
    0x39,                    # RTS
])

# Принять команду
bootloader += bytes([
    0xB6, 0x00, 0x12,        # LDAA $0012 (RDR) - читаем байт команды
    0xB7, CMD >> 8, CMD & 0xFF,  # STAA CMD
    0xB7, CHKSUM >> 8, CHKSUM & 0xFF,  # STAA CHKSUM (начало checksum)
])

# Разбор команды
bootloader += bytes([
    0x81, ord('W'),          # CMPA #'W'
    0x27, 0x05,              # BEQ +5 -> cmd_write
    0x81, ord('P'),          # CMPA #'P'
    0x27, 0x30,              # BEQ +48 -> cmd_ping (примерное смещение)
    0x20, 0x50,              # BRA +80 -> send_error
])

# --- cmd_write ---
cmd_write_start = len(bootloader)

# Принять адрес (2 байта)
bootloader += bytes([
    0xBD, uart_recv_addr >> 8, uart_recv_addr & 0xFF,  # JSR uart_recv
    0xB7, ADDR_HI >> 8, ADDR_HI & 0xFF,  # STAA ADDR_HI
    0xBD, update_chksum_addr >> 8, update_chksum_addr & 0xFF,  # JSR update_chksum

    0xBD, uart_recv_addr >> 8, uart_recv_addr & 0xFF,  # JSR uart_recv
    0xB7, ADDR_LO >> 8, ADDR_LO & 0xFF,  # STAA ADDR_LO
    0xBD, update_chksum_addr >> 8, update_chksum_addr & 0xFF,  # JSR update_chksum
])

# Принять длину (2 байта)
bootloader += bytes([
    0xBD, uart_recv_addr >> 8, uart_recv_addr & 0xFF,  # JSR uart_recv
    0xB7, LEN_HI >> 8, LEN_HI & 0xFF,  # STAA LEN_HI
    0xBD, update_chksum_addr >> 8, update_chksum_addr & 0xFF,  # JSR update_chksum

    0xBD, uart_recv_addr >> 8, uart_recv_addr & 0xFF,  # JSR uart_recv
    0xB7, LEN_LO >> 8, LEN_LO & 0xFF,  # STAA LEN_LO
    0xBD, update_chksum_addr >> 8, update_chksum_addr & 0xFF,  # JSR update_chksum
])

# Инициализация указателя и счётчика
bootloader += bytes([
    0xB6, ADDR_HI >> 8, ADDR_HI & 0xFF,  # LDAA ADDR_HI
    0xB7, PTR_HI >> 8, PTR_HI & 0xFF,    # STAA PTR_HI
    0xB6, ADDR_LO >> 8, ADDR_LO & 0xFF,  # LDAA ADDR_LO
    0xB7, PTR_LO >> 8, PTR_LO & 0xFF,    # STAA PTR_LO

    0xB6, LEN_HI >> 8, LEN_HI & 0xFF,    # LDAA LEN_HI
    0xB7, COUNT_HI >> 8, COUNT_HI & 0xFF,  # STAA COUNT_HI
    0xB6, LEN_LO >> 8, LEN_LO & 0xFF,    # LDAA LEN_LO
    0xB7, COUNT_LO >> 8, COUNT_LO & 0xFF,  # STAA COUNT_LO
])

# write_loop
write_loop_start = len(bootloader)
bootloader += bytes([
    # Проверить счётчик
    0xB6, COUNT_HI >> 8, COUNT_HI & 0xFF,  # LDAA COUNT_HI
    0x9A, COUNT_LO & 0xFF,                 # ORAA COUNT_LO (direct mode)
    0x27, 0x20,                            # BEQ +32 -> write_done

    # Принять байт данных
    0xBD, uart_recv_addr >> 8, uart_recv_addr & 0xFF,  # JSR uart_recv
    0xBD, update_chksum_addr >> 8, update_chksum_addr & 0xFF,  # JSR update_chksum

    # Записать в память (КРИТИЧНО: запись через LDX/STAA)
    0x36,                                  # PSHA (сохранить данные)
    0xDE, PTR_HI & 0xFF,                   # LDX PTR_HI (direct mode)
    0x32,                                  # PULA
    0xA7, 0x00,                            # STAA 0,X (запись в FM18W08!)

    # Увеличить указатель
    0xDE, PTR_HI & 0xFF,                   # LDX PTR_HI
    0x08,                                  # INX
    0xDF, PTR_HI & 0xFF,                   # STX PTR_HI

    # Уменьшить счётчик
    0xDE, COUNT_HI & 0xFF,                 # LDX COUNT_HI
    0x09,                                  # DEX
    0xDF, COUNT_HI & 0xFF,                 # STX COUNT_HI

    0x20, write_loop_start - len(bootloader) - 2 & 0xFF,  # BRA write_loop (relative)
])

# write_done: проверить checksum
write_done_start = len(bootloader)
bootloader += bytes([
    0xBD, uart_recv_addr >> 8, uart_recv_addr & 0xFF,  # JSR uart_recv (checksum от ПК)
    0x91, CHKSUM & 0xFF,                               # CMPA CHKSUM (direct)
    0x26, 0x05,                                        # BNE +5 -> send_error
    0x20, send_ok_addr - (BASE + len(bootloader)) - 2 & 0xFF,  # BRA send_ok
])

# --- cmd_ping ---
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

# --- uart_recv (0x45E4 + 0x80) ---
while len(bootloader) < 0x80:
    bootloader.append(0x00)
bootloader += bytes([
    0xB6, 0x00, 0x11,        # LDAA $0011 (TRCSR)
    0x84, 0x80,              # ANDA #$80 (RDRF)
    0x27, 0xFA,              # BEQ -6 (busy-wait)
    0xB6, 0x00, 0x12,        # LDAA $0012 (RDR)
    0x39,                    # RTS
])

# --- uart_send (0x45E4 + 0xA0) ---
while len(bootloader) < 0xA0:
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

# --- update_chksum (0x45E4 + 0xC0) ---
while len(bootloader) < 0xC0:
    bootloader.append(0x00)
bootloader += bytes([
    0x98, CHKSUM & 0xFF,     # EORA CHKSUM (direct)
    0x97, CHKSUM & 0xFF,     # STAA CHKSUM
    0x39,                    # RTS
])

# --- send_ok (0x45E4 + 0xD0) ---
while len(bootloader) < 0xD0:
    bootloader.append(0x00)
bootloader += bytes([
    0x86, ord('O'),          # LDAA #'O'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x86, ord('K'),          # LDAA #'K'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x86, 0x0A,              # LDAA #'\n'
    0xBD, uart_send_addr >> 8, uart_send_addr & 0xFF,
    0x39,                    # RTS
])

# --- send_error (0x45E4 + 0xE0) ---
while len(bootloader) < 0xE0:
    bootloader.append(0x00)
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

# ============================================================================
# ВПАТЧИТЬ В ПРОШИВКУ
# ============================================================================

# Загрузчик по адресу 0x45E4
for i, byte in enumerate(bootloader):
    if BASE + i < len(b):
        b[BASE + i] = byte

print(f"Загрузчик: {len(bootloader)} байт по адресу 0x{BASE:04X}")

# TODO: Найти главный цикл и добавить вызов JSR $45E4
# Пока оставляю без автовызова - требуется ручной анализ дизассемблера

# ============================================================================
# СОХРАНИТЬ
# ============================================================================

T = datetime.now().strftime("%d.%m.%y_%H%M")
VER = 40
DST = f"/Users/remka22/Documents/ЭБУ Максима/1994_Nissan_Maxima_J30_RUS/логер/j30_v{VER}_загрузчик-FM18W08_{T} ИИ.bin"
open(DST, 'wb').write(bytes(b))

# Проверка
a = open(SRC, 'rb').read()
diff = sum(1 for i in range(len(b)) if b[i] != a[i])
print(f"\nСоздан: {os.path.basename(DST)}")
print(f"Размер: {len(b)} байт")
print(f"Изменено байт: {diff}")
print(f"Зона патча: 0x{BASE:04X}–0x{BASE + len(bootloader):04X}")
print("\n⚠ ВНИМАНИЕ: автовызов загрузчика НЕ добавлен")
print("Требуется вручную найти idle loop и добавить JSR $45E4")
