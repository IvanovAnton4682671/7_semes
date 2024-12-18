
import tkinter as tk

####################################################################################################

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

    while True:
        if system_status == 0:
            button_status = check_emergency_button(inputs)
            if button_status == 1:
                print("Блокировка")
                print(f"Вывели на порт вывода {port_OUT} значения 000000000000")
                label_iteration_info.config(text=f"Статус системы: {system_status} (ОЖИДАНИЕ)\nИтерация процесса: {cur_iter}\nОписание: Блокировка\nВывод: Вывели на порт вывода {port_OUT} значения 000000000000\nЗадержка: Не вызывалась")
                return 0, button_status, system_status, cur_iter
            prdz_status = check_PRDZ(inputs)
            if prdz_status == 0:
                print("От ПРДЗ не пришёл разрешающий сигнал")
                print(f"Вывели на порт вывода {port_OUT} значение 0000000000000000")
                label_iteration_info.config(text=f"Статус системы: {system_status} (ОЖИДАНИЕ)\nИтерация процесса: {cur_iter}\nОписание: От ПРДЗ не пришёл разрешающий сигнал\nВывод: Вывели на порт вывода {port_OUT} значения 000000000000\nЗадержка: Не вызывалась")
                return 0, button_status, system_status, cur_iter
            system_status = 1
            cur_iter = 0
            print("От ПРДЗ пришёл разрешающий сигнал")

        elif system_status == 1:
            button_status = check_emergency_button(inputs)
            if button_status == 1:
                print("Блокировка")
                print(f"Вывели на порт вывода {port_OUT} значения 000000000000")
                label_iteration_info.config(text=f"Статус системы: {system_status} (ЗАХВАТ)\nИтерация процесса: {cur_iter}\nОписание: Блокировка\nВывод: Вывели на порт вывода {port_OUT} значения 000000000000\nЗадержка: Не вызывалась")
                return 0, button_status, system_status, cur_iter
            if cur_iter <= catch_release_T:
                res_calc = calc_amps_for_catch(cur_iter)
                bin_res_calc = convert_int_to_bin(res_calc)
                print(f"Вывели на адрес ЦАПа {address_TSAP} силу тока {res_calc} ({bin_res_calc}) мА для {cur_iter} мс захвата")
                label_iteration_info.config(text=f"Статус системы: {system_status} (ЗАХВАТ)\nИтерация процесса: {cur_iter}\nОписание: Вывели на адрес ЦАПа {address_TSAP} силу тока {res_calc} ({bin_res_calc}) мА для {cur_iter} мс захвата\nВывод: Вывели на порт вывода {port_OUT} значения 000000000000\nЗадержка: Произошла задержка в 1 мс")
                gripping(cur_iter, catch_release_T)
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
                label_iteration_info.config(text=f"Статус системы: {system_status} (РЕЗКА)\nИтерация процесса: {cur_iter}\nОписание: Блокировка\nВывод: Вывели на порт вывода {port_OUT} значения 000000000000\nЗадержка: Не вызывалась")
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
                label_iteration_info.config(text=f"Статус системы: {system_status} (РЕЗКА)\nИтерация процесса: {cur_iter}\nОписание: Произошла итерация резки для {cur_iter} мс\nВывод: Вывели на порт вывода {port_OUT} значение 0000000001101000\nЗадержка: Произошла задержка в 1 мс")
                cutting(cur_iter, cutting_T, -18)
                move_front_cart(cur_iter, cutting_T)
                cur_iter += 1
                print(f"Вывели на порт вывода {port_OUT} значение 0000000001101000")
                delay()
                return 0, button_status, system_status, cur_iter
            elif cutting_rolgang_T < cur_iter <= cutting_T:
                print(f"Произошла итерация резки для {cur_iter} мс")
                label_iteration_info.config(text=f"Статус системы: {system_status} (РЕЗКА)\nИтерация процесса: {cur_iter}\nОписание: Произошла итерация резки для {cur_iter} мс\nВывод: Вывели на порт вывода {port_OUT} значение 0000000011101000\nЗадержка: Произошла задержка в 1 мс")
                cutting(cur_iter, cutting_T, -18)
                move_front_cart(cur_iter, cutting_T)
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
                label_iteration_info.config(text=f"Статус системы: {system_status} (ОТПУСКАНИЕ)\nИтерация процесса: {cur_iter}\nОписание: Блокировка\nВывод: Вывели на порт вывода {port_OUT} значения 000000000000\nЗадержка: Не вызывалась")
                return 0, button_status, system_status, cur_iter
            if cur_iter <= catch_release_T:
                res_calc = calc_amps_for_release(cur_iter)
                bin_res_calc = convert_int_to_bin(res_calc)
                print(f"Вывели на адрес ЦАПа {address_TSAP} силу тока {res_calc} ({bin_res_calc}) мА для {cur_iter} мс отпускания")
                label_iteration_info.config(text=f"Статус системы: {system_status} (ОТПУСКАНИЕ)\nИтерация процесса: {cur_iter}\nОписание: Вывели на адрес ЦАПа {address_TSAP} силу тока {res_calc} ({bin_res_calc}) мА для {cur_iter} мс отпускания\nВывод: Вывели на порт вывода {port_OUT} значение 0000000000000000\nЗадержка: Произошла задержка в 1 мс")
                releasing(cur_iter, catch_release_T)
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
                label_iteration_info.config(text=f"Статус системы: {system_status} (ИСХОДНАЯ)\nИтерация процесса: {cur_iter}\nОписание: Блокировка\nВывод: Вывели на порт вывода {port_OUT} значения 000000000000\nЗадержка: Не вызывалась")
                return 0, button_status, system_status, cur_iter
            kv0_status = check_KV0(inputs)
            if kv0_status == 0:
                if cur_iter <= cutting_T:
                    print("Движемся в исходную позицию (и тележка, и резак)")
                    label_iteration_info.config(text=f"Статус системы: {system_status} (ИСХОДНАЯ)\nИтерация процесса: {cur_iter}\nОписание: Движемся в исходную позицию (и тележка, и резак)\nВывод: Вывели на порт вывода {port_OUT} значение 0000000000010100\nЗадержка: Произошла задержка в 1 мс")
                    cutting(cur_iter, cutting_T, 18)
                    move_back_cart(cur_iter, kv0_status)
                    cur_iter += 1
                    print(f"Вывели на порт вывода {port_OUT} значение 0000000000010100")
                    delay()
                    return 0, button_status, system_status, cur_iter
                else:
                    print("Движемся в исходную позицию (только тележка)")
                    label_iteration_info.config(text=f"Статус системы: {system_status} (ИСХОДНАЯ)\nИтерация процесса: {cur_iter}\nОписание: Движемся в исходную позицию (только тележка)\nВывод: Вывели на порт вывода {port_OUT} значение 0000000000000100\nЗадержка: Произошла задержка в 1 мс")
                    move_back_cart(cur_iter, kv0_status)
                    cur_iter += 1
                    print(f"Вывели на порт вывода {port_OUT} значение 0000000000000100")
                    delay()
                    return 0, button_status, system_status, cur_iter
            else:
                if cur_iter <= cutting_T:
                    print("Движемся в исходную позицию (только резак)")
                    label_iteration_info.config(text=f"Статус системы: {system_status} (ИСХОДНАЯ)\nИтерация процесса: {cur_iter}\nОписание: Движемся в исходную позицию (только резак)\nВывод: Вывели на порт вывода {port_OUT} значение 0000000000010000\nЗадержка: Произошла задержка в 1 мс")
                    cutting(cur_iter, cutting_T, 18)
                    cur_iter += 1
                    print(f"Вывели на порт вывода {port_OUT} значение 0000000000010000")
                    delay()
                    return 0, button_status, system_status, cur_iter
                else:
                    cur_iter = 0
                    system_status = 0
                    move_back_cart(cur_iter, 1)
                    print("Приехали в исходную")
                    return 1, button_status, system_status, cur_iter

        elif system_status == 5:
            button_status = check_emergency_button(inputs)
            if button_status == 1:
                print("Блокировка")
                print(f"Вывели на порт вывода {port_OUT} значения 000000000000")
                label_iteration_info.config(text=f"Статус системы: {system_status} (ОТПУСКАНИЕ С ЛАМПОЙ)\nИтерация процесса: {cur_iter}\nОписание: Блокировка\nВывод: Вывели на порт вывода {port_OUT} значения 000000000000\nЗадержка: Не вызывалась")
                return 0, button_status, system_status, cur_iter
            if cur_iter <= catch_release_T:
                res_calc = calc_amps_for_release(cur_iter)
                bin_res_calc = convert_int_to_bin(res_calc)
                print(f"Вывели на адрес ЦАПа {address_TSAP} силу тока {res_calc} ({bin_res_calc}) мА для {cur_iter} мс отпускания")
                label_iteration_info.config(text=f"Статус системы: {system_status} (ОТПУСКАНИЕ С ЛАМПОЙ)\nИтерация процесса: {cur_iter}\nОписание: Вывели на адрес ЦАПа {address_TSAP} силу тока {res_calc} ({bin_res_calc}) мА для {cur_iter} мс отпускания\nВывод: Вывели на порт вывода {port_OUT} значение 0000000000000001 (лампа индикации)\nЗадержка: Произошла задержка в 1 мс")
                releasing(cur_iter, catch_release_T)
                lamp_status(True)
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
                label_iteration_info.config(text=f"Статус системы: {system_status} (ИСХОДНАЯ С ЛАМПОЙ)\nИтерация процесса: {cur_iter}\nОписание: Блокировка\nВывод: Вывели на порт вывода {port_OUT} значения 000000000000\nЗадержка: Не вызывалась")
                return 0, button_status, system_status, cur_iter
            kv0_status = check_KV0(inputs)
            if kv0_status == 0:
                if cur_iter <= cutting_T:
                    print("Движемся в исходную позицию (и тележка, и резак) с лампой индикации")
                    label_iteration_info.config(text=f"Статус системы: {system_status} (ИСХОДНАЯ С ЛАМПОЙ)\nИтерация процесса: {cur_iter}\nОписание: Движемся в исходную позицию (и тележка, и резак) с лампой индикации\nВывод: Вывели на порт вывода {port_OUT} значение 0000000000010101\nЗадержка: Произошла задержка в 1 мс")
                    cutting(cur_iter, cutting_T, 18)
                    move_back_cart(cur_iter, kv0_status)
                    cur_iter += 1
                    print(f"Вывели на порт вывода {port_OUT} значение 0000000000010101")
                    delay()
                    return 0, button_status, system_status, cur_iter
                else:
                    print("Движемся в исходную позицию (только тележка) с лампой индикации")
                    label_iteration_info.config(text=f"Статус системы: {system_status} (ИСХОДНАЯ С ЛАМПОЙ)\nИтерация процесса: {cur_iter}\nОписание: Движемся в исходную позицию (только тележка) с лампой индикации\nВывод: Вывели на порт вывода {port_OUT} значение 0000000000000101\nЗадержка: Произошла задержка в 1 мс")
                    move_back_cart(cur_iter, kv0_status)
                    cur_iter += 1
                    print(f"Вывели на порт вывода {port_OUT} значение 0000000000000101")
                    delay()
                    return 0, button_status, system_status, cur_iter
            else:
                if cur_iter <= cutting_T:
                    print("Движемся в исходную позицию (только резак) с лампой индикации")
                    label_iteration_info.config(text=f"Статус системы: {system_status} (ИСХОДНАЯ С ЛАМПОЙ)\nИтерация процесса: {cur_iter}\nОписание: Движемся в исходную позицию (только резак) с лампой индикации\nВывод: Вывели на порт вывода {port_OUT} значение 0000000000010001\nЗадержка: Произошла задержка в 1 мс")
                    cutting(cur_iter, cutting_T, 18)
                    cur_iter += 1
                    print(f"Вывели на порт вывода {port_OUT} значение 0000000000010001")
                    delay()
                    return 0, button_status, system_status, cur_iter
                else:
                    cur_iter = 0
                    system_status = 0
                    lamp_status(False)
                    move_back_cart(cur_iter, 1)
                    print("Приехали в исходную")
                    return 1, button_status, system_status, cur_iter

