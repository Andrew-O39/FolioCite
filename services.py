from typing import List, Tuple
import httpx
import re

from book_citation import Book

OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


def _extract_year_from_string(value: str) -> str | None:
    """
    Try to pull a 4-digit year out of strings like '2011', '2011-05-01', etc.
    """
    if not value:
        return None
    match = re.search(r"\d{4}", value)
    return match.group(0) if match else None


async def search_books_openlibrary(query: str, limit: int = 10) -> tuple[List[Book], bool]:
    """
    Primary search: Open Library Search API.

    Returns: (results, had_error)
      - results: list[Book]
      - had_error: True if the *API call itself* failed (network / 4xx/5xx), not just "no hits".
    """
    fields = [
        "title",
        "author_name",
        "first_publish_year",
        "publisher",
        "publish_place",
        "publish_places",
        "place",
        "cover_i",
        "editions",
        "editions.publisher",
        "editions.publish_place",
        "editions.publish_places",
        "editions.place",
    ]
    params = {
        "q": query,
        "limit": limit,
        "fields": ",".join(fields),
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(OPEN_LIBRARY_SEARCH_URL, params=params)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"Open Library request failed: {exc}")
        return [], True  # had_error=True

    data = response.json()
    results: List[Book] = []

    for doc in data.get("docs", []):
        title = doc.get("title")
        if not title:
            continue

        authors = doc.get("author_name") or []
        year = doc.get("first_publish_year")

        # ---------- Publisher (work level) ----------
        publisher_list = doc.get("publisher") or []

        # ---------- Place (work level) ----------
        place_list = None
        for key in ("publish_place", "publish_places", "place"):
            val = doc.get(key)
            if isinstance(val, list) and val:
                place_list = val
                break
            if isinstance(val, str) and val.strip():
                place_list = [val]
                break

        # ---------- Edition-level fallback for publisher/place ----------
        if (not publisher_list) or (not place_list):
            editions = doc.get("editions") or {}
            ed_docs = editions.get("docs") or []

            for ed in ed_docs:
                # Publisher
                if not publisher_list:
                    ed_pubs = ed.get("publisher") or ed.get("publishers") or []
                    if isinstance(ed_pubs, list) and ed_pubs:
                        publisher_list = ed_pubs
                    elif isinstance(ed_pubs, str) and ed_pubs.strip():
                        publisher_list = [ed_pubs]

                # Place
                if not place_list:
                    for key in ("publish_place", "publish_places", "place"):
                        val = ed.get(key)
                        if isinstance(val, list) and val:
                            place_list = val
                            break
                        if isinstance(val, str) and val.strip():
                            place_list = [val]
                            break

                if publisher_list and place_list:
                    break  # found enough

        publisher = publisher_list[0] if publisher_list else None
        place = place_list[0] if place_list else None

        # ---------- Cover image ----------
        cover_id = doc.get("cover_i")
        if cover_id:
            cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
        else:
            cover_url = None

        results.append(
            Book(
                title=title,
                authors=authors,
                year=str(year) if year else None,
                publisher=publisher,
                place=place,
                cover_url=cover_url,
            )
        )

    return results, False  # no HTTP error


async def search_books_google(query: str, limit: int = 10) -> tuple[List[Book], bool]:
    """
    Secondary search: Google Books API.

    Used as a fallback (or top-up) when Open Library returns few or no results.
    """
    params = {
        "q": query,
        "maxResults": min(limit, 40),
        # you *can* add an API key here later if needed:
        # "key": os.getenv("GOOGLE_BOOKS_API_KEY"),
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(GOOGLE_BOOKS_API_URL, params=params)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"Google Books request failed: {exc}")
        return [], True

    data = response.json()
    results: List[Book] = []

    for item in data.get("items", []):
        volume = item.get("volumeInfo") or {}
        title = volume.get("title")
        if not title:
            continue

        authors = volume.get("authors") or []
        published_date = volume.get("publishedDate") or ""
        year = _extract_year_from_string(published_date)
        publisher = volume.get("publisher")

        # Google Books usually doesn't give a clean "place"; we leave it empty
        place = None

        # Cover image (if any)
        cover_url = None
        image_links = volume.get("imageLinks") or {}
        thumb = image_links.get("thumbnail") or image_links.get("smallThumbnail")
        if thumb:
            cover_url = thumb

        results.append(
            Book(
                title=title,
                authors=authors,
                year=year,
                publisher=publisher,
                place=place,
                cover_url=cover_url,
            )
        )

        if len(results) >= limit:
            break

    return results, False


async def search_books(query: str, limit: int = 10) -> tuple[List[Book], bool]:
    """
    Enhanced book search:
      1) Try Open Library
      2) If we get fewer than `limit` results, top up from Google Books
    """
    # 1) Primary: Open Library
    ol_results, ol_error = await search_books_openlibrary(query, limit=limit)

    results = list(ol_results)

    # If we already have enough results (and the API didn't explode), we’re done.
    if len(results) >= limit and not ol_error:
        return results[:limit], ol_error

    # 2) Fallback / top-up: Google Books
    remaining = max(0, limit - len(results))
    if remaining > 0:
        gb_results, gb_error = await search_books_google(query, limit=remaining)
        results.extend(gb_results)
        # overall error only if *both* backends failed
        had_error = ol_error and gb_error
    else:
        had_error = ol_error

    return results[:limit], had_error