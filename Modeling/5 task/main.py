
from Module import *
from Agent import *
from Graph_of_modules import *
from Graph_of_agents import *
import typing as tp
import time

def create_graph_of_agents(n: int, p: float) -> tp.Tuple[Graph_of_agents, list]:
    """
    Функция, которая создаёт граф агентов

    Args:
        n (int): Кол-во агентов
        p (float): Величина выполнения агентов

    Returns:
        graph_of_agents (Graph_of_agents): Граф агентов
        list_of_agents (list): Список всех агентов
    """
    graph_of_agents = Graph_of_agents(n, p)
    list_of_agents = graph_of_agents.list_of_agents
    return graph_of_agents, list_of_agents

def create_graph_of_modules(m: int, a: float, b: float) -> tp.Tuple[Graph_of_modules, list]:
    """
    Функция, которая создаёт граф модулей

    Args:
        m (int): Кол-во модулей
        a (float): Нижняя граница нагрузки модуля
        b (float): Верхняя граница нагрузки модуля

    Returns:
        graph_of_modules (Graph_of_modules): Граф модулей
        list_of_modules (list): Список всех модулей
    """
    graph_of_modules = Graph_of_modules(m, a, b)
    list_of_modules = graph_of_modules.list_of_modules
    return graph_of_modules, list_of_modules

def create_modules_dependencies_v1(graph_of_modules: Graph_of_modules, list_of_modules: list) -> None:
    """
    Функция, которая задаёт связи для ориентированного графа модулей

    Args:
        graph_of_modules (Graph_of_modules): Граф модулей
        list_of_modules (list): Список всех модулей

    Returns:
        None
    """
    graph_of_modules.creating_dependencies(list_of_modules[0], list_of_modules[1])
    graph_of_modules.creating_dependencies(list_of_modules[0], list_of_modules[2])
    graph_of_modules.creating_dependencies(list_of_modules[1], list_of_modules[2])
    graph_of_modules.creating_dependencies(list_of_modules[1], list_of_modules[3])
    graph_of_modules.creating_dependencies(list_of_modules[2], list_of_modules[3])
    graph_of_modules.creating_dependencies(list_of_modules[3], list_of_modules[4])

def create_modules_dependencies_v2(graph_of_modules: Graph_of_modules, list_of_modules: list) -> None:
    """
    Функция, которая задаёт связи для ориентированного графа модулей

    Args:
        graph_of_modules (Graph_of_modules): Граф модулей
        list_of_modules (list): Список всех модулей

    Returns:
        None
    """
    graph_of_modules.creating_dependencies(list_of_modules[0], list_of_modules[1])
    graph_of_modules.creating_dependencies(list_of_modules[0], list_of_modules[2])
    graph_of_modules.creating_dependencies(list_of_modules[1], list_of_modules[3])
    graph_of_modules.creating_dependencies(list_of_modules[2], list_of_modules[4])

def create_modules_dependencies_v3(graph_of_modules: Graph_of_modules, list_of_modules: list) -> None:
    """
    Функция, которая задаёт связи для ориентированного графа модулей

    Args:
        graph_of_modules (Graph_of_modules): Граф модулей
        list_of_modules (list): Список всех модулей

    Returns:
        None
    """
    graph_of_modules.creating_dependencies(list_of_modules[0], list_of_modules[3])
    graph_of_modules.creating_dependencies(list_of_modules[1], list_of_modules[3])
    graph_of_modules.creating_dependencies(list_of_modules[2], list_of_modules[3])
    graph_of_modules.creating_dependencies(list_of_modules[3], list_of_modules[4])
    graph_of_modules.creating_dependencies(list_of_modules[3], list_of_modules[5])
    graph_of_modules.creating_dependencies(list_of_modules[3], list_of_modules[6])

def create_agents_neighborhood_v1(graph_of_agents: Graph_of_agents, list_of_agents: list) -> None:
    """
    Функция, которая задаёт связи для неориентированного графа агентов

    Args:
        graph_of_agents (Graph_of_agents): Граф агентов
        list_of_agents (list): Список всех агентов

    Returns:
        None
    """
    graph_of_agents.creating_neighborhood(list_of_agents[0], list_of_agents[1])
    graph_of_agents.creating_neighborhood(list_of_agents[1], list_of_agents[2])

def create_agents_neighborhood_v2(graph_of_agents: Graph_of_agents, list_of_agents: list) -> None:
    """
    Функция, которая задаёт связи для неориентированного графа агентов

    Args:
        graph_of_agents (Graph_of_agents): Граф агентов
        list_of_agents (list): Список всех агентов

    Returns:
        None
    """
    graph_of_agents.creating_neighborhood(list_of_agents[0], list_of_agents[1])
    graph_of_agents.creating_neighborhood(list_of_agents[1], list_of_agents[2])
    graph_of_agents.creating_neighborhood(list_of_agents[2], list_of_agents[0])

def base_cycle(list_of_modules: list, list_of_agents: list, graph_of_agents: Graph_of_agents) -> None:
    """
    Функция, которая выполняет основной цикл работы системы

    Args:
        list_of_modules (list): Список всех модулей
        list_of_agents (list): Список всех агентов
        graph_of_agents (Graph_of_agents): Граф агентов

    Returns:
        None
    """
    print("Начало выполнения программы")

    i = 0

    count = 0
    for module in list_of_modules:
        if module.completed == False:
            count += 1

    while count > 0:
        i += 1

        for agent in list_of_agents:
            for module in list_of_modules:
                if agent.cur_module == None:
                    agent.attempt_get_module(module)
            if agent.cur_module != None:
                agent.check_breakdown()

        check = graph_of_agents.check_agents_breakdown()
        if check == False:
            return

        print(f"Текущая итерация = {i}")

        count = 0
        for module in list_of_modules:
            if module.completed == False:
                count += 1
        time.sleep(0.5)
    print(f"Агенты успешно выполнили все модули за {i} итераций")
    print()

def main_cycle(m, a, b, n, p):
    """
    Функция, которая запускает основной цикл работы программы
    Цикл работает, пока все модули не будут выполнены

    Args:
        list_of_modules (list): Список всех модулей
        list_of_agents (list): Список всех агентов

    Returns:
        None
    """
    graph_of_modules, list_of_modules = create_graph_of_modules(m, a, b)
    create_modules_dependencies_v1(graph_of_modules, list_of_modules)
    graph_of_agents, list_of_agents = create_graph_of_agents(n, p)
    create_agents_neighborhood_v1(graph_of_agents, list_of_agents)

    base_cycle(list_of_modules, list_of_agents, graph_of_agents)

    graph_of_modules, list_of_modules = create_graph_of_modules(5, 1.0, 7.1)
    create_modules_dependencies_v2(graph_of_modules, list_of_modules)
    graph_of_agents, list_of_agents = create_graph_of_agents(3, 1.5)
    create_agents_neighborhood_v2(graph_of_agents, list_of_agents)

    base_cycle(list_of_modules, list_of_agents, graph_of_agents)

    graph_of_modules, list_of_modules = create_graph_of_modules(7, 5.0, 10.1)
    create_modules_dependencies_v3(graph_of_modules, list_of_modules)
    graph_of_agents, list_of_agents = create_graph_of_agents(3, 2.0)
    create_agents_neighborhood_v2(graph_of_agents, list_of_agents)

    base_cycle(list_of_modules, list_of_agents, graph_of_agents)

m = 5
a = 1.0
b = 5.1
n = 3
p = 1.0

if __name__ == "__main__":
    main_cycle(m, a, b, n, p)
