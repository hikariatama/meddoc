import logging
from logging.handlers import RotatingFileHandler


def init():
    rotating_handler = RotatingFileHandler(
        filename="debug.log",
        mode="a",
        maxBytes=5 * 1024 * 1024,
        backupCount=2,
        encoding=None,
        delay=0,
    )

    stream_handler = logging.StreamHandler()

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
        handlers=[rotating_handler, stream_handler],
    )

    logging.getLogger("aiogram").setLevel(logging.WARNING)
