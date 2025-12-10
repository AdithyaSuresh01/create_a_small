from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class Book:
    """Represents a single book in the catalog.

    Attributes
    ----------
    id:
        Unique integer identifier for the book within a catalog.
    title:
        Title of the book.
    author:
        Author or authors of the book.
    year:
        Publication year. Optional.
    isbn:
        ISBN identifier. Optional.
    """

    id: int
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the book to a plain dictionary suitable for JSON serialization."""

        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Book":
        """Create a :class:`Book` instance from a dictionary.

        Extra keys in *data* are ignored; missing optional fields default to ``None``.
        """

        return Book(
            id=int(data["id"]),
            title=str(data.get("title", "")),
            author=str(data.get("author", "")),
            year=int(data["year"]) if "year" in data and data["year"] is not None else None,
            isbn=str(data["isbn"]) if "isbn" in data and data["isbn"] is not None else None,
        )

    def __str__(self) -> str:  # pragma: no cover - trivial formatting
        pieces = [f"#{self.id}", f"{self.title}"]
        if self.author:
            pieces.append(f"by {self.author}")
        if self.year is not None:
            pieces.append(f"({self.year})")
        if self.isbn:
            pieces.append(f"ISBN: {self.isbn}")
        return " ".join(pieces)
