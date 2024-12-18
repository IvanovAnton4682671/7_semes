
import random as rnd
import math as mt

class Agent:
    def __init__(self, id: int, x: float, y: float) -> None:
        """
        Метод-конструктор класса Агент

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

        Args:
            id (int): Id агента
            x (float): Координата агента по X
            y (float): Координата агента по Y

        Returns:
            None
        """
        self.id = id
        self.x = x
        self.y = y
        self.vision_radius = rnd.randint(10, 15)
        self.vision_angle = rnd.randint(90, 150)
        self.speed = 0
        self.speed_x = 0
        self.speed_y = 0
        self.direction = 0
        self.overview = []
        self.t_move = 0

    def info(self) -> None:
        """
        Метод, который выводит основную информацию об агенте

        Args:
            None

        Returns:
            None
        """
        print(f"id = {self.id} x = {self.x} y = {self.y} vision_radius = {self.vision_radius} vision_angle = {self.vision_angle} speed = {self.speed} speed_x = {self.speed_x} speed_y = {self.speed_y} direction = {self.direction} overview = {self.overview} t_move = {self.t_move}")

    def speed_calculation(self) -> None:
        """
        Метод, который рассчитывает координатные скорости в зависимости от направления движения агента

        Args:
            None

        Returns:
            None
        """
        angle_radian = mt.radians(self.direction)
        #по оси X выбран sin, потому что 0 градусов - вертикаль Y+, а не горизонталь X+
        self.speed_x = self.speed * mt.sin(angle_radian)
        self.speed_y = self.speed * mt.cos(angle_radian)

    def overview_calculation(self) -> None:
        """
        Метод, который вычисляет точки конуса видимости агента в зависимости от его положения и направления движения

        Args:
            None

        Returns:
            None
        """
        cone_points = [(self.x, self.y)]            #начальная точка сектора - позиция агента
        half_angle = self.vision_angle / 2          #половина угла обзора
        angle_center = mt.radians(self.direction)   #угол направления агента в радианах

        #вычисление крайних точек сектора видимости
        for angle_offset in [-half_angle, half_angle]:
            angle = angle_center + mt.radians(angle_offset)
            cone_x = self.x + self.vision_radius * mt.sin(angle)
            cone_y = self.y + self.vision_radius * mt.cos(angle)
            cone_points.append((cone_x, cone_y))

        self.overview = cone_points

    def is_in_vision_cone(self, other_agent) -> bool:
        """
        Метод, который проверяет, попадает ли другой агент в область видимости текущего агента

        Args:
            other_agent (Agent): проверяемый агент

        Returns:
            bool: True, если агент находится в секторе видимости, иначе False
        """
        self.overview_calculation()
        a, b, c = self.overview   #координаты вершин треугольника конуса видимости

        #функция для вычисления площади треугольника по координатам
        def triangle_area(p1, p2, p3):
            return abs((p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])) / 2.0)

        area_ABC = triangle_area(a, b, c)   #полная площадь треугольника ABC

        # Площадь треугольников, образованных точкой other и вершинами треугольника ABC
        area_ABP = triangle_area(a, b, (other_agent.x, other_agent.y))
        area_BCP = triangle_area(b, c, (other_agent.x, other_agent.y))
        area_CAP = triangle_area(c, a, (other_agent.x, other_agent.y))

        #проверка: other_agent находится внутри треугольника, если сумма площадей совпадает с полной площадью
        return abs(area_ABC - (area_ABP + area_BCP + area_CAP)) < 1e-5   #допустимая погрешность

    def initial_movement(self) -> None:
        """
        Метод, который инициализирует случайные параметры для начала перемещения агента

        Args:
            None

        Returns:
            None
        """
        self.speed = rnd.randint(3, 7)
        self.direction = rnd.randint(0, 360)
        self.t_move = rnd.randint(25, 50)
        self.speed_calculation()
        self.overview_calculation()

    def move_iteration(self) -> None:
        """
        Метод, который выполняет итерацию перемещения агента исходя из параметров перемещения

        Args:
            None

        Returns:
            None
        """
        self.x += self.speed_x
        self.y += self.speed_y

        #если агент пытается пересечь границу по X - направление меняется как 360-текущее и пересчитывается скорость по X
        #если агент путается пересечь границу по Y - направление меняется как 180-текущее и пересчитывается скорость по Y
        #решено делать так, а не менять знак соответствующей скорости для того, чтобы корректно изменялось направление
        # движение агента
        if self.x < 0 or self.x > 100:
            self.direction = 360 - self.direction
            self.speed_calculation()
            self.x += self.speed_x * 2
        if self.y < 0 or self.y > 100:
            self.direction = 180 - self.direction
            self.speed_calculation()
            self.y += self.speed_y * 2

        self.overview_calculation()

    def who_does_see(self, list_of_agents: list) -> list:
        """
        Метод, который перебирает список всех агентов и ищет тех, кого видит агент

        Args:
            list_of_agents (list): Список всех агентов

        Returns:
            visible_agents (list): Список id видимых агентов
        """
        visible_agents = []
        for i in range(len(list_of_agents)):
            if list_of_agents[i].id != self.id:
                if self.is_in_vision_cone(list_of_agents[i]):
                    visible_agents.append(list_of_agents[i].id)
            else:
                continue
        return visible_agents

    def calculate_escape_direction(self, zombies_left, zombies_right):
        """
        Метод для вычисления нового направления, чтобы избежать зомби

        Args:
            zombies_left (bool): Есть ли зомби в левом секторе
            zombies_right (bool): Есть ли зомби в правом секторе

        Returns:
            int: Новое направление агента
        """
        if zombies_left and zombies_right:
            #зомби с обеих сторон - поворот на 180 градусов
            return (self.direction + 180) % 360
        elif zombies_right:
            #зомби справа - поворот влево
            return (self.direction - 90) % 360
        elif zombies_left:
            #зомби слева - поворот вправо
            return (self.direction + 90) % 360
        return self.direction   #если нет зомби, направление не меняется

    def move(self, list_of_agents: list) -> None:
        """
        Метод, который управляет перемещением агента.
        Если в поле зрения есть зомби, агент меняет направление.

        Args:
            list_of_agents (list): Список всех агентов

        Returns:
            None
        """
        #проверка на видимых агентов
        visible_agents = self.who_does_see(list_of_agents)
        zombies_left = zombies_right = False

        for agent_id in visible_agents:
            target_agent = next((a for a in list_of_agents if a.id == agent_id), None)
            if target_agent.__class__.__name__ == "ZombieAgent":  #проверка на зомби без импорта класса Зомби
                #определяем угол до зомби
                angle_to_zombie = mt.degrees(mt.atan2(target_agent.y - self.y, target_agent.x - self.x))
                angle_to_zombie = (angle_to_zombie + 360) % 360   #приводим к диапазону [0, 360]

                #определяем левый и правый пределы сектора обзора
                left_bound = (self.direction - self.vision_angle / 2 + 360) % 360
                right_bound = (self.direction + self.vision_angle / 2) % 360

                #проверка положения зомби относительно центральной линии обзора
                if left_bound < right_bound:
                    if left_bound <= angle_to_zombie < self.direction:
                        zombies_left = True
                    elif self.direction <= angle_to_zombie < right_bound:
                        zombies_right = True
                else:
                    #если сектор пересекает границу 360 градусов
                    if left_bound <= angle_to_zombie < 360 or 0 <= angle_to_zombie < self.direction:
                        zombies_left = True
                    elif self.direction <= angle_to_zombie < 360 or 0 <= angle_to_zombie < right_bound:
                        zombies_right = True

        #если есть зомби в поле зрения, меняем направление
        if zombies_left or zombies_right:
            new_direction = self.calculate_escape_direction(zombies_left, zombies_right)
            #print(f"Agent id={self.id} меняет направление на {new_direction} чтобы убежать от зомби")
            self.direction = new_direction
            self.speed_calculation()   #пересчёт скоростей в новом направлении

        #движение агента
        if self.t_move == 0:
            self.initial_movement()
        self.move_iteration()
        self.t_move -= 1
