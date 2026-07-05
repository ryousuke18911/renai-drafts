# Ren_ai 投稿下書きツール

X（旧Twitter）アカウント「Ren_ai」(@ren___ai) 向けに、AI/テック系ニュースから投稿下書きを生成するプロジェクト。生成結果は GitHub Pages（https://ryousuke18911.github.io/renai-drafts/ 、mainブランチの docs/ フォルダ）で公開される。

**自動投稿は絶対にしない。** このツールは下書きの生成・表示のみ（ユーザーが手動でXに投稿する）。

## 「下書き作って」と頼まれたときの手順

ユーザーが「下書き作って」「下書き更新して」等と頼んだら、以下を実行する。Claude自身が下書きを書くこと（Anthropic APIは呼ばない。課金を避けるため）。

1. **環境準備**（venvが無い場合のみ）: `python3 -m venv venv && ./venv/bin/pip install -r requirements.txt`
2. **記事取得**: `./venv/bin/python -c "import json; from fetch_news import fetch_all_articles; print(json.dumps([a.__dict__ for a in fetch_all_articles()], ensure_ascii=False, indent=1))"`
   - `data/history.json` に記録済みのURLは自動で除外される
   - 新着が0件なら、その旨をユーザーに伝えて終了する
3. **下書き作成**: 各記事につき3案の投稿文と、日本語ミニ解説（summary_ja）をClaude自身が書く（トーンは下記）
4. **保存**: `data/drafts.json` を既存フォーマットで上書きする
   - `generated_at`: UTCのISO形式 / `generated_at_display`: 日本時間で「2026年7月6日 09:00」形式
   - 各記事: `title` / `url` / `source` / `drafts`（3案の配列）/ `error`(null) / `summary_ja`
   - 使った記事URLを `data/history.json` に追記する（既存分に追加。フォーマットはURL文字列の配列）
5. **公開**: `./venv/bin/python build_site.py` を実行し、`git add -A && git commit && git push` する
   - **mainブランチへ直接pushすること**（GitHub Pagesはmainのdocs/を配信しているため）。ブランチしか作れない環境の場合はPRを作り、可能なら即マージする
6. ユーザーに完了報告（記事数と、1〜2分でページに反映されることを伝える）

## 投稿文のトーン（必ず守る）

- 語尾は「〜です/ます」＋「〜しましょう！」「気になりますね」など、ふんわり親しみやすい口調
- 「事実の要約」＋「気になったポイント・一言感想」を必ず両方含める
- 全体で140字以内（90〜110字が目安。投稿時に記事URLが後ろに付く）
- 絵文字は最大1〜2個、ハッシュタグは0〜2個
- 事実は記事タイトル・要約の範囲内に限定し、誇張・断定をしない
- 記事本文の丸写しをせず、自分なりの視点を加える
- 出典URLは本文に含めない（ページ側で別途表示される）

## 補足

- ニュースソースや件数の設定は `config.py`
- `generate_drafts.py` はAnthropic API用の未使用コード（将来用に残置。呼ばないこと）
- ローカル閲覧用のFlask UI: `./venv/bin/python app.py`（port 5001）
