from typing import Literal, Optional
from pydantic import BaseModel
from app.models.responses.globals import LocationResponseModel, MessTimingsResponseModel


class MenuItemResponseModel(BaseModel):
    id: int
    name: str
    description: Optional[str]
    rating: Optional[float]
    cal: Optional[int]
    image: Optional[str]


class DayMenuResponseModel(BaseModel):
    breakfast: Optional[list[MenuItemResponseModel]]
    lunch: Optional[list[MenuItemResponseModel]]
    snacks: Optional[list[MenuItemResponseModel]]
    dinner: Optional[list[MenuItemResponseModel]]


class MessMenuResponseModel(BaseModel):
    id: int
    month: int
    year: int
    monday: Optional[DayMenuResponseModel]
    tuesday: Optional[DayMenuResponseModel]
    wednesday: Optional[DayMenuResponseModel]
    thursday: Optional[DayMenuResponseModel]
    friday: Optional[DayMenuResponseModel]
    saturday: Optional[DayMenuResponseModel]
    sunday: Optional[DayMenuResponseModel]


class MessResponseModel(BaseModel):
    id: int
    name: str
    location: Optional[LocationResponseModel]
    landmark: Optional[str]
    timings: Optional[MessTimingsResponseModel]
    rating: Optional[float]
    menu: Optional[MessMenuResponseModel]
    image: Optional[str]


class GetAllMessDetailsResponseModel(BaseModel):
    messes: list[MessResponseModel]


class GetMessDetailsResponseModel(BaseModel):
    mess: MessResponseModel


class GetMessDetailsResponseModel_ERR_404(BaseModel):
    detail: Literal["Mess not found"]


class CreateMessResponseModel(BaseModel):
    mess: MessResponseModel


class CreateMessResponseModel_ERR_400(BaseModel):
    detail: Literal["Mess already exists"]


class UpdateMessResponseModel(BaseModel):
    mess: MessResponseModel


class UpdateMessResponseModel_ERR_404(BaseModel):
    detail: Literal["Mess not found"]


class UpdateMessChangeMenuResponseModel(BaseModel):
    mess: MessResponseModel


class UpdateMessChangeMenuResponseModel_ERR_404_MessNotFound(BaseModel):
    detail: Literal["Mess not found"]


class UpdateMessChangeMenuResponseModel_ERR_404_MessMenuNotFound(BaseModel):
    detail: Literal["Mess menu not found"]


class DeleteMessResponseModel_ERR_404(BaseModel):
    detail: Literal["Mess not found"]


class GetCurrentMessMenuDetailsResponseModel(BaseModel):
    menu: MessMenuResponseModel | None


class GetCurrentMessMenuDetailsResponseModel_ERR_404(BaseModel):
    detail: Literal["Mess not found"]


class GetCurrentMessMenuDetailsByDayResponseModel(BaseModel):
    menu: DayMenuResponseModel | None


class GetCurrentMessMenuDetailsByDayResponseModel_ERR_404(BaseModel):
    detail: Literal["Mess not found"]


class GetMessMenuDetailsResponseModel(BaseModel):
    menus: list[MessMenuResponseModel]


class GetMessMenuDetailsByIDsResponseModel(BaseModel):
    menu: MessMenuResponseModel | None


class GetMessMenuDetailsByIDsResponseModel_ERR_404(BaseModel):
    detail: Literal["Mess menu not found"]


class CreateMessMenuResponseModel(BaseModel):
    menu: MessMenuResponseModel


class CreateMessMenuResponseModel_ERR_400(BaseModel):
    detail: Literal["Mess menu already exists"]


class UpdateMessMenuResponseModel(BaseModel):
    menu: MessMenuResponseModel


class UpdateMessMenuResponseModel_ERR_404(BaseModel):
    detail: Literal["Mess menu not found"]


class DeleteMessMenuResponseModel_ERR_404(BaseModel):
    detail: Literal["Mess menu not found"]


class GetAllMessMenuItemsDetails(BaseModel):
    items: list[MenuItemResponseModel]


class GetMessMenuItemDetailsResponseModel(BaseModel):
    item: MenuItemResponseModel


class GetMessMenuItemDetailsResponseModel_ERR_404(BaseModel):
    detail: Literal["Mess menu item not found"]


class CreateMessMenuItemResponseModel(BaseModel):
    item: MenuItemResponseModel


class CreateMessMenuItemResponseModel_ERR_400(BaseModel):
    detail: Literal["Mess menu item already exists"]


class UpdateMessMenuItemResponseModel(BaseModel):
    item: MenuItemResponseModel


class UpdateMessMenuItemResponseModel_ERR_404(BaseModel):
    detail: Literal["Mess menu item not found"]


class DeleteMessMenuItemResponseModel_ERR_404(BaseModel):
    detail: Literal["Mess menu item not found"]
