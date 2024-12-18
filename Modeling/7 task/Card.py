
class Card:
    def __init__(self, value: int, suit: str, name: str) -> None:
        """
        Метод-конструктор класса Карта

        Поля:
            value (int): Номинал карты
            suit (str): Масть карты
            name (str): Имя карты
            trump (bool): Является ли карта козырной

        Args:
            value (int): Номинал карты
            suit (str): Масть карты
            name (str): Имя карты

        Returns:
            None
        """
        self._value = value
        self._suit = suit
        self._name = name
        self._trump = False

    def __str__(self) -> str:
        """
        Метод, который показывает основную информацию о карте

        Args:
            None

        Returns:
            info (str): Основная информация о карте
        """
        return f"Имя - {self._name}, номинал - {self._value}, масть - {self._suit}, козырь - {self._trump}"

############################## ГЕТТЕРЫ и СЕТТЕРЫ ##############################

    def get_value(self) -> int:
        return self._value

    def get_suit(self) -> str:
        return self._suit

    def get_name(self) -> str:
        return self._name

    def get_trump(self) -> bool:
        return self._trump

    def set_trump(self, trump: bool) -> None:
        self._trump = trump

############################## ГЕТТЕРЫ и СЕТТЕРЫ ##############################
