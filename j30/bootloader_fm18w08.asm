; ==============================================================================
; ЗАГРУЗЧИК ДЛЯ FM18W08 — запись прошивки через UART
; ==============================================================================
; Назначение: принимает команды с ПК через FT232/ESP32 → UART ЭБУ,
;             записывает данные в FM18W08 (FRAM на месте ROM).
;
; Размещение: 0x45E4–0x6EFF (свободная зона ~10 КБ)
; Процессор: HD6303
; Прошивка: J30 v39_7 и далее
;
; ПРОТОКОЛ КОМАНД:
; ┌────────────────────────────────────────────────────────────────┐
; │ Команда      │ Формат                                          │
; ├──────────────┼─────────────────────────────────────────────────┤
; │ WRITE        │ 'W' адрес_hi адрес_lo длина_hi длина_lo [данные]│
; │ READ         │ 'R' адрес_hi адрес_lo длина_hi длина_lo         │
; │ PING         │ 'P'                                              │
; │ RESET        │ 'Z'                                              │
; └──────────────┴─────────────────────────────────────────────────┘
;
; ОТВЕТЫ:
;   'OK\n'        — команда выполнена
;   'ERR\n'       — ошибка (неверная команда, checksum)
;   'PONG\n'      — ответ на PING
;   [данные]      — ответ на READ
;
; КОНТРОЛЬНАЯ СУММА:
;   После блока данных идёт 1 байт checksum = XOR всех байтов команды+данных
;
; ПРИМЕР WRITE 2 байта по адресу 0x4900:
;   'W' 0x49 0x00 0x00 0x02 0xAA 0xBB checksum
;
; ==============================================================================

; Регистры UART HD6303
RMCR    = $0010         ; режим (не трогаем, настроен штатно)
TRCSR   = $0011         ; статус (бит 0x80=RDRF, бит 0x20=TDRE)
RDR     = $0012         ; приём
TDR     = $0013         ; передача

RDRF    = $80           ; маска бита "байт принят"
TDRE    = $20           ; маска бита "готов передать"

; Рабочие переменные (используем зону RAM 0x0100–0x01FF, свободную в J30)
WORK    = $0180         ; базовый адрес рабочей зоны
CMD     = WORK+0        ; код команды
ADDR_HI = WORK+1        ; адрес записи (старший байт)
ADDR_LO = WORK+2        ; адрес записи (младший байт)
LEN_HI  = WORK+3        ; длина данных (старший)
LEN_LO  = WORK+4        ; длина данных (младший)
CHKSUM  = WORK+5        ; контрольная сумма
PTR_HI  = WORK+6        ; указатель на данные (старший)
PTR_LO  = WORK+7        ; указатель на данные (младший)
COUNT_HI= WORK+8        ; счётчик байтов (старший)
COUNT_LO= WORK+9        ; счётчик байтов (младший)

; ==============================================================================
; ТОЧКА ВХОДА: вызывается из опорного прерывания (RTI) или главного цикла
; ==============================================================================
        ORG     $45E4

bootloader_entry:
        ; Проверить, есть ли байт в UART (бит RDRF)
        LDAA    TRCSR
        ANDA    #RDRF
        BEQ     boot_exit       ; нет байта -> выход

        ; Принять команду
        LDAA    RDR             ; читаем байт команды
        STAA    CMD
        STAA    CHKSUM          ; начинаем checksum

        ; Разбор команды
        CMPA    #'W'
        BEQ     cmd_write
        CMPA    #'R'
        BEQ     cmd_read
        CMPA    #'P'
        BEQ     cmd_ping
        CMPA    #'Z'
        BEQ     cmd_reset

        ; Неизвестная команда
        BRA     send_error

boot_exit:
        RTS

; ==============================================================================
; КОМАНДА WRITE: записать блок данных в FM18W08
; ==============================================================================
cmd_write:
        ; Принять адрес (2 байта)
        JSR     uart_recv       ; -> A
        STAA    ADDR_HI
        JSR     update_chksum

        JSR     uart_recv
        STAA    ADDR_LO
        JSR     update_chksum

        ; Принять длину (2 байта)
        JSR     uart_recv
        STAA    LEN_HI
        JSR     update_chksum

        JSR     uart_recv
        STAA    LEN_LO
        JSR     update_chksum

        ; Подготовить указатель
        LDAA    ADDR_HI
        STAA    PTR_HI
        LDAA    ADDR_LO
        STAA    PTR_LO

        ; Подготовить счётчик
        LDAA    LEN_HI
        STAA    COUNT_HI
        LDAA    LEN_LO
        STAA    COUNT_LO

write_loop:
        ; Проверить счётчик
        LDAA    COUNT_HI
        ORAA    COUNT_LO
        BEQ     write_done      ; счётчик = 0 -> конец

        ; Принять байт данных
        JSR     uart_recv       ; -> A
        JSR     update_chksum

        ; Записать байт в память (FM18W08)
        ; ВНИМАНИЕ: запись идёт напрямую по адресу, GAL видит R/W=0 -> формирует /WE
        LDX     PTR_HI          ; X = адрес (используем 16-бит указатель)
        STAA    0,X             ; пишем байт

        ; Увеличить указатель
        LDX     PTR_HI
        INX
        STX     PTR_HI

        ; Уменьшить счётчик
        LDX     COUNT_HI        ; загружаем 16-бит счётчик
        DEX
        STX     COUNT_HI

        BRA     write_loop

