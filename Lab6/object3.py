import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Object3")
    root.geometry("420x260+40+340")
    tk.Label(root, text="Object3 — відсортований вектор", font=("Arial", 16)).pack(
        expand=True
    )
    root.mainloop()


if __name__ == "__main__":
    main()
