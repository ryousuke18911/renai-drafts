"""AI/テック系ニュースの取得（RSS + Hacker News）."""

import html
import json
import os
import re
from dataclasses import dataclass

import feedparser
import requests

import config

HISTORY_PATH = os.path.join(os.path.dirname(__file__), "data", "history.json")


def load_history() -> set[str]:
    """過去に下書きを作った記事URLの一覧（重複投稿の防止用）."""
    if not os.path.exists(HISTORY_PATH):
        return set()
    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_history(urls: set[str]) -> None:
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted(urls), f, ensure_ascii=False, indent=1)


@dataclass
class Article:
    title: str
    url: str
    summary: str
    source: str


def _clean_summary(raw: str, max_len: int = 300) -> str:
    text = re.sub(r"<[^>]+>", "", raw or "")
    text = html.unescape(text).strip()
    text = re.sub(r"\s+", " ", text)
    return text[:max_len]


def fetch_rss_articles() -> list[Article]:
    articles = []
    for source in config.RSS_SOURCES:
        try:
            feed = feedparser.parse(source["url"])
        except Exception:
            continue
        for entry in feed.entries[:5]:
            title = getattr(entry, "title", "").strip()
            link = getattr(entry, "link", "").strip()
            summary = _clean_summary(getattr(entry, "summary", "") or getattr(entry, "description", ""))
            if not title or not link:
                continue
            articles.append(Article(title=title, url=link, summary=summary, source=source["name"]))
    return articles


def fetch_hn_articles() -> list[Article]:
    articles = []
    seen_ids = set()
    for keyword in config.HN_KEYWORDS:
        try:
            resp = requests.get(
                config.HN_SEARCH_URL,
                params={"query": keyword, "tags": "story", "hitsPerPage": 5},
                timeout=10,
            )
            resp.raise_for_status()
            hits = resp.json().get("hits", [])
        except Exception:
            continue
        for hit in hits:
            object_id = hit.get("objectID")
            if object_id in seen_ids:
                continue
            title = (hit.get("title") or "").strip()
            url = hit.get("url") or f"https://news.ycombinator.com/item?id={object_id}"
            if not title:
                continue
            seen_ids.add(object_id)
            articles.append(
                Article(title=title, url=url, summary="", source="Hacker News")
            )
        if len(articles) >= config.HN_MAX_RESULTS:
            break
    return articles


def fetch_all_articles(exclude_history: bool = True) -> list[Article]:
    articles = fetch_rss_articles() + fetch_hn_articles()
    history = load_history() if exclude_history else set()

    # URL重複と過去に使った記事を除外（順序維持）
    seen_urls = set()
    unique = []
    for article in articles:
        if article.url in seen_urls or article.url in history:
            continue
        seen_urls.add(article.url)
        unique.append(article)

    return unique[: config.MAX_ARTICLES]
