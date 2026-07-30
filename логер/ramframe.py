# -*- coding: utf-8 -*-
"""
Протокол ПОЛНОГО ДАМПА ОЗУ. Блок:
    [SYNC 0xAE 0x17][addr_hi][addr_lo][len][данные...][checksum]
  - addr = абсолютный адрес первого байта данных в ОЗУ блока;
  - данные — сырые байты как есть (ЛЮБЫЕ, включая 0xFF — не зажимаем);
  - checksum = XOR(addr_hi, addr_lo, len, данные).

Синхра 0xAE17 может случайно встретиться в данных — но ложный кадр не сойдётся
по контрольной сумме, декодер сдвигается на байт и ищет дальше. Так дамп с
произвольными байтами кадрируется надёжно.

ПК собирает из блоков полный ОБРАЗ ОЗУ (адрес -> байт), обновляя его по мере
прихода блоков. Один проход указателя = одно (слегка размазанное по времени)
состояние всего ОЗУ.
"""
SYNC = b"\xAE\x17"
MAX_DATA = 64          # блоки данных не длиннее этого; больше -> ложная синхра


def encode_block(addr, data):
    body = bytes([(addr >> 8) & 0xFF, addr & 0xFF, len(data)]) + bytes(data)
    chk = 0
    for b in body:
        chk ^= b
    return SYNC + body + bytes([chk])


class RamDecoder:
    """Кормим байтами -> собираем образ ОЗУ. feed() возвращает пришедшие блоки."""

    def __init__(self):
        self.buf = bytearray()
        self.image = {}      # адрес -> последний байт
        self.bad = 0         # отброшено байт (диагностика)

    def feed(self, data):
        self.buf.extend(data)
        blocks = []
        while True:
            i = self.buf.find(SYNC)
            if i < 0:
                # мусор без синхры — выкинуть, но оставить хвост (синхра могла
                # разорваться между чанками)
                if len(self.buf) > 1:
                    self.bad += len(self.buf) - 1
                    del self.buf[:-1]
                break
            if i > 0:
                self.bad += i
                del self.buf[:i]
            if len(self.buf) < 5:        # ещё нет заголовка (SYNC+addr+len)
                break
            ln = self.buf[4]
            if ln == 0 or ln > MAX_DATA:  # мусорная длина -> точно ложная синхра
                self.bad += 1
                del self.buf[0]
                continue
            need = 2 + 3 + ln + 1        # SYNC + (addr,len) + данные + checksum
            if len(self.buf) < need:
                break
            body = self.buf[2:5 + ln]
            chk = self.buf[5 + ln]
            calc = 0
            for b in body:
                calc ^= b
            if calc != chk:              # ложная синхра — сдвиг на байт
                self.bad += 1
                del self.buf[0]
                continue
            addr = (self.buf[2] << 8) | self.buf[3]
            payload = bytes(self.buf[5:5 + ln])
            for k, b in enumerate(payload):
                self.image[addr + k] = b
            blocks.append((addr, payload))
            del self.buf[:need]
        return blocks
