
;��� ������ �[10], ����� ����������� ������� Amin � ��������� ��� ��������� (Amin!)

.486
.model flat

.data
A DW 10, 20, 30, 40, -5, 6, 7, 8, 9, 10

A_min DW ?
A_cur DW ?
A_min_fact_star DW -1
A_min_fact_mlad DW -1

.code
_start:
    ;���������� ������������ ��������
    mov eax, offset A
    mov ebx, 0
    mov dx, [eax+ebx]
    mov A_min, dx
    xor ecx, ecx
    mov cx, 10
    tipa_for:
        mov dx, [eax+ebx]
        mov A_cur, dx
        mov sp, A_cur
        mov bp, A_min
        cmp sp, bp
        jge skip
            mov dx, A_cur
            mov A_min, dx
        skip:
        add ebx, 2
    loop tipa_for

    ;�������� ������������ �� ����� (��������� ������������� ����� �� ��������) � ������� ����������
    xor eax, eax
    mov sp, 0
    mov bp, A_min
    cmp sp, bp
    jge minus
        mov A_min_fact_star, 0
        mov sp, 1
        mov A_min_fact_mlad, sp
        mov cx, A_min
        opiat_for:
            mov ax, A_min_fact_mlad
            mov bx, A_min_fact_star
            mov dx, A_min
            mul dx
            mov A_min_fact_mlad, ax
            mov A_min_fact_star, dx
            mov dx, A_min
            dec dx
            mov A_min, dx
        loop opiat_for
    minus:

    ret
end _start