port_IN = "300h"
port_OUT = "301h"
address_TSAP = "302h"
catch_release_T = 5   #5 для теста, 120 - норма
cutting_T = 5   #5 для теста, 5000 - норма
cutting_rolgang_T = 3   #3 для теста, 3500 - норма
global system_status, cur_iter   # эти переменные глобальные, чтобы их можно было изменять из кнопки
system_status = 0
cur_iter = 0

####################################################################################################

root = tk.Tk()
root.title("Эмулятор газорезки МНЛЗ")
root.geometry("900x700")
root.resizable(False, False)

####################################################################################################

label_prdz = tk.Label(root, text="Данные от ПРДЗ", font=("Courier New", 12), fg="black")
label_prdz.place(x=25, y=25)

label_emergency_button = tk.Label(root, text="Данные от аварийной кнопки", font=("Courier New", 12), fg="black")
label_emergency_button.place(x=25, y=75)

label_kv0 = tk.Label(root, text="Данные от КВ0", font=("Courier New", 12), fg="black")
label_kv0.place(x=25, y=125)

label_kv1 = tk.Label(root, text="Данные от КВ1", font=("Courier New", 12), fg="black")
label_kv1.place(x=25, y=175)

label_gas_pressure = tk.Label(root, text="Данные от датчика давления газа", font=("Courier New", 12), fg="black")
label_gas_pressure.place(x=25, y=225)

