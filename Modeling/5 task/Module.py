
import random as rnd

class Module:

    def __init__(self, id: int, a: float, b: float) -> None:
        """
        Метод-конструктор

        Поля:
            id (int): Id модуля
            load (float): Общая нагрузка модуля
            cur_load (float): Текущая нагрузка модуля
            dependencies (list): Зависимости модуля (другие модули, которые нужно выполнить, чтобы получить доступ к этому модулю)
            availability (bool): Доступность выполнения модуля (доступен/не доступен)
            cur_agent (None/Agent): Текущий агент модуля
            completed (bool): Завершённость модуля (выполнен/не выполнен)

        Args:
            id (int): Id модуля
            a (float): Нижняя граница нагрузки
            b (float): Верхняя граница нагрузки

        Returns:
            None
        """
        self.id = id
        self.load = round(rnd.uniform(a, b), 1)
        self.cur_load = self.load
        self.dependencies = []
        self.availability = False
        self.cur_agent = None
        self.completed = False

    def check_availability(self) -> bool:
        """
        Метод, который проверяет возможность выполнения модуля
        Модуль считается доступным, если он: не выполнен; не имеет текущего агента; является стартовым или выполнены все его зависимости

        Args:
            None

        Returns:
            res (bool): Результат проверки
        """
        if self.completed == False:
            if self.cur_agent == None:
                if len(self.dependencies) == 0:
                    self.availability = True
                    print(f"Модуль id = {self.id} можно взять на выполнение (стартовый)")
                    return True
                else:
                    for dep in self.dependencies:
                        if dep.completed == False:
                            print(f"Модуль id = {self.id} недоступен для выполнения пока не будут выполнены все его зависимости")
                            return False
                    else:
                        self.availability = True
                        print(f"Модуль id = {self.id} можно взять на выполнение (все зависимости выполнены)")
                        return True
            else:
                print(f"Модуль id = {self.id} занят агентом id = {self.cur_agent.id}")
                return False
        else:
            print(f"Модуль id = {self.id} уже выполнен")
            return False

    def appointment_agent(self, agent) -> None:
        """
        Метод, который назначает модулю агента для выполнения
        Модулю можно назначить агента, если он: не выполнен; не имеет текущего агента; является доступным

        Args:
            agent (Agent): Агент, который пробует назначить себе модуль

        Returns:
            None
        """
        if self.completed == False:
            if self.cur_agent == None:
                if self.availability == True:
                    self.cur_agent = agent
                    print(f"Модулю id = {self.id} был назначен агент id = {self.cur_agent.id}")
                else:
                    print(f"Модулю id = {self.id} нельзя назначить агента id = {agent.id}, т.к. модуль недоступен для выполнения")
            else:
                print(f"Модулю id = {self.id} нельзя назначить агента id = {agent.id}, т.к. модуль занят агентом id = {self.cur_agent.id}")
        else:
            print(f"Модулю id = {self.id} нельзя назначить агента id = {agent.id}, т.к. модуль выполнен")

    def check_execution(self) -> bool:
        """
        Метод, который проверяет завершённость модуля
        Модуль считается завершённым, если его текущая нагрузка <= 0

        Args:
            None

        Returns:
            res (bool): Результат проверки
        """
        if self.completed == False:
            if self.cur_agent != None:
                if self.availability == True:
                    if self.cur_load <= 0:
                        self.completed = True
                        print(f"Модуль id = {self.id} был выполнен агентом id = {self.cur_agent.id}")
                        self.cur_agent = None
                        return True
                    else:
                        print(f"Модуль id = {self.id} пока не выполнен (текущая нагрузка = {self.cur_load}) агентом id = {self.cur_agent.id}")
                        return False
                else:
                    print(f"Модуль id = {self.id} не нужно проверять, т.к. он недоступен для выполнения")
                    return False
            else:
                print(f"Модуль id = {self.id} не нужно проверять, т.к. у него нет агента")
                return False
        else:
            print(f"Модуль id = {self.id} не нужно проверять, т.к. он выполнен")
            return False

    def load_recovery(self) -> bool:
        """
        Метод, который восстанавливает агенту нагрузку в случае поломки агента, который модуль выполнял
        Нагрузка восстанавливается, если модуль: не выполнен; у него есть агента; модуль доступен

        Args:
            None

        Returns:
            res (bool): Результат восстановления нагрузки
        """
        if self.completed == False:
            if self.cur_agent != None:
                if self.availability == True:
                    self.cur_load = self.load
                    print(f"Модуль id = {self.id} восстановил нагрузку из-за поломки своего агента (id = {self.cur_agent.id})")
                    self.cur_agent = None
                    return True
                else:
                    print(f"Модулю id = {self.id} не нужно восстанавливать нагрузку, т.к. он недоступен для выполнения")
                    return False
            else:
                print(f"Модулю id = {self.id} не нужно восстанавливать нагрузку, т.к. у него нет агента (модуль не выполняется)")
                return False
        else:
            print(f"Модулю id = {self.id} не нужно восстанавливать нагрузку, т.к. он выполнен")
            return False
