from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware, rate_limit


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
