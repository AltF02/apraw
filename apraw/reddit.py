import configparser
import os

from itertools import islice
from typing import IO, Any, Dict, Generator, Optional, Sequence, Type, Union

from aprawcore import (requestor, exceptions)
from aprawcore.requestor import Requestor

from . import models
from .exceptions import ClientException

Subreddit = models.Subreddit
Redditor = models.Redditor


class Reddit:

    @property
    def _next_unique(self):
        value = self._unique_counter
        self._unique_counter += 1
        return value

    @property
    def read_only(self) -> bool:
        return self._core == self._read_only_core

    @read_only.setter()
    def read_only(self, value: bool) -> None:
        if value:
            self._core = self._read_only_core
        elif self._authorized_core is None:
            raise ClientException(
                "read_only cannot be unset as only the "
                "ReadOnlyAuthorizer is available."
            )
        else:
            self._core = self._authorized_core

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        """Handle the context manager close."""

    def __init__(
            self,
            site_name: str = None,
            requestor_class: Optional[Type[Requestor]] = None,
            requestor_kwargs: Dict[str, Any] = None,
            **config_settings: str
    ):
        self._core = self._authorized_core = self._read_only_core = None
        self._objector = None
        self._unique_counter = 0

        try:
            config_section = site_name or os.getenv("praw_site") or "DEFAULT"
            # self.config = Config(config_section, **config_settings)
        except configparser.NoSectionError as exc:
            raise exc

        required_message = (
            "Required configuration setting {!r} missing. \n"
            "This setting can be provided in a praw.ini file, "
            "as a keyword argument to the `Reddit` class "
            "constructor, or as an environment variable."
        )

    async def get(self, path: str, params: Optional[Union[str, Dict[str, str]]] = None):
        data = await self.request("GET", path, params=params)
        return self._objector.objectify(data)

    async def redditor(self, name: Optional[str] = None, fullname: Optional[str] = None
                       ) -> Redditor:
        return models.Redditor(self, name=name, fullname=fullname)

    async def request(
            self,
            method: str,
            path: str,
            params: Optional[Union[str, Dict[str, str]]] = None,
            data: Optional[
                Union[Dict[str, Union[str, Any]], bytes, IO, str]
            ] = None,
            files: Optional[Dict[str, IO]] = None,
    ) -> Any:
        return await self._core.request(
            method, path, data=data, files=files, params=params
        )

