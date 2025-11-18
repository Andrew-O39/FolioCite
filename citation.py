
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


@dataclass
class Book:
    """
    Simple representation of a book for citation purposes.
    """
    title: str
    authors: List[str]
    year: Optional[str] = None
    publisher: Optional[str] = None


class CitationStyle(str, Enum):
    apa = "apa"
    mla = "mla"
    chicago = "chicago"


def format_citation(book: Book, style: CitationStyle) -> str:
    """
    Format a Book object into a reference string using the given style.
    """
    if style == CitationStyle.apa:
        return format_apa(book)
    if style == CitationStyle.mla:
        return format_mla(book)
    if style == CitationStyle.chicago:
        return format_chicago(book)
    # Fallback (should not happen)
    return format_apa(book)


# --------- Helper functions for author formatting ---------

def _parse_author_name(name: str) -> str:
    """
    Convert 'First Middle Last' to 'Last, F. M.' for APA-like styles.

    This is a simple heuristic and won't be perfect, but it's good enough for a first version.
    """
    parts = [p.strip() for p in name.split() if p.strip()]
    if not parts:
        return name

    if len(parts) == 1:
        # Single word, probably a last name
        return parts[0]

    last = parts[-1]
    initials = []
    for p in parts[:-1]:
        if p and p[0].isalpha():
            initials.append(p[0].upper() + ".")

    if initials:
        return f"{last}, {' '.join(initials)}"
    else:
        return last


def _format_authors_apa(authors: List[str]) -> str:
    if not authors:
        return ""

    parsed = [_parse_author_name(a) for a in authors]

    if len(parsed) == 1:
        return parsed[0]
    if len(parsed) == 2:
        return f"{parsed[0]}, & {parsed[1]}"
    if len(parsed) == 3:
        return f"{parsed[0]}, {parsed[1]}, & {parsed[2]}"

    # More than 3 authors: list first 3 and then et al.
    first_three = ", ".join(parsed[:3])
    return f"{first_three}, et al."


def _format_authors_last_first(authors: List[str]) -> str:
    """
    Return 'Last, First and First Last' style for MLA/Chicago.

    Very simplified: only the first author is inverted.
    """
    if not authors:
        return ""

    # First author as "Last, First"
    first = authors[0]
    parts = [p.strip() for p in first.split() if p.strip()]
    if len(parts) >= 2:
        last = parts[-1]
        first_names = " ".join(parts[:-1])
        first_formatted = f"{last}, {first_names}"
    else:
        first_formatted = first

    if len(authors) == 1:
        return first_formatted

    # Remaining authors: "First Last"
    rest = authors[1:]
    if len(rest) == 1:
        return f"{first_formatted}, and {rest[0]}"
    else:
        middle = ", ".join(rest[:-1])
        last = rest[-1]
        return f"{first_formatted}, {middle}, and {last}"


# --------- Style-specific formatters ---------

def format_apa(book: Book) -> str:
    """
    Very simplified APA 7th edition style for books.
    """
    authors = _format_authors_apa(book.authors)
    year = f"({book.year})." if book.year else "(n.d.)."
    title = book.title.strip() if book.title else "[No title]"
    publisher = book.publisher.strip() if book.publisher else ""

    parts = [p for p in [authors, year, f"{title}.", publisher] if p]
    return " ".join(parts)


def format_mla(book: Book) -> str:
    """
    Very simplified MLA 9 style for books.
    """
    authors = _format_authors_last_first(book.authors)
    title = book.title.strip() if book.title else "[No title]"
    publisher = book.publisher.strip() if book.publisher else ""
    year = book.year.strip() if book.year else ""

    pieces = []
    if authors:
        pieces.append(f"{authors}.")
    pieces.append(f"{title}.")
    if publisher:
        pieces.append(publisher + ",")
    if year:
        pieces.append(year + ".")

    return " ".join(pieces)


def format_chicago(book: Book) -> str:
    """
    Very simplified Chicago author-date style for books.
    """
    authors = _format_authors_last_first(book.authors)
    year = book.year.strip() if book.year else "n.d."
    title = book.title.strip() if book.title else "[No title]"
    publisher = book.publisher.strip() if book.publisher else ""

    pieces = []
    if authors:
        pieces.append(f"{authors}.")
    pieces.append(year + ".")
    pieces.append(f"{title}.")
    if publisher:
        pieces.append(publisher + ".")

    return " ".join(pieces)
