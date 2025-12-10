from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from .models import Book


def _ensure_path(path: str | Path) -> Path:
    """Return *path* as a :class:`Path` instance.

    Does not touch the filesystem, only coerces the type.
    """

    return path if isinstance(path, Path) else Path(path)


def load_books(path: str | Path) -> List[Book]:
    """Load all books from a JSON file.

    The JSON file must contain a list of objects with at least an ``id`` field.
    If the file does not exist, an empty list is returned.
    """

    p = _ensure_path(path)
    if not p.exists():
        return []

    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Book storage file must contain a JSON list")

    books: List[Book] = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each book entry must be a JSON object")
        books.append(Book.from_dict(item))
    return books


def save_books(path: str | Path, books: Iterable[Book]) -> None:
    """Persist *books* to *path* as a JSON list.

    The directory is created if it does not already exist.
    """

    p = _ensure_path(path)
    if p.parent and not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)

    serializable = [b.to_dict() for b in books]
    with p.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)
