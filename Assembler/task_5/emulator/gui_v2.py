
import tkinter as tk
from typing import Tuple, List
import sys

################################################################################
#создание основного окна

root = tk.Tk()
root.title("Эмулятор газорезки МНЛЗ")
root.geometry("800x600")
root.resizable(False, False)

################################################################################
#создание канваса

canvas = tk.Canvas(root, width=800, height=300, bg="white")
canvas.place(x=0, y=300)

################################################################################
#создание всех объектов

#жёлоб
chute = canvas.create_rectangle(0, 125, 800, 175, fill="#adb5bd", outline="#000814")

#система охлаждения
cooling_system = canvas.create_rectangle(0, 75, 100, 225, fill="#495057", outline="#000814")

#заготовка
workpiece = canvas.create_rectangle(100, 140, 800, 160, fill="#ffbe0B", outline="#000814")
prdz_text = canvas.create_text(150, 50, text="Разрешение от ПРДЗ: да", font=("Times New Roman", 14))

#лампа
lamp = canvas.create_oval(600, 40, 630, 70, fill="", outline="#000814")
lamp_text = canvas.create_text(600, 25, text="Лампа индикации 'Заготовка не отрезана'", font=(("Times New Roman", 14)))

#статус рольганга
rolgang_text = canvas.create_text(150, 25, text="Разрешение для рольганга: нет", font=("Times New Roman", 14))

#КВ0
kv_0 = canvas.create_rectangle(110, 205, 130, 225, fill="#000814", outline="#000814")
kv_0_inner = canvas.create_rectangle(112, 207, 128, 223, fill="#da2c38", outline="")

#КВ1
kv_1 = canvas.create_rectangle(770, 205, 790, 225, fill="#000814", outline="#000814")
kv_1_inner = canvas.create_rectangle(772, 207, 788, 223, fill="#edf6f9", outline="")

#тележка с захватом и резаком
def create_cart() -> Tuple[List[int], List[int], List[int]]:
    """
    Метод, который создаёт и объединяет в группы основные объекты (тележка, резак и захват)

    Args:
        None

    Returns:
        cart (List[int]): Список объектов тележки (+ клапан и захват)
        gripping_valve (List[int]): Список объектов клапана захвата
        cutter (List[int]): Список объектов резак
    """
    cart = canvas.create_rectangle(100, 180, 200, 210, fill="#343a40", outline="#000814")
    cart_wheel_1 = canvas.create_oval(110, 200, 130, 220, fill="#8d0801", outline="#000814")
    cart_wheel_2 = canvas.create_oval(170, 200, 190, 220, fill="#8d0801", outline="#000814")
    cath_rail = canvas.create_rectangle(180, 180, 181, 110, fill="#343a40", outline="#000814")
    catch_foot_down = canvas.create_rectangle(180, 170, 165, 170, fill="#343a40", outline="#000814")
    catch_foot_up = canvas.create_rectangle(180, 130, 165, 130, fill="#343a40", outline="#000814")
    cutter_rail = canvas.create_rectangle(120, 180, 121, 110, fill="#343a40", outline="#000814")
    cutter_body = canvas.create_rectangle(110, 175, 120, 160, fill="#d62828", outline="#000814")
    cutter_nozzle = canvas.create_rectangle(110, 167, 100, 167, fill="#343a40", outline="#000814")

    return [cart, cart_wheel_1, cart_wheel_2, cath_rail, catch_foot_down, catch_foot_up, cutter_rail, cutter_body, cutter_nozzle], [catch_foot_down, catch_foot_up], [cutter_body, cutter_nozzle]
cart, valve, cutter = create_cart()

################################################################################
#функции анимаций объектов

#печать разрешения ПРДЗ
def prdz_mode(status: bool) -> None:
    """
    Функция, которая печатает разрешение от ПРДЗ

    Args:
        status (bool): Статус разрешения (True - есть, False - нет)

    Returns:
        None
    """
    if status:
        canvas.itemconfig(prdz_text, text="Разрешение от ПРДЗ: да")
    else:
        canvas.itemconfig(prdz_text, text="Разрешение от ПРДЗ: нет")

#включение/выключение лампы
def lamp_mode(status: bool) -> None:
    """
    Функция, которая заполняет лампу цветом

    Args:
        status (bool): Режим работы лампы (True - включить, False - выключить)

    Returns:
        None
    """
    if status:
        canvas.itemconfig(lamp, fill="#fca311")
    else:
        canvas.itemconfig(lamp, fill="")

#печать разрешения рольганга
def rolgang_mode(status: bool) -> None:
    """
    Функция, которая печатает статус получения рольгангом разрешения

    Args:
        status (bool): Статус получения рольгангом разрешения (True - есть, False - нет)

    Returns:
        None
    """
    if status:
        canvas.itemconfig(rolgang_text, text="Разрешение для рольганга: да")
    else:
        canvas.itemconfig(rolgang_text, text="Разрешение для рольганга: нет")

