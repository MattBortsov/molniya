"""Private, durable storage for lead applications and consent evidence."""

from __future__ import annotations

import hashlib
import os
import sqlite3
import uuid
from contextlib import closing
from datetime import datetime, timedelta, timezone
from pathlib import Path


SITE_ROOT = Path(__file__).resolve().parent.parent
CONSENT_TEXT = "Согласен на обработку персональных данных по политике конфиденциальности."
POLICY_URL = "https://molniya-tech.ru/privacy"
FORM_NAMES = {
    "home": "Главная — бесплатный доступ",
    "beta": "Главная — бета-тестирование",
    "auto": "Автобизнес — бесплатный доступ",
    "beauty": "Красота — бесплатный доступ",
    "health": "Здоровье — бесплатный доступ",
    "spaces": "Аренда пространств — бесплатный доступ",
    "education": "Образование — бесплатный доступ",
    "pets": "Груминг-салоны — бесплатный доступ",
}
SOURCE_PATHS = {
    "home": "/",
    "beta": "/#beta",
    "auto": "/auto",
    "beauty": "/beauty",
    "health": "/health",
    "spaces": "/spaces",
    "education": "/education",
    "pets": "/pets",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _db_path() -> Path:
    return Path(os.getenv("LEADS_DB_PATH", SITE_ROOT / ".leads-data" / "leads.sqlite3"))


def _policy_path() -> Path:
    return Path(os.getenv("LEADS_POLICY_PATH", SITE_ROOT / "privacy.html"))


def _connect() -> sqlite3.Connection:
    path = _db_path()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
    except FileExistsError:
        pass
    else:
        os.close(fd)
    connection = sqlite3.connect(path, timeout=5)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    with closing(_connect()) as connection, connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS consent_documents (
                sha256 TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                html TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS leads (
                id TEXT PRIMARY KEY,
                received_at_utc TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                source_slug TEXT NOT NULL DEFAULT 'home',
                form_name TEXT NOT NULL DEFAULT 'Главная — бесплатный доступ',
                consent_checked INTEGER NOT NULL CHECK (consent_checked = 1),
                consent_text TEXT NOT NULL,
                consent_document_sha256 TEXT NOT NULL REFERENCES consent_documents(sha256),
                telegram_sent_at_utc TEXT,
                telegram_attempts INTEGER NOT NULL DEFAULT 0,
                telegram_last_attempt_at_utc TEXT
            );
            CREATE INDEX IF NOT EXISTS leads_pending_telegram
            ON leads(telegram_sent_at_utc, telegram_last_attempt_at_utc);
        """)
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(leads)")}
        if "source_slug" not in columns:
            connection.execute("ALTER TABLE leads ADD COLUMN source_slug TEXT NOT NULL DEFAULT 'home'")
        if "form_name" not in columns:
            connection.execute("ALTER TABLE leads ADD COLUMN form_name TEXT NOT NULL DEFAULT 'Главная — бесплатный доступ'")


def save_lead(lead: dict[str, str]) -> dict[str, str]:
    """Save the accepted application and the exact policy shown at submission."""
    policy_bytes = _policy_path().read_bytes()
    policy_sha256 = hashlib.sha256(policy_bytes).hexdigest()
    policy_html = policy_bytes.decode("utf-8")
    record = {
        "id": uuid.uuid4().hex,
        "received_at_utc": _now(),
        "name": lead["name"],
        "email": lead["email"],
        "phone": lead["phone"],
        "source_slug": lead.get("source_slug", "home"),
        "form_name": lead.get("form_name", FORM_NAMES["home"]),
        "consent_text": CONSENT_TEXT,
        "consent_document_sha256": policy_sha256,
    }
    with closing(_connect()) as connection, connection:
        connection.execute(
            "INSERT OR IGNORE INTO consent_documents (sha256, url, html) VALUES (?, ?, ?)",
            (policy_sha256, POLICY_URL, policy_html),
        )
        connection.execute(
            """INSERT INTO leads
               (id, received_at_utc, name, email, phone, source_slug, form_name,
                consent_checked, consent_text, consent_document_sha256)
               VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?)""",
            (
                record["id"], record["received_at_utc"], record["name"], record["email"],
                record["phone"], record["source_slug"], record["form_name"],
                record["consent_text"], record["consent_document_sha256"],
            ),
        )
    return record


def mark_telegram_attempt(lead_id: str, sent: bool) -> None:
    now = _now()
    with closing(_connect()) as connection, connection:
        connection.execute(
            """UPDATE leads SET telegram_attempts = telegram_attempts + 1,
               telegram_last_attempt_at_utc = ?,
               telegram_sent_at_utc = CASE WHEN ? THEN ? ELSE telegram_sent_at_utc END
               WHERE id = ?""",
            (now, sent, now, lead_id),
        )


def pending_telegram_leads(limit: int = 20) -> list[dict[str, str]]:
    cutoff = (datetime.now(timezone.utc) - timedelta(seconds=60)).isoformat(timespec="seconds")
    with closing(_connect()) as connection:
        rows = connection.execute(
            """SELECT id, received_at_utc, name, email, phone, source_slug, form_name,
                      consent_text, consent_document_sha256
               FROM leads
               WHERE telegram_sent_at_utc IS NULL
                 AND (telegram_last_attempt_at_utc IS NULL OR telegram_last_attempt_at_utc <= ?)
               ORDER BY received_at_utc LIMIT ?""",
            (cutoff, limit),
        ).fetchall()
    return [dict(row) for row in rows]
