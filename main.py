import asyncio
import logging
import sys
import os
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import json

with open("config.json") as f:
    templates = json.load(f)

Token = os.getenv(templates["Token"])

dp = Dispatcher()


@dp.message(CommandStart())
async def Starter():
    pass


async def main() -> None:
    bot = Bot(token=Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
