"""Тесты чтения стартового скрипта."""
import os
import tempfile
import unittest

from script import ScriptError, read_script


class ScriptTests(unittest.TestCase):
    """Проверки read_script."""

    def test_skips_empty_lines(self):
        """Пустые строки пропускаются, номера строк сохраняются."""
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "s.txt")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("ls\n\ncd docs\n")
            self.assertEqual(
                read_script(path), [(1, "ls"), (3, "cd docs")])

    def test_missing_file(self):
        """Несуществующий скрипт даёт ScriptError."""
        with self.assertRaises(ScriptError):
            read_script("no_such_script.txt")


if __name__ == "__main__":
    unittest.main()
