import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

BASE = Path(__file__).resolve().parent


def main():
    root = tk.Tk()
    root.title("Lab6")
    root.geometry("420x260+40+40")

    status = tk.Label(root, text="Lab6 — менеджер", font=("Arial", 16))
    status.pack(expand=True)

    started = {}

    def program_is_running(pid_file):
        if not pid_file.exists():
            return False
        try:
            pid = int(pid_file.read_text().strip())
            os.kill(pid, 0)
        except (OSError, ValueError):
            pid_file.unlink(missing_ok=True)
            return False
        return True

    def ensure_started(script_name):
        proc = started.get(script_name)
        if proc is not None and proc.poll() is None:
            return
        if program_is_running(BASE / f"{script_name}.pid"):
            return
        (BASE / f"{script_name}.quit").unlink(missing_ok=True)
        started[script_name] = subprocess.Popen(
            [sys.executable, BASE / f"{script_name}.py"]
        )

    def close_all():
        for name in ("object2", "object3"):
            proc = started.get(name)
            launched = proc is not None and proc.poll() is None
            if launched or program_is_running(BASE / f"{name}.pid"):
                (BASE / f"{name}.quit").write_text("quit\n")
        root.destroy()

    def open_dialog():
        dialog = tk.Toplevel(root)
        dialog.title("Dialog")
        dialog.geometry("280x180+80+80")
        dialog.transient(root)
        dialog.grab_set()
        dialog.columnconfigure(0, weight=1)
        dialog.columnconfigure(1, weight=1)

        tk.Label(dialog, text="n").grid(row=0, column=0, padx=8, pady=6, sticky="e")
        tk.Label(dialog, text="Min").grid(row=1, column=0, padx=8, pady=6, sticky="e")
        tk.Label(dialog, text="Max").grid(row=2, column=0, padx=8, pady=6, sticky="e")

        n_var = tk.StringVar()
        min_var = tk.StringVar()
        max_var = tk.StringVar()

        tk.Entry(dialog, textvariable=n_var, width=16).grid(row=0, column=1, padx=8)
        tk.Entry(dialog, textvariable=min_var, width=16).grid(row=1, column=1, padx=8)
        tk.Entry(dialog, textvariable=max_var, width=16).grid(row=2, column=1, padx=8)

        def on_execute():
            try:
                n = int(n_var.get())
                min_value = float(min_var.get())
                max_value = float(max_var.get())
            except ValueError:
                messagebox.showerror(
                    "Помилка", "n — ціле число, Min і Max — числа", parent=dialog
                )
                return
            if n <= 0 or min_value >= max_value:
                messagebox.showerror(
                    "Помилка", "Потрібно n > 0 і Min < Max", parent=dialog
                )
                return
            status.config(text=f"n = {n}\nMin = {min_value}\nMax = {max_value}")
            ensure_started("object2")
            ensure_started("object3")

            task = BASE / "object2.task"
            task.write_text(f"{n}\n{min_value}\n{max_value}")

            dialog.destroy()

        buttons = tk.Frame(dialog)
        buttons.grid(row=3, column=0, columnspan=2, sticky="ew", pady=12)
        pair = tk.Frame(buttons)
        pair.pack()
        tk.Button(pair, text="Виконати", command=on_execute).pack(side="left", padx=8)
        tk.Button(pair, text="Скасувати", command=dialog.destroy).pack(
            side="left", padx=8
        )

    menu = tk.Menu(root)
    work = tk.Menu(menu, tearoff=0)
    work.add_command(label="Виконати", command=open_dialog)
    work.add_separator()
    work.add_command(label="Вихід", command=close_all)
    menu.add_cascade(label="Робота", menu=work)
    root.config(menu=menu)

    root.protocol("WM_DELETE_WINDOW", close_all)

    root.mainloop()


if __name__ == "__main__":
    main()
