
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
    place: Optional[str] = None
    cover_url: Optional[str] = None      # Open Library cover image URL

class CitationStyle(str, Enum):
    apa = "apa"
    mla = "mla"
    chicago = "chicago"
    harvard = "harvard"
    vancouver = "vancouver"


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
    if style == CitationStyle.harvard:
        return format_harvard(book)
    if style == CitationStyle.vancouver:
        return format_vancouver(book)
    # Fallback
    return format_apa(book)

# --------- Helper functions for author formatting ---------

def _parse_author_name(name: str) -> str:
    """
    Convert 'First Middle Last' to 'Last, F. M.' for APA/Harvard/Chicago-ish styles.
    Simple heuristic; not perfect but good enough for a prototype.
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
    """
    APA-like author list:
    One: Smith, J.
    Two: Smith, J., & Doe, A.
    Three: Smith, J., Doe, A., & Brown, T.
    Four+: Smith, J., Doe, A., Brown, T., et al.
    """
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
    Generic 'Last, First and First Last' style.

    Very simplified: only the first author is inverted.
    e.g. "Kahneman, Daniel and Amos Tversky"
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


def _format_authors_mla(authors: List[str]) -> str:
    """
    MLA-style author list (simplified):

    1 author:   Last, First
    2 authors:  Last, First, and First Last
    3+ authors: Last, First, et al.
    """
    if not authors:
        return ""

    # Invert only the first author for MLA
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
    if len(authors) == 2:
        return f"{first_formatted}, and {authors[1]}"

    # 3 or more authors
    return f"{first_formatted}, et al."


def _format_authors_chicago(authors: List[str]) -> str:
    """
    Very simplified Chicago author-date author list:

    1 author:  Last, First
    2–3:       'Last, First, Second, and Third'
               (using _format_authors_last_first)
    4+:        'Last, First, et al.'
    """
    if not authors:
        return ""

    if len(authors) <= 3:
        # Reuse the more generic helper for up to 3 authors
        return _format_authors_last_first(authors)

    # 4+ authors: First author (inverted) + 'et al.'
    first = _format_authors_last_first(authors[:1])
    return f"{first}, et al."


def _format_authors_harvard(authors: List[str]) -> str:
    """
    Very simple Harvard-style author list.

    Uses 'and' between the last two authors and 'et al.' for 4+ authors.
    Authors are formatted as 'Last, F.' using _parse_author_name.
    """
    if not authors:
        return ""

    parsed = [_parse_author_name(a) for a in authors]

    if len(parsed) == 1:
        return parsed[0]
    if len(parsed) == 2:
        return f"{parsed[0]} and {parsed[1]}"
    if len(parsed) == 3:
        return f"{parsed[0]}, {parsed[1]} and {parsed[2]}"

    # More than 3 authors: "FirstAuthor et al."
    return f"{parsed[0]} et al."

def _format_authors_vancouver(authors: List[str]) -> str:
    """
    Very simplified Vancouver author list.

    Pattern:
    'Bawumia M' or 'Smith AB, Jones CD'

    - Last word is treated as surname
    - All preceding words give initials
    """
    parts = []
    for name in authors:
        tokens = [t.strip() for t in name.split() if t.strip()]
        if not tokens:
            continue
        last = tokens[-1]
        initials = "".join(t[0].upper() for t in tokens[:-1] if t)
        if initials:
            parts.append(f"{last} {initials}")
        else:
            parts.append(last)
    return ", ".join(parts)

def _format_authors_bibtex(authors: List[str]) -> str:
    """
    Format authors for BibTeX.

    Very simple approach:
    - Convert 'First Middle Last' to 'Last, First Middle'
    - Join multiple authors with ' and '
    """
    formatted = []

    for name in authors:
        parts = [p.strip() for p in name.split() if p.strip()]
        if not parts:
            continue
        if len(parts) == 1:
            # Single word, treat as last name
            formatted.append(parts[0])
        else:
            last = parts[-1]
            first_names = " ".join(parts[:-1])
            formatted.append(f"{last}, {first_names}")

    return " and ".join(formatted)

def _make_bibtex_key(book: Book) -> str:
    """
    Create a simple BibTeX key like 'Kahneman2011Thinking'.

    - Use the last name of the first author (if available)
    - Use the year (or 'n.d.')
    - Use first word of the title (alphanumeric only)
    """
    # Author part
    if book.authors:
        first_author = book.authors[0].strip()
        parts = first_author.split()
        author_part = parts[-1] if parts else "key"
    else:
        author_part = "key"

    # Year part
    year_part = (book.year or "nd").strip()

    # Title part: first word, stripped of non-alphanumerics
    if book.title:
        first_word = book.title.split()[0]
        title_part = "".join(ch for ch in first_word if ch.isalnum())
    else:
        title_part = "ref"

    # Combine and remove problematic characters
    key = f"{author_part}{year_part}{title_part}"
    key = "".join(ch for ch in key if ch.isalnum())
    return key or "ref"


# --------- Helper functions for title capitalization ---------

def _to_sentence_case(text: str) -> str:
    """
    Convert a title to simple sentence case:
    - Capitalize the first word.
    - Lowercase other words, unless the word is already ALL CAPS (to preserve acronyms).
    """
    if not text:
        return text

    words = text.strip().split()
    if not words:
        return text

    first = words[0]
    first = first[0].upper() + first[1:]

    rest_words = []
    for w in words[1:]:
        if w.isupper():
            # keep acronyms like "EU", "USA"
            rest_words.append(w)
        else:
            rest_words.append(w.lower())

    return " ".join([first] + rest_words)


def _to_title_case(text: str) -> str:
    """
    Convert a title to simple title case (for MLA):

    - Capitalize first and last words.
    - Capitalize 'important' words.
    - Keep small words (a, an, the, of, in, on, etc.) lowercase,
      unless they are the first word.
    """
    if not text:
        return text

    small_words = {
        "and", "or", "but", "for", "nor",
        "a", "an", "the",
        "as", "at", "by", "for", "in", "of", "on", "per", "to", "via"
    }

    words = text.strip().split()
    if not words:
        return text

    def cap_word(w: str) -> str:
        if w.isupper():
            return w  # preserve acronyms
        return w[0].upper() + w[1:].lower() if w else w

    titled = []
    for i, w in enumerate(words):
        lw = w.lower()
        if i == 0 or i == len(words) - 1:
            # Always capitalize first & last word
            titled.append(cap_word(w))
        elif lw in small_words:
            titled.append(lw)
        else:
            titled.append(cap_word(w))

    return " ".join(titled)


# --------- Style-specific formatters ---------

def format_apa(book: Book) -> str:
    """
    APA (approx Google Scholar):
    Bawumia, M. (2004). A life in the political history of Ghana: Memoirs of Alhaji Mumuni Bawumia. Ghana University Press.
    """
    authors = _format_authors_apa(book.authors)
    year = f"({book.year.strip()})." if book.year else "(n.d.)."
    raw_title = book.title.strip() if book.title else "[No title]"
    title = _to_sentence_case(raw_title)
    publisher = book.publisher.strip() if book.publisher else ""

    parts = [p for p in [authors, year, f"{title}.", publisher] if p]
    return " ".join(parts)


def format_mla(book: Book) -> str:
    """
    MLA (approx Google Scholar):
    Bawumia, Mumuni. A life in the political history of Ghana: Memoirs of Alhaji Mumuni Bawumia. Ghana University Press, 2004.
    """
    authors = _format_authors_mla(book.authors)
    raw_title = book.title.strip() if book.title else "[No title]"
    title = _to_title_case(raw_title)
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
    Chicago (aligned with Google Scholar example for books):

    Bawumia, Mumuni. A life in the political history of Ghana: Memoirs of Alhaji Mumuni Bawumia. Ghana University Press, 2004.
    """
    authors = _format_authors_chicago(book.authors)
    year = book.year.strip() if book.year else "n.d."
    raw_title = book.title.strip() if book.title else "[No title]"
    title = _to_sentence_case(raw_title)
    publisher = book.publisher.strip() if book.publisher else ""

    pieces = []
    if authors:
        pieces.append(f"{authors}.")
    pieces.append(f"{title}.")
    if publisher or year:
        # "Publisher, Year." / "Publisher." / "Year."
        tail = ""
        if publisher and year:
            tail = f"{publisher}, {year}."
        elif publisher:
            tail = f"{publisher}."
        else:
            tail = f"{year}."
        pieces.append(tail)

    return " ".join(pieces)