label_oxygen_pressure = tk.Label(root, text="Данные от датчика давления кислорода", font=("Courier New", 12), fg="black")
label_oxygen_pressure.place(x=25, y=275)

label_inputs = tk.Label(root, text="", font=("Courier New", 12), justify="left", fg="black")
label_inputs.place(x=25, y=325)

label_iteration_info = tk.Label(root, text="", font=("Courier New", 12), justify="left", fg="black")
label_iteration_info.place(x=25, y=390)

####################################################################################################

def validate_spinbox_input(new_value):
    return new_value in ("0", "1")

vcmd = (root.register(validate_spinbox_input), "%P")

spinbox_prdz = tk.Spinbox(root, from_=0, to=1, font=("Courier New", 12), width=3, justify="center", validate="key", validatecommand=vcmd)
spinbox_prdz.place(x=450, y=25)

spinbox_emergency_button = tk.Spinbox(root, from_=0, to=1, font=("Courier New", 12), width=3, justify="center", validate="key", validatecommand=vcmd)
spinbox_emergency_button.place(x=450, y=75)

spinbox_kv0 = tk.Spinbox(root, from_=0, to=1, font=("Courier New", 12), width=3, justify="center", validate="key", validatecommand=vcmd)
spinbox_kv0.place(x=450, y=125)

