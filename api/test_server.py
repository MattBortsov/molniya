import json
import os
import sqlite3
import stat
import tempfile
import threading
import unittest
from pathlib import Path
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from unittest.mock import patch

import leads as lead_store
from server import MolniyaApiHandler, build_decision_request, call_jev, format_public_result, retry_pending_leads_once, send_lead_to_telegram, validate_lead


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
        self.storage = tempfile.TemporaryDirectory()
        self.db_path = Path(self.storage.name) / "leads.sqlite3"
        self.policy_path = Path(self.storage.name) / "privacy.html"
        self.policy_path.write_text("<html>Редакция 1</html>", encoding="utf-8")
        self.env = patch.dict(os.environ, {"LEADS_DB_PATH": str(self.db_path), "LEADS_POLICY_PATH": str(self.policy_path)})
        self.env.start()
        lead_store.init_db()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), MolniyaApiHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.env.stop()
        self.storage.cleanup()

    def stored_leads(self) -> list[sqlite3.Row]:
        with sqlite3.connect(self.db_path) as connection:
            connection.row_factory = sqlite3.Row
            return connection.execute("SELECT * FROM leads ORDER BY received_at_utc").fetchall()

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
        stored = self.stored_leads()
        self.assertEqual(len(stored), 1)
        self.assertEqual((stored[0]["name"], stored[0]["email"], stored[0]["phone"]), ("Анна", "anna@example.com", "+7 (999) 123-45-67"))
        self.assertEqual(stored[0]["consent_checked"], 1)
        self.assertIsNotNone(stored[0]["telegram_sent_at_utc"])
        send.assert_called_once()
        self.assertEqual(send.call_args.args[0]["id"], stored[0]["id"])

    def test_invalid_contact_or_missing_consent_is_rejected(self) -> None:
        payload = {"name": "А", "email": "wrong", "phone": "123", "consent": False}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual(status, 400)
        self.assertIn("error", result)
        send.assert_not_called()
        self.assertEqual(self.stored_leads(), [])

    def test_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Анна", "email": "anna@example.com", "phone": "+79991234567", "consent": True, "source": "auto"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "auto")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Автобизнес — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "auto")

    def test_spaces_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Максим", "email": "maxim@example.com", "phone": "+79991234567", "consent": True, "source": "spaces"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "spaces")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Аренда пространств — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "spaces")

    def test_education_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Елена", "email": "elena@example.com", "phone": "+79991234567", "consent": True, "source": "education"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "education")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Образование — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "education")

    def test_pets_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Мария", "email": "maria@example.com", "phone": "+79991234567", "consent": True, "source": "pets"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "pets")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Груминг-салоны — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "pets")

    def test_unknown_form_source_is_rejected(self) -> None:
        payload = {"name": "Анна", "email": "anna@example.com", "phone": "+79991234567", "consent": True, "source": "unknown"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, _ = self.post_lead(payload)
        self.assertEqual(status, 400)
        self.assertEqual(self.stored_leads(), [])
        send.assert_not_called()

    def test_honeypot_does_not_send(self) -> None:
        payload = {"website": "spam.example"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        send.assert_not_called()
        self.assertEqual(self.stored_leads(), [])

    def test_missing_bot_token_queues_saved_lead(self) -> None:
        payload = {"name": "Анна", "email": "anna@example.com", "phone": "+79991234567", "consent": True}
        with patch("server.rate_limit_allows", return_value=True), patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": ""}):
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(len(self.stored_leads()), 1)
        self.assertIsNone(self.stored_leads()[0]["telegram_sent_at_utc"])

    def test_database_failure_does_not_report_success_or_send(self) -> None:
        payload = {"name": "Анна", "email": "anna@example.com", "phone": "+79991234567", "consent": True}
        with patch("server.rate_limit_allows", return_value=True), patch("server.lead_store.save_lead", side_effect=OSError("disk full")), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual(status, 503)
        self.assertIn("error", result)
        send.assert_not_called()

    def test_telegram_receives_only_validated_contact_fields(self) -> None:
        lead = lead_store.save_lead(validate_lead({"name": "Анна", "email": "anna@example.com", "phone": "+79991234567", "consent": True}))
        with patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_PROXY_URL": "", "OPENROUTER_PROXY_URL": ""}), patch("server.requests.Session") as session_factory:
            session = session_factory.return_value.__enter__.return_value
            session.post.return_value.json.return_value = {"ok": True}
            send_lead_to_telegram(lead)
        self.assertFalse(session.trust_env)
        self.assertEqual(session.post.call_args.kwargs["json"]["chat_id"], -1003993624474)
        message = session.post.call_args.kwargs["json"]["text"]
        self.assertIn("anna@example.com", message)
        self.assertIn("Форма: Главная — бесплатный доступ", message)
        self.assertIn("Страница: https://molniya-tech.ru/", message)
        self.assertIn("Согласие на обработку ПДн: чекбокс отмечен", message)
        self.assertIn("Проверено сервером: " + lead["received_at_utc"], message)
        self.assertIn("Текст чекбокса: Согласен на обработку персональных данных по политике конфиденциальности.", message)
        self.assertIn("Политика: https://molniya-tech.ru/privacy", message)
        self.assertIn("SHA-256 политики: " + lead["consent_document_sha256"], message)
        self.assertIsNone(session.post.call_args.kwargs["proxies"])

    def test_telegram_uses_existing_socks_proxy_when_needed(self) -> None:
        lead = lead_store.save_lead({"name": "Анна", "email": "anna@example.com", "phone": "+79991234567"})
        env = {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_PROXY_URL": "", "OPENROUTER_PROXY_URL": "socks5://user:pass@proxy.example:1080"}
        with patch.dict(os.environ, env), patch("server.requests.Session") as session_factory:
            session = session_factory.return_value.__enter__.return_value
            session.post.return_value.json.return_value = {"ok": True}
            send_lead_to_telegram(lead)
        self.assertEqual(session.post.call_args.kwargs["proxies"], {"https": "socks5h://user:pass@proxy.example:1080"})

    def test_telegram_rejection_keeps_lead_pending(self) -> None:
        payload = {"name": "Анна", "email": "anna@example.com", "phone": "+79991234567", "consent": True}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram", side_effect=ValueError("Telegram rejected")):
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        stored = self.stored_leads()
        self.assertEqual(len(stored), 1)
        self.assertIsNone(stored[0]["telegram_sent_at_utc"])
        self.assertEqual(stored[0]["telegram_attempts"], 1)

    def test_consent_policy_snapshot_survives_policy_change(self) -> None:
        lead = {"name": "Анна", "email": "anna@example.com", "phone": "+79991234567"}
        first = lead_store.save_lead(lead)
        self.policy_path.write_text("<html>Редакция 2</html>", encoding="utf-8")
        second = lead_store.save_lead(lead)
        self.assertNotEqual(first["consent_document_sha256"], second["consent_document_sha256"])
        with sqlite3.connect(self.db_path) as connection:
            snapshots = dict(connection.execute("SELECT sha256, html FROM consent_documents"))
        self.assertEqual(snapshots[first["consent_document_sha256"]], "<html>Редакция 1</html>")
        self.assertEqual(snapshots[second["consent_document_sha256"]], "<html>Редакция 2</html>")
        self.assertEqual(stat.S_IMODE(self.db_path.stat().st_mode), 0o600)

    def test_failed_telegram_delivery_can_be_retried(self) -> None:
        record = lead_store.save_lead({"name": "Анна", "email": "anna@example.com", "phone": "+79991234567"})
        lead_store.mark_telegram_attempt(record["id"], False)
        with sqlite3.connect(self.db_path) as connection:
            connection.execute("UPDATE leads SET telegram_last_attempt_at_utc = '2000-01-01T00:00:00+00:00' WHERE id = ?", (record["id"],))
        with patch("server.send_lead_to_telegram") as send:
            retry_pending_leads_once()
        send.assert_called_once_with(record)
        self.assertEqual(lead_store.pending_telegram_leads(), [])
        self.assertIsNotNone(self.stored_leads()[0]["telegram_sent_at_utc"])


class LeadDatabaseMigrationTests(unittest.TestCase):
    def test_existing_database_gets_source_columns_without_losing_leads(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "leads.sqlite3"
            with sqlite3.connect(db_path) as connection:
                connection.executescript("""
                    CREATE TABLE consent_documents (sha256 TEXT PRIMARY KEY, url TEXT NOT NULL, html TEXT NOT NULL);
                    CREATE TABLE leads (
                        id TEXT PRIMARY KEY, received_at_utc TEXT NOT NULL, name TEXT NOT NULL,
                        email TEXT NOT NULL, phone TEXT NOT NULL, consent_checked INTEGER NOT NULL,
                        consent_text TEXT NOT NULL, consent_document_sha256 TEXT NOT NULL,
                        telegram_sent_at_utc TEXT, telegram_attempts INTEGER NOT NULL DEFAULT 0,
                        telegram_last_attempt_at_utc TEXT
                    );
                    INSERT INTO leads (id, received_at_utc, name, email, phone, consent_checked,
                                       consent_text, consent_document_sha256)
                    VALUES ('existing', '2026-10-02T00:00:00+00:00', 'Анна', 'anna@example.com',
                            '+79991234567', 1, 'Согласен', 'old-hash');
                """)
            with patch.dict(os.environ, {"LEADS_DB_PATH": str(db_path)}):
                lead_store.init_db()
            with sqlite3.connect(db_path) as connection:
                source = connection.execute("SELECT source_slug, form_name FROM leads WHERE id = 'existing'").fetchone()
            self.assertEqual(source, ("home", "Главная — бесплатный доступ"))


if __name__ == "__main__":
    unittest.main()
