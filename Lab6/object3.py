import atexit
import os
import tkinter as tk
from pathlib import Path

BASE = Path(__file__).resolve().parent
PID_FILE = BASE / "object3.pid"
TASK_FILE = BASE / "object3.task"

COLUMNS = 5
GEOMETRY = "560x360+40+420"


def main():
    PID_FILE.write_text(str(os.getpid()))
    atexit.register(lambda: PID_FILE.unlink(missing_ok=True))

    root = tk.Tk()
    root.title("Object3")
    root.geometry(GEOMETRY)

    tk.Label(root, text="Відсортований вектор", font=("Arial", 11), fg="#8e8e8e").pack(
        pady=(14, 0)
    )
    meta = tk.Label(root, text="очікування даних", font=("Arial", 10), fg="#8e8e8e")
    meta.pack(pady=(2, 4))

    grid = tk.Frame(root)
    grid.pack(expand=True, pady=(0, 12))

    def present_window():
        root.deiconify()
        root.geometry(GEOMETRY)
        root.lift()
        root.attributes("-topmost", True)
        root.after(150, drop_topmost)
        root.focus_force()

    def drop_topmost():
        if root.winfo_exists():
            root.attributes("-topmost", False)

    def check_task():
        quit_file = BASE / "object3.quit"
        if quit_file.exists():
            quit_file.unlink()
            root.destroy()
            return

        if TASK_FILE.exists():
            TASK_FILE.unlink()
            present_window()
            try:
                raw = root.clipboard_get()
            except tk.TclError:
                raw = ""
            try:
                values = [float(line) for line in raw.splitlines() if line.strip()]
            except ValueError:
                meta.config(text="у буфері немає чисел")
                show_vector([])
            else:
                values.sort()
                meta.config(text=f"{len(values)} чисел    відсортовано")
                show_vector(values)
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
