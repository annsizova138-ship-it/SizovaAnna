"""Тесты загрузки VFS из JSON и команды vfs-info."""
import hashlib
import json
import os
import tempfile
import unittest

from shell import Shell
from vfs import VfsError, empty_vfs, load_vfs

SAMPLE = {
    "name": "test",
    "root": {"type": "dir", "children": {
        "a.txt": {"type": "file", "content": "hello"},
        "bin": {"type": "file", "encoding": "base64",
                "content": "AAEC/w=="},
        "docs": {"type": "dir", "children": {
            "b.txt": {"type": "file", "content": "hi"}}},
    }},
}


def write_json(folder, data):
    """Записывает data в vfs.json внутри folder и возвращает путь."""
    path = os.path.join(folder, "vfs.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle)
    return path


def load_spec(spec):
    """Загружает VFS, описанную словарём spec."""
    with tempfile.TemporaryDirectory() as folder:
        return load_vfs(write_json(folder, spec))


class LoadTests(unittest.TestCase):
    """Проверки load_vfs."""

    def test_load_ok(self):
        """Корректный файл загружается, имя берётся из JSON."""
        vfs = load_spec(SAMPLE)
        self.assertEqual(vfs.name, "test")
        self.assertTrue(vfs.root.children["docs"].is_dir)
        self.assertIn("b.txt", vfs.root.children["docs"].children)

    def test_text_and_binary_data(self):
        """Текст кодируется в UTF-8, base64 декодируется."""
        vfs = load_spec(SAMPLE)
        self.assertEqual(vfs.root.children["a.txt"].data, b"hello")
        self.assertEqual(vfs.root.children["bin"].data,
                         bytes([0, 1, 2, 255]))

    def test_digest(self):
        """SHA-256 считается от байтов файла."""
        with tempfile.TemporaryDirectory() as folder:
            path = write_json(folder, SAMPLE)
            with open(path, "rb") as handle:
                expected = hashlib.sha256(handle.read()).hexdigest()
            self.assertEqual(load_vfs(path).digest, expected)

    def test_missing_file(self):
        """Нет файла - ошибка."""
        with self.assertRaises(VfsError):
            load_vfs("no_such_vfs.json")

    def test_broken_json(self):
        """Битый JSON - ошибка."""
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "bad.json")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("{ not json")
            with self.assertRaises(VfsError):
                load_vfs(path)

    def test_bad_structure(self):
        """Нет root, неизвестный тип, неверный base64 - ошибки."""
        bad_specs = [
            {"name": "x"},
            {"root": {"type": "link"}},
            {"root": {"type": "dir", "children": {
                "d": {"type": "file", "encoding": "base64",
                      "content": "!!!"}}}},
        ]
        for spec in bad_specs:
            with self.assertRaises(VfsError):
                load_spec(spec)


class VfsInfoTests(unittest.TestCase):
    """Проверка команды vfs-info."""

    def test_vfs_info(self):
        """Команда выводит имя и SHA-256."""
        vfs = load_spec(SAMPLE)
        text = Shell(vfs).execute("vfs-info")
        self.assertIn("VFS: test", text)
        self.assertIn(vfs.digest, text)

    def test_vfs_info_default(self):
        """Без --vfs используется пустая VFS с именем default."""
        text = Shell().execute("vfs-info")
        self.assertIn(empty_vfs().name, text)


if __name__ == "__main__":
    unittest.main()
