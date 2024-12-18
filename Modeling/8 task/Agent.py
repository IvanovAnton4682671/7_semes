
from Colony import *
from constants import PRICE_STEP

price_step = PRICE_STEP

class Agent:
    def __init__(self, id: int, colony: Colony) -> None:
        """
        Конструктор класса Агент

        Поля:
            id (int): ID агента
            colony (Colony): Колония, которой управляет агент

        Args:
            id (int): ID агента
            colony (Colony): Колония, которой управляет агент

        Returns:
            None
        """
        self._id = id
        self._colony = colony

    def __str__(self) -> str:
        """
        Метод, который возвращает основную информацию об агенте

        Args:
            None

        Returns:
            info (str): основная информация об агенте
        """
        return f"Агент {self._id} управляет колонией {self._colony.get_id()}"

##################################################

    def get_colony(self) -> Colony:
        return self._colony

##################################################

    def place_a_bet(self, cur_price: int, cur_balance: int):
        """
        Метод, который пробует сделать ставку для покупки артефакта

        Args:
            cur_price (int): Текущая цена артефакта
            cur_balance (int): Текущий баланс колонии агента

        Returns:
            tuple (tuple): статус ставки и величина ставки
        """
        new_bet = 0
        if cur_price + price_step < cur_balance:
            new_bet = cur_price + price_step
            return True, new_bet
        else:
            return False, new_bet