spinbox_kv1 = tk.Spinbox(root, from_=0, to=1, font=("Courier New", 12), width=3, justify="center", validate="key", validatecommand=vcmd)
spinbox_kv1.place(x=450, y=175)

spinbox_gas_pressure = tk.Spinbox(root, from_=0, to=1, font=("Courier New", 12), width=3, justify="center", validate="key", validatecommand=vcmd)
spinbox_gas_pressure.place(x=450, y=225)

spinbox_oxygen_pressure = tk.Spinbox(root, from_=0, to=1, font=("Courier New", 12), width=3, justify="center", validate="key", validatecommand=vcmd)
spinbox_oxygen_pressure.place(x=450, y=275)

####################################################################################################

canvas = tk.Canvas(root, width=900, height=200, bg="white")
canvas.place(x=0, y=500)

#жёлоб
chute = canvas.create_rectangle(0, 75, 900, 125, fill="#ADB5BD", outline="#000814")

#система охлаждения
cooling_system = canvas.create_rectangle(0, 15, 100, 185, fill="#495057", outline="#000814")

#заготовка
workpiece = canvas.create_rectangle(100, 90, 195, 110, fill="#FFBE0B", outline="#000814")

#лампа
lamp = canvas.create_oval(800, 10, 830, 40, fill="", outline="#000814")

