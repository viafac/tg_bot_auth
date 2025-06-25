import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from bot.handlers.user_registration import user_reg_router

load_dotenv()


async def main():
    logging.basicConfig(level=logging.INFO)

    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN is not set in environment variables.")

    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(user_reg_router)

    logging.info("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")
