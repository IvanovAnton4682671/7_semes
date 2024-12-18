
from constants import NUMBER_OF_COLONIES, SIMULATION_TIME, AUCTION_INTERVAL, START_PRICE, EVENT_INTERVAL, DUST_STORM, RENAISSANCE, ARTIFACT_N
from Colony import *
from Artifact import *
from Agent import *
import random as rnd

number_of_colonies = NUMBER_OF_COLONIES
simulation_time = SIMULATION_TIME
auction_interval = AUCTION_INTERVAL
start_price = START_PRICE
event_interval = EVENT_INTERVAL
dust_storm = DUST_STORM
renaissance = RENAISSANCE
artifact_n = ARTIFACT_N

class Mars:
    def __init__(self) -> None:
        """
        Конструктор класса Марс

        Поля:
            list_active_colonies (list[Colony]): Список активных колоний
            list_win_colonies (list[Colony]): Список колоний-победителей
            list_loss_colonies (list[Colony]): Список проигравших колоний

        Args:
            None

        Returns:
            None
        """
        self._simulation_time = simulation_time
        self._list_active_colonies = [Colony(i + 1) for i in range(number_of_colonies)]
        self._list_win_colonies = []
        self._list_loss_colonies = []
        self._list_artifacts = [Artifact(30, artifact_n), Artifact(42, artifact_n), Artifact(48, artifact_n), Artifact(49, artifact_n), Artifact(64, artifact_n)]
        self._list_all_agents = [Agent(colony.get_id(), colony) for colony in self._list_active_colonies]

    def __str__(self) -> str:
        """
        Метод, который возвращает основную информацию о состоянии Марса

        Args:
            None

        Returns:
            info (str): Основная информация о состоянии Марса
        """
        info = "Колонии Марса"
        info += "\nУправляющие агенты:"
        for agent in self._list_all_agents:
            info += f"\n{agent}"
        info += "\nАктивные колонии:"
        for colony in self._list_active_colonies:
            info += f"\n{colony}"
        info += "\nКолонии-победители:"
        for colony in self._list_win_colonies:
            info += f"\n{colony}"
        info += "\nПроигравшие колонии:"
        for colony in self._list_loss_colonies:
            info += f"\n{colony}"
        return info

    def create_random_event(self, colony: Colony) -> None:
        """
        Метод, который запускает случайное событие для колонии

        Args:
            colony (Colony): Колония, для которой срабатывает событие

        Returns:
            None
        """
        event = rnd.randint(0, 1)
        if event == 0:
            print(f"Колония {colony.get_id()} столкнулась с Песчаной бурей!")
            print(f"Прошлые доход и расход: {colony.get_income()} и {colony.get_expense()}")
            colony.set_income(colony.get_income() + dust_storm[0])
            colony.set_expense(colony.get_expense() + dust_storm[1])
            print(f"Новые доход и расход: {colony.get_income()} и {colony.get_expense()}")
        else:
            print(f"В колонии {colony.get_id()} произошёл Ренессанс!")
            print(f"Прошлые доход и расход: {colony.get_income()} и {colony.get_expense()}")
            colony.set_income(colony.get_income() + renaissance[0])
            colony.set_expense(colony.get_expense() + renaissance[1])
            print(f"Новые доход и расход: {colony.get_income()} и {colony.get_expense()}")

    def try_use_colony_artifact(self, colony: Colony) -> None:
        """
        Метод, который пробует применить артефакт колонии

        Args:
            colony (Colony): Колония, которая применяет артефакт

        Returns:
            None
        """
        if colony.get_cur_artifact():
            if colony.get_cur_artifact().get_duration() > 0:
                colony_artifact = colony.get_cur_artifact()
                if colony_artifact.get_id() == 42:
                    #в качестве враждебной колонии выбирается колония с самым высоким показателем опыта
                    enemy_colony = max((c for c in self._list_active_colonies if c != colony), key=lambda c: c.get_exp(), default=None)
                    if enemy_colony:
                        colony_artifact.apply_to_colony(colony, enemy_colony=enemy_colony)
                else:
                    colony_artifact.apply_to_colony(colony)
            if colony.get_cur_artifact().get_duration() == 0:
                colony.set_cur_artifact(None)
        else:
            print(f"У колонии {colony.get_id()} нет артефакта!")

    def set_colony_artifact(self, colony: Colony, artifact: Artifact) -> None:
        """
        Метод, который устанавливает колонии артефакт

        Args:
            colony (Colony): Колония, которой устанавливается артефакт
            artifact (Artifact): Артефакт, который устанавливается колонии

        Returns:
            None
        """
        if colony.get_cur_artifact() is None:
            colony.set_cur_artifact(artifact)
            self.try_use_colony_artifact(colony)
        else:
            print(f"У колонии {colony.get_id()} уже есть артефакт {colony.get_cur_artifact().get_id()}!")

    def auction(self) -> None:
        """
        Метод, который проводит аукцион для продажи 5 артефактов

        Args:
            None

        Returns:
            None
        """
        print("Начался аукцион!")
        active_agents = [agent for agent in self._list_all_agents if agent.get_colony().get_cur_artifact() is None]
        if len(active_agents) == 0:
            return
        count_failed = 0
        for lot in self._list_artifacts:
            cur_price = start_price
            purchased = False
            new_price = cur_price
            last_agent = None
            while not purchased:
                for agent in active_agents[:]:
                    can_bet, new_bet = agent.place_a_bet(new_price, agent.get_colony().get_balance())
                    if can_bet:
                        new_price = new_bet
                        last_agent = agent
                    else:
                        if last_agent:
                            last_agent_colony = last_agent.get_colony()
                            print(f"Колония {last_agent_colony.get_id()} покупает артефакт {lot.get_id()} за {new_price}!")
                            last_agent_colony.set_balance(last_agent_colony.get_balance() - new_price)
                            self.set_colony_artifact(last_agent_colony, lot)
                            purchased = True
                            break
                if len(active_agents) == 1:
                    last_agent = active_agents[0]
                    last_agent_colony = last_agent.get_colony()
                    print(f"Колония {last_agent_colony.get_id()} покупает артефакт {lot.get_id()} за {new_price}!")
                    last_agent_colony.set_balance(last_agent_colony.get_balance() - new_price)
                    self.set_colony_artifact(last_agent_colony, lot)
                    purchased = True
                if not purchased:
                    print(f"Текущая цена артефакта {lot.get_id()}: {new_price}")
                    count_failed += 1
                if count_failed > 5:
                    break
            active_agents = [agent for agent in active_agents if agent.get_colony().get_cur_artifact() is None]
        print("Аукцион завершён!")

    def main_cycle(self) -> int:
        """
        Метод, который выполняет основной цикл симуляции

        Args:
            None

        Returns:
            count_iterations (int): Кол-во пройденных итераций моделирования до его окончания
        """
        for i in range(self._simulation_time):
            if len(self._list_active_colonies) == 0:
                break
            else:
                print(f"{i + 1} итерация симуляции")
                if (i + 1) % auction_interval == 0:
                    self.auction()
                if (i + 1) % event_interval == 0:
                    for colony in self._list_active_colonies:
                        self.create_random_event(colony)
                for colony in self._list_active_colonies:
                    self.try_use_colony_artifact(colony)
                for colony in self._list_active_colonies:
                    colony.calculate_new_balance()
                for colony in self._list_active_colonies:
                    if colony.get_status() == "win":
                        self._list_active_colonies.remove(colony)
                        self._list_win_colonies.append(colony)
                    elif colony.get_status() == "loss":
                        self._list_active_colonies.remove(colony)
                        self._list_loss_colonies.append(colony)
        print(self)
        return i, len(self._list_win_colonies), len(self._list_win_colonies)
