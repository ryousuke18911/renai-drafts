"""Ren_ai 投稿下書きツール - 簡易Web UI（フェーズ1: 下書き表示のみ、自動投稿なし）.

下書きの生成はClaude Codeのチャット経由で行い、このアプリは data/drafts.json の閲覧専用。
"""

import json
import os

from flask import Flask, render_template

import config

app = Flask(__name__)


def load_drafts():
    if not os.path.exists(config.DRAFTS_JSON_PATH):
        return None
    with open(config.DRAFTS_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def index():
    data = load_drafts()
    return render_template("index.html", data=data, persona=config.PERSONA)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
