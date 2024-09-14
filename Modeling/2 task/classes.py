
import random as rnd
from collections import Counter

target_str = 'abcdefghijklmnopqrstuvwxyz'
len_target_task = 5

class Agent:

    def __init__(self, id_agent: int) -> None:
        """
        Конструктор, который создаёт объект типа Агент с нужными полями

        Args:
            id_agent (int): id агента
        """
        self.id = id_agent                                                                               # задаём агенту id
        self.target_task = sorted([target_str[rnd.randint(0, len(target_str) - 1)] for i in range(len_target_task)])   # создаём случайный целевой список
        self.important_patents = []                                                                      # патенты, которые агент не отдаст
        self.useless_patents = []                                                                        # патенты, которыми агент может обменяться
        self.number_of_iteration = 0                                                                     # количество итераций агента
        self.number_of_communications = 0                                                                # количество коммуникаций агента

    def info(self) -> None:
        """
        Метод, который печатает основную информацию об агенте
        """
        missing_important_patents = self.checking_task()       # получение словаря недостающих патентов
        mis_imp_pat_list = []                                  # создание списка недостающих патентов
        for key, value in missing_important_patents.items():   # перебор ключей и значений словаря недостающих патентов
            mis_imp_pat_list.extend(key * value)               # заполнение списка недостающих патентов
        mis_imp_pat_list = sorted(mis_imp_pat_list)            # сортировка списка недостающих патентов
        print(f"Агент: id = {self.id}; целевая задача: {self.target_task}; собранные патенты: {self.important_patents}; ненужные патенты: {self.useless_patents}, нужные патенты: {mis_imp_pat_list}")

    def obtaining_a_patent(self, patent: str) -> None:
        """
        Метод, который проверяет, является ли полученный патент важным, и в зависимости от результата помещает его в один из списков

        Args:
            patent (str): Получаемый патент
        """
        count_patent = self.target_task.count(patent)                                  # считаем количество таких патентов среди целевых
        if count_patent > 0 and self.important_patents.count(patent) < count_patent:   # если такой патент является целевым и среди важных таких патентов не хватает
            self.important_patents.append(patent)                                      # то добавляем патент к важным
            self.important_patents = sorted(self.important_patents)                    # сортируем список
        else:                                                                          # иначе
            self.useless_patents.append(patent)                                        # добавляем патент к бесполезным
            self.useless_patents = sorted(self.useless_patents)                        # сортируем список

    def swap(self, patent: str) -> None:
        """
        Метод, который вызывается при получении патента агентом

        Args:
            patent (str): Получаемый патент
        """
        self.number_of_communications += 1   # увеличиваем количество коммуникаций
        self.obtaining_a_patent(patent)      # вызываем метод получение патента

    def update_state(self) -> None:
        """
        Метод, который увеличивает количество итераций агента
        """
        self.number_of_iteration += 1   # увеличиваем количество итераций

    def checking_task(self) -> dict:
        """
        Метод, который составляет словарь отсутствующих нужных патентов агента

        Returns:
            dict: Словарь отсутствующих патентов
        """
        target_patent_count = Counter(self.target_task)                    # сколько раз патенты встречаются в целевой задаче
        collected_patent_count = Counter(self.important_patents)           # сколько раз патенты уже собраны
        missing_patents = {}                                               # результирующий словарь
        for patent, target_count in target_patent_count.items():           # перебор пар ключ-значение в целевых патентах
            collected_count = collected_patent_count.get(patent, 0)        # получаем сколько уже собрано патентов, или 0, если ничего не собрано
            if collected_count < target_count:                             # если собрано меньше, чем нужно
                missing_patents[patent] = target_count - collected_count   # добавляем недостающие патенты
        return missing_patents                                             # возвращаем составленный словарь

    def check_completion(self) -> bool:
        """
        Метод, который проверяет, выполнил ли агент свою целевую задачу
        """
        if dict(Counter(self.target_task)) == dict(Counter(self.important_patents)):   # проверка совпадения словарей целевой задачи и имеющихся важных патентов
            return True
        else:
            return False

    def win_info(self) -> None:
        """
        Метод, который печатает результирующую информацию при победе агентов
        """
        print(f"Агенту {self.id} для сбора целевого набора {self.target_task} потребовалось {self.number_of_iteration} итераций и {self.number_of_communications} коммуникаций")

