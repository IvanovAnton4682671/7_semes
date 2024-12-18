
from __future__ import annotations   #используется для того, чтобы можно было при типизировании указывать Player внутри Player
import random as rnd
from constants import SUITS

from Card import Card

class Player:
    def __init__(self, id: int) -> None:
        """
        Метод-конструктор класса Игрок

        Поля:
            id (int): Id игрока
            hand (list): Рука игрока (имеющиеся карты)
            partner (Player): Напарник игрока
            left_opponent (Player): Противник слева
            right_opponent (Player): Противник справа

        Args:
            id (int): Id игрока

        Returns:
            None
        """
        self._id = id
        self._hand = []
        self._partner = None
        self._left_opponent = None
        self._right_opponent = None

    def __str__(self) -> str:
        """
        Метод, который показывает основную информацию об игроке

        Args:
            None

        Returns:
            info (str): Основная информация об игроке
        """
        player_info = f"Текущий игрок - {self._id}\n"
        player_info += f"Карты на руке ({len(self._hand)}):\n"
        for card in self._hand:
            player_info += f"{card}\n"
        player_info += f"Напарник - игрок {self._partner.get_id()}\n"
        player_info += f"Оппонент слева - игрок {self._left_opponent.get_id()}\n"
        player_info += f"Оппонент справа - игрок {self._right_opponent.get_id()}\n"
        return player_info

############################## ГЕТТЕРЫ и СЕТТЕРЫ ##############################

    def get_id(self) -> int:
        return self._id

    def get_hand(self) -> list[Card]:
        return self._hand

    def set_hand_card(self, card: Card) -> None:
        self._hand.append(card)

    def get_partner(self) -> Player:
        return self._partner

    def set_partner(self, partner: Player) -> None:
        self._partner = partner

    def get_left_opponent(self) -> Player:
        return self._left_opponent

    def set_left_opponent(self, left_opponent: Player) -> None:
        self._left_opponent = left_opponent

    def get_right_opponent(self) -> Player:
        return self._right_opponent

    def set_right_opponent(self, right_opponent: Player) -> None:
        self._right_opponent = right_opponent

