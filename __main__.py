from aiogram import Bot, Dispatcher
from tortoise import Tortoise
import asyncio
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Импортируем конфигурацию базы данных
from src.bot.config import BOT_TOKEN, TORTOISE_ORM
from src.bot.handlers.registration import router as registration_router
from aiogram.exceptions import TelegramBadRequest
from src.utils.middleware import LoggingMiddleware
from aerich import Command


# async def delete_webhook(bot: Bot):
#     try:
#         await bot.delete_webhook(drop_pending_updates=True)
#         print("Webhook successfully deleted.")
#     except TelegramBadRequest as e:
#         if "Not Found" in str(e):
#             print("Webhook is not set or already deleted.")
#         else:
#             print(f"Failed to delete webhook: {e}")
# Функция для инициализации базы данных
async def init_db():
    try:
        command = Command(
            tortoise_config=TORTOISE_ORM,
            app="models",
            location="./migrations"
        )
        await command.init()
        await command.upgrade()
        print("Database migrations applied successfully.")
    except Exception as e:
        print(f"Error while applying migrations: {e}")
    try:
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()
        
        print("Database connection established and schemas generated.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

# Основной цикл бота
async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.message.middleware(LoggingMiddleware())
    # Подключаем маршруты (обработчики)
    dp.include_router(registration_router)

    # Инициализируем базу данных
    await init_db()

    print("Bot is running...")
    try:
        # await delete_webhook(bot)
        await dp.start_polling(bot)
    finally:
        # Закрываем соединение с базой данных
        await Tortoise.close_connections()

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
