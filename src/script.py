"""Чтение стартовых скриптов эмулятора."""

FIRST_LINE = 1
SCRIPT_ENCODING = "utf-8-sig"


class ScriptError(Exception):
    """Скрипт невозможно прочитать."""


def read_script(path):
    """Возвращает список (номер строки, команда) без пустых строк."""
    try:
        with open(path, encoding=SCRIPT_ENCODING) as handle:
            lines = handle.read().splitlines()
    except (OSError, UnicodeDecodeError) as err:
        raise ScriptError(f"не удалось прочитать {path}: {err}") from err
    numbered = enumerate(lines, start=FIRST_LINE)
    return [(number, text.strip()) for number, text in numbered
            if text.strip()]
