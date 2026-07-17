"""Runtime configuration and XDG-compatible state paths."""

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Config:
    model: str
    host: str
    port: int
    state_dir: Path
    pid_file: Path
    log_file: Path

    @classmethod
    def from_environment(cls) -> "Config":
        state_root = Path(
            os.environ.get(
                "OXGPT_STATE_DIR",
                Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
                / "oxgpt",
            )
        ).expanduser()
        return cls(
            model=os.environ.get("OXGPT_MODEL", "gemma3:270m-it-qat"),
            host=os.environ.get("OXGPT_HOST", "127.0.0.1"),
            port=int(os.environ.get("OXGPT_PORT", "8765")),
            state_dir=state_root,
            pid_file=state_root / "oxgpt.pid",
            log_file=state_root / "oxgpt.log",
        )
