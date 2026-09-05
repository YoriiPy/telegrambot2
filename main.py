from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from os import getenv

from aiohttp import ClientSession
from dotenv import load_dotenv
from handlers import router
import asyncio
import aiohttp
import logging



load_dotenv(r"D:\projects\telegram\telegrambot2\TOKEN.env")

TOKEN = getenv("BOT_TOKEN")

print("Бот запущен ✅")



dp = Dispatcher()
try:
    async def main():
        session = AiohttpSession(
            proxy="http://dRSgn6:kRngt0@181.177.89.21:9995"
        )

        bot = Bot(
            token=TOKEN,
            session=session
        )
        dp.include_router(router)

        await dp.start_polling(bot)


    if __name__ == "__main__":
        asyncio.run(main())
except KeyboardInterrupt:
    print("\nБот выключен")