def format_harvard(book: Book) -> str:
    """
    Harvard (approx Google Scholar):
    Bawumia, M., 2004. A life in the political history of Ghana: Memoirs of Alhaji Mumuni Bawumia. Ghana University Press.
    """
    authors = _format_authors_harvard(book.authors)
    year = book.year.strip() if book.year else "n.d."
    raw_title = book.title.strip() if book.title else "[No title]"
    title = _to_sentence_case(raw_title)
    publisher = book.publisher.strip() if book.publisher else ""

    pieces = []
    if authors:
        pieces.append(f"{authors},")
    pieces.append(f"{year}.")
    pieces.append(f"{title}.")
    if publisher:
        pieces.append(f"{publisher}.")

    return " ".join(pieces)


def format_vancouver(book: Book) -> str:
    """
    Vancouver (approx Google Scholar):
    Bawumia M. A life in the political history of Ghana: Memoirs of Alhaji Mumuni Bawumia. Ghana University Press; 2004.
    """
    authors = _format_authors_vancouver(book.authors)
    raw_title = book.title.strip() if book.title else "[No title]"
    # Vancouver typically uses sentence case for titles
    title = _to_sentence_case(raw_title)
    publisher = book.publisher.strip() if book.publisher else ""
    year = book.year.strip() if book.year else ""

    pieces = []
    if authors:
        pieces.append(f"{authors}.")
    pieces.append(f"{title}.")
    if publisher or year:
        tail = ""
        if publisher and year:
            tail = f"{publisher}; {year}."
        elif publisher:
            tail = f"{publisher}."
        else:
            tail = f"{year}."
        pieces.append(tail)

    return " ".join(pieces)


