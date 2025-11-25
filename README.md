# 📚 FolioCite

**FolioCite** is a clean, multi-source citation generator built with **FastAPI** 

It supports **books, journal articles _and_ websites**,
generating citations in all major styles through a simple and elegant web interface.

It also supports **user accounts**, **saved bibliographies**, **BibTeX export**, **copy-all**, and more.

---

## 🚀 Features

### 🔍 Source Search & Import
- Search for **Books** via the **Open Library API**
- Search for **Journal Articles** via **Crossref API**
- Unified search UX for Books and Journals
- Search by title, author, ISBN, DOI, or keywords
- Manual entry mode for 
- - books, 
- - journals & 
- - websites 

### ✍️ Citation Generation
- Styles supported:
  - APA (7th)
  - MLA (9th)
  - Chicago (author–date)
  - Harvard
  - Vancouver

### 📄 Output Formats
- Plain text citation
- Rich HTML-styled citation (with italics / formatting), 
- **BibTeX export**
- **Bibliography export** as:
    - .txt
	- .bib

- 

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
- Responsive and simple design powered by Jinja2 templates
- One-click “Copy to clipboard”

---

## 🗂️ Project Structure

```text
FolioCiteApp/
│
├── main.py                     # FastAPI app & routes
├── book_citation.py            # Book model & formatting logic
├── journal_citation.py         # Article model & formatting logic
├── website_citation.py         # Website model & citation logic
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
If you don't want to search for books or articles, you could as well visit the manual entry page 
and enter book/article/or website post details and generate citation for the said book, article or website.

---

## ✨ Notes & limitations

- Metadata quality for books comes from **Open Library** 
- Metadata for journal articles comes from **Crossref(articles)** which may have varying author formatting. 
- Some sources may have missing or incomplete fields
  (years, publishers, pages or author lists) from the APIs, so it is important to verify entries before using them.
- Citation formatting is intentionally **simplified** but covers all required major style rules and are accurate for standard academic use.
  Nevertheless, always double-check for strict institutional requirements.
- This is a starter project and a great base to extend with more features.

---

## 🌱 Ideas for future improvements

- Website search via structured metadata (if reliable sources become available)
- Support for
- - Book chapter citations
- - Thesis & dissertation formats
- - Conference papers
- - Report and grey literature
- Export Options:
- - RIS export
- - EndNote XML
- Browser extension or auto-capturing of website citation metadata
- Email export / Share bibliography
- Multi-language UI (EN, DE, FR…)
- Collaborative bibliographies

---

## 💡 About the name

**FolioCite** combines:

- **Folio** – pages, books, and manuscripts
- **Cite** – the act of referencing sources

It reflects the app’s focus and mission: helping students, researchers and
writers generate clean, accurate citations with ease.

Enjoy experimenting and extending FolioCite!
