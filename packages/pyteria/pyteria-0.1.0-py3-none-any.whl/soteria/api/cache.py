import abc
import typing as t

from ..models.object import Snowflake, SoteriaObject

ObjectT = t.TypeVar("ObjectT", bound=SoteriaObject)

__all__ = (
    "Cache",
    "MemoryCache",
)


class Cache(abc.ABC):
    __slots__ = ()

    @abc.abstractmethod
    async def store(self, object: SoteriaObject) -> None:
        pass

    @abc.abstractmethod
    async def retrieve(self, id: Snowflake, type_: type[ObjectT]) -> t.Optional[ObjectT]:
        pass

    @abc.abstractmethod
    async def remove(self, object: SoteriaObject) -> None:
        pass


class MemoryCache(Cache):
    __slots__ = ("_memory",)

    _memory: dict[Snowflake, SoteriaObject]

    def __init__(self) -> None:
        self._memory = {}

    async def store(self, object: SoteriaObject) -> None:
        # TODO: error handling?
        if object.id in self._memory:
            return

        self._memory[object.id] = object

    async def retrieve(self, id: Snowflake, type_: type[ObjectT]) -> t.Optional[ObjectT]:
        obj = self._memory.get(id)

        if not isinstance(obj, type_):
            return None

        return obj

    async def remove(self, object: SoteriaObject) -> None:
        pass
