
;������ ������: ������� - 300h; �������� 301h

;���������� �������� ������:
;�������:
;0 - ����, 1 - ������, 2 - ��0, 3 - ��1, 4 - �������� ����, 5 - �������� ���������
;��������:
;0 - �����, 1 - �������/�����, 2 - �������/�����, 3 - �����/�����, 4 - �����/�����, 5 - ���, 6 - ��������, 7 - ��������

;V_c = 25 ��/�, ����� L = 95 ��, ����� T = (95+30)/25 = 5 c

;�� 1.5 ��� �� ����� ����� - ������ ��������� ���������

;������/���������� - 120 ��, ����� - 5000 ��

;������ ���� ��� �������: I = 2.16 * t + 36.11
;������ ���� ��� ����������: I = -2.28 * t + 296.21

;������ � ���������� �������� ���� ���� ����� ������������ ����� �����������

.486

.model flat

.data
port_IN DW 300h
port_OUT DW 301h
address_TSAP DW 302h
catch_release_T DB 120
cutting_T DW 5000

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

    push ebx ;15 ������
    push ecx ;15 ������
    pushf ;14 ������
    
    ;mov cx, 100 ;4 �����
    mov cx, 1
    first_cycle:
        ;mov bx, 1189 ;4 �����
        mov bx, 1
        second_cycle:
            nop ;3 �����
            dec bx ;2 �����
            jnz second_cycle ;16/4 �����
    loop first_cycle ;17/5 ������
    ;mov bx, 117 ;4 �����
    mov bx, 1
    third_cycle:
        dec bx ;2 �����
        jnz third_cycle ;16/4 �����
    nop ;3 �����
    nop ;3 �����
    dec bx ;2 �����
    dec bx ;2 �����
    
    popf ;12 ������
    pop ecx ;12 ������
    pop ebx ;12 ������

    ret ;20 ������



_check_PRDZ:
    ;�������� ���� (0 ������)
    mov bx, ax
    and bx, 0000000000000001b
    ret

_check_emergency_button:
    ;�������� ��������� ������ (1 ������)
    mov bx, ax
    and bx, 0000000000000010b
    ret

_check_KV0:
    ;�������� ��0 (2 ������)
    mov bx, ax
    and bx, 0000000000000100b
    ret

_check_KV1:
    ;�������� ��1 (3 ������)
    mov bx, ax
    and bx, 0000000000001000b
    ret

_check_gas_pressure:
    ;�������� �������� ���� (4 ������)
    mov bx, ax
    and bx, 0000000000010000b
    ret

_check_oxygen_pressure:
    ;�������� �������� ��������� (5 ������)
    mov bx, ax
    and bx, 0000000000100000b
    ret



