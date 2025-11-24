# 📚 FolioCite

**FolioCite** is a clean, citation generator built with **FastAPI** — now supporting **books _and_ journal articles**.

It lets you search for sources (via **Open Library** for books and **Crossref** for articles), manually enter metadata, and generate formatted citations in:

- **APA (7th)**
- **MLA (9th)**
- **Chicago (Author–Date)**
- **Harvard**
- **Vancouver**

It also supports **user accounts**, **saved bibliographies**, **BibTeX export**, **copy-all**, and more.

---

## 🚀 Features

### 🔍 Source Search
- **Books** (Open Library API)
- **Journal Articles** (Crossref API)
- Unified search UX
- Search by title, author, ISBN, DOI, or keywords
- Manual entry mode for books & journals

### ✍️ Citation Generation
- Styles supported:
  - APA (7th)
  - MLA (9th)
  - Chicago (author–date)
  - Harvard
  - Vancouver
- Plain text, rich HTML (with italics), and **BibTeX** output

### 📘 Manual Entry
- Books
- Journal articles  
(Both with fully editable metadata)

### 💾 My Bibliography
- Save unlimited citations to your account (SQLite-backed)
- Auto-sorted alphabetically
- Filter by **Books / Articles / All**
- Export:
  - `.txt`
  - `.bib`
- Delete individual entries
- Clear entire bibliography
- One-click action:
  - `Copy citation (plain text)`
  - `Copy formatted HTML version`
  - `Copy BipTex`

### 👤 User Accounts
- Register / Login / Logout
- Each user has their own saved bibliography

### 🎨 Clean UI
- Responsive layout
- Dark header + modern aesthetic
- Clear forms and structured results

---

## 🗂️ Project Structure

```text
FolioCiteApp/
│
├── main.py                     # FastAPI app & routes
├── book_citation.py            # Book model & formatting logic
├── journal_citation.py         # Article model & formatting logic
├── services.py                 # External API integrations
├── db.py                       # SQLite user + bibliography storage
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   ├── confirm.html
│   ├── citation.html
│   ├── manual.html
│   └── bibliography.html
│
├── static/
│   ├── styles.css
│   └── logo.svg
│
├── docs/
│   └── user_guide.md
│
├── requirements.txt
├── env.local
├── .env
└── README.md

```

## ⚙️ Installation

1. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   ```

   Activate it:

   - **Windows (PowerShell)**

     ```bash
     .venv\Scripts\activate
     ```

   - **macOS / Linux**

     ```bash
     source .venv/bin/activate
     ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Running the app

From the project folder (where `main.py` lives), run:

```bash
uvicorn main:app --reload
```

Then open your browser and go to:

```text
http://127.0.0.1:8000/
```

You will see the FolioCite home page. Enter a book or article title, author, or ISBN,
choose a style, and follow the steps to get your formatted citation.

---

## ✨ Notes & limitations

- Metadata quality depends on **Open Library** and **Crossref(articles)**. Some sources may have missing or incomplete fields
  (years, publishers, pages or author lists)
- Citation formatting is intentionally **simplified** though accurate for standard academic use.
  Always double-check for strict institutional requirements.
- This is a starter project and a great base to extend with more features.

---

## 🌱 Ideas for future improvements

- Website citations
- Journal articles
- Book chapter citations
- Thesis & dissertation formats
- RIS export
- Browser extension
- Email export / Share bibliography
- Multi-language UI (EN, DE, FR…)
- Collaborative bibliographies

---

## 💡 About the name

**FolioCite** combines:

- **Folio** – pages, books, and manuscripts
- **Cite** – the act of referencing sources

It reflects the app’s focus on helping students and researchers quickly turn
books and articles into clean citations.

Enjoy experimenting and extending FolioCite!
