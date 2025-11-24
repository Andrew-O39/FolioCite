# 📘 FolioCite – User Guide
*A simple guide for using the FolioCite book citation generator.*

---

## 🗂️ What is FolioCite?

FolioCite is a simple tool that helps you:

- Search for a book (via Open Library)
- Search for a **journal article** (via Crossref)
- Confirm or edit its details  
- Generate a citation in multiple styles  
- Save citations to your personal bibliography  
- Export your bibliography as **.txt** or **.bib**  
- Manually enter a book if it cannot be found online  
- Delete items or clear your bibliography entirely

FolioCite is designed to make referencing quick and stress-free.


---

## 🚀 Getting Started

### 1️⃣ Open the app

After running the program, open your browser and visit:http://127.0.0.1:8000

This is the main search page.

---

## 👤 Creating an Account

1. Click **Register** in the top navigation bar.
2. Enter:
   - Username  
   - Email  
   - Password  
   - Confirm password  
3. After registration, you will be redirected to the login page.
4. Log in using your **username + password**.

Once logged in, the navigation bar will show:

- **Search**
- **Manual entry**
- **My Bibliography**
- **Logout (your username)**

---

## 🔍 Searching for a Source

On the homepage:

1. Enter your search query  
   - For **books**: title, author, or ISBN  
   - For **articles**: title, author, or DOI  
2. Choose what you are searching for:
   - **Book**
   - **Journal article**
3. Choose your citation style:
   - APA (7th)
   - MLA (9th)
   - Chicago
   - Harvard
   - Vancouver
4. Click **Search**.

Search results will show:

### For Books:
- Title  
- Authors  
- Publisher (if available)  
- Year  
- Book cover  

### For Articles:
- Title  
- Authors  
- Journal  
- Volume/issue  
- Pages  
- DOI  

Click **Select this item** to continue.

---

## ✏️ Confirming Source Details  
After selecting a result, you'll see a **confirmation page**.

This page lets you edit metadata before generating the citation.

### For Books:
- Title  
- Authors  
- Year  
- Publisher  
- Place  

### For Articles:
- Title  
- Authors  
- Journal  
- Year  
- Volume  
- Issue  
- Pages  
- DOI  

Fix anything that looks incorrect, then click:

### **Generate citation**

---

## 📄 Viewing Your Citation

The citation page provides:

### ✔ Plain-text citation  
Ready to paste into Word, Google Docs, etc.

### ✔ Formatted citation  
With italics and styling (HTML-based).

### ✔ BibTeX entry  
For LaTeX users.

All 3 areas include **Copy** buttons.

You’ll also see metadata and (for books) the cover image.

---

## 📚 Saving to My Bibliography

Click **Add to My Bibliography** to save the source.

To view your saved items:

1. Click **My Bibliography** in the navigation bar.

Your bibliography includes:

- All your saved citations  
- Sorted alphabetically  
- Switchable **style display** (APA/MLA/Chic./Harvard/Vancouver)  
- Filters:
  - **All**
  - **Books only**
  - **Articles only**

---

## 🧹 Managing Your Bibliography

On the **My Bibliography** page, you can:

### ✔ Delete one entry  
Each item has a delete button (with confirmation).

### ✔ Clear the entire bibliography  
A **Clear My Bibliography** button removes everything (with confirmation).

### ✔ Export your bibliography  
You can download:

- **.txt** — plain text list  
- **.bib** — BibTeX for LaTeX  

---

## ✍️ Manual Entry (Books & Articles)

If search doesn’t find your source:

1. Click **Manual entry**.
2. Choose:
   - **Book**
   - **Journal article**
3. Fill in the fields manually.
4. Select your citation style.
5. Click **Generate citation**.

Use manual entry for:

- Rare books  
- Old publications  
- Conference papers  
- Articles missing from databases  
- Local or unpublished material  

---

## 🚪 Logging Out

Click **Logout (your username)** in the navigation bar.

---

## 🆘 Troubleshooting

### **No results found**
Try:
- A simpler query  
- Author name only  
- ISBN (for books)  
- DOI (for articles)

### **API temporarily unavailable**
This occurs if Open Library or Crossref is offline.  
Try again in a few minutes.

### **Incorrect metadata**
Always double-check the **confirmation page**  
— you can edit anything before generating the citation.

### **Cannot copy citation**
If browser clipboard permissions fail, just select the text manually.

---

## 🎉 You’re ready to use FolioCite!

FolioCite makes referencing easy whether you're writing an essay, report, thesis, or research paper.

If you have suggestions or issues, feel free to provide feedback.

Happy writing! ✨