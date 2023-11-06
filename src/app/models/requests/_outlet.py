from typing import Optional, Literal
from datetime import time
from pydantic import BaseModel
from app.models.requests.globals import LocationRequestModel


class AddMenuItemFoodOutletBodyParams(BaseModel):
    name: str
    price: int
    description: Optional[str] = None
    rating: Optional[float] = None
    size: Optional[str] = None
    cal: Optional[int] = None
    image: Optional[str] = None


class UpdateMenuItemFoodOutletBodyParams(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    size: Optional[str] = None
    cal: Optional[int] = None
    image: Optional[str] = None


class NewFoodOutletBodyParams(BaseModel):
    name: str
    location: Optional[LocationRequestModel] = None
    landmark: Optional[str] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    rating: Optional[float] = None
    image: Optional[str] = None


class UpdateFoodOutletBodyParams(BaseModel):
    name: Optional[str] = None
    location: Optional[LocationRequestModel] = None
    landmark: Optional[str] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    rating: Optional[float] = None
    image: Optional[str] = None


class FilterFoodOutletBodyParams(BaseModel):
    name: Optional[str] = None
    location: Optional[LocationRequestModel] = None
    landmark: Optional[str] = None
    current_time: Optional[time] = None
    rating: Optional[float] = None
    food_item: Optional[str] = None
