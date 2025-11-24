from dataclasses import dataclass
from typing import List, Optional

from book_citation import CitationStyle


@dataclass
class Article:
    title: str
    authors: List[str]
    year: Optional[str] = None
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None


# --------- helpers ---------

def _format_authors_plain(authors: List[str], style: CitationStyle) -> str:
    """
    Very simple author formatting helper.
    We reuse the 'Surname, Initials' style for most.
    """
    if not authors:
        return ""

    def split_name(a: str):
        parts = a.split()
        if len(parts) == 1:
            return parts[0], ""
        return parts[-1], " ".join(parts[:-1])

    formatted = []
    for a in authors:
        last, firsts = split_name(a)
        initials = "".join(part[0].upper() + "." for part in firsts.split() if part)
        if initials:
            formatted.append(f"{last}, {initials}")
        else:
            formatted.append(last)

    if style in {CitationStyle.apa, CitationStyle.harvard, CitationStyle.chicago}:
        if len(formatted) == 1:
            return formatted[0]
        if len(formatted) == 2:
            return " & ".join(formatted)
        return ", ".join(formatted[:-1]) + ", & " + formatted[-1]

    # MLA, Vancouver – simpler
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return " and ".join(authors)
    return ", ".join(authors[:-1]) + ", and " + authors[-1]


def _safe(s: Optional[str]) -> str:
    return s or ""


def _format_year(year: Optional[str]) -> str:
    return year or "n.d."


# --------- plain-text citation ---------

def format_article_citation(article: Article, style: CitationStyle) -> str:
    authors_txt = _format_authors_plain(article.authors, style)
    year_txt = _format_year(article.year)
    title = article.title.strip()
    journal = _safe(article.journal)
    volume = _safe(article.volume)
    issue = _safe(article.issue)
    pages = _safe(article.pages)
    doi = article.doi.strip() if article.doi else ""
    has_authors = bool(article.authors)

    # APA 7: Author, A. A., & Author, B. B. (Year). Title of article. Journal Title, volume(issue), pages. https://doi.org/...
    if style is CitationStyle.apa:
        parts = []
        if authors_txt:
            parts.append(f"{authors_txt} ({year_txt}).")
        else:
            parts.append(f"({year_txt}).")
        parts.append(f"{title}.")
        if journal:
            vol_issue = volume
            if issue:
                vol_issue += f"({issue})"
            if vol_issue:
                parts.append(f"{journal}, {vol_issue}")
            else:
                parts.append(f"{journal}")
            if pages:
                parts[-1] += f", {pages}."
            else:
                parts[-1] += "."
        if doi:
            parts.append(f"https://doi.org/{doi}")
        return " ".join(p for p in parts if p)

    # MLA 9: Surname, Firstname, and Second Author. "Title of Article." Journal Title, vol. X, no. Y, Year, pp. Z.
    if style is CitationStyle.mla:
        parts = []

        if article.authors:
            # crude but readable: first author as-is, then and/et al.
            parts.append(article.authors[0])
            if len(article.authors) == 2:
                parts.append(f"and {article.authors[1]}.")
            elif len(article.authors) > 2:
                parts.append("et al.")

        if title:
            parts.append(f"\"{title}.\"")
        if journal:
            parts.append(f"{journal},")
        if volume:
            parts.append(f"vol. {volume},")
        if issue:
            parts.append(f"no. {issue},")
        parts.append(f"{year_txt},")
        if pages:
            parts.append(f"pp. {pages}.")
        return " ".join(p for p in parts if p)

    # Chicago (author-date): Author, Firstname Lastname. Year. "Title of Article." Journal Title volume, no. issue: pages.
    if style is CitationStyle.chicago:
        parts = []

        if article.authors:
            # first author only + possible "et al."
            first = article.authors[0].rstrip(".")
            if len(article.authors) > 1:
                parts.append(f"{first} et al.")
            else:
                parts.append(f"{first}.")
        parts.append(f"{year_txt}.")
        if title:
            parts.append(f"\"{title}.\"")
        if journal:
            j_part = journal
            if volume:
                j_part += f" {volume}"
            if issue:
                j_part += f", no. {issue}"
            if pages:
                j_part += f": {pages}."
            else:
                j_part += "."
            parts.append(j_part)
        return " ".join(p for p in parts if p)

    # Harvard: Author, A., Year. Title of article. Journal Title, volume(issue), pages.
    if style is CitationStyle.harvard:
        parts = []
        if authors_txt:
            parts.append(f"{authors_txt},")
        parts.append(f"{year_txt}.")
        if title:
            parts.append(f"{title}.")
        if journal:
            vol_issue = volume
            if issue:
                vol_issue += f"({issue})"
            j_part = journal
            if vol_issue:
                j_part += f", {vol_issue}"
            if pages:
                j_part += f", {pages}."
            else:
                j_part += "."
            parts.append(j_part)
        return " ".join(p for p in parts if p)

    # Vancouver: Author AA, Author BB. Title of article. Journal Title. Year;volume(issue):pages.
    if style is CitationStyle.vancouver:
        author_van = "; ".join(article.authors) if article.authors else ""
        parts = []
        if author_van:
            parts.append(f"{author_van}.")
        if title:
            parts.append(f"{title}.")
        if journal:
            j_part = f"{journal}."
            parts.append(j_part)
        y_part = year_txt
        if volume:
            y_part += f";{volume}"
            if issue:
                y_part += f"({issue})"
        if pages:
            y_part += f":{pages}"
        y_part += "."
        parts.append(y_part)
        return " ".join(p for p in parts if p)

    # fallback
    return f"{authors_txt} ({year_txt}). {title}. {journal}."


# --------- HTML citation (with italics) ---------

def format_article_citation_html(article: Article, style: CitationStyle) -> str:
    """
    Same content as plain, but journal name in <em>...</em>.
    We'll reuse the plain logic and just replace journal with <em>journal</em>.
    """
    plain = format_article_citation(article, style)
    if not article.journal:
        return plain
    return plain.replace(article.journal, f"<em>{article.journal}</em>", 1)


# --------- BibTeX ---------

def format_article_bibtex(article: Article) -> str:
    # Simple key: first author surname + year + "a"
    key = "article"
    if article.authors:
        first = article.authors[0].split()[-1].lower()
        year = article.year or "n.d."
        key = f"{first}{year}"

    authors_bib = " and ".join(article.authors)

    fields = [
        f"  author = {{{authors_bib}}}",
        f"  title = {{{article.title}}}",
    ]
    if article.journal:
        fields.append(f"  journal = {{{article.journal}}}")
    if article.year:
        fields.append(f"  year = {{{article.year}}}")
    if article.volume:
        fields.append(f"  volume = {{{article.volume}}}")
    if article.issue:
        fields.append(f"  number = {{{article.issue}}}")
    if article.pages:
        fields.append(f"  pages = {{{article.pages}}}")
    if article.doi:
        fields.append(f"  doi = {{{article.doi}}}")

    inner = ",\n".join(fields)
    return f"@article{{{key},\n{inner}\n}}"