import os
import tempfile
import pytest
import logging
from src.logging import setup_logger, set_logging_level


@pytest.fixture
def logger():
    log_file = "test.log"
    logger = setup_logger("test_logger", log_file)
    yield logger
    if os.path.exists(log_file):
        os.remove(log_file)


def test_logging(logger):
    log_file = "test.log"
    logger.info("Test log message")
    assert os.path.exists(log_file)
    with open(log_file, "r") as f:
        content = f.read()
        assert "Test log message" in content


@pytest.mark.parametrize(
    "level_name, log_level",
    [
        ("DEBUG", logging.DEBUG),
        ("INFO", logging.INFO),
        ("WARNING", logging.WARNING),
        ("ERROR", logging.ERROR),
        ("CRITICAL", logging.CRITICAL),
        ("INVALID", logging.INFO),  # Default case for invalid level
    ],
)
def test_set_logging_level(level_name, log_level):
    assert set_logging_level(level_name) == log_level


@pytest.mark.parametrize(
    "level_name, log_message, is_in_log",
    [
        ("DEBUG", "This is a debug message", True),
        ("INFO", "This is an info message", True),
        ("WARNING", "This is a warning message", True),
        ("ERROR", "This is an error message", True),
        ("CRITICAL", "This is a critical message", True),
        ("INFO", "This debug message should not appear", False),
    ],
)
def test_logger_levels(level_name, log_message, is_in_log):
    log_file = "test.log"
    log_level = set_logging_level(level_name)
    logger = setup_logger("test_logger_level", log_file, log_level)

    if "debug" in log_message.lower():
        logger.debug(log_message)
    elif "info" in log_message.lower():
        logger.info(log_message)
    elif "warning" in log_message.lower():
        logger.warning(log_message)
    elif "error" in log_message.lower():
        logger.error(log_message)
    elif "critical" in log_message.lower():
        logger.critical(log_message)

    with open(log_file, "r") as f:
        content = f.read()
        assert (log_message in content) == is_in_log

    if os.path.exists(log_file):
        os.remove(log_file)


def test_console_logging(caplog):
    with caplog.at_level(logging.INFO):
        logger = setup_logger("console_logger", None, logging.INFO, console=True)
        logger.info("Console log message")
        assert "Console log message" in caplog.text


def test_file_and_console_logging(caplog):
    log_file = "test_file_console.log"
    with caplog.at_level(logging.INFO):
        logger = setup_logger(
            "file_console_logger", log_file, logging.INFO, console=True
        )
        logger.info("File and console log message")
        assert "File and console log message" in caplog.text
        with open(log_file, "r") as f:
            content = f.read()
            assert "File and console log message" in content

    if os.path.exists(log_file):
        os.remove(log_file)


def test_invalid_log_level():
    with pytest.raises(ValueError):
        set_logging_level(None)


def test_invalid_log_file_path():
    with pytest.raises(FileNotFoundError):
        setup_logger("test_logger_invalid_path", "/invalid/path/test.log")


def test_missing_parameters():
    with pytest.raises(TypeError):
        setup_logger()  # Missing required parameters


def test_invalid_log_file_permission():
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, "test.log")
        os.chmod(tmpdir, 0o400)  # Set directory to read-only
        with pytest.raises(PermissionError):
            setup_logger("test_logger_permission", log_file)

    # Cleanup not needed as tempfile handles it


def test_no_log_destination():
    with pytest.raises(ValueError):
        setup_logger("no_destination_logger", None, logging.INFO, console=False)
