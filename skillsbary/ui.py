"""Halaman list skill pakai Prefab UI.

Render tabel skill dari SQLite jadi satu file HTML self-contained
(renderer di-load dari CDN). Tidak butuh server MCP atau backend —
data dibaca sekali saat render, sisanya jalan di browser.

Pakai:
    uv run skillsbary-ui              # tulis skills.html
    uv run skillsbary-ui -o out.html
    uv run prefab serve skillsbary/ui.py   # preview live-reload
"""
import argparse

from prefab_ui.app import PrefabApp
from prefab_ui.components import (
    DataTable,
    DataTableColumn,
    Heading,
    Link,
    Text,
)

from skillsbary import db

COLUMNS = [
    DataTableColumn(key="name", header="Nama", sortable=True, min_width="150px"),
    DataTableColumn(key="description", header="Deskripsi", min_width="260px"),
    DataTableColumn(key="tags", header="Tags", width="180px"),
    DataTableColumn(key="url", header="Repo"),
    DataTableColumn(key="added", header="Ditambahkan", sortable=True, width="130px"),
]


def _row(skill: dict) -> dict:
    url = skill["url"]
    return {
        "name": skill["name"],
        "description": skill["description"] or "—",
        "tags": skill["tags"] or "—",
        "url": Link(url.removeprefix("https://").removeprefix("http://"), href=url, target="_blank"),
        "added": (skill.get("created_at") or "")[:10],
    }


def build_app() -> PrefabApp:
    db.init_db()
    skills = db.list_skills(limit=500)
    with PrefabApp(title="skillsbary", css_class="p-6") as app:
        Heading("skillsbary")
        Text(f"{len(skills)} skill tersimpan")
        DataTable(columns=COLUMNS, rows=[_row(s) for s in skills], search=True, paginated=True)
    return app


app = build_app()  # untuk `prefab serve`


def render(output: str = "skills.html") -> str:
    html = build_app().html()
    with open(output, "w", encoding="utf-8") as f:
        f.write(html)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Render list skill skillsbary ke HTML")
    parser.add_argument("-o", "--output", default="skills.html", help="path output HTML")
    args = parser.parse_args()
    print(f"ok: {render(args.output)}")


if __name__ == "__main__":
    main()
