
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import random as rnd
import math as mt

from Agent import *
from InfectedAgent import *
from ZombieAgent import *
from RecoveredAgent import *

def create_all_agents(n: int) -> list:
    """
    Функция, которая создаёт n агентов в случайных точках зоны 100x100

    Args:
        n (int): Кол-во агентов

    Returns:
        list_of_agents (list): Список всех агентов
    """
    list_of_agents = []
    for i in range(n):
        coords = [rnd.uniform(1, 99) for _ in range(2)]
        agent = Agent(i + 1, coords[0], coords[1])
        #agent.info()
        agent.initial_movement()
        agent.overview_calculation()
        list_of_agents.append(agent)
    return list_of_agents

def anim_multiple_agents(list_of_agents: list, m: int, t_inc_min: int, t_inc_max: int) -> None:
    """
    Функция, которая анимирует перемещение всех агентов с визуализацией их зон видимости
    и включает этап заражения и инкубации в одной анимации

    Args:
        list_of_agents (list): Список агентов
        m (int): Количество агентов, которые станут заражёнными
        t_inc_min (int): Минимальное время инкубации
        t_inc_max (int): Максимальное время инкубации

    Returns:
        None
    """
    #параметры анимации
    walk_frames = 50   #количество кадров для "прогулки"
    infection_start = walk_frames + 1   #номер кадра, с которого начинается заражение

    #настройка графика
    fig, ax = plt.subplots()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    #создаём точку и конус видимости для каждого агента
    points = []
    vision_cones = []
    typing_list = [Agent(0, 0, 0), InfectedAgent(0, 0, 0, 0), ZombieAgent(0, 0, 0, 0, 0), RecoveredAgent(0, 0, 0)]
    for agent in list_of_agents:
        if type(agent) == type(typing_list[0]):
            color = "blue"
        elif type(agent) == type(typing_list[1]):
            color = "green"
        elif type(agent) == type(typing_list[2]):
            color = "red"
        point, = ax.plot([], [], marker="o", markersize=7, color=color)   #точка-агент
        vision_cone = plt.Polygon([(agent.x, agent.y), (agent.x, agent.y), (agent.x, agent.y)], color='lightblue', alpha=0.3)   #конус видимости агента
        ax.add_patch(vision_cone)
        points.append(point)
        vision_cones.append(vision_cone)

    #инициализация анимации
    def init():
        for point, vision_cone, agent in zip(points, vision_cones, list_of_agents):
            point.set_data(agent.x, agent.y)
            vision_cone.set_xy(agent.overview)
        return points + vision_cones

    #функция для обновления каждого кадра анимации
    def update(frame):
        #этап 1: первая "прогулка" агентов
        if frame <= walk_frames:
            for i, agent in enumerate(list_of_agents):
                agent.move(list_of_agents)
                points[i].set_data(agent.x, agent.y)
                vision_cones[i].set_xy(agent.overview)

        #этап 2: заражение определённых агентов
        elif frame == infection_start:
            for i in range(m):
                agent = list_of_agents[i]
                infected_agent = InfectedAgent(agent.id, agent.x, agent.y, rnd.randint(t_inc_min, t_inc_max))
                list_of_agents[i] = infected_agent  #заменяем на заражённого агента
                points[i].set_color("green")  #обновляем цвет для заражённого

        #этап 3: основная симуляция заражения и инкубации
        else:
            for i, agent in enumerate(list_of_agents):
                agent.move(list_of_agents)   #обновляем положение агента
                points[i].set_data(agent.x, agent.y)
                vision_cones[i].set_xy(agent.overview)
                if type(agent) == type(typing_list[2]):
                    points[i].set_color("red")
                if type(agent) == type(typing_list[3]):
                    points[i].set_color("yellow")

        return points + vision_cones

    # Создание анимации
    anim = FuncAnimation(fig, update, frames=150, init_func=init, blit=True, repeat=False, interval=500)
    plt.show()

def all_simulations(pair_values: list):
    """
    Функция, которая выполняет по 1000 симуляций для каждой пары значений

    Args:
        pair_values (list): Список кортежей (пар) значений n и m

    Returns:
        None
    """
    list_all_times = []
    for pair in pair_values:
        n = pair[0]
        m = pair[1]
        num_of_iterations = 0
        for i in range(5):
            list_of_agents = create_all_agents(n)
            for _ in range(25):
                for agent in list_of_agents:
                    agent.move(list_of_agents)
            for j in range(m):
                agent = list_of_agents[j]
                infected_agent = InfectedAgent(agent.id, agent.x, agent.y, rnd.randint(t_inc_min, t_inc_max))
                list_of_agents[j] = infected_agent
            num_it = 0
            for j in range(500):
                print(f"Итерация {j} симуляции {i} пары {pair}")
                for agent in list_of_agents:
                    agent.move(list_of_agents)
                num_it += 1
                count_zombie = 0
                for agent in list_of_agents:
                    if isinstance(agent, ZombieAgent):
                        count_zombie += 1
                if count_zombie == len(list_of_agents):
                    break
            num_of_iterations += num_it
        list_all_times.append(num_of_iterations / 5)
        print(list_all_times)
        if i % 10 == 0:
            print(f"Прошло {i} симуляций для пары {pair}")

if __name__ == "__main__":
    #основные переменные
    n = 10   #кол-во агентов
    m = 5   #кол-во агентов, которые станут заражёнными
    t_inc_min = 10   #минимальное время инкубации
    t_inc_max = 25   #максимальное время инкубации
    pair_values = [(10, 5), (100, 10), (100, 25), (500, 50)]

    #создание списка всех агентов
    list_of_agents = create_all_agents(n)

    #основная симуляция
    anim_multiple_agents(list_of_agents, m, t_inc_min, t_inc_max)

    #all_simulations(pair_values)
