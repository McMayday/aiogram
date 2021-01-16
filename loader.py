import asyncio
import logging
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import types
from data import config
from sql import create_pool


loop = asyncio.get_event_loop()
storage = MemoryStorage()


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

db = loop.run_until_complete(create_pool())
