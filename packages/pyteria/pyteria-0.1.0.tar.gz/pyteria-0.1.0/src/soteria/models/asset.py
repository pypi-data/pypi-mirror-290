import contextlib
import os
import pathlib
import typing as t

import aiohttp
import attrs

if t.TYPE_CHECKING:
    from ..api.client import Client

__all__ = ("Asset",)


def _ensure_path(p: str | os.PathLike[str] | pathlib.Path):
    if not isinstance(p, pathlib.Path):
        p = pathlib.Path(p)

    return p


@attrs.define(slots=True)
class WebReader:
    resp: aiohttp.ClientResponse

    async def __aiter__(self) -> t.AsyncGenerator[t.Any, bytes]:
        stream = self.resp.content
        while not stream.at_eof():
            chunk, _ = await stream.readchunk()
            yield chunk


@attrs.define(kw_only=True, slots=True)
class Asset:
    client: "Client"
    asset_id: str

    @property
    def url(self) -> str:
        return f"{self.client.cdn_url}/{self.asset_id}"
    
    @contextlib.asynccontextmanager
    async def stream(self):
        client = aiohttp.ClientSession()
        req = client.request("GET", self.url)

        try:
            resp = await req.__aenter__()
            yield WebReader(resp)
        finally:
            await req.__aexit__(None, None, None)
            await client.close()

    async def read(self) -> bytes:
        buffer = bytearray()
        async with self.stream() as stream:
            async for chunk in stream:
                buffer.extend(chunk)

        return bytes(buffer)

    async def save(self, path: str | os.PathLike[str] | pathlib.Path) -> None:
        path = _ensure_path(path)
        contents = await self.read()
        path.write_bytes(contents)
