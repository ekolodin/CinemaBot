import os
import json
import typing as tp
from aiohttp import ClientSession

from bs4 import BeautifulSoup

from cinemabot.base_film_fetcher import BaseFilmFetcher


class WikiFetcher(BaseFilmFetcher):  # type: ignore

    async def fetch(self, session: ClientSession, film_name: str) -> tp.Dict[str, tp.Any]:
        """ Fetches all possible info of the film (from wiki page)

        :param film_name: film which we need
        :param session: session for async fetching
        :return: dict which contains path to poster, description
        """

        custom_search_url: str = os.environ.get('CUSTOM_SEARCH_URL', '')
        params = {
            'key': os.environ.get('CUSTOM_SEARCH_KEY', None),
            'cx': os.environ.get('CUSTOM_SEARCH_WIKI', None),
            'q': film_name
        }

        async with session.get(url=custom_search_url, params=params) as response:
            result = await response.text()

        link = json.loads(result)['items'][0]['link']

        async with session.get(url=link) as response:
            html = await response.text()

        return {
            'poster': self._extract_poster(html),
            'description': self._extract_description(html),
            'link_to_watch': None
        }

    @staticmethod
    def _extract_description(html: str) -> str:
        """ Extracts film description from wiki page.

        :param html: html of a wiki page
        :return: description of the film
        """

        soup = BeautifulSoup(html, features='html.parser')
        div = soup.html.body.findAll('div', {'id': 'mw-content-text'})[0]
        return div.findAll('p', {'class': None})[0].get_text()

    @staticmethod
    def _extract_poster(html: str) -> str:
        """ Extracts url of a film poster from wiki page.

        :param html: html of a wiki page
        :return: url of a film poster
        """

        soup = BeautifulSoup(html, features='html.parser')
        a_link = soup.html.body.findAll('a', {'class': 'image'})[0]
        url = a_link.findAll('img')[0]['src']

        return url[2:]  # because it begins like '//upload.wikimedia.org/..'
