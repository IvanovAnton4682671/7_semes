
def calc_amps_for_catch(t):
    return int(round((2.16 * t + 36.11), 0))

def calc_amps_for_release(t):
    return int(round((-2.28 * t + 296.21), 0))

def delay():
    print("Произошла задержка в 1 мс")

def check_PRDZ(inputs):
    return inputs[0]

def check_emergency_button(inputs):
    return inputs[1]

def check_KV0(inputs):
    return inputs[2]

def check_KV1(inputs):
    return inputs[3]

def check_gas_pressure(inputs):
    return inputs[4]

def check_oxygen_pressure(inputs):
    return inputs[5]

def main_cycle_iteration(inputs, system_status, cur_iter):
    def convert_int_to_bin(number):
        return bin(number)[2:]

    print(f"Получили данные {inputs} с порта ввода {port_IN}")

    while True:
        if system_status == 0:
            button_status = check_emergency_button(inputs)
            if button_status == 1:
                print("Блокировка")
                print(f"Вывели на порт вывода {port_OUT} значения 000000000000")
                return 0, button_status, system_status, cur_iter
            prdz_status = check_PRDZ(inputs)
            if prdz_status == 0:
                print("От ПРДЗ не пришёл разрешающий сигнал")
                print(f"Вывели на порт вывода {port_OUT} значение 0000000000000000")
                return 0, button_status, system_status, cur_iter
            system_status = 1
            cur_iter = 0
            print("От ПРДЗ пришёл разрешающий сигнал")

        elif system_status == 1:
            button_status = check_emergency_button(inputs)
            if button_status == 1:
                print("Блокировка")
                print(f"Вывели на порт вывода {port_OUT} значения 000000000000")
                return 0, button_status, system_status, cur_iter
            if cur_iter <= catch_release_T:
                res_calc = calc_amps_for_catch(cur_iter)
                bin_res_calc = convert_int_to_bin(res_calc)
                print(f"Вывели на адрес ЦАПа {address_TSAP} силу тока {res_calc} ({bin_res_calc}) мА для {cur_iter} мс захвата")
                cur_iter += 1
                print(f"Вывели на порт вывода {port_OUT} значение 0000000000000000")
                delay()
                return 0, button_status, system_status, cur_iter
            else:
                cur_iter = 0
                system_status = 2
                print("Захват выполнен")

        elif system_status == 2:
            button_status = check_emergency_button(inputs)
            if button_status == 1:
                print("Блокировка")
                print(f"Вывели на порт вывода {port_OUT} значения 000000000000")
                return 0, button_status, system_status, cur_iter
            kv1_status = check_KV1(inputs)
            if kv1_status == 1:
                cur_iter = 0
                system_status = 5
                print("Резка не окончена: тележка доехала до КВ1")
            else:
                gas_status = check_gas_pressure(inputs)
                if gas_status == 0:
                    cur_iter = 0
                    system_status = 5
                    print("Резка не окончена: упало давление газа")
                else:
                    oxygen_status = check_oxygen_pressure(inputs)
                    if oxygen_status == 0:
                        cur_iter = 0
                        system_status = 5
                        print("Резка не окончена: упало давление кислорода")
            if cur_iter <= cutting_rolgang_T:
                print(f"Произошла итерация резки для {cur_iter} мс")
                cur_iter += 1
                print(f"Вывели на порт вывода {port_OUT} значение 0000000001101000")
                delay()
                return 0, button_status, system_status, cur_iter
            elif cutting_rolgang_T < cur_iter <= cutting_T:
                print(f"Произошла итерация резки для {cur_iter} мс")
                cur_iter += 1
                print(f"Вывели на порт вывода {port_OUT} значение 0000000011101000")
                delay()
                return 0, button_status, system_status, cur_iter
            else:
                cur_iter = 0
                system_status = 3
                print("Резка окончена")

        elif system_status == 3:
            button_status = check_emergency_button(inputs)
            if button_status == 1:
                print("Блокировка")
                print(f"Вывели на порт вывода {port_OUT} значения 000000000000")
                return 0, button_status, system_status, cur_iter
            if cur_iter <= catch_release_T:
                res_calc = calc_amps_for_release(cur_iter)
                bin_res_calc = convert_int_to_bin(res_calc)
                print(f"Вывели на адрес ЦАПа {address_TSAP} силу тока {res_calc} ({bin_res_calc}) мА для {cur_iter} мс отпускания")
                cur_iter += 1
                print(f"Вывели на порт вывода {port_OUT} значение 0000000000000000")
                delay()
                return 0, button_status, system_status, cur_iter
            else:
                cur_iter = 0
                system_status = 4
                print("Отпускание выполнено")

        elif system_status == 4:
            button_status = check_emergency_button(inputs)
            if button_status == 1:
                print("Блокировка")
                print(f"Вывели на порт вывода {port_OUT} значения 000000000000")
                return 0, button_status, system_status, cur_iter
            kv0_status = check_KV0(inputs)
            if kv0_status == 0:
                if cur_iter <= cutting_T:
                    print("Движемся в исходную позицию (и тележка, и резак)")
                    cur_iter += 1
                    print(f"Вывели на порт вывода {port_OUT} значение 0000000000010100")
                    delay()
                    return 0, button_status, system_status, cur_iter
                else:
                    print("Движемся в исходную позицию (только тележка)")
                    print(f"Вывели на порт вывода {port_OUT} значение 0000000000000100")
                    delay()
                    return 0, button_status, system_status, cur_iter
            else:
                if cur_iter <= cutting_T:
                    print("Движемся в исходную позицию (только резак)")
                    cur_iter += 1
                    print(f"Вывели на порт вывода {port_OUT} значение 0000000000010000")
                    delay()
                    return 0, button_status, system_status, cur_iter
                else:
                    cur_iter = 0
                    system_status = 0
                    print("Приехали в исходную")
                    return 1, button_status, system_status, cur_iter

        elif system_status == 5:
            button_status = check_emergency_button(inputs)
            if button_status == 1:
                print("Блокировка")
                print(f"Вывели на порт вывода {port_OUT} значения 000000000000")
                return 0, button_status, system_status, cur_iter
            if cur_iter <= catch_release_T:
                res_calc = calc_amps_for_release(cur_iter)
                bin_res_calc = convert_int_to_bin(res_calc)
                print(f"Вывели на адрес ЦАПа {address_TSAP} силу тока {res_calc} ({bin_res_calc}) мА для {cur_iter} мс отпускания")
                cur_iter += 1
                print(f"Вывели на порт вывода {port_OUT} значение 0000000000000001 (лампа индикации)")
                delay()
                return 0, button_status, system_status, cur_iter
            else:
                cur_iter = 0
                system_status = 6
                print("Отпускание выполнено")

        elif system_status == 6:
            button_status = check_emergency_button(inputs)
            if button_status == 1:
                print("Блокировка")
                print(f"Вывели на порт вывода {port_OUT} значения 000000000000")
                return 0, button_status, system_status, cur_iter
            kv0_status = check_KV0(inputs)
            if kv0_status == 0:
                if cur_iter <= cutting_T:
                    print("Движемся в исходную позицию (и тележка, и резак) с лампой индикации")
                    cur_iter += 1
                    print(f"Вывели на порт вывода {port_OUT} значение 0000000000010101")
                    delay()
                    return 0, button_status, system_status, cur_iter
                else:
                    print("Движемся в исходную позицию (только тележка) с лампой индикации")
                    print(f"Вывели на порт вывода {port_OUT} значение 0000000000000101")
                    delay()
                    return 0, button_status, system_status, cur_iter
            else:
                if cur_iter <= cutting_T:
                    print("Движемся в исходную позицию (только резак) с лампой индикации")
                    cur_iter += 1
                    print(f"Вывели на порт вывода {port_OUT} значение 0000000000010001")
                    delay()
                    return 0, button_status, system_status, cur_iter
                else:
                    cur_iter = 0
                    system_status = 0
                    print("Приехали в исходную")
                    return 1, button_status, system_status, cur_iter

port_IN = "300h"
port_OUT = "301h"
address_TSAP = "302h"
catch_release_T = 5   #5 для теста, 120 - норма
cutting_T = 5   #5 для теста, 5000 - норма
cutting_rolgang_T = 3   #3 для теста, 3500 - норма
system_status = 0
cur_iter = 0

inputs = [1, 0, 1, 0, 1, 1]
res = 0
while res != 1:
    res, button_status, system_status, cur_iter = main_cycle_iteration(inputs, system_status, cur_iter)
