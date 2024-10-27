
import numpy as np
import matplotlib.pyplot as plt

def calculate_g_t(t: float, t_stop: int) -> int:
    """
    Функция, которая вычисляет целевое состояние среды в зависимости от времени

    Args:
        t (float): Текущее время
        t_stop (int): Лимит симуляции

    Returns:
        result (int): Текущее целевое состояние среды
    """
    mid = t_stop / 2
    return 0 if 0 <= t <= mid else 1

def calculate_u_t(k: float, g_t: int, x_t_tau: float) -> float:
    """
    Функция, которая вычисляет воздействие агента на среду

    Args:
        k (float): Коэффициент агента
        g_t (int): Целевое состояние среды
        x_t_tau (float): Предыдущее состояние среды

    Returns:
        result (float): Воздействие агента на среду
    """
    return k * (g_t - x_t_tau)

def calculate_interpolated_x_i(all_time: list, all_x_i: list, t_minus_tau: float) -> float:
    """
    Функция, которая реализует линейную интерполяцию для вычисления значения x(t-tau) вместо подбора ближайшего значения

    Args:
        all_time (list): Список всех моментов времени симуляции
        all_x_i (list): Список всех значений функции x(t)
        t_minus_tau (float): Текущее значение t-tau, для которого ищем значение функции

    Returns:
        result (float): Значение функции x(t) для заданного t-tau
    """
    if t_minus_tau <= all_time[0]:
        return all_x_i[0]
    return np.interp(t_minus_tau, all_time, all_x_i)

def calculate_x_i(big_T: float, delta_t: float, x_i_prev: float, u_i: float) -> float:
    """
    Функция, которая вычисляет новое состояние среды

    Args:
        big_T (float): Коэффициент среды
        delta_t (float): Временной шаг
        x_i_prev (float): Предыдущее состояние среды
        u_i (float): Воздействие агента на среду

    Returns:
        result (float): Новое состояние среды
    """
    return (big_T / (big_T + delta_t)) * x_i_prev + (delta_t / (big_T + delta_t)) * u_i

def check_stability(g_t: int, x_t: float) -> float:
    """
    Функция, вычисляющая разность между целевым и текущим состоянием среды

    Args:
        g_t (int): Целевое состояние
        x_t (float): Текущее состояние

    Returns:
        result (float): Разность целевого и текущего состояния
    """
    return abs(g_t - x_t)

def simulation(t: float, delta_t: float, t_stop: int, tau: float, k: float, big_T: float) -> list:
    """
    Функция, которая проводит симуляцию системы до времени t_stop

    Args:
        t (float): Начальный момент времени
        delta_t (float): Временной шаг
        t_stop (int): Конец симуляции
        tau (float): Величина tau
        k (float): Параметр агента
        big_T (float): Параметр среды

    Returns:
        all_time (list): Список всего времени симуляции
        all_g_t (list): Список всех целевых состояний системы
        all_x_i (list): Список всех вычисленных состояний системы
        all_stability (list): Список ошибок (проверка стабильности)
    """
    all_time = []
    all_g_t = []
    all_x_i = [0]
    all_stability = []

    while t < t_stop:
        all_time.append(t)

        cur_g_t = calculate_g_t(t, t_stop)
        all_g_t.append(cur_g_t)

        t_minus_tau = t - tau
        cur_x_t_minus_tau = calculate_interpolated_x_i(all_time, all_x_i, t_minus_tau)
        cur_u_t = calculate_u_t(k, cur_g_t, cur_x_t_minus_tau)
        cur_x_i = calculate_x_i(big_T, delta_t, all_x_i[-1], cur_u_t)
        all_x_i.append(cur_x_i)

        cur_stability = check_stability(cur_g_t, cur_x_i)
        all_stability.append(cur_stability)
        t += delta_t
    return all_time, all_g_t, all_x_i, all_stability

t = 0.00
delta_t = 0.01
t_stop = 10
tau = 2
k = 3
big_T = 3

all_time, all_g_t, all_x_i, all_stability = simulation(t, delta_t, t_stop, tau, k, big_T)

plt.figure(figsize=(10, 6))
plt.plot(all_time, all_stability, label="Вычисленные состояния среды", color="red")
plt.plot(all_time, all_x_i[1:], label="Состояния среды", color="green")
plt.plot(all_time, all_g_t, label="Целевые состояния среды", color="blue")
plt.xlabel("Время")
plt.ylabel("Состояния среды")
plt.title(f"Сравнение результатов (tau = {tau}; k = {k}; T = {big_T})")
plt.legend()
plt.grid(True)
plt.show()
