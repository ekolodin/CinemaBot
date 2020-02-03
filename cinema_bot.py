import os

import aiohttp
from aiohttp import ClientSession
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from cinemabot.wiki_fetcher import WikiFetcher
from cinemabot.kinopoisk_fetcher import KinopoiskFetcher

proxy_host = os.environ.get('PROXY', None)
proxy_credentials = os.environ.get('PROXY_CREDS', None)
proxy_auth = None

if proxy_credentials:
    login, password = proxy_credentials.split(':')
    proxy_auth = aiohttp.BasicAuth(login=login, password=password)

bot = Bot(token=os.environ['BOT_TOKEN'], proxy=proxy_host, proxy_auth=proxy_auth)
dp = Dispatcher(bot)
wiki_fetcher = WikiFetcher()
link_to_watch_fetcher = KinopoiskFetcher()


@dp.message_handler(commands=['help', 'start'])
async def _help(message: types.Message) -> None:
    await message.reply("Hello, I'm cinema bot\nPlease, type your movie :)\n")


@dp.message_handler()
async def _get_film_info(message: types.Message) -> None:
    async with ClientSession() as session:
        wiki_result = await wiki_fetcher.fetch(session, message.text)
        kinopoisk_result = await link_to_watch_fetcher.fetch(session, message.text)

        caption = '{}\nLink to watch: {}'.format(wiki_result['description'], kinopoisk_result['link_to_watch'])

        await message.reply_photo(photo=wiki_result['poster'], caption=caption)


if __name__ == '__main__':
    executor.start_polling(dp)
