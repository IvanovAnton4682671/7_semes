
;������ ������:
;A_in: 8A7h; A_out: 8A8h

;��������� ���� (����������� ����� ������ ������):
;������� ����:
;U_0: 8Ch; delta_U: 06h
;������� ����:
;SR: 6; RS: 4, 7

;��������� �������������:
;tau (��): 51; R_C: 10; N: 20

;�������� 51 �� = 51 000 000 �� -> ��� ����-� �� 2.50 ��� ��� 127 500 000 ������

;push, pushf, pop � popf ��������� �������� � ��� �������������� ����� ��� ������������� ������� ������ ������

;������ ������: ��� ������ ��������� ����� call � ����� ������� ��������� ���������� ��������� ���������
;������: � ���� � ���� ���������� call _delay, � � ����� _delay ����������� ������� jmp come_back_here
;���� ����� come_back_here: ����������� ����� ����� ������� call _delay � ��������� _start
;��-�� �����, ����� ���� ��� �������� �������� � CX ���������� 0, � ����������� ������� ret �� �������� ���������
;����� ���������� ������� �� ����� come_back_here:, ��-�� ���� ����� ��������� ���� ���� ����������� � ��������
;������ ���, ��� �����, ��� ��� �� ����� ������������ �����, � ������� ����� ���������� ��������� ���������
;������ ����� ������ ��������� ��������� ����� ������ �������� ret, � ����� ����� ����������� ����������,
;��������� �� ���, ������� ������� ��������� ����� call

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
_delay:   ;������������, ����������� �������� �������� � 127 000 000 ������
    ;���������� ��������� � ������ � �����
    push ecx   ;���������� ECX
    push ebx   ;���������� EBX
    push eax   ;���������� EAX
    pushf      ;���������� ���� ������
    
    ;�������� ��������� ��������
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
    
    ;�������������� ��������� � ������ �� �����
    popf
    pop eax
    pop ebx
    pop ecx

    ret

_start:

    ;��������� ��������� ����� �������
    xor ecx, ecx
    xor ebx, ebx
    xor edx, edx
    xor eax, eax

    ;�������� ���� ���������
    mov cx, 20
    mov ebx, 0
    main_for:
        
        ;�������� R_c �� 1
        mov dx, port_A_in
        ;in ax, dx
        mov ax, 0FFFFh
        and ax, 0400h
        jz not_one
            
            ;����������� ����[0]
            test cx, 1
            jz chet
                mov YSRR_0, 90h
                jmp dalee
            chet:
                mov YSRR_0, 40h
            dalee:
            
            ;����� ����
            mov dh, YSRR_1
            mov dl, YSRR_0
            mov ax, dx
            mov dx, port_A_out
            ;out dx, ax
            
            ;��������
            call _delay
            
            ;���� ��������� �� ���
            mov dx, port_A_in
            ;in ax, dx
            mov ax, 0001h
            mov dx, ax
            
            ;���������� ������ � �������
            mov eax, offset receiv_input
            mov [eax+ebx], dx
            mov eax, offset new_YSRR
            mov dh, YSRR_1
            mov dl, YSRR_0
            mov [eax+ebx], dx
            add ebx, 2
            
            ;���������� ����[1]
            mov dl, YSRR_1
            mov dh, delta_YSRR
            add dl, dh
            mov YSRR_1, dl
            
        not_one:
        
    dec cx
    jnz main_for

    ret
end _start