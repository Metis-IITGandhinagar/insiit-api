from pydantic import BaseModel
from typing import Optional
from typing_extensions import TypedDict


class NewMessBodyParams(BaseModel):
    name: str
    location: Optional[dict[str, str]] = None
    landmark: Optional[str] = None
    timings: Optional[dict[str, str]] = None
    rating: Optional[float] = None
    image: Optional[str] = None


class UpdateMessBodyParams(BaseModel):
    name: Optional[str] = None
    location: Optional[dict[str, str]] = None
    landmark: Optional[str] = None
    timings: Optional[dict[str, str]] = None
    rating: Optional[float] = None
    image: Optional[str] = None


class DayMenuBodyParams(TypedDict):
    breakfast: list[int] | None
    lunch: list[int] | None
    snacks: list[int] | None
    dinner: list[int] | None


class NewMessMenuBodyParams(BaseModel):
    month: int
    year: int
    monday: Optional[DayMenuBodyParams] = None
    tuesday: Optional[DayMenuBodyParams] = None
    wednesday: Optional[DayMenuBodyParams] = None
    thursday: Optional[DayMenuBodyParams] = None
    friday: Optional[DayMenuBodyParams] = None
    saturday: Optional[DayMenuBodyParams] = None
    sunday: Optional[DayMenuBodyParams] = None


class UpdateMessMenuBodyParams(BaseModel):
    monday: Optional[DayMenuBodyParams] = None
    tuesday: Optional[DayMenuBodyParams] = None
    wednesday: Optional[DayMenuBodyParams] = None
    thursday: Optional[DayMenuBodyParams] = None
    friday: Optional[DayMenuBodyParams] = None
    saturday: Optional[DayMenuBodyParams] = None
    sunday: Optional[DayMenuBodyParams] = None


class NewMessMenuItemBodyParams(BaseModel):
    name: str
    description: Optional[str] = None
    rating: Optional[float] = None
    cal: Optional[int] = None
    image: Optional[str] = None


class UpdateMessMenuItemBodyParams(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    cal: Optional[int] = None
    image: Optional[str] = None
