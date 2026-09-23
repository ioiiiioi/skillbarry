# skillsbary

MCP server untuk menyimpan & mencari URL repository **skill** AI beserta deskripsinya.

Kumpulkan public skills dari GitHub ke satu tempat. Nanti kalau AI-mu butuh skill tambahan,
dia cukup `search_skills("pdf parsing")` → dapat URL → install (clone / baca SKILL.md) ke agent-nya sendiri.

## Install

```bash
cd ~/Documents/personal/skillbarry
uv sync
```

## Jalankan via Docker Compose (streamable HTTP)

```bash
cd ~/Documents/personal/skillbarry
docker compose up -d --build
```

- Server MCP jalan di `http://localhost:8765` (transport streamable HTTP), endpoint `/mcp`.
- Data persisten di volume `skillsbary_data` (SQLite `/data/skills.db`).
- Daftarkan ke Claude Code:
  ```bash
  claude mcp add --transport http skillsbary http://localhost:8765/mcp
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

## UI List (Prefab)

Tabel skill pakai [Prefab UI](https://prefab.prefect.io/docs/welcome.md) — di-render jadi satu file HTML
self-contained (renderer dari CDN). Tanpa server, tanpa build step.

```bash
uv run skillsbary-ui              # tulis skills.html
uv run skillsbary-ui -o out.html  # path custom
```

Kolom: Nama, Deskripsi, Tags, Repo (link), Ditambahkan. Ada search + pagination + sort.

Preview live-reload saat ngoprek tampilan:

```bash
uv run prefab serve skillsbary/ui.py
```

`SKILLSBARY_DB` menentukan DB yang dibaca — default `~/.skillsbary/skills.db`,
DB repo bisa dipakai lewat `SKILLSBARY_DB=./skillbarry-skills.db uv run skillsbary-ui`.

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
