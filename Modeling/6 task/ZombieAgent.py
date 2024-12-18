
import math as mt
import random as rnd
from agent_factory import replace_agent

from Agent import Agent

class ZombieAgent(Agent):
    def __init__(self, id: int, x: float, y: float, vision_radius: int, vision_angle: int) -> None:
        """
        Метод-конструктор класса Зомби, наследуется от класса Агент

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
            action_radius (int): Радиус действия зомби
            action_angle (int): Угол действия зомби
            action_overview (list): Координаты точек конуса сектора действия зомби относительно направления движения
            target_agent (Agent): Цель преследования зомби

        Args:
            id (int): Id агента
            x (float): Координата агента по X
            y (float): Координата агента по Y
            vision_radius (int): Радиус обзора агента
            vision_angle (int): Угол обзора агента

        Returns:
            None
        """
        super().__init__(id, x, y)
        self.vision_radius = vision_radius * 1.1
        self.vision_angle = vision_angle * 0.75
        self.action_radius = self.vision_radius * 0.93
        self.action_angle = self.vision_angle * 0.93
        self.action_overview = []
        self.target_agent = None

    def overview_calculation(self) -> None:
        """
        Метод, который вычисляет сектор действия зомби
        """
        super().overview_calculation()

        #вычисляем сектор действия на основе action_radius и action_angle
        action_cone_points = [(self.x, self.y)]   #начальная точка сектора действия - позиция зомби
        half_action_angle = self.action_angle / 2
        angle_center = mt.radians(self.direction)
        
        for angle_offset in [-half_action_angle, half_action_angle]:
            angle = angle_center + mt.radians(angle_offset)
            action_x = self.x + self.action_radius * mt.sin(angle)
            action_y = self.y + self.action_radius * mt.cos(angle)
            action_cone_points.append((action_x, action_y))
        
        self.action_overview = action_cone_points   #координаты для сектора действия

    def is_in_action_cone(self, other_agent) -> bool:
        """
        Проверяет, находится ли другой агент в секторе действия зомби

        Args:
            other_agent (Agent): проверяемый агент

        Returns:
            bool: True, если агент находится в секторе действия, иначе False
        """
        self.overview_calculation()
        a, b, c = self.action_overview  #координаты вершин треугольника сектора действия

        #вычисление площади треугольников для проверки нахождения внутри сектора действия
        def triangle_area(p1, p2, p3):
            return abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) / 2.0)

        area_ABC = triangle_area(a, b, c)
        area_ABP = triangle_area(a, b, (other_agent.x, other_agent.y))
        area_BCP = triangle_area(b, c, (other_agent.x, other_agent.y))
        area_CAP = triangle_area(c, a, (other_agent.x, other_agent.y))

        return abs(area_ABC - (area_ABP + area_BCP + area_CAP)) < 1e-5

    def move_iteration(self) -> None:
        """
        Метод, который выполняет итерацию перемещения агента исходя из параметров перемещения

        Args:
            None

        Returns:
            None
        """
        if self.target_agent:
            #если есть цель, продолжаем движение к ней
            angle_to_target = mt.degrees(mt.atan2(self.target_agent.y - self.y, self.target_agent.x - self.x))
            self.direction = angle_to_target
            self.speed_calculation()   #обновляем скорости в новом направлении
            self.x += self.speed_x * 0.85
            self.y += self.speed_y * 0.85
        else:
            #скорость заражённого агента = 85% скорости обычного агента (здорового)
            self.x += self.speed_x * 0.85
            self.y += self.speed_y * 0.85

            #если агент пытается пересечь границу по X - направление меняется как 360-текущее и пересчитывается скорость по X
            #если агент путается пересечь границу по Y - направление меняется как 180-текущее и пересчитывается скорость по Y
            #решено делать так, а не менять знак соответствующей скорости для того, чтобы корректно изменялось направление
            # движение агента
            if self.x < 0 or self.x > 100:
                self.direction = 360 - self.direction
                self.speed_calculation()
                self.x += self.speed_x * 2 * 0.85
            if self.y < 0 or self.y > 100:
                self.direction = 180 - self.direction
                self.speed_calculation()
                self.y += self.speed_y * 2 * 0.85

            self.overview_calculation()

    def move(self, list_of_agents: list) -> None:
        """
        Метод, который управляет перемещением зомби

        Args:
            list_of_agents (list): Список всех агентов

        Returns:
            None
        """
        if rnd.random() < 0.01:
            #print(f"Зомби id={self.id} выздоровел!")
            replace_agent(list_of_agents, self, "recovered")  #выздоровление зомби
            return  #прекращаем выполнение, так как агент стал выздоровевшим

        visible_agents = self.who_does_see(list_of_agents)

        #проверка видимых агентов и выбор цели
        if self.target_agent == None:
            for agent_id in visible_agents:
                target_agent = next((a for a in list_of_agents if a.id == agent_id), None)
                if type(target_agent) == type(Agent(0, 0, 0)):
                    self.target_agent = target_agent
                    break

        #проверка сектора действия и превращение цели в зомби
        if self.target_agent and self.is_in_action_cone(self.target_agent):
            #print(f"Агент id = {self.target_agent.id} превращается в зомби!")
            for i, agent in enumerate(list_of_agents):
                if agent.id == self.target_agent.id:
                    list_of_agents[i] = ZombieAgent(self.target_agent.id, self.target_agent.x, self.target_agent.y, self.target_agent.vision_radius, self.target_agent.vision_angle)
                    break
            self.target_agent = None

        #движение зомби
        if self.t_move == 0:
            self.initial_movement()
        self.move_iteration()
        self.t_move -= 1
