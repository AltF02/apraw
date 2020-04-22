from copy import deepcopy
from typing import Any, Dict, Optional, TypeVar

Reddit = TypeVar("Reddit")


class APRAWBase:

    @staticmethod
    def _safely_add_arguments(argument_dict, key, **new_arguments):
        value = deepcopy(argument_dict[key]) if key in argument_dict else {}
        value.update(new_arguments)
        argument_dict[key] = value

    @classmethod
    def parse(cls, data: Dict[str, Any], reddit: Reddit) -> Any:
        return cls(reddit, _data=data)

    def __init__(self, reddit: Reddit, _data: Optional[Dict[str, Any]]):
        self._reddit = reddit
        if _data:
            for attribute, value in _data.items():
                setattr(self, attribute, value)
