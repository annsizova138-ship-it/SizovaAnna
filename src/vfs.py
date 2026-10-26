"""Виртуальная файловая система, загружаемая из JSON-файла."""
import base64
import binascii
import hashlib
import json

TYPE_DIR = "dir"
TYPE_FILE = "file"
ENCODING_TEXT = "text"
ENCODING_BASE64 = "base64"
DEFAULT_NAME = "default"
JSON_ENCODING = "utf-8-sig"


class VfsError(Exception):
    """Ошибка загрузки VFS."""


class Node:
    """Узел VFS: папка (есть children) или файл (есть data)."""

    def __init__(self, is_dir, data=b""):
        """Создаёт узел; у папки словарь детей изначально пуст."""
        self.is_dir = is_dir
        self.data = data
        self.children = {}


class Vfs:
    """Дерево папок и файлов в памяти, его имя и SHA-256 данных."""

    def __init__(self, name, root, digest):
        """Запоминает имя, корневую папку и хеш данных."""
        self.name = name
        self.root = root
        self.digest = digest


def _decode_content(spec):
    """Превращает содержимое файла из JSON в байты."""
    content = spec.get("content", "")
    encoding = spec.get("encoding", ENCODING_TEXT)
    if not isinstance(content, str):
        raise VfsError("content файла должен быть строкой")
    if encoding == ENCODING_TEXT:
        return content.encode("utf-8")
    if encoding == ENCODING_BASE64:
        try:
            return base64.b64decode(content, validate=True)
        except (binascii.Error, ValueError) as err:
            raise VfsError(f"неверный base64: {err}") from err
    raise VfsError(f"неизвестная кодировка: {encoding}")


def _build_node(spec):
    """Рекурсивно строит узел по описанию из JSON."""
    if not isinstance(spec, dict):
        raise VfsError("узел VFS должен быть объектом JSON")
    kind = spec.get("type")
    if kind == TYPE_FILE:
        return Node(False, _decode_content(spec))
    if kind != TYPE_DIR:
        raise VfsError(f"неизвестный тип узла: {kind}")
    children = spec.get("children", {})
    if not isinstance(children, dict):
        raise VfsError("children должен быть объектом JSON")
    node = Node(True)
    for name, child in children.items():
        node.children[name] = _build_node(child)
    return node


def _read_bytes(path):
    """Читает файл целиком; ошибки превращает в VfsError."""
    try:
        with open(path, "rb") as handle:
            return handle.read()
    except FileNotFoundError as err:
        raise VfsError(f"файл VFS не найден: {path}") from err
    except OSError as err:
        raise VfsError(f"не удалось прочитать {path}: {err}") from err


def load_vfs(path):
    """Загружает VFS из JSON и считает SHA-256 байтов этого файла."""
    raw = _read_bytes(path)
    try:
        spec = json.loads(raw.decode(JSON_ENCODING))
    except (UnicodeDecodeError, json.JSONDecodeError) as err:
        raise VfsError(f"неверный формат JSON: {err}") from err
    if not isinstance(spec, dict) or "root" not in spec:
        raise VfsError("неверный формат: нет поля root")
    root = _build_node(spec["root"])
    if not root.is_dir:
        raise VfsError("неверный формат: root должен быть папкой")
    name = str(spec.get("name", DEFAULT_NAME))
    return Vfs(name, root, hashlib.sha256(raw).hexdigest())


def empty_vfs():
    """Создаёт пустую VFS (когда параметр --vfs не задан)."""
    return Vfs(DEFAULT_NAME, Node(True), hashlib.sha256(b"").hexdigest())
