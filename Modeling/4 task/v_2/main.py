
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

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

def calculate_x_i(big_T_1: float, big_T_2: float, big_D: float, x_i_prev: float, x_i_prev_2: float, delta_t: float, u_i: float) -> float:
    """
    Функция, которая рассчитывает новое состояние среды

    Args:
        big_T_1 (float): Коэффициент среды
        big_T_2 (float): Коэффициент среды
        big_D (float): Коэффициент воздействия
        x_i_prev (float): Предыдущее состояние среды
        x_i_prev_2 (float): Предыдущее перед предыдущим состояние среды
        delta_t (float): Временной шаг
        u_i (float): Воздействие агента на среду

    Returns:
        result (float): Новое состояние среды
    """
    return ((2 * big_T_2 * x_i_prev) - (big_T_2 * x_i_prev_2) + (big_T_1 * delta_t * x_i_prev) + (big_D * (delta_t**2) * u_i) + (delta_t**2)) / (big_T_2 + (big_T_1 * delta_t) + delta_t**2)

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

def simulation(t: float, delta_t: float, t_stop: int, tau: float, k: float, big_T_1: float, big_T_2: float, big_D: float, max_error_threshold: float) -> float:
    """
    Функция, которая проводит симуляцию системы до времени t_stop

    Args:
        t (float): Начальный момент времени
        delta_t (float): Временной шаг
        t_stop (int): Конец симуляции
        tau (float): Величина tau
        k (float): Параметр агента
        big_T_1 (float): Параметр среды
        big_T_2 (float): Параметр среды
        big_D (float): Параметр воздействия
        max_error_threshold (float): Порог ошибки устойчивости системы

    Returns:
        result (float): Максимальная ошибка системы
    """
    #заполняем массивы начальными данными для того, чтобы они все были одной длины
    all_time = [0]
    all_g_t = [0]
    all_x_i = [0, 0]
    all_stability = [0]

    while t < t_stop:
        all_time.append(t)

        cur_g_t = calculate_g_t(t, t_stop)
        all_g_t.append(cur_g_t)

        t_minus_tau = t - tau
        cur_x_t_minus_tau = calculate_interpolated_x_i(all_time, all_x_i, t_minus_tau)
        cur_u_t = calculate_u_t(k, cur_g_t, cur_x_t_minus_tau)
        cur_x_i = calculate_x_i(big_T_1, big_T_2, big_D, all_x_i[-1], all_x_i[-2], delta_t, cur_u_t)
        all_x_i.append(cur_x_i)

        cur_stability = check_stability(cur_g_t, cur_x_i)
        all_stability.append(cur_stability)

        if cur_stability > max_error_threshold:
            return -1

        t += delta_t
    return max(all_stability)

