
class Ball:

    def __init__(self) -> None:
        """
        Метод, который создаёт объект-мяч с нужными полями

        Args:
            None

        Returns:
            None
        """
        self.x = None   # при инициализации мяча у него нет координат
        self.y = None

    def new_location(self, new_x: int, new_y: int) -> None:
        """
        Метод, который переносит мяч в новое местоположение

        Args:
            new_x (int): Новое положение по X
            new_y (int): Новое положение по Y

        Returns:
            None
        """
        self.x = new_x
        self.y = new_y
