
from collections import deque

from Card import Card

class BitoDeck:
    def __init__(self) -> None:
        """
        Метод-конструктор класса Колода бито

        Поля:
            deck (deque): Колода бито

        Args:
            None

        Returns:
            None
        """
        self._deck = deque(maxlen=52)

    def __str__(self) -> str:
        """
        Метод, который показывает основную информацию о колоде бито

        Args:
            None

        Returns:
            info (str): Основная информация о колоде бито
        """
        deck_info = f"Количество карт в колоде бито - {len(self._deck)}\n"
        for card in self._deck:
            deck_info += f"{card}\n"
        return deck_info

############################## ГЕТТЕРЫ и СЕТТЕРЫ ##############################

    def get_deck(self) -> deque[Card]:
        return self._deck

    def set_deck_card(self, card: Card) -> None:
        self._deck.append(card)

############################## ГЕТТЕРЫ и СЕТТЕРЫ ##############################

    def give_a_card(self, card: Card) -> bool:
        """
        Метод, который принимает карту в колоду бито
        Карта принимается в колоду, если колода бито не переполнена и такой карты ещё нет в колоде бито

        Args:
            card (Card): Карта, которую кладут в колоду бито

        Returns:
            status (bool): Результат добавления карты в колоду бито (если получилось - True, иначе False)
        """
        if len(self._deck) < 52 and card.get_value() not in [card.get_value() for card in self._deck]:
            self._deck.append(card)
            return True
        else:
            print("Колода бито переполнена!")
            return False
