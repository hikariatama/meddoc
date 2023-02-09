import dataclasses
import datetime
import hashlib

from ..utils import format_phone, name_from_row, safedate, safestr, strdate


@dataclasses.dataclass
class User:
    """Represents a user."""

    real_name: str
    m: str
    f: str
    date_of_birth: str
    grade: str
    phone: str
    address: str
    childhoodillnesses: str
    DPT: str
    OPV: str
    measels: str
    mantoux: str
    fluorography: str
    health_group: str
    physical: str
    chronicals: str
    diagnosis: str
    day: str
    month: str
    year: str
    date: str
    id: str = dataclasses.field(init=False)

    def __post_init__(self):
        self.id = hashlib.md5(self.real_name.lower().encode()).hexdigest()

    @classmethod
    def from_row(cls, row):
        return cls(
            real_name=name_from_row(row),
            m="" if safestr(row[4].value).upper() == "Ж" else "X",
            f="X" if safestr(row[4].value).upper() == "Ж" else "",
            date_of_birth=strdate(safedate(row[5].value)),
            grade=safestr(row[0].value),
            phone=format_phone(row[13].value),
            address=safestr(row[14].value),
            childhoodillnesses=(
                ", ".join(
                    f"{illness} - переболел"
                    for trigger, illness in {
                        "коклюш": "коклюш",
                        "ветрян": "ветряная оспа",
                        "скарлат": "скарлатина",
                        "мононуклеоз": "инфекционный мононуклеоз",
                    }.items()
                    if trigger in safestr(row[15].value)
                )
                or "нет"
            ),
            DPT=strdate(safedate(row[7].value)),
            OPV=strdate(safedate(row[8].value)),
            measels=strdate(safedate(row[9].value)),
            mantoux=strdate(safedate(row[6].value)),
            fluorography=strdate(safedate(row[10].value)),
            health_group=safestr(row[18].value).strip(),
            physical=safestr(row[19].value),
            chronicals=safestr(row[16].value),
            diagnosis=safestr(row[16].value).replace("\n", ", "),
            day=(datetime.datetime.now() + datetime.timedelta(hours=3)).day,
            month=(
                [
                    "января",
                    "февраля",
                    "марта",
                    "апреля",
                    "мая",
                    "июня",
                    "июля",
                    "августа",
                    "сентября",
                    "октября",
                    "ноября",
                    "декабря",
                ][(datetime.datetime.now() + datetime.timedelta(hours=3)).month - 1]
            ),
            year=str((datetime.datetime.now() + datetime.timedelta(hours=3)).year)[-2:],
            date=(
                (datetime.datetime.now() + datetime.timedelta(hours=3))
                .strftime("«%d» %B %Y года")
                .replace("January", "января")
                .replace("February", "февраля")
                .replace("March", "марта")
                .replace("April", "апреля")
                .replace("May", "мая")
                .replace("June", "июня")
                .replace("July", "июля")
                .replace("August", "августа")
                .replace("September", "сентября")
                .replace("October", "октября")
                .replace("November", "ноября")
                .replace("December", "декабря")
            ),
        )

    def to_dict(self):
        return dataclasses.asdict(self)
