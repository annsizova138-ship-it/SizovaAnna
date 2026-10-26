"""Точка входа эмулятора."""
import tkinter as tk

from config import parse_args
from gui import App
from shell import Shell

DEFAULT_VFS_NAME = "default"
SCRIPT_DELAY_MS = 100


def main():
    """Читает параметры, создаёт окно и запускает стартовый скрипт."""
    args = parse_args()
    print(f"Параметры: vfs={args.vfs}, script={args.script}")
    root = tk.Tk()
    app = App(root, Shell(), DEFAULT_VFS_NAME)
    app.show_params(args)
    if args.script:
        root.after(SCRIPT_DELAY_MS, app.run_script, args.script)
    root.mainloop()


if __name__ == "__main__":
    main()
