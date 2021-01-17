from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


choice = InlineKeyboardMarkup(row_width=1,
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(
                                        text="Общее количество никнеймов в базе",
                                        callback_data="all_insta_names",
                                    ),
                                ],
                                [
                                        InlineKeyboardButton(
                                            text="Кол-во никнеймов без блокировки",
                                            callback_data="insta_count_no_block",
                                            ),
                                ],
                                [
                                    InlineKeyboardButton(
                                        text="Кол-во никнеймов в блеклисте",
                                        callback_data="insta_count_block",
                                    ),

                                ],

                                [
                                    InlineKeyboardButton(
                                        text="Внести никнейм в блеклист",
                                        callback_data="insta_add_blacklist",
                                    ),

                                ],
                                [
                                        InlineKeyboardButton(
                                            text="Убрать никнейм из блеклиста",
                                            callback_data="insta_remove_blacklist",
                                    ),

                                ],
                                [

                                    InlineKeyboardButton(
                                        text="Какие юзеры обращались к никнейму",
                                        callback_data="insta_users_calls",
                                    ),

                                ],
                                [
                                    InlineKeyboardButton(
                                        text="Кол-во обращений к никнейму",
                                        callback_data="insta_users_calls_count",
                                    ),
                                ],
                                [

                                    InlineKeyboardButton(
                                        text="Внести юзернейм(telegram) в блеклист",
                                        callback_data="user_add_blaclkist",
                                    ),



                                ],
                                [
                                    InlineKeyboardButton(
                                        text="Убрать юзернейм(telegram) из блеклиста",
                                        callback_data="user_remove_blacklist",
                                    ),
                                ],
                                [
                                    InlineKeyboardButton(
                                        text="Заблокировать инстаграм(10лет)",
                                        callback_data="block_forever",
                                    ),
                                ]





                            ])
