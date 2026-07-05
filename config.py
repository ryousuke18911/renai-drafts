"""Ren_ai 投稿下書きツールの設定."""

import os

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
FABLE_MODEL = "claude-fable-5"

# --- アカウントのペルソナ設定（仕様書 1章より） ---
PERSONA = {
    "display_name": "Ren_ai",
    "username": "@ren___ai",
    "genre": "AI / テック",
    "tone": "ふんわり・親しみやすい系（硬すぎない、「〜しましょう！」「フォローお願いします！」など）",
    "bio": "気になるAI・テックニュースをゆるく紹介📡 一緒に情報キャッチアップしましょう。フォローお願いします！",
}

# 1記事あたりの下書き生成パターン数
VARIATIONS_PER_ARTICLE = 3

# 取得する記事の最大件数（全ソース合計）
MAX_ARTICLES = 8

# --- ニュースソース ---
RSS_SOURCES = [
    {"name": "TechCrunch (AI)", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"name": "Ars Technica (AI)", "url": "https://arstechnica.com/tag/ai/feed/"},
]

# Hacker News: Algolia Search APIでAI/テック関連キーワードのタイトルのみ抽出
HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search_by_date"
HN_KEYWORDS = ["AI", "LLM", "GPT", "Claude", "machine learning", "OpenAI", "Anthropic", "chatbot"]
HN_MAX_RESULTS = 20

DRAFTS_JSON_PATH = os.path.join(os.path.dirname(__file__), "data", "drafts.json")
