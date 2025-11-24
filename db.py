import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = Path(os.getenv("DATABASE_URL", "foliocite.db"))


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Users table (unchanged)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    # Bibliography entries linked to user_id
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS bibliography (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            entry_type TEXT NOT NULL, -- "book", "article", or "website"
            title TEXT NOT NULL,
            authors TEXT NOT NULL,    -- semicolon-separated
            year TEXT,
            publisher TEXT,
            place TEXT,
            journal TEXT,
            volume TEXT,
            issue TEXT,
            pages TEXT,
            doi TEXT,
            site_name TEXT,
            url TEXT,
            accessed TEXT,
            style TEXT NOT NULL,
            cover_url TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )

# ---------- User helpers ----------

def create_user(username: str, email: str, password_hash: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO users (username, email, password_hash, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (username, email, password_hash, datetime.utcnow().isoformat()),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def get_user_by_email(email: str) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    return row


def get_user_by_username(username: str) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row


def get_user_by_id(user_id: int) -> Optional[sqlite3.Row]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row

# ---------- Bibliography helpers (per user) ----------

def add_entry(user_id: int, data: Dict[str, Any]) -> int:
    """
    data keys: entry_type, title, authors (semicolon string),
               year, publisher, place,
               journal, volume, issue, pages, doi,
               site_name, url, accessed,
               style, cover_url
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO bibliography (
            user_id,
            entry_type,
            title,
            authors,
            year,
            publisher,
            place,
            journal,
            volume,
            issue,
            pages,
            doi,
            site_name,
            url,
            accessed,
            style,
            cover_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            data["entry_type"],
            data["title"],
            data["authors"],
            data.get("year"),
            data.get("publisher"),
            data.get("place"),
            data.get("journal"),
            data.get("volume"),
            data.get("issue"),
            data.get("pages"),
            data.get("doi"),
            data.get("site_name"),
            data.get("url"),
            data.get("accessed"),
            data["style"],
            data.get("cover_url"),
        ),
    )
    conn.commit()
    entry_id = cur.lastrowid
    conn.close()
    return entry_id

def get_all_entries(user_id: int, entry_type: Optional[str] = None) -> List[sqlite3.Row]:
    conn = get_connection()
    cur = conn.cursor()

    if entry_type and entry_type != "all":
        cur.execute(
            "SELECT * FROM bibliography WHERE user_id = ? AND entry_type = ?",
            (user_id, entry_type),
        )
    else:
        cur.execute(
            "SELECT * FROM bibliography WHERE user_id = ?",
            (user_id,),
        )

    rows = cur.fetchall()
    conn.close()
    return rows


def delete_entry(user_id: int, entry_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM bibliography WHERE id = ? AND user_id = ?",
        (entry_id, user_id),
    )
    conn.commit()
    conn.close()


def clear_entries(user_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM bibliography WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()