# 📚 FolioCite

**FolioCite** is a full-featured, multi-source citation manager built with **FastAPI**.  

It allows users to generate citations for **books, journal articles, and websites**, organize them into a personal bibliography, add research notes, and export to multiple formats. 

Unlike simple citation generators, FolioCite acts as a **lightweight research management system**.

---

## 🚀 Features

### 🔍 Source Search & Import
- Search for **books** using:
  - Open Library API
  - Google Books API (enhanced search)
- Search for **journal articles**
- **Manual entry** for:
  - Books
  - Journal articles
  - Websites

### ✍️ Citation Generation
- Generates citations in:
  - APA (7th)
  - MLA (9th)
  - Chicago (Author–Date)
  - Harvard
  - Vancouver


### 📄 Output Formats
- Plain text citation
- Rich HTML-styled citation (with italics / formatting)

### 📤 Export Options
- Export bibliography as:
  - `.txt` (plain text)
  - `.bib` (BibTeX)
  - `.docx` (Microsoft Word / Google Docs compatible)
- Notes are **excluded** from bulk exports for clean academic formatting

### 📝 Research Notes
- Add **private notes** to every bibliography item
- Notes are:
  - Saved persistently
  - Editable at any time
- Copy:
  - Citation only
  - Citation + notes (per entry)

### 📘 Manual Entry
- Books
- Journal articles  
(Both with fully editable metadata)

### 💾 My Bibliography
- Save unlimited citations to your account (SQLite-backed)
- - Filter by:
  - All
  - Books only
  - Articles only
  - Websites only
- Auto-sort citation alphabetically
- Delete individual entries
- Clear entire bibliography
- One-click action:
  - `Copy citation (plain text)`
  - `Copy formatted HTML version`
  - `Copy BipTex`

### 👤 User Accounts
- Register & login system
- Each user has a **secure private bibliography**
- Logout confirmation for safety

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
├── services.py                 # Book search (Open Library + Google Books)
├── journal_services.py         # Journal article search (Open Library + Google Books)
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
├── run_foliocite_window.bat
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

- Metadata quality for books comes from **Open Library** and **Google Books** 
- Metadata for journal articles comes from **Crossref(articles)** and **Google Books** which may have varying author formatting. 
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