#рабочая вагонетка с захватом и резаком
def create_cart() -> list[object]:
    """
    Метод, который создаёт и объединяет в группы основные объекты (тележка, резак и захват)

    Args:
        None

    Returns:
        cart (list[object]): Список объектов составляющих тележки
        gripping_valve (list[objects]): Список объектов составляющих клапана захвата
        cutter (list[object]): Список объектов составляющих резак
    """
    cart = canvas.create_rectangle(100, 130, 200, 160, fill="#343A40", outline="#000814")
    cart_wheel_1 = canvas.create_oval(110, 150, 130, 170, fill="#8D0801", outline="#000814")
    cart_wheel_2 = canvas.create_oval(170, 150, 190, 170, fill="#8D0801", outline="#000814")
    cath_rail = canvas.create_rectangle(180, 130, 181, 60, fill="#343A40", outline="#000814")
    catch_foot_down = canvas.create_rectangle(180, 120, 165, 120, fill="#343A40", outline="#000814")
    catch_foot_up = canvas.create_rectangle(180, 80, 165, 80, fill="#343A40", outline="#000814")
    cutter_rail = canvas.create_rectangle(120, 130, 121, 60, fill="#343A40", outline="#000814")
    cutter_body = canvas.create_rectangle(110, 125, 120, 110, fill="#D62828", outline="#000814")
    cutter_nozzle = canvas.create_rectangle(110, 117, 100, 117, fill="#343A40", outline="#000814")

    return [cart, cart_wheel_1, cart_wheel_2, cath_rail, catch_foot_down, catch_foot_up, cutter_rail, cutter_body, cutter_nozzle], [catch_foot_down, catch_foot_up], [cutter_body, cutter_nozzle]

cart, gripping_valve, cutter = create_cart()

def move_group_obj(group_obj: list, d_x: int, d_y: int) -> None:
    """
    Метод, который перемещает нарисованный объект канваса в новое положение

    Args:
        group_obj (list): Список объектов, которые нужно переместить
        d_x (int): Величина перемещения по оси X
        d_y (int): Величина перемещения по оси Y

    Returns:
        None
    """
    for obj in group_obj:
        canvas.move(obj, d_x, d_y)

def lamp_status(status: bool) -> None:
    """
    Метод, который включает/выключает аварийную лампу

    Args:
        status (bool): Статус лампы (True - включена, False - выключена)

    Returns:
        None
    """
    if status:
        canvas.itemconfig(lamp, fill="#FCA311")
    else:
        canvas.itemconfig(lamp, fill="")

def gripping(cur_iter: int, total_iter: int) -> None:
    """
    Метод, который производит анимацию захвата заготовки

    Args:
        cur_iter (int): Текущая итераций процесса захвата
        total_iter (int): Общее количество итераций процесса захвата

    Returns:
        None
    """
    if cur_iter == 0:
        move_group_obj([gripping_valve[0]], 0, -5)
        move_group_obj([gripping_valve[1]], 0, 5)
    elif cur_iter == total_iter:
        move_group_obj([gripping_valve[0]], 0, -5)
        move_group_obj([gripping_valve[1]], 0, 5)

def releasing(cur_iter: int, total_iter: int) -> None:
    """
    Метод, который производит анимацию отпускания заготовки

    Args:
        cur_iter (int): Текущая итераций процесса отпускания
        total_iter (int): Общее количество итераций процесса отпускания

    Returns:
        None
    """
    if (cur_iter - 1) == 0:
        move_group_obj([gripping_valve[0]], 0, 5)
        move_group_obj([gripping_valve[1]], 0, -5)
    elif cur_iter == total_iter:
        move_group_obj([gripping_valve[0]], 0, 5)
        move_group_obj([gripping_valve[1]], 0, -5)

