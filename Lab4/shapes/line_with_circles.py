from shapes.primitives import Ellipse, Line


class LineWithCircles(Line, Ellipse):
    def __init__(self, x1, y1, x2, y2):
        Line.__init__(self, x1, y1, x2, y2)
        Ellipse.__init__(self, x1, y1, x2, y2)
        self.line_color = "navy"
        self.outline_color = "navy"
        self.fill_color = "lightblue"
        self.radius = 6

    def draw(self, canvas):
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2
        radius = self.radius
        Line.draw(self, canvas)
        self.x1, self.y1 = x1 - radius, y1 - radius
        self.x2, self.y2 = x1 + radius, y1 + radius
        Ellipse.draw(self, canvas)
        self.x1, self.y1 = x2 - radius, y2 - radius
        self.x2, self.y2 = x2 + radius, y2 + radius
        Ellipse.draw(self, canvas)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def draw_rubber(self, canvas, x1, y1, x2, y2):
        self.__init__(x1, y1, x2, y2)
        self.fill_color = ""
        self.dash = (4, 4)
        self.tags = "preview"
        self.draw(canvas)
        self.dash = None
        self.tags = None
