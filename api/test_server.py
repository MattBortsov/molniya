import os
import unittest
from unittest.mock import patch

from server import build_decision_request, call_jev, format_public_result


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


if __name__ == "__main__":
    unittest.main()
