import asyncio
import asyncpg
import logging

from data import config

async def create_db():
    create_db_command = open("aiogram/create_db.sql", "r").read()
    connection = await asyncpg.connect(
        database=config.PGDB,
        user=config.PGUSER,
        host=config.PGPASSWORD,
        )
    await connection.execute(create_db_command)
    await connection.close()


async def create_pool():
    return await asyncpg.create_pool(
        database='tgbot',
        user='user',
        host='localhost',
    )


if __name__=='__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
