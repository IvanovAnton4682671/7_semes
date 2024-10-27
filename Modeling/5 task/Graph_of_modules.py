
from Module import *

class Graph_of_modules:

    def __init__(self, m: int, a: float, b: float) -> None:
        """
        Метод-конструктор
        Создаёт m модулей

        Поля:
            list_of_modules (list): Список всех созданных модулей

        Args:
            m (int): Кол-во модулей
            a (float): Нижняя граница нагрузки модуля
            b (float): Верхняя граница нагрузки модуля

        Returns:
            None
        """
        self.list_of_modules = [Module(i + 1, a, b) for i in range(m)]

    def creating_dependencies(self, module_main: Module, module_dependent: Module) -> None:
        """
        Метод, который устанавливает зависимость между парой модулей

        Args:
            module_main (Module): Главный модуль
            module_dependent (Module): Зависимый модуль

        Returns:
            None
        """
        if module_dependent not in module_main.dependencies and module_main not in module_dependent.dependencies:
            module_dependent.dependencies.append(module_main)
            print(f"Модуль id = {module_dependent.id} зависим от модуля id = {module_main.id}")
        else:
            print(f"Не удалось установить зависимость между модулями id = {module_main.id} и id = {module_dependent.id}")
