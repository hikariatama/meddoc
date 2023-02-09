from aiogram import Dispatcher

from . import db_upload, getdoc, start


def init(dp: Dispatcher):
    start.init(dp)
    getdoc.init(dp)
    db_upload.init(dp)
