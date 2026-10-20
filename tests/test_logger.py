from datetime import datetime

import pytest

from bm25_mcp.logger import logger
from bm25_mcp.server import build_server


@pytest.fixture(autouse=True)
def fresh_logger():
    logger.reset()
    yield
    logger.reset()


def test_enabled_logger_prints_timestamp_and_debug_message(capsys):
    logger.configure(enabled=True)
    logger.debug(message="hello")
    timestamp, message = capsys.readouterr().out.rstrip("\n").split(" [DEBUG]: ")
    datetime.fromisoformat(timestamp)
    assert message == "hello"


def test_disabled_or_unconfigured_logger_prints_nothing(capsys):
    logger.debug(message="before configure")
    logger.configure(enabled=False)
    logger.debug(message="hello")
    assert capsys.readouterr().out == ""


def test_logger_can_only_be_configured_once():
    logger.configure(enabled=True)
    with pytest.raises(RuntimeError):
        logger.configure(enabled=False)


def test_server_logs_its_steps(capsys, tmp_path):
    logger.configure(enabled=True)
    build_server(tmp_path)
    assert "[DEBUG]: Building server" in capsys.readouterr().out
