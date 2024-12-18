from Agent import Agent
from agent_factory import replace_agent
import random as rnd

class RecoveredAgent(Agent):
    def __init__(self, id: int, x: float, y: float) -> None:
        """
        Конструктор класса Выздоровевший агент.

        Args:
            id (int): ID агента
            x (float): Начальная координата по X
            y (float): Начальная координата по Y
        """
        super().__init__(id, x, y)

    def move(self, list_of_agents: list) -> None:
        """
        Метод, который управляет перемещением выздоровевшего агента.

        Args:
            list_of_agents (list): Список всех агентов

        Returns:
            None
        """
        # Проверка на возможность повторного заражения
        for agent_id in self.who_does_see(list_of_agents):
            target_agent = next((a for a in list_of_agents if a.id == agent_id), None)
            if target_agent and target_agent.__class__.__name__ == "ZombieAgent" and target_agent.is_in_action_cone(self):
                if rnd.random() < 0.25:  # Шанс 25% снова стать зомби
                    #print(f"Выздоровевший агент id={self.id} снова стал зомби!")
                    replace_agent(list_of_agents, self, "zombie")  # Превращаем обратно в зомби
                    return  # Прекращаем выполнение, так как агент снова стал зомби

        # Если не заразился, движется как обычный агент
        if self.t_move == 0:
            self.initial_movement()
        self.move_iteration()
        self.t_move -= 1
