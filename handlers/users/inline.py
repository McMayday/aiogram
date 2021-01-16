from loader import dp
from aiogram import types
from data import config
from .db_commands import database

from aiogram.dispatcher.filters import CommandStart


@dp.inline_handler(text="")
async def empty_query(query: types.InlineQuery):
    await query.answer(
        results=[
        types.InlineQueryResultArticle(
        id="unknow",
        title="Введите какой-то запрос",
        input_message_content=types.InputTextMessageContent(
            message_text="Не обязательно жать при этом на кнопку"
        )
        )
        ],
        cache_time=5
    )

@dp.inline_handler()
async def some_query(query: types.InlineQuery):
    user = query.from_user.id
    if user not in config.ALLOWED_USERS:
        await query.answer(
            results=[],
            switch_pm_text='Бот недоступен, подключите бота',
            switch_pm_parameter="connect_user",
            cache_time=5
        )
        return
    products = await database.get_products(query.query)
    print(products)
    print(dir(products))
    await query.answer(
        results=[
            types.InlineQueryResultArticle(
            id="1",
            title="Название, которое отображается в инлайн режиме",
            input_message_content=types.InputTextMessageContent(message_text="Тут какой-то текст"),
            url = "https://ireland.apollo.olxcdn.com/v1/files/hx4jgwfeyj6v1-UA/image;s=1000x700",
            thumb_url="https://ireland.apollo.olxcdn.com/v1/files/hx4jgwfeyj6v1-UA/image;s=1000x700",
            description="Описание в инлайн режиме",
        ),
        types.InlineQueryResultVideo(id="4", video_url="https://pixabay.com/en/videos/download/video-10737_medium.mp4",
        caption="подпись к видео", title='Какое-то видео тайтл', description="описание видео",
        thumb_url='https://i.pinimg.com/originals/c1/48/20/c1482019aee334b33177e5744a495ac0.jpg',
        mime_type="video/mp4"
        ),
        types.InlineQueryResultPhoto(id="2", photo_url="https://ireland.apollo.olxcdn.com/v1/files/hx4jgwfeyj6v1-UA/image;s=1000x700",
        thumb_url='https://i.pinimg.com/originals/c1/48/20/c1482019aee334b33177e5744a495ac0.jpg', caption="asdasd")
        ]
    )

@dp.message_handler(CommandStart(deep_link="connect_user"))
async def connect_user(message):
    config.ALLOWED_USERS.append(message.from_user.id)
    await message.answer('Вы подключены',
                        reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                            IlineKeyboardButton(text="Войти в инлайн режим",
                                                switch_inline_query_current_chat="Запрос")
                            ]
                        ]
                        ))
