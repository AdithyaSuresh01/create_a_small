from __future__ import annotations

from book_catalog.models import Book
from book_catalog.operations import (
    add_book,
    list_books,
    remove_book,
    search_books,
    update_book,
)


def _sample_books():
    return [
        Book(id=1, title="A", author="Author One", year=2000, isbn="111"),
        Book(id=2, title="B", author="Author Two", year=2001, isbn="222"),
        Book(id=3, title="Python Guide", author="Expert", year=2020, isbn="333"),
    ]


def test_list_books_sorts_by_id():
    books = _sample_books()[::-1]  # reversed order
    sorted_books = list_books(books)
    assert [b.id for b in sorted_books] == [1, 2, 3]


def test_search_books_matches_title_or_author_case_insensitive():
    books = _sample_books()
    results = search_books(books, "python")
    assert len(results) == 1
    assert results.title == "Python Guide"

    # empty query returns all
    all_results = search_books(books, " ")
    assert len(all_results) == len(books)


def test_add_book_assigns_incremental_id_and_appends():
    books = _sample_books()
    new = add_book(books, title="New", author="Someone")
    assert new.id == 4
    assert books[-1] is new


def test_remove_book_removes_and_returns_true():
    books = _sample_books()
    ok = remove_book(books, 2)
    assert ok is True
    assert [b.id for b in books] == [1, 3]


def test_remove_book_returns_false_if_not_found():
    books = _sample_books()
    ok = remove_book(books, 99)
    assert ok is False
    assert len(books) == 3


def test_update_book_updates_fields_and_returns_book():
    books = _sample_books()
    updated = update_book(books, 1, title="New Title", year=2010)
    assert updated is not None
    assert updated.title == "New Title"
    assert updated.year == 2010
    # ensure list is updated
    assert books.title == "New Title"


def test_update_book_returns_none_if_not_found():
    books = _sample_books()
    updated = update_book(books, 99, title="X")
    assert updated is None
