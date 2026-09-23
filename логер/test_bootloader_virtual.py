#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Виртуальная проверка загрузчика v40 и прошивальщика
Симулирует работу загрузчика на уровне протокола
"""
import sys
sys.path.insert(0, '.')

# Симуляция загрузчика
class VirtualBootloader:
    def __init__(self):
        # Виртуальная память 32KB (имитация FM18W08)
        self.memory = bytearray(32768)
        # Загружаем v40 как начальное состояние
        with open('логер/j30_v40_загрузчик-FM18W08_25.08.26_1704 ИИ.bin', 'rb') as f:
            data = f.read()
            self.memory[:len(data)] = data
        print("Виртуальный загрузчик запущен")
        print(f"Память инициализирована: {len(data)} байт")

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
                print(f"  ✗ READ checksum не совпал: ожидали 0x{expected_chk:02X}, получили 0x{header_chk:02X}")
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
                print(f"  ✗ WRITE checksum не совпал: ожидали 0x{expected_chk:02X}, получили 0x{received_chk:02X}")
                return b'ERR\n'

            return self.handle_write(addr, data)

        else:
            return b'ERR\n'


# Виртуальный serial порт
class VirtualSerial:
    def __init__(self, bootloader):
        self.bootloader = bootloader
        self.tx_buffer = bytearray()
        self.rx_buffer = bytearray()

    def write(self, data):
        """Отправка данных в загрузчик"""
        self.tx_buffer.extend(data)

        # Обработка команды (упрощённо: считаем что вся команда пришла сразу)
        response = self.bootloader.process_command(bytes(self.tx_buffer))
        self.rx_buffer.extend(response)
        self.tx_buffer.clear()

    def read(self, size):
        """Чтение ответа от загрузчика"""
        if len(self.rx_buffer) < size:
            # В реальности был бы timeout, тут возвращаем что есть
            result = bytes(self.rx_buffer)
            self.rx_buffer.clear()
            return result

        result = bytes(self.rx_buffer[:size])
        self.rx_buffer = self.rx_buffer[size:]
        return result

    def close(self):
        pass


# Патчим serial для виртуальной проверки
import serial as real_serial

class MockSerial:
    def __init__(self, port, baud, timeout):
        print(f"[MOCK] Подключение к виртуальному загрузчику (вместо {port})")
        self.bootloader = VirtualBootloader()
        self.vserial = VirtualSerial(self.bootloader)

    def write(self, data):
        return self.vserial.write(data)

    def read(self, size):
        return self.vserial.read(size)

    def close(self):
        return self.vserial.close()

# Подменяем serial.Serial
real_serial.Serial = MockSerial

# Запускаем прошивальщик
print("\n" + "="*60)
print("ВИРТУАЛЬНАЯ ПРОВЕРКА ЗАГРУЗЧИКА И ПРОШИВАЛЬЩИКА")
print("="*60 + "\n")

# Импортируем прошивальщик
import importlib.util
spec = importlib.util.spec_from_file_location("flash_j30", "логер/flash_j30.py")
flash_module = importlib.util.module_from_spec(spec)

# Создаём тестовый .bin (небольшой, для скорости)
import os
test_bin = '/tmp/test_firmware.bin'
test_data = bytearray(1024)  # 1KB для теста
for i in range(len(test_data)):
    test_data[i] = i % 256
with open(test_bin, 'wb') as f:
    f.write(test_data)

print(f"Создан тестовый .bin: {len(test_data)} байт\n")

# Запускаем прошивку
sys.argv = ['flash_j30.py', test_bin, '--no-reset']

try:
    spec.loader.exec_module(flash_module)
except SystemExit as e:
    if e.code == 0:
        print("\n" + "="*60)
        print("✓ ВИРТУАЛЬНАЯ ПРОВЕРКА ПРОЙДЕНА")
        print("="*60)

        # Дополнительная проверка: читаем память напрямую
        bootloader = MockSerial('', 0, 0).bootloader
        written = bytes(bootloader.memory[:len(test_data)])

        if written == test_data:
            print("\n✓ Данные в виртуальной памяти совпадают с записанными")
        else:
            diff = sum(1 for i in range(len(test_data)) if written[i] != test_data[i])
            print(f"\n✗ Найдено {diff} несовпадений в виртуальной памяти")
    else:
        print("\n✗ ВИРТУАЛЬНАЯ ПРОВЕРКА ПРОВАЛЕНА")
        sys.exit(1)
