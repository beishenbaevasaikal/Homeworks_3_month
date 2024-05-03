import asyncio

from config import dp, bot
from handlers import setup_routers
from database.db import AsyncDatabase


async def main():
    db = AsyncDatabase()
    await db.create_tables()
    router = setup_routers()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
