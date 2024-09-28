
from Zone import *
from Ball import *
import random as rnd

class Dummy:

    def __init__(self, r: int, l: int) -> None:
        """
        Метод, который создаёт объект-болванчика с нужными полями

        Args:
            r (int): Радиус обзора болванчика (полукруг перед ним)
            l (int): Максимальное расстояние перемещения болванчика между атаками

        Returns:
            None
        """
        self.r = r
        self.l = l
        self.x = None   # при инициализации болванчика у него нет координат
        self.y = None
        self.score = 0
        self.game = 0
        self.set = 0
        self.match = 0

    def pitch(self, dict_of_zones: dict, ball: Ball) -> None:
        """
        Метод, который случайным образом выбирает зону для подачи в раунде, клетку в зоне и отправляет туда мяч

        Args:
            dict_of_zones (dict): Словарь всех зон корта
            ball (Ball): Мяч

        Returns:
            None
        """
        rand_zone = rnd.randint(1, 3)
        if rand_zone == 1:
            zone = dict_of_zones.get("A")
        elif rand_zone == 2:
            zone = dict_of_zones.get("B")
        else:
            zone = dict_of_zones.get("C")
        square_x = rnd.randint(zone.min_x, zone.max_x)   # выбираем случайную координату по X в зоне
        square_y = rnd.randint(zone.min_y, zone.max_y)   # выбираем случайную координату по Y в зоне
        ball.new_location(square_x, square_y)            # и отправляем туда мяч
        # print(f"Болванчик отправил мяч в клетку {ball.x}, {ball.y} (это зона {zone.name})")

    def move(self, ball: Ball) -> bool:
        """
        Метод, который реализует перемещение по корту к мячу и определяет, можно ли отбить мяч
        У болванчика тактика простая: сначала сравняться к мячом по Y, а затем по X
        Тут отдельно не рассматриваются случаи когда мяч за спиной или спереди, т.к. у болванчика зона видимости - окружность

        Смысл алгоритма очень прост (рассмотрим на примере оси Y, т.е. вертикаль)
        Если мяч выше болванчика (ball.y < dummy.y), то болванчик проверяет, может ли он "дотянуться" до этой клетки
        с учётом обзора (уменьшает свою координату на self.r); если его координата всё равно больше, то он перемещается на 1 вверх
        (self.y -= 1) и проверяет опять.
        Если же ball.y > (dummy.y + self.r), то болванчик перемещается на 1 вниз (self.y += 1) и проверяет опять.
        С осью X ситуация аналогичная

        Args:
            ball (Ball): Мяч

        Returns:
            flag (bool): Флаг, который отвечает, можно отбить мяч или нет
        """
        ball_x = ball.x
        ball_y = ball.y
        number_of_movements = self.l
        while (self.y + self.r) < ball_y or (self.y - self.r) > ball_y:
            if number_of_movements > 0:
                if (self.y + self.r) < ball_y:
                    self.y += 1
                elif (self.y - self.r) > ball_y:
                    self.y -= 1
                number_of_movements -= 1
            else:
                # print("Болванчик не смог добежать и отбить мяч!")
                return False
        while (self.x + self.r) < ball_x or (self.x - self.r) > ball_x:
            if number_of_movements > 0:
                if (self.x + self.r) < ball_x:
                    self.x += 1
                elif (self.x - self.r) > ball_x:
                    self.x -= 1
                number_of_movements -= 1
            else:
                # print("Болванчик не смог добежать и отбить мяч!")
                return False
        # print("Болванчик смог добежать и отбить мяч!")
        return True
