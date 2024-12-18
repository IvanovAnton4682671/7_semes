
;адреса портов: входной - 300h; выходной 301h

;назначение разрядов портов:
;входной:
;0 - ПРДЗ, 1 - кнопка, 2 - КВ0, 3 - КВ1, 4 - давление газа, 5 - давление кислорода
;выходной:
;0 - лампа, 1 - тележка/вперёд, 2 - тележка/назад, 3 - резак/вперёд, 4 - резак/назад, 5 - газ, 6 - кислород, 7 - рольганг

;V_c = 25 мм/с, пусть L = 95 мм, тогда T = (95+30)/25 = 5 c

;за 1.5 сек до конца резки - выдать разрешени рольгангу

;захват/отпускание - 120 мс, резка - 5000 мс

;расчёт тока для захвата: I = 2.16 * t + 36.11
;расчёт тока для отпускания: I = -2.28 * t + 296.21

;расчёт и округление величины силы тока будем осуществлять через сопроцессор

.486

.model flat

.data
port_IN DW 300h
port_OUT DW 301h
address_TSAP DW 302h
catch_release_T DB 120
cutting_T DW 5000
cutting_rolgang_T DW 3500

system_status DW 0
cur_iter Dw 0

param_1 DD 2.16
param_2 DD 36.11
param_3 DW ?
param_4 DD -2.28
param_5 DD 296.21
res_calc DW ?

.code
_delay:

    push ebx ;15 тактов
    push ecx ;15 тактов
    pushf ;14 тактов
    
    ;mov cx, 100 ;4 такта
    mov cx, 1
    first_cycle:
        ;mov bx, 1189 ;4 такта
        mov bx, 1
        second_cycle:
            nop ;3 такта
            dec bx ;2 такта
            jnz second_cycle ;16/4 такта
    loop first_cycle ;17/5 тактов
    ;mov bx, 117 ;4 такта
    mov bx, 1
    third_cycle:
        dec bx ;2 такта
        jnz third_cycle ;16/4 такта
    nop ;3 такта
    nop ;3 такта
    dec bx ;2 такта
    dec bx ;2 такта
    
    popf ;12 тактов
    pop ecx ;12 тактов
    pop ebx ;12 тактов

    ret ;20 тактов



_check_PRDZ:
    ;проверка ПРДЗ (0 разряд)
    mov bx, ax
    and bx, 0000000000000001b
    ret

_check_emergency_button:
    ;проверка аварийнйо кнопки (1 разряд)
    mov bx, ax
    and bx, 0000000000000010b
    ret

_check_KV0:
    ;проверка КВ0 (2 разряд)
    mov bx, ax
    and bx, 0000000000000100b
    ret

_check_KV1:
    ;проверка КВ1 (3 разряд)
    mov bx, ax
    and bx, 0000000000001000b
    ret

_check_gas_pressure:
    ;проверка давления газа (4 разряд)
    mov bx, ax
    and bx, 0000000000010000b
    ret

_check_oxygen_pressure:
    ;проверка давления кислорода (5 разряд)
    mov bx, ax
    and bx, 0000000000100000b
    ret



