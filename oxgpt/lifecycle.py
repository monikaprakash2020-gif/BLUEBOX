"""OxGPT background process lifecycle."""

from __future__ import annotations

import os
from pathlib import Path
import signal
import subprocess
import sys
import time

from .client import health_check
from .config import Config
from .ollama import Ollama


def _read_pid(config: Config) -> int | None:
    try:
        return int(config.pid_file.read_text().strip())
    except (FileNotFoundError, ValueError):
        return None


def _alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def start(config: Config) -> tuple[bool, str]:
    existing = _read_pid(config)
    if existing and _alive(existing) and health_check(config):
        return True, "OxGPT Server Online"
    config.state_dir.mkdir(parents=True, exist_ok=True)
    process = subprocess.Popen(
        [sys.executable, "-m", "oxgpt.service"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        env=os.environ.copy(),
    )
    config.pid_file.write_text(str(process.pid))
    for _ in range(20):
        if health_check(config):
            return True, "OxGPT Server Online"
        time.sleep(0.1)
    stop(config)
    return False, "Server Not Available"


def stop(config: Config) -> bool:
    pid = _read_pid(config)
    if not pid:
        config.pid_file.unlink(missing_ok=True)
        return False
    try:
        os.kill(pid, signal.SIGTERM)
        for _ in range(20):
            if not _alive(pid):
                break
            time.sleep(0.1)
        else:
            os.kill(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    finally:
        config.pid_file.unlink(missing_ok=True)
    return True
