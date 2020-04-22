from json import dumps
from typing import Any, Dict, List, Optional, TypeVar

from ...const import API_PATH
from ..listing.mixins import RedditLisingMixin
from .base import RedditBase
from .mixins import FullnameMixin, MessageableMixin

_Redditor = TypeVar("_Redditor")
Reddit = TypeVar("Reddit")
Subreddit = TypeVar("Subreddit")

class Redditor(
    MessageableMixin, RedditorListingMixin, FullnameMixin, RedditBase
):

    @classmethod
    async def _from_data(cls, reddit, data):
        if data == "[deleted]":
            return None
        return cls(reddit, data)

    @property
    def _kind(self):
        return self._reddit.config.kinds['redditor']

    @property
    def _path(self):
        return API_PATH["user"].format(user=self)

    def __init__(self, reddit: Reddit, name: Optional[str] = None,
                 fullname: Optional[str] = None,
                 _data: Optional[Dict[str, Any]] = None):

        if (name, fullname, _data).count(None) != 2:
            raise TypeError(
                "Exactly one of `name`, `fullname`, or `_data` must be "
                "provided."
            )
        if _data:
            assert (isinstance(_data, dict) and "name" in _data), "Please file a bug with APRAW"
            super().__init__(reddit, _data=_data)
            self._listing_use_sort = True
            if name:
                self.name = name
            elif fullname:
                self._fullname = fullname

    async def _fetch_username(self, fullname):
        return await self._reddit.get(API_PATH["user_by_fullname"], params={"ids": fullname})[fullname]["name"]

    async def _fetch_info(self):
        if hasattr(self, "_fullname"):
            self.name = await self._fetch_username(self._fullname)
        return "user_about", {"user": self.name}, None

    async def _fetch_data(self):
        name, fields, params = await self._fetch_info()
        path = API_PATH[name].format(**fields)
        return await self._reddit.request("GET", path, params)

    async def _fetch(self):
        data = await self._fetch_data()
        data = data["data"]
        other = type(self)(self._reddit, _data=data)
        self.__dict__.update(other.__dict__)
        self._fetched = True

    async def _friend(self, method, data):
        url = API_PATH["friend_v1"].format(user=self)
        await self._reddit.request(method, url, data=dumps(data))

    async def block(self):
        await self._reddit.post(API_PATH["block_user"], params={"account_id": self.fullname})

    async def friend(self, note: str = None):
        await self._friend("PUT", data={"note": note} if note else {})

    async def friend_info(self) -> _Redditor:
        return await self._reddit.get(API_PATH["friend_v1"].format(user=self))

    async def gild(self, months: int = 1):
        if months < 1 or months > 36:
            raise TypeError("Months must be between 1 and 36")
        await self._reddit.post(API_PATH["gild_user"].format(username=self),
                                data={"months": months},)

    async def moderated(self) -> List[Subreddit]:
        modded_data = await self._reddit.get(API_PATH["moderated"].format(user=self))
        if "data" not in modded_data:
            return []
        else:
            subreddits = [await self._reddit.subreddit(x["sr"]) for x in modded_data["data"]]
            return subreddits

    async def unblock(self):
        data = {
            "container": await self._reddit.user.me().fullname,
            "name": str(self),
            "type": "enemy",
        }
        url = API_PATH["unfriend"].format(subreddit="all")
        await self._reddit.post(url, data=data)

    def unfriend(self):
        await self._friend(method="DELETE", data={"id": str(self)})

