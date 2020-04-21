from typing import Any, Optional

from ..base import APRAWBase


class Listing(APRAWBase):

    CHILD_ATTRIBUTE = "children"

    def __len__(self) -> int:
        """Return the number of items in the Listing."""
        return len(getattr(self, self.CHILD_ATTRIBUTE))

    def __getitem__(self, index: int) -> Any:
        """Return the item at position index in the list."""
        return getattr(self, self.CHILD_ATTRIBUTE)[index]

    def __setattr__(self, attribute: str, value: Any):
        """Objectify the CHILD_ATTRIBUTE attribute."""
        if attribute == self.CHILD_ATTRIBUTE:
            value = self._reddit._objector.objectify(value)
        super().__setattr__(attribute, value)


class FlairListing(Listing):

    CHILD_ATTRIBUTE = "users"

    @property
    async def after(self) -> Optional[Any]:
        return getattr(self, "next", None)
