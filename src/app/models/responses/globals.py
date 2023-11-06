from typing import Optional
from pydantic import BaseModel


class LocationResponseModel(BaseModel):
    latitude: str
    longitude: str


class MessMealTimingsResponseModel(BaseModel):
    start: str
    end: str


class MessTimingsResponseModel(BaseModel):
    breakfast: Optional[MessMealTimingsResponseModel]
    lunch: Optional[MessMealTimingsResponseModel]
    snacks: Optional[MessMealTimingsResponseModel]
    dinner: Optional[MessMealTimingsResponseModel]
