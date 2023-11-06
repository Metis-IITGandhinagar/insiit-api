from app.models.requests._outlet import (
    NewFoodOutletBodyParams,
    UpdateFoodOutletBodyParams,
    FilterFoodOutletBodyParams,
    AddMenuItemFoodOutletBodyParams,
    UpdateMenuItemFoodOutletBodyParams,
)
from app.app import app
from app.db import connect, disconnect
from app.models.outlet import FoodOutlet, searchOutlets, FoodOutletMenuItem
from app.models.globals import Location
from app.auth.key import get_api_key
from fastapi import Depends, Response, status, HTTPException
from fastapi.security.api_key import APIKey
from app.utils.globals import obj_to_json
from app.models.responses._outlet import (
    GetAllFoodOutletDetailsResponseModel,
    GetFoodOutletDetailsResponseModel,
    GetFoodOutletDetailsResponseModel_ERR_404,
    FilterFoodOutletsResponseModel,
    FilterFoodOutletsResponseModel_ERR_404,
    CreateFoodOutletResponseModel,
    CreateFoodOutletResponseModel_ERR_400,
    UpdateFoodOutletResponseModel,
    UpdateFoodOutletResponseModel_ERR_404,
    DeleteFoodOutletResponseModel_ERR_404,
    GetAllMenuItemsResponseModel,
    GetMenuItemResponseModel,
    GetMenuItemResponseModel_ERR_404,
    CreateMenuItemResponseModel,
    CreateMenuItemResponseModel_ERR_400,
    CreateMenuItemResponseModel_ERR_404,
    UpdateMenuItemResponseModel,
    UpdateMenuItemResponseModel_ERR_404_MenuItemNotFound,
    UpdateMenuItemResponseModel_ERR_404_FoodOutletNotFound,
    DeleteMenuItemResponseModel_ERR_404_MenuItemNotFound,
    DeleteMenuItemResponseModel_ERR_404_FoodOutletNotFound,
)


@app.get(
    "/food-outlet",
    summary="Get Details of All Food Outlets on the Campus",
    tags=["Food Outlets"],
    response_model=GetAllFoodOutletDetailsResponseModel,
)
async def get_all_food_outlet_details():
    con = connect()
    cursor = con.cursor()

    cursor.execute("SELECT id FROM food_outlets")
    result = cursor.fetchall()
    ids = [row[0] for row in result]
    details = []

    # print(ids)
    cursor.close()
    for id in ids:
        outlet = FoodOutlet(id=id)
        await outlet.sync_details(con)

        details.append(obj_to_json(outlet))

    disconnect(con)

    return {"outlets": details}


@app.get(
    "/food-outlet/{id}",
    summary="Get Details of any Food Outlet by ID",
    tags=["Food Outlets"],
    response_model=GetFoodOutletDetailsResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": GetFoodOutletDetailsResponseModel_ERR_404,
        },
    },
)
async def get_food_outlet_details(id: int):
    con = connect()

    outlet = FoodOutlet(id=id)
    await outlet.sync_details(con)
    disconnect(con)

    return {"outlet": obj_to_json(outlet)}


@app.get(
    "/search/food-outlet",
    summary="Search for Food Outlets on the Campus",
    tags=["Food Outlets"],
    response_model=FilterFoodOutletsResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": FilterFoodOutletsResponseModel_ERR_404,
        },
    },
)
async def filter_food_outlets(
    params: FilterFoodOutletBodyParams,
):
    con = connect()
    outlets = [
        obj_to_json(outlet)
        for outlet in await searchOutlets(
            con=con,
            nameFilter=params.name.lower() if params.name is not None else None,
            locationFilter=Location(**params.location)
            if params.location is not None
            else None,
            landmarkFilter=params.landmark.lower()
            if params.landmark is not None
            else None,
            timeFilter=params.current_time,
            ratingFilter=params.rating,
            itemFilter=params.food_item.lower()
            if params.food_item is not None
            else None,
        )
    ]

    disconnect(con)

    if len(outlets) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No food outlets found",
        )

    return {"outlets": outlets}


@app.post(
    "/food-outlet",
    status_code=status.HTTP_201_CREATED,
    summary="Add a new Food Outlet",
    tags=["[ADMIN] Food Outlets"],
    response_model=CreateFoodOutletResponseModel,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request Error",
            "model": CreateFoodOutletResponseModel_ERR_400,
        },
    },
)
async def create_food_outlet(
    params: NewFoodOutletBodyParams, api_key: APIKey = Depends(get_api_key)
):
    params_dict = params.model_dump()
    if params_dict["location"] is not None:
        params_dict["location"] = Location(**params_dict["location"])

    for key, value in params_dict.items():
        if type(value) is str:
            params_dict[key] = value.lower()

    con = connect()

    outlet = FoodOutlet(**params_dict)
    try:
        await outlet.sync_details(con)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Food outlet already exists",
        )
    except HTTPException as e:
        if (e.status_code != status.HTTP_404_NOT_FOUND) and (
            e.detail != "Food Outlet not found"
        ):
            disconnect(con)
            raise e
        else:
            con = connect()

    await outlet.create(con)

    disconnect(con)

    return {"outlet": obj_to_json(outlet)}


