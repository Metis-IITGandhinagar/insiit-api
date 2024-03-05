from pydantic import BaseModel
from typing import Union, List
from app.models.requests.globals import LocationRequestModel


class NewBusStopBodyParams(BaseModel):
    name: str
    location: Union[LocationRequestModel, None] = None
    landmark: Union[str, None] = None


class UpdateBusStopBodyParams(BaseModel):
    name: Union[str, None] = None
    location: Union[LocationRequestModel, None] = None
    landmark: Union[str, None] = None


class NewBusRouteBodyParams(BaseModel):
    name: str
    from_stop_id: int
    to_stop_id: int
    via_stops: List[int]


class UpdateBusRouteBodyParams(BaseModel):
    name: Union[str, None] = None
    from_stop_id: Union[int, None] = None
    to_stop_id: Union[int, None] = None
    via_stops: Union[List[int], None] = None
