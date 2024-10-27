
import random as rnd

class Agent:

    def __init__(self, id: int, p: float) -> None:
        """
        Метод-конструктор

        Поля:
            id (int): Id агента
            neighbors (list): Список соседей агента, которым он может передать модуль
            cur_module (None/Module): Текущий модуль агента
            execution (bool): Возможность агента выполнять вычисления модуля
            amount_of_execution (float): Величина, на которую агент уменьшает текущую нагрузку модуля каждую итерацию выполнения

        Args:
            id (int): Id агента
            p (float): Величина выполнения агента

        Returns:
            None
        """
        self.id = id
        self.neighbors = []
        self.cur_module = None
        self.execution = True
        self.amount_of_execution = p

    def attempt_get_module(self, module) -> None:
        """
        Метод, который пробует взять модуль на выполнение
        Агент может взять модуль на выполнение, если он: не сломан; не имеет модуль; модуль доступен

        Args:
            module (Module): Модуль, который агент пробует взять на выполнение

        Returns:
            None
        """
        if self.execution == True:
            if self.cur_module == None:
                check = module.check_availability()
                if check == True:
                    self.cur_module = module
                    print(f"Агент id = {self.id} взял модуль id = {self.cur_module.id} на выполнение")
                    module.appointment_agent(self)
                else:
                    print(f"Агент id = {self.id} не может взять модуль id = {module.id} на выполнение")
            else:
                print(f"Агент id = {self.id} не может взять модуль id = {module.id}, т.к. у агента уже есть модуль id = {self.cur_module.id}")
        else:
            print(f"Агент id = {self.id} не может взять модуль id = {module.id}, т.к. агент сломался")

    def execution_step(self) -> None:
        """
        Метод, который выполняет шаг выполнения модуля агентом
        Шаг выполняется, если агент: не сломан; имеет модуль

        Args:
            None

        Returns:
            None
        """
        if self.execution == True:
            if self.cur_module != None:
                check = self.cur_module.check_execution()
                if check == False:
                    self.cur_module.cur_load -= self.amount_of_execution
                    print(f"Агент id = {self.id} уменьшил нагрузку своего модуля (id = {self.cur_module.id}) на {self.amount_of_execution}")
                    check = self.cur_module.check_execution()
                    if check == True:
                        print(f"Агент id = {self.id} выполнил модуль id = {self.cur_module.id}")
                        self.cur_module = None
                else:
                    print(f"Агент id = {self.id} выполнил модуль id = {self.cur_module.id}")
                    self.cur_module = None
            else:
                print(f"Агент id = {self.id} не может выполнять модуль, т.к. агент не имеет модуля")
        else:
            print(f"Агент id = {self.id} не может выполнять модуль, т.к. агент сломался")

    def check_breakdown(self) -> None:
        """
        Метод, который на итерационном шаге проверяет, не сломался ли агент
        Если агент сломался, то его модуль восстанавливает нагрузку, а агент пытается передать этот модуль соседу

        Args:
            None

        Returns:
            None
        """
        b = rnd.randint(1, 100)
        if b <= 5:
            if self.execution == True:
                if self.cur_module != None:
                    check = self.cur_module.load_recovery()
                    if check == True:
                        self.execution = False
                        module = self.cur_module
                        self.cur_module = None
                        if len(self.neighbors) >= 1:
                            for neig in self.neighbors:
                                if neig.execution == True and neig.cur_module == None:
                                    neig.cur_module = module
                                    print(f"Агент id = {self.id} сломался и передал свой модуль id = {module.id} агенту-соседу id = {neig.id}")
                                    module.appointment_agent(neig)
                                    return
                                else:
                                    print(f"Агент id = {self.id} сломался, и не может передать свой модуль id = {module.id} агенту-соседу id = {neig.id}")
                        else:
                            print(f"Агент id = {self.id} не имеет соседей... ОШИБКА")
                            raise ValueError
                    else:
                        print(f"Агент id = {self.id} сломался, а его модуль id = {module.id} не восстановил нагрузку (0_0)")
                else:
                    print(f"Агент id = {self.id} не может сломаться без модуля... ОШИБКА")
                    raise ValueError
            else:
                print(f"Агент id = {self.id} не может сломаться второй раз... ОШИБКА")
                raise ValueError
        else:
            self.execution_step()
