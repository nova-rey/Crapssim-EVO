from __future__ import annotations

from evo.logging import setup_logging


def test_basic_logging_output_contains_utc_and_level(capsys):
    logger = setup_logging("INFO", name="evo.test")
    logger.info("hello world")

    out = capsys.readouterr().out.strip()
    assert out.endswith("hello world")
    assert "INFO" in out
    assert out.split(" ")[0].endswith("Z")


def test_setup_logging_respects_level(capsys):
    logger = setup_logging("WARNING", name="evo.test.level")
    logger.info("should not appear")
    logger.warning("something happened")

    lines = [line for line in capsys.readouterr().out.splitlines() if line]
    assert len(lines) == 1
    assert "something happened" in lines[0]
