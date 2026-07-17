import os
import unittest
from unittest.mock import patch

from oxgpt.config import Config


class ConfigTests(unittest.TestCase):
    def test_defaults_are_local_and_model_is_configurable(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            config = Config.from_environment()
        self.assertEqual(config.model, "gemma3:270m")
        self.assertEqual(config.host, "127.0.0.1")
        self.assertEqual(config.port, 8765)

    def test_environment_overrides(self) -> None:
        with patch.dict(
            os.environ,
            {"OXGPT_MODEL": "llama3.2", "OXGPT_PORT": "9999"},
            clear=True,
        ):
            config = Config.from_environment()
        self.assertEqual(config.model, "llama3.2")
        self.assertEqual(config.port, 9999)


if __name__ == "__main__":
    unittest.main()
