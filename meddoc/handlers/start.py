from aiogram import Dispatcher, types

from .. import fsm
from ..config import ADMINS


def init(dp: Dispatcher):
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        await fsm.ss(message, None, "state")
        if message.text == "/start":
            if message.from_user.id not in ADMINS:
                await message.answer_animation(
                    "https://t.me/hikari_assets/56",
                    caption="😕 <b>Привет, странник. Я не отвечу тебе ни на что!</b>",
                )
                return

            await message.answer_animation(
                "https://t.me/hikari_assets/70",
                caption=(
                    "🧑‍⚕️ <b>Добро пожаловать в генератор медицинских"
                    " документов!</b>\n\n<b>🌸 Напишите фамилию лицеиста, чтобы получить"
                    " справку для него</b>\n\n<b>🌸 Напишите </b><code>долги</code><b>,"
                    " чтобы получить список должников 😊</b>\n\n🌸 <b>Отправьте файл с"
                    " базой данных, чтобы обновить ее в боте</b>"
                ),
            )
