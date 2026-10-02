"""Small same-origin proxy for the Molniya industry-fit decision form."""

from __future__ import annotations

import json
import hashlib
import hmac
import os
import re
import sqlite3
import threading
import time
from collections import defaultdict, deque
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlsplit

import requests

if __package__:
    from . import blog as blog_store, leads as lead_store
else:
    import blog as blog_store
    import leads as lead_store


OPENROUTER_URL = "https://openrouter.ai/api/alpha/decisions"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "typesafe/jev-1.13")
MAX_BODY_BYTES = 4_096
MAX_WEBHOOK_BYTES = 2_000_000
MAX_BUSINESS_LENGTH = 240
MAX_LEAD_BODY_BYTES = 2_048
TELEGRAM_LEADS_CHAT_ID = "-1003993624474"
RATE_WINDOW_SECONDS = 60
RATE_REQUESTS = 8

_requests_by_ip: dict[str, deque[float]] = defaultdict(deque)
_rate_lock = threading.Lock()


def build_decision_request(business: str) -> dict[str, Any]:
    """Build a typed Jev choice request. User text remains state, never instructions."""
    return {
        "model": OPENROUTER_MODEL,
        "state": business,
        "questions": {
            "fit": {
                "type": "choice",
                "instructions": (
                    "Определи, насколько Молния подходит организации из описания. "
                    "Молния управляет онлайн-записью, расписанием сотрудников или рабочих мест, "
                    "услугами и ценами, этапами выполнения, клиентской базой, филиалами, "
                    "аналитикой и расчётом зарплаты."
                ),
                "criteria": {
                    "fit": (
                        "Организация оказывает услуги клиентам, работает по записи или расписанию "
                        "и управляет сотрудниками, рабочими местами либо этапами выполнения услуг."
                    ),
                    "clarify": (
                        "Организация может оказывать услуги, но в описании недостаточно информации "
                        "о записи, расписании, ресурсах или процессе обслуживания."
                    ),
                    "not_fit": (
                        "Основная деятельность не связана с оказанием услуг клиентам по записи, "
                        "расписанию или управляемому процессу выполнения."
                    ),
                },
            }
        },
    }


def format_public_result(choice: str, confidence: float) -> dict[str, Any]:
    """Turn Jev's typed answer into deterministic user-facing copy."""
    if confidence < 0.58 or choice == "clarify":
        return {
            "status": "clarify",
            "title": "Похоже, Молния может подойти",
            "message": (
                "Нужно чуть больше деталей о записи клиентов, расписании команды "
                "или рабочих местах. Мы быстро разберём ваш сценарий на консультации."
            ),
            "confidence": round(confidence, 3),
        }
    if choice == "fit":
        return {
            "status": "fit",
            "title": "Да, Молния подходит вашей сфере",
            "message": (
                "Можно связать запись, расписание, услуги, сотрудников, клиентов "
                "и финансовые показатели в одном рабочем процессе."
            ),
            "confidence": round(confidence, 3),
        }
    return {
        "status": "not_fit",
        "title": "Нужна короткая консультация",
        "message": (
            "Описанный сценарий не похож на основной формат Молнии, но мы проверим, "
            "можно ли адаптировать систему под вашу работу."
        ),
        "confidence": round(confidence, 3),
    }


def call_jev(business: str) -> dict[str, Any]:
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not configured")

    proxy_url = os.getenv("OPENROUTER_PROXY_URL", "").strip()
    if proxy_url.startswith("socks5://"):
        proxy_url = "socks5h://" + proxy_url.removeprefix("socks5://")
    proxies = {"https": proxy_url} if proxy_url else None

    with requests.Session() as session:
        session.trust_env = False
        response = session.post(
            OPENROUTER_URL,
            json=build_decision_request(business),
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://molniya-tech.ru",
                "X-OpenRouter-Title": "Molniya Tech",
            },
            proxies=proxies,
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()

    answer = payload.get("answers", {}).get("fit", {})
    choice = answer.get("choice")
    confidence = answer.get("confidence")
    if choice not in {"fit", "clarify", "not_fit"} or not isinstance(confidence, (int, float)):
        raise ValueError("Unexpected Jev response")
    return format_public_result(choice, float(confidence))


