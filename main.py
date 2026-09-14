import asyncio
from os import getenv
from DataBase import init_db
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers import router

# Загружаем файл .env из текущей папки на сервере
load_dotenv()

TOKEN = getenv("BOT_TOKEN")

print("Бот запущен ✅")

dp = Dispatcher()

try:
    async def main():
        # Создаем бота напрямую, без использования прокси-сессии
        bot = Bot(token=TOKEN)

        await init_db()
        dp.include_router(router)
        await dp.start_polling(bot)


    if __name__ == "__main__":
        asyncio.run(main())
except KeyboardInterrupt:
    print("\nБот выключен")
