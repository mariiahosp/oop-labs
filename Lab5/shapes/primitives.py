from shapes.base import Shape


class Point(Shape):
    title = "Point"

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coords(self):
        return self.x, self.y

    def draw(self, canvas):
        radius = 3
        canvas.create_oval(
            self.x - radius,
            self.y - radius,
            self.x + radius,
            self.y + radius,
            fill="black",
            outline="black",
        )


class Line(Shape):
    title = "Line"

    def get_coords(self):
        return self.x1, self.y1, self.x2, self.y2

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas):
        options = {"fill": getattr(self, "line_color", "black"), "width": 2}
        if getattr(self, "dash", None):
            options["dash"] = self.dash
        if getattr(self, "tags", None):
            options["tags"] = self.tags
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, **options)

    def draw_rubber(self, canvas, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.dash = (4, 4)
        self.tags = "preview"
        self.draw(canvas)
        self.dash = None
        self.tags = None


class Rectangle(Shape):
    title = "Прямокутник"

    def get_coords(self):
        return self.get_bounds()

    def __init__(self, cx, cy, x, y):
        self.cx = cx
        self.cy = cy
        self.x = x
        self.y = y

    def get_bounds(self):
        left = 2 * self.cx - self.x
        top = 2 * self.cy - self.y

        return (
            min(left, self.x),
            min(top, self.y),
            max(left, self.x),
            max(top, self.y),
        )

    def draw(self, canvas):
        left, top, right, bottom = self.get_bounds()
        options = {
            "outline": getattr(self, "outline_color", "black"),
            "fill": getattr(self, "fill_color", "lightgreen"),
            "width": 2,
        }
        if getattr(self, "dash", None):
            options["dash"] = self.dash
        if getattr(self, "tags", None):
            options["tags"] = self.tags
        canvas.create_rectangle(left, top, right, bottom, **options)

    def draw_rubber(self, canvas, x1, y1, x2, y2):
        self.cx, self.cy, self.x, self.y = x1, y1, x2, y2
        self.fill_color = ""
        self.dash = (4, 4)
        self.tags = "preview"
        self.draw(canvas)
        self.dash = None
        self.tags = None


class Ellipse(Shape):
    title = "Еліпс"

    def get_coords(self):
        return self.x1, self.y1, self.x2, self.y2

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas):
        options = {
            "outline": getattr(self, "outline_color", "black"),
            "fill": getattr(self, "fill_color", ""),
            "width": 2,
        }
        if getattr(self, "dash", None):
            options["dash"] = self.dash
        if getattr(self, "tags", None):
            options["tags"] = self.tags
        canvas.create_oval(
            min(self.x1, self.x2),
            min(self.y1, self.y2),
            max(self.x1, self.x2),
            max(self.y1, self.y2),
            **options,
        )

    def draw_rubber(self, canvas, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.fill_color = ""
        self.dash = (4, 4)
        self.tags = "preview"
        self.draw(canvas)
        self.dash = None
        self.tags = None