def refine_simulate(t: float, delta_t: float, t_stop: int, prev_tau_list: list, prev_k_list: list, prev_big_T_1_list: list, prev_big_T_2_list: list, prev_big_D_list: list, max_error_threshold: float, step: float) -> list:
    """
    Функция, реализующая сужение диапазона значений tau, k, big_T_1, big_T_2, big_D для поиска оптимальных значений для устойчивости системы

    Args:
        t (float): Начальный момент времени
        delta_t (float): Временной шаг
        t_stop (int): Конец симуляции
        prev_tau_list (list): Список предыдущих значений tau
        prev_k_list (list): Список предыдущих значений k
        prev_big_T_1_list (list): Список предыдущих значений big_T_1
        prev_big_T_2_list (list): Список предыдущих значений big_T_2
        prev_big_D_list (list): Список предыдущих значений big_D
        max_error_threshold (float): Порог ошибки устойчивости системы
        step (float): Шаг уменьшения пределов параметров

    Returns:
        list, list, list, list, list, list (list): 6 списков, описывающие 5 параметров (tau, k, big_T_1, big_T_2, big_D) и максимальные ошибки для каждой комбинации параметров
    """
    tau_list = prev_tau_list
    k_list = prev_k_list
    big_T_1_list = prev_big_T_1_list
    big_T_2_list = prev_big_T_2_list
    big_D_list = prev_big_D_list

    for i in range(10):
        print(f"{i + 1} попытка сужения диапазонов значений")

        tau_critical = []
        tau_stable = []
        x1, x2, y1, y2, z, colors = [], [], [], [], [], []
        error_occurred = False

        print("Начало симуляции:")
        for tau in tau_list:
            for k in k_list:
                for big_T_1 in big_T_1_list:
                    for big_T_2 in big_T_2_list:
                        for big_D in big_D_list:
                            max_stability = simulation(t, delta_t, t_stop, tau, k, big_T_1, big_T_2, big_D, max_error_threshold)
                            if max_stability == -1:
                                tau_critical.append((tau, k, big_T_1, big_T_2, big_D))
                                error_occurred = True
                            else:
                                tau_stable.append((tau, k, big_T_1, big_T_2, big_D))
                            x1.append(tau)
                            x2.append(k)
                            y1.append(big_T_1)
                            y2.append(big_T_2)
                            z.append(big_D)
                            colors.append(max_stability)
            print(f"Симуляция для tau = {tau} закончена")

        if error_occurred and tau_stable:
            tau_min = min([t[0] for t in tau_stable])
            tau_max = max([t[0] for t in tau_stable]) - step
            k_min = min([t[1] for t in tau_stable])
            k_max = max([t[1] for t in tau_stable]) - step
            big_T_1_min = min([t[2] for t in tau_stable])
            big_T_1_max = max([t[2] for t in tau_stable]) - step
            big_T_2_min = min([t[3] for t in tau_stable])
            big_T_2_max = max([t[3] for t in tau_stable]) - step
            big_D_min = min([t[4] for t in tau_stable])
            big_D_max = max([t[4] for t in tau_stable]) - step

            tau_list = np.linspace(tau_min, tau_max, 4)
            k_list = np.linspace(k_min, k_max, 4)
            big_T_1_list = np.linspace(big_T_1_min, big_T_1_max, 4)
            big_T_2_list = np.linspace(big_T_2_min, big_T_2_max, 4)
            big_D_list = np.linspace(big_D_min, big_D_max, 4)
            print(f"Новые диапазоны: tau [{tau_min}, {tau_max}], k [{k_min}, {k_max}], T_1 [{big_T_1_min}, {big_T_1_max}], T_2 [{big_T_2_min}, {big_T_2_max}], D [{big_D_min}, {big_D_max}]")
        elif not tau_stable:
            print("Все комбинации параметров приводят к ошибке")
            break
        else:
            print("Система устойчива при данных параметрах")
            break
    return x1, x2, y1, y2, z, colors

def dot_graphic(x1: list, x2: list, y1: list, y2: list, z: list, colors: list, slice_1: str, slice_2: str) -> None:
    """
    Функция, которая строит точечный 3-мерный график, срезая 2 измерения

    Args:
        x1 (list): Список значений tau
        x2 (list): Список значений k
        y1 (list): Список значений T1
        y2 (list): Список значений T2
        z (list): Список значений D
        colors (list): Список кодировки цветов ошибки системы
        slice_1 (str): Первое срезаемое измерение
        slice_2 (str): Втрое срезаемое измерение

    Returns:
        None
    """
    if slice_1 == "big_T_2" and slice_2 == "big_D":
        flat_1 = x1[:, :, :, 0, 0]
        flat_2 = x2[:, :, :, 0, 0]
        flat_3 = y1[:, :, :, 0, 0]
        flat_4 = colors[:, :, :, 0, 0]
        x_label = "Tau"
        y_label = "K"
        z_label = "T1"
        title = "График с цветовой кодировкой устойчивости системы (Tau, K, T1)"
    elif slice_1 == "big_T_1" and slice_2 == "big_T_2":
        flat_1 = x1[:, :, 0, 0, :]
        flat_2 = x2[:, :, 0, 0, :]
        flat_3 = z[:, :, 0, 0, :]
        flat_4 = colors[:, :, 0, 0, :]
        x_label = "Tau"
        y_label = "K"
        z_label = "D"
        title = "График с цветовой кодировкой устойчивости системы (Tau, K, D)"
    elif slice_1 == "big_T_1" and slice_2 == "big_D":
        flat_1 = x1[:, :, 0, :, 0]
        flat_2 = x2[:, :, 0, :, 0]
        flat_3 = y2[:, :, 0, :, 0]
        flat_4 = colors[:, :, 0, :, 0]
        x_label = "Tau"
        y_label = "K"
        z_label = "T2"
        title = "График с цветовой кодировкой устойчивости системы (Tau, K, T2)"

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    img = ax.scatter(flat_1.flatten(), flat_2.flatten(), flat_3.flatten(), c=flat_4.flatten(), cmap=cm.viridis)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)
    plt.title(title)
    fig.colorbar(img, ax=ax, label="Ошибка системы")
    plt.show()

