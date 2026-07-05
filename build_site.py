"""data/drafts.json から GitHub Pages 用の静的ページ (docs/) を生成する."""

import json
import os
import shutil

from jinja2 import Environment, FileSystemLoader

import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")


def _static_url_for(endpoint: str, filename: str = "") -> str:
    # Flaskのurl_for('static', filename=...)を静的サイト用の相対パスに置き換える
    return filename


def build() -> str:
    with open(config.DRAFTS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    env = Environment(loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")))
    template = env.get_template("index.html")
    html = template.render(data=data, persona=config.PERSONA, url_for=_static_url_for)

    os.makedirs(DOCS_DIR, exist_ok=True)
    out_path = os.path.join(DOCS_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copy(os.path.join(BASE_DIR, "static", "style.css"), os.path.join(DOCS_DIR, "style.css"))
    return out_path


if __name__ == "__main__":
    path = build()
    print(f"生成しました: {path}")
