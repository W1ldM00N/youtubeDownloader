import asyncio
import logging
import sys
import re
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import json

with open("config.json") as f:
    templates = json.load(f)

Token = templates["Token"]

dp = Dispatcher()


@dp.message(CommandStart())
async def Starter(message: Message) -> None:
    text = f"""
        Hello, {html.bold(message.from_user.full_name)}! I am here to download youtube videos for you! Just send an URL
    """
    await message.answer(text)


@dp.message()
async def get_link(message: Message) -> None:
    text = message.text
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, text)
    print(url)


async def main() -> None:
    bot = Bot(token=Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
