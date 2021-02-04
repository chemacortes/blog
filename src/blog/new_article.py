#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tarea para generar la plantilla de un nuevo artículo para el blog

Se lanza dentro del vscode con F6

"""


import sys
from datetime import datetime
from pathlib import Path

from slugify import slugify

SCRIPTS_DIR = Path(__file__).parent


def new_article(title: str, category: str) -> None:

    now: datetime = datetime.now()
    year: str = str(now.year)
    prefix: str = now.strftime("%Y-%m-%d")
    slug = slugify(sys.argv[1])
    article = Path.cwd() / "content" / year / f"{prefix}-{slug}.md"

    if article.exists():
        print(f"### ERROR: artículo '{article}' ya existe")
        return

    vars = {
        "TITLE": title,
        "CATEGORY": category,
        "AUTHOR": "Chema Cortés",
        "NOW": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "SLUG": slug,
    }

    template = (SCRIPTS_DIR / "template.md").read_text()
    for k, v in vars.items():
        template = template.replace(f"<<{k}>>", v)

    article.write_text(template)

    print(f"Creado artículo '{article}'")


if __name__ == "__main__":

    if len(sys.argv) <= 2:
        print(f"USAGE: {sys.argv[0]} <articleTitle> <articleCategory")
        sys.exit()

    title = sys.argv[1]
    category = sys.argv[2]
    new_article(title, category)
