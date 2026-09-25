"""Local Molniya server: static files and the Jev API on one origin."""

from __future__ import annotations

import argparse
import os
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit


PROJECT_ROOT = Path(__file__).resolve().parent


def load_local_env(path: Path) -> None:
    """Load a small KEY=VALUE file without an external dependency."""
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"").strip("'")
        if key:
            os.environ.setdefault(key, value)


load_local_env(PROJECT_ROOT / ".env")

from api.server import MolniyaApiHandler  # noqa: E402


class DevHandler(MolniyaApiHandler, SimpleHTTPRequestHandler):
    """Serve project files while keeping secrets and source internals private."""

    def do_GET(self) -> None:  # noqa: N802
        request_path = urlsplit(self.path).path
        parts = PurePosixPath(request_path).parts

        if request_path == "/health":
            MolniyaApiHandler.do_GET(self)
            return
        if request_path.startswith("/api/") or any(part.startswith(".") for part in parts):
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Не найдено"})
            return
        SimpleHTTPRequestHandler.do_GET(self)

    def translate_path(self, path: str) -> str:
        relative = super().translate_path(path)
        return str(PROJECT_ROOT / Path(relative).relative_to(Path.cwd()))


def run() -> None:
    parser = argparse.ArgumentParser(description="Run Molniya locally with the Jev API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    os.chdir(PROJECT_ROOT)
    server = ThreadingHTTPServer((args.host, args.port), DevHandler)
    print(f"Molniya is available at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
