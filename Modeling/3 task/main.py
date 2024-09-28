
from Cort import *
from Ball import *
from Player import *
from Dummy import *
import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def game(n: int, r: int, l: int, player_pitch: list, player_tactic: str) -> bool:
    """
    Метод, который моделирует игру в теннис между игроком и болванчиком

    Args:
        n (int): Кол-во квадратов, на которое разбивается корт
        r (int): Радиус обзора игрока и болванчика
        l (int): Максимальное расстояние перемещения игрока и болванчика
        player_pitch (list): Список возможных подач игрока (первая и обычная)
        player_tactic (str): Тактика, по которой играет игрок (случайная и дальний квадрат)

    Returns:
        flag (bool): Флаг показывает, выиграл ли игрок в текущей партии
    """
    player_score = 0   # очки игрока
    dummy_score = 0    # очки болванчика
    cort = Cort(n)
    all_zones = cort.all_zones
    player = Player(r, l)
    dummy = Dummy(r, l)
    ball = Ball()
    cort.start_positions(all_zones.get("A"), all_zones.get("D"), player, dummy)

    while True:
        # игрок всегда подает первым после установки на исходные позиции
        player.zone_selection(all_zones, ball, player_pitch[0], player_tactic, dummy)  # первая подача
        # cort.print_cort_state(player, dummy, ball)

        while True:   # цикл для текущего розыгрыша мяча до тех пор, пока кто-то не проиграет
            # болванчик пытается отбить мяч
            flag_dummy = dummy.move(ball)

            if not flag_dummy:   # если болванчик не отбил мяч
                player_score += 1
                # print(f"Очко игрока! Счёт: Игрок {player_score} - {dummy_score} Болванчик")
                cort.start_positions(all_zones.get("A"), all_zones.get("D"), player, dummy)
                break   # возвращаемся к подаче игрока

            # если болванчик отбил, он подает обратно игроку
            dummy.pitch(all_zones, ball)
            # cort.print_cort_state(player, dummy, ball)
            # теперь игрок должен отбить мяч
            flag_player = player.move(ball)

            if not flag_player:   # если игрок не отбил мяч
                dummy_score += 1
                # print(f"Очко болванчика! Счёт: Игрок {player_score} - {dummy_score} Болванчик")
                cort.start_positions(all_zones.get("A"), all_zones.get("D"), player, dummy)
                break   # возвращаемся к подаче игрока

            # если оба отбили, игрок подает свою обычную подачу
            miss = player.zone_selection(all_zones, ball, player_pitch[1], player_tactic, dummy)   # последующий подачи игрока имеют шанс промаха
            if miss == True:
                dummy_score += 1
                # print(f"Игрок попал в аут! Счёт: Игрок {player_score} - {dummy_score} Болванчик")
                cort.start_positions(all_zones.get("A"), all_zones.get("D"), player, dummy)
                break
            else:
                pass
                # cort.print_cort_state(player, dummy, ball)
            #time.sleep(1)

        # проверка условий победы
        if (player_score >= 10 or dummy_score >= 10) and abs(player_score - dummy_score) >= 2:
            break   # если один из игроков набрал 40 и разница не менее 2 очков
        #time.sleep(1)

    # проверка, кто победил
    if player_score > dummy_score:
        # print("Игрок победил!")
        return True
    else:
        # print("Болванчик победил!")
        return False


if __name__ == "__main__":
    n_values = [48, 192, 432, 768]              # несколько возможных вариантов разбиения корта на квадраты
    r_values = range(1, 6)                      # радиус обзора от 1 до 5
    l_values = range(1, 11)                     # максимальное расстояние перемещения от 1 до 10
    player_pitch = ["first", "default"]
    player_tactics = ["random", "far square"]

    # проводим симуляции для каждого n
    results = {}  # результаты для каждого n будут сохраняться здесь

    for n in n_values:
        # создаём массив для хранения результатов
        player_wins = np.zeros((len(r_values), len(l_values)))

        for r_idx, r in enumerate(r_values):
            for l_idx, l in enumerate(l_values):
                player_total_win = 0
                dummy_total_win = 0

                # запускаем 100 игр
                for _ in range(100):
                    player_game_win = 0
                    dummy_game_win = 0
                    player_set_win = 0
                    dummy_set_win = 0

                    # пока кто-то не выиграет 2 сета
                    while player_set_win < 2 and dummy_set_win < 2:
                        player_game_win = 0
                        dummy_game_win = 0

                        # пока кто-то не выиграет гейм с разницей в 2
                        while True:
                            if game(n, r, l, player_pitch, player_tactics[0]):
                                player_game_win += 1
                            else:
                                dummy_game_win += 1

                            if (player_game_win >= 6 or dummy_game_win >= 6) and abs(player_game_win - dummy_game_win) >= 2:
                                break

                        # определение победителя сета
                        if player_game_win > dummy_game_win:
                            player_set_win += 1
                        else:
                            dummy_set_win += 1

                    # подсчёт победителя в соревновании
                    if player_set_win > dummy_set_win:
                        print("Игрок выиграл в соревнованиях!")
                        player_total_win += 1
                    else:
                        print("Болванчик выиграл в соревнованиях!")
                        dummy_total_win += 1

                # записываем результат (количество побед игрока) для текущего r и l
                player_wins[r_idx, l_idx] = player_total_win

        # сохраняем результаты для текущего n
        results[n] = player_wins

        # строим 3D график для текущего n
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # создаём сетку для r и l
        r_grid, l_grid = np.meshgrid(r_values, l_values)

        # транспонируем player_wins для корректного отображения на графике
        ax.plot_surface(r_grid, l_grid, player_wins.T, cmap='viridis')

        ax.set_xlabel('r (радиус обзора)')
        ax.set_ylabel('l (максимальное расстояние перемещения)')
        ax.set_zlabel('Победы игрока')
        ax.set_title(f'Результаты для n = {n}')

        plt.show()

    print(f"Завершено построение графиков для всех значений n.")