class Message_Box:

    def __init__(self) -> None:
        pass

    def consilium(self, list_of_agents: list) -> None:
        """
        Метод, который ищет пару агентов, которые могут поменяться патентами

        Args:
            list_of_agents (list): Список всех агентов
        """
        list_of_all_useless_patents = []                                                                        # список словарей всех ненужных патентов агентов
        successful_trade = False
        for i in range(len(list_of_agents)):                                                                    # перебираем всех агентов
            patents_count = Counter(list_of_agents[i].useless_patents)                                          # считаем кол-во каждого ненужного патента 
            list_of_all_useless_patents.append(dict(patents_count))                                             # добавляем в общий список словарь для текущего агента
        for i in range(len(list_of_agents)):                                                                    # перебираем всех агентов
            missing_patents_i = list_of_agents[i].checking_task()                                               # получаем словарь недостающих патентов для i-агента
            for j in range(len(list_of_agents)):                                                                # перебираем остальных агентов
                if i != j:                                                                                      # проверка на разных агентов
                    if any(patent in list_of_all_useless_patents[j] for patent in missing_patents_i):           # если среди ненужных патентов j-го агента содержится хотя бы 1 из недостающих i-го агента
                        missing_patents_j = list_of_agents[j].checking_task()                                   # получаем словарь недостающих патентов для j-го агента
                        if any(patent in list_of_all_useless_patents[i] for patent in missing_patents_j):       # проверяем аналогично патенты для j-го агента
                            self.trade(list_of_agents[i], list_of_agents[j])                                    # если нашли такую пару, то выполняем для них обмен
                            list_of_all_useless_patents[i] = dict(Counter(list_of_agents[i].useless_patents))   # обновляем словарь ненужных патентов i-му агенту
                            list_of_all_useless_patents[j] = dict(Counter(list_of_agents[j].useless_patents))   # обновляем словарь ненужных патентов j-му агенту
                            successful_trade = True
                            break                                                                               # выходим из цикла
        if not successful_trade:                                                                                # если не нашлось ни одной пары для обмена
            for i in range(len(list_of_agents)):                                                                # перебор агентов
                if not list_of_agents[i].check_completion():                                                    # проверка, что текущий агент не выполнил целевую задачу
                    print(f"Для агента {list_of_agents[i].id} прямой обмен невозможен, ищем цепочку обменов")   # уведомление
                    chain = self.find_chain(list_of_agents, i, list_of_all_useless_patents)                     # строим цепочку обменов
                    if chain:                                                                                   # если цепь нашлась
                        print(f"Цепочка нашлась: {chain}")                                                      # то выводим её

    def trade(self, agent_1: Agent, agent_2: Agent):
        """
        Метод обмена патентами между двумя агентами

        Args:
            agent_1 (Agent): Первый агент
            agent_2 (Agent): Второй агент
        """
        patent_1 = 0
        for patent in agent_1.useless_patents:           # перебираем ненужные патенты первого агента
            if patent in agent_2.checking_task():        # проверяем, если патент нужен второму агенту
                agent_1.useless_patents.remove(patent)   # удаляем патент из ненужных у первого агента
                agent_2.swap(patent)                     # добавляем патент второму агенту
                patent_1 = patent                        # находим первый патент
                break                                    # один обмен произошёл, выходим
        patent_2 = 0
        for patent in agent_2.useless_patents:           # перебираем ненужные патенты второго агента
            if patent in agent_1.checking_task():        # проверяем, если патент нужен первому агенту
                agent_2.useless_patents.remove(patent)   # удаляем патент из ненужных у второго агента
                agent_1.swap(patent)                     # добавляем патент первому агенту
                patent_2 = patent                        # находим второй патент
                break                                    # второй обмен произошёл, выходим
        print(f"Агенты {agent_1.id} и {agent_2.id} поменялись патентами {patent_1} и {patent_2}")
        agent_1.info()
        agent_2.info()

    def find_chain(self, list_of_agents: list, i: int, list_of_all_useless_patents: list) -> None:
        """
        Метод, который циклично подбирает агентов так, чтобы они могли составить цепь обменов

        Args:
            list_of_agents (list): Список всех агентов
            i (int): Номер текущего агента в списке
            list_of_all_useless_patents (list): Список словарей всех ненужных патентов
        """
        print(f"Начинается поиск цепи для агента {list_of_agents[i].id}")                                       # уведомление
        current_agent = list_of_agents[i]                                                                       # текущий агент
        path = [list_of_agents[i].id]                                                                           # путь, по которому будем делать обмен
        visited_agents = []                                                                                     # посещённые агенты (текущего не вносим, потому что им должен закончиться путь)
        new_current_agent = self.find_next_agent(list_of_agents, current_agent, path, visited_agents)           # получаем нового агента в цепочке
        while path[0] != path[-1]:                                                                              # пока первый и последний агенты в цепи не одинаковые
            new_current_agent = self.find_next_agent(list_of_agents, new_current_agent, path, visited_agents)   # продолжаем находить новых агентов
        print(f"Нашлась цепочка агентов: {path}")                                                               # уведомление
        self.chain_exchange(list_of_agents, path, list_of_all_useless_patents)                                  # запуск цепочки обменов

    def find_next_agent(self, list_of_agents: list, current_agent: Agent, path: list, visited_agents: list) -> Agent:
        """
        Метод, который ищет агента, которому нужен ненужный патент текущего агента

        Args:
            list_of_agents (list): Список всех агентов
            current_agent (Agent): Агент, для которого ищется "нуждающийся"
            path (list): Список индексов агентов, по которым идёт поиск цепочки
            visited_agents (list): Список посещённых агентов

        Returns:
            agent: "нуждающийся" агент для текущего
        """
        for useless_patent in current_agent.useless_patents:                                         # перебираем ненужные патенты текущего агента
            for i in range(len(list_of_agents)):                                                     # начинаем перебирать всех агентов
                if list_of_agents[i] != current_agent and list_of_agents[i] not in visited_agents:   # проверяем, чтобы агенты были разные и ещё не посещённые
                    if useless_patent in list_of_agents[i].checking_task():                          # нужен ли новому агенту патент
                        path.append(list_of_agents[i].id)                                            # записываем нового агента в путь
                        visited_agents.append(list_of_agents[i])                                     # записываем нового агента в посещённые
                        print(f"Следующий агент для цепочки найден: {list_of_agents[i].id}")         # уведомление
                        return list_of_agents[i]                                                     # возвращаем нового агента

    def chain_exchange(self, list_of_agents: list, path: list, list_of_all_useless_patents: list) -> None:
        """
        Метод, который совершает обмены по цепочке

        Args:
            list_of_agents (list): Список всех агентов
            path (list): Путь обмена агентов
            list_of_all_useless_patents (list): Список словарей всех ненужных патентов
        """
        for i in range(len(path) - 1):                                                                                           # начинаем идти по цепочке обменов
            for j in range(len(list_of_agents)):                                                                                 # перебираем агентов
                if list_of_agents[j].id == path[i]:                                                                              # ищем подходящего агента
                    useless_patent = list_of_agents[j].useless_patents[0]                                                        # (костыль, но с ним почему-то всё работает) берём первый ненужный патент текущего агента
                    list_of_agents[j].useless_patents.remove(useless_patent)                                                     # удаляем этот патент
                    for k in range(len(list_of_agents)):                                                                         # начинаем перебирать агентов
                        if list_of_agents[k].id == path[i+1]:                                                                    # ищем подходящего агента
                            list_of_agents[k].swap(useless_patent)                                                               # даём ему тот патент, который удалили у предыдущего агента
                            print(f"Агент {list_of_agents[j].id} отдал патент {useless_patent} агенту {list_of_agents[k].id}")   # уведомление
                            list_of_agents[i].info()                                                                             # уведомление
                            list_of_agents[k].info()                                                                             # уведомление
                            list_of_all_useless_patents[j] = dict(Counter(list_of_agents[j].useless_patents))                    # корректируем общий список словарей ненужных патентов