def cutting(cur_iter: int, total_iter: int, y: int) -> None:
    """
    Метод, который производит анимацию процесса резки

    Args:
        cur_iter (int): Текущая итераций процесса резки
        total_iter (int): Общее количество итераций процесса резки

    Returns:
        None
    """
    if cur_iter == 0:
        move_group_obj(cutter, 0, y)
    elif cur_iter == total_iter:
        move_group_obj(cutter, 0, y)

def move_front_cart(cur_iter: int, total_iter: int) -> None:
    """
    Метод, который двигает вагонетку вперёд при резке

    Args:
        cur_iter (int): Текущая итераций процесса резки
        total_iter (int): Общее количество итераций процесса резки

    Returns:
        None
    """
    if cur_iter == 0:
        if workpiece not in cart:
            cart.append(workpiece)
        move_group_obj(cart, 300, 0)
    elif cur_iter == total_iter:
        if workpiece not in cart:
            cart.append(workpiece)
        move_group_obj(cart, 300, 0)

def set_start_cart(cart: list[object]) -> None:
    """
    Метод, который устанавливает вагонетку в изначальную позицию

    Args:
        cart (list[object]): Список всех составляющих вагонетки

    Returns:
        None
    """
    canvas.coords(workpiece, 100, 90, 195, 110)
    canvas.coords(cart[0], 100, 130, 200, 160)
    canvas.coords(cart[1], 110, 150, 130, 170)
    canvas.coords(cart[2], 170, 150, 190, 170)
    canvas.coords(cart[3], 180, 130, 181, 60)
    canvas.coords(cart[4], 180, 120, 165, 120)
    canvas.coords(cart[5], 180, 80, 165, 80)
    canvas.coords(cart[6], 120, 130, 121, 60)
    canvas.coords(cart[7], 110, 125, 120, 110)
    canvas.coords(cart[8], 110, 117, 100, 117)

def move_back_cart(cur_iter: int, kv0_status: int) -> None:
    """
    Метод, который двигает вагонетку в исходную позицию

    Args:
        cur_iter (int): Текущая итерация процесса движения назад
        kv0_status (int): Статус КВ0

    Returns:
        None
    """
    if workpiece in cart:
        cart.remove(workpiece)
    if kv0_status == 1:
        set_start_cart(cart)
    elif cur_iter == 0:
        move_group_obj(cart, -300, 0)
        move_group_obj([workpiece], 100, 0)

####################################################################################################
def get_inputs():
    prdz = spinbox_prdz.get()
    emergency_button = spinbox_emergency_button.get()
    kv0 = spinbox_kv0.get()
    kv1 = spinbox_kv1.get()
    gas_pressure = spinbox_gas_pressure.get()
    oxygen_pressure = spinbox_oxygen_pressure.get()
    return prdz, emergency_button, kv0, kv1, gas_pressure, oxygen_pressure

def print_inputs(prdz, emergency_button, kv0, kv1, gas_pressure, oxygen_pressure):
    inputs = f"Данные, пришедшие на порт ввода 300h: ПРДЗ - {prdz}; аварийная кнопка - {emergency_button};\nКВ0 - {kv0}; КВ1 - {kv1}; датчик давления газа - {gas_pressure}; датчик давления кислорода - {oxygen_pressure}"
    label_inputs.config(text=inputs)

def button_click():
    global system_status, cur_iter
    prdz, emergency_button, kv0, kv1, gas_pressure, oxygen_pressure = get_inputs()
    print_inputs(prdz, emergency_button, kv0, kv1, gas_pressure, oxygen_pressure)
    inputs = [int(prdz), int(emergency_button), int(kv0), int(kv1), int(gas_pressure), int(oxygen_pressure)]
    flag, button_status, system_status, cur_iter = main_cycle_iteration(inputs, system_status, cur_iter)
    if button_status == 1:
        root.destroy()
    return system_status, cur_iter

button_iteration = tk.Button(root, text="Отправить данные", font=("Courier New", 12), command=lambda: button_click())
button_iteration.place(x=550, y=150)

####################################################################################################

root.mainloop()
