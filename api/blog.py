"""Persist SeoSmith articles and publish static HTML for Nginx."""

from __future__ import annotations

import copy
import html
import json
import os
import re
import threading
import uuid
from pathlib import Path
from typing import Any
from urllib.parse import quote
from xml.sax.saxutils import escape as xml_escape


SITE_URL = "https://molniya-tech.ru"
TEMPLATE_DIR = Path(os.getenv("BLOG_TEMPLATE_DIR", Path(__file__).resolve().parent.parent / "blog"))
RECORDS_SEED_DIR = Path(os.getenv("BLOG_SEED_DIR", TEMPLATE_DIR / "records"))
DATA_DIR = Path(os.getenv("BLOG_DATA_DIR", Path(__file__).resolve().parent.parent / ".blog-data"))
RECORDS_DIR = DATA_DIR / ".records"
REDIRECTS_PATH = DATA_DIR / ".redirects.json"
SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
_write_lock = threading.Lock()



def _articles() -> list[tuple[Path, dict[str, Any]]]:
    if not RECORDS_DIR.exists():
        return []
    return [(path, json.loads(path.read_text(encoding="utf-8"))) for path in RECORDS_DIR.glob("*.json")]


def _redirects() -> dict[str, str]:
    if not REDIRECTS_PATH.exists():
        return {}
    return json.loads(REDIRECTS_PATH.read_text(encoding="utf-8"))


def _write_atomic(path: Path, content: str) -> None:
    temp = path.parent / f".{uuid.uuid4().hex}.tmp"
    try:
        temp.write_text(content, encoding="utf-8")
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def _prepare_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RECORDS_DIR.mkdir(exist_ok=True)
    # Earlier webhook builds stored records at the volume root.
    for legacy in DATA_DIR.glob("*.json"):
        if legacy.name.startswith("."):
            continue
        destination = RECORDS_DIR / legacy.name
        if destination.exists():
            raise OSError(f"Duplicate article record: {legacy.name}")
        os.replace(legacy, destination)


def _sync_template_records() -> None:
    if not RECORDS_SEED_DIR.is_dir():
        return
    articles = _articles()
    existing_by_id = {row["id"]: (path, row) for path, row in articles}
    existing_by_slug = {row["slug"]: (path, row) for path, row in articles}
    redirects = _redirects()
    for seed_path in sorted(RECORDS_SEED_DIR.glob("*.json")):
        try:
            data = json.loads(seed_path.read_text(encoding="utf-8"))
            article = validate_article(data)
        except Exception:
            continue
        target_info = existing_by_id.get(article["id"]) or existing_by_slug.get(article["slug"])
        if target_info:
            target, old = target_info
            if old["slug"] != article["slug"]:
                redirects[old["slug"]] = target.name
        else:
            target = RECORDS_DIR / f"{article['slug']}.json"
        redirects.pop(article["slug"], None)
        _write_atomic(target, json.dumps(article, ensure_ascii=False))
    if redirects:
        _write_atomic(REDIRECTS_PATH, json.dumps(redirects, ensure_ascii=False))


