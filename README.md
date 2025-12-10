# BookCatalog

A simple Python project for managing a catalog of books stored in JSON.

## Features

- Load and persist books from/to a JSON file
- Represent books with a simple `Book` data model
- List, search, add, remove, and update books
- Command Line Interface (CLI) for common operations
- Basic test suite for core operations
- Example data under `data/sample_books.json`

## Project Structure

- `book_catalog/`
  - `__init__.py`: Package initialization and convenient exports
  - `models.py`: Core data model(s), e.g. `Book`
  - `storage.py`: JSON file based storage backend
  - `operations.py`: Higher-level business operations on the catalog
  - `cli.py`: Command line interface built on top of `operations`
- `data/sample_books.json`: Sample book data file
- `main.py`: Entry point for the CLI (`python -m book_catalog` style)
- `notebooks/exploration.ipynb`: Jupyter notebook for exploratory work
- `tests/`: Unit tests for operations and storage behavior

## Installation

Use a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

There are two ways to run the app: via `main.py` or using the module form.

### Using `main.py`

```bash
python main.py --help
```

Example commands:

```bash
# List all books
python main.py list --data data/sample_books.json

# Search books by title or author
python main.py search --query "Python" --data data/sample_books.json

# Add a new book
python main.py add \
  --title "Clean Code" \
  --author "Robert C. Martin" \
  --year 2008 \
  --isbn 9780132350884 \
  --data data/sample_books.json

# Remove a book by ID
python main.py remove --id 1 --data data/sample_books.json

# Update a book
python main.py update --id 1 --title "New Title" --data data/sample_books.json
```

### Using the package directly

You can also interact with the package from Python code:

```python
from book_catalog.operations import load_catalog, list_books

books = load_catalog("data/sample_books.json")
for book in list_books(books):
    print(book)
```

## Data Model

A **Book** has the following fields:

- `id` (int): Unique identifier within a catalog
- `title` (str)
- `author` (str)
- `year` (int, optional)
- `isbn` (str, optional)

Books are stored in a JSON file as a list of objects, each representing one book.

## Running Tests

```bash
pytest
```

## Extensibility Notes

- Additional storage backends (e.g., SQLite) can be added by following the interface in `storage.py`.
- New operations (e.g., statistics or recommendations) belong in `operations.py`.
- The CLI can be extended with new subcommands in `cli.py`.