_start:

    MAIN_CYCLE:
    
        xor ecx, ecx
    
        ;��������� ������ �� ������� ����
        mov dx, port_IN
        ;in ax, dx
        mov ax, 0000000000110101b
        
        ;����������� �������� ������� �������
        mov bx, system_status
        cmp bx, 0
        je WAITING   ;������� ������� ������ ����
        cmp bx, 1
        je CATCH   ;������� ��������� ������
        cmp bx, 2
        je CUTTING   ;������� ��������� �����
        cmp bx, 3
        je RELEASE   ;������� ��������� ����������
        cmp bx, 4
        je SOURCE   ;������� ��������� � �������� ���������
        cmp bx, 5
        je RELEASE_LAMP   ;������� ��������� ���������� � ������ ���������
        cmp bx, 6
        je SOURCE_LAMP   ;������� ��������� � �������� ��������� � ������ ���������
        
        ;��������� ��������� ��������
        WAITING:
        call _check_emergency_button ;�������� ��������� ������
        jnz BLOCKING
        
        call _check_PRDZ ;�������� ����
        jnz PRDZ_true
        mov dx, port_OUT
        mov ax, 0000000000000000b
        ;out dx, ax
        jmp AGAIN
        
        ;��� �������� ������ ��������� - ������������� ����� ������ � ��������� � ��������� �������
        PRDZ_true:
        mov bx, 1
        mov system_status, bx
        mov bx, 0
        mov cur_iter, bx
        jmp CATCH
        
        ;��������� ��������� �������
        CATCH:
        call _check_emergency_button ;�������� ��������� ������
        jnz BLOCKING
        
        ;������ �������� ���� ���� � ����������� �� �������� �������
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
        ;�������� ���� ���� � ��� � ������ ����������� �������
        mov dx, address_TSAP
        mov ax, res_calc
        ;out dx, ax
        mov dx, port_OUT
        mov ax, 0000000000000000b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;������ �������� - ��������� ������ ������� � ������� � ����� �����
        catch_true:
        mov bx, 0
        mov cur_iter, bx
        mov bx, 2
        mov system_status, bx
        jmp CUTTING
        
        ;��������� ��������� �����
        CUTTING:
        call _check_emergency_button ;�������� ��������� ������
        jnz BLOCKING
        
        call _check_KV1 ;�������� ��1
        jnz cutting_false
        
        call _check_gas_pressure ;�������� �������� ����
        jz cutting_false
        
        call _check_oxygen_pressure ;�������� �������� ���������
        jz cutting_false
        
        ;� ����������� �� �������� ����� ������� ������ ����������� ��������
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
        
        ;�������� 1.5 ������� �� ����� ����� - ������������� ������� ������ ���������
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
        
        ;����� ��������� - ��������� � ����������
        cutting_true:
        mov bx, 0
        mov cur_iter, bx
        mov bx, 3
        mov system_status, bx
        jmp RELEASE
        
        ;����� �� ��������� �� �����-�� ������� - ��������� � ��������� � ������ "��������� �� ��������"
        cutting_false:
        mov bx, 0
        mov cur_iter, bx
        mov bx, 5
        mov system_status, bx
        jmp RELEASE_LAMP
        
        ;��������� ��������� ����������
        RELEASE:
        call _check_emergency_button ;�������� ��������� ������
        jnz BLOCKING
        
        ;������ �������� ���� ���� � ����������� �� �������� ����������
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
        ;�������� ���� ���� � ��� � ������ ����������� �������
        mov dx, address_TSAP
        mov ax, res_calc
        ;out dx, ax
        mov dx, port_OUT
        mov ax, 0000000000000000b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;���������� ��������� - ��������� ������ ������� � ������� � �������� ���������
        release_true:
        mov bx, 0
        mov cur_iter, bx
        mov bx, 4
        mov system_status, bx
        jmp SOURCE
        
        ;��������� �������� � �������� ���������
        SOURCE:
        call _check_emergency_button ;�������� ��������� ������
        jnz BLOCKING
        
        call _check_KV0 ;�������� ��0
        jnz KV0_true
        
        ;��0 �� ���������, ��� ��� ������� ����� � �������, � �����
        mov bx, cur_iter
        cmp bx, 5000
        ja cutting_source
        inc bx
        mov cur_iter, bx
        ;�������� ����������� �������
        mov dx, port_OUT
        mov ax, 0000000000010100b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;��0 ���������, ��� ��� ������� ����� ������ �����
        KV0_true:
        mov bx, cur_iter
        cmp bx, 5000
        ja cutting_source
        inc bx
        mov cur_iter, bx
        ;�������� ����������� �������
        mov dx, port_OUT
        mov ax, 0000000000010000b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;������� �� �������� ������� - ������������� ����� ������ � ��������� � ��������� ��������
        cutting_source:
        mov bx, 0
        mov cur_iter, bx
        mov system_status, bx
        jmp WAITING
        
        ;��������� ��������� ���������� � ������
        RELEASE_LAMP:
        call _check_emergency_button ;�������� ��������� ������
        jnz BLOCKING
        
        ;������ �������� ���� ���� � ����������� �� �������� ����������
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
        ;�������� ���� ���� � ��� � ������ ����������� ������� (����� ��������� "��������� �� ��������")
        mov dx, address_TSAP
        mov ax, res_calc
        ;out dx, ax
        mov dx, port_OUT
        mov ax, 0000000000000001b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;���������� ��������� - ��������� ������ ������� � ������� � �������� ��������� � ������ ���������
        release_lamp_true:
        mov bx, 0
        mov cur_iter, bx
        mov bx, 6
        mov system_status, bx
        jmp SOURCE
        
        ;��������� �������� � �������� ��������� � ������
        SOURCE_LAMP:
        call _check_emergency_button ;�������� ��������� ������
        jnz BLOCKING
        
        call _check_KV0 ;�������� ��0
        jnz KV0_lamp_true
        
        ;��0 �� ���������, ��� ��� ������� ����� � �������, � �����
        mov bx, cur_iter
        cmp bx, 5000
        ja cutting_lamp_source
        inc bx
        mov cur_iter, bx
        ;�������� ����������� ������� (����� ��������� "��������� �� ��������")
        mov dx, port_OUT
        mov ax, 0000000000010101b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;��0 ���������, ��� ��� ������� ����� ������ �����
        KV0_lamp_true:
        mov bx, cur_iter
        cmp bx, 5000
        ja cutting_lamp_source
        inc bx
        mov cur_iter, bx
        ;�������� ����������� ������� (����� ��������� "��������� �� ��������")
        mov dx, port_OUT
        mov ax, 0000000000010001b
        ;out dx, ax
        call _delay
        jmp AGAIN
        
        ;������� �� �������� ������� - ������������� ����� ������ � ��������� � ��������� ��������
        cutting_lamp_source:
        mov bx, 0
        mov cur_iter, bx
        mov system_status, bx
        jmp WAITING
        
        ;��������� ������� ��������� - ����������
        BLOCKING:
        mov dx, port_OUT
        mov ax, 0000000000000000b
        ;out dx, ax
        jmp SHUTDOWN
    
    ;������ ��������� ����� ������
    AGAIN:
    jmp MAIN_CYCLE

    ;��� ���� ������ ���������, ������� ��������� ��������� ������ ������� (���� ������ �������������, � ����� ������ ��������� ������)
    SHUTDOWN:
    ret

end _start
