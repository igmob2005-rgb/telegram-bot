import asyncio, logging
from aiogram import Bot, Dispatcher
from Telegram_API.config import BOT_TOKEN
from database import init_db
from Telegram_API.handlers import router

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def main():
    init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    me = await bot.get_me()
    logging.info(f"Bot name: @{me.username}")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())