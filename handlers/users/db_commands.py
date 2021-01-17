from aiogram import types
from asyncpg import Connection, Record
from loader import bot, dp, db
from data import config
from aiogram.types import InputFile
from keyboards.inline.choice_buttons import choice
from datetime import timedelta, datetime
from aiogram.utils.callback_data import CallbackData
from keyboards.inline.callback_datas import *
from states.menu import Test
from aiogram.dispatcher.filters import BoundFilter
import os

class IsAdmin(BoundFilter):


    async def check(self, message):
        chat_id = message.from_user.id
        user_count = await database.get_admin(chat_id)
        if user_count:
            return True
        else:
            return False

class DbCommands:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pool = db
    ADD_ADMIN = "INSERT INTO admins(chat_id, username) VALUES($1,$2) RETURNING id"
    GET_ADMIN = "SELECT id FROM admins WHERE chat_id=$1"
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name, in_blacklist, active) VALUES ($1, $2, $3, $4, $5) RETURNING id"
    GET_ID = "SELECT id FROM users WHERE chat_id=$1"
    CREATE_USERNAMES = "INSERT INTO usernames(username, chat_id, users_id) VALUES ($1, $2, $3) RETURNING id"
    GET_USER_CREDENTIALS = "SELECT (active, in_blacklist) FROM users WHERE chat_id=$1"
    COUNT_INSTAGRAM_WITH_OUT_BLACKLIST = "SELECT COUNT(*) FROM instagram WHERE in_blacklist = false"
    COUNT_INSTAGRAM_IN_BLACKLIST = "SELECT COUNT(*) FROM instagram WHERE in_blacklist = true"
    GET_INSTAGRAM_USERS = "SELECT updated_at, username FROM instagram WHERE in_blacklist=true"
    COUNT_INSTAGRAM = "SELECT COUNT(*) FROM instagram"
    INSTAGRAM_USER_COUNT = "SELECT user_count FROM instagram where username = $1"
    GET_ID_INSTAGRAM = "SELECT id FROM instagram WHERE username=$1"
    GET_BLACKLIST_INSTAGRAM = "SELECT (in_blacklist, updated_at) FROM instagram WHERE username=$1"
    ADD_NEW_USER_REFERRAL = "INSERT INTO users(chat, username, full_name, referral)" \
                            "VALUES ($1, $2, $3, $4) RETURNING id"
    RESET_BLACKLIST = "UPDATE instagram SET in_blacklist=false WHERE username=$1"
    ADD_TO_BLACKLIST = "UPDATE instagram SET in_blacklist=true WHERE username=$1"
    UPDATE_COUNT_INSTAGRAM ="UPDATE instagram SET user_count = user_count + 1 WHERE username=$1"
    COUNT_INSTAGRAM_CALLS = "SELECT user_count from instagram WHERE username=$1"
    INSTAGRAM_USERNAME_CALLS = "SELECT username, chat_id from usernames WHERE users_id=$1"
    GET_INSTAGRAM_ID = "SELECT id FROM instagram where username=$1"
    ADD_USER_TO_BLACKLIST = "UPDATE users SET in_blacklist=true WHERE username=$1"
    REMOVE_USER_FROM_BLACKLIST = "UPDATE users SET in_blacklist=false WHERE username=$1"
    UPDATE_BLACKLIST_INSTAGRAM = "UPDATE instagram SET in_blacklist=true WHERE username=$1"
    ACTIVATE_USER = "UPDATE users SET active=true WHERE username=$1"
    GET_ID_BY_USERNAME = "SELECT id FROM users WHERE username=$1"
    RESET_DATE = "UPDATE instagram SET updated_at=$2 WHERE username=$1"
    ADD_NEW_INSTAGRAM = "INSERT INTO instagram(username, created_at, updated_at, in_blacklist, user_count) VALUES ($1, $2, $3, $4, $5) RETURNING id"
    UPLOAD_TO_CSV_INSTAGRAM =  f"COPY instagram TO '{BASE_DIR}/instagram.csv' DELIMITER ',' CSV HEADER;"
    async def add_new_user(self, referral=None):
        user = types.User.get_current()
        chat_id = user.id
        username = user.username
        active = True
        in_blacklist = False
        full_name = user.full_name
        args = (chat_id, username, full_name, in_blacklist, active)
        if referral:
            command = self.ADD_NEW_USER
        else:
            return None
        try:
            record_id = await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            return None
        return record_id

    async def count_instagram(self):
        record = await self.pool.fetchval(self.COUNT_INSTAGRAM)
        return record

    async def count_instagram_with_out_blacklist(self):
        record = await self.pool.fetchval(self.COUNT_INSTAGRAM_WITH_OUT_BLACKLIST)
        return record

    async def count_instagram_in_blacklist(self):
        record = await self.pool.fetchval(self.COUNT_INSTAGRAM_IN_BLACKLIST)
        return record

    async def get_admin(self, chat_id):
        id = await self.pool.fetchval(self.GET_ADMIN, str(chat_id))
        return id

    async def reset_blacklist(self, username=None):
        if not username:
            return None
        id = await self.pool.fetchval(self.GET_ID_INSTAGRAM, username)
        if id:
            record = await self.pool.fetchval(self.RESET_BLACKLIST, username)
            return True
        return False


    async def get_insta_id(self, username=None):
        if not username:
            return None
        id = await self.pool.fetchval(self.GET_ID_INSTAGRAM, username)
        return id


    async def add_to_blacklist(self, username=None):
        if not username:
            return None
        id = await self.pool.fetchval(self.GET_ID_INSTAGRAM, username)
        if id:
            record = await self.pool.fetchval(self.ADD_TO_BLACKLIST, username)
            return True
        return False


    async def inc_instagram_calls(self, username=None):
        if not username:
            return None
        record = await self.pool.fetchval(self.UPDATE_COUNT_INSTAGRAM, username)
        return record


    async def get_insta_blacklist_and_date(self, username=None):
        if not username:
            return None
        record = await self.pool.fetchval(self.GET_BLACKLIST_INSTAGRAM, username)
        return record


    async def count_instagram_calls(self, username=None):
        if not username:
            return None
        record = await self.pool.fetchval(self.COUNT_INSTAGRAM_CALLS, username)
        return record

    async def get_user_credentials(self, username):
        record = await self.pool.fetchval(self.GET_USER_CREDENTIALS, username)
        return record

    async def count_instagram_calls(self, username=None):
        if not username:
            return None
        record = await self.pool.fetchval(self.COUNT_INSTAGRAM_CALLS, username)
        return record

    async def instagram_username_calls(self, id):
        record = await self.pool.fetch(self.INSTAGRAM_USERNAME_CALLS, id)
        return record


    async def add_user_to_blacklist(self, username):
        if not username:
            return None
        id = await self.pool.fetchval(self.GET_ID_BY_USERNAME, username)
        if id:
            record = await self.pool.fetchval(self.ADD_USER_TO_BLACKLIST, username)
            return True
        return False


    async def remove_user_from_blacklist(self, username):
        if not username:
            return None
        id = await self.pool.fetchval(self.GET_ID_BY_USERNAME, username)
        if id:
            record = await self.pool.fetchval(self.REMOVE_USER_FROM_BLACKLIST, username)
            return True
        return False

    async def increment_user(self, username=None):
        await self.pool.fetchval(self.UPDATE_COUNT_INSTAGRAM, username)

    async def get_insta_count(self, username=None):
        if not username:
            return None
        user_count = await self.pool.fetchval(self.INSTAGRAM_USER_COUNT, username)
        return user_count

    async def add_insta_calls(self, username, chat_id, user_id):
        args = username, chat_id, user_id
        await self.pool.fetchval(self.CREATE_USERNAMES, *args)

    async def add_new_instagram(self, username=None):
        if not username:
            return None
        tg_user = types.User.get_current()
        tg_chat_id = tg_user.id
        tg_username = tg_user.username
        in_blacklist = False
        insta_username = username
        created_at = datetime.today()
        updated_at = created_at
        user_count = 1
        args = (insta_username, created_at, updated_at, in_blacklist, user_count)
        record_id = await self.pool.fetchval(self.ADD_NEW_INSTAGRAM, *args)
        return record_id

    async def reset_date(self, username):
        date = datetime.today()
        args = (username, date)
        await self.pool.fetchval(self.RESET_DATE, *args)

    async def get_csv(self, chat_id):
        await self.pool.fetchval(self.UPLOAD_TO_CSV_INSTAGRAM)
        ff = InputFile(f"{self.BASE_DIR}/instagram.csv", filename='instaDB.csv')
        await bot.send_document(chat_id=chat_id, document = ff)


    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        return user_id

    async def add_new_admin(self, user, chat_id):
        id = await self.pool.fetch(self.ADD_ADMIN, str(chat_id), user)
        return id

    async def check_accounts(self):
        users = await self.pool.fetch(self.GET_INSTAGRAM_USERS)
        for row in users:
            if row['updated_at'] + timedelta(days=7) < datetime.now().date():
                await self.reset_blacklist(row['username'])


