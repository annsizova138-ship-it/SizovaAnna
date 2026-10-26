"""Разбор и выполнение команд эмулятора."""
import os
import re
import shlex

COMMAND_PREFIX = "cmd_"
ARGS_NONE = 0
ARGS_ONE = 1
HOME_VAR = "HOME"
VAR_PATTERN = re.compile(r"\$(\w+)|\$\{(\w+)\}")


class ShellError(Exception):
    """Ошибка команды; её текст показывается пользователю."""


class ShellExit(Exception):
    """Запрос на завершение работы эмулятора."""


def expand_vars(word):
    """Подставляет переменные окружения вместо $NAME и ${NAME}."""

    def replace(match):
        """Возвращает значение найденной переменной."""
        name = match.group(1) or match.group(2)
        value = os.environ.get(name)
        if value is None and name == HOME_VAR:
            value = os.path.expanduser("~")
        return value or ""

    return VAR_PATTERN.sub(replace, word)


def parse_line(line):
    """Делит строку на слова и раскрывает переменные окружения."""
    try:
        words = shlex.split(line)
    except ValueError as err:
        raise ShellError("незакрытая кавычка") from err
    result = []
    for word in words:
        expanded = expand_vars(word)
        if expanded or not word:
            result.append(expanded)
    return result


def check_args(name, args, low, high):
    """Проверяет, что число аргументов лежит в границах low..high."""
    if not low <= len(args) <= high:
        raise ShellError(f"{name}: неверное число аргументов")


class Shell:
    """Интерпретатор команд. Команда x выполняется методом cmd_x."""

    def execute(self, line):
        """Выполняет строку и возвращает текст результата."""
        words = parse_line(line)
        if not words:
            return ""
        name, args = words[0], words[1:]
        return self._find_handler(name)(args)

    def _find_handler(self, name):
        """Ищет метод команды по её имени."""
        method = COMMAND_PREFIX + name.replace("-", "_")
        handler = getattr(self, method, None)
        if handler is None:
            raise ShellError(f"{name}: команда не найдена")
        return handler

    def cmd_ls(self, args):
        """Заглушка ls: печатает своё имя и аргументы."""
        return " ".join(["ls"] + args)

    def cmd_cd(self, args):
        """Заглушка cd: печатает имя и аргумент (не более одного)."""
        check_args("cd", args, ARGS_NONE, ARGS_ONE)
        return " ".join(["cd"] + args)

    def cmd_exit(self, args):
        """Завершает работу эмулятора."""
        check_args("exit", args, ARGS_NONE, ARGS_NONE)
        raise ShellExit()
