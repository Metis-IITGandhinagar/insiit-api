from typing import Optional
from pydantic import BaseModel


class LocationRequestModel(BaseModel):
    latitude: str
    longitude: str


class MessMealTimingsRequestModel(BaseModel):
    start: str
    end: str


class MessTimingsRequestModel(BaseModel):
    breakfast: Optional[MessMealTimingsRequestModel]
    lunch: Optional[MessMealTimingsRequestModel]
    snacks: Optional[MessMealTimingsRequestModel]
    dinner: Optional[MessMealTimingsRequestModel]
