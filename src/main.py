"""Точка входа эмулятора."""
import tkinter as tk

from config import parse_args
from gui import App
from shell import Shell
from vfs import VfsError, empty_vfs, load_vfs

SCRIPT_DELAY_MS = 100


def open_vfs(path):
    """Загружает VFS; возвращает (vfs, текст ошибки или None)."""
    if path is None:
        return empty_vfs(), None
    try:
        return load_vfs(path), None
    except VfsError as err:
        return empty_vfs(), str(err)


def main():
    """Читает параметры, грузит VFS, создаёт окно, запускает скрипт."""
    args = parse_args()
    print(f"Параметры: vfs={args.vfs}, script={args.script}")
    vfs, error = open_vfs(args.vfs)
    root = tk.Tk()
    app = App(root, Shell(vfs), vfs.name)
    app.show_params(args)
    if error:
        app.print_line(f"Ошибка загрузки VFS: {error}")
    elif args.script:
        root.after(SCRIPT_DELAY_MS, app.run_script, args.script)
    root.mainloop()


if __name__ == "__main__":
    main()