def rate_limit_allows(ip_address: str, now: float | None = None) -> bool:
    current = now if now is not None else time.monotonic()
    with _rate_lock:
        bucket = _requests_by_ip[ip_address]
        cutoff = current - RATE_WINDOW_SECONDS
        while bucket and bucket[0] <= cutoff:
            bucket.popleft()
        if len(bucket) >= RATE_REQUESTS:
            return False
        bucket.append(current)
        return True


def validate_lead(payload: Any) -> dict[str, str]:
    """Accept only the three contact fields needed to reply to an applicant."""
    if not isinstance(payload, dict) or payload.get("consent") is not True:
        raise ValueError("Подтвердите согласие на обработку данных")

    fields: dict[str, str] = {}
    for key in ("name", "email", "phone"):
        value = payload.get(key)
        if not isinstance(value, str):
            raise ValueError("Заполните имя, почту и телефон")
        fields[key] = " ".join(value.split())

    name, email, phone = fields["name"], fields["email"], fields["phone"]
    if not 2 <= len(name) <= 80 or any(ord(char) < 32 for char in name):
        raise ValueError("Укажите имя от 2 до 80 символов")
    if len(email) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        raise ValueError("Укажите корректную почту")
    if len(phone) > 32 or not re.fullmatch(r"\+?[\d\s().-]+", phone) or not 10 <= sum(char.isdigit() for char in phone) <= 15:
        raise ValueError("Укажите корректный телефон")
    return fields


def send_lead_to_telegram(lead: dict[str, str]) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Telegram bot is not configured")

    proxy_url = os.getenv("TELEGRAM_PROXY_URL", "").strip() or os.getenv("OPENROUTER_PROXY_URL", "").strip()
    if proxy_url.startswith("socks5://"):
        proxy_url = "socks5h://" + proxy_url.removeprefix("socks5://")
    proxies = {"https": proxy_url} if proxy_url else None

    text = (
        "Новая заявка с molniya-tech.ru\n"
        f"ID: {lead['id']}\n"
        f"Имя: {lead['name']}\n"
        f"Почта: {lead['email']}\n"
        f"Телефон: {lead['phone']}\n"
        "Согласие на обработку ПДн: чекбокс отмечен\n"
        f"Проверено сервером: {lead['received_at_utc']}\n"
        f"Текст чекбокса: {lead['consent_text']}\n"
        f"Политика: {lead_store.POLICY_URL}\n"
        f"SHA-256 политики: {lead['consent_document_sha256']}"
    )
    with requests.Session() as session:
        session.trust_env = False
        response = session.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": int(os.getenv("TELEGRAM_LEADS_CHAT_ID", TELEGRAM_LEADS_CHAT_ID)), "text": text},
            proxies=proxies,
            timeout=8,
        )
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict) or result.get("ok") is not True:
            raise ValueError("Telegram rejected the message")


def deliver_lead_notification(record: dict[str, str]) -> None:
    try:
        send_lead_to_telegram(record)
    except (RuntimeError, requests.RequestException, ValueError):
        sent = False
    else:
        sent = True
    try:
        lead_store.mark_telegram_attempt(record["id"], sent)
    except (OSError, sqlite3.Error):
        # The saved application remains pending for the retry worker.
        pass


