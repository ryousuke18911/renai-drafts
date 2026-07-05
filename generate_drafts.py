"""Fable5 (claude-fable-5) を使って Ren_ai トーンの投稿下書きを生成する."""

import json
import re
from datetime import datetime, timezone

import anthropic

import config
from fetch_news import Article, fetch_all_articles

SYSTEM_PROMPT = f"""あなたはX（旧Twitter）アカウント「{config.PERSONA['display_name']}」({config.PERSONA['username']}) の投稿文を書くライターです。

# アカウントの人格
- ジャンル: {config.PERSONA['genre']}
- トーン: {config.PERSONA['tone']}
- Bio: {config.PERSONA['bio']}

# 投稿文のルール（必ず守ること）
- 語尾は「〜です/ます」＋「〜しましょう！」「フォローお願いします！」のような、ふんわり親しみやすい口調にする
- 「事実の要約」と「気になったポイント・一言感想」の両方を必ず含める
- 全体で140字前後に収める
- 絵文字は最大1〜2個までとし、上品さを保つ（多用しない）
- ハッシュタグは0〜2個まで
- 事実は与えられた記事タイトル・要約の範囲内に限定し、誇張・断定的な表現は使わない
- 記事本文の丸写しはせず、自分なりの視点を必ず加える
- 出典URLは本文に含めない（別途表示するため）

# 出力形式
必ず次のJSON形式のみを出力すること。説明文やコードブロックの記法は不要。
{{"drafts": ["1つ目の下書き", "2つ目の下書き", "3つ目の下書き"]}}
"""


def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"JSONが見つかりませんでした: {text[:200]}")
    return json.loads(match.group(0))


def generate_drafts_for_article(client: anthropic.Anthropic, article: Article) -> list[str]:
    user_prompt = (
        f"次の記事をもとに、{config.VARIATIONS_PER_ARTICLE}パターンの投稿下書きを作成してください。\n\n"
        f"記事タイトル: {article.title}\n"
        f"記事要約: {article.summary or '(要約なし。タイトルから内容を推測して書いてください)'}\n"
        f"情報源: {article.source}\n"
    )

    response = client.messages.create(
        model=config.FABLE_MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )
    text = "".join(block.text for block in response.content if block.type == "text")
    data = _extract_json(text)
    drafts = data.get("drafts", [])
    return [d.strip() for d in drafts if isinstance(d, str) and d.strip()]


def generate_all(progress_callback=None) -> dict:
    if not config.ANTHROPIC_API_KEY:
        raise RuntimeError(
            "ANTHROPIC_API_KEY が設定されていません。.env ファイルに設定してください。"
        )

    client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    articles = fetch_all_articles()

    results = []
    for i, article in enumerate(articles):
        if progress_callback:
            progress_callback(i + 1, len(articles), article.title)
        try:
            drafts = generate_drafts_for_article(client, article)
        except Exception as exc:
            drafts = []
            error = str(exc)
        else:
            error = None
        results.append(
            {
                "title": article.title,
                "url": article.url,
                "source": article.source,
                "drafts": drafts,
                "error": error,
            }
        )

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "articles": results,
    }

    with open(config.DRAFTS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return output


if __name__ == "__main__":
    def _print_progress(current, total, title):
        print(f"[{current}/{total}] 生成中: {title}")

    result = generate_all(progress_callback=_print_progress)
    print(f"\n{len(result['articles'])}件の記事について下書きを生成しました。")
    print(f"保存先: {config.DRAFTS_JSON_PATH}")
