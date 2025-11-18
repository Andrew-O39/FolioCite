
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from citation import format_citation, CitationStyle, Book
from services import search_books

app = FastAPI(title="FolioCite – Book Citation Generator")

# Mount static files (CSS, logo, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the main search page.
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": None,
            "error": None,
            "selected_style": "apa",
        },
    )


@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...), style: str = Form(...)):
    """
    Search for books using the Open Library API and show results to pick from.
    """
    books = await search_books(query)
    if not books:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "results": None,
                "error": f"No results found for '{query}'. Please try another search.",
                "selected_style": style,
            },
        )

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "results": books,
            "style": style,
            "query": query,
        },
    )

@app.post("/confirm", response_class=HTMLResponse)
async def confirm(
    request: Request,
    title: str = Form(...),
    authors: str = Form(...),
    year: str = Form(None),
    publisher: str = Form(None),
    style: str = Form(...),
):
    """
    Show a confirmation/edit page where the user can adjust metadata
    before generating a citation.
    """
    return templates.TemplateResponse(
        "confirm.html",
        {
            "request": request,
            "title": title,
            "authors": authors,
            "year": year or "",
            "publisher": publisher or "",
            "style": style,
        },
    )

@app.post("/cite", response_class=HTMLResponse)
async def cite(
    request: Request,
    title: str = Form(...),
    authors: str = Form(...),
    year: str = Form(None),
    publisher: str = Form(None),
    style: str = Form(...),
):
    """
    Generate a formatted citation for the selected book.
    """
    authors_list = [a.strip() for a in authors.split(";") if a.strip()]
    book = Book(
        title=title,
        authors=authors_list,
        year=year or None,
        publisher=publisher or None,
    )

    citation = format_citation(book, CitationStyle(style))

    return templates.TemplateResponse(
        "citation.html",
        {
            "request": request,
            "citation": citation,
            "style": style,
            "book": book,
        },
    )


# For local debugging: `python main.py`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
