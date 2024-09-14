
from classes import *
import random as rnd
import time

def create_agents(number_of_agents: int) -> None:
    """
    Функция, которая создаёт всех агентов

    Args:
        number_of_agents (int): Общее кол-во агентов
    """
    for i in range(number_of_agents):
        agent = Agent(i+1)
        list_of_agents.append(agent)

def consilium(client: Client) -> int:
    """
    Функция, которая выполняет роль "консилиума" агентов (они выбирают кому отдать нового клиента)

    Args:
        client (Client): Клиент, которого "делят" агенты
    """
    if len(list_of_agents) > 0:                                                                # если список агентов не пуст
        list_of_messages = []                                                                  # создаём список сообщений агентов
        for i in range(len(list_of_agents)):                                                   # проходимся по всем агентам
            list_of_messages.append(list_of_agents[i].agent_load())                            # каждый агент записывает свою текущую загрузку
        min_load = min(list_of_messages)                                                       # находим минимальную текущую загрузку
        for i in range(len(list_of_messages)):                                                 # проходимся по всем сообщениям
            if list_of_messages[i] == min_load:                                                # если нашли минимальную текущую загрузку
                list_of_agents[i].add_to_queue(client)                                         # то по этому id (у агентов аналогичные) выдаём нового клиента
                print(f"Агент id = {list_of_agents[i].id} получил клиента id = {client.id}")   # просто уведомление
                break                                                                          # выходим из цикла

def main(n: int, m: int, ab: list, t_global: int, list_of_agents: list, list_of_clients: list) -> None:
    """
    Основная функция, которая отвечает за симуляцию

    Args:
        n (int): Общее количество агентов
        m (int): Общее количество клиентов
        ab (list): Интервал появления клиентов
        t_global (int): Общее время симуляции
        list_of_agents (list): Общий список агентов
        list_of_clients (list): Общий список клиентов
    """
    client_count = 0                                                                                                         # кол-во созданных клиентов
    create_agents(n)                                                                                                         # создание всех агентов
    next_client_time_spawn = rnd.uniform(ab[0], ab[1])                                                                       # задаём время появления следующего клиента
    while client_count < m:                                                                                                  # запускаем цикл пока не создастся m клиентов
        print(f"Текущий момент времени: {t_global}")                                                                         # отмечаем текущий момент времени
        if t_global >= next_client_time_spawn and client_count < m:                                                          # проверяем время на предмет появления и общее количество
            client = Client(client_count + 1, t_global)                                                                      # создаём клиента
            list_of_clients.append(client)                                                                                   # добавляем клиента в общий список
            print(f"Клиент {client.id} появился в момент времени {t_global}, сложность обслуживания: {client.complexity}")   # информация
            consilium(client)                                                                                                # совещания агентов при появлении нового клиента
            client_count += 1                                                                                                # увеличиваем счётчик клиентов
            next_client_time_spawn = t_global + rnd.uniform(ab[0], ab[1])                                                    # создаём время для появления следующего клиента
        for agent in list_of_agents:                                                                                         # перебираем всех агентов
            agent.update_state()                                                                                             # обновляем состояния всех агентов
        t_global += 1                                                                                                        # увеличиваем глобальное время
        time.sleep(0.05)                                                                                                     # приятный вывод
    while any(agent.agent_load() > 0 for agent in list_of_agents):                                                           # вспомогательный цикл для дообработки клиентов
        print(f"Текущий момент времени: {t_global} (ожидаем обработки оставшихся клиентов)")                                 # информация
        for agent in list_of_agents:                                                                                         # снова перебираем всех агентов
            agent.update_state()                                                                                             # обновляем состояния всех агентов
        t_global += 1                                                                                                        # увеличиваем общее время
        time.sleep(0.05)                                                                                                     # приятный вывод

n = 5                                                # кол-во агентов
m = 20                                               # кол-во клиентов
ab = sorted([rnd.uniform(1, 6) for i in range(2)])   # интервал появления клиентов
t = 0                                                # глобальное время
list_of_agents = []                                  # хранилище агентов
list_of_clients = []                                 # хранилище клиентов

if __name__ == "__main__":
    main(n, m, ab, t, list_of_agents, list_of_clients)                                                                # запуск симуляции
    sorted_agents = sorted(list_of_agents, key=lambda agent: (-agent.total_clients_served, agent.total_time_spent))   # сортировка агентов по убыванию (обслуженные) и по возрастанию (время)
    print()
    print("Отчёт об агентах:")
    for agent in sorted_agents:
        agent.agent_info()
