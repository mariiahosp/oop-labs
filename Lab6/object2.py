import atexit
import os
import tkinter as tk
from pathlib import Path

BASE = Path(__file__).resolve().parent
PID_FILE = BASE / "object2.pid"
TASK_FILE = BASE / "object2.task"


def main():
    PID_FILE.write_text(str(os.getpid()))
    atexit.register(lambda: PID_FILE.unlink(missing_ok=True))

    root = tk.Tk()
    root.title("Object2")
    root.geometry("420x260+480+40")
    status = tk.Label(root, text="Object2 — згенерований вектор", font=("Arial", 16))
    status.pack(expand=True)

    def check_task():
        if TASK_FILE.exists():
            lines = TASK_FILE.read_text().splitlines()
            TASK_FILE.unlink()
            if len(lines) == 3:
                n, min_value, max_value = lines
                status.config(
                    text=f"Отримано\nn = {n}\nMin = {min_value}\nMax = {max_value}"
                )

        root.after(200, check_task)

    check_task()
    root.mainloop()


if __name__ == "__main__":
    main()
