from appTypes.outletTypes import (
    NewFoodOutletBodyParams,
    UpdateFoodOutletBodyParams,
    FilterFoodOutletBodyParams,
    AddMenuItemFoodOutletBodyParams,
    UpdateMenuItemFoodOutletBodyParams,
)
from app.app import app
from app.db import connect, disconnect
from app.interfaces.outlet import FoodOutlet, searchOutlets, FoodOutletMenuItem
from app.interfaces.common import Location
from app.auth.key import get_api_key
from fastapi import Depends, status, HTTPException
from fastapi.security.api_key import APIKey
from datetime import time
from typing import Optional, List


@app.get(
    "/food-outlet",
    summary="Get Details of All Food Outlets on the Campus",
    tags=["Food Outlets"],
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

        outlet_details = outlet.__dict__
        outlet_details["location"] = (
            outlet.location.__dict__ if outlet.location is not None else None
        )

        outlet_details["menu"] = (
            [item.__dict__ for item in outlet.menu] if outlet.menu is not None else None
        )

        details.append(outlet_details)

    disconnect(con)

    return {"outlets": details}


@app.get(
    "/food-outlet/{id}",
    summary="Get Details of any Food Outlet by ID",
    tags=["Food Outlets"],
)
async def get_food_outlet_details(id: int):
    con = connect()

    outlet = FoodOutlet(id=id)
    await outlet.sync_details(con)
    disconnect(con)

    details = outlet.__dict__
    details["location"] = (
        outlet.location.__dict__ if outlet.location is not None else None
    )

    details["menu"] = (
        [item.__dict__ for item in outlet.menu] if outlet.menu is not None else None
    )

    return {"outlet": details}


@app.get(
    "/search/food-outlet",
    summary="Search for Food Outlets on the Campus",
    tags=["Food Outlets"],
)
async def filter_food_outlets(
    params: FilterFoodOutletBodyParams,
):
    con = connect()
    outlets = await searchOutlets(
        con=con,
        nameFilter=params.name.lower() if params.name is not None else None,
        locationFilter=Location(**params.location)
        if params.location is not None
        else None,
        landmarkFilter=params.landmark.lower() if params.landmark is not None else None,
        timeFilter=params.current_time,
        ratingFilter=params.rating,
        itemFilter=params.food_item.lower() if params.food_item is not None else None,
    )

    disconnect(con)

    if len(outlets) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No food outlets found",
        )

    for i in range(len(outlets)):
        outlets[i] = outlets[i].__dict__
        outlets[i]["location"] = (
            outlets[i]["location"].__dict__
            if outlets[i]["location"] is not None
            else None
        )

        outlets[i]["menu"] = (
            [item.__dict__ for item in outlets[i]["menu"]]
            if outlets[i]["menu"] is not None
            else None
        )

    return {"outlets": outlets}


@app.post(
    "/food-outlet",
    status_code=status.HTTP_201_CREATED,
    summary="Add a new Food Outlet",
    tags=["Food Outlets - ADMIN"],
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
        if e.status_code != status.HTTP_404_NOT_FOUND:
            disconnect(con)
            raise e
        else:
            con = connect()

    details = await outlet.create(con)

    disconnect(con)

    details["location"] = (
        details["location"].__dict__ if details["location"] is not None else None
    )

    return {"outlet": details}


@app.put(
    "/food-outlet/{id}",
    summary="Update Details of any Food Outlet by ID",
    tags=["Food Outlets - ADMIN"],
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

    details = await outlet.update(con=con)

    details["location"] = (
        details["location"].__dict__ if details["location"] is not None else None
    )

    details["menu"] = (
        [item.__dict__ for item in details["menu"]]
        if details["menu"] is not None
        else None
    )

    disconnect(con)
    return {"outlet": details}


@app.delete(
    "/food-outlet/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete any Food Outlet by ID",
    tags=["Food Outlets - ADMIN"],
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


@app.post(
    "/food-outlet/{id}/menu/food-item",
    status_code=status.HTTP_201_CREATED,
    summary="Add a new Menu Item to any Food Outlet by ID",
    tags=["Food Outlets - ADMIN"],
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
    item_details = await menu_item.create(con=con)

    disconnect(con)

    return {"item": item_details}


@app.put(
    "/food-outlet/{id}/menu/food-item/{item_id}",
    summary="Update Details of any Menu Item of any Food Outlet by ID",
    tags=["Food Outlets - ADMIN"],
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

    details = await menu_item.update(con=con)

    disconnect(con)

    return {"item": details}


@app.delete(
    "/food-outlet/{id}/menu/food-item/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete any Menu Item of any Food Outlet by ID",
    tags=["Food Outlets - ADMIN"],
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
