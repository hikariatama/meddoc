# flake8: noqa: E402

import asyncio
import logging

from aiogram import Bot, Dispatcher, types

from . import log

log.init()

from . import config, handlers
from .notifier import Notifier

bot = Bot(
    token=config.BOT_TOKEN,
    parse_mode=types.ParseMode.HTML,
    disable_web_page_preview=True,
)

dp = Dispatcher(bot)

handlers.init(dp)

notifier = Notifier()
notifier.set_bot(bot)

logger = logging.getLogger("root")


def start():
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.create_task(notifier.poll())
    loop.run_forever()
