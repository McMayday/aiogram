from loader import db
from utils.set_bot_commands import set_default_commands
from data import config
from loader import bot



async def on_startup(dp):
    await set_default_commands(dp)
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


async def on_shutdown(dp):
    await bot.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