@app.put(
    "/food-outlet/{id}",
    summary="Update Details of any Food Outlet by ID",
    tags=["[ADMIN] Food Outlets"],
    response_model=UpdateFoodOutletResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": UpdateFoodOutletResponseModel_ERR_404,
        },
    },
)
async def update_food_outlet(
    id: int,
    params: UpdateFoodOutletBodyParams,
    api_key: APIKey = Depends(get_api_key),
):
    con = connect()
    outlet = FoodOutlet(id=id)
    await outlet.sync_details(con=con)
    params_dict = params.model_dump()
    for key, value in params_dict.items():
        if value is not None:
            if key == "location":
                outlet.location = Location(**params_dict["location"])

            else:
                outlet.__setattr__(key, value.lower() if type(value) is str else value)

    await outlet.update(con=con)

    disconnect(con)
    return {"outlet": obj_to_json(outlet)}


@app.delete(
    "/food-outlet/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete any Food Outlet by ID",
    tags=["[ADMIN] Food Outlets"],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successfully Deteled",
            "model": None,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": DeleteFoodOutletResponseModel_ERR_404,
        },
    },
)
async def delete_food_outlet(id: int, api_key: APIKey = Depends(get_api_key)):
    con = connect()
    outlet = FoodOutlet(id=id)

    try:
        await outlet.sync_details(con)
    except HTTPException as e:
        if e.status_code == status.HTTP_404_NOT_FOUND:
            raise e

    await outlet.remove(con)


@app.get(
    "/food-outlet_menu_food-item",
    summary="Get Details of All Menu Items of Food Outlets",
    tags=["Food Outlets"],
    response_model=GetAllMenuItemsResponseModel,
)
async def get_all_menu_items():
    con = connect()
    cursor = con.cursor()

    cursor.execute("SELECT id FROM food_outlet_menu_items")
    result = cursor.fetchall()
    ids = [row[0] for row in result]
    details = []

    cursor.close()
    for id in ids:
        item = FoodOutletMenuItem(id=id)
        await item.sync_details(con)

        details.append(obj_to_json(item))

    disconnect(con)

    return {"food_items": details}


@app.get(
    "/food-outlet_menu_food-item/{id}",
    summary="Get Details of any Menu Item of Food Outlets by ID",
    tags=["Food Outlets"],
    response_model=GetMenuItemResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": GetMenuItemResponseModel_ERR_404,
        },
    },
)
async def get_menu_item(id: int):
    con = connect()

    item = FoodOutletMenuItem(id=id)
    await item.sync_details(con)
    disconnect(con)

    return {"food_item": obj_to_json(item)}


@app.post(
    "/food-outlet/{id}/menu/food-item",
    status_code=status.HTTP_201_CREATED,
    summary="Add a new Menu Item to any Food Outlet by ID",
    tags=["[ADMIN] Food Outlets"],
    response_model=CreateMenuItemResponseModel,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request Error",
            "model": CreateMenuItemResponseModel_ERR_400,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": CreateMenuItemResponseModel_ERR_404,
        },
    },
)
async def add_menu_item_food_outlet(
    id: int,
    params: AddMenuItemFoodOutletBodyParams,
    api_key: APIKey = Depends(get_api_key),
):
    con = connect()

    outlet = FoodOutlet(id=id)
    await outlet.sync_details(con=con)

    if outlet.menu is not None:
        for item in outlet.menu:
            if item.name == params.name.lower():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Menu item already exists",
                )

    params_dict = {
        key: value.lower() if type(value) is str else value
        for key, value in params.model_dump().items()
    }

    menu_item = FoodOutletMenuItem(**params_dict, outlet_id=id)
    await menu_item.create(con=con)

    disconnect(con)

    return {"item": obj_to_json(menu_item)}


@app.put(
    "/food-outlet/{id}/menu/food-item/{item_id}",
    summary="Update Details of any Menu Item of any Food Outlet by ID",
    tags=["[ADMIN] Food Outlets"],
    response_model=UpdateMenuItemResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": UpdateMenuItemResponseModel_ERR_404_MenuItemNotFound
            | UpdateMenuItemResponseModel_ERR_404_FoodOutletNotFound,
        }
    },
)
async def update_menu_item_food_outlet(
    id: int,
    item_id: int,
    params: UpdateMenuItemFoodOutletBodyParams,
    api_key: APIKey = Depends(get_api_key),
):
    con = connect()

    outlet = FoodOutlet(id=id)
    await outlet.sync_details(con=con)

    menu_item = FoodOutletMenuItem(id=item_id)
    await menu_item.sync_details(con=con)

    params_dict = params.model_dump()

    for key, value in params_dict.items():
        if value is not None:
            menu_item.__setattr__(key, value.lower() if type(value) is str else value)

    await menu_item.update(con=con)

    disconnect(con)

    return {"item": obj_to_json(menu_item)}


@app.delete(
    "/food-outlet/{id}/menu/food-item/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete any Menu Item of any Food Outlet by ID",
    tags=["[ADMIN] Food Outlets"],
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Successfully Deteled",
            "model": None,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": DeleteMenuItemResponseModel_ERR_404_MenuItemNotFound
            | DeleteMenuItemResponseModel_ERR_404_FoodOutletNotFound,
        },
    },
)
async def delete_menu_item_food_outlet(
    id: int, item_id: int, api_key: APIKey = Depends(get_api_key)
):
    con = connect()

    outlet = FoodOutlet(id=id)
    await outlet.sync_details(con=con)

    item = FoodOutletMenuItem(id=item_id)
    await item.sync_details(con=con)
    await item.remove(con=con)
