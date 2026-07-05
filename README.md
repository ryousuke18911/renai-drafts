# Ren_ai 投稿下書き生成ツール（フェーズ1）

AI/テック系ニュースを取得し、X アカウント「Ren_ai」(@ren___ai) のトーンに合った投稿下書きを生成するツールです。

**このツールは下書きの生成・表示のみ行います。X への自動投稿は行いません**（人間が確認してコピー → 手動投稿）。

## 使い方（追加課金なしの運用）

下書きの生成は **Claude Code のチャットで「下書き作って」と頼むだけ**です。
Claude がニュースを取得して下書きを書き、`data/drafts.json` に保存 → 静的ページを生成して GitHub Pages に公開します。

**スマホ・外出先からの閲覧**: https://ryousuke18911.github.io/renai-drafts/

各下書きには次の機能があります:

- **Xで投稿** — Xの投稿画面が下書き＋記事URL入りで開く（投稿ボタンは自分で押す）
- **コピー** — クリップボードにコピー
- **投稿済みマーク** — チェックすると薄く表示（保存は端末のブラウザごと）
- **日本語ミニ解説** — 英語記事の内容を開かずに把握できる

ローカルで閲覧する場合:

```bash
./venv/bin/python app.py   # http://localhost:5001
```

### 下書き生成後の公開手順（Claude が実行）

```bash
./venv/bin/python build_site.py   # docs/index.html を生成
git add -A && git commit -m "下書き更新" && git push   # 1〜2分でページに反映
```

一度下書きを作った記事は `data/history.json` に記録され、次回以降は自動で除外されます。

## セットアップ（再構築する場合）

依存パッケージは `venv/` にインストール済み。作り直す場合:

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

## Anthropic API を使った全自動生成（オプション・従量課金）

将来 API 課金してもよくなった場合は、`.env` に `ANTHROPIC_API_KEY` を設定して:

```bash
./venv/bin/python generate_drafts.py
```

で Fable5 (claude-fable-5) による自動生成ができます（現在は未使用）。

## ファイル構成

| ファイル | 役割 |
|---|---|
| `config.py` | ペルソナ設定・ニュースソース・モデル設定 |
| `fetch_news.py` | TechCrunch / Ars Technica RSS + Hacker News API から記事取得 |
| `generate_drafts.py` | Fable5 で下書き生成（1記事につき3パターン） |
| `app.py` | Flask 簡易Web UI |
| `data/drafts.json` | 生成結果の保存先（.gitignore 対象） |

## トーン設定の調整

投稿文のルール（語尾・絵文字数・文字数など）は `generate_drafts.py` の `SYSTEM_PROMPT`、ペルソナ情報は `config.py` の `PERSONA` で調整できます。

## フェーズ2（予定・7/7以降）

- X API 接続によるワンクリック投稿
- 限定的な自動返信
- エンゲージメント記録とプロンプト改善のフィードバック
