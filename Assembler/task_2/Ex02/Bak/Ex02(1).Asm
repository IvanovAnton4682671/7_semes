
.486
.model flat

.data
const_1 DB 255
const_2 DB 7
const_3 DB 78
a_1 DW 22958
b_1 DW 11
c_1 DB 3
desiat DB 10

a_1_tsel DB ?
a_1_ost DB ?
c_1_res DB ?
b_1_tsel DB ?
b_1_ost DB ?
b_1_mul_tsel DW ?
b_1_mul_ost DW ?
res_tsel DW ?
res_ost DW ?
check_tsel DB ?
check_ost DB ?
RESULT DB ?

.code
_start:
    ;A/255
    mov ax, a_1
    xor dx, dx
    div const_1
    mov a_1_tsel, al
    mov a_1_ost, ah
    
    ;7+C
    mov ah, const_2
    mov bl, c_1
    add ah, bl
    mov c_1_res, ah
    
    ;B/(7+C)
    mov ax, b_1
    xor dx, dx
    div c_1_res
    mov b_1_tsel, al
    mov b_1_ost, ah
    
    ;B/(7+C)*78
    mov al, b_1_tsel
    mul const_3
    mov b_1_mul_tsel, ax
    mov al, b_1_ost
    mul const_3
    mov b_1_mul_ost, ax
    mov ax, b_1_mul_ost
    xor dx, dx
    div desiat
    movzx bx, ah
    mov b_1_mul_ost, bx
    movzx bx, al
    mov ax, b_1_mul_tsel
    add ax, bx
    mov b_1_mul_tsel, ax
    
    ;A/255-B/(7+C)*78
    movzx ax, a_1_ost      ;перемещаем остаток от деления
    mov bx, b_1_mul_ost    ;перемещаем остаток от умножения
    sub ax, bx             ;вычитаем
    mov res_ost, ax        ;записываем результат вычитания
    movzx ax, a_1_tsel     ;перемещаем целую часть деления
    mov bx, b_1_mul_tsel   ;перемещаем целую часть умножения
    sbb ax, bx             ;вычитаем с учётом флага заёма
    mov res_tsel, ax       ;записываем результат вычитания
    
    ;проверка целой части на наличие 1 в разряде 9
    mov ax, res_tsel    ;загружаем целую часть в AX для проверки
    and ax, 0200h       ;0200h - маска (0000 0010 0000 0000) для проверки (1 на 10 месте справа, потому что отсчёт - младший бит имеет номер 0, за ним 1 и т.д.)
    jz not_set_tsel     ;если бит не установлен, то прыгаем на not_set
    mov check_tsel, 1   ;если бит установлен, то запишем 1 по адресу
    not_set_tsel:       ;если бит не установлен, то запишем 2 по адресу
    mov check_tsel, 2
    
    ;аналогичная проверка остатка
    mov ax, res_ost
    and ax, 0200h
    jz not_set_ost
    mov check_ost, 1
    not_set_ost:
    mov check_ost, 2
    
    ;такая же проверка в DX
    mov ax, 0200h
    and dx, ax
    jz not_set_dx
    mov RESULT, 1
    not_set_dx:
    mov RESULT, 2
    
    ret
end _start