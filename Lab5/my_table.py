import tkinter as tk
from tkinter import ttk


class MyTable:
    COLUMNS = ("name", "x1", "y1", "x2", "y2")

    def __init__(self, root):
        self.root = root
        self.window = None
        self.tree = None

    def is_open(self):
        return self.window is not None and self.window.winfo_exists()

    def open(self, shapes):
        if self.is_open():
            self.window.lift()
            self.refresh(shapes)
            return

        self.window = tk.Toplevel(self.root)
        self.window.title("Таблиця графічних об'єктів")
        self.window.geometry("480x300")
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.tree = ttk.Treeview(self.window, columns=self.COLUMNS, show="headings")
        headings = ("Назва", "x1", "y1", "x2", "y2")
        for column, text in zip(self.COLUMNS, headings):
            self.tree.heading(column, text=text)
            self.tree.column(column, width=70, anchor=tk.CENTER)
        self.tree.column("name", width=160, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.refresh(shapes)

    def close(self):
        if self.is_open():
            self.window.destroy()
        self.window = None
        self.tree = None

    def toggle(self, shapes):
        if self.is_open():
            self.close()
        else:
            self.open(shapes)

    def refresh(self, shapes):
        if not self.is_open():
            return
        self.tree.delete(*self.tree.get_children())
        for shape in shapes:
            coords = tuple(
                "" if value is None else value for value in shape.get_coords()
            )
            self.tree.insert("", tk.END, values=(shape.title, *coords))
