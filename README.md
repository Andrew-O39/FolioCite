
# 📚 FolioCite

**FolioCite** is a clean, book-focused citation generator built with **FastAPI**.

It lets you search for a book (via the Open Library API) and generate formatted
citations in **APA**, **MLA**, or **Chicago (author–date)** style — all through
a simple web interface.

---

## 🚀 Features

- 🔍 Search for books by **title, author, or ISBN**
- 🌐 Uses the **Open Library** Search API for metadata
- 📝 Generates book citations in:
  - APA (7th edition, simplified)
  - MLA (9th edition, simplified)
  - Chicago (author–date, simplified)
- 🖥️ Clean, minimal web UI with Jinja2 templates
- 📋 One-click “Copy to clipboard” for the final citation
- 🧩 Small, readable codebase that is easy to extend

---

## 🗂️ Project structure

```text
FolioCiteApp/
│
├── main.py              # FastAPI app & routes
├── citation.py          # Book model & citation formatting logic
├── services.py          # Open Library API integration
├── db.py                # Database
│
├── templates/           # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   └── citation.html
│
├── static/
│   ├── styles.css       # Basic styling
│   └── logo.svg         # Simple FolioCite logo
├── docs/
│   └── user_guide.md
│
├── requirements.txt     # Python dependencies
├── run_foliocite_window.bat     # Script for running on Windows
├── env.local 
├── .env     # Environment file
└── README.md
         

```

---

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

You should see the FolioCite search page. Enter a book title, author, or ISBN,
choose a style, and follow the steps to get your formatted citation.

---

## ✨ Notes & limitations

- Metadata quality depends on **Open Library**. Some books may have missing or
  approximate years, publishers, or author lists.
- Citation formatting is intentionally **simplified** and currently focused on
  **books only**. Always double-check against your institution’s official style
  guide.
- This is a starter project and a great base to extend with more features.

---

## 🌱 Ideas for future improvements

- Support for other source types:
  - Journal articles
  - Book chapters
  - Theses
  - Websites
- Allow manual editing of metadata before generating the citation
- Add export formats (BibTeX, RIS, etc.)
- Add a public API endpoint (e.g. `/api/cite?isbn=...`)
- User accounts and saved citation collections

---

## 💡 About the name

**FolioCite** combines:

- **Folio** – pages, books, and manuscripts
- **Cite** – the act of referencing sources

It reflects the app’s focus on helping students and researchers quickly turn
books into clean citations.

Enjoy experimenting and extending FolioCite!
