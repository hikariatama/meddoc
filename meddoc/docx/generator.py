import hashlib
import os
import tempfile
import typing

from docxtpl import DocxTemplate
from openpyxl import load_workbook

from ..schema import User
from ..utils import name_from_row, safestr


def find_user(
    surname: typing.Optional[str] = None,
    md5: typing.Optional[str] = None,
) -> typing.List[User]:
    """
    Find user by pertial surname or md5 of name
    :param surname: Partial surname
    :param md5: MD5 of full name
    :return: List of users
    :rtype: typing.List[User]
    """
    wb = load_workbook(os.path.join(os.path.dirname(__file__), "database.xlsx"))

    return [
        User.from_row(row)
        for row in wb.active.iter_rows(min_row=2, max_row=wb.active.max_row)
        if (
            surname
            and safestr(row[1].value)
            .lower()
            .replace("ё", "е")
            .startswith(surname.lower().replace("ё", "е"))
        )
        or (md5 and hashlib.md5(name_from_row(row).lower().encode()).hexdigest() == md5)
    ]


def generate_079_u(user: User) -> bytes:
    """
    Generate 079-U
    :param user: User
    :return: Generated document
    :rtype: bytes
    """
    doc = DocxTemplate(
        os.path.join(os.path.dirname(__file__), "079У Template.docx"),
    )
    doc.render(user.to_dict())
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "sheet.docx")
        doc.save(path)
        with open(path, "rb") as f:
            return f.read()


def generate_medical_certificate(user: User) -> bytes:
    """
    Generate medical certificate
    :param user: User
    :return: Generated document
    :rtype: bytes
    """
    doc = DocxTemplate(
        os.path.join(
            os.path.dirname(__file__),
            "Справка о состоянии здоровья Template.docx",
        )
    )
    doc.render(user.to_dict())
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "sheet.docx")
        doc.save(path)
        with open(path, "rb") as f:
            return f.read()


def generate_medical_verification(user: User) -> bytes:
    """
    Generate medical verification
    :param user: User
    :return: Generated document
    :rtype: bytes
    """
    doc = DocxTemplate(
        os.path.join(
            os.path.dirname(__file__),
            "Справка об отсутствии инфекций Template.docx",
        )
    )
    doc.render(user.to_dict())
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "sheet.docx")
        doc.save(path)
        with open(path, "rb") as f:
            return f.read()
