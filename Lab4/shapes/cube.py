from shapes.primitives import Line, Rectangle


class CubeShape(Rectangle, Line):
    """Каркас куба без заливки.

    Обидва батьки походять від Shape, тому успадкування ромбічне.
    Rectangle.draw малює передню і задню грані лише контуром.
    Line.draw малює чотири ребра між їхніми кутами.
    Перед кожним викликом у поля відповідного батька підставляються координати
    цієї грані або цього ребра.
    """

    def __init__(self, x1, y1, x2, y2):
        Rectangle.__init__(self, x1, y1, x2, y2)
        Line.__init__(self, x1, y1, x2, y2)
        self.outline_color = "sienna"
        self.fill_color = ""
        self.line_color = "sienna"

    def _stroke(self, canvas, start, end):
        self.x1, self.y1 = start
        self.x2, self.y2 = end
        Line.draw(self, canvas)

    def draw(self, canvas):
        cx, cy, corner_x, corner_y = self.cx, self.cy, self.x, self.y
        x1, y1, x2, y2 = self.x1, self.y1, self.x2, self.y2

        left, top, right, bottom = self.get_bounds()
        depth = min(abs(right - left), abs(bottom - top)) * 0.45
        dx = dy = depth

        front = ((left, top), (right, top), (right, bottom), (left, bottom))
        back = (
            (left + dx, top - dy),
            (right + dx, top - dy),
            (right + dx, bottom - dy),
            (left + dx, bottom - dy),
        )

        self.fill_color = ""
        self.cx, self.cy = cx + dx, cy - dy
        self.x, self.y = corner_x + dx, corner_y - dy
        Rectangle.draw(self, canvas)

        self.cx, self.cy, self.x, self.y = cx, cy, corner_x, corner_y
        Rectangle.draw(self, canvas)

        for start, end in (
            (front[0], back[0]),
            (front[1], back[1]),
            (front[2], back[2]),
            (front[3], back[3]),
        ):
            self._stroke(canvas, start, end)

        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def draw_rubber(self, canvas, x1, y1, x2, y2):
        self.__init__(x1, y1, x2, y2)
        self.dash = (4, 4)
        self.tags = "preview"
        self.draw(canvas)
        self.dash = None
        self.tags = None
