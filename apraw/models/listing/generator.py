from copy import deepcopy
from typing import Any, Dict, Iterator, Optional, TypeVar

from apraw.models.base import APRAWBase
from apraw.models.listing.listing import FlairListing

Reddit = TypeVar("Reddit")


class ListingGenerator(APRAWBase):

    def __init__(self, reddit: Reddit, url: str, limit: int = 100, params: Optional[Dict[str, str]] = None):
        super().__init__(reddit, _data=None)
        self._exhausted = False
        self._listing = None
        self._list_index = None
        self.limit = limit
        self.params = deepcopy(params) if params else {}
        self.params["limit"] = limit or 1024
        self.url = url
        self.yielded = 0

    def __iter__(self) -> Iterator[Any]:
        return self

    def __next__(self) -> Any:
        if self.limit is not None and self.yielded >= self.limit:
            raise StopIteration()

        if self._listing is None or self._list_index >= len(self._listing):
            self._next_batch()

        self._list_index += 1
        self.yielded += 1
        return self._listing[self._list_index - 1]

    def _next_batch(self):
        if self._exhausted:
            raise StopIteration()

        self._listing = self._reddit.get(self.url, params=self.params)
        if isinstance(self._listing, list):
            self._listing = self._listing[1]  # for submission duplicates
        elif isinstance(self._listing, dict):
            self._listing = FlairListing(self._reddit, self._listing)
        self._list_index = 0

        if not self._listing:
            raise StopIteration()

        if self._listing.after and self._listing.after != self.params.get(
            "after"
        ):
            self.params["after"] = self._listing.after
        else:
            self._exhausted = True

