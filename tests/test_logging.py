from evo.logging import setup_logging


def test_basic_logging_output_contains_utc_and_level(capsys):
    logger = setup_logging("INFO", name="evo.test")
    logger.info("hello world")
    out = capsys.readouterr().out.strip()
    assert " | INFO | evo.test | hello world" in out
    assert out.count("|") == 3
    assert out.endswith("hello world")

def test_duplicate_handlers_not_added(capsys):
    logger = setup_logging("INFO", name="evo.dupe")
    h1 = len(logger.handlers)
    logger = setup_logging("INFO", name="evo.dupe")
    h2 = len(logger.handlers)
    assert h2 == h1  # no duplicate handlers

def test_debug_level_applies(capsys):
    logger = setup_logging("DEBUG", name="evo.debug")
    logger.debug("dbg")
    out = capsys.readouterr().out
    assert " | DEBUG | evo.debug | dbg" in out

def test_info_level_default(capsys):
    logger = setup_logging(name="evo.info")
    logger.debug("should not see")
    out = capsys.readouterr().out
    assert "should not see" not in out
