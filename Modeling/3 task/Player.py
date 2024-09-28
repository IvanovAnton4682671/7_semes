
from Zone import *
from Ball import *
from Dummy import *
import random as rnd

class Player:

    def __init__(self, r: int, l: int) -> None:
        """
        Метод, который создаёт объект-игрока с нужными полями

        Args:
            r (int): Радиус обзора игрока (полукруг перед ним)
            l (int): Максимальное расстояние перемещения игрока между атаками

        Returns:
            None
        """
        self.r = 2 * r
        self.l = l
        self.x = None   # при инициализации игрока у него нет координат
        self.y = None
        self.score = 0
        self.game = 0
        self.set = 0
        self.match = 0

    def pitch(self, zone: Zone, ball: Ball, message: str) -> bool:
        """
        Метод, который выбирает в зоне случайный квадрат и отправляет туда мяч, а также реализует промах

        Args:
            zone (Zone): Зона корта, куда полетит мяч
            ball (Ball): Мяч
            message (str): Сообщение о промахе (если есть)

        Returns:
            flag (bool): Флаг показывает, попал ли игрок из-за промаха в аут
        """
        square_x = rnd.randint(zone.min_x, zone.max_x)   # выбираем случайную координату по X в зоне
        square_y = rnd.randint(zone.min_y, zone.max_y)   # выбираем случайную координату по Y в зоне
        if message == "Не промах":                       # стандартная ситуация (не промах)
            ball.new_location(square_x, square_y)        # и отправляем туда мяч
            # print(f"Игрок отправил мяч в клетку {ball.x}, {ball.y} (это зона {zone.name})")
            return False
        else:   # нестандартная ситуация - промах
            # "ленивый рандом" (при рандоме всё равно может выбраться точка == изначально выбранной, так что используем while)
            square_of_miss_x = rnd.randint(square_x - 1, square_x + 1)
            square_of_miss_y = rnd.randint(square_y - 1, square_y + 1)
            while square_of_miss_x == square_x and square_of_miss_y == square_y:
                square_of_miss_x = rnd.randint(square_x - 1, square_x + 1)
                square_of_miss_y = rnd.randint(square_y - 1, square_y + 1)
            # проверка попадания в аут
            if (square_of_miss_y < zone.min_y and (zone.name == "E" or zone.name == "D")) or (square_of_miss_x > zone.max_x and zone.name == "D") or (square_of_miss_y > zone.max_y and (zone.name == "D" or zone.name == "F")):
                # print(f"Игрок хотел отправить мяч в клетку {square_x}, {square_y} (это зона {zone.name}), но промахнулся и попал в аут ({square_of_miss_x}, {square_of_miss_y})")
                return True
            # а это просто попадание в соседнюю клетку
            else:
                ball.new_location(square_of_miss_x, square_of_miss_y)
                # print(f"Игрок хотел отправить мяч в клетку {square_x}, {square_y} (это зона {zone.name}), но промахнулся и попал в клетку {ball.x}, {ball.y}")
                return False

    def tactic_pitch(self, max_x: int, max_y: int, ball: Ball, message: str, dict_of_zones: dict) -> bool:
        """
        Метод, который отправляем мяч в заданный квадрат, а также реализует промах

        Args:
            max_x (int): Координата X для дальнего квадрата
            max_y (int): Координата Y для дальнего квадрата
            ball (Ball): Мяч
            message (str): Сообщение о промахе (если есть)
            dict_of_zones (dict): Словарь всех зон

        Returns:
            flag (bool): Флаг показывает, попал ли игрок из-за промаха в аут
        """
        if message == "Не промах":
            ball.new_location(max_x, max_y)
            # print(f"Игрок отправил мяч в клетку {ball.x}, {ball.y}")
            return False
        elif message == "Промах":
            square_of_miss_x = rnd.randint(max_x - 1, max_x + 1)
            square_of_miss_y = rnd.randint(max_y - 1, max_y + 1)
            while square_of_miss_x == max_x and square_of_miss_y == max_y:
                square_of_miss_x = rnd.randint(max_x - 1, max_x + 1)
                square_of_miss_y = rnd.randint(max_y - 1, max_y + 1)
            # проверка попадания в аут
            zone_d = dict_of_zones.get("D")
            zone_e = dict_of_zones.get("E")
            if (square_of_miss_y < zone_e.min_y) or (square_of_miss_x > zone_d.max_x) or (square_of_miss_y > zone_d.max_y):
                # print(f"Игрок хотел отправить мяч в клетку {max_x}, {max_y}, но промахнулся и попал в аут ({square_of_miss_x}, {square_of_miss_y})")
                return True
            # а это просто попадание в соседнюю клетку
            else:
                ball.new_location(square_of_miss_x, square_of_miss_y)
                # print(f"Игрок хотел отправить мяч в клетку {max_x}, {max_y}, но промахнулся и попал в клетку {ball.x}, {ball.y}")
                return False

    def zone_selection(self, dict_of_zones: dict, ball: Ball, flag: str, tactic: str, dummy: Dummy) -> None:
        """
        Метод, который случайным образом выбирает зону для подачи в раунде

        Args:
            dict_of_zones (dict): Словарь всех зон корта
            ball (Ball): Мяч
            flag (str): Тип подачи (первая или обычная)
            tactic (str): Тип стратегии (рандомная или дальний квадрат)
            dummy (Dummy): Болванчик

        Returns:
            None
        """
        if tactic == "random":   # тактики нет, выбираем случайную точку
            message = "Не промах"
            if flag == "first":   # первая подача направлена только в E/F
                rand_zone = rnd.randint(1, 2)
                zone = dict_of_zones.get("E") if rand_zone == 1 else dict_of_zones.get("F")
                return self.pitch(zone, ball, message)
            elif flag == "default":   # а обычная подача уже в D, E, F
                rand_zone = rnd.randint(1, 3)
                if rand_zone == 1:
                    zone = dict_of_zones.get("D")
                elif rand_zone == 2:
                    zone = dict_of_zones.get("E")
                else:
                    zone = dict_of_zones.get("F")
                # проверяем, промахнулся ли игрок
                probability_of_miss = rnd.randint(1, 100)
                if 1 <= probability_of_miss <= 5:
                    message = "Промах"
                else:
                    message = "Не промах"
                return self.pitch(zone, ball, message)
            else:
                print(f"Получен некорректный тип подачи: {flag}")
                raise ValueError
        elif tactic == "far square":   # тактика есть, выбираем самую дальнюю точку от болванчика 
            message = "Не промах"
            dummy_x = dummy.x
            dummy_y = dummy.y
            max_x = 0
            max_y = 0
            # зону F не используем, потому что максимальные значения по X охватывает и E, а по Y только D
            zone_d = dict_of_zones.get("D")
            zone_e = dict_of_zones.get("E")
            if flag == "first":
                # выбираем дальнюю координату по X с учётом первой подачи (только в E/F)
                if abs(dummy_x - zone_e.min_x) >= abs(dummy_x - zone_e.max_x):
                    max_x = zone_e.min_x
                else:
                    max_x = zone_e.max_x
                # выбираем дальнюю координату по Y
                if abs(dummy_y - zone_d.min_y) >= abs(dummy_y - zone_d.max_y):
                    max_y = zone_d.min_y
                else:
                    max_y = zone_d.max_y
                return self.tactic_pitch(max_x, max_y, ball, message, dict_of_zones)
            elif flag == "default":
                # выбираем дальнюю координату по X с учётом не первой подачи (D, E, F)
                if abs(dummy_x - zone_e.min_x) >= abs(dummy_x - zone_d.max_x):
                    max_x = zone_e.min_x
                else:
                    max_x = zone_d.max_x
                # выбираем дальнюю координату по Y
                if abs(dummy_y - zone_d.min_y) >= abs(dummy_y - zone_d.max_y):
                    max_y = zone_d.min_y
                else:
                    max_y = zone_d.max_y
                # проверяем, промахнулся ли игрок
                probability_of_miss = rnd.randint(1, 100)
                if 1 <= probability_of_miss <= 5:
                    message = "Промах"
                else:
                    message = "Не промах"
                return self.tactic_pitch(max_x, max_y, ball, message, dict_of_zones)

    def move(self, ball: Ball) -> bool:
        """
        Метод, который реализует перемещение по корту к мячу и определяет, можно ли отбить мяч
        Отдельно рассматриваются случаи когда мяч за спиной у игрока и когда он спереди

        Ситуация с мячом позади: игрок сначала пытается сравняться с мячом по оси X, чтобы быть в одной вертикали
        Это делается для того, чтобы игрок смог воспользоваться своим обзором (полукруг перед собой + одна с ним полоса по оси Y)
        Когда он сравнялся с мячом, то начинает проверять, достаёт ли до мяча с учётом обзора (self.x + self.r)

        Ситуация, когда мяч спереди игрока: игрок сразу пользуется обзором и пробует поравняться с мячом по условию (self.y + self.r)
        или (self.y - self.r) (когда мяч снизу или сверху соответственно), а затем аналогично по оси X

        Args:
            ball (Ball): Мяч

        Returns:
            flag (bool): Флаг, который отвечает, можно отбить мяч или нет
        """
        ball_x = ball.x
        ball_y = ball.y
        number_of_movements = self.l
        if ball_x < self.x:
            while self.x > ball_x:
                if number_of_movements > 0:
                    self.x -= 1
                    number_of_movements -= 1
                else:
                    # print("Игрок не смог добежать и отбить мяч!")
                    return False
            while (self.y + self.r) < ball.y or (self.y - self.r) > ball.y:
                if number_of_movements > 0:
                    if (self.y + self.r) < ball_y:
                        self.y += 1
                    elif (self.y - self.r) > ball_y:
                        self.y -= 1
                    number_of_movements -= 1
                else:
                    # print("Игрок не смог добежать и отбить мяч!")
                    return False
        elif ball_x > self.x:
            while (self.y + self.r) < ball_y or (self.y - self.r) > ball_y:
                if number_of_movements > 0:
                    if (self.y + self.r) < ball_y:
                        self.y += 1
                    elif (self.y - self.r) > ball_y:
                        self.y -= 1
                    number_of_movements -= 1
                else:
                    # print("Игрок не смог добежать и отбить мяч!")
                    return False
            while (self.x + self.r) < ball_x or (self.x - self.r) > ball_x:
                if number_of_movements > 0:
                    if (self.x + self.r) < ball_x:
                        self.x += 1
                    elif (self.x - self.r) > ball_x:
                        self.x -= 1
                    number_of_movements -= 1
                else:
                    # print("Игрок не смог добежать и отбить мяч!")
                    return False
        # print("Игрок смог добежать и отбить мяч!")
        return True