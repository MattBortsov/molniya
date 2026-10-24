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
        self.assertEqual(stored[0]["consent_text"], lead_store.CONSENT_TEXT)
        self.assertEqual(len(stored[0]["consent_document_sha256"]), 64)
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

    def test_beta_application_has_its_own_source_and_form_name(self) -> None:
        payload = {"name": "Анна", "email": "anna@example.com", "phone": "+79991234567", "consent": True, "source": "beta"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        stored = self.stored_leads()[0]
        self.assertEqual(stored["source_slug"], "beta")
        self.assertEqual(stored["form_name"], "Главная — бета-тестирование")
        self.assertEqual(stored["consent_checked"], 1)
        self.assertEqual(send.call_args.args[0]["form_name"], "Главная — бета-тестирование")

    def test_spaces_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Максим", "email": "maxim@example.com", "phone": "+79991234567", "consent": True, "source": "spaces"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "spaces")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Аренда пространств — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "spaces")

    def test_photostudios_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Артем", "email": "artem@example.com", "phone": "+79991234567", "consent": True, "source": "photostudios"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "photostudios")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Фотостудии — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "photostudios")

    def test_quests_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Роман", "email": "roman@example.com", "phone": "+79991234567", "consent": True, "source": "quests"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "quests")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Квесты и перформансы — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "quests")

    def test_vr_arena_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Павел", "email": "pavel@example.com", "phone": "+79991234567", "consent": True, "source": "vr-arena"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "vr-arena")
        self.assertEqual(self.stored_leads()[0]["form_name"], "VR-арены и клубы — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "vr-arena")

    def test_karting_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Илья", "email": "ilya@example.com", "phone": "+79991234567", "consent": True, "source": "karting"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "karting")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Картинг-центры — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "karting")

    def test_anticafe_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Артем", "email": "artem@example.com", "phone": "+79991234567", "consent": True, "source": "anticafe"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "anticafe")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Антикафе и тайм-клубы — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "anticafe")

    def test_saunas_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Владимир", "email": "vladimir@example.com", "phone": "+79991234567", "consent": True, "source": "saunas"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "saunas")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Бани и сауны — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "saunas")

    def test_glamping_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Егор", "email": "egor@example.com", "phone": "+79991234567", "consent": True, "source": "glamping"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "glamping")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Глэмпинги и беседки — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "glamping")

    def test_furniture_cleaning_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Максим", "email": "maxim@example.com", "phone": "+79991234567", "consent": True, "source": "furniture-cleaning"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "furniture-cleaning")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Химчистка мебели — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "furniture-cleaning")

    def test_window_cleaning_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Сергей", "email": "sergey@example.com", "phone": "+79991234567", "consent": True, "source": "window-cleaning"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "window-cleaning")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Мойка окон — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "window-cleaning")

    def test_pest_control_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Андрей", "email": "andrey@example.com", "phone": "+79991234567", "consent": True, "source": "pest-control"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "pest-control")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Дезинсекция и СЭС — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "pest-control")

    def test_cleaning_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Ольга", "email": "olga@example.com", "phone": "+79991234567", "consent": True, "source": "cleaning"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "cleaning")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Клининг — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "cleaning")

    def test_psychologist_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Дарья", "email": "daria@example.com", "phone": "+79991234567", "consent": True, "source": "psychologist"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "psychologist")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Психологи — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "psychologist")

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

    def test_repair_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Артем", "email": "artem@example.com", "phone": "+79991234567", "consent": True, "source": "repair"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "repair")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Ремонт и сервис — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "repair")

    def test_pricing_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Дмитрий", "email": "dmitry@example.com", "phone": "+79991234567", "consent": True, "source": "pricing"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "pricing")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Тарифы — заявка на подключение")
        self.assertEqual(send.call_args.args[0]["source_slug"], "pricing")

    def test_dikidi_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Оксана", "email": "oksana@example.com", "phone": "+79991234567", "consent": True, "source": "dikidi"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "dikidi")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Переход с DIKIDI — 3 месяца бесплатно")
        self.assertEqual(send.call_args.args[0]["source_slug"], "dikidi")

    def test_yclients_sector_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Игорь", "email": "igor@example.com", "phone": "+79991234567", "consent": True, "source": "yclients"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "yclients")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Переход с YCLIENTS — 3 месяца бесплатно")
        self.assertEqual(send.call_args.args[0]["source_slug"], "yclients")

    def test_about_page_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Елена", "email": "elena@example.com", "phone": "+79991234567", "consent": True, "source": "about"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "about")
        self.assertEqual(self.stored_leads()[0]["form_name"], "О компании — заявка на подключение")
        self.assertEqual(send.call_args.args[0]["source_slug"], "about")

    def test_salary_tool_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Илья", "email": "ilya@example.com", "phone": "+79991234567", "consent": True, "source": "salary"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "salary")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Калькулятор зарплат — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "salary")

    def test_pricelist_tool_source_is_saved_and_sent(self) -> None:
        payload = {"name": "Мария", "email": "maria@example.com", "phone": "+79991234567", "consent": True, "source": "pricelist"}
        with patch("server.rate_limit_allows", return_value=True), patch("server.send_lead_to_telegram") as send:
            status, result = self.post_lead(payload)
        self.assertEqual((status, result), (200, {"ok": True}))
        self.assertEqual(self.stored_leads()[0]["source_slug"], "pricelist")
        self.assertEqual(self.stored_leads()[0]["form_name"], "Конструктор прайс-листов — бесплатный доступ")
        self.assertEqual(send.call_args.args[0]["source_slug"], "pricelist")

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
        payload = session.post.call_args.kwargs["json"]
        self.assertEqual(payload["chat_id"], -1003993624474)
        self.assertEqual(payload["parse_mode"], "HTML")
        message = payload["text"]
        self.assertIn("<b>Заявка №" + lead["id"][:8].upper() + "</b>", message)
        self.assertIn("<b>Информация о клиенте:</b>", message)
        self.assertIn("Имя: Анна", message)
        self.assertIn("Телефон: +79991234567", message)
        self.assertIn("anna@example.com", message)
        self.assertIn("<b>Дополнительная информация:</b>", message)
        self.assertIn("Код заявки: <code>" + lead["id"] + "</code>", message)
        self.assertIn("Форма: Главная — бесплатный доступ", message)
        self.assertIn('<a href="https://molniya-tech.ru/">https://molniya-tech.ru/</a>', message)
        self.assertNotIn("Согласие на обработку ПДн", message)
        self.assertNotIn("Проверено сервером", message)
        self.assertNotIn("Текст чекбокса", message)
        self.assertNotIn(lead_store.POLICY_URL, message)
        self.assertNotIn(lead["consent_document_sha256"], message)
        self.assertIsNone(session.post.call_args.kwargs["proxies"])

    def test_telegram_escapes_contact_fields_in_html_message(self) -> None:
        lead = lead_store.save_lead(validate_lead({"name": "Анна <VIP>", "email": "anna+vip@example.com", "phone": "+79991234567", "consent": True}))
        with patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_PROXY_URL": "", "OPENROUTER_PROXY_URL": ""}), patch("server.requests.Session") as session_factory:
            session = session_factory.return_value.__enter__.return_value
            session.post.return_value.json.return_value = {"ok": True}
            send_lead_to_telegram(lead)
        message = session.post.call_args.kwargs["json"]["text"]
        self.assertIn("Имя: Анна &lt;VIP&gt;", message)
        self.assertNotIn("Анна <VIP>", message)

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


class WeatherEndpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), MolniyaApiHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def test_weather_cities_list(self) -> None:
        connection = HTTPConnection("127.0.0.1", self.server.server_port, timeout=2)
        connection.request("GET", "/api/weather/cities")
        response = connection.getresponse()
        self.assertEqual(response.status, 200)
        data = json.loads(response.read().decode("utf-8"))
        connection.close()
        self.assertIn("cities", data)
        self.assertGreaterEqual(len(data["cities"]), 20)
        slugs = [c["slug"] for c in data["cities"]]
        self.assertIn("msk", slugs)
        self.assertIn("spb", slugs)

    def test_compute_wash_index_sunny_vs_rainy(self) -> None:
        from server import compute_wash_index

        sunny_forecast = {
            "daily": {
                "time": ["2026-10-24", "2026-10-25", "2026-10-26", "2026-10-27", "2026-10-28"],
                "weathercode": [0, 1, 0, 0, 1],
                "temperature_2m_max": [18.0, 19.0, 17.0, 18.0, 19.0],
                "temperature_2m_min": [9.0, 10.0, 8.0, 9.0, 10.0],
                "precipitation_sum": [0.0, 0.0, 0.0, 0.0, 0.0],
                "precipitation_probability_max": [0, 5, 0, 0, 10],
                "windspeed_10m_max": [8.0, 10.0, 9.0, 7.0, 8.0],
            },
            "current_weather": {"temperature": 18.0, "weathercode": 0},
        }
        res_sunny = compute_wash_index(sunny_forecast, "Москва", "msk")
        self.assertGreaterEqual(res_sunny["score"], 80)
        self.assertEqual(res_sunny["status"], "perfect")
        self.assertIn("wash-perfect.webp", res_sunny["image"])

        rainy_forecast = {
            "daily": {
                "time": ["2026-10-24", "2026-10-25", "2026-10-26", "2026-10-27", "2026-10-28"],
                "weathercode": [65, 81, 63, 61, 80],
                "temperature_2m_max": [11.0, 9.0, 8.0, 10.0, 11.0],
                "temperature_2m_min": [6.0, 5.0, 4.0, 5.0, 6.0],
                "precipitation_sum": [15.0, 20.0, 8.0, 5.0, 3.0],
                "precipitation_probability_max": [95, 90, 85, 70, 60],
                "windspeed_10m_max": [25.0, 30.0, 20.0, 15.0, 12.0],
            },
            "current_weather": {"temperature": 10.0, "weathercode": 65},
        }
        res_rainy = compute_wash_index(rainy_forecast, "Санкт-Петербург", "spb")
        self.assertLess(res_rainy["score"], 35)
        self.assertEqual(res_rainy["status"], "disaster")
        self.assertIn("wash-disaster.webp", res_rainy["image"])

    def test_weather_endpoint_with_mocked_fetch(self) -> None:
        mock_data = {
            "city_slug": "msk",
            "city_name": "Москва",
            "score": 88,
            "status": "perfect",
            "verdict": "Идеально! Мой на все деньги",
            "tagline": "Впереди сухие чистые дни.",
            "image": "/assets/img/carwash/wash-perfect.webp",
            "badge_text": "Зеленый свет",
            "badge_color": "#2E7D32",
            "days": [],
        }
        with patch("server.fetch_weather_data", return_value=mock_data):
            connection = HTTPConnection("127.0.0.1", self.server.server_port, timeout=2)
            connection.request("GET", "/api/weather?city=msk")
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            data = json.loads(response.read().decode("utf-8"))
            connection.close()
            self.assertEqual(data["score"], 88)
            self.assertEqual(data["status"], "perfect")


if __name__ == "__main__":
    unittest.main()
