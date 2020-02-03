import typing as tp

from abc import ABC, abstractmethod
from aiohttp import ClientSession


class BaseFilmFetcher(ABC):
    @abstractmethod
    async def fetch(self, session: ClientSession, film_name: str) -> tp.Dict[str, tp.Any]:
        pass
