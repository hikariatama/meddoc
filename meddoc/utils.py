import asyncio
import datetime
import functools
import re
import typing


def run_sync(func, *args, **kwargs):
    """
    Run a non-async function in a new thread and return an awaitable
    :param func: Sync-only function to execute
    :returns: Awaitable coroutine
    """
    return asyncio.get_event_loop().run_in_executor(
        None,
        functools.partial(func, *args, **kwargs),
    )


def chunks(lst: list, n: int) -> typing.Iterator[list]:
    """
    Yield successive n-sized chunks from lst.
    """
    for i in range(0, len(lst), n):
        yield lst[i : i + n]  # noqa: E203


def safestr(value) -> str:
    return "" if value is None else str(value).strip()


def strdate(date: datetime.datetime) -> str:
    if not isinstance(date, datetime.datetime):
        return ""

    return date.strftime("%d.%m.%Y")


def safedate(value: str) -> typing.Optional[datetime.datetime]:
    if isinstance(value, datetime.datetime):
        return value

    value = safestr(value)

    try:
        date = list(re.findall(r"\d+\.\d+\.\d+", value))[-1]
    except IndexError:
        return None

    day, month, year = re.findall(r"\d+", date)

    if len(day) == 1:
        day = f"0{day}"

    if len(month) == 1:
        month = f"0{month}"

    if len(year) == 2:
        year = f"20{year}"

    return datetime.datetime.strptime(f"{day}.{month}.{year}", "%d.%m.%Y")


def format_phone(phone: str) -> str:
    phone = safestr(phone)
    if phone is None:
        return ""

    phone = phone.strip().split()[0]
    return f"+7 ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:11]}"


def name_from_row(row: list) -> str:
    return " ".join(
        (
            safestr(row[1].value),
            safestr(row[2].value),
            safestr(row[3].value),
        )
    ).strip()
