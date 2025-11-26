# journal_services.py

from typing import List, Tuple
import httpx

from journal_citation import Article, CitationStyle  # Article is mainly for type clarity

CROSSREF_WORKS_URL = "https://api.crossref.org/works"


def _extract_year(item: dict) -> str | None:
    """
    Try to pull a reasonable publication year from a Crossref work object.
    """
    for key in ("published-print", "published-online", "issued"):
        data = item.get(key)
        if not data:
            continue
        parts = data.get("date-parts")
        if isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]:
            year = parts[0][0]
            return str(year)
    return None


def _extract_authors(item: dict) -> List[str]:
    """
    Build a list of 'Family, Given' strings from Crossref's author array.
    """
    authors_raw = item.get("author") or []
    authors: List[str] = []

    for a in authors_raw:
        given = (a.get("given") or "").strip()
        family = (a.get("family") or "").strip()
        if family and given:
            authors.append(f"{family}, {given}")
        elif family:
            authors.append(family)
        elif given:
            authors.append(given)

    return authors


async def _fetch_crossref_items(url: str, params: dict | None = None) -> Tuple[List[dict], bool]:
    """
    Generic helper to call Crossref and return a list of 'work' dicts plus an error flag.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)

        resp.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"Crossref request failed: {exc}")
        return [], True

    data = resp.json() or {}
    message = data.get("message") or {}

    # /works/{doi} returns a single object in "message"
    if isinstance(message, dict) and "items" not in message:
        return [message], False

    # /works?query=... returns "items"
    items = message.get("items") or []
    return items, False


async def search_articles(query: str, limit: int = 10) -> Tuple[List[dict], bool]:
    """
    Search for journal articles using Crossref.

    Returns:
      - a list of *unified* dicts which results.html expects:
        {
          "entry_type": "article",
          "title": ...,
          "authors": [...],
          "year": ...,
          "journal": ...,
          "volume": ...,
          "issue": ...,
          "pages": ...,
          "doi": ...,
          "publisher": "",
          "place": "",
          "cover_url": "",
        }
      - had_error: bool indicating network/HTTP issues.
    """

    # --- Strategy 1: treat query as DOI if it looks like one ---
    # Very rough heuristic: starts with "10." and has a slash, and no spaces.
    query_stripped = query.strip()
    looks_like_doi = query_stripped.startswith("10.") and ("/" in query_stripped) and (" " not in query_stripped)

    items: List[dict] = []
    had_error = False

    if looks_like_doi:
        # Try DOI lookup first
        doi_url = f"{CROSSREF_WORKS_URL}/{query_stripped}"
        items, had_error = await _fetch_crossref_items(doi_url)
        # If DOI lookup failed (e.g., 404), fall back to a normal query search
        if had_error or not items:
            had_error = False  # we’ll try again with normal search
            items = []

    # --- Strategy 2: normal title/keyword search ---
    if not items:
        params = {
            "query": query,
            "filter": "type:journal-article",
            "rows": limit,
        }
        items, had_error = await _fetch_crossref_items(CROSSREF_WORKS_URL, params=params)

    if had_error:
        return [], True

    results: List[dict] = []

    for item in items[:limit]:
        title_list = item.get("title") or []
        title = title_list[0] if title_list else None
        if not title:
            continue

        authors = _extract_authors(item)
        year = _extract_year(item)

        container_titles = item.get("container-title") or []
        journal = container_titles[0] if container_titles else None

        volume = item.get("volume")
        issue = item.get("issue") or item.get("journal-issue", {}).get("issue")
        pages = item.get("page")
        doi = item.get("DOI")

        results.append(
            {
                "entry_type": "article",
                "title": title,
                "authors": authors,
                "year": year,
                "publisher": "",   # not used for articles, but included for template symmetry
                "place": "",
                "journal": journal or "",
                "volume": volume or "",
                "issue": issue or "",
                "pages": pages or "",
                "doi": doi or "",
                "cover_url": "",
            }
        )

    return results, False