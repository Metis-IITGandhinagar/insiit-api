from typing_extensions import TypedDict


class Location(TypedDict):
    latitude: str
    longitude: str


class Rating(TypedDict):
    total: float
    count: int
