import atexit
import os
import tkinter as tk
from pathlib import Path

PID_FILE = Path(__file__).resolve().parent / "object3.pid"


def main():
    PID_FILE.write_text(str(os.getpid()))
    atexit.register(lambda: PID_FILE.unlink(missing_ok=True))

    root = tk.Tk()
    root.title("Object3")
    root.geometry("420x260+40+340")
    tk.Label(root, text="Object3 — відсортований вектор", font=("Arial", 16)).pack(
        expand=True
    )
    root.mainloop()


if __name__ == "__main__":
    main()
