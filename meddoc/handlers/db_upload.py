import io
import logging
import os

from aiogram import Dispatcher, types

from .. import fsm
from ..config import ADMIN_FILTER

logger = logging.getLogger(__name__)


def init(dp: Dispatcher):
    @dp.message_handler(ADMIN_FILTER, content_types=types.ContentTypes.DOCUMENT)
    async def upload_state(message: types.Message):
        if not message.document:
            await message.answer("❌ <b>Это не файл!</b>")
            return

        await dp.bot.send_chat_action(message.chat.id, "typing")

        data = io.BytesIO()
        await message.document.download(data)
        data.seek(0)

        with open("/mnt/data/database.xlsx", "wb") as f:
            f.write(data.read())

        await message.delete()

        await message.answer(
            "✅ <b>Информация о лицеистах успешно"
            " загружена!</b>\n\n🌸 <b>Напишите фамилию лицеиста, чтобы получить"
            " справку для него</b>\n\n🌸 <b>Напишите </b><code>долги</code><b>,"
            " чтобы получить список должников 😊</b>"
        )
        await fsm.ss(message, None, "state")
