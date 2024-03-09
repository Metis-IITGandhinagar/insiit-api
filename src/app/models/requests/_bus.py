from pydantic import BaseModel
from typing import Union, List
from app.models.requests.globals import LocationRequestModel


class NewBusTypeBodyParams(BaseModel):
    name: str


class UpdateBusTypeBodyParams(BaseModel):
    name: Union[str, None] = None


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


class NewBusScheduleBodyParams(BaseModel):
    route_id: int
    bus_type_id: int
    start_time: str
    end_time: Union[str, None] = None
    via_stops_times: Union[List[Union[str, None]], None] = None


class UpdateBusScheduleBodyParams(BaseModel):
    route_id: Union[int, None] = None
    bus_type_id: Union[int, None] = None
    start_time: Union[str, None] = None
    end_time: Union[str, None] = None
    via_stops_times: Union[List[Union[str, None]], None] = None
