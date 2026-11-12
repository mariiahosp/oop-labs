from abc import ABC, abstractmethod


class Shape(ABC):
    title = ""

    @abstractmethod
    def draw(self, canvas):
        pass

    @abstractmethod
    def get_coords(self):
        pass

    def draw_rubber(self, canvas, x1, y1, x2, y2):
        return
