import json
import os
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from unittest.mock import patch

from server import MolniyaApiHandler, build_decision_request, call_jev, format_public_result, send_lead_to_telegram, validate_lead


class IndustryFitTests(unittest.TestCase):
    def test_user_text_is_kept_in_state(self) -> None:
        payload = build_decision_request("Моя сфера услуг")
        self.assertEqual(payload["state"], "Моя сфера услуг")
        self.assertEqual(payload["questions"]["fit"]["type"], "choice")

    def test_low_confidence_requires_clarification(self) -> None:
        result = format_public_result("fit", 0.4)
        self.assertEqual(result["status"], "clarify")

    def test_confident_fit_is_positive(self) -> None:
        result = format_public_result("fit", 0.92)
        self.assertEqual(result["status"], "fit")

    def test_non_fit_does_not_overpromise(self) -> None:
        result = format_public_result("not_fit", 0.9)
        self.assertEqual(result["status"], "not_fit")

    def test_jev_uses_configured_socks_proxy(self) -> None:
        env = {"OPENROUTER_API_KEY": "test-key", "OPENROUTER_PROXY_URL": "socks5://user:pass@proxy.example:1080"}
        with patch.dict(os.environ, env), patch("server.requests.Session") as session_factory:
            session = session_factory.return_value.__enter__.return_value
            session.post.return_value.json.return_value = {
                "answers": {"fit": {"choice": "fit", "confidence": 0.9}}
            }

            result = call_jev("Студия услуг")

            self.assertEqual(result["status"], "fit")
            self.assertFalse(session.trust_env)
            self.assertEqual(
                session.post.call_args.kwargs["proxies"],
                {"https": "socks5h://user:pass@proxy.example:1080"},
            )


class LeadFormTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), MolniyaApiHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def post_lead(self, payload: dict) -> tuple[int, dict]:
        connection = HTTPConnection("127.0.0.1", self.server.server_port, timeout=2)
        connection.request("POST", "/api/lead", body=json.dumps(payload), headers={"Content-Type": "application/json"})
        response = connection.getresponse()
        result = response.status, json.loads(response.read())
        connection.close()
        return result

    def test_valid_lead_is_sent_once(self) -> None:
        payload = {"name": "  Анна  ", "email": "anna@example.com", "phone": "+7 (999) 123-45-67", "consent": True, "website": ""}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        send.assert_called_once_with({"name": "Анна", "email": "anna@example.com", "phone": "+7 (999) 123-45-67"})

    def test_invalid_contact_or_missing_consent_is_rejected(self) -> None:
        payload = {"name": "А", "email": "wrong", "phone": "123", "consent": False}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual(status, 400)
        self.assertIn("error", result)
        send.assert_not_called()

    def test_honeypot_does_not_send(self) -> None:
        payload = {"website": "spam.example"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        send.assert_not_called()

    def test_missing_bot_token_does_not_report_success(self) -> None:
        payload = {"name": "Анна", "email": "anna@example.com", "phone": "+79991234567", "consent": True}
        with patch("server.rate_limit_allows", return_value=True), patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": ""}):
            status, result = self.post_lead(payload)
        self.assertEqual(status, 503)
        self.assertIn("error", result)

    def test_telegram_receives_only_validated_contact_fields(self) -> None:
        lead = validate_lead({"name": "Анна", "email": "anna@example.com", "phone": "+79991234567", "consent": True})
        with patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_PROXY_URL": "", "OPENROUTER_PROXY_URL": ""}), patch("server.requests.Session") as session_factory:
            session = session_factory.return_value.__enter__.return_value
            session.post.return_value.json.return_value = {"ok": True}
            send_lead_to_telegram(lead)
        self.assertFalse(session.trust_env)
        self.assertEqual(session.post.call_args.kwargs["json"]["chat_id"], -1003993624474)
        message = session.post.call_args.kwargs["json"]["text"]
        self.assertIn("anna@example.com", message)
        self.assertIn("Согласие на обработку ПДн: чекбокс отмечен", message)
        self.assertRegex(message, r"Проверено сервером: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC")
        self.assertIn("Текст чекбокса: Согласен на обработку персональных данных по политике конфиденциальности.", message)
        self.assertIn("Политика: https://molniya-tech.ru/privacy", message)
        self.assertIsNone(session.post.call_args.kwargs["proxies"])

    def test_telegram_uses_existing_socks_proxy_when_needed(self) -> None:
        lead = {"name": "Анна", "email": "anna@example.com", "phone": "+79991234567"}
        env = {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_PROXY_URL": "", "OPENROUTER_PROXY_URL": "socks5://user:pass@proxy.example:1080"}
        with patch.dict(os.environ, env), patch("server.requests.Session") as session_factory:
            session = session_factory.return_value.__enter__.return_value
            session.post.return_value.json.return_value = {"ok": True}
            send_lead_to_telegram(lead)
        self.assertEqual(session.post.call_args.kwargs["proxies"], {"https": "socks5h://user:pass@proxy.example:1080"})

    def test_telegram_rejection_is_not_reported_as_success(self) -> None:
        payload = {"name": "Анна", "email": "anna@example.com", "phone": "+79991234567", "consent": True}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram", side_effect=ValueError("Telegram rejected")):
            status, result = self.post_lead(payload)
        self.assertEqual(status, 502)
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
