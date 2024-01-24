import pathlib
import logging
from fancylogging import setup_fancy_logging

log = logging.getLogger("test")

if __name__ == "__main__":
    cwd = pathlib.Path.cwd()

    setup_fancy_logging(
        "test",
        console_log_level=logging.INFO,
        file_log_level=logging.DEBUG,
        log_file_path=cwd / "logs" / "test.json",
        file_mode="w",
    )

    log.info("Info message")
    log.debug("Debug message")
    log.warning("Warning message")
    log.error("Error message")
    log.critical("Critical message")
    try:
        raise Exception("Raising a test exception in main")
    except Exception:
        log.exception("Exception message")