############################## ГЕТТЕРЫ и СЕТТЕРЫ ##############################

    def take_a_card(self, card: Card) -> bool:
        """
        Метод, который добавляет карту в руку игрока
        Карта добавляется, если её нет в руке у игрока

        Args:
            card (Card): Карта, которая добавляется в руку игрока

        Returns:
            status (bool): Результат взятия карты (если получилось - True, иначе False)
        """
        if card not in self._hand:
            self._hand.append(card)
            return True
        else:
            print(f"Игрок {self._id} не может взять карту {card.get_name()}, потому что она уже есть у него в руке!")
            return False

    def delete_a_card(self, card: Card) -> bool:
        """
        Метод, который удаляет карту из руки игрока
        Карта удаляется, если она есть в руке у игрока

        Args:
            card (Card): Карта, которая удаляется из руки игрока

        Returns:
            status (bool): Результат удаления карты (если получилось - True, иначе False)
        """
        if card in self._hand:
            self._hand.remove(card)
            return True
        else:
            print(f"Игрок {self._id} не может удалить карту {card.get_name()}, потому что её нет у него в руке!")
            return False

    def random_choice_card(self, table, player_defending: Player) -> bool:
        """
        Метод, который выбирает случайную карту (подходящую под карты раунда) и совершает ход
        Случайная карта считается корректной, если: сейчас нет карт на столе (подходит любая);
        на столе есть карты, и случайная карта выбирается из тех, которые подходят под условия стола
        Разрешается походить, если у защищающегося игрока на руке есть хотя бы одна карта

        Args:
            table (Table): Игровой стол (общая зона)
            player_defending (Player): Защищающийся игрок, на которого выполняется ход

        Returns:
            status (bool): Результат хода игрока (если получилось - True, иначе False)
        """
        round_cards = table.get_round_cards()
        if len(round_cards) == 0 and len(player_defending.get_hand()) > 0:
            random_card = self._hand[rnd.randint(0, len(self._hand) - 1)]
            status_give = table.give_round_card(self, random_card)
            if status_give == True:
                status_del = self.delete_a_card(random_card)
                if status_del == True:
                    return True
        else:
            correct_cards = []
            for card in self._hand:
                if card.get_value() in [card.get_value() for card in round_cards]:
                    correct_cards.append(card)
            if len(correct_cards) > 0 and len(player_defending.get_hand()) > 0:
                random_card = correct_cards[rnd.randint(0, len(correct_cards) - 1)]
                status_give = table.give_round_card(self, random_card)
                if status_give == True:
                    status_del = self.delete_a_card(random_card)
                    if status_del == True:
                        return True
        #print(f"Игрок {self._id} не может походить ни одной картой")
        return False

    def random_choice_beat(self, table) -> bool:
        """
        Метод, который выбирает случайную карту (подходящую под последнюю карту) и бьёт её
        Карта считается подходящей, если: карта, которую нужно побить - не козырная, то подходящая - та карта, которая имеет
        такую же масть и больший номинал, или является козырной; карта, которую нужно побить - козырная, то подходящая - та
        карта, которая тоже козырная и имеет больший номинал

        Args:
            table (Table): Игровой стол (общая зона)

        Returns:
            status (bool): Результат битья карты (если получилось - True, иначе False)
        """
        round_cards = table.get_round_cards()
        correct_cards = []
        last_card = round_cards[-1]
        if last_card.get_trump() == False:
            for card in self._hand:
                if (card.get_value() > last_card.get_value() and card.get_suit() == last_card.get_suit()) or card.get_trump() == True:
                    correct_cards.append(card)
            if len(correct_cards) > 0:
                random_card = correct_cards[rnd.randint(0, len(correct_cards) - 1)]
                status_beat = table.beat_round_card(self, random_card)
                if status_beat == True:
                    status_del = self.delete_a_card(random_card)
                    if status_del == True:
                        return True
            else:
                #print(f"Игрок {self._id} не может побить карту {last_card.get_name()}")
                return False
        else:
            for card in self._hand:
                if card.get_trump() == True and card.get_value() > last_card.get_value():
                    correct_cards.append(card)
            if len(correct_cards) > 0:
                random_card = correct_cards[rnd.randint(0, len(correct_cards) - 1)]
                status_beat = table.beat_round_card(self, random_card)
                if status_beat == True:
                    status_del = self.delete_a_card(random_card)
                    if status_del == True:
                        return True
            else:
                #print(f"Игрок {self._id} не может побить карту {last_card.get_name()}")
                return False

    def economy_choice_card(self, table, player_defending: Player) -> bool:
        """
        Метод, который реализует экономный алгоритм для хода:
        1. Ищет масть, карт которой больше всего (приоритетно не козырную).
        2. Выбирает карту с минимальным номиналом из этой масти.
        3. Проверяет, можно ли походить этой картой.

        Args:
            table (Table): Игровой стол (общая зона)
            player_defending (Player): Защищающийся игрок, на которого выполняется ход

        Returns:
            status (bool): Результат хода игрока (если получилось - True, иначе False)
        """
        if not self._hand:
            #print(f"Игрок {self._id} не может походить: у него нет карт.")
            return False
        trump = table.get_trump()
        suits = SUITS
        dict_of_cards = {suit: 0 for suit in suits}
        for card in self._hand:
            suit = card.get_suit()
            dict_of_cards[suit] += 1
        non_trump_suits = {suit: count for suit, count in dict_of_cards.items() if suit != trump and count > 0}
        if non_trump_suits:
            max_count = max(non_trump_suits.values())
            selected_suit = next(suit for suit, count in non_trump_suits.items() if count == max_count)
        else:
            selected_suit = trump
        selected_cards = [card for card in self._hand if card.get_suit() == selected_suit]
        if not selected_cards:  # Если нет карт выбранной масти
            #print(f"Игрок {self._id} не может походить: нет карт масти {selected_suit}.")
            return False
        chosen_card = min(selected_cards, key=lambda card: card.get_value())
        round_cards = table.get_round_cards()
        if len(round_cards) == 0 and len(player_defending.get_hand()) > 0:
            status_give = table.give_round_card(self, chosen_card)
            if status_give:
                self.delete_a_card(chosen_card)
                return True
        else:
            if chosen_card.get_value() in [card.get_value() for card in round_cards] and len(player_defending.get_hand()) > 0:
                status_give = table.give_round_card(self, chosen_card)
                if status_give:
                    self.delete_a_card(chosen_card)
                    return True
        #print(f"Игрок {self._id} не может походить ни одной картой")
        return False

    def economy_choice_beat(self, table) -> bool:
        """
        Метод, который реализует экономный алгоритм для битья:
        1. Ставит минимально подходящую карту для защиты (по масти и весу).
        2. Использует козыри только в крайнем случае.

        Args:
            table (Table): Игровой стол (общая зона)

        Returns:
            status (bool): Результат битья карты (если получилось - True, иначе False)
        """
        round_cards = table.get_round_cards()
        if len(round_cards) > 0:
            last_card = round_cards[-1]
            trump = table.get_trump()
            correct_cards = [card for card in self._hand if card.get_suit() == last_card.get_suit() and card.get_value() > last_card.get_value()]
            if len(correct_cards) == 0:
                correct_cards = [card for card in self._hand if card.get_suit() == trump and card.get_value() > last_card.get_value()]
            if len(correct_cards) > 0:
                chosen_card = min(correct_cards, key=lambda card: card.get_value())
                status_beat = table.beat_round_card(self, chosen_card)
                if status_beat:
                    self.delete_a_card(chosen_card)
                    return True
        #print(f"Игрок {self._id} не может побить карту {last_card.get_name()}")
        return False
