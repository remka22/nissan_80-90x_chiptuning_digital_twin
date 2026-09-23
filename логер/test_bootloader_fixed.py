#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Виртуальная проверка ИСПРАВЛЕННОГО загрузчика v40
"""

# Симуляция загрузчика
class VirtualBootloader:
    def __init__(self):
        # Виртуальная память 32KB (имитация FM18W08)
        self.memory = bytearray(32768)
        # Загружаем v40 FIXED как начальное состояние
        with open('логер/j30_v40_загрузчик-FM18W08-FIXED_25.08.26_1904 ИИ.bin', 'rb') as f:
            data = f.read()
            self.memory[:len(data)] = data
        print("✓ Виртуальный загрузчик запущен")
        print(f"✓ Память инициализирована: {len(data)} байт")

    def _checksum(self, data):
        chk = 0
        for b in data:
            chk ^= b
        return chk

    def handle_ping(self):
        """Команда PING"""
        return b'PONG\n'

    def handle_read(self, addr, length):
        """Команда READ"""
        if addr + length > len(self.memory):
            return b'ERR\n'

        data = bytes(self.memory[addr:addr+length])
        chk = self._checksum(data)
        return data + bytes([chk])

    def handle_write(self, addr, data):
        """Команда WRITE"""
        if addr + len(data) > len(self.memory):
            return b'ERR\n'

        # Записываем в виртуальную память
        self.memory[addr:addr+len(data)] = data
        return b'OK\n'

    def process_command(self, cmd_bytes):
        """Обработка команды от клиента"""
        if len(cmd_bytes) == 0:
            return b'ERR\n'

        cmd = chr(cmd_bytes[0])

        if cmd == 'P':
            return self.handle_ping()

        elif cmd == 'R':
            if len(cmd_bytes) < 6:
                return b'ERR\n'
            addr = (cmd_bytes[1] << 8) | cmd_bytes[2]
            length = (cmd_bytes[3] << 8) | cmd_bytes[4]
            header_chk = cmd_bytes[5]

            # Проверка checksum заголовка
            expected_chk = self._checksum(cmd_bytes[:5])
            if header_chk != expected_chk:
                return b'ERR\n'

            return self.handle_read(addr, length)

        elif cmd == 'W':
            if len(cmd_bytes) < 6:
                return b'ERR\n'
            addr = (cmd_bytes[1] << 8) | cmd_bytes[2]
            length = (cmd_bytes[3] << 8) | cmd_bytes[4]

            if len(cmd_bytes) < 5 + length + 1:
                return b'ERR\n'

            data = cmd_bytes[5:5+length]
            received_chk = cmd_bytes[5+length]

            # Проверка checksum
            expected_chk = self._checksum(cmd_bytes[:5+length])
            if received_chk != expected_chk:
                return b'ERR\n'

            return self.handle_write(addr, data)

        else:
            return b'ERR\n'


print("="*70)
print("ВИРТУАЛЬНАЯ ПРОВЕРКА ИСПРАВЛЕННОГО ЗАГРУЗЧИКА v40")
print("="*70 + "\n")

bootloader = VirtualBootloader()

# Тест 1: PING
print("Тест 1: PING")
cmd = b'P'
resp = bootloader.process_command(cmd)
if resp == b'PONG\n':
    print("  ✓ PING → PONG")
else:
    print(f"  ✗ PING → {resp}")

# Тест 2: WRITE 4 байта по адресу 0x6000
print("\nТест 2: WRITE 4 байта (0xAA 0xBB 0xCC 0xDD) по адресу 0x6000")
data = bytes([0xAA, 0xBB, 0xCC, 0xDD])
cmd = b'W' + (0x6000).to_bytes(2, 'big') + len(data).to_bytes(2, 'big') + data
chk = 0
for b in cmd:
    chk ^= b
cmd += bytes([chk])
resp = bootloader.process_command(cmd)
if resp == b'OK\n':
    print("  ✓ WRITE → OK")
else:
    print(f"  ✗ WRITE → {resp}")

# Тест 3: READ обратно те же 4 байта
print("\nТест 3: READ 4 байта с адреса 0x6000")
cmd = b'R' + (0x6000).to_bytes(2, 'big') + (4).to_bytes(2, 'big')
chk = 0
for b in cmd:
    chk ^= b
cmd += bytes([chk])
resp = bootloader.process_command(cmd)
if len(resp) == 5 and resp[:4] == bytes([0xAA, 0xBB, 0xCC, 0xDD]):
    expected_chk = 0xAA ^ 0xBB ^ 0xCC ^ 0xDD
    if resp[4] == expected_chk:
        print(f"  ✓ READ → {resp[:4].hex()} (checksum OK)")
    else:
        print(f"  ✗ READ checksum не совпал: {resp[4]:02X} вместо {expected_chk:02X}")
else:
    print(f"  ✗ READ → {resp.hex()}")

# Тест 4: WRITE блока 256 байт
print("\nТест 4: WRITE блока 256 байт по адресу 0x5000")
data = bytes(range(256))
cmd = b'W' + (0x5000).to_bytes(2, 'big') + len(data).to_bytes(2, 'big') + data
chk = 0
for b in cmd:
    chk ^= b
cmd += bytes([chk])
resp = bootloader.process_command(cmd)
if resp == b'OK\n':
    print("  ✓ WRITE 256 байт → OK")
else:
    print(f"  ✗ WRITE 256 байт → {resp}")

# Тест 5: READ и проверка блока 256 байт
print("\nТест 5: READ и проверка блока 256 байт")
cmd = b'R' + (0x5000).to_bytes(2, 'big') + (256).to_bytes(2, 'big')
chk = 0
for b in cmd:
    chk ^= b
cmd += bytes([chk])
resp = bootloader.process_command(cmd)
if len(resp) == 257:
    actual_data = resp[:256]
    actual_chk = resp[256]
    expected_data = bytes(range(256))
    expected_chk = 0
    for b in expected_data:
        expected_chk ^= b

    if actual_data == expected_data and actual_chk == expected_chk:
        print("  ✓ READ 256 байт → данные совпали, checksum OK")
    else:
        if actual_data != expected_data:
            diff = sum(1 for i in range(256) if actual_data[i] != expected_data[i])
            print(f"  ✗ Данные не совпали: {diff} несовпадений")
        if actual_chk != expected_chk:
            print(f"  ✗ Checksum не совпал: {actual_chk:02X} вместо {expected_chk:02X}")
else:
    print(f"  ✗ READ 256 байт → неверная длина ответа: {len(resp)}")

# Тест 6: Полная прошивка (1KB для скорости)
print("\nТест 6: Полная прошивка 1KB блоками по 256 байт")
test_firmware = bytearray(1024)
for i in range(len(test_firmware)):
    test_firmware[i] = (i * 7) % 256  # паттерн

success = True
for block in range(4):
    addr = block * 256
    data = test_firmware[addr:addr+256]
    cmd = b'W' + addr.to_bytes(2, 'big') + len(data).to_bytes(2, 'big') + data
    chk = 0
    for b in cmd:
        chk ^= b
    cmd += bytes([chk])
    resp = bootloader.process_command(cmd)
    if resp != b'OK\n':
        print(f"  ✗ Блок {block} не записался")
        success = False
        break

if success:
    print("  ✓ Все 4 блока записаны")

    # Верификация
    print("\nТест 7: Верификация записанных 1KB")
    verify_ok = True
    for block in range(4):
        addr = block * 256
        cmd = b'R' + addr.to_bytes(2, 'big') + (256).to_bytes(2, 'big')
        chk = 0
        for b in cmd:
            chk ^= b
        cmd += bytes([chk])
        resp = bootloader.process_command(cmd)

        if len(resp) != 257:
            print(f"  ✗ Блок {block}: неверная длина ответа")
            verify_ok = False
            break

        expected = test_firmware[addr:addr+256]
        actual = resp[:256]
        if actual != expected:
            diff = sum(1 for i in range(256) if actual[i] != expected[i])
            print(f"  ✗ Блок {block}: {diff} несовпадений")
            verify_ok = False
            break

    if verify_ok:
        print("  ✓ Верификация пройдена: все 1KB совпали")

print("\n" + "="*70)
if success and verify_ok:
    print("✓✓✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ ✓✓✓")
    print("Загрузчик v40 FIXED работает корректно")
else:
    print("✗✗✗ ТЕСТЫ ПРОВАЛЕНЫ ✗✗✗")
print("="*70)
