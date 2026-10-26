"""Точка входа эмулятора."""
import tkinter as tk

from gui import App
from shell import Shell

DEFAULT_VFS_NAME = "default"


def main():
    """Создаёт окно эмулятора и запускает его."""
    root = tk.Tk()
    App(root, Shell(), DEFAULT_VFS_NAME)
    root.mainloop()


if __name__ == "__main__":
    main()
