import logging
from pathlib import Path
from unittest.mock import patch

from app.logger import Logger


def test_configure_calls_basic_config(tmp_path):
    log_file = tmp_path / "calculator.log"
    with patch('app.logger.logging.basicConfig') as mock_basic_config:
        Logger.configure(log_file)
        mock_basic_config.assert_called_once_with(
            filename=str(log_file),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            force=True,
        )


def test_configure_writes_to_file(tmp_path):
    log_file = tmp_path / "calculator.log"
    Logger.configure(log_file)
    Logger.info("hello from test_configure_writes_to_file")
    assert log_file.exists()
    assert "hello from test_configure_writes_to_file" in log_file.read_text()


def test_info_logs_message(caplog):
    with caplog.at_level(logging.INFO, logger="calculator"):
        Logger.info("an info message")
    assert "an info message" in caplog.text


def test_warning_logs_message(caplog):
    with caplog.at_level(logging.WARNING, logger="calculator"):
        Logger.warning("a warning message")
    assert "a warning message" in caplog.text


def test_error_logs_message(caplog):
    with caplog.at_level(logging.ERROR, logger="calculator"):
        Logger.error("an error message")
    assert "an error message" in caplog.text
