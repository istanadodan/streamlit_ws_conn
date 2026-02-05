import logging


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    logging.basicConfig(level=level, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    return logging.getLogger("__root__")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
