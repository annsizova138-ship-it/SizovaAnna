"""Графический интерфейс эмулятора (tkinter)."""
import tkinter as tk

from script import ScriptError, read_script
from shell import ShellError, ShellExit

PROMPT = "$"
TEXT_HEIGHT = 24
TEXT_WIDTH = 80
END = "end"


class App:
    """Окно эмулятора: поле вывода и строка ввода."""

    def __init__(self, root, shell, vfs_name):
        """Создаёт окно; имя VFS показывается в его заголовке."""
        self.root = root
        self.shell = shell
        self.closed = False
        root.title(f"Эмулятор - VFS: {vfs_name}")
        self.output = tk.Text(
            root, state="disabled", height=TEXT_HEIGHT, width=TEXT_WIDTH)
        self.output.pack(fill="both", expand=True)
        self.entry = tk.Entry(root)
        self.entry.pack(fill="x")
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

    def print_line(self, text):
        """Добавляет строку в поле вывода."""
        if self.closed:
            return
        self.output.configure(state="normal")
        self.output.insert(END, text + "\n")
        self.output.configure(state="disabled")
        self.output.see(END)

    def on_enter(self, _event):
        """Берёт строку из поля ввода и выполняет её."""
        line = self.entry.get()
        self.entry.delete(0, END)
        self.submit(line)

    def submit(self, line):
        """Показывает ввод и выполняет команду; False при ошибке."""
        self.print_line(f"{PROMPT} {line}")
        try:
            result = self.shell.execute(line)
        except ShellExit:
            self.closed = True
            self.root.destroy()
            return False
        except ShellError as err:
            self.print_line(f"Ошибка: {err}")
            return False
        if result:
            self.print_line(result)
        return True

    def show_params(self, args):
        """Выводит параметры запуска (отладочный вывод)."""
        self.print_line("Параметры запуска:")
        self.print_line(f"  vfs    = {args.vfs}")
        self.print_line(f"  script = {args.script}")

    def run_script(self, path):
        """Выполняет стартовый скрипт и останавливается на ошибке."""
        try:
            commands = read_script(path)
        except ScriptError as err:
            self.print_line(f"Ошибка скрипта: {err}")
            return
        for number, line in commands:
            if not self.submit(line):
                self.print_line(f"Скрипт остановлен на строке {number}")
                return
