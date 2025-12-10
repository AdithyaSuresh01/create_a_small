"""BookCatalog package.

Provides models, storage, and operations for managing a simple JSON-backed
book catalog.

Typical usage:

    from book_catalog.operations import load_catalog, list_books

    books = load_catalog("data/sample_books.json")
    for book in list_books(books):
        print(book)
"""

from .models import Book
from .operations import (
    load_catalog,
    save_catalog,
    list_books,
    search_books,
    add_book,
    remove_book,
    update_book,
)

__all__ = [
    "Book",
    "load_catalog",
    "save_catalog",
    "list_books",
    "search_books",
    "add_book",
    "remove_book",
    "update_book",
]
