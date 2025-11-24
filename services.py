from typing import List
import httpx

from book_citation import Book

OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"


async def search_books(query: str, limit: int = 5) -> tuple[List[Book], bool]:
    """
    Search for books via the Open Library Search API and return:
      - a list of Book objects
      - a boolean flag indicating whether a service/API error occurred

    If had_error is True, the caller should assume something went wrong
    with the API (network error, 5xx, etc.), not just "no results".
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

        # This will raise for 4xx/5xx responses
        response.raise_for_status()
    except httpx.HTTPError as exc:
        # Log to console for debugging
        print(f"Open Library request failed: {exc}")
        # No results, and indicate that an error happened
        return [], True

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
                    break  # we found enough

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

    # No HTTP error, so had_error is False
    return results, False