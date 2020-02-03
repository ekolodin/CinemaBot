import os
import json
import typing as tp

from aiohttp import ClientSession

from cinemabot.base_film_fetcher import BaseFilmFetcher


class KinopoiskFetcher(BaseFilmFetcher):  # type: ignore

    async def fetch(self, session: ClientSession, film_name: str) -> tp.Dict[str, tp.Any]:
        """ Fetches link to watch the film (from kinopoisk page)

        :param film_name: film which we need
        :param session: session for async fetching
        :return: dict which contains link to watch the film
        """
        custom_search_url: str = os.environ.get('CUSTOM_SEARCH_URL', '')
        params = {
            'key': os.environ.get('CUSTOM_SEARCH_KEY', None),
            'cx': os.environ.get('CUSTOM_SEARCH_KINOPOISK', None),
            'q': film_name
        }

        async with session.get(url=custom_search_url, params=params) as response:
            result = await response.text()

        link = json.loads(result)['items'][0]['link']

        return {
            'poster': None,
            'description': None,
            'link_to_watch': link
        }
