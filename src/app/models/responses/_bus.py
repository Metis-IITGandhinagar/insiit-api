from pydantic import BaseModel
from typing import List, Union, Literal
from app.models.responses.globals import LocationResponseModel


class BusStopResponseModel(BaseModel):
    id: int
    name: str
    location: Union[LocationResponseModel, None]
    landmark: Union[str, None]


class GetAllBusStopsResponseModel(BaseModel):
    stops: List[BusStopResponseModel]


class GetBusStopResponseModel(BaseModel):
    stop: BusStopResponseModel


class GetBusStopResponseModel_ERR_404(BaseModel):
    detail: Literal["Bus Stop Not Found"]


class NewBusStopResponseModel(BaseModel):
    id: int
    name: str
    location: Union[LocationResponseModel, None]
    landmark: Union[str, None]


class NewBusStopResponseModel_ERR_400(BaseModel):
    detail: Literal["Bus Stop Already Exists"]


class UpdateBusStopResponseModel(BaseModel):
    id: int
    name: str
    location: Union[LocationResponseModel, None]
    landmark: Union[str, None]


class UpdateBusStopResponseModel_ERR_404(BaseModel):
    detail: Literal["Bus Stop Not Found"]


class DeleteBusStopResponseModel_ERR_404(BaseModel):
    detail: Literal["Bus Stop Not Found"]


class BusRouteResponseModel(BaseModel):
    id: int
    name: str
    from_stop: BusStopResponseModel
    to_stop: BusStopResponseModel
    via_stops: List[BusStopResponseModel]


class GetAllBusRoutesResponseModel(BaseModel):
    routes: List[BusRouteResponseModel]


class GetBusRouteResponseModel(BaseModel):
    route: BusRouteResponseModel


class GetBusRouteResponseModel_ERR_404(BaseModel):
    detail: Literal["Bus Route Not Found"]


class NewBusRouteResponseModel(BaseModel):
    id: int
    name: str
    from_stop: BusStopResponseModel
    to_stop: BusStopResponseModel
    via_stops: List[BusStopResponseModel]


class NewBusRouteResponseModel_ERR_400(BaseModel):
    detail: Literal["Bus Route Already Exists"]


class NewBusRouteResponseModel_ERR_404(BaseModel):
    detail: Union[
        Literal["FROM Bus Stop Not Found"],
        Literal["TO Bus Stop Not Found"],
        Literal["VIA Bus Stop Not Found"],
    ]


class UpdateBusRouteResponseModel(BaseModel):
    id: int
    name: str
    from_stop: BusStopResponseModel
    to_stop: BusStopResponseModel
    via_stops: List[BusStopResponseModel]


class UpdateBusRouteResponseModel_ERR_404(BaseModel):
    detail: Union[
        Literal["Bus Route Not Found"],
        Literal["FROM Bus Stop Not Found"],
        Literal["TO Bus Stop Not Found"],
        Literal["VIA Bus Stop Not Found"],
    ]


class DeleteBusRouteResponseModel_ERR_404(BaseModel):
    detail: Literal["Bus Route Not Found"]