def format_bibtex(book: Book) -> str:
    """
    Build a simple BibTeX @book entry from a Book.

    Example:

    @book{Kahneman2011Thinking,
      author    = {Kahneman, Daniel},
      title     = {Thinking, fast and slow},
      year      = {2011},
      publisher = {Farrar, Straus and Giroux},
      address   = {London},
    }
    """
    key = _make_bibtex_key(book)
    author_field = _format_authors_bibtex(book.authors) if book.authors else ""
    title = book.title.strip() if book.title else "[No title]"
    year = book.year.strip() if book.year else ""
    publisher = book.publisher.strip() if book.publisher else ""
    address = book.place.strip() if book.place else ""

    lines = [f"@book{{{key},"]

    if author_field:
        lines.append(f"  author    = {{{author_field}}},")
    if title:
        lines.append(f"  title     = {{{title}}},")
    if year:
        lines.append(f"  year      = {{{year}}},")
    if publisher:
        lines.append(f"  publisher = {{{publisher}}},")
    if address:
        lines.append(f"  address   = {{{address}}},")

    lines.append("}")

    return "\n".join(lines)


def format_citation_html(book: Book, style: CitationStyle) -> str:
    """
    HTML version of the citation with <em> for book titles.
    Vancouver is kept without italics to match typical style.
    """
    # We'll reuse the same patterns but wrap the title in <em> for all styles except Vancouver.
    import html

    raw_title = book.title.strip() if book.title else "[No title]"
    # Use appropriate casing helpers
    if style == CitationStyle.mla:
        title_text = _to_title_case(raw_title)
    else:
        title_text = _to_sentence_case(raw_title)

    title_html = f"<em>{html.escape(title_text)}</em>"

    # Build for each style
    if style == CitationStyle.apa:
        authors = html.escape(_format_authors_apa(book.authors))
        year = html.escape(book.year.strip()) if book.year else "n.d."
        publisher = html.escape(book.publisher.strip()) if book.publisher else ""
        parts = [authors, f"({year}).", f"{title_html}.", publisher]
        return " ".join(p for p in parts if p)

    if style == CitationStyle.mla:
        authors = html.escape(_format_authors_mla(book.authors))
        publisher = html.escape(book.publisher.strip()) if book.publisher else ""
        year = html.escape(book.year.strip()) if book.year else ""
        pieces = []
        if authors:
            pieces.append(f"{authors}.")
        pieces.append(f"{title_html}.")
        if publisher:
            pieces.append(publisher + ",")
        if year:
            pieces.append(year + ".")
        return " ".join(pieces)

    if style == CitationStyle.chicago:
        authors = html.escape(_format_authors_chicago(book.authors))
        year = html.escape(book.year.strip()) if book.year else "n.d."
        publisher = html.escape(book.publisher.strip()) if book.publisher else ""
        pieces = []
        if authors:
            pieces.append(f"{authors}.")
        pieces.append(f"{title_html}.")
        if publisher or year:
            if publisher and year:
                tail = f"{publisher}, {year}."
            elif publisher:
                tail = f"{publisher}."
            else:
                tail = f"{year}."
            pieces.append(tail)
        return " ".join(pieces)

    if style == CitationStyle.harvard:
        authors = html.escape(_format_authors_harvard(book.authors))
        year = html.escape(book.year.strip()) if book.year else "n.d."
        publisher = html.escape(book.publisher.strip()) if book.publisher else ""
        pieces = []
        if authors:
            pieces.append(f"{authors},")
        pieces.append(f"{year}.")
        pieces.append(f"{title_html}.")
        if publisher:
            pieces.append(f"{publisher}.")
        return " ".join(pieces)

    if style == CitationStyle.vancouver:
        # No italics for Vancouver – plain title
        authors = html.escape(_format_authors_vancouver(book.authors))
        title = html.escape(_to_sentence_case(raw_title))
        publisher = html.escape(book.publisher.strip()) if book.publisher else ""
        year = html.escape(book.year.strip()) if book.year else ""
        pieces = []
        if authors:
            pieces.append(f"{authors}.")
        pieces.append(f"{title}.")
        if publisher or year:
            if publisher and year:
                tail = f"{publisher}; {year}."
            elif publisher:
                tail = f"{publisher}."
            else:
                tail = f"{year}."
            pieces.append(tail)
        return " ".join(pieces)

    # Fallback to plain text if something unexpected happens
    return html.escape(format_citation(book, style))