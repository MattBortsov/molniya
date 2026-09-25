import unittest

from server import build_decision_request, format_public_result


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


if __name__ == "__main__":
    unittest.main()
