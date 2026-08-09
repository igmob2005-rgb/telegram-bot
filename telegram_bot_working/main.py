import asyncio, logging
from aiogram import Bot, Dispatcher
from Telegram_API.config import BOT_TOKEN
from database import DatabaseManager
from Pricelist import PricelistManager
from Telegram_API.handlers import router

db_manager = DatabaseManager()
pricelist_manager = PricelistManager()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def on_startup(*args, **kwargs):
    """
    Функция-хук, которая выполняется ТОЛЬКО один раз при старте бота.
    Тут мы гарантируем инициализацию всех системных данных.
    """
    print("********************************************")
    print("🎉 Бот успешно запущен и готов принимать команды!")
    # 1. Создание структуры БД.
    await db_manager.initialize_db()
    await pricelist_manager.initialize_pricelist_db()
    # 2. Заполнение структур заготовленными данными.
    await pricelist_manager.populate_initial_data()
    print("==============================================")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    dp.startup.register(on_startup) # Регистрация on_startup как обработчик старта бота

    me = await bot.get_me()
    logging.info(f"Bot name: @{me.username}")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped manually.")