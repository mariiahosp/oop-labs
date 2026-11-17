import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Lab6")
    root.geometry("420x260+40+40")
    tk.Label(root, text="Lab6 — менеджер", font=("Arial", 16)).pack(expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
