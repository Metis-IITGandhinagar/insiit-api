from pydantic import BaseModel
from typing import List, Union, Literal
from app.models.responses.globals import LocationResponseModel


class BusTypeResponseModel(BaseModel):
    id: int
    name: str


class GetAllBusTypesResponseModel(BaseModel):
    types: List[BusTypeResponseModel]


class GetBusTypeResponseModel(BaseModel):
    type: BusTypeResponseModel


class GetBusTypeResponseModel_ERR_404(BaseModel):
    detail: Literal["Bus Type Not Found"]


class NewBusTypeResponseModel(BaseModel):
    type: BusTypeResponseModel


class NewBusTypeResponseModel_ERR_400(BaseModel):
    detail: Literal["Bus Type Already Exists"]


class UpdateBusTypeResponseModel(BaseModel):
    type: BusTypeResponseModel


class UpdateBusTypeResponseModel_ERR_404(BaseModel):
    detail: Literal["Bus Type Not Found"]


class DeleteBusTypeResponseModel_ERR_404(BaseModel):
    detail: Literal["Bus Type Not Found"]


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


class BusScheduleResponseModel(BaseModel):
    id: int
    start_time: str
    route: BusRouteResponseModel
    end_time: Union[str, None]
    via_stop_times: Union[List[Union[str, None]], None]


class GetAllBusSchedulesResponseModel(BaseModel):
    schedules: List[BusScheduleResponseModel]


class GetBusScheduleResponseModel(BaseModel):
    schedule: BusScheduleResponseModel


class GetBusScheduleResponseModel_ERR_404(BaseModel):
    detail: Literal["Bus Schedule Not Found"]


class NewBusScheduleResponseModel(BaseModel):
    schedule: BusScheduleResponseModel


class NewBusScheduleResponseModel_ERR_404(BaseModel):
    detail: Union[
        Literal["Bus Route Not Found"],
        Literal["Bus Type Not Found"],
    ]


class NewBusScheduleResponseModel_ERR_400(BaseModel):
    detail: Union[
        Literal["Bus Schedule Already Exists"], Literal["Invalid Time Format"]
    ]


class UpdateBusScheduleResponseModel(BaseModel):
    schedule: BusScheduleResponseModel


class UpdateBusScheduleResponseModel_ERR_404(BaseModel):
    detail: Union[
        Literal["Bus Schedule Not Found"],
        Literal["Bus Route Not Found"],
        Literal["Bus Type Not Found"],
    ]


class UpdateBusScheduleResponseModel_ERR_400(BaseModel):
    detail: Literal["Invalid Time Format"]


class DeleteBusScheduleResponseModel_ERR_404(BaseModel):
    detail: Literal["Bus Schedule Not Found"]
