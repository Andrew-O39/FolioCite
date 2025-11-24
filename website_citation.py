
from dataclasses import dataclass
from typing import List, Optional

from book_citation import CitationStyle  # same enum we already use
from journal_citation import _format_authors_plain  # reuse helpers


@dataclass
class Website:
    title: str
    authors: List[str]
    year: Optional[str] = None
    site_name: Optional[str] = None
    url: str = ""
    accessed: Optional[str] = None  # free-text access date, e.g. "24 Nov 2025"


def _safe(value: Optional[str]) -> str:
    return value.strip() if value else ""


def _format_year(year: Optional[str]) -> str:
    y = (year or "").strip()
    return y if y else "n.d."


# ---------- Plain-text citation ----------

def format_website_citation(website: Website, style: CitationStyle) -> str:
    """
    Format a website citation for the given style.
    Handles missing URL / accessed date safely.
    """
    authors_txt = _format_authors_plain(website.authors, style)
    title = (website.title or "").strip()
    site_name = _safe(website.site_name)
    url = (website.url or "").strip()
    accessed = (website.accessed or "").strip()
    year_txt = _format_year(website.year)

    # --- APA 7 ---
    # Author, A. A. (Year). Title of page. Site Name. URL
    if style is CitationStyle.apa:
        parts = []
        if authors_txt:
            parts.append(f"{authors_txt} ({year_txt}).")
        else:
            parts.append(f"({year_txt}).")
        if title:
            parts.append(f"{title}.")
        if site_name:
            parts.append(f"{site_name}.")
        if url:
            parts.append(url)
        return " ".join(p for p in parts if p)

    # --- MLA 9 ---
    # "Title of Web Page." Website Name, Day Month Year, URL.
    if style is CitationStyle.mla:
        parts = []
        if authors_txt:
            parts.append(f"{authors_txt}.")
        if title:
            parts.append(f"\"{title}.\"")
        if site_name:
            parts.append(f"{site_name},")
        if year_txt:
            parts.append(f"{year_txt},")
        if url:
            parts.append(f"{url}.")
        return " ".join(p for p in parts if p)

    # --- Chicago (author-date) ---
    # Author, Firstname. Year. "Title of Page." Website Name. URL (accessed ...).
    if style is CitationStyle.chicago:
        parts = []
        if authors_txt:
            parts.append(f"{authors_txt}.")
        if year_txt:
            parts.append(f"{year_txt}.")
        if title:
            parts.append(f"\"{title}.\"")
        if site_name:
            parts.append(f"{site_name}.")
        if url:
            parts.append(url + ".")
        if accessed:
            parts.append(f"(accessed {accessed}).")
        return " ".join(p for p in parts if p)

    # --- Harvard ---
    # Author, A., Year. Title of page. Website Name. Available at: URL (Accessed: ...).
    if style is CitationStyle.harvard:
        parts = []
        if authors_txt:
            parts.append(f"{authors_txt},")
        if year_txt:
            parts.append(f"{year_txt}.")
        if title:
            parts.append(f"{title}.")
        if site_name:
            parts.append(f"{site_name}.")
        if url:
            at_part = f"Available at: {url}"
            if accessed:
                at_part += f" (Accessed: {accessed})."
            else:
                at_part += "."
            parts.append(at_part)
        return " ".join(p for p in parts if p)

    # --- Vancouver ---
    # Author AA. Title of page. Website Name. Year. Available from: URL.
    if style is CitationStyle.vancouver:
        parts = []
        if authors_txt:
            parts.append(f"{authors_txt}.")
        if title:
            parts.append(f"{title}.")
        if site_name:
            parts.append(f"{site_name}.")
        if year_txt:
            parts.append(f"{year_txt}.")
        if url:
            parts.append(f"Available from: {url}.")
        return " ".join(p for p in parts if p)

    # --- Fallback ---
    base = f"{authors_txt} ({year_txt}). {title}"
    if site_name:
        base += f". {site_name}"
    if url:
        base += f". {url}"
    base += "."
    return base

# ---------- HTML version (italicise site name) ----------

def format_website_citation_html(website: Website, style: CitationStyle) -> str:
    """
    Same as plain text, but italics for site name where appropriate.
    We keep it simple and mostly mirror format_website_citation.
    """
    base = format_website_citation(website, style)
    site = _safe(website.site_name)
    if not site:
        return base
    # naive, but OK: replace first occurrence of site name with <em>site</em>
    return base.replace(site, f"<em>{site}</em>", 1)


# ---------- BibTeX ----------

def format_website_bibtex(website: Website) -> str:
    """
    Minimal @online BibTeX entry.
    """
    authors_str = " and ".join(website.authors) if website.authors else ""
    year_txt = _format_year(website.year)
    key = "website:" + (website.authors[0].split(" ")[-1].lower() if website.authors else "anon")
    key += f":{year_txt}"

    lines = [
        f"@online{{{key},",
        f"  title = {{{website.title}}},",
    ]
    if authors_str:
        lines.append(f"  author = {{{authors_str}}},")
    if website.site_name:
        lines.append(f"  organization = {{{website.site_name}}},")
    if website.year:
        lines.append(f"  year = {{{website.year}}},")
    if website.url:
        lines.append(f"  url = {{{website.url}}},")
    if website.accessed:
        lines.append(f"  note = {{{{Accessed: {website.accessed}}}}},")
    lines.append("}")
    return "\n".join(lines)