#покраска КВ
def kv_mode(status: bool, kv_in: int) -> None:
    """
    Функция, которая меняет цвет КВ

    Args:
        status (bool): Статус покраски КВ (True - красный, False - светлый)
        kv_in (int): ID КВ, который нужно покрасить

    Returns:
        None
    """
    if status:
        canvas.itemconfig(kv_in, fill="#da2c38")
    else:
        canvas.itemconfig(kv_in, fill="#edf6f9")

#захват/отпускание заготовки
def valve_mode(status: bool) -> None:
    """
    Функция, которая выполняет анимацию захвата/отпускания заготовки

    Args:
        status (bool): Режим работы клапана (True - захват, False - отпускание)

    Returns:
        None
    """
    valve_0_coords = canvas.coords(valve[0])
    valve_1_coords = canvas.coords(valve[1])

    if status and valve_0_coords[1] == 170.0 and valve_1_coords[1] == 130.0:
        canvas.move(valve[0], 0, -10)
        canvas.move(valve[1], 0, 10)
    elif not status and valve_0_coords[1] == 160.0 and valve_1_coords[1] == 140.0:
        canvas.move(valve[0], 0, 10)
        canvas.move(valve[1], 0, -10)

#движение резака
def cutter_move(canvas, status: bool, duration: int, delay: int, on_complete: callable) -> None:
    """
    Функция, которая выполняет плавное перемещение резака к конечной позиции за указанную длительность

    Args:
        canvas: Главный canvas, на котором изображены все объекты
        status (bool): Направление перемещения резака (True - вверх, False - вниз)
        duration (int): Длительность процесса резки в секундах
        delay (int): Величина задержки (в мс) между кадрами перерисовки
        on_complete (callable): Функция, которая изменяет флаг состояния резки

    Returns:
        None
    """
    global cutter_anim_id
    if status:
        target_coords_cutter = [110.0, 138.0, 120.0, 123.0]
        target_coords_nozzle = [110.0, 133.0, 100.0, 133.0]
    else:
        target_coords_cutter = [110.0, 147.0, 120.0, 162.0] #какого-то хуя тут надо было поменять координаты y1 и y2 местами
        target_coords_nozzle = [110.0, 167.0, 100.0, 167.0]
    start_coords_cutter = canvas.coords(cutter[0])
    start_coords_nozzle = canvas.coords(cutter[1])
    iterations = (duration * 1000) // delay
    dy = (target_coords_cutter[1] - start_coords_cutter[1]) / iterations
    if status:
        dy -= 0.13 #доводка скорости
    else:
        dy += 0.13 #доводка скорости

    def anim_step(current_iteration: int) -> None:
        """
        Вспомогательная функция, выполняющая один шаг перемещения резака

        Args:
            current_iteration (int): Текущая итерация движения

        Returns:
            None
        """
        global cutter_anim_id
        if current_iteration < iterations and (canvas.coords(cutter[0]) != target_coords_cutter) and (canvas.coords(cutter[1]) != target_coords_nozzle):
            if current_iteration + 25 == iterations and status:
                rolgang_mode(True)
            for obj in cutter:
                canvas.move(obj, 0, dy)
            cutter_anim_id = canvas.after(delay, lambda: anim_step(current_iteration + 1))
        if current_iteration >= iterations or canvas.coords(cutter[0]) == target_coords_cutter or canvas.coords(cutter[1]) == target_coords_nozzle:
            on_complete()
            return

    anim_step(0)

#движение тележки
def cart_move(canvas, status: bool, dx: int, delay: int, on_complete: callable) -> None:
    """
    Функция, которая выполняет плавную анимацию перемещения тележки

    Args:
        canvas: Главный canvas, на котором изображены все объекты
        status (bool): Сторона перемещения тележки (True - вправо, False - влево)
        dx (int): Величина перемещения по оси X
        delay (int): Величина задержки (в мс) между кадрами перерисовки
        on_complete (callable): Функция, вызываемая после завершения текущего цикла движения

    Returns:
        None
    """
    global cart_anim_id

    def anim_step() -> None:
        """
        Вспомогательная функция, которая выполняет расчёт позиций объектов для кадра анимации

        Args:
            None

        Returns:
            None
        """
        global cart_anim_id
        cart_coords = canvas.coords(cart[0])
        if status and cart_coords[2] >= 800.0:
            on_complete()
            return
        elif not status and cart_coords[0] <= 100.0:
            on_complete()
            return
        for obj in cart:
            canvas.move(obj, dx if status else -dx, 0)
            cart_coords = canvas.coords(cart[0])
            if cart_coords[0] == 100.0:
                kv_mode(True, kv_0_inner)
            else:
                kv_mode(False, kv_0_inner)
            if cart_coords[2] == 800.0:
                kv_mode(True, kv_1_inner)
            else:
                kv_mode(False, kv_1_inner)
        cart_anim_id = canvas.after(delay, anim_step)

    anim_step()

################################################################################

