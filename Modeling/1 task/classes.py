
import random as rnd
from collections import deque

class Client:

    def __init__(self, client_id: int, client_arrival_time: float) -> None:
        """
        Конструктор, который создаёт объект класса Клиент с нужными полями

        Args:
            client_id (int): Id, который присваивается каждому клиенту
            client_arrival_time (float): Время появления данного клиента
        """
        self.id = client_id                       # id клиента
        self.complexity = rnd.randint(1, 10)      # сложность обслуживания клиента
        self.arrival_time = client_arrival_time   # время появления клиента

class Agent:

    def __init__(self, agent_id: int) -> None:
        """
        Конструктор, который создаёт объект класса Агент с нужными полями

        Args:
            agent_id (int): Id, который присваивается каждому агенту
        """
        self.id = agent_id              # id агента
        self.queue = deque()            # очередь клиентов данного агента
        self.current_client = None      # текущий клиент, которого обслуживает агент
        self.remaining_time = 0         # время, оставшееся до конца обслуживания текущего клиента
        self.total_clients_served = 0   # кол-во обслуженных клиентов
        self.total_time_spent = 0       # кол-во затраченного времени

    def agent_info(self) -> None:
        """
        Метод, который выводит краткую информацию об агенте
        """
        print(f"Агент: id = {self.id}, обслужено клиентов = {self.total_clients_served}, потрачено времени = {self.total_time_spent}")

    def agent_load(self) -> int:
        """
        Метод, который возвращает текущую загрузку агента
        """
        queue_load = sum(client.complexity for client in self.queue)   # загрузка очереди
        return self.remaining_time + queue_load                        # загрузка очереди + оставшееся время обслуживания

    def add_to_queue(self, client: Client):
        """
        Метод, который добавляет нового клиента в очередь агенту

        Args:
            client (Client): Клиент, который добавляется в очередь
        """
        self.queue.append(client)         # добавляем клиента в очередь
        if self.current_client is None:   # если сейчас никакой клиент не обслуживается
            self.start_next_client()      # то стартуем обработку нового клиента

    def start_next_client(self):
        """
        Метод, который берёт в обработку следующего клиента из очереди
        """
        if (len(self.queue) > 0):                                  # проверка очереди на наличие клиентов
            self.current_client = self.queue.popleft()             # делаем активным нового клиента
            self.remaining_time = self.current_client.complexity   # устанавливаем текущую загрузку клиента

    def update_state(self) -> None:
        """
        Метод, который обновляет состояние агента
        """
        if self.current_client is not None:                               # если сейчас есть обслуживаемый клиент
            self.remaining_time -= 1                                      # уменьшаем оставшееся время обслуживания
            if self.remaining_time <= 0:                                  # если оставшееся время <= 0
                self.total_clients_served += 1                            # прибавляем одного клиента к обслуженным
                self.total_time_spent += self.current_client.complexity   # прибавляем его сложность к затраченному времени
                self.remaining_time = 0                                   # устанавливаем новое оставшееся время обслуживания
                self.current_client = None                                # устанавливаем отсутствие текущего клиента
                self.start_next_client()                                  # стартуем обслуживание нового клиента