class MolniyaApiHandler(BaseHTTPRequestHandler):
    server_version = "MolniyaApi/1.0"
    sys_version = ""

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        self._send(status, json.dumps(payload, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def _client_ip(self) -> str:
        forwarded = self.headers.get("X-Real-IP", "").strip()
        return forwarded or self.client_address[0]

    def do_GET(self) -> None:  # noqa: N802
        path = urlsplit(self.path).path
        if path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
            return
        if path in {"/blog", "/blog/", "/blog/index.html"}:
            self._send(HTTPStatus.OK, (blog_store.DATA_DIR / "index.html").read_bytes(), "text/html; charset=utf-8")
            return
        if path == "/sitemap.xml":
            self._send(HTTPStatus.OK, (blog_store.DATA_DIR / "sitemap.xml").read_bytes(), "application/xml; charset=utf-8")
            return
        if path.startswith("/blog/"):
            slug = path.removeprefix("/blog/")
            if blog_store.SLUG_RE.fullmatch(slug):
                page = blog_store.DATA_DIR / f"{slug}.html"
                if page.is_file():
                    self._send(HTTPStatus.OK, page.read_bytes(), "text/html; charset=utf-8")
                    return
                target = blog_store.redirect_target(slug)
                if target:
                    self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                    self.send_header("Location", f"/blog/{target}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Не найдено"})

    def do_POST(self) -> None:  # noqa: N802
        if urlsplit(self.path).path == "/api/seosmith":
            self._handle_seosmith()
            return
        if urlsplit(self.path).path == "/api/lead":
            self._handle_lead()
            return
        if self.path != "/api/industry-fit":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Не найдено"})
            return

        if not rate_limit_allows(self._client_ip()):
            self._send_json(HTTPStatus.TOO_MANY_REQUESTS, {"error": "Слишком много запросов"})
            return

        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            self._send_json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "Ожидается JSON"})
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0 or content_length > MAX_BODY_BYTES:
            self._send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "Некорректный размер запроса"})
            return

        try:
            raw_payload = self.rfile.read(content_length)
            payload = json.loads(raw_payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Некорректный JSON"})
            return

        if not isinstance(payload, dict) or payload.get("website"):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Некорректный запрос"})
            return

        business = payload.get("business")
        if not isinstance(business, str):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Опишите сферу бизнеса"})
            return
        business = " ".join(business.split())
        if not 3 <= len(business) <= MAX_BUSINESS_LENGTH:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Описание должно содержать от 3 до 240 символов"})
            return

        try:
            result = call_jev(business)
        except (requests.RequestException, ValueError, RuntimeError):
            self._send_json(HTTPStatus.BAD_GATEWAY, {"error": "Сервис проверки временно недоступен"})
            return

        self._send_json(HTTPStatus.OK, result)

    def _handle_lead(self) -> None:
        if not rate_limit_allows("lead:" + self._client_ip()):
            self._send_json(HTTPStatus.TOO_MANY_REQUESTS, {"error": "Слишком много заявок. Попробуйте позже."})
            return
        if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
            self._send_json(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "Ожидается JSON"})
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0 or content_length > MAX_LEAD_BODY_BYTES:
            self._send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "Некорректный размер запроса"})
            return
        try:
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Некорректный JSON"})
            return
        if isinstance(payload, dict) and payload.get("website"):
            self._send_json(HTTPStatus.OK, {"ok": True})
            return
        try:
            lead = validate_lead(payload)
        except ValueError as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        try:
            record = lead_store.save_lead(lead)
        except (OSError, sqlite3.Error, UnicodeError):
            self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "Не удалось сохранить заявку. Попробуйте позже."})
            return
        deliver_lead_notification(record)
        self._send_json(HTTPStatus.OK, {"ok": True})

    def _handle_seosmith(self) -> None:
        secret = os.getenv("SEOSMITH_WEBHOOK_SECRET", "")
        if not secret:
            self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "Webhook не настроен"})
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        if content_length <= 0 or content_length > MAX_WEBHOOK_BYTES:
            self._send_json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "Некорректный размер запроса"})
            return
        raw_body = self.rfile.read(content_length)
        signature = self.headers.get("X-SeoSmith-Signature", "")
        expected = "sha256=" + hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected):
            self._send_json(HTTPStatus.UNAUTHORIZED, {"error": "Неверная подпись"})
            return
        try:
            payload = json.loads(raw_body)
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Некорректный JSON"})
            return
        if not isinstance(payload, dict):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "Некорректный запрос"})
            return
        if payload.get("event") != "article.published":
            self._send_json(HTTPStatus.OK, {"ok": True, "skipped": True})
            return
        try:
            article = blog_store.validate_article(payload.get("article"))
            blog_store.upsert_article(article)
        except ValueError as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        except OSError:
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Не удалось сохранить статью"})
            return
        self._send_json(HTTPStatus.OK, {"ok": True})

    def log_message(self, _format: str, *_args: Any) -> None:
        # Intentionally avoid request logs: descriptions may contain business details.
        return


def run() -> None:
    blog_store.rebuild_public()
    lead_store.init_db()
    threading.Thread(target=_retry_pending_leads, daemon=True, name="telegram-lead-retry").start()
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8080"))
    server = ThreadingHTTPServer((host, port), MolniyaApiHandler)
    server.serve_forever()


def _retry_pending_leads() -> None:
    while True:
        time.sleep(60)
        try:
            retry_pending_leads_once()
        except (OSError, sqlite3.Error):
            continue


def retry_pending_leads_once() -> None:
    for record in lead_store.pending_telegram_leads():
        deliver_lead_notification(record)


if __name__ == "__main__":
    run()
