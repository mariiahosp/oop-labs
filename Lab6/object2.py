import atexit
import os
import tkinter as tk
from pathlib import Path

PID_FILE = Path(__file__).resolve().parent / "object2.pid"


def main():
    PID_FILE.write_text(str(os.getpid()))
    atexit.register(lambda: PID_FILE.unlink(missing_ok=True))

    root = tk.Tk()
    root.title("Object2")
    root.geometry("420x260+480+40")
    tk.Label(root, text="Object2 — згенерований вектор", font=("Arial", 16)).pack(
        expand=True
    )
    root.mainloop()


if __name__ == "__main__":
    main()
