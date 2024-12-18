
"""
TODO:
    - проверить корректность текущей игры (посмотреть как игроки выходят из игры, как берут карты)
    - изменить алгоритм атаки (добавить проверку на кол-во карт отбивающегося)
"""

from Table import Table

def simulation():
    list_of_results = [0, 0]
    for _ in range(1000):
        table = Table()
        game_result = table.game_cycle()
        if game_result == 1:
            list_of_results[0] += 1
        else:
            list_of_results[1] += 1
    print(f"Симуляции закончены, результаты: {list_of_results}")

if __name__ == "__main__":
    simulation()
    #table = Table()
    #table.game_cycle()