"""Local OxGPT HTTP service."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
from pathlib import Path
import signal
import threading
from typing import Any

from .config import Config
from .ollama import Ollama, OllamaError


def configure_logging(log_file: Path) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


class Handler(BaseHTTPRequestHandler):
    ollama = Ollama()
    config: Config

    def _send(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send(200, {"status": "ok", "model": self.config.model})
        else:
            self._send(404, {"error": "Not found"})

    def do_POST(self) -> None:
        if self.path != "/chat":
            self._send(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            message = payload.get("message")
            if not isinstance(message, str) or not message.strip():
                self._send(400, {"error": "message must be a non-empty string"})
                return
            response = self.ollama.generate(self.config.model, message)
            self._send(200, {"response": response})
        except (ValueError, json.JSONDecodeError) as exc:
            self._send(400, {"error": f"Invalid request: {exc}"})
        except OllamaError as exc:
            logging.exception("Ollama generation failed")
            self._send(502, {"error": str(exc)})

    def log_message(self, format: str, *args: object) -> None:
        logging.info(format, *args)


def run(config: Config) -> None:
    configure_logging(config.log_file)
    Handler.config = config
    server = ThreadingHTTPServer((config.host, config.port), Handler)
    server.timeout = 1
    logging.info("OxGPT service listening on %s:%s", config.host, config.port)

    def shutdown(signum: int, _frame: object) -> None:
        logging.info("Received signal %s; stopping service", signum)
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    try:
        server.serve_forever()
    finally:
        server.server_close()
        logging.info("OxGPT service stopped")


def main() -> None:
    """Run the OxGPT service using environment configuration."""
    run(Config.from_environment())


if __name__ == "__main__":
    main()