database = DbCommands()

@dp.message_handler(commands=["start"])
async def register_user(message):
    chat_id = message.from_user.id
    user = message.from_user.username
    key = message.get_args()
    if key == config.ADMIN_KEY:
        id = await database.add_new_admin(user, chat_id)
        if not id:
            text = 'Доброго времени суток'
            await bot.send_message(chat_id, text)
        else:
            text = 'Записал в базу'
            await bot.send_message(chat_id, text)
    else:
        if key != config.KEY:
            text = f'Для того чтобы пользоваться ботом сначала активируйте его'
            await bot.send_message(chat_id, text)
        else:
            id = await database.add_new_user(referral=key)
            if not id:
                text = 'Доброго времени суток'
                await bot.send_message(chat_id, text)
            else:
                text = 'Записал в базу'
                await bot.send_message(chat_id, text)


@dp.message_handler(IsAdmin(), commands=["CountInstaNames"])
async def register_user(message):
    chat_id = message.from_user.id
    permission = await check_permissions(chat_id)
    if not permission:
        await bot.send_message(chat_id, 'Для работы с ботом необходимо активировать аккаунт')
    else:
        count = await database.count_instagram()
        await database.get_csv(chat_id)
        await bot.send_message(chat_id, f'На данный момент в базе {count} пользователей instagram') #FIX IT: прикрутить вывод базы из excel

