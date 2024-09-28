
class Zone:

    def __init__(self, length: int, width: int, name: str) -> None:
        """
        Метод, который задаёт зоне координаты исходя из её названия (у каждой зоны своё положение на корте)

        Args:
            length (int): Длина корта
            width (int): Ширина корта
            name (str): Название зоны

        Returns:
            None
        """
        self.name = name                   # задаём зоне имя
        if name == "A":                    # исходя из имени выделяем зоне конкретные координаты (у каждой зоны своё положение)
            self.min_x = 0
            self.max_x = (length // 4) - 1
            self.min_y = 0
            self.max_y = width - 1
        elif name == "B":
            self.min_x = length // 4
            self.max_x = (length // 2) - 1
            self.min_y = width // 2
            self.max_y = width - 1
        elif name == "C":
            self.min_x = length // 4
            self.max_x = (length // 2) - 1
            self.min_y = 0
            self.max_y = (width // 2) - 1
        elif name == "D":
            self.min_x = (length // 4) * 3
            self.max_x = length - 1
            self.min_y = 0
            self.max_y = width - 1
        elif name == "E":
            self.min_x = length // 2
            self.max_x = ((length // 4) * 3) - 1
            self.min_y = 0
            self.max_y = (width // 2) - 1
        elif name == "F":
            self.min_x = length // 2
            self.max_x = ((length // 4) * 3) - 1
            self.min_y = width // 2
            self.max_y = width - 1
        else:
            print(f"Получено некорректное имя зоны: {name}")   # если получили неверное имя
            raise ValueError                                   # то вызываем ошибку значения (передали неверное значение)
