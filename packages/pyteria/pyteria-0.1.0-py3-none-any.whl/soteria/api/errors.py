import json
import typing as t

from ..types.errors import HTTPErrorData

__all__ = (
    "SoteriaError",
    "HTTPError",
)


class SoteriaError(Exception):
    pass


class HTTPError(SoteriaError):
    __slots__ = ("status", "data", "message")

    data: t.Union[HTTPErrorData, str]
    message: str
    status: int

    def __init__(self, status: int, content: str, content_type: str):
        self.status: int = status

        if content_type == "application/json":
            self.data = t.cast(HTTPErrorData, json.loads(content))
            self.message = self.data["message"]
        else:
            self.data = content
            self.message = content

        super().__init__(f"Status code ({self.status}), message:\n{self.message}")
