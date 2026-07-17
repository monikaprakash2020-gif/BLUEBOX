import unittest
from unittest.mock import patch

from oxgpt import service
from oxgpt.config import Config


class ServiceMainTests(unittest.TestCase):
    def test_main_runs_service_with_environment_config(self) -> None:
        expected = Config.from_environment()
        with patch.object(
            service.Config, "from_environment", return_value=expected
        ) as config:
            with patch.object(service, "run") as run:
                service.main()
        config.assert_called_once_with()
        run.assert_called_once_with(expected)


if __name__ == "__main__":
    unittest.main()
