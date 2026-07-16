"""HTTP client for the local OxGPT service."""

from http.client import HTTPConnection
import json

from .config import Config


class ServiceError(RuntimeError):
    """Raised when the OxGPT service cannot be reached."""


def health_check(config: Config, timeout: float = 2) -> bool:
    try:
        connection = HTTPConnection(config.host, config.port, timeout=timeout)
        connection.request("GET", "/health")
        response = connection.getresponse()
        return response.status == 200
    except OSError:
        return False


def chat(config: Config, message: str, timeout: float = 600) -> str:
    try:
        connection = HTTPConnection(config.host, config.port, timeout=timeout)
        body = json.dumps({"message": message})
        connection.request(
            "POST",
            "/chat",
            body=body,
            headers={"Content-Type": "application/json"},
        )
        response = connection.getresponse()
        payload = json.loads(response.read())
    except (OSError, json.JSONDecodeError) as exc:
        raise ServiceError("OxGPT service is not available. Run `oxgpt start`.") from exc
    if response.status != 200:
        raise ServiceError(payload.get("error", "The service returned an error."))
    return payload["response"]
