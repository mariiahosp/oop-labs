from shapes.primitives import Line, Rectangle


class CubeShape(Rectangle, Line):
    """Каркас куба.

    Обидва батьки походять від Shape, тому успадкування ромбічне.
    draw збирається з уже готових методів:
    Rectangle.draw малює передню і задню грані, Line.draw — ребра між ними.
    Перед кожним викликом у поля відповідного батька підставляються координати
    цієї грані або цього ребра.
    """

    def __init__(self, x1, y1, x2, y2):
        Rectangle.__init__(self, x1, y1, x2, y2)
        Line.__init__(self, x1, y1, x2, y2)
        self.outline_color = "sienna"
        self.fill_color = "khaki"
        self.top_color = "#f6e7a8"
        self.side_color = "#c6b36a"
        self.line_color = "sienna"

    def _fill_face(self, canvas, points, color):
        coords = [value for point in points for value in point]
        options = {"fill": color, "outline": ""}
        if getattr(self, "tags", None):
            options["tags"] = self.tags
        canvas.create_polygon(*coords, **options)

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
        filled = bool(self.fill_color)

        self.cx, self.cy = cx + dx, cy - dy
        self.x, self.y = corner_x + dx, corner_y - dy
        saved_fill = self.fill_color
        if filled:
            self.fill_color = ""
        Rectangle.draw(self, canvas)
        self.fill_color = saved_fill

        if filled:
            self._fill_face(canvas, (front[0], front[1], back[1], back[0]), self.top_color)
            self._fill_face(canvas, (front[1], front[2], back[2], back[1]), self.side_color)

        self.cx, self.cy, self.x, self.y = cx, cy, corner_x, corner_y
        Rectangle.draw(self, canvas)

        connectors = [(front[0], back[0]), (front[1], back[1]), (front[2], back[2])]
        if not filled:
            connectors.append((front[3], back[3]))
        for start, end in connectors:
            self._stroke(canvas, start, end)

        if filled:
            self._stroke(canvas, back[0], back[1])
            self._stroke(canvas, back[1], back[2])
            self._stroke(canvas, front[0], front[1])
            self._stroke(canvas, front[1], front[2])

        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def draw_rubber(self, canvas, x1, y1, x2, y2):
        self.__init__(x1, y1, x2, y2)
        self.fill_color = ""
        self.dash = (4, 4)
        self.tags = "preview"
        self.draw(canvas)
        self.dash = None
        self.tags = None