def validate_article(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("article must be an object")
    article_id = value.get("id")
    if isinstance(article_id, bool) or not isinstance(article_id, (str, int)) or not str(article_id).strip():
        raise ValueError("article.id is required")
    slug = value.get("slug")
    if not isinstance(slug, str) or not SLUG_RE.fullmatch(slug):
        raise ValueError("article.slug is invalid")
    for key in ("title", "body_html"):
        if not isinstance(value.get(key), str) or not value[key].strip():
            raise ValueError(f"article.{key} is required")
    meta = value.get("meta") or {}
    if not isinstance(meta, dict):
        raise ValueError("article.meta must be an object")
    for key in ("title", "description"):
        if key in meta and not isinstance(meta[key], str):
            raise ValueError(f"article.meta.{key} is invalid")
    if "keywords" in meta and not isinstance(meta["keywords"], (str, list)):
        raise ValueError("article.meta.keywords is invalid")
    for key in ("url", "short_answer", "alt_text", "image_prompt"):
        if key in value and value[key] is not None and not isinstance(value[key], str):
            raise ValueError(f"article.{key} must be a string")
    if "faq" in value and value["faq"] is not None and not isinstance(value["faq"], list):
        raise ValueError("article.faq must be a list")
    if "insights" in value and value["insights"] is not None and not isinstance(value["insights"], (str, list)):
        raise ValueError("article.insights is invalid")
    return {
        "id": str(article_id).strip(),
        "title": value["title"].strip(),
        "slug": slug,
        "url": value.get("url") or "",
        "short_answer": value.get("short_answer") or "",
        "insights": value.get("insights") or [],
        "body_html": value["body_html"],
        "meta": {key: meta.get(key, "") for key in ("title", "description", "keywords")},
        "faq": value.get("faq") or [],
        "json_ld": value.get("json_ld"),
        "image_prompt": value.get("image_prompt") or "",
        "alt_text": value.get("alt_text") or "",
    }


def upsert_article(article: dict[str, Any]) -> None:
    """Update the record and materialized public pages under one writer lock."""
    with _write_lock:
        _prepare_storage()
        articles = _articles()
        by_id = next((path for path, row in articles if row["id"] == article["id"]), None)
        by_slug = next((path for path, row in articles if row["slug"] == article["slug"]), None)
        if by_id and by_slug and by_id != by_slug:
            raise ValueError("slug belongs to another article")
        target = by_id or by_slug or RECORDS_DIR / f"{uuid.uuid4().hex}.json"
        redirects = _redirects()
        reserved = redirects.get(article["slug"])
        if reserved and reserved != target.name:
            raise ValueError("slug belongs to another article")
        old = next((row for path, row in articles if path == target), None)
        updated = [(path, article if path == target else row) for path, row in articles]
        if old is None:
            updated.append((target, article))
        rows = [row for _, row in updated]
        if old and old["slug"] != article["slug"]:
            redirects[old["slug"]] = target.name
        redirects.pop(article["slug"], None)

        # Make the new URL available before pointing the index and sitemap to it.
        _write_atomic(DATA_DIR / f"{article['slug']}.html", render_article(article))
        _write_atomic(DATA_DIR / "index.html", render_blog(rows))
        _write_atomic(DATA_DIR / "sitemap.xml", render_sitemap(rows))
        _write_atomic(REDIRECTS_PATH, json.dumps(redirects, ensure_ascii=False))
        _write_atomic(target, json.dumps(article, ensure_ascii=False))
        if old and old["slug"] != article["slug"]:
            (DATA_DIR / f"{old['slug']}.html").unlink(missing_ok=True)


def rebuild_public() -> None:
    """Refresh pages from durable records on API startup, including template edits."""
    with _write_lock:
        _prepare_storage()
        _sync_template_records()
        rows = [row for _, row in _articles()]
        for article in rows:
            _write_atomic(DATA_DIR / f"{article['slug']}.html", render_article(article))
        _write_atomic(DATA_DIR / "index.html", render_blog(rows))
        _write_atomic(DATA_DIR / "sitemap.xml", render_sitemap(rows))
        current = {"index.html", *(f"{row['slug']}.html" for row in rows)}
        for stale in DATA_DIR.glob("*.html"):
            if stale.name not in current:
                stale.unlink()


def redirect_target(slug: str) -> str | None:
    record_name = _redirects().get(slug)
    if not record_name:
        return None
    record_path = RECORDS_DIR / record_name
    if not record_path.is_file():
        return None
    return json.loads(record_path.read_text(encoding="utf-8"))["slug"]


def _escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _summary_items(value: str | list[Any]) -> list[str]:
    if isinstance(value, str):
        return [value] if value.strip() else []
    items = []
    for item in value:
        if isinstance(item, str) and item.strip():
            items.append(item)
        elif isinstance(item, dict):
            text = item.get("text") or item.get("insight") or item.get("title")
            if isinstance(text, str) and text.strip():
                items.append(text)
    return items


def _description(article: dict[str, Any]) -> str:
    return str(article["meta"].get("description") or article["short_answer"] or article["title"])


def _link_organization_publisher(schema: Any) -> Any:
    """Connect legacy SeoSmith article markup to the site's Organization node."""
    schema = copy.deepcopy(schema)

    def visit(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                visit(item)
        elif isinstance(node, dict):
            article_type = node.get("@type")
            if article_type in ("Article", "BlogPosting", "NewsArticle"):
                publisher = node.get("publisher")
                if (isinstance(publisher, dict)
                        and not publisher.get("@id")
                        and isinstance(publisher.get("url"), str)
                        and publisher["url"].rstrip("/") == SITE_URL):
                    publisher["@id"] = f"{SITE_URL}/#organization"
            graph = node.get("@graph")
            if isinstance(graph, (dict, list)):
                visit(graph)

    visit(schema)
    return schema


def render_blog(articles: list[dict[str, Any]] | None = None) -> str:
    page = (TEMPLATE_DIR / "index.html").read_text(encoding="utf-8")
    articles = sorted(articles if articles is not None else (row for _, row in _articles()), key=lambda row: row["slug"])
    if articles:
        cards = []
        for article in articles:
            href = f"/blog/{quote(article['slug'])}"
            cards.append(
                '<a class="mt-post-card mt-post-card--published" href="' + href + '">'
                '<span class="mt-post-status">Статья</span>'
                '<h2 class="mt-post-topic">' + _escape(article["title"]) + '</h2>'
                '<p class="mt-post-desc">' + _escape(_description(article)) + '</p>'
                '<span class="mt-post-read">Читать статью →</span></a>'
            )
        content = '<div class="mt-blog-grid">' + "\n".join(cards) + '</div>'
    else:
        content = page.split("<!-- POSTS START -->", 1)[1].split("<!-- POSTS END -->", 1)[0]
    return page.split("<!-- POSTS START -->", 1)[0] + content + page.split("<!-- POSTS END -->", 1)[1]


def render_article(article: dict[str, Any]) -> str:
    page = (TEMPLATE_DIR / "index.html").read_text(encoding="utf-8")
    title = article["meta"].get("title") or article["title"]
    description = _description(article)
    canonical = f"{SITE_URL}/blog/{quote(article['slug'])}"
    keywords = article["meta"].get("keywords") or ""
    if isinstance(keywords, list):
        keywords = ", ".join(str(item) for item in keywords)
    seo = (
        f'<title>{_escape(title)} — Молния Тех</title>\n'
        f'  <meta name="description" content="{_escape(description)}">\n'
        f'  <meta name="keywords" content="{_escape(keywords)}">\n'
        f'  <link rel="canonical" href="{_escape(canonical)}">\n'
        f'  <meta property="og:type" content="article">\n'
        f'  <meta property="og:site_name" content="Молния Тех">\n'
        f'  <meta property="og:locale" content="ru_RU">\n'
        f'  <meta property="og:title" content="{_escape(title)}">\n'
        f'  <meta property="og:description" content="{_escape(description)}">\n'
        f'  <meta property="og:url" content="{_escape(canonical)}">\n'
        f'  <meta property="og:image" content="{SITE_URL}/assets/img/schedule.jpg">\n'
        f'  <meta name="twitter:card" content="summary_large_image">\n'
        f'  <meta name="twitter:title" content="{_escape(title)}">\n'
        f'  <meta name="twitter:description" content="{_escape(description)}">\n'
        f'  <meta name="twitter:image" content="{SITE_URL}/assets/img/schedule.jpg">\n'
    )
    if article["json_ld"]:
        structured = article["json_ld"]
        if isinstance(structured, str):
            try:
                structured = json.loads(structured)
            except json.JSONDecodeError:
                structured = None
        if structured is not None:
            structured = _link_organization_publisher(structured)
            seo += '<script type="application/ld+json">' + json.dumps(structured, ensure_ascii=False).replace("<", "\\u003c") + '</script>\n'
    page = page.split("<!-- SEO START -->", 1)[0] + seo + page.split("<!-- SEO END -->", 1)[1]

    intro = ''
    if article["short_answer"]:
        intro = '<aside class="mt-article-answer"><strong>Короткий ответ</strong><p>' + _escape(article["short_answer"]) + '</p></aside>'
    items = _summary_items(article["insights"])
    summary = ''
    if items:
        summary = '<aside class="mt-article-insights"><h2>Главное из статьи</h2><ul>' + ''.join('<li>' + _escape(item) + '</li>' for item in items) + '</ul></aside>'
    faq_html = ''
    if article.get("faq") and isinstance(article["faq"], list):
        faq_items = []
        for item in article["faq"]:
            if isinstance(item, dict):
                q = item.get("question") or item.get("q")
                a = item.get("answer") or item.get("a")
                if q and a:
                    faq_items.append(
                        '<div class="mt-faq-item"><h3 class="mt-faq-q">' + _escape(q) + '</h3><p class="mt-faq-a">' + _escape(a) + '</p></div>'
                    )
        if faq_items:
            faq_html = '<section class="mt-article-faq"><h2>Часто задаваемые вопросы</h2>' + ''.join(faq_items) + '</section>'
    content = (
        '<section class="mt-section mt-article-section"><div class="mt-article">'
        '<a class="mt-article-back" href="/blog">← Все статьи</a>'
        '<div class="mt-eyebrow">Блог Молнии</div>'
        '<h1 class="mt-section-title">' + _escape(article["title"]) + '</h1>'
        + intro + summary + '<div class="mt-article-body">' + article["body_html"] + '</div>'
        + faq_html
        + '</div></section>\n'
    )
    return page.split("<!-- BLOG CONTENT START -->", 1)[0] + content + page.split("<!-- BLOG CONTENT END -->", 1)[1]


def render_sitemap(articles: list[dict[str, Any]] | None = None) -> str:
    rows = articles if articles is not None else (row for _, row in _articles())
    urls = ["/", "/auto", "/beauty", "/health", "/requisites", "/privacy", "/blog"] + [f"/blog/{quote(row['slug'])}" for row in rows]
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{xml_escape(SITE_URL + path)}</loc></url>\n' for path in urls
    ) + '</urlset>\n'
