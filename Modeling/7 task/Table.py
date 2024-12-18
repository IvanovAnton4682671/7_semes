
from constants import SUITS, NAME_VALUE_PAIRS
from collections import deque
from typing import Tuple

from Card import Card
from MainDeck import MainDeck
from BitoDeck import BitoDeck
from Player import Player

class Table:
    def __init__(self) -> None:
        """
        Метод-конструктор класса Стол

        Поля:
            main_deck (MainDeck): Основная колода карт (случайно перемешанная)
            bito_deck (BitoDeck): Колода бито (изначально пустая)
            round_cards (list): Карты текущего раунда (изначально пусто)
            list_of_players (list): Список всех игроков
            deque_active_players (deque[Player]): Очередь активных игроков, которые участвуют в игре
            starting_round_player (Player): Игрок, который начинает раунд (будет ходить)
            deque_taking_cards (deque(Player)): Очередь, по которой игроки берут карты из колоды

        Args:
            None

        Returns:
            None
        """
        suits = SUITS
        name_value_pairs = NAME_VALUE_PAIRS
        list_of_cards = []
        for suit in suits:
            for name, value in name_value_pairs.items():
                card = Card(value, suit, f"{name} {suit}")
                list_of_cards.append(card)
        self._main_deck = MainDeck(list_of_cards)
        self._bito_deck = BitoDeck()
        self._round_cards = []
        self._list_of_players = [Player(i + 1) for i in range(4)]
        self._deque_active_players = deque(self._list_of_players, maxlen=4)
        self._starting_round_player = self._list_of_players[0]
        self._deque_taking_cards = deque(self._list_of_players, maxlen=4)

    def __str__(self) -> str:
        """
        Метод, который показывает основную информацию об игровом столе

        Args:
            None

        Returns:
            info (str): Основная информация об игровом столе
        """
        table_info = f"Информация о столе:\n"
        table_info += "\n"
        table_info += f"{self._main_deck}\n"
        table_info += f"{self._bito_deck}\n"
        for player in self._list_of_players:
            table_info += f"{player}\n"
        return table_info

############################## ГЕТТЕРЫ и СЕТТЕРЫ ##############################

    def get_main_deck(self) -> MainDeck:
        return self._main_deck.get_deck()

    def get_trump(self) -> str:
        return self._main_deck.get_trump()

    def get_bito_deck(self) -> BitoDeck:
        return self._bito_deck.get_deck()

    def get_round_cards(self) -> list[Card]:
        return self._round_cards

    def get_list_of_players(self) -> list[Player]:
        return self._list_of_players

    def get_deque_active_players(self) -> deque[Player]:
        return self._deque_active_players

    def get_starting_round_player(self) -> Player:
        return self._starting_round_player

    def get_deque_taking_cards(self) -> deque[Player]:
        return self._deque_taking_cards

