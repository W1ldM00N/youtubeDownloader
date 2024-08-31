import asyncio
import logging
import sys
import os
import re

import pytube.exceptions
from pytube import YouTube
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import json

# opening json file with configs
with open("config.json") as f:
    templates = json.load(f)

Token = templates["Token"]

dp = Dispatcher()


@dp.callback_query()
async def video_downloader(callback_query: CallbackQuery) -> None:
    data = callback_query.data
    splitted_data = data.split("<>")
    code = splitted_data[0]
    url = splitted_data[1]
    try:
        if code == 'mp3':
            # downloading video using youTube link
            yt = YouTube(url)
            stream = yt.streams.get_audio_only()
            audio_path = stream.download()
            audio = FSInputFile(audio_path)
            await callback_query.message.answer_audio(audio=audio)
            # removing file
            os.remove(audio_path)
        elif code == '480':
            yt = YouTube(url)
            stream = yt.streams.filter(file_extension='mp4', resolution='480p').first()
            video_path = stream.download()
            video = FSInputFile(video_path)
            await callback_query.message.answer_video(video=video)
            # removing file
            os.remove(video_path)
        elif code == '720':
            yt = YouTube(url)
            stream = yt.streams.filter(file_extension='mp4', resolution='720p').first()
            video_path = stream.download()
            video = FSInputFile(video_path)
            await callback_query.message.answer_video(video=video)
            # removing file
            os.remove(video_path)
        elif code == '1080':
            yt = YouTube(url)
            stream = yt.streams.filter(file_extension='mp4', resolution='1080p').first()
            video_path = stream.download()
            video = FSInputFile(video_path)
            await callback_query.message.answer_video(video=video)
            # removing file
            os.remove(video_path)
    except pytube.exceptions.VideoUnavailable:
        await callback_query.message.answer(text='sorry, your link does not work')


# start command handler
@dp.message(CommandStart())
async def starter(message: Message) -> None:
    text = f"""
        Hello, {html.bold(message.from_user.full_name)}! I am here to download youtube videos for you! Just send an URL
    """
    await message.answer(text)


# every message handler
@dp.message()
async def everyMessageHandler(message: Message) -> None:
    # getting link from message
    text = message.text
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, text)
    if not url:
        await message.answer("sorry, we can not find url!")
    else:
        markup_option_one = InlineKeyboardButton(text='mp3', callback_data=f"mp3<>{url[0][0]}")
        markup_option_two = InlineKeyboardButton(text='480px', callback_data=f"480<>{url[0][0]}")
        markup_option_three = InlineKeyboardButton(text='720px', callback_data=f"720<>{url[0][0]}")
        markup_option_four = InlineKeyboardButton(text='1080px', callback_data=f"1080<>{url[0][0]}")
        keyboard = [
            [markup_option_one, markup_option_two],
            [markup_option_three, markup_option_four]
        ]
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

        await message.answer("what type and quality would you like?", reply_markup=markup)


# bot starter
async def main() -> None:
    bot = Bot(token=Token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

# logging
if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        exit()
