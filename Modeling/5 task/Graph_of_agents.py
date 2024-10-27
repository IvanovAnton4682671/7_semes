
from Agent import *

class Graph_of_agents:

    def __init__(self, n: int, p: float) -> None:
        """
        Метод-конструктор
        Создаёт n агентов

        Поля:
            list_of_agents (list): Список всех агентов

        Args:
            n (int): Кол-во агентов
            p (float): Величина выполнения агента

        Returns:
            None
        """
        self.list_of_agents = [Agent(i + 1, p) for i in range(n)]

    def creating_neighborhood(self, agent_1: Agent, agent_2: Agent) -> None:
        """
        Метод, который устанавливает соседство между парой агентов

        Args:
            agent_1 (Agent): Первый агент
            agent_2 (Agent): Второй агент

        Returns:
            None
        """
        if agent_1 not in agent_2.neighbors and agent_2 not in agent_1.neighbors:
            agent_1.neighbors.append(agent_2)
            agent_2.neighbors.append(agent_1)
            print(f"Агенты id = {agent_1.id} и id = {agent_2.id} соседи")
        else:
            print(f"Не удалось установить соседство между агентами id = {agent_1.id} и id = {agent_2.id}")

    def check_agents_breakdown(self) -> bool:
        """
        Метод, который проверяет всех агентов на предмет общей поломки

        Args:
            None

        Returns:
            res (bool): Результат проверки
        """
        count = 0
        for agent in self.list_of_agents:
            if agent.execution == False:
                count += 1
        if count == len(self.list_of_agents):
            print(f"Все агенты сломались, дальнейшее выполнение программы невозможно!")
            return False
        else:
            return True
