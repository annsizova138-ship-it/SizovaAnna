"""Тесты параметров командной строки."""
import unittest

from config import parse_args


class ConfigTests(unittest.TestCase):
    """Проверки разбора параметров."""

    def test_defaults(self):
        """Без параметров обе настройки не заданы."""
        args = parse_args([])
        self.assertIsNone(args.vfs)
        self.assertIsNone(args.script)

    def test_both_params(self):
        """Оба параметра читаются."""
        args = parse_args(["--vfs", "a.json", "--script", "s.txt"])
        self.assertEqual(args.vfs, "a.json")
        self.assertEqual(args.script, "s.txt")


if __name__ == "__main__":
    unittest.main()
