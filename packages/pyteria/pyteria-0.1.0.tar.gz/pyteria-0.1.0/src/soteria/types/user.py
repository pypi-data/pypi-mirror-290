import typing as t

__all__ = (
    "User",
    "Followers",
    "Followees",
    "Blocked",
)


class User(t.TypedDict):
    id: str
    username: str
    display_name: t.Optional[str]
    description: t.Optional[str]
    created_at: str
    visible: bool
    avatar: str
    banner: t.Optional[str]


class Followers(t.TypedDict):
    count: int
    followers: list[str]


class Followees(t.TypedDict):
    count: int
    followees: list[str]


class Blocked(t.TypedDict):
    blocked: list[str]
