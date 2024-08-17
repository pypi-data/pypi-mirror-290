import typing as t

__all__ = (
    "Post",
    "Likes",
)


class Attachment(t.TypedDict):
    id: str
    type: str
    post: str


class Post(t.TypedDict):
    id: str
    author: str
    content: str
    created_at: str
    attachments: list[Attachment]


class Likes(t.TypedDict):
    count: int
    likes: list[str]
