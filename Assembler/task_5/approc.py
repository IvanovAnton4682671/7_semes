
from scipy.stats import linregress
import matplotlib.pyplot as plt

# Объединение всех точек каждого графика для построения единой зависимости
# График захвата (а)
t_capture_all = [0, 40, 73, 105, 120]
I_capture_all = [0, 140, 260, 250, 260]

# График отпускания (б)
t_release_all = [0, 20, 35, 75, 120]
I_release_all = [260, 250, 260, 140, 0]

# Линейная аппроксимация для захвата (а)
slope_capture, intercept_capture, _, _, _ = linregress(t_capture_all, I_capture_all)
I_capture_approx = [slope_capture * t + intercept_capture for t in t_capture_all]

# Линейная аппроксимация для отпускания (б)
slope_release, intercept_release, _, _, _ = linregress(t_release_all, I_release_all)
I_release_approx = [slope_release * t + intercept_release for t in t_release_all]

# Построение графиков для визуализации
plt.figure(figsize=(10, 6))

# Захват (а)
plt.plot(t_capture_all, I_capture_all, 'bo-', label='Захват (исходные точки)')
plt.plot(t_capture_all, I_capture_approx, 'b--', label=f'Захват (аппроксимация): I = {slope_capture:.2f}t + {intercept_capture:.2f}')

# Отпускание (б)
plt.plot(t_release_all, I_release_all, 'ro-', label='Отпускание (исходные точки)')
plt.plot(t_release_all, I_release_approx, 'r--', label=f'Отпускание (аппроксимация): I = {slope_release:.2f}t + {intercept_release:.2f}')

# Настройка графика
plt.title("Линейная аппроксимация для графиков захвата и отпускания")
plt.xlabel("t, мс")
plt.ylabel("I, мА")
plt.grid()
plt.legend()
plt.show()

# Возвращаем уравнения аппроксимации
print(slope_capture)
print(intercept_capture)
print(slope_release)
print(intercept_release)
