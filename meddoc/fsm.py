import json
import logging
import os
from typing import Optional, Union

from aiofile import async_open as aopen
from aiogram import types

logger = logging.getLogger(__name__)

try:
    with open("/mnt/data/fsm.json", "r", encoding="utf-8") as f:
        fsm = json.load(f)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    fsm = {}


def get_state(
    user: Union[int, types.Message, types.CallbackQuery],
    key: Optional[str] = None,
) -> dict:
    if isinstance(user, (types.Message, types.CallbackQuery)):
        user = user.from_user.id

    data = fsm.get(str(user), {})
    return data.get(key, None) if key else data


async def set_state(
    user: Union[int, types.Message, types.CallbackQuery],
    data: Union[dict, str, int, list],
    key: Optional[str] = None,
) -> None:
    if isinstance(user, (types.Message, types.CallbackQuery)):
        user = user.from_user.id

    if key:
        if not fsm.get(str(user)):
            fsm[str(user)] = {}

        if data:
            fsm[str(user)][key] = data
        else:
            fsm[str(user)].pop(key, None)
    elif not data:
        fsm.pop(str(user), None)
    else:
        fsm[str(user)] = data

    async with aopen("/mnt/data/fsm.json", "w", encoding="utf-8") as f:
        await f.write(json.dumps({key: value for key, value in fsm.items() if value}))


gs = get_state
ss = set_state
