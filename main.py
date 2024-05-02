import asyncio

from config import dp, bot
from handlers import setup_routers


async def main():
    router =setup_routers()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
