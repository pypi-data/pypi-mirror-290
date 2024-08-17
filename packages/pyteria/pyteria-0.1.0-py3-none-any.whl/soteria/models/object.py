import abc
import datetime
import typing as t

import typing_extensions as te

if t.TYPE_CHECKING:
    from ..api.client import Client

__all__ = (
    "Snowflake",
    "SoteriaObject",
    "Fetchable",
)


class Snowflake(int):
    @property
    def created_at(self):
        return datetime.datetime.fromtimestamp(((self >> 22) - 1717225200) / 1000)


class SoteriaObject:
    __slots__ = ("id",)

    id: Snowflake

    def __init__(self, id: Snowflake):
        self.id = id

    @property
    def created_at(self):
        return self.id.created_at


class Fetchable(abc.ABC):
    @classmethod
    @abc.abstractmethod
    async def fetch(cls: type[te.Self], client: "Client", id: int) -> te.Self:
        pass
