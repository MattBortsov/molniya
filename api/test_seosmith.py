import hashlib
import hmac
import http.client
import json
import os
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest.mock import patch

import blog
from server import MolniyaApiHandler


class SeoSmithWebhookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        patcher = patch.object(blog, "DATA_DIR", Path(self.directory.name))
        patcher.start()
        self.addCleanup(patcher.stop)
        for name, path in (("RECORDS_DIR", Path(self.directory.name) / ".records"), ("REDIRECTS_PATH", Path(self.directory.name) / ".redirects.json")):
            path_patcher = patch.object(blog, name, path)
            path_patcher.start()
            self.addCleanup(path_patcher.stop)
        blog.rebuild_public()
        env = patch.dict(os.environ, {"SEOSMITH_WEBHOOK_SECRET": "test-secret"})
        env.start()
        self.addCleanup(env.stop)
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), MolniyaApiHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def post(self, payload, signed=True):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        signature = "sha256=" + hmac.new(b"test-secret", body, hashlib.sha256).hexdigest()
        request = Request(
            self.base_url + "/api/seosmith",
            data=body,
            headers={"Content-Type": "application/json", "X-SeoSmith-Signature": signature if signed else "sha256=invalid"},
            method="POST",
        )
        try:
            with urlopen(request) as response:
                return response.status, json.load(response)
        except HTTPError as response:
            return response.code, json.load(response)

    def get(self, path):
        with urlopen(self.base_url + path) as response:
            return response.read().decode("utf-8")

    def test_signature_publish_and_repeat_update(self):
        payload = {
            "event": "article.published",
            "company": {"name": "Молния", "site_url": "https://molniya-tech.ru"},
            "article": {
                "id": "article-1", "slug": "first-post", "title": "Первый пост", "url": "https://molniya-tech.ru/blog/first-post",
                "short_answer": "Краткий ответ", "insights": ["Первый вывод"],
                "body_html": "<h2>Исходный текст</h2>",
                "meta": {"title": "SEO заголовок", "description": "Описание", "keywords": "блог, молния"},
                "faq": [{"question": "Вопрос", "answer": "Ответ"}],
                "json_ld": {"@type": "Article", "headline": "Первый пост"},
            },
        }
        self.assertEqual(self.post(payload, signed=False)[0], 401)
        self.assertEqual(list(blog.RECORDS_DIR.glob("*.json")), [])
        self.assertEqual(self.post(payload), (200, {"ok": True}))
        page = self.get("/blog/first-post")
        self.assertIn("<h2>Исходный текст</h2>", page)
        self.assertIn("Короткий ответ", page)
        self.assertIn("Главное из статьи", page)
        self.assertIn("SEO заголовок", page)
        self.assertIn("/blog/first-post", self.get("/blog"))
        self.assertIn("/blog/first-post", self.get("/sitemap.xml"))
        self.assertIn("Исходный текст", (blog.DATA_DIR / "first-post.html").read_text(encoding="utf-8"))

        payload["article"]["slug"] = "updated-post"
        payload["article"]["title"] = "Обновлённый пост"
        payload["article"]["body_html"] = "<p>Новый текст</p>"
        self.assertEqual(self.post(payload), (200, {"ok": True}))
        self.assertEqual(len(list(blog.RECORDS_DIR.glob("*.json"))), 1)
        self.assertFalse((blog.DATA_DIR / "first-post.html").exists())
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port)
        connection.request("GET", "/blog/first-post")
        response = connection.getresponse()
        self.assertEqual(response.status, 301)
        self.assertEqual(response.getheader("Location"), "/blog/updated-post")
        connection.close()
        self.assertIn("<p>Новый текст</p>", self.get("/blog/updated-post"))
        self.assertIn("Обновлённый пост", self.get("/blog"))
        self.assertNotIn("/blog/first-post", self.get("/blog"))

        payload["article"]["id"] = "new-source-id"
        self.assertEqual(self.post(payload), (200, {"ok": True}))
        self.assertEqual(len(list(blog.RECORDS_DIR.glob("*.json"))), 1)

    def test_other_event_is_skipped_only_with_valid_signature(self):
        payload = {"event": "article.draft"}
        self.assertEqual(self.post(payload, signed=False)[0], 401)
        self.assertEqual(self.post(payload), (200, {"ok": True, "skipped": True}))

    def test_startup_migrates_previous_records_and_rebuilds_static_pages(self):
        article = blog.validate_article({
            "id": 12, "slug": "saved-post", "title": "Сохранённая статья",
            "body_html": "<p>Текст после перезапуска</p>",
        })
        legacy = blog.DATA_DIR / "legacy.json"
        legacy.write_text(json.dumps(article, ensure_ascii=False), encoding="utf-8")

        blog.rebuild_public()

        self.assertFalse(legacy.exists())
        self.assertTrue((blog.RECORDS_DIR / "legacy.json").is_file())
        self.assertIn("Текст после перезапуска", (blog.DATA_DIR / "saved-post.html").read_text(encoding="utf-8"))
        self.assertIn("/blog/saved-post", (blog.DATA_DIR / "index.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
