from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import click

from .operations import (
    add_book,
    list_books,
    load_catalog,
    remove_book,
    save_catalog,
    search_books,
    update_book,
)


def _default_data_path() -> str:
    return str(Path("data") / "sample_books.json")


@click.group()
@click.option(
    "--data",
    "data_path",
    type=click.Path(dir_okay=False, path_type=str),
    default=_default_data_path,
    show_default=True,
    help="Path to the JSON file that stores the catalog.",
)
@click.pass_context
def cli(ctx: click.Context, data_path: str) -> None:
    """Book catalog command line interface."""

    ctx.ensure_object(dict)
    ctx.obj["data_path"] = data_path


@cli.command("list")
@click.pass_context
def list_cmd(ctx: click.Context) -> None:
    """List all books in the catalog."""

    data_path = ctx.obj["data_path"]
    books = load_catalog(data_path)
    for b in list_books(books):
        click.echo(str(b))


@cli.command("search")
@click.option("--query", "query", required=True, help="Text to search in title/author.")
@click.pass_context
def search_cmd(ctx: click.Context, query: str) -> None:
    """Search for books by title or author."""

    data_path = ctx.obj["data_path"]
    books = load_catalog(data_path)
    results = search_books(books, query=query)
    if not results:
        click.echo("No books found.")
        return
    for b in results:
        click.echo(str(b))


@cli.command("add")
@click.option("--title", required=True, help="Title of the book.")
@click.option("--author", required=True, help="Author of the book.")
@click.option("--year", type=int, required=False, help="Publication year.")
@click.option("--isbn", required=False, help="ISBN of the book.")
@click.pass_context
def add_cmd(
    ctx: click.Context,
    title: str,
    author: str,
    year: Optional[int],
    isbn: Optional[str],
) -> None:
    """Add a new book to the catalog."""

    data_path = ctx.obj["data_path"]
    books = load_catalog(data_path)
    book = add_book(books, title=title, author=author, year=year, isbn=isbn)
    save_catalog(data_path, books)
    click.echo(f"Added book: {book}")


@cli.command("remove")
@click.option("--id", "book_id", type=int, required=True, help="ID of the book to remove.")
@click.pass_context
def remove_cmd(ctx: click.Context, book_id: int) -> None:
    """Remove a book by ID."""

    data_path = ctx.obj["data_path"]
    books = load_catalog(data_path)
    removed = remove_book(books, book_id)
    if not removed:
        click.echo("No book with that ID found.")
        raise SystemExit(1)
    save_catalog(data_path, books)
    click.echo(f"Removed book with id {book_id}.")


@cli.command("update")
@click.option("--id", "book_id", type=int, required=True, help="ID of the book to update.")
@click.option("--title", required=False, help="New title.")
@click.option("--author", required=False, help="New author.")
@click.option("--year", type=int, required=False, help="New year.")
@click.option("--isbn", required=False, help="New ISBN.")
@click.pass_context
def update_cmd(
    ctx: click.Context,
    book_id: int,
    title: Optional[str],
    author: Optional[str],
    year: Optional[int],
    isbn: Optional[str],
) -> None:
    """Update an existing book's details."""

    data_path = ctx.obj["data_path"]
    books = load_catalog(data_path)
    updated = update_book(
        books,
        book_id,
        title=title,
        author=author,
        year=year,
        isbn=isbn,
    )
    if updated is None:
        click.echo("No book with that ID found.")
        raise SystemExit(1)
    save_catalog(data_path, books)
    click.echo(f"Updated book: {updated}")


def main(argv: Optional[list[str]] = None) -> int:
    """Entry point for running the CLI from Python code.

    Returns an exit status code compatible with :func:`sys.exit`.
    """

    argv = list(argv) if argv is not None else None
    try:
        cli.main(args=argv, prog_name="book-catalog", standalone_mode=True)
    except SystemExit as exc:  # click exits using SystemExit
        return int(exc.code or 0)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main(sys.argv[1:]))
