import abc
import typing as t

import attrs
import typing_extensions as te

from .. import types
from .object import Fetchable, Snowflake, SoteriaObject

if t.TYPE_CHECKING:
    from ..api.client import Client
    from .user import SelfUser, User

__all__ = ("Post",)


class BasePost(abc.ABC):
    __slots__ = ()

    client: "Client"

    id: Snowflake
    author_id: Snowflake
    content: str
    # TODO: attachments

    _cached_likes: list["User"]

    @classmethod
    @abc.abstractmethod
    def from_payload(cls: type[te.Self], client: "Client", payload: types.Post) -> te.Self:
        pass

    async def fetch_likes(self) -> list["User"]:
        data: types.Likes = await self.client.request("GET", f"/posts/{self.id}/likes")
        users = [await self.client.get_or_fetch(Snowflake(id), User) for id in data["likes"]]
        self._cached_likes = users

        return users

    @property
    def likes(self) -> list["User"]:
        return self._cached_likes

    async def like(self) -> None:
        await self.client.request("PUT", f"/posts/{self.id}/like")

    async def unlike(self) -> None:
        await self.client.request("DELETE", f"/posts/{self.id}/like")


@attrs.define(kw_only=True, slots=True)
class Post(SoteriaObject, Fetchable, BasePost):
    client: "Client" = attrs.field(repr=False)

    id: Snowflake = attrs.field(repr=True)
    author_id: Snowflake = attrs.field(repr=False)
    content: str = attrs.field(repr=True)

    _cached_author: t.Optional["User"] = attrs.field(init=False, repr=False)
    _cached_likes: list["User"] = attrs.field(init=False, repr=False)

    @classmethod
    def from_payload(cls, client: "Client", payload: types.Post):
        self = cls(
            client=client,
            id=Snowflake(payload["id"]),
            author_id=Snowflake(payload["author"]),
            content=payload["content"],
        )
        return self

    @classmethod
    async def fetch(cls, client: "Client", id: int):
        data: types.Post = await client.request("GET", f"/posts/{id}")
        return cls.from_payload(client, data)

    async def fetch_author(self) -> "User":
        from .user import User

        user = await self.client.get_or_fetch(self.author_id, User)
        self._cached_author = user

        return user

    @property
    def author(self) -> t.Optional["User"]:
        return self._cached_author


@attrs.define(kw_only=True, slots=True)
class SelfPost(SoteriaObject, BasePost):
    client: "Client" = attrs.field(repr=False)

    id: Snowflake = attrs.field(repr=True)
    author_id: Snowflake = attrs.field(repr=False)
    content: str = attrs.field(repr=True)

    _cached_author: t.Optional["SelfUser"] = attrs.field(init=False, repr=False)
    _cached_likes: list["User"] = attrs.field(init=False, repr=False)

    @classmethod
    def from_payload(cls, client: "Client", payload: types.Post):
        self = cls(
            client=client,
            id=Snowflake(payload["id"]),
            author_id=Snowflake(payload["author"]),
            content=payload["content"],
        )
        return self

    async def fetch_author(self) -> "SelfUser":
        self_user = await self.client.fetch_self()
        self._cached_author = self_user

        return self_user

    @property
    def author(self) -> t.Optional["SelfUser"]:
        return self._cached_author

    async def edit(self, content: str):
        payload: dict[str, t.Any] = {"content": content}

        res: types.Post = await self.client.request("PATCH", f"/posts/{id}", json=payload)
        return SelfPost.from_payload(self.client, res)

    async def delete(self):
        await self.client.request("DELETE", f"/posts/{id}")
