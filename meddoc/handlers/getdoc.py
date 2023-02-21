import io
import logging
import typing

from aiogram import Dispatcher, types

from .. import docx, utils
from ..config import ADMIN_FILTER
from ..notifier import Notifier

logger = logging.getLogger(__name__)


def init(dp: Dispatcher):
    @dp.callback_query_handler(lambda c: c.data.startswith("getdoc:"))
    async def getdoc_call(callback: types.CallbackQuery):
        await callback.message.delete()
        await getdoc_state(callback.message, force_user=callback.data.split(":")[1])

    @dp.message_handler(ADMIN_FILTER, content_types=types.ContentTypes.TEXT)
    async def getdoc_state(
        message: types.Message,
        force_user: typing.Optional[str] = None,
        override_text: typing.Optional[str] = None,
    ):
        if "долги" in message.text.lower():
            await dp.bot.send_chat_action(message.chat.id, "typing")
            notifier = Notifier()
            notifier.set_bot(dp.bot)
            await notifier.poll(force_send=message.from_user.id)
            return
        
        if not override_text:
            if "," in message.text:
                users = list(map(lambda x: x.strip(), message.text.split(",")))
                await message.answer(
                    f"👥 <b>Запрашиваю справки для {len(users)} лицеистов</b>"
                )
            else:
                users = [message.text]
        else:
            users = [override_text]

        for user in users:
            await dp.bot.send_chat_action(message.chat.id, "typing")

            if force_user:
                user = docx.find_user(md5=force_user)[0]
            else:
                fullname = override_text or user
                users = docx.find_user(fullname)
                if len(users) > 1:
                    markup = types.InlineKeyboardMarkup()
                    for user in users:
                        markup.row(
                            types.InlineKeyboardButton(
                                f"{user.real_name} • {user.grade}",
                                callback_data="getdoc:{}".format(user.id),
                            )
                        )
                    await message.answer(
                        "📝 <b>Выберите лицеиста для которого нужно сгенерировать "
                        "документы:</b>",
                        reply_markup=markup,
                    )
                    continue

                if not users:
                    await message.answer(
                        "❌ <b>Не удалось найти лицеиста с такой фамилией! Попробуйте"
                        " еще раз:</b>"
                    )
                    continue

                user = users[0]

            docs = []

            await dp.bot.send_chat_action(message.chat.id, "upload_document")

            name = user.real_name

            try:
                bytes_ = await utils.run_sync(lambda: docx.generate_079_u(user))
                assert bytes_
                doc = io.BytesIO(bytes_)
                doc.name = f"079-У {name}.docx".replace(" ", "_")
                docs.append(doc)
            except Exception:
                logger.exception("Failed to generate 079-У")

            try:
                bytes_ = await utils.run_sync(
                    lambda: docx.generate_medical_certificate(user)
                )
                assert bytes_
                doc = io.BytesIO(bytes_)
                doc.name = f"О состоянии здоровья {name}.docx".replace(" ", "_")
                docs.append(doc)
            except Exception:
                logger.exception("Failed to generate medical certificate")

            try:
                bytes_ = await utils.run_sync(
                    lambda: docx.generate_medical_verification(user)
                )
                assert bytes_
                doc = io.BytesIO(bytes_)
                doc.name = f"Об отсутствии инфекций {name}.docx".replace(" ", "_")
                docs.append(doc)
            except Exception:
                logger.exception("Failed to generate medical verification")

            if not docs:
                await message.answer(
                    "❌ <b>Не удалось сгенерировать ни одного документа!</b>"
                )
                continue

            media_group = types.MediaGroup()
            for doc in docs[:-1]:
                media_group.attach_document(doc)

            media_group.attach_document(
                docs[-1],
                caption=f"🧑‍⚕️ <b>{name}, {user.grade} класс</b>",
            )

            await message.answer_media_group(media_group)
