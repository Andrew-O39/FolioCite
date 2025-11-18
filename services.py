
from typing import List
import httpx

from citation import Book

OPEN_LIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"


async def search_books(query: str, limit: int = 5) -> List[Book]:
    """
    Search for books via the Open Library Search API and return a list of Book objects.
    """
    params = {"q": query, "limit": limit}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(OPEN_LIBRARY_SEARCH_URL, params=params)

    response.raise_for_status()
    data = response.json()

    results: List[Book] = []
    for doc in data.get("docs", []):
        title = doc.get("title")
        if not title:
            continue

        authors = doc.get("author_name") or []
        year = doc.get("first_publish_year")
        publisher_list = doc.get("publisher") or []
        publisher = publisher_list[0] if publisher_list else None

        results.append(
            Book(
                title=title,
                authors=authors,
                year=str(year) if year else None,
                publisher=publisher,
            )
        )

    return results
