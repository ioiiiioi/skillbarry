"""SQLite storage for skillsbary.

Each skill = a GitHub repo URL + a human description + optional tags.
The DB lives at ~/.skillsbary/skills.db by default (shared across all agents),
overridable via SKILLSBARY_DB env var.
"""
import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("SKILLSBARY_DB", Path.home() / ".skillsbary" / "skills.db"))


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                url TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                tags TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )


def _row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


def add_skill(name: str, url: str, description: str = "", tags: str = "") -> dict:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO skills (name, url, description, tags)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                url = excluded.url,
                description = excluded.description,
                tags = excluded.tags
            """,
            (name.strip(), url.strip(), description.strip(), tags.strip()),
        )
        conn.commit()
    return get_skill(name)


def get_skill(name: str) -> dict | None:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM skills WHERE name = ?", (name.strip(),)
        ).fetchone()
    return _row_to_dict(row) if row else None


def search_skills(query: str, limit: int = 10) -> list[dict]:
    q = f"%{query.strip()}%"
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT * FROM skills
            WHERE name LIKE ? OR description LIKE ? OR tags LIKE ?
            ORDER BY name
            LIMIT ?
            """,
            (q, q, q, limit),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def list_skills(limit: int = 100) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM skills ORDER BY name LIMIT ?", (limit,)
        ).fetchall()
    return [_row_to_dict(r) for r in rows]


def remove_skill(name: str) -> bool:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM skills WHERE name = ?", (name.strip(),))
        conn.commit()
    return cur.rowcount > 0
