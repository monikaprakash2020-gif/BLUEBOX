"""Small, dependency-free wrapper around the Ollama CLI."""

from dataclasses import dataclass
import shutil
import subprocess


class OllamaError(RuntimeError):
    """Raised when Ollama is unavailable or returns an error."""


@dataclass(frozen=True)
class Ollama:
    executable: str = "ollama"

    def installed(self) -> bool:
        return shutil.which(self.executable) is not None

    def _run(self, *args: str, timeout: float = 10) -> subprocess.CompletedProcess[str]:
        try:
            return subprocess.run(
                [self.executable, *args],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise OllamaError(str(exc)) from exc

    def is_running(self) -> bool:
        result = self._run("list")
        return result.returncode == 0

    def has_model(self, model: str) -> bool:
        result = self._run("list")
        if result.returncode != 0:
            return False
        rows = result.stdout.splitlines()[1:]
        return any(row.split(maxsplit=1)[0] == model for row in rows if row.strip())

    def generate(self, model: str, prompt: str) -> str:
        result = self._run("run", model, prompt, timeout=600)
        if result.returncode != 0:
            message = result.stderr.strip() or "Ollama failed to generate a response."
            raise OllamaError(message)
        return result.stdout.strip()
