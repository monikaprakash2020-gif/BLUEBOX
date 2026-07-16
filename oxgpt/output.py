"""Terminal output helpers."""

import os
import sys


RESET = "\033[0m"
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BOLD = "\033[1m"


def _paint(text: str, color: str) -> str:
    if os.environ.get("NO_COLOR") or not sys.stdout.isatty():
        return text
    return f"{color}{text}{RESET}"


def info(text: str) -> None:
    print(_paint(text, CYAN))


def success(text: str) -> None:
    print(_paint(text, GREEN))


def error(text: str) -> None:
    print(_paint(text, RED), file=sys.stderr)


def warning(text: str) -> None:
    print(_paint(text, YELLOW))


def prompt(text: str) -> str:
    return _paint(text, BOLD)
