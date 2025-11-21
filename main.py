from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware

from citation import format_citation, CitationStyle, Book, format_bibtex, format_citation_html
from services import search_books
import db
from typing import List, Dict, Any, Optional

from passlib.hash import pbkdf2_sha256
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env into environment

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    # Fallback / safety: you can either raise or use a default for dev
    raise RuntimeError("SECRET_KEY is not set. Please define it in your .env file.")

app = FastAPI(title="FolioCite – Book Citation Generator")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


# Mount static files (CSS, logo, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

db.init_db()

class CurrentUser:
    def __init__(self, user_id: int, username: str, email: str):
        self.id = user_id
        self.username = username
        self.email = email


def get_current_user(request: Request) -> Optional[CurrentUser]:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    row = db.get_user_by_id(int(user_id))
    if not row:
        return None
    row = db.get_user_by_id(int(user_id))
    return CurrentUser(
        user_id=row["id"],
        username=row["username"],
        email=row["email"],
    )

@app.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    current_user = get_current_user(request)
    if current_user:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        "register.html",
        {"request": request, "error": None, "current_user": current_user},
    )


@app.post("/register", response_class=HTMLResponse)
async def register_post(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    # Normalize inputs
    username = username.strip()
    email = email.strip().lower()

    def render_with_error(message: str):
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": message,
                "current_user": None,
                "username": username,
                "email": email,
            },
        )

    if password != confirm_password:
        return render_with_error("Passwords do not match.")

    if db.get_user_by_username(username):
        return render_with_error("Username is already taken.")

    if db.get_user_by_email(email):
        return render_with_error("An account with this email already exists.")

    password_hash = pbkdf2_sha256.hash(password)
    db.create_user(username, email, password_hash)

    # Do NOT log the user in here.
    # Send them to the login page instead.
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    current_user = get_current_user(request)
    if current_user:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": None, "current_user": current_user},
    )


@app.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    username = username.strip()

    def render_with_error(message: str):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": message,
                "current_user": None,
                "username": username,  # so the form can re-fill it
            },
        )

    # Look up user by username
    row = db.get_user_by_username(username)
    if not row or not pbkdf2_sha256.verify(password, row["password_hash"]):
        return render_with_error("Invalid username or password.")

    # Success: store user_id in session
    request.session["user_id"] = row["id"]
    return RedirectResponse(url="/", status_code=303)


@app.post("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "error": None,
            "selected_style": "apa",
            "current_user": current_user,
        },
    )

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request, query: str = Form(...), style: str = Form(...)):
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    books, had_error = await search_books(query)

    if had_error:
        # API / server problem
        error_message = (
            "We couldn't reach the book database (Open Library) just now. "
            "This is a temporary problem on their side. Please try again in a few minutes."
        )
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "results": None,
                "error": error_message,
                "selected_style": style,
                "current_user": current_user,
            },
        )

    if not books:
        # No error, but no matches
        error_message = (
            f"No books found for '{query}'. Please check the spelling or try "
            "a different search (e.g. author name or ISBN)."
        )
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "results": None,
                "error": error_message,
                "selected_style": style,
                "current_user": current_user,
            },
        )

    # All good: show results
    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "results": books,
            "style": style,
            "query": query,
            "current_user": current_user,
        },
    )

@app.post("/confirm", response_class=HTMLResponse)
async def confirm(
    request: Request,
    title: str = Form(...),
    authors: str = Form(...),
    year: str = Form(None),
    publisher: str = Form(None),
    place: str = Form(None),
    style: str = Form(...),
    cover_url: str = Form(None),
):
    """
    Show a confirmation/edit page where the user can adjust metadata
    before generating a citation.
    """
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        "confirm.html",
        {
            "request": request,
            "title": title,
            "authors": authors,
            "year": year or "",
            "publisher": publisher or "",
            "place": place or "",
            "style": style,
            "cover_url": cover_url or "",
            "current_user": current_user,
        },
    )


@app.get("/manual", response_class=HTMLResponse)
async def manual_entry(request: Request):
    """
    Show a blank form for manually entering book details (no Open Library).
    """
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        "manual.html",
        {
            "request": request,
            "selected_style": "apa",
            "current_user": current_user,
        },
    )

@app.post("/cite", response_class=HTMLResponse)
async def cite(
    request: Request,
    title: str = Form(...),
    authors: str = Form(...),
    year: str = Form(None),
    publisher: str = Form(None),
    place: str = Form(None),
    style: str = Form(...),
    cover_url: str = Form(None),
):
    """
    Generate a formatted citation for the selected book.
    """
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    authors_list = [a.strip() for a in authors.split(";") if a.strip()]
    book = Book(
        title=title,
        authors=authors_list,
        year=year or None,
        publisher=publisher or None,
        place=place or None,
        cover_url=cover_url or None,
    )

    citation = format_citation(book, CitationStyle(style))
    citation_html = format_citation_html(book, CitationStyle(style))
    bibtex = format_bibtex(book)

    return templates.TemplateResponse(
        "citation.html",
        {
            "request": request,
            "citation": citation,           # plain text (for textarea/copy)
            "citation_html": citation_html, # HTML with <em> for titles
            "bibtex": bibtex,               # BibTeX block
            "style": style,
            "book": book,
            "current_user": current_user,
        },
    )

