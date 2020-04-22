from typing import Any, Dict, TypeVar, Union
from urllib.parse import urlparse

from ..base import APRAWBase

Reddit = TypeVar("Reddit")


class RedditBase(APRAWBase):

    def __init__(self, reddit: Reddit, _data: Dict[str, Any]):
        super().__init__(reddit, _data=_data)
        self._fetched = False


