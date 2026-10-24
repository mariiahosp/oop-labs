from abc import ABC, abstractmethod


class Shape(ABC):
    """Спільний тип фігури. Редактор зберігає об'єкти лише як Shape."""

    @abstractmethod
    def draw(self, canvas):
        """Остаточне зображення фігури."""

    def draw_rubber(self, canvas, x1, y1, x2, y2):
        """Пунктирний гумовий слід під час введення.

        Нащадки перекривають цей метод. Базова версія нічого не малює:
        точка сліду не має.
        """
        return