@app.get("/bibliography", response_class=HTMLResponse)
async def show_bibliography(
    request: Request,
    style: str = Query("apa"),
):
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    rows = db.get_all_entries(current_user.id)

    try:
        chosen_style = CitationStyle(style)
    except ValueError:
        chosen_style = CitationStyle.apa
        style = "apa"

    entries = []
    for row in rows:
        authors_list = [a.strip() for a in (row["authors"] or "").split(";") if a.strip()]
        book = Book(
            title=row["title"],
            authors=authors_list,
            year=row["year"],
            publisher=row["publisher"],
            place=row["place"],
            cover_url=row["cover_url"],
        )
        citation = format_citation(book, chosen_style)
        entries.append({"id": row["id"], "citation": citation})

    entries_sorted = sorted(entries, key=lambda e: e["citation"].lower())

    return templates.TemplateResponse(
        "bibliography.html",
        {
            "request": request,
            "entries": entries_sorted,
            "current_style": style,
            "current_user": current_user,
        },
    )


@app.post("/bibliography/add", response_class=HTMLResponse)
async def add_to_bibliography(
    request: Request,
    title: str = Form(...),
    authors: str = Form(...),
    year: str = Form(None),
    publisher: str = Form(None),
    place: str = Form(None),
    style: str = Form(...),
    cover_url: str = Form(None),
):
    """
    Add a book to the persistent bibliography (SQLite).
    """
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    authors_str = ";".join([a.strip() for a in authors.split(";") if a.strip()])

    db.add_entry(
        current_user.id,
        {
            "title": title.strip(),
            "authors": authors_str,
            "year": (year or "").strip() or None,
            "publisher": (publisher or "").strip() or None,
            "place": (place or "").strip() or None,
            "style": style,
            "cover_url": (cover_url or "").strip() or None,
        },
    )

    return RedirectResponse(url="/bibliography", status_code=303)


@app.post("/bibliography/clear", response_class=HTMLResponse)
async def clear_bibliography(request: Request):
    """
    Remove all entries from the current user's bibliography.
    """
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    db.clear_entries(current_user.id)
    return RedirectResponse(url="/bibliography", status_code=303)


@app.post("/bibliography/delete", response_class=HTMLResponse)
async def delete_from_bibliography(
    request: Request,
    entry_id: int = Form(...),
):
    """
    Delete a single entry from the current user's bibliography by its ID.
    """
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    db.delete_entry(current_user.id, entry_id)
    return RedirectResponse(url="/bibliography", status_code=303)


@app.get("/bibliography/export.txt")
async def export_bibliography_txt(
    request: Request,
    style: str = Query("apa"),
):
    """
    Export all citations as a plain-text .txt file, one per line, in the chosen style.
    """
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    rows = db.get_all_entries(current_user.id)

    try:
        chosen_style = CitationStyle(style)
    except ValueError:
        chosen_style = CitationStyle.apa
        style = "apa"

    citations = []
    for row in rows:
        authors_list = [a.strip() for a in (row["authors"] or "").split(";") if a.strip()]
        book = Book(
            title=row["title"],
            authors=authors_list,
            year=row["year"],
            publisher=row["publisher"],
            place=row["place"],
            cover_url=row["cover_url"],
        )
        citations.append(format_citation(book, chosen_style))

    citations_sorted = sorted(citations, key=lambda c: c.lower())
    text = "\n".join(citations_sorted)

    return PlainTextResponse(
        text,
        media_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename=\"bibliography_{style}.txt\"'},
    )


@app.get("/bibliography/export.bib")
async def export_bibliography_bib(
    request: Request,
    style: str = Query("apa"),
):
    """
    Export all entries as a .bib file (BibTeX), in alphabetical order.
    """
    current_user = get_current_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    rows = db.get_all_entries(current_user.id)

    bib_entries = []
    for row in rows:
        authors_list = [a.strip() for a in (row["authors"] or "").split(";") if a.strip()]
        book = Book(
            title=row["title"],
            authors=authors_list,
            year=row["year"],
            publisher=row["publisher"],
            place=row["place"],
            cover_url=row["cover_url"],
        )
        bib_entries.append(format_bibtex(book))

    text = "\n\n".join(bib_entries)

    return PlainTextResponse(
        text,
        media_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename=\"bibliography_{style}.bib\"'},
    )

# For local debugging: `python main.py`
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
