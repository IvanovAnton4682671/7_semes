
;адреса портов:
;A_in: 8A7h; A_out: 8A8h

;параметры УСРР (управляющее слово режима работы):
;старший байт:
;U_0: 8Ch; delta_U: 06h
;младший байт:
;SR: 6; RS: 4, 7

;параметры синхронизации:
;tau (мс): 51; R_C: 10; N: 20

;задержка 51 мс = 51 000 000 нс -> для проц-а на 2.50 ГГц это 127 500 000 тактов

;push, pushf, pop и popf корректно работают и без резервирования стека при использовании плоской модели памяти

;важный момент: при вызове программы через call в стеке остаётся последняя инструкция вызванной программы
;пример: у меня в коде происходит call _delay, а в конце _delay расположена команда jmp come_back_here
;сама метка come_back_here: установлена сразу после команды call _delay в программе _start
;из-за этого, после того как значение итераций в CX становится 0, и выполняется команда ret из основной программы
;затем происходит переход на метку come_back_here:, из-за чего потом программа ведёт себя некорректно и работает
;больше раз, чем нужно, так что не нужно использовать метку, к которой будет переходить вызванная программа
;вместо этого вконце вызванной программы можно просто написать ret, и далее будет выполняться инструкция,
;следующая за той, которая вызвала программу через call

.486

.model flat

.data
port_A_in DW 8A7h
port_A_out DW 8A8h
YSRR_1 DB 8Ch
YSRR_0 DB 0
delta_YSRR DB 06h
receiv_input DW 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
new_YSRR DW 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  

.code
_delay:   ;подпрограмма, реализующая задержку примерно в 127 000 000 тактов
    ;сохранение регистров и флагов в стеке
    push ecx   ;сохранение ECX
    push ebx   ;сохранение EBX
    push eax   ;сохранение EAX
    pushf      ;сохранение всех флагов
    
    ;основная программа задержки
    xor eax, eax
    xor ebx, ebx
    xor ecx, ecx
    mov cx, 1448
    first_for:
        mov bx, 3516
        second_for:
            dec bx
            mov ax, 0
            cmp bx, ax
            jz second_for
    loop first_for
    
    ;восстановление регистров и флагов из стека
    popf
    pop eax
    pop ebx
    pop ecx

    ret

_start:

    ;зануление регистров перед работой
    xor ecx, ecx
    xor ebx, ebx
    xor edx, edx
    xor eax, eax

    ;основной цикл программы
    mov cx, 20
    mov ebx, 0
    main_for:
        
        ;проверка R_c на 1
        mov dx, port_A_in
        ;in ax, dx
        mov ax, 0FFFFh
        and ax, 0400h
        jz not_one
            
            ;модификация УСРР[0]
            test cx, 1
            jz chet
                mov YSRR_0, 90h
                jmp dalee
            chet:
                mov YSRR_0, 40h
            dalee:
            
            ;вывод УСРР
            mov dh, YSRR_1
            mov dl, YSRR_0
            mov ax, dx
            mov dx, port_A_out
            ;out dx, ax
            
            ;задержка
            call _delay
            
            ;ввод состояния ПУ СРВ
            mov dx, port_A_in
            ;in ax, dx
            mov ax, 0001h
            mov dx, ax
            
            ;сохранение данных в массивы
            mov eax, offset receiv_input
            mov [eax+ebx], dx
            mov eax, offset new_YSRR
            mov dh, YSRR_1
            mov dl, YSRR_0
            mov [eax+ebx], dx
            add ebx, 2
            
            ;приращение УСРР[1]
            mov dl, YSRR_1
            mov dh, delta_YSRR
            add dl, dh
            mov YSRR_1, dl
            
        not_one:
        
    dec cx
    jnz main_for

    ret
end _start