############################## ГЕТТЕРЫ и СЕТТЕРЫ ##############################

    def set_player_dependencies(self) -> None:
        """
        Метод, который устанавливает корректных напарников и оппонентов игрокам
        Напарником становится игрок с id > self.id на 2; оппонентом слева - игрок с id > self.id на 1;
        оппонентом справа - игрок с id > self.id на 3

        Args:
            None

        Returns:
            None
        """
        for player in self._list_of_players:
            if player.get_id() == 1:
                player.set_partner(self._list_of_players[2])
                player.set_left_opponent(self._list_of_players[1])
                player.set_right_opponent(self._list_of_players[3])
            elif player.get_id() == 2:
                player.set_partner(self._list_of_players[3])
                player.set_left_opponent(self._list_of_players[2])
                player.set_right_opponent(self._list_of_players[0])
            elif player.get_id() == 3:
                player.set_partner(self._list_of_players[0])
                player.set_left_opponent(self._list_of_players[3])
                player.set_right_opponent(self._list_of_players[1])
            elif player.get_id() == 4:
                player.set_partner(self._list_of_players[1])
                player.set_left_opponent(self._list_of_players[0])
                player.set_right_opponent(self._list_of_players[2])

    def next_player(self, current_player: Player) -> Player:
        """
        Метод, который возвращает следующего активного игрока
        Если игрока нет, ищет ближайшего

        Args:
            current_player (Player): Текущий игрок

        Returns:
            player (Player): Следующий активный игрок
        """
        if current_player not in self._deque_active_players:
            raise ValueError(f"Player {current_player} is not in deque_active_players")
        idx = self._deque_active_players.index(current_player)
        return self._deque_active_players[(idx + 1) % len(self._deque_active_players)]

    def prev_player(self, current_player: Player) -> Player:
        """
        Метод, который возвращает предыдущего активного игрока
        Если игрока нет, ищет ближайшего

        Args:
            current_player (Player): Текущий игрок

        Returns:
            player (Player): Предыдущий активный игрок
        """
        if current_player not in self._deque_active_players:
            raise ValueError(f"Player {current_player} is not in deque_active_players")
        idx = self._deque_active_players.index(current_player)
        return self._deque_active_players[(idx - 1) % len(self._deque_active_players)]

    def update_active_players(self) -> None:
        """
        Метод, который обновляет список активных игроков и проверяет корректность ссылок на стартового игрока
        Если стартовый игрок отсутствует, выбирает нового

        Args:
            None

        Returns:
            None
        """
        self._deque_active_players = deque([player for player in self._deque_active_players if len(player.get_hand()) > 0 or len(self._main_deck.get_deck()) > 0], maxlen=4)
        if self._starting_round_player not in self._deque_active_players:
            self._starting_round_player = self._deque_active_players[0] if self._deque_active_players else None

    def set_starting_round_player(self) -> None:
        """
        Метод, который устанавливает нового стартового игрока на основе текущего состояния

        Args:
            None

        Returns:
            None
        """
        self.update_active_players()
        if self._starting_round_player is not None:
            self._starting_round_player = self.next_player(self._starting_round_player)

    def update_deque_taking_cards(self) -> None:
        """
        Вспомогательный метод, который формирует корректную очередь игроков на взятие карт
        Очередь формируется относительно текущего первого игрока в раунде

        Args:
            None

        Returns:
            None
        """
        self._deque_taking_cards.append(self._starting_round_player)
        for _ in range(len(self._deque_active_players) - 1):
            self._deque_taking_cards.append(self.next_player(self._deque_taking_cards[-1]))

    def distribute_cards(self) -> None:
        """
        Метод, который раздаёт карты игрокам по очереди взятия

        Args:
            None

        Returns:
            None
        """
        for player in list(self._deque_taking_cards):
            while len(player.get_hand()) < 6:
                if len(self._main_deck.get_deck()) > 0:
                    player.take_a_card(self._main_deck.take_a_card())
                else:
                    break

    def give_round_card(self, player: Player, card: Card) -> bool:
        """
        Метод, который по правилам принимает карту на стол
        Карта принимается на стол если стол пустой, или если номинал карты == любому номиналу другой карты,
        которая уже лежит на столе

        Args:
            player (Player): Игрок, который совершает ход
            card (Card): Карта, которой игрок совершает ход

        Returns:
            status (bool): Результат хода игрока (если получилось - True, иначе False)
        """
        if len(self._round_cards) == 0:
            self._round_cards.append(card)
            #print(f"Игрок {player.get_id()} походил картой {card.get_name()}")
            return True
        else:
            if card.get_value() in [card.get_value() for card in self._round_cards]:
                self._round_cards.append(card)
                #print(f"Игрок {player.get_id()} походил картой {card.get_name()}")
                return True
        #print(f"Игрок {player.get_id()} не может походить картой {card.get_name()}!")
        return False

    def beat_round_card(self, player: Player, card: Card) -> bool:
        """
        Метод, который по правилам разрешает побить карту на столе
        Карту можно побить, если: битая карта такой же масти и имеет меньший номинал; битая карта не козырь,
        а та, которой бьют - козырь; битая карта козырь, но имеет меньший номинал чем карта,
        которой бьют и которая тоже является козырем

        Args:
            player (Player): Игрок, который пробует побить карту
            card (Card): Карта, которой игрок пробует побить карту

        Returns:
            status (bool): Результат попытки побить карту (если получилось - True, иначе False)
        """
        if len(self._round_cards) == 0:
            print("Нельзя бить карту, т.к. пока нет карт!")
            return False
        else:
            if card.get_suit() == self._round_cards[-1].get_suit() and card.get_value() > self._round_cards[-1].get_value():
                self._round_cards.append(card)
                #print(f"Игрок {player.get_id()} успешно побил карту {self._round_cards[-2].get_name()} картой {card.get_name()}")
                return True
            elif card.get_suit() == self._main_deck.get_trump() and self._round_cards[-1].get_suit() != self._main_deck.get_trump():
                self._round_cards.append(card)
                #print(f"Игрок {player.get_id()} успешно побил карту {self._round_cards[-2].get_name()} козырем {card.get_name()}")
                return True
            elif card.get_suit() == self._main_deck.get_trump() and self._round_cards[-1].get_suit() == self._main_deck.get_trump() and card.get_value() > self._round_cards[-1].get_value():
                self._round_cards.append(card)
                #print(f"Игрок {player.get_id()} успешно побил карту {self._round_cards[-2].get_name()} козырем {card.get_name()}")
                return True
            else:
                #print(f"Игрок {player.get_id()} не может побить карту {self._round_cards[-2].get_name()} картой {card.get_name()}")
                return False

    def give_bito_card(self) -> bool:
        """
        Метод, который карты раунда переносит в колоду бито

        Args:
            None

        Returns:
            status (bool): Результат перемещения карт раунда в колоду бито (если получилось - True, иначе False)
        """
        while len(self._round_cards) > 0:
            card = self._round_cards.pop()
            self._bito_deck.set_deck_card(card)
        if len(self._round_cards) == 0:
            return True
        else:
            return False

    def take_round_cards(self, player: Player) -> bool:
        """
        Метод, который добавляет игроку в руку все карты раунда (а сами карты раунда очищает)

        Args:
            player (Player): Игрок, который берёт все карты раунда

        Return:
            status (bool): Результат взятия карт раунда (если получилось - True, иначе - False)
        """
        while len(self._round_cards) > 0:
            card = self._round_cards.pop()
            player.set_hand_card(card)
        if len(self._round_cards) == 0:
            return True
        else:
            return False

    def define_player_defending(self, player_attacking: Player) -> Player:
        """
        Метод, который подбирает защищающегося игрока для соперника
        Подбирается такой защищающийся игрок, чтобы у него в руке было больше 0 карт

        Args:
            player_attacking (Player): Атакующий игрок, для которого подбирается оппонент

        Returns:
            player (Player): Защищающийся игрок
        """
        player_defending = None
        if len(player_attacking.get_left_opponent().get_hand()) > 0:
            player_defending = player_attacking.get_left_opponent()
        elif len(player_attacking.get_right_opponent().get_hand()) > 0:
            player_defending = player_attacking.get_right_opponent()
        return player_defending

    def game_round(self) -> Tuple[int, Player, Player]:
        """
        Метод, который проводит игровой раунд между двумя-тремя игроками.
        Раунд заканчивается, когда атакующий и его напарник не могут больше ходить
        или защищающийся не может побить карту.

        Returns:
            Tuple[int, Player, Player]: Код окончания раунда (1 - атакующий не может больше ходить;
            2 - защищающийся взял карты) + игроки раунда.
        """
        player_attacking = self._starting_round_player
        player_defending = self.define_player_defending(player_attacking)
        player_attacking_partner = player_attacking.get_partner()
        while True:
            if player_attacking.get_id() in [2, 4]:
                status_give = player_attacking.economy_choice_card(self, player_defending)
            else:
                status_give = player_attacking.random_choice_card(self, player_defending)
            if not status_give:
                if len(player_attacking_partner.get_hand()) > 0:
                    #print(f"Подкидывает напарник - {player_attacking_partner.get_id()}")
                    if player_attacking_partner.get_id() in [2, 4]:
                        status_give_partner = player_attacking_partner.economy_choice_card(self, player_defending)
                    else:
                        status_give_partner = player_attacking_partner.random_choice_card(self, player_defending)
                    if not status_give_partner:
                        if self.get_round_cards():
                            #print(f"Раунд завершён: все карты уходят в бито.")
                            self.give_bito_card()
                        return 1, player_attacking, player_defending
                else:
                    if self.get_round_cards():
                        #print(f"Раунд завершён: все карты уходят в бито.")
                        self.give_bito_card()
                    return 1, player_attacking, player_defending
            if player_defending.get_id() in [2, 4]:
                status_beat = player_defending.economy_choice_beat(self)
            else:
                status_beat = player_defending.random_choice_beat(self)
            if not status_beat:
                #print(f"Игрок {player_defending.get_id()} не может побить карту.")
                self.take_round_cards(player_defending)
                return 2, player_attacking, player_defending
            if not player_attacking.get_hand() and not player_attacking_partner.get_hand():
                #print(f"Раунд завершён: все карты уходят в бито.")
                self.give_bito_card()
                return 1, player_attacking, player_defending

    def check_end_game(self) -> int:
        """
        Метод, который определяет конец игры
        Конец игры - ситуация, когда оба игрока из пары вышли, т.е. у них на руках по 0 карт (в обшей колоде тоже 0 карт)

        Args:
            None

        Returns:
            code (int): Результат проверки конца игры (1 - победа пары 1; 2 - победа пары 2; 3 - игра продолжается; 4 - ошибка)
        """
        pair_1 = [self._list_of_players[0], self._list_of_players[0].get_partner()]
        pair_2 = [self._list_of_players[0].get_left_opponent(), self._list_of_players[0].get_left_opponent().get_partner()]
        if len(pair_1[0].get_hand()) == 0 and len(pair_1[1].get_hand()) == 0:
            print("Победа пары 1!")
            return 1
        elif len(pair_2[0].get_hand()) == 0 and len(pair_2[1].get_hand()) == 0:
            print("Победа пары 2!")
            return 2
        elif sum([len(pair_1[i].get_hand()) for i in range(len(pair_1))]) > 0 and sum([len(pair_2[i].get_hand()) for i in range(len(pair_2))]) > 0:
            #print("Игра ещё не закончилась.")
            return 3
        else:
            print(f"Кол-во карт в руках у игроков: {[len(self._list_of_players[i].get_hand()) for i in range(len(self._list_of_players))]}")
            return 4

    def game_cycle(self) -> int:
        """
        Метод, который реализует основной игровой цикл, обрабатывает все раунды и передачу хода

        Args:
            None

        Returns:
            code (int): Результат окончания игры (1 - победила пара 1; 2 - победила пара 2)
        """
        self.set_player_dependencies()
        self.distribute_cards()
        count_round = 0
        while True:
            count_round += 1
            #print(f"Раунд {count_round}. Нападающий - {self._starting_round_player.get_id()}, защищающийся - {self.define_player_defending(self._starting_round_player).get_id()}. Карты в руках - {[len(player.get_hand()) for player in self._list_of_players]}. Карт в основной колоде - {len(self._main_deck.get_deck())}. Карт в колоде бито - {len(self._bito_deck.get_deck())}. Активная очередь - {[player.get_id() for player in self._deque_active_players]}")
            round_result, round_player_attacking, round_player_defending = self.game_round()
            self.distribute_cards()
            self.update_active_players()
            if round_result == 1:
                self.set_starting_round_player()
            elif round_result == 2:
                self._starting_round_player = self.next_player(round_player_defending)
            else:
                raise ValueError("Unexpected round result.")
            checking_end_result = self.check_end_game()
            if checking_end_result in [1, 2]:
                return checking_end_result
