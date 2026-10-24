import tkinter as tk

from editor import MyEditor


def main():
    root = tk.Tk()
    editor = MyEditor(root)
    root.mainloop()
    editor.destroy()
    del editor


if __name__ == "__main__":
    main()