@dp.message_handler(IsAdmin(), commands=["CountInstaNotInBlackList"])
async def insta_no_blacklist_count(message):
    chat_id = message.from_user.id
    permission = await check_permissions(chat_id)
    if not permission:
        await bot.send_message(chat_id, 'Для работы с ботом необходимо активировать аккаунт')
    else:
        count = await database.count_instagram_with_out_blacklist()
        await database.get_csv(chat_id)
        await bot.send_message(chat_id, f'Кол-во пользователей с отсутствующей семидневной блокировкой {count}')  #FIX IT: прикрутить вывод базы из excel


@dp.message_handler(IsAdmin(), commands=["CountInstaInBlackList"])
async def insta_in_blacklist_count(message):
    await database.check_accounts()
    chat_id = message.from_user.id
    permission = await check_permissions(chat_id)
    if not permission:
        await bot.send_message(chat_id, 'Для работы с ботом необходимо активировать аккаунт')
    else:
        count = await database.count_instagram_in_blacklist()
        await database.get_csv(chat_id)
        await bot.send_message(chat_id, f'Кол-во пользователей с семидневной блокировкой {count}')  #FIX IT: прикрутить вывод базы из excel

@dp.message_handler(IsAdmin(), commands=["ResetInstaBlacklist"])
async def reset_insta_blacklist_count(message, user=None):
    chat_id = message.from_user.id
    permission = await check_permissions(chat_id)
    if not permission:
        await bot.send_message(chat_id, 'Для работы с ботом необходимо активировать аккаунт')
    else:
        if user:
            username = user
        else:
            username = message.get_args()
        result = await database.reset_blacklist(username)
        if result:
            await bot.send_message(chat_id, f'Снял блокировку с пользователя {username}')
        else:
            await bot.send_message(chat_id, f'Пользователя {username} не существует')

@dp.message_handler(IsAdmin(), commands=["InstaAddBlacklist"])
async def add_insta_in_blacklist_count(message, user=None):
    await database.check_accounts()
    chat_id = message.from_user.id
    permission = await check_permissions(chat_id)
    if not permission:
        await bot.send_message(chat_id, 'Для работы с ботом необходимо активировать аккаунт')
    else:
        if user:
            username = user
        else:
            username = message.get_args()
        result = await database.add_to_blacklist(username)
        if result:
            await bot.send_message(chat_id, f'Добавил  пользователя {username} в черный список')
        else:
            await bot.send_message(chat_id, f'Пользователя {username} не существует')

@dp.message_handler(IsAdmin(), commands=["UserAddBlacklist"])
async def user_add_blacklist_count(message, user=None):
    chat_id = message.from_user.id
    permission = await check_permissions(chat_id)
    if not permission:
        await bot.send_message(chat_id, 'Для работы с ботом необходимо активировать аккаунт')
    else:
        if user:
            username = user
        else:
            username = message.get_args()
        result = await database.add_user_to_blacklist(username)
        if result:
            await bot.send_message(chat_id, f'Добавил  пользователя {username} в черный список')
        else:
            await bot.send_message(chat_id, f'Пользователя {username} не существует')

@dp.message_handler(IsAdmin(), commands=["UserRemoveFromBlacklist"])
async def user_remove_blacklist_count(message, user=None):
    chat_id = message.from_user.id
    permission = await check_permissions(chat_id)
    if not permission:
        await bot.send_message(chat_id, 'Для работы с ботом необходимо активировать аккаунт')
    else:
        if user:
            username = user
        else:
            username = message.get_args()
        result = await database.remove_user_from_blacklist(username)
        if result:
            await bot.send_message(chat_id, f'Снял блокировку с пользователя {username}')
        else:
            await bot.send_message(chat_id, f'Пользователя {username} не существует')


