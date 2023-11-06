from pydantic import BaseModel
from typing import Literal, Optional
from app.models.responses.globals import LocationResponseModel


class OutletMenuItemResponseModel(BaseModel):
    id: int
    name: str
    price: float
    outlet_id: int
    description: Optional[str] = None
    rating: Optional[float] = None
    size: Optional[str] = None
    cal: Optional[int] = None
    image: Optional[str] = None


class OutletResponseModel(BaseModel):
    id: int
    name: str
    location: Optional[LocationResponseModel] = None
    landmark: Optional[str] = None
    open_time: Optional[str] = None
    close_time: Optional[str] = None
    rating: Optional[float] = None
    menu: Optional[list[OutletMenuItemResponseModel]] = None
    image: Optional[str] = None


class GetAllFoodOutletDetailsResponseModel(BaseModel):
    outlets: list[OutletResponseModel]


class GetFoodOutletDetailsResponseModel(BaseModel):
    outlet: OutletResponseModel


class GetFoodOutletDetailsResponseModel_ERR_404(BaseModel):
    detail: Literal["Food Outlet not found"]


class FilterFoodOutletsResponseModel(BaseModel):
    outlets: list[OutletResponseModel]


class FilterFoodOutletsResponseModel_ERR_404(BaseModel):
    detail: Literal["No food outlets found"]


class CreateFoodOutletResponseModel(BaseModel):
    outlet: OutletResponseModel


class CreateFoodOutletResponseModel_ERR_400(BaseModel):
    detail: Literal["Food Outlet already exists"]


class UpdateFoodOutletResponseModel(BaseModel):
    outlet: OutletResponseModel


class UpdateFoodOutletResponseModel_ERR_404(BaseModel):
    detail: Literal["Food Outlet not found"]


class DeleteFoodOutletResponseModel_ERR_404(BaseModel):
    detail: Literal["Food Outlet not found"]


class MenuItemResponseModel(BaseModel):
    id: int
    name: str
    price: int
    outlet_id: int
    description: Optional[str]
    rating: Optional[float]
    size: Optional[str]
    cal: Optional[int]
    image: Optional[str]


class GetAllMenuItemsResponseModel(BaseModel):
    food_items: list[MenuItemResponseModel]


class GetMenuItemResponseModel(BaseModel):
    food_item: MenuItemResponseModel


class GetMenuItemResponseModel_ERR_404(BaseModel):
    detail: Literal["Menu item not found"]


class CreateMenuItemResponseModel(BaseModel):
    food_item: MenuItemResponseModel


class CreateMenuItemResponseModel_ERR_400(BaseModel):
    detail: Literal["Menu item already exists"]


class CreateMenuItemResponseModel_ERR_404(BaseModel):
    detail: Literal["Food Outlet not found"]


class UpdateMenuItemResponseModel(BaseModel):
    food_item: MenuItemResponseModel


class UpdateMenuItemResponseModel_ERR_404_MenuItemNotFound(BaseModel):
    detail: Literal["Menu item not found"]


class UpdateMenuItemResponseModel_ERR_404_FoodOutletNotFound(BaseModel):
    detail: Literal["Food Outlet not found"]


class DeleteMenuItemResponseModel_ERR_404_MenuItemNotFound(BaseModel):
    detail: Literal["Menu item not found"]


class DeleteMenuItemResponseModel_ERR_404_FoodOutletNotFound(BaseModel):
    detail: Literal["Food Outlet not found"]