def surf_graphic(x1: list, x2: list, y1: list, y2: list, z: list, colors: list, slice: str):
    """
    Функция, которая строит поверхностный 3-мерный график, выбирая 2-ое измерение

    Args:
        x1 (list): Список значений tau
        x2 (list): Список значений k
        y1 (list): Список значений T1
        y2 (list): Список значений T2
        z (list): Список значений D
        colors (list): Список кодировки цветов ошибки системы
        slice (str): Выбор второго измерения

    Returns:
        None
    """
    if slice == "K":
        tau_grid, slice_grid = np.meshgrid(x1[:, 0, 0, 0, 0], x2[0, :, 0, 0, 0])
        z_values = colors[:, :, 0, 0, 0]
        y_label = "K"
        title = "График с цветовой кодировкой устойчивости системы (Tau, K)"
    elif slice == "T1":
        tau_grid, slice_grid = np.meshgrid(x1[:, 0, 0, 0, 0], y1[0, 0, :, 0, 0])
        z_values = colors[:, 0, :, 0, 0]
        y_label = "T1"
        title = "График с цветовой кодировкой устойчивости системы (Tau, T1)"
    elif slice == "T2":
        tau_grid, slice_grid = np.meshgrid(x1[:, 0, 0, 0, 0], y2[0, 0, 0, :, 0])
        z_values = colors[:, 0, 0, :, 0]
        y_label = "T2"
        title = "График с цветовой кодировкой устойчивости системы (Tau, T2)"
    elif slice == "D":
        tau_grid, slice_grid = np.meshgrid(x1[:, 0, 0, 0, 0], z[0, 0, 0, 0, :])
        z_values = colors[:, 0, 0, 0, :]
        y_label = "D"
        title = "График с цветовой кодировкой устойчивости системы (Tau, D)"
    
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(tau_grid, slice_grid, z_values, cmap=cm.viridis)
    ax.set_xlabel("Tau")
    ax.set_ylabel(y_label)
    ax.set_zlabel("Ошибка системы")
    plt.title(title)
    fig.colorbar(surf, ax=ax, label="Ошибка системы")
    plt.show()

def all_graphics(t: float, delta_t: float, t_stop: float, tau_list: list, k_list: list, big_T_1_list: list, big_T_2_list: list, big_D_list: list, max_error_threshold: int, step: int) -> None:
    """
    Функция, которая выполняет симуляции и строит графики по разным параметрам

    Args:
        t (float): Начальный момент времени
        delta_t (float): Временной шаг
        t_stop (float): Конец симуляции
        tau_list (list): Список значений tau
        k_list (list): Список значений K
        big_T_1_list (list): Список значений T1
        big_T_2_list (list): Список значений T2
        big_D_list (list): Список значений D
        max_error_threshold (int): Порог ошибки устойчивости системы
        step (int): Шаг уменьшения пределов параметров

    Returns:
        None
    """
    x1, x2, y1, y2, z, colors = refine_simulate(t, delta_t, t_stop, tau_list, k_list, big_T_1_list, big_T_2_list, big_D_list, max_error_threshold, step)

    x1 = np.array(x1)
    x2 = np.array(x2)
    y1 = np.array(y1)
    y2 = np.array(y2)
    z = np.array(z)
    colors = np.array(colors)

    n = len(tau_list)

    new_x1 = x1.reshape(n, n, n, n, n)
    new_x2 = x2.reshape(n, n, n, n, n)
    new_y1 = y1.reshape(n, n, n, n, n)
    new_y2 = y2.reshape(n, n, n, n, n)
    new_z = z.reshape(n, n, n, n, n)
    new_colors = colors.reshape(n, n, n, n, n)

    dot_graphic(new_x1, new_x2, new_y1, new_y2, new_z, new_colors, "big_T_2", "big_D")
    dot_graphic(new_x1, new_x2, new_y1, new_y2, new_z, new_colors, "big_T_1", "big_T_2")
    dot_graphic(new_x1, new_x2, new_y1, new_y2, new_z, new_colors, "big_T_1", "big_D")

    surf_graphic(new_x1, new_x2, new_y1, new_y2, new_z, new_colors, "K")
    surf_graphic(new_x1, new_x2, new_y1, new_y2, new_z, new_colors, "T1")
    surf_graphic(new_x1, new_x2, new_y1, new_y2, new_z, new_colors, "T2")
    surf_graphic(new_x1, new_x2, new_y1, new_y2, new_z, new_colors, "D")

t = 0.00
delta_t = 0.01
t_stop = 10.00
tau_list = np.linspace(0.00, 10.0, 4)
k_list = np.linspace(0.00, 10.0, 4)
big_T_1_list = np.linspace(0.00, 10.0, 4)
big_T_2_list = np.linspace(0.00, 10.0, 4)
big_D_list = np.linspace(0.00, 10.0, 4)
max_error_threshold = 1
step = 1

if __name__ == "__main__":
    all_graphics(t, delta_t, t_stop, tau_list, k_list, big_T_1_list, big_T_2_list, big_D_list, max_error_threshold, step)
