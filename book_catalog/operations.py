from __future__ import annotations

from dataclasses import replace
from typing import Iterable, List, Optional

from .models import Book
from .storage import load_books, save_books


def load_catalog(path: str) -> List[Book]:
    """Load a catalog of books from *path*.

    This is a thin wrapper over :func:`book_catalog.storage.load_books`.
    """

    return load_books(path)


def save_catalog(path: str, books: Iterable[Book]) -> None:
    """Save *books* to *path*.

    Thin wrapper over :func:`book_catalog.storage.save_books`.
    """

    save_books(path, books)


def list_books(books: Iterable[Book]) -> List[Book]:
    """Return a list of all books sorted by ``id``.

    The function does not mutate the input iterable.
    """

    return sorted(list(books), key=lambda b: b.id)


def search_books(books: Iterable[Book], query: str) -> List[Book]:
    """Return books whose title or author contains *query* (case-insensitive)."""

    q = query.lower().strip()
    if not q:
        return list_books(books)

    matches: List[Book] = []
    for b in books:
        haystack = f"{b.title} {b.author}".lower()
        if q in haystack:
            matches.append(b)
    return list_books(matches)


def _next_id(books: Iterable[Book]) -> int:
    max_id = 0
    for b in books:
        if b.id > max_id:
            max_id = b.id
    return max_id + 1


def add_book(
    books: List[Book],
    title: str,
    author: str,
    year: Optional[int] = None,
    isbn: Optional[str] = None,
) -> Book:
    """Create a new book, append it to *books*, and return it.

    A new ``id`` is generated as ``max(existing) + 1``, starting from 1.
    The input list *books* is mutated in-place for convenience and is also
    returned indirectly via the created :class:`Book` instance.
    """

    new_id = _next_id(books)
    book = Book(id=new_id, title=title, author=author, year=year, isbn=isbn)
    books.append(book)
    return book


def remove_book(books: List[Book], book_id: int) -> bool:
    """Remove a book with ``id == book_id`` from *books*.

    Returns ``True`` if a book was removed, or ``False`` if no such book
    existed. The list is mutated in-place.
    """

    for idx, b in enumerate(books):
        if b.id == book_id:
            del books[idx]
            return True
    return False


def update_book(
    books: List[Book],
    book_id: int,
    *,
    title: Optional[str] = None,
    author: Optional[str] = None,
    year: Optional[int] = None,
    isbn: Optional[str] = None,
) -> Optional[Book]:
    """Update a book's fields and return the updated instance.

    Only non-``None`` keyword arguments are applied. If no book with
    ``id == book_id`` is found, ``None`` is returned.
    """

    for idx, b in enumerate(books):
        if b.id != book_id:
            continue

        new_values = {}
        if title is not None:
            new_values["title"] = title
        if author is not None:
            new_values["author"] = author
        if year is not None:
            new_values["year"] = year
        if isbn is not None:
            new_values["isbn"] = isbn

        if not new_values:
            return b

        updated = replace(b, **new_values)
        books[idx] = updated
        return updated

    return None
