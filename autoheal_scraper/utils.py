import os
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "storage.db"
SELECTOR_KEY = "price_selectors"
HTML_KEY = "product_page:last_html"
DEFAULT_SELECTOR = {"type": "css", "value": "div.price"}


# -------------------------
# SELECTOR MANAGEMENT
# -------------------------

def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS selectors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                value TEXT NOT NULL,
                position INTEGER NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS html_snapshot (
                key TEXT PRIMARY KEY,
                html TEXT,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


# -------------------------
# SELECTOR MANAGEMENT
# -------------------------

def load_selectors():
    """Read selectors from SQLite, falling back to the default selector."""
    init_db()
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT type, value FROM selectors ORDER BY position ASC"
        ).fetchall()

    if rows:
        return [{"type": row["type"], "value": row["value"]} for row in rows]

    default_selectors = [DEFAULT_SELECTOR]
    save_selectors(default_selectors)
    return default_selectors


def save_selectors(selectors):
    """Save selectors to SQLite."""
    init_db()
    with get_conn() as conn:
        conn.execute("DELETE FROM selectors")
        for position, selector in enumerate(selectors):
            conn.execute(
                "INSERT INTO selectors (type, value, position) VALUES (?, ?, ?)",
                (selector["type"], selector["value"], position),
            )
        conn.commit()


def init_selectors():
    """Initialize selectors if empty (run once)."""
    init_db()
    with get_conn() as conn:
        count = conn.execute("SELECT COUNT(*) FROM selectors").fetchone()[0]
    if count == 0:
        save_selectors([DEFAULT_SELECTOR])


def add_selector(new_selector):
    """Add new selector with priority."""
    selectors = load_selectors()
    selectors = [new_selector] + [s for s in selectors if s != new_selector]
    save_selectors(selectors)


# -------------------------
# HTML SNAPSHOT
# -------------------------

def save_html_snapshot(html: str):
    """Store the last successful HTML snapshot in SQLite."""
    init_db()
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO html_snapshot (key, html)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET
                html = excluded.html,
                saved_at = CURRENT_TIMESTAMP
            """,
            (HTML_KEY, html),
        )
        conn.commit()


def get_last_html():
    """Retrieve the last working HTML snapshot from SQLite."""
    init_db()
    with get_conn() as conn:
        row = conn.execute(
            "SELECT html FROM html_snapshot WHERE key = ?",
            (HTML_KEY,),
        ).fetchone()

    return row["html"] if row is not None else ""