_start:

    MAIN_CYCLE:
    
        xor ecx, ecx ;зануление регистра-счётчика для корректной работы подпрограммы задержки
    
        ;получение данных на входной порт
        mov dx, port_IN
        ;in ax, dx
        mov ax, 0000000000110101b
        
        ;определение текущего статуса системы
        mov bx, system_status
        cmp bx, 0
        je WAITING   ;система ожидает сигнал ПРДЗ
        cmp bx, 1
        je CATCH   ;система выполняет захват
        cmp bx, 2
        je CUTTING   ;система выполняет резку
        cmp bx, 3
        je RELEASE   ;система выполняет отпускание
        cmp bx, 4
        je SOURCE   ;система переходит в исходное состояние
        cmp bx, 5
        je RELEASE_LAMP   ;система выполняет отпускание с лампой индикации
        cmp bx, 6
        je SOURCE_LAMP   ;система переходит в исходное состояние с лампой индикации
        
        ;обработка состояния ожидания
        WAITING:
        call _check_emergency_button ;проверка аварийной кнопки
        jnz BLOCKING
        
        call _check_PRDZ ;проверка ПРДЗ
        jnz PRDZ_true
        mov dx, port_OUT
        mov ax, 0000000000000000b
        ;out dx, ax
        jmp AGAIN
        
        ;все проверки прошли корректно - устанавливаем новый статус и переходим в состояние захвата
        PRDZ_true:
        mov bx, 1
        mov system_status, bx
        mov bx, 0
        mov cur_iter, bx
        jmp CATCH
        
        ;обработка состояние захвата
        CATCH:
        call _check_emergency_button ;проверка аварийной кнопки
        jnz BLOCKING
        
        ;расчёт величины силы тока в зависимости от итерации захвата
        mov bx, cur_iter
        cmp bx, 120
        ja catch_true
        mov param_3, bx
        fld dword ptr [param_1]
        fimul word ptr [param_3]
        fadd dword ptr [param_2]
        fistp word ptr [res_calc]
        inc bx
        mov cur_iter, bx
        ;передача силы тока в ЦАП и других управляющих величин
        mov dx, address_TSAP
        mov ax, res_calc
        ;out dx, ax
        mov dx, port_OUT
        mov ax, 0000000000000000b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;захват выполнен - установка нового статуса и переход в режим резки
        catch_true:
        mov bx, 0
        mov cur_iter, bx
        mov bx, 2
        mov system_status, bx
        jmp CUTTING
        
        ;обработка состояния резки
        CUTTING:
        call _check_emergency_button ;проверка аварийной кнопки
        jnz BLOCKING
        
        call _check_KV1 ;проверка КВ1
        jnz cutting_false
        
        call _check_gas_pressure ;проверка давления газа
        jz cutting_false
        
        call _check_oxygen_pressure ;проверка давления кислорода
        jz cutting_false
        
        ;в зависимости от итерации резки передаём нужные управляющие величины
        mov bx, cur_iter
        cmp bx, 3500
        ja cutting_rolgang
        inc bx
        mov cur_iter, bx
        mov dx, port_OUT
        mov ax, 0000000001101000b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;осталось 1.5 секунды до конца резки - дополнительно выводим сигнал рольгангу
        cutting_rolgang:
        mov bx, cur_iter
        cmp bx, 5000
        ja cutting_true
        inc bx
        mov cur_iter, bx
        mov dx, port_OUT
        mov ax, 0000000011101000b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;резка выполнена - переходим к отпусканию
        cutting_true:
        mov bx, 0
        mov cur_iter, bx
        mov bx, 3
        mov system_status, bx
        jmp RELEASE
        
        ;резка не выполнена по какой-то причине - переходим к отпускаию с лампой "Заготовка не отрезана"
        cutting_false:
        mov bx, 0
        mov cur_iter, bx
        mov bx, 5
        mov system_status, bx
        jmp RELEASE_LAMP
        
        ;обработка состояния отпускания
        RELEASE:
        call _check_emergency_button ;проверка аварийной кнопки
        jnz BLOCKING
        
        ;расчёт величины силы тока в зависимости от итерации отпускания
        mov bx, cur_iter
        cmp bx, 120
        ja release_true
        mov param_3, bx
        fld dword ptr [param_4]
        fimul word ptr [param_3]
        fadd dword ptr [param_5]
        fistp word ptr [res_calc]
        inc bx
        mov cur_iter, bx
        ;передача силы тока в ЦАП и других управляющих величин
        mov dx, address_TSAP
        mov ax, res_calc
        ;out dx, ax
        mov dx, port_OUT
        mov ax, 0000000000000000b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;отпускание выполнено - установка нового статуса и переход в исходное состояние
        release_true:
        mov bx, 0
        mov cur_iter, bx
        mov bx, 4
        mov system_status, bx
        jmp SOURCE
        
        ;обработка перехода в исходное состояние
        SOURCE:
        call _check_emergency_button ;проверка аварийной кнопки
        jnz BLOCKING
        
        call _check_KV0 ;проверка КВ0
        jnz KV0_true
        
        ;КВ0 не достигнут, так что двигаем назад и тележку, и резак
        mov bx, cur_iter
        cmp bx, 5000
        ja cutting_source
        inc bx
        mov cur_iter, bx
        ;передача управляющих величин
        mov dx, port_OUT
        mov ax, 0000000000010100b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;КВ0 достигнут, так что двигаем назад только резак
        KV0_true:
        mov bx, cur_iter
        cmp bx, 5000
        ja cutting_source
        inc bx
        mov cur_iter, bx
        ;передача управляющих величин
        mov dx, port_OUT
        mov ax, 0000000000010000b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;доехали до исходной позиции - устанавливаем новый статус и переходим в состояние ожидания
        cutting_source:
        mov bx, 0
        mov cur_iter, bx
        mov system_status, bx
        jmp WAITING
        
        ;обработка состояния отпускания с лампой
        RELEASE_LAMP:
        call _check_emergency_button ;проверка аварийной кнопки
        jnz BLOCKING
        
        ;расчёт величины силы тока в зависимости от итерации отпускания
        mov bx, cur_iter
        cmp bx, 120
        ja release_lamp_true
        mov param_3, bx
        fld dword ptr [param_4]
        fimul word ptr [param_3]
        fadd dword ptr [param_5]
        fistp word ptr [res_calc]
        inc bx
        mov cur_iter, bx
        ;передача силы тока в ЦАП и других управляющих величин (лампа индикации "Заготовка не отрезана")
        mov dx, address_TSAP
        mov ax, res_calc
        ;out dx, ax
        mov dx, port_OUT
        mov ax, 0000000000000001b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;отпускание выполнено - установка нового статуса и переход в исходное состояние с лампой индикации
        release_lamp_true:
        mov bx, 0
        mov cur_iter, bx
        mov bx, 6
        mov system_status, bx
        jmp SOURCE
        
        ;обработка перехода в исходное состояние с лампой
        SOURCE_LAMP:
        call _check_emergency_button ;проверка аварийной кнопки
        jnz BLOCKING
        
        call _check_KV0 ;проверка КВ0
        jnz KV0_lamp_true
        
        ;КВ0 не достигнут, так что двигаем назад и тележку, и резак
        mov bx, cur_iter
        cmp bx, 5000
        ja cutting_lamp_source
        inc bx
        mov cur_iter, bx
        ;передача управляющих величин (лампа индикации "Заготовка не отрезана")
        mov dx, port_OUT
        mov ax, 0000000000010101b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;КВ0 достигнут, так что двигаем назад только резак
        KV0_lamp_true:
        mov bx, cur_iter
        cmp bx, 5000
        ja cutting_lamp_source
        inc bx
        mov cur_iter, bx
        ;передача управляющих величин (лампа индикации "Заготовка не отрезана")
        mov dx, port_OUT
        mov ax, 0000000000010001b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;доехали до исходной позиции - устанавливаем новый статус и переходим в состояние ожидания
        cutting_lamp_source:
        mov bx, 0
        mov cur_iter, bx
        mov system_status, bx
        jmp WAITING
        
        ;обработка особого состояния - блокировки
        BLOCKING:
        mov dx, port_OUT
        mov ax, 0000000000000000b
        ;out dx, ax
        jmp SHUTDOWN
    
    ;запуск основного цикла заново
    AGAIN:
    jmp MAIN_CYCLE

    ;ещё одно особое состояние, которое полностью блокирует работу объекта (цикл просто заканчивается, и нужно заново запускать объект)
    SHUTDOWN:
    ret

end _start
