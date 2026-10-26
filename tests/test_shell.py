"""Тесты разбора строки и простых команд."""
import os
import unittest
from unittest import mock

from shell import Shell, ShellError, ShellExit, parse_line


class ShellTests(unittest.TestCase):
    """Проверки этапа 1."""

    def setUp(self):
        """Создаёт новый интерпретатор для каждого теста."""
        self.shell = Shell()

    def test_ls_prints_args(self):
        """Заглушка ls печатает своё имя и аргументы."""
        self.assertEqual(self.shell.execute("ls -l a"), "ls -l a")

    def test_cd_prints_arg(self):
        """Заглушка cd печатает своё имя и аргумент."""
        self.assertEqual(self.shell.execute("cd docs"), "cd docs")

    def test_unknown_command(self):
        """Неизвестная команда даёт ошибку."""
        with self.assertRaises(ShellError):
            self.shell.execute("foo")

    def test_cd_too_many_args(self):
        """cd с двумя аргументами даёт ошибку."""
        with self.assertRaises(ShellError):
            self.shell.execute("cd a b")

    def test_exit(self):
        """exit завершает работу."""
        with self.assertRaises(ShellExit):
            self.shell.execute("exit")

    def test_exit_with_args(self):
        """exit с аргументом даёт ошибку."""
        with self.assertRaises(ShellError):
            self.shell.execute("exit now")

    def test_empty_line(self):
        """Пустая строка ничего не делает."""
        self.assertEqual(self.shell.execute("   "), "")

    def test_env_variable(self):
        """Переменная окружения раскрывается."""
        with mock.patch.dict(os.environ, {"EMU_TEST": "value"}):
            self.assertEqual(
                parse_line("ls $EMU_TEST ${EMU_TEST}"),
                ["ls", "value", "value"])

    def test_home_variable(self):
        """$HOME раскрывается, даже если HOME не задана в ОС."""
        with mock.patch.dict(os.environ):
            os.environ.pop("HOME", None)
            self.assertEqual(
                parse_line("ls $HOME"), ["ls", os.path.expanduser("~")])

    def test_unset_variable_removed(self):
        """Незаданная переменная исчезает, как в обычной оболочке."""
        with mock.patch.dict(os.environ):
            os.environ.pop("EMU_NOPE", None)
            self.assertEqual(parse_line("ls $EMU_NOPE a"), ["ls", "a"])

    def test_quotes(self):
        """Кавычки объединяют слова с пробелами."""
        self.assertEqual(parse_line('ls "my dir"'), ["ls", "my dir"])

    def test_unbalanced_quotes(self):
        """Незакрытая кавычка даёт ошибку разбора."""
        with self.assertRaises(ShellError):
            parse_line('ls "abc')


if __name__ == "__main__":
    unittest.main()
