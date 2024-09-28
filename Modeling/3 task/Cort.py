
import math as mt
from Zone import *
from Ball import *
from Player import *
from Dummy import *
from colorama import Fore, Style

class Cort:

    def __init__(self, number_of_squares: int) -> None:
        """
        Метод, который создаёт корт и исходя из заданного числа квадратов строит проекцию корта в виде матрицы

        Args:
            number_of_squares (int): Кол-во квадратов, на которое делится корт

        Returns:
            None
        """
        width = int(mt.sqrt(number_of_squares // 3))                          # получение ширины корта исходя из кол-ва квадратов
        self.matrix = [[0 for i in range(width * 3)] for j in range(width)]   # создание проецирующей матрицы в соотношении 3:1 (длина:ширина)
        # print("Корт в виде матрицы:")
        # for i in range(width):
            # print(self.matrix[i])
        self.all_zones = self.division_into_zones(width * 3, width)           # разделение матрицы на игровые зоны
        # print("Игровые зоны")
        # for zone in self.all_zones.values():                                  # перебор всех зон из словаря
            # print(f"Зона {zone.name}")
            # print(f"min_x: {zone.min_x}")
            # print(f"max_x: {zone.max_x}")
            # print(f"min_y: {zone.min_y}")
            # print(f"max_y: {zone.max_y}")

    def division_into_zones(self, length: int, width: int) -> dict:
        """
        Метод, который создаёт 6 игровых зон

        Args:
            length (int): Длина корта
            width (int): Ширина корта

        Returns:
            dict: Словарь всех игровых зон
        """
        a = Zone(length, width, "A")   # поочерёдное создание всех зон
        b = Zone(length, width, "B")
        c = Zone(length, width, "C")
        d = Zone(length, width, "D")
        e = Zone(length, width, "E")
        f = Zone(length, width, "F")
        return {"A": a, "B": b, "C": c, "D": d, "E": e, "F": f}

    def start_positions(self, a: Zone, d: Zone, player: Player, dummy: Dummy) -> None:
        """
        Метод, который перемещает игрока и болванчика на стартовые позиции (центр A и пересечение F, E, D)

        Args:
            a (Zone): Зона A, в которой будет располагаться игрок
            d (Zone): Зона D, в которой будет располагаться болванчик (берётся клетка, максимально близкая к границе F, E относительно D)
            player (Player): Игрок
            dummy (Dummy): Болванчик

        Returns:
            None
        """
        player_x = round((a.min_x + a.max_x) / 2)   # середина зоны А по X
        player_y = round((a.min_y + a.max_y) / 2)   # середина зоны А по Y
        player.x = player_x
        player.y = player_y
        dummy_x = d.min_x   # край зоны D по X
        dummy_y = round((d.min_y + d.max_y) / 2)   # середина зоны D по Y
        dummy.x = dummy_x
        dummy.y = dummy_y
        # print("Стартовое положение игрока (P) и болванчика (D)")
        # for i in range(len(self.matrix)):
            # for j in range(len(self.matrix[i])):
                # if i == player.y and j == player.x:   # печатаем символ игрока на корте
                    # self.matrix[i][j] = f"{Fore.BLUE}P{Style.RESET_ALL}"
                # elif i == dummy.y and j == dummy.x:   # печатаем символ болванчика на корте
                    # self.matrix[i][j] = f"{Fore.BLUE}D{Style.RESET_ALL}"
                # else:
                    # self.matrix[i][j] = f"{Fore.GREEN}O{Style.RESET_ALL}"   # иначе печатаем ноль (нужно чтобы символы игроков, болванчиков и мячей не дублировались)
        # for row in self.matrix:
            # print(" ".join(row))

    def print_cort_state(self, player: Player, dummy: Dummy, ball: Ball) -> None:
        """
        Метод, который печатает текущее состояние корта

        Args:
            player (Player): Игрок
            dummy (Dummy): Болванчик
            ball (Ball): Мяч

        Returns:
            None
        """
        print("Текущее состояние корта")
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if i == player.y and j == player.x:   # печатаем символ игрока на корте
                    self.matrix[i][j] = f"{Fore.BLUE}P{Style.RESET_ALL}"
                elif i == dummy.y and j == dummy.x:   # печатаем символ болванчика на корте
                    self.matrix[i][j] = f"{Fore.BLUE}D{Style.RESET_ALL}"
                elif i == ball.y and j == ball.x:     # печатаем символ мяча на корте
                    self.matrix[i][j] = f"{Fore.BLUE}B{Style.RESET_ALL}"
                else:
                    self.matrix[i][j] = f"{Fore.GREEN}O{Style.RESET_ALL}"           # иначе печатаем ноль (нужно чтобы символы игроков, болванчиков и мячей не дублировались)
        for row in self.matrix:
            print(" ".join(row))
