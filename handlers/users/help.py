from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку",
            "/CountInstaNames - Кол-во аккаунтов Instagram",
            "/CountInstaNotInBlackList - Кол-во незаблокированных аккаунтов Instagram",
            "/CountInstaInBlackList - Кол-во заблокированных аккаунтов Instagram",
            '/ResetInstaBlacklist - убрать конкретного пользователя instagram из черного списка',
            '/InstaAddBlacklist - добавить конкретного пользователя instagram в черный список',
            '/UserAddBlacklist - добавить telegram в черный список',
            '/UserRemoveFromBlacklist - убрать telegram из черного списка',
            '/InstaUsersCalls - какие юзернеймы обращались к никнейму',
            '/InstaUsersCallsCount - кол-во обращений к никнейму')

    await message.answer("\n".join(text))
