
from Agent import *
from ZombieAgent import *

class InfectedAgent(Agent):
    def __init__(self, id: int, x: float, y: float, incubation_period: int) -> None:
        """
        Метод-конструктор класса Заражённый агент, наследуется от класса Агент

        Поля:
            id (int): Id агента
            x (float): Координата агента по X
            y (float): Координата агента по Y
            vision_radius (int): Радиус обзора агента
            vision_angle (int): Угол обзора агента
            speed (int): Общая скорость агента
            speed_x (float): Скорость агента по X
            speed_y (float): Скорость агента по Y
            direction (int): Направление движения агента (в градусах (0 - вертикаль по Y+))
            overview (list): Координаты точек конуса видимости агента относительно направления движения
            t_move (int): Время, в течении которого агент перемещается
            incubation_period (int): Инкубационные период заражённого агента

        Args:
            id (int): Id заражённого агента
            x (float): Координата заражённого агента по X
            y (float): Координата заражённого агента по Y
            incubation_period (int): Инкубационный период заражённого агента

        Returns:
            None
        """
        super().__init__(id, x, y)
        self.incubation_period = incubation_period

    def move_iteration(self) -> None:
        """
        Метод, который выполняет итерацию перемещения агента исходя из параметров перемещения

        Args:
            None

        Returns:
            None
        """
        #скорость заражённого агента = 90% скорости обычного агента (здорового)
        self.x += self.speed_x * 0.9
        self.y += self.speed_y * 0.9

        #если агент пытается пересечь границу по X - направление меняется как 360-текущее и пересчитывается скорость по X
        #если агент путается пересечь границу по Y - направление меняется как 180-текущее и пересчитывается скорость по Y
        #решено делать так, а не менять знак соответствующей скорости для того, чтобы корректно изменялось направление
        # движение агента
        if self.x < 0 or self.x > 100:
            self.direction = 360 - self.direction
            self.speed_calculation()
            self.x += self.speed_x * 2 * 0.9
        if self.y < 0 or self.y > 100:
            self.direction = 180 - self.direction
            self.speed_calculation()
            self.y += self.speed_y * 2 * 0.9

        self.overview_calculation()
        if self.incubation_period > 0:
            self.incubation_period -= 1

    def move(self, list_of_agents: list) -> None:
        """
        Метод, который управляет перемещением агента

        Args:
            list_of_agents (list): Список всех агентов

        Returns:
            None
        """
        if self.t_move == 0:
            self.initial_movement()
        self.move_iteration()
        if self.incubation_period <= 0:
            list_of_agents[list_of_agents.index(self)] = ZombieAgent(
                self.id, self.x, self.y, self.vision_radius, self.vision_angle)
        visible_agents = self.who_does_see(list_of_agents)
        if len(visible_agents) == 0:
            #print(f"Агент id = {self.id} никого не видит")
            pass
        else:
            #print(f"Агент id = {self.id} видит агентов {visible_agents}")
            pass

        self.t_move -= 1
