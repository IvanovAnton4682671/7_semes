
# Параметры для ЦАП
n_c = 10  # разрядность ЦАП
u1_c = 0  # минимальное значение тока, мА
u2_c = 300  # максимальное значение тока, мА

# Токовые значения, которые необходимо преобразовать
current_values = [0, 140, 250, 260, 300]  # мА

# Формула для преобразования u -> D
def calculate_equiv(u, u1, u2, n):
    return round((u - u1) / (u2 - u1) * (2 ** n))

# Расчёт эквивалентов
equivalents_values = [calculate_equiv(u, u1_c, u2_c, n_c) for u in current_values]
print(equivalents_values)
