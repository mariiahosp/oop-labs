import atexit
import os
import tkinter as tk
from pathlib import Path
import random

BASE = Path(__file__).resolve().parent
PID_FILE = BASE / "object2.pid"
TASK_FILE = BASE / "object2.task"

COLUMNS = 5


def main():
    PID_FILE.write_text(str(os.getpid()))
    atexit.register(lambda: PID_FILE.unlink(missing_ok=True))

    root = tk.Tk()
    root.title("Object2")
    root.geometry("560x360+480+40")

    tk.Label(root, text="Згенерований вектор", font=("Arial", 11), fg="#8e8e8e").pack(
        pady=(14, 0)
    )
    meta = tk.Label(root, text="очікування параметрів", font=("Arial", 10), fg="#8e8e8e")
    meta.pack(pady=(2, 4))

    grid = tk.Frame(root)
    grid.pack(expand=True, pady=(0, 12))

    def check_task():
        quit_file = BASE / "object2.quit"
        if quit_file.exists():
            quit_file.unlink()
            root.destroy()
            return

        if TASK_FILE.exists():
            lines = TASK_FILE.read_text().splitlines()
            TASK_FILE.unlink()

            n = int(lines[0])
            min_value = float(lines[1])
            max_value = float(lines[2])
            values = [random.uniform(min_value, max_value) for _ in range(n)]
            meta.config(text=f"{n} чисел    від {min_value:g} до {max_value:g}")
            show_vector(values)

            text = "\n".join(f"{value:.3f}" for value in values)
            root.clipboard_clear()
            root.clipboard_append(text)
            root.update_idletasks()
            (BASE / "object3.task").write_text("read\n")

        root.after(200, check_task)

    def show_vector(values):
        for child in grid.winfo_children():
            child.destroy()
        for index, value in enumerate(values):
            row, column = divmod(index, COLUMNS)
            tk.Label(
                grid,
                text=f"{value:8.3f}",
                font=("Menlo", 16),
                width=8,
                anchor="e",
            ).grid(row=row, column=column, padx=8, pady=5)

    check_task()
    root.mainloop()


if __name__ == "__main__":
    main()
