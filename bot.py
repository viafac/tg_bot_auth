import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    print('Bot is running...')
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Exit')
    finally:
        loop.close()