write_done:
        ; Принять checksum от ПК
        JSR     uart_recv       ; -> A

        ; Сравнить с вычисленным
        CMPA    CHKSUM
        BNE     send_error

        ; Всё OK
        BRA     send_ok

; ==============================================================================
; КОМАНДА READ: прочитать блок данных из памяти
; ==============================================================================
cmd_read:
        ; Принять адрес
        JSR     uart_recv
        STAA    ADDR_HI
        JSR     update_chksum

        JSR     uart_recv
        STAA    ADDR_LO
        JSR     update_chksum

        ; Принять длину
        JSR     uart_recv
        STAA    LEN_HI
        JSR     update_chksum

        JSR     uart_recv
        STAA    LEN_LO
        JSR     update_chksum

        ; Принять checksum заголовка
        JSR     uart_recv
        CMPA    CHKSUM
        BNE     send_error

        ; Подготовить указатель и счётчик
        LDAA    ADDR_HI
        STAA    PTR_HI
        LDAA    ADDR_LO
        STAA    PTR_LO

        LDAA    LEN_HI
        STAA    COUNT_HI
        LDAA    LEN_LO
        STAA    COUNT_LO

        CLR     CHKSUM          ; новый checksum для данных

read_loop:
        ; Проверить счётчик
        LDAA    COUNT_HI
        ORAA    COUNT_LO
        BEQ     read_done

        ; Читать байт из памяти
        LDX     PTR_HI
        LDAA    0,X

        ; Обновить checksum
        EORA    CHKSUM
        STAA    CHKSUM

        ; Отправить байт
        LDX     PTR_HI
        LDAA    0,X
        JSR     uart_send

        ; Увеличить указатель
        LDX     PTR_HI
        INX
        STX     PTR_HI

        ; Уменьшить счётчик
        LDX     COUNT_HI
        DEX
        STX     COUNT_HI

        BRA     read_loop

read_done:
        ; Отправить checksum
        LDAA    CHKSUM
        JSR     uart_send
        RTS

; ==============================================================================
; КОМАНДА PING: проверка связи
; ==============================================================================
cmd_ping:
        LDAA    #'P'
        JSR     uart_send
        LDAA    #'O'
        JSR     uart_send
        LDAA    #'N'
        JSR     uart_send
        LDAA    #'G'
        JSR     uart_send
        LDAA    #$0A            ; '\n'
        JSR     uart_send
        RTS

; ==============================================================================
; КОМАНДА RESET: программный сброс ЭБУ
; ==============================================================================
cmd_reset:
        ; Отправить OK
        JSR     send_ok

        ; Ждём завершения передачи
        JSR     uart_flush

        ; Прыгаем на вектор сброса (адрес из 0xFFFE)
        JMP     [$FFFE]

; ==============================================================================
; ОТПРАВКА ОТВЕТОВ
; ==============================================================================
send_ok:
        LDAA    #'O'
        JSR     uart_send
        LDAA    #'K'
        JSR     uart_send
        LDAA    #$0A            ; '\n'
        JSR     uart_send
        RTS

send_error:
        LDAA    #'E'
        JSR     uart_send
        LDAA    #'R'
        JSR     uart_send
        LDAA    #'R'
        JSR     uart_send
        LDAA    #$0A
        JSR     uart_send
        RTS

; ==============================================================================
; НИЗКОУРОВНЕВЫЕ UART ФУНКЦИИ
; ==============================================================================

; Принять байт (ожидание, если нет данных)
; Возвращает: A = принятый байт
uart_recv:
        LDAA    TRCSR
        ANDA    #RDRF
        BEQ     uart_recv       ; busy-wait (в загрузчике допустимо)
        LDAA    RDR
        RTS

; Отправить байт (ожидание готовности)
; Вход: A = байт для отправки
uart_send:
        PSHA                    ; сохраняем A
uart_send_wait:
        LDAA    TRCSR
        ANDA    #TDRE
        BEQ     uart_send_wait
        PULA                    ; восстанавливаем A
        STAA    TDR
        RTS

; Ждать завершения передачи
uart_flush:
        LDAA    TRCSR
        ANDA    #TDRE
        BEQ     uart_flush
        RTS

; Обновить checksum (XOR с аккумулятором)
; Вход: A = новый байт
update_chksum:
        EORA    CHKSUM
        STAA    CHKSUM
        RTS

; ==============================================================================
; КОНЕЦ ЗАГРУЗЧИКА
; ==============================================================================
; Размер: ~250 байт (влезает в 0x45E4–0x46D0)
; Остаток зоны 0x46D0–0x6EFF остаётся свободным для расширений
