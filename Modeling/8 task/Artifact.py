
from constants import ARTIFACT_N, AUCTION_INTERVAL, EXPERIENCE_FOR_LEVEL
from Colony import *

artifact_n = ARTIFACT_N
auction_interval = AUCTION_INTERVAL
experience_for_level = EXPERIENCE_FOR_LEVEL

class Artifact:
    def __init__(self, id: int, duration: int) -> None:
        """
        Конструктор класса Артефакт

        Поля:
            id (int): ID артефакта
            duration (int): Сколько итераций работает артефакт

        Args:
            id (int): ID артефакта
            start_duration (int): Изначальное количество итераций длительности артефакта
            cur_duration (int): Текущее количество итераций длительности артефакта

        Returns:
            None
        """
        self._id = id
        self._start_duration = duration
        self._cur_duration = duration

##################################################

    def get_id(self) -> int:
        return self._id

    def get_duration(self) -> int:
        return self._cur_duration

##################################################

    def apply_to_colony(self, colony, **kwargs):
        """
        Метод, который применяет артефакт к колонии

        Args:
            colony (Colony): Колония, к которой применяется артефакт
            kwargs: Дополнительный параметры, которые нужны каждому конкретному артефакту

        Returns:
            None
        """
        if self._id == 30:
            self._apply_artifact_30(colony, **kwargs)
        elif self._id == 42:
            self._apply_artifact_42(colony, **kwargs)
        elif self._id == 48:
            self._apply_artifact_48(colony, **kwargs)
        elif self._id == 49:
            self._apply_artifact_49(colony, **kwargs)
        elif self._id == 64:
            self._apply_artifact_64(colony, **kwargs)
        else:
            print(f"Артефакт {self._id} неизвестен и не может быть применён!")

    def _apply_artifact_30(self, colony: Colony, **kwargs):
        """
        Метод артефакта 30
        Данный артефакт снижает расход на n единиц на протяжении n итераций

        Args:
            colony (Colony): Колония, к которой применяется артефакт

        Returns:
            None
        """
        if self._cur_duration > 0:
            new_colony_expense = colony.get_expense() - artifact_n
            colony.set_expense(new_colony_expense)
            print(f"Артефакт 30 применился к колонии {colony.get_id()}: расход снижен на {artifact_n} на {artifact_n} итераций!")
            self._cur_duration -= 1
        if self._cur_duration == 0:
            new_colony_expense = colony.get_expense() + artifact_n
            colony.set_expense(new_colony_expense)
            print(f"Артефакт 30 больше не действует у колонии {colony.get_id()}")

    def _apply_artifact_42(self, colony: Colony, **kwargs):
        """
        Метод артефакта 42
        Данный артефакт: увеличивает баланс на n до следующего аукциона; уменьшает расход на n на n итераций;
        обнуляет опыт какой-то колонии 1 раз

        Args:
            colony (Colony): Колония к которой применяются положительные эффекты
            enemy_colony (from kwargs): Колония, у которой обнуляется опыт

        Returns:
            None
        """
        if self._cur_duration == self._start_duration:
            enemy_colony = kwargs["enemy_colony"]
            enemy_colony.set_exp(0)
            print(f"Артефакт 42 применился к колонии {colony.get_id()}: колонии {enemy_colony.get_id()} обнулили опыт!")
        if self._cur_duration > 0:
            new_colony_balance = colony.get_balance() + artifact_n
            colony.set_balance(new_colony_balance)
            new_colony_expense = colony.get_expense() - artifact_n
            colony.set_expense(new_colony_expense)
            print(f"Артефакт 42 применился к колонии {colony.get_id()}: баланс увеличен на {artifact_n} до следующего аукциона; расход снижен на {artifact_n} на {artifact_n} итераций!")
            self._cur_duration -= 1
        if self._cur_duration == 0:
            new_colony_balance = colony.get_balance() - artifact_n
            colony.set_balance(new_colony_balance)
            new_colony_expense = colony.get_expense() + artifact_n
            colony.set_expense(new_colony_expense)
            print(f"Артефакт 42 больше не действует у колонии {colony.get_id()}")

    def _apply_artifact_48(self, colony: Colony, **kwargs):
        """
        Метод артефакта 48
        Данный артефакт: увеличивает текущий баланс на n% на n итераций; увеличивает текущий доход на n% от расхода до следующего аукциона

        Args:
            colony (Colony): Колония, к которой применяются эффекты артефакта

        Returns:
            None
        """
        if self._cur_duration > 0:
            new_colony_balance = colony.get_balance() + (colony.get_balance() / 100 * artifact_n)
            colony.set_balance(new_colony_balance)
            new_colony_income = colony.get_income() + (colony.get_expense() / 100 * artifact_n)
            colony.set_income(new_colony_income)
            print(f"Артефакт 48 применился к колонии {colony.get_id()}: баланс увеличен на {artifact_n}% на {artifact_n} итераций; доход увеличен на {artifact_n}% от расхода на {artifact_n} итераций!")
            self._cur_duration -= 1
        if self._cur_duration == 0:
            new_colony_balance = colony.get_balance() - (colony.get_balance() / 100 * artifact_n)
            colony.set_balance(new_colony_balance)
            new_colony_income = colony.get_income() - (colony.get_expense() / 100 * artifact_n)
            colony.set_income(new_colony_income)
            print(f"Артефакт 48 больше не действует у колонии {colony.get_id()}")

    def _apply_artifact_49(self, colony: Colony, **kwargs):
        """
        Метод артефакта 49
        Данный артефакт: увеличивает текущий баланс на n единоразово; увеличивает опыт на n% единоразово; увеличивает доход на n% от расхода на n итераций

        Args:
            colony (Colony): Колония, к которой применяется артефакт

        Returns:
            None
        """
        if self._cur_duration == self._start_duration:
            new_colony_balance = colony.get_balance() + artifact_n
            colony.set_balance(new_colony_balance)
            new_colony_exp = colony.get_exp() + experience_for_level / 100 * artifact_n
            colony.calculate_new_experience(new_colony_exp)
            print(f"Артефакт 49 применился к колонии {colony.get_id()}: баланс увеличен на {artifact_n}; опыт увеличен на {artifact_n}%!")
        if self._cur_duration > 0:
            new_colony_income = colony.get_income() + (colony.get_expense() / 100 * artifact_n)
            colony.set_income(new_colony_income)
            print(f"Артефакт 49 применился к колонии {colony.get_id()}: доход увеличен на {artifact_n}% от расхода на {artifact_n} итераций!")
            self._cur_duration -= 1
        if self._cur_duration == 0:
            new_colony_income = colony.get_income() - (colony.get_expense() / 100 * artifact_n)
            colony.set_income(new_colony_income)
            print(f"Артефакт 49 больше не действует у колонии {colony.get_id()}")

    def _apply_artifact_64(self, colony: Colony, **kwargs):
        """
        Метод артефакта 64
        Данный артефакт: даёт n опыта на n итераций; обнуляет расход до следующего аукциона

        Args:
            colony (Colony): Колония, к которой применяется артефакт

        Returns:
            None
        """
        if self._cur_duration > 0:
            new_colony_exp = colony.get_exp() + artifact_n
            colony.set_exp(new_colony_exp)
            colony.set_expense(0)
            print(f"Артефакт 64 применился к колонии {colony.get_id()}: опыт увеличен на {artifact_n}; расход обнулён на {artifact_n} итераций!")
            self._cur_duration -= 1
        if self._cur_duration == 0:
            new_colony_exp = colony.get_exp() - artifact_n
            colony.set_exp(new_colony_exp)
            new_colony_expense = colony.get_income() - 10
            colony.set_expense(new_colony_expense)
            print(f"Артефакт 64 больше не действует у колонии {colony.get_id()}")
