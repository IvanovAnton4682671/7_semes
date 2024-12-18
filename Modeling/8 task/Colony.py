
from constants import START_LEVEL, MAX_LEVEL, EXPERIENCE_FOR_LEVEL, START_BALANCE, MIN_MAX_INCOME, MIN_MAX_EXPENSE
import random as rnd

start_level = START_LEVEL
max_level = MAX_LEVEL
exp_cap = EXPERIENCE_FOR_LEVEL
start_balance = START_BALANCE
min_max_income = MIN_MAX_INCOME
min_max_expense = MIN_MAX_EXPENSE

class Colony:

    def __init__(self, id: int) -> None:
        """
        Конструктор класса Колония

        Поля:
            id (int): Id колонии
            level (int): Уровень колонии
            exp (int): Опыт колонии
            balance (int): Баланс колонии
            income (int): Доход колонии в цикл
            expense (int): Расход колонии в цикл
            status (str): Статус колонии
            cur_artifact (Artifact): Текущий артефакт колонии

        Args:
            id (int): ID колонии

        Returns:
            None
        """
        self._id = id
        self._level = start_level
        self._exp = 0
        self._balance = start_balance
        self._income = rnd.randint(min_max_income[0], min_max_income[1])
        self._expense = rnd.randint(min_max_expense[0], min_max_expense[1])
        self._status = "active"
        self._cur_artifact = None

    def __str__(self) -> str:
        """
        Метод, который показывает основную информацию о колонии

        Args:
            None

        Returns:
            info (str): Основная информация о колонии
        """
        artifact_info = f"; артефакт = {self._cur_artifact.get_id()}" if self._cur_artifact is not None else ""
        return f"Информация о колонии: id = {self._id}; уровень = {self._level}; опыт = {self._exp}; баланс = {self._balance}; доход = {self._income}; расход = {self._expense}; статус = {self._status}" + artifact_info

##################################################

    def get_id(self) -> int:
        return self._id

    def get_level(self) -> int:
        return self._level

    def get_exp(self) -> int:
        return self._exp

    def set_exp(self, new_exp: int) -> None:
        self._exp = new_exp

    def get_balance(self) -> int:
        return self._balance

    def set_balance(self, new_balance: int) -> None:
        self._balance = new_balance

    def get_income(self) -> int:
        return self._income

    def set_income(self, new_income: int) -> None:
        self._income = new_income

    def get_expense(self) -> int:
        return self._expense

    def set_expense(self, new_expense: int) -> None:
        self._expense = new_expense

    def get_status(self) -> str:
        return self._status

    def get_cur_artifact(self):
        return self._cur_artifact

    def set_cur_artifact(self, new_artifact) -> None:
        self._cur_artifact = new_artifact

##################################################

    def calculate_new_level(self) -> int:
        """
        Метод, который увеличивает уровень колонии на 1
        При достижении уровня >= 10 устанавливает статус колонии как "Победа"

        Args:
            None

        Return:
            status (int): Результат повышения уровня (0 - колония уже победила, 1 - колония победила, 2 - просто повышение уровня)
        """
        if self._level >= 10:
            print(f"Колония {self._id} уже получила максимальный уровень и победила. Дальнейшее повышение уровня невозможно!")
            self._status = "win"
            return 0
        else:
            self._level += 1
            if self._level >= 10:
                print(f"Колония {self._id} получила максимальный уровень и победила!")
                self._status = "win"
                return 1
            print(f"Колония {self._id} получила новый уровень: {self._level}")
            return 2

    def calculate_new_experience(self, exp: int) -> None:
        """
        Метод, который добавляет колонии опыт

        Args:
            exp (int): Опыт, который добавляется колонии

        Returns:
            None
        """
        print(f"Колония {self._id} получила {exp} опыта")
        self._exp += exp
        if self._exp < 0:
            self._exp = 0
        while True:
            if self._exp >= exp_cap:
                status = self.calculate_new_level()
                if status == 0:
                    break
                elif status == 1:
                    self._exp -= exp_cap
                    break
                else:
                    self._exp -= exp_cap
                    continue
            else:
                break

    def calculate_new_balance(self) -> None:
        """
        Метод, который вычисляет новый баланс колонии исходя из дохода/расхода колонии

        Args:
            None

        Returns:
            None
        """
        difference = self._income - self._expense
        self._balance += difference
        print(f"Колония {self._id} заработала {difference}. Новое значение баланса - {self._balance}")
        self.calculate_new_experience(difference)
        print(self)
        if self._balance < 0:
            self._status = "loss"
            print(f"У колонии {self._id} баланс ушёл в минус. Она проиграла!")
