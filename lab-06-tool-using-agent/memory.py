"""SQLite memory for the agent: stores what the user tells it and searches it later."""
import re
import sqlite3
from datetime import datetime

DB_FILE = "agent_memory.db"
STOPWORDS = {"what", "is", "my", "the", "a", "an", "of", "do", "you", "me", "i", "to", "and", "in",
             "user", "users", "user's", "about", "tell", "know", "remember", "does", "are", "was", "who", "where"}


def _connect():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("CREATE TABLE IF NOT EXISTS memories ("
                 "id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL, created TEXT NOT NULL)")
    return conn


def save_memory(text):
    """Store a statement from the user. Questions are not stored."""
    text = text.strip()
    if not text or text.endswith("?"):
        return False
    with _connect() as conn:
        conn.execute("INSERT INTO memories (content, created) VALUES (?, ?)",
                     (text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    return True


def search_memory(query, limit=5):
    """Return stored statements that share a keyword with the query (newest first)."""
    words = [w for w in re.findall(r"[a-zA-Z0-9']+", query.lower()) if w not in STOPWORDS and len(w) > 2]
    with _connect() as conn:
        if not words:
            rows = conn.execute("SELECT content, created FROM memories ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        else:
            where = " OR ".join(["LOWER(content) LIKE ?"] * len(words))
            rows = conn.execute(f"SELECT content, created FROM memories WHERE {where} ORDER BY id DESC LIMIT ?",
                                [f"%{w}%" for w in words] + [limit]).fetchall()
    return rows


def clear_memory():
    with _connect() as conn:
        conn.execute("DELETE FROM memories")
