import typing as t

__all__ = ("HTTPErrorData",)


class HTTPErrorData(t.TypedDict):
    code: int
    message: str
