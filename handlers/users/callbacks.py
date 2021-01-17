from states.menu import Test
from loader import bot, dp, db
from .db_commands import *

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


@dp.callback_query_handler(text='block_forever')
async def users_calls_count(message):
    await message.answer('Введите никнейм')
    await Test.Q7.set()

@dp.message_handler(state=Test.Q7)
async def users_calls_count_state2(message, state):
    answer = message.text
    await database.block_user_forever(answer)
    await state.finish()
