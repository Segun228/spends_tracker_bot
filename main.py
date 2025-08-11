import os
import logging
import asyncio

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers.router import router
import app.handlers.handlers
from app.middlewares.antiflud import ThrottlingMiddleware


load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

token = os.getenv("BOT_TOKEN")
if not token or token == "":
    raise ValueError("No token was provided")

bot:Bot = Bot(token = token)
dp = Dispatcher()
dp.message.middleware(ThrottlingMiddleware(limit=0.5))

async def main():
    try:
        logging.info("Bot started")
        dp.include_router(router)
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logging.info("Bot stopped")
    except ValueError as e:
        logging.error(e)
    except Exception as e:
        logging.error(e)



if __name__ == "__main__":
    asyncio.run(main())
