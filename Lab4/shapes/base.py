from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def draw(self, canvas):
        pass

    def draw_rubber(self, canvas, x1, y1, x2, y2):
        return
