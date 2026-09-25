"""Small same-origin proxy for the Molniya industry-fit decision form."""

from __future__ import annotations

import json
import os
import threading
import time
import urllib.error
import urllib.request
from collections import defaultdict, deque
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


OPENROUTER_URL = "https://openrouter.ai/api/alpha/decisions"
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "typesafe/jev-1.13")
MAX_BODY_BYTES = 4_096
MAX_BUSINESS_LENGTH = 240
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

    request = urllib.request.Request(
        OPENROUTER_URL,
        data=json.dumps(build_decision_request(business), ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://molniya-tech.ru",
            "X-OpenRouter-Title": "Molniya Tech",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        payload = json.loads(response.read().decode("utf-8"))

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


class MolniyaApiHandler(BaseHTTPRequestHandler):
    server_version = "MolniyaApi/1.0"
    sys_version = ""

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _client_ip(self) -> str:
        forwarded = self.headers.get("X-Real-IP", "").strip()
        return forwarded or self.client_address[0]

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok"})
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Не найдено"})

    def do_POST(self) -> None:  # noqa: N802
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

        if payload.get("website"):
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
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, RuntimeError):
            self._send_json(HTTPStatus.BAD_GATEWAY, {"error": "Сервис проверки временно недоступен"})
            return

        self._send_json(HTTPStatus.OK, result)

    def log_message(self, _format: str, *_args: Any) -> None:
        # Intentionally avoid request logs: descriptions may contain business details.
        return


def run() -> None:
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8080"))
    server = ThreadingHTTPServer((host, port), MolniyaApiHandler)
    server.serve_forever()


if __name__ == "__main__":
    run()
