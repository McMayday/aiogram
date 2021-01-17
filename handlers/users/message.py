from loader import dp
from aiogram import types
from data import config
from loader import bot, dp, db
from .db_commands import *
from datetime import timedelta, datetime
from utils.misc import rate_limit


@rate_limit(limit=10)
@dp.message_handler()
async def echo(message):
    chat_id = message.from_user.id
    tg_username = message.from_user.username
    permission = await check_permissions(chat_id)
    if not permission:
        await bot.send_message(chat_id, 'Нет доступа')
    else:
        url = message.text
        if 'https://www.instagram.com/' in url:
            insta_username = str(url).split('/')[-1].split('?')[0]
            username_exists = await database.get_insta_id(insta_username)
            if not username_exists:
                id = await database.add_new_instagram(insta_username)
                await database.add_to_blacklist(insta_username)
                await bot.send_message(chat_id, 'Можно писать')
                await database.add_insta_calls(tg_username, str(chat_id), id)
            else:
                await database.add_insta_calls(tg_username, str(chat_id), username_exists)
                in_blacklist, updated_at = await database.get_insta_blacklist_and_date(insta_username)
                if updated_at + timedelta(days=7) < datetime.now().date() or in_blacklist==False:
                    await database.reset_date(insta_username)
                    await database.add_to_blacklist(insta_username)
                    await bot.send_message(chat_id, 'Можно писать')
                    await database.increment_user(insta_username)
                else:
                    await bot.send_message(chat_id, 'Нельзя писать')
        else:
            await bot.send_message(chat_id, u"Неправильно введенный пользователь, \n" \
                                "формат ввода: https://www.instagram.com/имя_пользователя")
