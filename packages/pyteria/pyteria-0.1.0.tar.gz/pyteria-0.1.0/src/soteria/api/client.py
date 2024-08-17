import json as jsonmod
import logging
import typing as t

import aiohttp

from .. import types
from ..models.object import Fetchable, Snowflake, SoteriaObject
from ..models.post import SelfPost
from ..models.user import SelfUser
from .cache import Cache
from .errors import HTTPError

ObjectT = t.TypeVar("ObjectT", bound=SoteriaObject)

_log = logging.getLogger(__name__)

__all__ = ("Client",)


class Client:
    __slots__ = ("_http", "url", "cdn_url", "auth", "cache", "_user")

    _http: t.Optional[aiohttp.ClientSession]
    url: str
    cdn_url: str
    auth: t.Optional[str]
    cache: Cache
    _user: t.Optional[SelfUser]

    def __init__(
        self,
        *,
        auth: t.Optional[str] = None,
        url: t.Optional[str] = None,
        cdn_url: t.Optional[str] = None,
        cache: Cache
    ):
        self._http = None
        self.url = url or "https://api.soteria.social"
        self.cdn_url = cdn_url or (self.url + "/files")
        self.auth = auth
        self.cache = cache

    @property
    def http(self):
        if not self._http:
            self._http = aiohttp.ClientSession()

        return self._http

    # TODO: multipart forms
    async def request(
        self,
        method: str,
        route: str,
        *,
        params: t.Optional[dict[str, t.Any]] = None,
        json: t.Optional[t.Any] = None,
        auth: t.Optional[str] = None,
    ):
        auth = auth or self.auth
        headers = {"Authorization": f"Bearer {auth}"}
        url = self.url + route

        async with self.http.request(
            method,
            url,
            params=params,
            json=json,
            headers=headers,
        ) as resp:
            _log.debug("Made request to %s with method %s.", url, method)

            content = await resp.text()

            if resp.status > 400:
                raise HTTPError(resp.status, content, resp.content_type)

            return jsonmod.loads(content)

    async def close(self):
        if self._http is None:
            return

        await self._http.close()
        self._http = None

    async def get_or_fetch(self, id: Snowflake, type_: type[ObjectT]) -> ObjectT:
        if not issubclass(type_, Fetchable):
            raise TypeError(f"{type_.__name__} cannot be fetched!")

        obj = await self.cache.retrieve(id, type_)

        if obj is not None:
            return obj

        obj = await type_.fetch(self, id)
        return obj

    async def fetch_self(self) -> SelfUser:
        data: types.User = await self.request("GET", "/users/@me")
        user = SelfUser.from_payload(self, data)

        self._user = user
        return user

    @property
    def user(self) -> SelfUser | None:
        return self._user

    async def create_post(self, content: str) -> SelfPost:
        payload: dict[str, t.Any] = {"content": content}
        res: types.Post = await self.request("POST", "/posts", json=payload)

        post = SelfPost.from_payload(self, res)
        await self.cache.store(post)

        return post
