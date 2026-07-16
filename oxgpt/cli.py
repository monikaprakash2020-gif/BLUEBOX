"""Command-line interface for OxGPT."""

from __future__ import annotations

import argparse
import sys

from .client import ServiceError, chat
from .config import Config
from .lifecycle import start, stop
from .ollama import Ollama
from .output import error, info, prompt, success, warning


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="oxgpt",
        description="A local terminal AI assistant powered by Ollama.",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    parser.add_argument("command", choices=("start", "stop", "chat"))
    return parser


def start_command(config: Config, ollama: Ollama) -> int:
    info("Checking Ollama...")
    if not ollama.installed():
        error("Ollama is not installed. Install it from https://ollama.com/download")
        return 1
    if not ollama.is_running():
        error("Ollama service is not running. Start it with: ollama serve")
        return 1
    info("Checking model...")
    if not ollama.has_model(config.model):
        error(f"Required model is missing: {config.model}")
        error(f"Pull it with: ollama pull {config.model}")
        return 1
    info("Starting server...")
    info("Running health check...")
    healthy, message = start(config)
    if healthy:
        success(f"✅ {message}")
        return 0
    error(f"❌ {message}")
    return 1


def chat_command(config: Config) -> int:
    if not sys.stdin.isatty():
        error("Interactive chat requires a terminal.")
        return 1
    info(f"OxGPT chat ({config.model}). Type 'exit' to quit.")
    while True:
        try:
            message = input(f"{prompt('You:')} ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if message.strip().lower() == "exit":
            break
        if not message.strip():
            continue
        try:
            print(f"{prompt('OxGPT:')} {chat(config, message)}")
        except ServiceError as exc:
            error(str(exc))
            return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = Config.from_environment()
    ollama = Ollama()
    if args.command == "start":
        return start_command(config, ollama)
    if args.command == "stop":
        info("Stopping server...")
        stop(config)
        success("✅ Server stopped.")
        return 0
    return chat_command(config)


if __name__ == "__main__":
    raise SystemExit(main())
