"""Параметры командной строки эмулятора."""
import argparse


def parse_args(argv=None):
    """Разбирает параметры запуска; argv=None берёт sys.argv."""
    parser = argparse.ArgumentParser(
        description="Эмулятор оболочки ОС с виртуальной файловой системой")
    parser.add_argument(
        "--vfs", default=None, help="путь к файлу VFS (JSON)")
    parser.add_argument(
        "--script", default=None, help="путь к стартовому скрипту")
    return parser.parse_args(argv)
