import os
import tkinter as tk
from tkinter import messagebox, filedialog
from my_table import MyTable
import csv

from shapes import CubeShape, Ellipse, Line, LineWithCircles, Point, Rectangle
from tooltip import ToolTip

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Tool:
    def __init__(self, label, shape_cls, tip, icon_file):
        self.label = label
        self.shape_cls = shape_cls
        self.tip = tip
        self.icon_file = icon_file

    @property
    def name(self):
        return self.shape_cls.__name__


class MyEditor:
    _instance = None

    TOOLS = (
        Tool("Точка", Point, "Намалювати точку", "point.png"),
        Tool("Лінія", Line, "Намалювати лінію", "line.png"),
        Tool("Прямокутник", Rectangle, "Намалювати прямокутник", "rectangle.png"),
        Tool("Еліпс", Ellipse, "Намалювати еліпс", "ellipse.png"),
        Tool(
            "Лінія з кружечками",
            LineWithCircles,
            "Намалювати лінію з кружечками",
            "line_circles.png",
        ),
        Tool("Каркас куба", CubeShape, "Намалювати каркас куба", "cube.png"),
    )

    @classmethod
    def get_instance(cls, root):
        if cls._instance is None:
            cls._instance = cls(root)
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, root):
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self.root = root

        self.current_shape = self.TOOLS[0].name
        self.root.geometry("900x600")

        self.max_shapes = 107
        self.shapes = [None] * self.max_shapes
        self.shape_count = 0

        self.drawing_shape = self.current_shape
        self.drawing_allowed = True

        self.start_x = 0
        self.start_y = 0

        self.icons = {}
        self.tool_buttons = {}
        self.tool_icons = {}

        self.create_menu()
        self.create_toolbar()
        self.create_canvas()
        self.bind_mouse_events()
        self.update_shape_indicator()

        self.table = MyTable(
            self.root,
            on_select=self.highlight_shape,
            on_delete=self.delete_shape,
        )

    def destroy(self):
        self.table.close()
        self.shapes = None
        self.shape_count = 0
        self.icons.clear()
        self.tool_buttons.clear()
        self.tool_icons.clear()
        self.canvas = None
        self.root = None

    def tool_by_name(self, shape_name):
        for tool in self.TOOLS:
            if tool.name == shape_name:
                return tool
        return None

    def highlight_shape(self, index):
        self.canvas.delete("highlight")
        if index is None or index >= self.shape_count:
            return

        shape = self.shapes[index]
        x1, y1, x2, y2 = shape.highlight_box()
        if x2 is None:
            x2 = x1
        if y2 is None:
            y2 = y1
        pad = 6
        self.canvas.create_rectangle(
            min(x1, x2) - pad,
            min(y1, y2) - pad,
            max(x1, x2) + pad,
            max(y1, y2) + pad,
            outline="red",
            width=2,
            tags="highlight",
        )

    def delete_shape(self, index):
        if index is None or index >= self.shape_count:
            return
        self.root.after_idle(lambda index=index: self.remove_shape(index))

    def remove_shape(self, index):
        if index >= self.shape_count:
            return
        for i in range(index, self.shape_count - 1):
            self.shapes[i] = self.shapes[i + 1]
        self.shape_count -= 1
        self.shapes[self.shape_count] = None
        self.canvas.delete("all")
        for shape in self.shapes[: self.shape_count]:
            shape.draw(self.canvas)
        self.refresh_table()

    def shape_label(self, shape_name):
        tool = self.tool_by_name(shape_name)
        if tool is None:
            return shape_name
        return tool.label

    def update_shape_indicator(self):
        self.root.title(f"Lab5 — {self.shape_label(self.current_shape)}")
        self.update_toolbar()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Відкрити", command=self.load_shapes)
        file_menu.add_command(label="Зберегти", command=self.save_shapes)
        file_menu.add_command(label="Очистити", command=self.clear_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.root.destroy)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        self.objects_menu = tk.Menu(menu_bar, tearoff=0)
        self.shape_var = tk.StringVar(value=self.current_shape)

        for tool in self.TOOLS:
            self.objects_menu.add_radiobutton(
                label=tool.label,
                variable=self.shape_var,
                value=tool.name,
                command=self.select_shape,
            )

        menu_bar.add_cascade(label="Об'єкти", menu=self.objects_menu)

        self.table_menu = tk.Menu(menu_bar, tearoff=0)
        self.table_menu.add_command(
            label="Відкрити / закрити", command=self.toggle_table
        )
        menu_bar.add_cascade(label="Таблиця", menu=self.table_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Про програму", command=self.show_about)
        menu_bar.add_cascade(label="Довідка", menu=help_menu)

        self.root.config(menu=menu_bar)

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED, bg="#e4e4e4")
        toolbar.pack(side=tk.TOP, fill=tk.X)

        for tool in self.TOOLS:
            image = tk.PhotoImage(file=os.path.join(BASE_DIR, "icons", tool.icon_file))
            self.icons[tool.name] = image

            # Не Button: на macOS системна кнопка не зберігає втиснутий вигляд.
            button = tk.Frame(toolbar, bd=2, relief=tk.RAISED, bg="#f3f3f3")
            icon = tk.Label(
                button,
                image=image,
                bg="#f3f3f3",
                bd=0,
                padx=5,
                pady=5,
                cursor="hand2",
            )
            icon.pack()
            button.pack(side=tk.LEFT, padx=3, pady=3)

            for widget in (button, icon):
                widget.bind(
                    "<Button-1>",
                    lambda event, name=tool.name: self.select_shape_by_name(name),
                )
            ToolTip(icon, tool.tip)
            self.tool_buttons[tool.name] = button
            self.tool_icons[tool.name] = icon

    def update_toolbar(self):
        for name, button in self.tool_buttons.items():
            selected = name == self.current_shape
            bg = "#c4c4c4" if selected else "#f3f3f3"
            button.config(relief=tk.SUNKEN if selected else tk.RAISED, bg=bg)
            self.tool_icons[name].config(bg=bg)

    def select_shape_by_name(self, shape_name):
        self.current_shape = shape_name
        self.shape_var.set(shape_name)
        self.update_shape_indicator()

    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def select_shape(self):
        self.current_shape = self.shape_var.get()
        self.update_shape_indicator()

    def bind_mouse_events(self):
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def add_shape(self, shape):
        self.shapes[self.shape_count] = shape
        self.shape_count += 1
        shape.draw(self.canvas)
        self.refresh_table()

    def toggle_table(self):
        self.table.toggle(self.shapes[: self.shape_count])

    def toggle_table_menu(self):
        self.toggle_table()
        self.root.after(0, self.table_menu.unpost)

    def refresh_table(self):
        self.table.refresh(self.shapes[: self.shape_count])

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.drawing_shape = self.current_shape

        self.drawing_allowed = self.shape_count < self.max_shapes

        if not self.drawing_allowed:
            messagebox.showwarning(
                "Попередження",
                f"Досягнуто межу в {self.max_shapes} об'єктів.",
            )
            return
        tool = self.tool_by_name(self.drawing_shape)
        if tool.shape_cls is Point:
            self.add_shape(tool.shape_cls(event.x, event.y))

    def on_mouse_move(self, event):
        if not self.drawing_allowed:
            return
        tool = self.tool_by_name(self.drawing_shape)
        if tool.shape_cls is Point:
            return
        self.canvas.delete("preview")
        preview = tool.shape_cls(self.start_x, self.start_y, event.x, event.y)
        preview.draw_rubber(self.canvas, self.start_x, self.start_y, event.x, event.y)

    def on_mouse_up(self, event):
        self.canvas.delete("preview")

        if not self.drawing_allowed:
            return

        tool = self.tool_by_name(self.drawing_shape)
        if tool.shape_cls is Point:
            return
        shape = tool.shape_cls(self.start_x, self.start_y, event.x, event.y)
        self.add_shape(shape)

    def load_shapes(self):
        path = filedialog.askopenfilename(
            filetypes=[("CSV", "*.csv")],
            title="Відкрити об'єкти",
        )
        if not path:
            return

        by_title = {tool.shape_cls.title: tool.shape_cls for tool in self.TOOLS}
        loaded = []

        with open(path, newline="", encoding="utf-8") as file:
            for row in csv.reader(file):
                if not row or row[0] == "type":
                    continue
                title, x1, y1, x2, y2 = row
                shape_cls = by_title.get(title)
                if shape_cls is None:
                    continue
                x1, y1 = int(x1), int(y1)
                x2 = int(x2) if x2 else None
                y2 = int(y2) if y2 else None
                loaded.append(shape_cls.from_coords(x1, y1, x2, y2))

        self.clear_canvas()
        for shape in loaded[: self.max_shapes]:
            self.add_shape(shape)

    def save_shapes(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Зберегти об'єкти",
        )
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["type", "x1", "y1", "x2", "y2"])
            for shape in self.shapes[: self.shape_count]:
                coords = tuple(
                    "" if value is None else value for value in shape.get_coords()
                )
                writer.writerow((shape.title, *coords))

    def clear_canvas(self):
        self.shapes = [None] * self.max_shapes
        self.shape_count = 0
        self.canvas.delete("all")
        self.refresh_table()

    def show_about(self):
        messagebox.showinfo(
            "Про програму",
            "Lab5 — графічний редактор об'єктів.\n" "Розроблено на Python і Tkinter.",
        )
