#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Прошивальщик J30 через FM18W08 + загрузчик v40+
Отправляет .bin файл в ЭБУ через UART (FT232/ESP32)
"""
import serial
import time
import sys
import os
from pathlib import Path

# Настройки UART
PORT = '/dev/tty.usbserial-0001'  # FT232 или ESP32 (меняй на свой)
BAUD = 9600
TIMEOUT = 1.0

# Размер блока записи (байт)
BLOCK_SIZE = 256

class BootloaderClient:
    def __init__(self, port, baud):
        self.ser = serial.Serial(port, baud, timeout=TIMEOUT)
        time.sleep(0.5)  # ждём инициализации
        print(f"Подключено к {port} на {baud} baud")

    def _checksum(self, data):
        """XOR всех байтов"""
        chk = 0
        for b in data:
            chk ^= b
        return chk

    def ping(self):
        """Проверка связи"""
        print("PING...", end=' ', flush=True)
        self.ser.write(b'P')
        resp = self.ser.read(5)
        if resp == b'PONG\n':
            print("OK")
            return True
        else:
            print(f"FAIL (получено: {resp})")
            return False

    def read_block(self, addr, length):
        """Прочитать блок из памяти"""
        cmd = b'R' + addr.to_bytes(2, 'big') + length.to_bytes(2, 'big')
        chk = self._checksum(cmd)
        self.ser.write(cmd + bytes([chk]))

        data = self.ser.read(length)
        data_chk = self.ser.read(1)

        if len(data) != length:
            raise Exception(f"Прочитано {len(data)} байт вместо {length}")

        # Проверка checksum
        expected_chk = self._checksum(data)
        if len(data_chk) == 0 or data_chk[0] != expected_chk:
            raise Exception(f"Checksum не совпал при чтении 0x{addr:04X}")

        return data

    def write_block(self, addr, data):
        """Записать блок в память"""
        length = len(data)
        cmd = b'W' + addr.to_bytes(2, 'big') + length.to_bytes(2, 'big') + data
        chk = self._checksum(cmd)

        self.ser.write(cmd + bytes([chk]))

        resp = self.ser.read(3)
        if resp != b'OK\n':
            raise Exception(f"Запись 0x{addr:04X} failed: {resp}")

    def reset_ecu(self):
        """Перезагрузить ЭБУ"""
        print("Перезагрузка ЭБУ...", end=' ', flush=True)
        self.ser.write(b'Z')
        resp = self.ser.read(3)
        if resp == b'OK\n':
            print("OK")
        else:
            print(f"(ответ: {resp})")
        time.sleep(1)

    def flash_firmware(self, bin_path, verify=True):
        """Прошить .bin файл целиком"""
        if not os.path.exists(bin_path):
            raise FileNotFoundError(f"Файл {bin_path} не найден")

        with open(bin_path, 'rb') as f:
            firmware = f.read()

        total_size = len(firmware)
        print(f"\nПрошивка: {Path(bin_path).name}")
        print(f"Размер: {total_size} байт ({total_size // 1024} КБ)")

        # Проверка связи
        if not self.ping():
            raise Exception("Загрузчик не отвечает. Проверь подключение.")

        # Запись блоками
        print(f"\nЗапись блоками по {BLOCK_SIZE} байт...")
        blocks_total = (total_size + BLOCK_SIZE - 1) // BLOCK_SIZE

        for block_num in range(blocks_total):
            addr = block_num * BLOCK_SIZE
            end = min(addr + BLOCK_SIZE, total_size)
            chunk = firmware[addr:end]

            # Прогресс
            progress = (block_num + 1) * 100 // blocks_total
            print(f"\r[{'=' * (progress // 2)}{' ' * (50 - progress // 2)}] {progress}% (0x{addr:04X})",
                  end='', flush=True)

            try:
                self.write_block(addr, chunk)
            except Exception as e:
                print(f"\n✗ Ошибка записи на 0x{addr:04X}: {e}")
                return False

        print("\n✓ Запись завершена")

        # Верификация
        if verify:
            print("\nПроверка записанных данных...")
            errors = 0

            for block_num in range(blocks_total):
                addr = block_num * BLOCK_SIZE
                end = min(addr + BLOCK_SIZE, total_size)
                expected = firmware[addr:end]

                progress = (block_num + 1) * 100 // blocks_total
                print(f"\r[{'=' * (progress // 2)}{' ' * (50 - progress // 2)}] {progress}%",
                      end='', flush=True)

                try:
                    actual = self.read_block(addr, len(expected))
                    if actual != expected:
                        print(f"\n✗ Несовпадение на 0x{addr:04X}")
                        errors += 1
                        if errors > 10:
                            print("Слишком много ошибок, остановка проверки")
                            return False
                except Exception as e:
                    print(f"\n✗ Ошибка чтения 0x{addr:04X}: {e}")
                    return False

            if errors == 0:
                print("\n✓ Верификация успешна")
            else:
                print(f"\n✗ Найдено {errors} несовпадений")
                return False

        return True

    def close(self):
        self.ser.close()


def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print(f"  {sys.argv[0]} <путь_к_.bin> [--no-verify] [--no-reset]")
        print("\nПример:")
        print(f"  {sys.argv[0]} логер/j30_v41_новая-прошивка.bin")
        print("\nОпции:")
        print("  --no-verify   Не проверять после записи")
        print("  --no-reset    Не перезагружать ЭБУ после прошивки")
        sys.exit(1)

    bin_path = sys.argv[1]
    verify = '--no-verify' not in sys.argv
    do_reset = '--no-reset' not in sys.argv

    try:
        client = BootloaderClient(PORT, BAUD)

        success = client.flash_firmware(bin_path, verify=verify)

        if success and do_reset:
            print("\n" + "=" * 60)
            client.reset_ecu()
            print("ЭБУ перезагружен с новой прошивкой")

        client.close()

        if success:
            print("\n✓ Прошивка завершена успешно")
            sys.exit(0)
        else:
            print("\n✗ Прошивка завершилась с ошибками")
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ ОШИБКА: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
