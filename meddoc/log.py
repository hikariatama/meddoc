import logging


def init():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()],
    )

    logging.getLogger("aiogram").setLevel(logging.WARNING)