@dp.message_handler(IsAdmin(), commands=["InstaUsersCalls"])
async def insta_blacklist_counts(message, user=None):
    "какие пользователи обращались к instagram никнейму"
    chat_id = message.from_user.id
    permission = await check_permissions(chat_id)
    if not permission:
        await bot.send_message(chat_id, 'Для работы с ботом необходимо активировать аккаунт')
    else:
        if user:
            username = user
        else:
            username = message.get_args()
        id = await database.get_insta_id(username)
        if id:
            str = ''
            names = set()
            tg_names = await database.instagram_username_calls(id)
            for row in tg_names:
                names.add(row['username'])
            for name in names:
                str += f'\n {name}'
            await bot.send_message(chat_id, f'Пользователи, которые обращались к {username}' \
                                    f'\n {str}')
        else:
            await bot.send_message(chat_id, f'Пользователя {username} не существует')


@dp.message_handler(IsAdmin(), commands=["InstaUsersCallsCount"])
async def insta_count(message, user=None):
    "количество обращений к instagram никнейму"
    chat_id = message.from_user.id
    permission = await check_permissions(chat_id)
    if not permission:
        await bot.send_message(chat_id, 'Для работы с ботом необходимо активировать аккаунт')
    else:
        if user:
            username = user
        else:
            username = message.get_args()
        user_count = await database.get_insta_count(username)
        if id:
            return await bot.send_message(chat_id, f'К пользователю {username} обращались {user_count} раз')
        else:
            await bot.send_message(chat_id, f'Пользователя {username} не существует')

@dp.message_handler(IsAdmin(), commands=["Items"])
async def show_items(message):
    "количество обращений к instagram никнейму"
    chat_id = message.from_user.id
    permission = await check_permissions(chat_id)
    if not permission:
        await bot.send_message(chat_id, 'Для работы с ботом необходимо активировать аккаунт')
    else:
        await message.answer(text="для вызова списка команд напишите /help", reply_markup=choice)


async def check_permissions(chat_id):
    user_count = await database.get_admin(chat_id)
    if user_count:
        return True
    try:
        is_active, in_blacklist = await database.get_user_credentials(chat_id)
        if is_active == True and in_blacklist == False:
            return True
        else:
            return None
    except:
        return None


@dp.callback_query_handler(text='all_insta_names')
async def all_insta_names(message):
    await register_user(message)

@dp.callback_query_handler(text='insta_count_no_block')
async def with_out_blacklist(message):
    await insta_no_blacklist_count(message)

@dp.callback_query_handler(text='insta_count_block')
async def in_blacklist(message):
    await insta_in_blacklist_count(message)

@dp.callback_query_handler(text='insta_remove_blacklist')
async def insta_remove_from_blacklist(message):
    await message.answer('Введите никнейм')
    await Test.Q1.set()

@dp.message_handler(state=Test.Q1)
async def reset_all_blacklist(message, state):
    answer = message.text
    await reset_insta_blacklist_count(message, answer)
    await state.finish()

@dp.callback_query_handler(text='insta_add_blacklist')
async def insta_remove_from_blacklist(message):
    await message.answer('Введите никнейм')
    await Test.Q2.set()

@dp.message_handler(state=Test.Q2)
async def add_blacklist(message, state):
    answer = message.text
    await add_insta_in_blacklist_count(message, answer)
    await state.finish()


@dp.callback_query_handler(text='user_add_blaclkist')
async def insta_remove_from_blacklist(message):
    await message.answer('Введите никнейм')
    await Test.Q3.set()

@dp.message_handler(state=Test.Q3)
async def answer_q1(message, state):
    answer = message.text
    await user_add_blacklist_count(message, answer)
    await state.finish()

@dp.callback_query_handler(text='user_remove_blacklist')
async def insta_remove_from_blacklist(message):
    await message.answer('Введите никнейм')
    await Test.Q4.set()

@dp.message_handler(state=Test.Q4)
async def blacklist_count(message, state):
    answer = message.text
    await user_remove_blacklist_count(message, answer)
    await state.finish()

@dp.callback_query_handler(text='insta_users_calls')
async def users_calls(message):
    await message.answer('Введите никнейм')
    await Test.Q5.set()

@dp.message_handler(state=Test.Q5)
async def users_calls_state2(message, state):
    answer = message.text
    await insta_blacklist_counts(message, answer)
    await state.finish()

@dp.callback_query_handler(text='insta_users_calls_count')
async def users_calls_count(message):
    await message.answer('Введите никнейм')
    await Test.Q6.set()

@dp.message_handler(state=Test.Q6)
async def users_calls_count_state2(message, state):
    answer = message.text
    await insta_count(message, answer)
    await state.finish()
