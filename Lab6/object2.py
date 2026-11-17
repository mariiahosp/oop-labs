import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Object2")
    root.geometry("420x260+480+40")
    tk.Label(root, text="Object2 — згенерований вектор", font=("Arial", 16)).pack(
        expand=True
    )
    root.mainloop()


if __name__ == "__main__":
    main()
