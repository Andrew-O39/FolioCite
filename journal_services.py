from typing import List, Dict, Tuple
import httpx


CROSSREF_BASE_URL = "https://api.crossref.org/works"


async def search_articles(query: str, limit: int = 10) -> Tuple[List[Dict], bool]:
    """
    Search Crossref for journal articles matching the query.
    Returns (results, had_error).
    Each result is a dict with keys:
      - title, authors (list[str]), year, journal, volume, issue, pages, doi
    """
    params = {
        "query": query,
        "filter": "type:journal-article",
        "rows": limit,
    }

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(CROSSREF_BASE_URL, params=params)
        resp.raise_for_status()
    except httpx.HTTPError:
        return [], True

    data = resp.json()
    items = data.get("message", {}).get("items", [])

    results: List[Dict] = []
    for item in items:
        title_list = item.get("title") or []
        title = title_list[0] if title_list else ""

        # authors
        authors_raw = item.get("author") or []
        authors = []
        for a in authors_raw:
            given = a.get("given") or ""
            family = a.get("family") or ""
            full = (given + " " + family).strip()
            if full:
                authors.append(full)

        # year
        year = None
        for key in ("published-print", "published-online", "issued"):
            part = item.get(key)
            if part and "date-parts" in part and part["date-parts"]:
                first = part["date-parts"][0]
                if first:
                    year = str(first[0])
                    break

        journal_list = item.get("container-title") or []
        journal = journal_list[0] if journal_list else ""

        volume = item.get("volume") or ""
        issue = item.get("issue") or ""
        pages = item.get("page") or ""
        doi = item.get("DOI") or ""

        results.append(
            {
                "entry_type": "article",
                "title": title,
                "authors": authors,
                "year": year,
                "journal": journal,
                "volume": volume,
                "issue": issue,
                "pages": pages,
                "doi": doi,
                # book-only fields left blank
                "publisher": "",
                "place": "",
                "cover_url": "",
            }
        )

    return results, False