#запуск работы объекта
def start_object() -> None:
    """
    Функция, которая запускает цикл работы объекта

    Args:
        None

    Returns:
        None
    """
    global is_cutting, cutter_finished, cart_finished, cutter_anim_id, cart_anim_id
    button_start.config(state=tk.DISABLED)
    dx = 1 #скорость перемещения заготовки
    cart_delay = 30 #интервал между перерисовками вагонетки
    duration = 5 #время резки
    cutter_delay = 50 #интервал между перерисовками резака
    is_cutting = True #общий флаг резки
    cutter_finished = False #флаг процесса резака
    cart_finished = False #флаг процесса тележки
    cutter_anim_id = None #id текущей анимации резки
    cart_anim_id = None #id текущей анимации вагонетки

    #отмена анимации
    def cancel_anim(anim_id: str) -> None:
        """
        Функция, которая отменяет текущую анимацию

        Args:
            anim_id (str): ID отменяемой анимации

        Returns:
            None
        """
        if anim_id is not None:
            canvas.after_cancel(anim_id)

    def check_and_continue() -> None:
        """
        Основная функция, которая корректирует поведение анимаций всех объектов в цикле

        Args:
            None

        Returns:
            None
        """
        global is_cutting, cutter_finished, cart_finished

        if is_cutting and (cutter_finished or cart_finished):  # Если объект завершил движение вперёд
            # Остановить текущую анимацию противоположного объекта
            if cutter_finished and not cart_finished:
                cancel_anim(cart_anim_id)
                cart_finished = True
            elif cart_finished and not cutter_finished:
                cancel_anim(cutter_anim_id)
                lamp_mode(True)
                cutter_finished = True

            # Если оба объекта завершили движение
            if cutter_finished and cart_finished:
                is_cutting = False  # Меняем глобальный флаг
                cutter_finished = False
                cart_finished = False

                # Начинаем движение в обратном направлении
                valve_mode(False)
                canvas.after(30, lambda: (cutter_move(canvas, is_cutting, duration, cutter_delay, on_complete=on_cutter_complete),
                                           cart_move(canvas, is_cutting, dx, cart_delay, on_complete=on_cart_complete)))
                rolgang_mode(False)
                prdz_mode(False)
                button_gas_pressure.config(state=tk.DISABLED)
                button_oxygen_pressure.config(state=tk.DISABLED)

        elif not is_cutting and cutter_finished and cart_finished:  # Если оба объекта вернулись назад
            is_cutting = True  # Меняем глобальный флаг обратно
            cutter_finished = False
            cart_finished = False

            # Запускаем следующий цикл движения
            canvas.after(200)
            prdz_mode(True)
            valve_mode(True)
            canvas.after(30, lambda: (cutter_move(canvas, is_cutting, duration, cutter_delay, on_complete=on_cutter_complete),
                                        cart_move(canvas, is_cutting, dx, cart_delay, on_complete=on_cart_complete)))
            button_gas_pressure.config(state=tk.ACTIVE)
            button_oxygen_pressure.config(state=tk.ACTIVE)
            lamp_mode(False)
            rolgang_mode(False)

    #завершение процесса резки
    def on_cutter_complete() -> None:
        """
        Функция, которая завершает процесс резки

        Args:
            None

        Returns:
            None
        """
        global cutter_finished
        cutter_finished = True
        check_and_continue()

    #завершение движения вагонетки
    def on_cart_complete() -> None:
        """
        Функция, которая завершает процесс движения вагонетки

        Args:
            None

        Returns:
            None
        """
        global cart_finished
        cart_finished = True
        check_and_continue()

    def pressure_stop() -> None:
        """
        Функция, которая отменяет процесс резки

        Args:
            None

        Returns:
            None
        """
        global cutter_finished
        cancel_anim(cutter_anim_id)
        button_gas_pressure.config(state=tk.DISABLED)
        button_oxygen_pressure.config(state=tk.DISABLED)
        lamp_mode(True)
        cutter_finished = True
        check_and_continue()

    button_gas_pressure.config(command=pressure_stop)
    button_oxygen_pressure.config(command=pressure_stop)

    valve_mode(is_cutting)
    cutter_move(canvas, is_cutting, duration, cutter_delay, on_complete=on_cutter_complete)
    cart_move(canvas, is_cutting, dx, cart_delay, on_complete=on_cart_complete)

################################################################################

button_start = tk.Button(root, text="Запустить объект", font=("Times New Roman", 14), command=start_object)
button_start.place(x=50, y=50)

button_end = tk.Button(root, text="Аварийная кнопка", font=("Times New Roman", 14), command=sys.exit)
button_end.place(x=50, y=100)

button_gas_pressure = tk.Button(root, text="Упало давление газа", font=("Times New Roman", 14))
button_gas_pressure.place(x=300, y=50)

button_oxygen_pressure = tk.Button(root, text="Упало давление кислорода", font=("Times New Roman", 14))
button_oxygen_pressure.place(x=300, y=100)

################################################################################

root.mainloop()
