
from collections import deque
import random as rnd

from Card import Card

class MainDeck:
    def __init__(self, list_of_cards: list) -> None:
        """
        Метод-конструктор класса Основная колода

        Поля:
            deck (deque): Основная колода карт
            last_card (Card): Последняя карта колоды
            trump (str): Козырная масть колоды

        Args:
            list_of_cards (list): Список всех карт

        Returns:
            None
        """
        deck = deque(maxlen=52)
        for card in list_of_cards:
            deck.append(card)
        rnd.shuffle(deck)
        self._deck = deck
        self._last_card = self._deck[0]
        self._trump = self._last_card.get_suit()
        for card in self._deck:
            if card.get_suit() == self._trump:
                card.set_trump(True)

    def __str__(self) -> str:
        """
        Метод, который показывает основную информацию об основной колоде карт

        Args:
            None

        Returns:
            info (str): Основная информация об основной колоде карт
        """
        deck_info = f"Количество карт в основной колоде - {len(self._deck)}\n"
        deck_info += f"Козырная масть основной колоды - {self._trump}\n"
        for card in self._deck:
            deck_info += f"{card}\n"
        deck_info += f"Последняя карта основной колоды - {self._last_card}\n"
        return deck_info

############################## ГЕТТЕРЫ и СЕТТЕРЫ ##############################

    def get_deck(self) -> deque[Card]:
        return self._deck

    def get_last_card(self) -> Card:
        return self._last_card

    def get_trump(self) -> str:
        return self._trump

############################## ГЕТТЕРЫ и СЕТТЕРЫ ##############################

    def take_a_card(self) -> Card:
        """
        Метод, который удаляет и возвращает верхнюю карту из основной колоды
        Карта удаляется и возвращается если кол-во карт в колоде > 0

        Args:
            None

        Returns:
            card (Card): Верхняя карта основной колоды (или None, если колода пуста)
        """
        if len(self._deck) > 0:
            return self._deck.pop()
        else:
            print("В основной колоде закончились карты!")
            return None
