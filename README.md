# skillsbary

MCP server untuk menyimpan & mencari URL repository **skill** AI beserta deskripsinya.

Kumpulkan public skills dari GitHub ke satu tempat. Nanti kalau AI-mu butuh skill tambahan,
dia cukup `search_skills("pdf parsing")` → dapat URL → install (clone / baca SKILL.md) ke agent-nya sendiri.

## Install

```bash
cd ~/Documents/personal/skillbarry
uv sync
```

## Jalankan via Docker Compose (SSE)

```bash
cd ~/Documents/personal/skillbarry
docker compose up -d --build
```

- Server MCP jalan di `http://localhost:8765` (transport SSE), endpoint `/sse`.
- Data persisten di volume `skillsbary_data` (SQLite `/data/skills.db`).
- Daftarkan ke Claude Code:
  ```bash
  claude mcp add --transport sse skillsbary http://localhost:8765/sse
  ```

## Data

Lokal (stdio): SQLite `~/.skillsbary/skills.db` (shared antar agent). Override via env `SKILLSBARY_DB`.
Docker (SSE): SQLite di volume `skillsbary_data`.

## Tools

| Tool | Fungsi |
|------|--------|
| `add_skill(name, url, description, tags)` | Simpan skill (upsert by name) |
| `search_skills(query, limit)` | Cari by nama/deskripsi/tags |
| `list_skills(limit)` | List semua |
| `get_skill(name)` | Ambil satu (URL + deskripsi) |
| `remove_skill(name)` | Hapus |

## Daftarkan ke Claude Code

```bash
claude mcp add skillsbary -- uv run --directory /home/hexboi/Documents/personal/skillbarry skillsbary
```

Atau manual di `.mcp.json` / `claude mcp` config:

```json
{
  "mcpServers": {
    "skillsbary": {
      "command": "uv",
      "args": ["run", "--directory", "/home/hexboi/Documents/personal/skillbarry", "skillsbary"]
    }
  }
}
```

## Alur pakai

1. Ketemu skill GitHub bagus → `add_skill("web-scraper", "https://github.com/...", "scrape halaman web jadi markdown", "scraping,web")`.
2. Nanti butuh skill → `search_skills("scraping")` → dapat URL + deskripsi.
3. Install: clone repo-nya, baca `SKILL.md`/`AGENTS.md`, daftarkan ke agent-mu.
