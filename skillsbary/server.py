"""skillsbary MCP server.

Exposes tools to store and search GitHub skill repositories, so an AI agent
can collect public skills and later look them up when it needs one.

Transport is selected via SKILLSBARY_TRANSPORT env var:
  - "stdio" (default) — for local `claude mcp add` / agent subprocess
  - "sse"            — long-lived HTTP server (for Docker)
  - "streamable-http" — long-lived HTTP server
"""
import os

from mcp.server.fastmcp import FastMCP

from skillsbary import db

HOST = os.getenv("SKILLSBARY_HOST", "0.0.0.0")
PORT = int(os.getenv("SKILLSBARY_PORT", "8765"))

mcp = FastMCP("skillsbary", host=HOST, port=PORT)


@mcp.tool()
def add_skill(name: str, url: str, description: str = "", tags: str = "") -> dict:
    """Store a skill repository. Use when you find a useful public GitHub skill
    you want to remember.

    Args:
        name: Short unique identifier (e.g. "pdf-parser").
        url: Full GitHub repo URL (https://github.com/owner/repo).
        description: What the skill does, in your own words. Searchable.
        tags: Comma-separated categories (e.g. "pdf,docs,extract").

    Returns the stored entry. Upserts on name (re-add updates the entry).
    """
    db.init_db()
    return db.add_skill(name, url, description, tags)


@mcp.tool()
def search_skills(query: str, limit: int = 10) -> list[dict]:
    """Search stored skills by name, description, or tags. Use when you need a
    skill and want to find a matching repo URL to install.

    Args:
        query: Keyword(s) to match against name/description/tags.
        limit: Max results to return.

    Returns a list of matches, each with name, url, description, tags.
    """
    db.init_db()
    return db.search_skills(query, limit)


@mcp.tool()
def list_skills(limit: int = 100) -> list[dict]:
    """List all stored skills alphabetically by name."""
    db.init_db()
    return db.list_skills(limit)


@mcp.tool()
def get_skill(name: str) -> dict | None:
    """Get one skill by exact name. Returns its URL + description, or None if missing."""
    db.init_db()
    return db.get_skill(name)


@mcp.tool()
def remove_skill(name: str) -> dict:
    """Remove a skill by exact name. Returns removal status."""
    db.init_db()
    removed = db.remove_skill(name)
    return {"name": name, "removed": removed}


def main() -> None:
    db.init_db()
    transport = os.getenv("SKILLSBARY_TRANSPORT", "stdio")
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
