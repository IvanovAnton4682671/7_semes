
from classes import *
import random as rnd
import time

def create_agents(n: int, list_of_agents: list) -> None:
    """
    Функция, которая создаёт агентов и выдаёт им случайные патенты

    Args:
        n (int): Кол-во агентов
        list_of_agents (list): Список всех агентов
    """
    for i in range(n):                          # создаём n агентов
        agent = Agent(i + 1)                    # создаём агента
        agent.info()                            # выводим информацию о нём
        list_of_agents.append(agent)            # добавляем его в общий список
    all_patents = []                            # список для всех патентов
    for agent in list_of_agents:                # перебираем всех агентов
        for patent in agent.target_task:        # перебираем все целевые патенты каждого агента
            all_patents.append(patent)          # добавляем эти патенты в общий список
    print("Все патенты:", all_patents)
    rnd.shuffle(all_patents)                    # перемешиваем все патенты
    print("Перемешанные патенты:", all_patents)
    patents_per_agent = len(all_patents) // n   # определяем по сколько патентов выдадим каждому агенту
    for i in range(patents_per_agent):          # начинаем цикл раздачи
        for agent in list_of_agents:            # выдаём для каждого агента
            patent = all_patents.pop(0)         # удаляем первый патент из списка
            agent.obtaining_a_patent(patent)    # даём этот патент агенту
    for agent in list_of_agents:                # перебираем всех агентов
        agent.info()                            # печатаем информацию

def main(list_of_agents: list, t_start: int) -> None:
    """
    Функция, отвечающая за проведение симуляции

    Args:
        list_of_agents (list): Список всех агентов
        t_start (int): Счётчик итераций
    """
    message_box = Message_Box()                                                                                      # создание объекта-коробки сообщений
    while len([agent for agent in list_of_agents if len(agent.target_task) == len(agent.important_patents)]) != n:   # запуск основного цикла
        t_start += 1                                                                                                 # увеличение счётчика итераций
        print(f"Текущая итерация: {t_start}")                                                                        # уведомление
        message_box.consilium(list_of_agents)                                                                        # основная функция коммуникации агентов
        for agent in list_of_agents:                                                                                 # перебор агентов
            if (len(agent.target_task) != len(agent.important_patents)) or agent.number_of_iteration == 0:           # условие изменения состояния агентов
                agent.update_state()                                                                                 # изменение состояния агента
            agent.info()                                                                                             # уведомление
        time.sleep(0.5)                                                                                              # удобство вывода
    for agent in list_of_agents:                                                                                     # перебор агентов
        agent.update_state()                                                                                         # итоговое увеличение итерации
        agent.win_info()                                                                                             # итоговая информация

n = 5                 # кол-во агентов
list_of_agents = []   # список всех агентов
t_start = 0           # счётчик итераций симуляции

if __name__ == "__main__":
    create_agents(n, list_of_agents)
    main(list_of_agents, t_start)
