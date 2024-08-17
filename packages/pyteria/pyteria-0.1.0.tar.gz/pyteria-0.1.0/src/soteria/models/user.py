import abc
import typing as t

import attrs
import typing_extensions as te

from .. import types
from .object import Fetchable, Snowflake, SoteriaObject

if t.TYPE_CHECKING:
    from ..api.client import Client
    from .post import Post

__all__ = (
    "User",
    "SelfUser",
)


class BaseUser(abc.ABC):
    __slots__ = ()

    client: "Client"

    id: Snowflake
    username: str
    display_name: t.Optional[str]
    description: t.Optional[str]
    visible: bool
    avatar: str
    banner: t.Optional[str]

    _cached_followers: list["User"]
    _cached_followees: list["User"]
    _cached_posts: list["Post"]
    _cached_liked_posts: list["Post"]

    @classmethod
    @abc.abstractmethod
    def from_payload(cls: type[te.Self], client: "Client", payload: types.User) -> te.Self:
        pass

    async def fetch_followers(self) -> list["User"]:
        data: types.Followers = await self.client.request("GET", f"/users/{self.id}/followers")
        users = [await self.client.get_or_fetch(Snowflake(id), User) for id in data["followers"]]
        self._cached_followers = users

        return users

    async def fetch_followees(self) -> list["User"]:
        data: types.Followees = await self.client.request("GET", f"/users/{self.id}/followees")
        users = [await self.client.get_or_fetch(Snowflake(id), User) for id in data["followees"]]
        self._cached_followees = users

        return users

    async def fetch_posts(self) -> list["Post"]:
        from .post import Post

        data: list[types.Post] = await self.client.request("GET", f"/users/{self.id}/posts")
        posts: list["Post"] = []

        for payload in data:
            if not (obj := await self.client.cache.retrieve(Snowflake(payload["id"]), Post)):
                obj = Post.from_payload(self.client, payload)
                await self.client.cache.store(obj)

            posts.append(obj)

        self._cached_posts = posts
        return posts

    async def fetch_liked_posts(self) -> list["Post"]:
        from .post import Post

        data: list[str] = await self.client.request("GET", f"/users/{self.id}/posts/likes")
        posts: list["Post"] = [await self.client.get_or_fetch(Snowflake(id), Post) for id in data]

        self._cached_liked_posts = posts
        return posts

    @property
    def followers(self) -> list["User"]:
        return self._cached_followers

    @property
    def followees(self) -> list["User"]:
        return self._cached_followees

    @property
    def posts(self) -> list["Post"]:
        return self._cached_posts

    @property
    def liked_posts(self) -> list["Post"]:
        return self._cached_liked_posts


@attrs.define(kw_only=True, slots=True)
class User(SoteriaObject, Fetchable, BaseUser):
    client: "Client" = attrs.field(repr=False)

    id: Snowflake = attrs.field(repr=True)
    username: str = attrs.field(repr=True)
    display_name: t.Optional[str] = attrs.field(repr=True)
    description: t.Optional[str] = attrs.field(repr=False)
    visible: bool = attrs.field(repr=True)
    avatar: str = attrs.field(repr=False)
    banner: t.Optional[str] = attrs.field(repr=False)

    _cached_followers: list["User"] = attrs.field(init=False, repr=False)
    _cached_followees: list["User"] = attrs.field(init=False, repr=False)
    _cached_posts: list["Post"] = attrs.field(init=False, repr=False)
    _cached_liked_posts: list["Post"] = attrs.field(init=False, repr=False)

    @classmethod
    def from_payload(cls, client: "Client", payload: types.User):
        self = cls(
            client=client,
            id=Snowflake(payload["id"]),
            username=payload["username"],
            display_name=payload.get("display_name"),
            description=payload.get("description"),
            visible=payload["visible"],
            avatar=payload["avatar"],
            banner=payload.get("banner"),
        )
        return self

    @classmethod
    async def fetch(cls, client: "Client", id: int):
        data: types.User = await client.request("GET", f"/users/{id}")
        return cls.from_payload(client, data)

    async def follow(self) -> None:
        await self.client.request("POST", f"/users/{self.id}/followers")

    async def unfollow(self) -> None:
        await self.client.request("DELETE", f"/users/{self.id}/followers")


@attrs.define(kw_only=True, slots=True)
class SelfUser(SoteriaObject, BaseUser):
    client: "Client" = attrs.field(repr=False)

    id: Snowflake = attrs.field(repr=True)
    username: str = attrs.field(repr=True)
    display_name: t.Optional[str] = attrs.field(repr=True)
    description: t.Optional[str] = attrs.field(repr=False)
    visible: bool = attrs.field(repr=True)
    avatar: str = attrs.field(repr=False)
    banner: t.Optional[str] = attrs.field(repr=False)

    _cached_followers: list["User"] = attrs.field(init=False, repr=False)
    _cached_followees: list["User"] = attrs.field(init=False, repr=False)
    _cached_blocked: list["User"] = attrs.field(init=False, repr=False)
    _cached_posts: list["Post"] = attrs.field(init=False, repr=False)
    _cached_liked_posts: list["Post"] = attrs.field(init=False, repr=False)

    @classmethod
    def from_payload(cls, client: "Client", payload: types.User):
        self = cls(
            client=client,
            id=Snowflake(payload["id"]),
            username=payload["username"],
            display_name=payload.get("display_name"),
            description=payload.get("description"),
            visible=payload["visible"],
            avatar=payload["avatar"],
            banner=payload.get("banner"),
        )
        return self

    async def fetch_blocked(self) -> list["User"]:
        data: types.Blocked = await self.client.request("GET", "/users/@me/blocked")
        users = [await self.client.get_or_fetch(Snowflake(id), User) for id in data["blocked"]]
        self._cached_blocked = users

        return users

    @property
    def blocked(self) -> list["User"]:
        return self._cached_blocked

    async def edit_account(
        self,
        *,
        username: t.Optional[str] = None,
        email: t.Optional[str] = None,
        password: t.Optional[str] = None,
        visible: t.Optional[bool] = None,
        current_email: t.Optional[str] = None,
        current_password: t.Optional[str] = None,
    ):
        payload: dict[str, t.Any] = dict(
            filter(
                lambda x: x[1] is not None,
                {
                    "username": username,
                    "email": email,
                    "password": password,
                    "visible": visible,
                    "current_email": current_email,
                    "current_password": current_password,
                }.items(),
            )
        )

        res: types.User = await self.client.request("PATCH", "/users/@me", json=payload)
        return SelfUser.from_payload(self.client, res)

    async def edit_profile(
        self,
        *,
        display_name: t.Optional[str] = None,
        description: t.Optional[str] = None,
    ):
        payload: dict[str, t.Any] = dict(
            filter(
                lambda x: x[1] is not None,
                {
                    "display_name": display_name,
                    "description": description,
                }.items(),
            )
        )

        res: types.User = await self.client.request("PATCH", "/users/profile/@me", json=payload)
        return SelfUser.from_payload(self.client, res)
