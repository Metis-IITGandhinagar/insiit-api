from app.db import connect, disconnect
from app.models.mess import Mess, MessMenu, MessMenuItem, DayMenu
from app.models.globals import Location
from app.auth.key import get_api_key
from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security.api_key import APIKey
from app.utils.globals import obj_to_json
from app.models.requests._mess import (
    NewMessBodyParams,
    UpdateMessBodyParams,
    NewMessMenuBodyParams,
    UpdateMessMenuBodyParams,
    NewMessMenuItemBodyParams,
    UpdateMessMenuItemBodyParams,
)
from app.models.responses._mess import (
    GetAllMessDetailsResponseModel,
    GetMessDetailsResponseModel,
    GetMessDetailsResponseModel_ERR_404,
    CreateMessResponseModel,
    CreateMessResponseModel_ERR_400,
    UpdateMessResponseModel,
    UpdateMessResponseModel_ERR_404,
    UpdateMessChangeMenuResponseModel,
    UpdateMessChangeMenuResponseModel_ERR_404_MessMenuNotFound,
    UpdateMessChangeMenuResponseModel_ERR_404_MessNotFound,
    DeleteMessResponseModel_ERR_404,
    GetCurrentMessMenuDetailsResponseModel,
    GetCurrentMessMenuDetailsResponseModel_ERR_404,
    GetCurrentMessMenuDetailsByDayResponseModel,
    GetCurrentMessMenuDetailsByDayResponseModel_ERR_404,
    GetMessMenuDetailsResponseModel,
    GetMessMenuDetailsByIDsResponseModel,
    GetMessMenuDetailsByIDsResponseModel_ERR_404,
    CreateMessMenuResponseModel,
    CreateMessMenuResponseModel_ERR_400,
    UpdateMessMenuResponseModel,
    UpdateMessMenuResponseModel_ERR_404,
    DeleteMessMenuResponseModel_ERR_404,
    GetAllMessMenuItemsDetails,
    GetMessMenuItemDetailsResponseModel,
    GetMessMenuItemDetailsResponseModel_ERR_404,
    CreateMessMenuItemResponseModel,
    CreateMessMenuItemResponseModel_ERR_400,
    UpdateMessMenuItemResponseModel,
    UpdateMessMenuItemResponseModel_ERR_404,
    DeleteMessMenuItemResponseModel_ERR_404,
)
from typing import Optional, Literal


router = APIRouter()


@router.get(
    "/mess",
    summary="Get Details of All Messes on the Campus",
    tags=["Mess"],
    response_model=GetAllMessDetailsResponseModel,
)
async def get_all_mess_details():
    con = connect()
    cursor = con.cursor()

    cursor.execute("SELECT id FROM messes")
    result = cursor.fetchall()
    ids = [row[0] for row in result]

    cursor.close()

    details = []
    for id in ids:
        mess = Mess(id=id)
        await mess.sync_details(con)

        details.append(obj_to_json(mess))

    disconnect(con)

    return {"messes": details}


@router.get(
    "/mess/{id}",
    summary="Get Details of any Mess by ID",
    tags=["Mess"],
    response_model=GetMessDetailsResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": GetMessDetailsResponseModel_ERR_404,
        }
    },
)
async def get_mess_details(id: int):
    con = connect()

    mess = Mess(id=id)
    await mess.sync_details(con)

    disconnect(con)

    return {"mess": obj_to_json(mess)}


@router.post(
    "/mess",
    status_code=status.HTTP_201_CREATED,
    summary="Add a new Mess",
    tags=["[ADMIN] Mess"],
    response_model=CreateMessResponseModel,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request Error",
            "model": CreateMessResponseModel_ERR_400,
        }
    },
)
async def create_mess(
    params: NewMessBodyParams, api_key: APIKey = Depends(get_api_key)
):
    params_dict = params.model_dump()
    if params_dict["location"] is not None:
        params_dict["location"] = Location(**params_dict["location"])

    con = connect()
    mess = Mess(**params_dict)

    try:
        await mess.sync_details(con)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mess already exists",
        )
    except HTTPException as e:
        if e.status_code != status.HTTP_404_NOT_FOUND:
            disconnect(con)
            raise e

    await mess.create(con)

    return {"mess": obj_to_json(mess)}


@router.put(
    "/mess/{id}",
    summary="Update Details of any Mess by ID",
    tags=["[ADMIN] Mess"],
    response_model=UpdateMessResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": UpdateMessResponseModel_ERR_404,
        }
    },
)
async def update_mess(
    id: int, params: UpdateMessBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()
    mess = Mess(id=id)
    await mess.sync_details(con=con)
    params_dict = params.model_dump()
    for key, value in params_dict.items():
        if value is not None:
            if key == "location":
                mess.location = Location(**params_dict["location"])
            else:
                setattr(mess, key, value)

    await mess.update(con)

    disconnect(con)

    return {"mess": obj_to_json(mess)}


@router.put(
    "/mess/{mess_id}/menu/{menu_id}",
    summary="Change the Menu of any Mess by ID",
    tags=["[ADMIN] Mess"],
    response_model=UpdateMessChangeMenuResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": UpdateMessChangeMenuResponseModel_ERR_404_MessMenuNotFound
            | UpdateMessChangeMenuResponseModel_ERR_404_MessNotFound,
        }
    },
)
async def update_mess_change_menu(
    mess_id: int, menu_id: int, api_key: APIKey = Depends(get_api_key)
):
    con = connect()

    mess = Mess(id=mess_id)
    await mess.sync_details(con)

    menu = MessMenu(id=menu_id)
    await menu.sync_details(con)

    mess.menu = menu
    await mess.update(con)

    disconnect(con)

    return {"mess": obj_to_json(mess)}


@router.delete(
    "/mess/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete any Mess by ID",
    tags=["[ADMIN] Mess"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": DeleteMessResponseModel_ERR_404,
        }
    },
)
async def delete_mess(id: int, api_key: APIKey = Depends(get_api_key)):
    con = connect()
    mess = Mess(id=id)
    await mess.sync_details(con=con)

    await mess.remove(con)

    disconnect(con)


@router.get(
    "/mess/{id}/menu",
    summary="Get the Current Menu of any Mess by ID",
    tags=["Mess"],
    response_model=GetCurrentMessMenuDetailsResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": GetCurrentMessMenuDetailsResponseModel_ERR_404,
        }
    },
)
async def get_current_mess_menu_details(id: int):
    con = connect()

    mess = Mess(id=id)
    await mess.sync_details(con)

    disconnect(con)

    menu = mess.menu

    return {"menu": menu}


@router.get(
    "/mess/{id}/menu/{day}",
    summary="Get the Current Menu of a particular Day of any Mess by ID",
    tags=["Mess"],
    response_model=GetCurrentMessMenuDetailsByDayResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": GetCurrentMessMenuDetailsByDayResponseModel_ERR_404,
        }
    },
)
async def get_current_mess_menu_details_byDay(
    id: int,
    day: Literal[
        "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
    ],
):
    con = connect()

    mess = Mess(id=id)
    await mess.sync_details(con)

    disconnect(con)

    menu = mess.menu

    if menu is None:
        return {"menu": None}

    menu_today = getattr(menu, day)

    return {"menu": menu_today}


@router.get(
    "/mess_menu",
    summary="Get Details of any Mess Menus by Month/Year",
    tags=["Mess"],
    response_model=GetMessMenuDetailsResponseModel,
)
async def get_mess_menu_details(month: int | None = None, year: int | None = None):
    con = connect()
    cursor = con.cursor()

    cursor.execute("SELECT id FROM messes")
    result = cursor.fetchall()
    ids = [row[0] for row in result]

    cursor.close()

    details = []
    for id in ids:
        menu = MessMenu(id=id)
        await menu.sync_details(con)

        if year is not None:
            if menu.year != year:
                continue
        if month is not None:
            if menu.month != month:
                continue

        details.append(obj_to_json(menu))

    disconnect(con)

    return {"menus": details}


@router.get(
    "/mess_menu/{id}",
    summary="Get Details of any Mess Menu by ID",
    tags=["Mess"],
    response_model=GetMessMenuDetailsByIDsResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": GetMessMenuDetailsByIDsResponseModel_ERR_404,
        }
    },
)
async def get_mess_menu_details_byID(id: int):
    con = connect()

    menu = MessMenu(id=id)
    await menu.sync_details(con)

    disconnect(con)

    return {"menu": obj_to_json(menu)}


@router.post(
    "/mess_menu",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Mess Menu",
    tags=["[ADMIN] Mess"],
    response_model=CreateMessMenuResponseModel,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request Error",
            "model": CreateMessMenuResponseModel_ERR_400,
        }
    },
)
async def create_mess_menu(
    params: NewMessMenuBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()

    try:
        menu = MessMenu(month=params.month, year=params.year)
        await menu.sync_details(con)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mess menu already exists",
        )
    except HTTPException as e:
        if e.status_code != status.HTTP_404_NOT_FOUND:
            disconnect(con)
            raise e

    monday: DayMenu | None = None
    if params.monday is not None:
        monday = {}
        if params.monday["breakfast"] is not None:
            monday["breakfast"] = [
                MessMenuItem(id=item_id) for item_id in params.monday["breakfast"]
            ]

            for item in monday["breakfast"]:
                await item.sync_details(con)
        else:
            monday["breakfast"] = None

        if params.monday["lunch"] is not None:
            monday["lunch"] = [
                MessMenuItem(id=item_id) for item_id in params.monday["lunch"]
            ]

            for item in monday["lunch"]:
                await item.sync_details(con)
        else:
            monday["lunch"] = None

        if params.monday["snacks"] is not None:
            monday["snacks"] = [
                MessMenuItem(id=item_id) for item_id in params.monday["snacks"]
            ]

            for item in monday["snacks"]:
                await item.sync_details(con)
        else:
            monday["snacks"] = None

        if params.monday["dinner"] is not None:
            monday["dinner"] = [
                MessMenuItem(id=item_id) for item_id in params.monday["dinner"]
            ]

            for item in monday["dinner"]:
                await item.sync_details(con)
        else:
            monday["dinner"] = None

    tuesday: DayMenu | None = None
    if params.tuesday is not None:
        tuesday = {}
        if params.tuesday["breakfast"] is not None:
            tuesday["breakfast"] = [
                MessMenuItem(id=item_id) for item_id in params.tuesday["breakfast"]
            ]

            for item in tuesday["breakfast"]:
                await item.sync_details(con)
        else:
            tuesday["breakfast"] = None

        if params.tuesday["lunch"] is not None:
            tuesday["lunch"] = [
                MessMenuItem(id=item_id) for item_id in params.tuesday["lunch"]
            ]

            for item in tuesday["lunch"]:
                await item.sync_details(con)
        else:
            tuesday["lunch"] = None

        if params.tuesday["snacks"] is not None:
            tuesday["snacks"] = [
                MessMenuItem(id=item_id) for item_id in params.tuesday["snacks"]
            ]

            for item in tuesday["snacks"]:
                await item.sync_details(con)
        else:
            tuesday["snacks"] = None

        if params.tuesday["dinner"] is not None:
            tuesday["dinner"] = [
                MessMenuItem(id=item_id) for item_id in params.tuesday["dinner"]
            ]

            for item in tuesday["dinner"]:
                await item.sync_details(con)
        else:
            tuesday["dinner"] = None

    wednesday: DayMenu | None = None
    if params.wednesday is not None:
        wednesday = {}
        if params.wednesday["breakfast"] is not None:
            wednesday["breakfast"] = [
                MessMenuItem(id=item_id) for item_id in params.wednesday["breakfast"]
            ]

            for item in wednesday["breakfast"]:
                await item.sync_details(con)
        else:
            wednesday["breakfast"] = None

        if params.wednesday["lunch"] is not None:
            wednesday["lunch"] = [
                MessMenuItem(id=item_id) for item_id in params.wednesday["lunch"]
            ]

            for item in wednesday["lunch"]:
                await item.sync_details(con)
        else:
            wednesday["lunch"] = None

        if params.wednesday["snacks"] is not None:
            wednesday["snacks"] = [
                MessMenuItem(id=item_id) for item_id in params.wednesday["snacks"]
            ]

            for item in wednesday["snacks"]:
                await item.sync_details(con)
        else:
            wednesday["snacks"] = None

        if params.wednesday["dinner"] is not None:
            wednesday["dinner"] = [
                MessMenuItem(id=item_id) for item_id in params.wednesday["dinner"]
            ]

            for item in wednesday["dinner"]:
                await item.sync_details(con)
        else:
            wednesday["dinner"] = None

    thursday: DayMenu | None = None
    if params.thursday is not None:
        thursday = {}
        if params.thursday["breakfast"] is not None:
            thursday["breakfast"] = [
                MessMenuItem(id=item_id) for item_id in params.thursday["breakfast"]
            ]

            for item in thursday["breakfast"]:
                await item.sync_details(con)
        else:
            thursday["breakfast"] = None

        if params.thursday["lunch"] is not None:
            thursday["lunch"] = [
                MessMenuItem(id=item_id) for item_id in params.thursday["lunch"]
            ]

            for item in thursday["lunch"]:
                await item.sync_details(con)
        else:
            thursday["lunch"] = None

        if params.thursday["snacks"] is not None:
            thursday["snacks"] = [
                MessMenuItem(id=item_id) for item_id in params.thursday["snacks"]
            ]

            for item in thursday["snacks"]:
                await item.sync_details(con)
        else:
            thursday["snacks"] = None

        if params.thursday["dinner"] is not None:
            thursday["dinner"] = [
                MessMenuItem(id=item_id) for item_id in params.thursday["dinner"]
            ]

            for item in thursday["dinner"]:
                await item.sync_details(con)
        else:
            thursday["dinner"] = None

    friday: DayMenu | None = None
    if params.friday is not None:
        friday = {}
        if params.friday["breakfast"] is not None:
            friday["breakfast"] = [
                MessMenuItem(id=item_id) for item_id in params.friday["breakfast"]
            ]

            for item in friday["breakfast"]:
                await item.sync_details(con)
        else:
            friday["breakfast"] = None

        if params.friday["lunch"] is not None:
            friday["lunch"] = [
                MessMenuItem(id=item_id) for item_id in params.friday["lunch"]
            ]

            for item in friday["lunch"]:
                await item.sync_details(con)
        else:
            friday["lunch"] = None

        if params.friday["snacks"] is not None:
            friday["snacks"] = [
                MessMenuItem(id=item_id) for item_id in params.friday["snacks"]
            ]

            for item in friday["snacks"]:
                await item.sync_details(con)
        else:
            friday["snacks"] = None

        if params.friday["dinner"] is not None:
            friday["dinner"] = [
                MessMenuItem(id=item_id) for item_id in params.friday["dinner"]
            ]

            for item in friday["dinner"]:
                await item.sync_details(con)
        else:
            friday["dinner"] = None

    saturday: DayMenu | None = None
    if params.saturday is not None:
        saturday = {}
        if params.saturday["breakfast"] is not None:
            saturday["breakfast"] = [
                MessMenuItem(id=item_id) for item_id in params.saturday["breakfast"]
            ]

            for item in saturday["breakfast"]:
                await item.sync_details(con)
        else:
            saturday["breakfast"] = None

        if params.saturday["lunch"] is not None:
            saturday["lunch"] = [
                MessMenuItem(id=item_id) for item_id in params.saturday["lunch"]
            ]

            for item in saturday["lunch"]:
                await item.sync_details(con)
        else:
            saturday["lunch"] = None

        if params.saturday["snacks"] is not None:
            saturday["snacks"] = [
                MessMenuItem(id=item_id) for item_id in params.saturday["snacks"]
            ]

            for item in saturday["snacks"]:
                await item.sync_details(con)
        else:
            saturday["snacks"] = None

        if params.saturday["dinner"] is not None:
            saturday["dinner"] = [
                MessMenuItem(id=item_id) for item_id in params.saturday["dinner"]
            ]

            for item in saturday["dinner"]:
                await item.sync_details(con)

        else:
            saturday["dinner"] = None

    sunday: DayMenu | None = None
    if params.sunday is not None:
        sunday = {}
        if params.sunday["breakfast"] is not None:
            sunday["breakfast"] = [
                MessMenuItem(id=item_id) for item_id in params.sunday["breakfast"]
            ]

            for item in sunday["breakfast"]:
                await item.sync_details(con)
        else:
            sunday["breakfast"] = None

        if params.sunday["lunch"] is not None:
            sunday["lunch"] = [
                MessMenuItem(id=item_id) for item_id in params.sunday["lunch"]
            ]

            for item in sunday["lunch"]:
                await item.sync_details(con)
        else:
            sunday["lunch"] = None

        if params.sunday["snacks"] is not None:
            sunday["snacks"] = [
                MessMenuItem(id=item_id) for item_id in params.sunday["snacks"]
            ]

            for item in sunday["snacks"]:
                await item.sync_details(con)
        else:
            sunday["snacks"] = None

        if params.sunday["dinner"] is not None:
            sunday["dinner"] = [
                MessMenuItem(id=item_id) for item_id in params.sunday["dinner"]
            ]

            for item in sunday["dinner"]:
                await item.sync_details(con)
        else:
            sunday["dinner"] = None

    menu = MessMenu(
        month=params.month,
        year=params.year,
        monday=monday,
        tuesday=tuesday,
        wednesday=wednesday,
        thursday=thursday,
        friday=friday,
        saturday=saturday,
        sunday=sunday,
    )

    await menu.create(con)

    disconnect(con)

    return {"menu": obj_to_json(menu)}


@router.put(
    "/mess_menu/{id}",
    summary="Update Details of any Mess Menu by ID",
    tags=["[ADMIN] Mess"],
    response_model=UpdateMessMenuResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": UpdateMessMenuResponseModel_ERR_404,
        }
    },
)
async def update_mess_menu(
    id: int,
    params: UpdateMessMenuBodyParams,
    api_key: APIKey = Depends(get_api_key),
):
    con = connect()
    menu = MessMenu(id=id)
    await menu.sync_details(con)

    if params.monday is not None:
        if params.monday["breakfast"] is not None:
            monday_breakfast = [
                MessMenuItem(id=item_id) for item_id in params.monday["breakfast"]
            ]

            for item in monday_breakfast:
                await item.sync_details(con)

            menu.monday["breakfast"] = monday_breakfast

        if params.monday["lunch"] is not None:
            monday_lunch = [
                MessMenuItem(id=item_id) for item_id in params.monday["lunch"]
            ]

            for item in monday_lunch:
                await item.sync_details(con)

            menu.monday["lunch"] = monday_lunch

        if params.monday["snacks"] is not None:
            monday_snacks = [
                MessMenuItem(id=item_id) for item_id in params.monday["snacks"]
            ]

            for item in monday_snacks:
                await item.sync_details(con)

            menu.monday["snacks"] = monday_snacks

        if params.monday["dinner"] is not None:
            monday_dinner = [
                MessMenuItem(id=item_id) for item_id in params.monday["dinner"]
            ]

            for item in monday_dinner:
                await item.sync_details(con)

            menu.monday["dinner"] = monday_dinner

    if params.tuesday is not None:
        if params.tuesday["breakfast"] is not None:
            tuesday_breakfast = [
                MessMenuItem(id=item_id) for item_id in params.tuesday["breakfast"]
            ]

            for item in tuesday_breakfast:
                await item.sync_details(con)

            menu.tuesday["breakfast"] = tuesday_breakfast

        if params.tuesday["lunch"] is not None:
            tuesday_lunch = [
                MessMenuItem(id=item_id) for item_id in params.tuesday["lunch"]
            ]

            for item in tuesday_lunch:
                await item.sync_details(con)

            menu.tuesday["lunch"] = tuesday_lunch

        if params.tuesday["snacks"] is not None:
            tuesday_snacks = [
                MessMenuItem(id=item_id) for item_id in params.tuesday["snacks"]
            ]

            for item in tuesday_snacks:
                await item.sync_details(con)

            menu.tuesday["snacks"] = tuesday_snacks

        if params.tuesday["dinner"] is not None:
            tuesday_dinner = [
                MessMenuItem(id=item_id) for item_id in params.tuesday["dinner"]
            ]

            for item in tuesday_dinner:
                await item.sync_details(con)

            menu.tuesday["dinner"] = tuesday_dinner

    if params.wednesday is not None:
        if params.wednesday["breakfast"] is not None:
            wednesday_breakfast = [
                MessMenuItem(id=item_id) for item_id in params.wednesday["breakfast"]
            ]

            for item in wednesday_breakfast:
                await item.sync_details(con)

            menu.wednesday["breakfast"] = wednesday_breakfast

        if params.wednesday["lunch"] is not None:
            wednesday_lunch = [
                MessMenuItem(id=item_id) for item_id in params.wednesday["lunch"]
            ]

            for item in wednesday_lunch:
                await item.sync_details(con)

            menu.wednesday["lunch"] = wednesday_lunch

        if params.wednesday["snacks"] is not None:
            wednesday_snacks = [
                MessMenuItem(id=item_id) for item_id in params.wednesday["snacks"]
            ]

            for item in wednesday_snacks:
                await item.sync_details(con)

            menu.wednesday["snacks"] = wednesday_snacks

        if params.wednesday["dinner"] is not None:
            wednesday_dinner = [
                MessMenuItem(id=item_id) for item_id in params.wednesday["dinner"]
            ]

            for item in wednesday_dinner:
                await item.sync_details(con)

            menu.wednesday["dinner"] = wednesday_dinner

    if params.thursday is not None:
        if params.thursday["breakfast"] is not None:
            thursday_breakfast = [
                MessMenuItem(id=item_id) for item_id in params.thursday["breakfast"]
            ]

            for item in thursday_breakfast:
                await item.sync_details(con)

            menu.thursday["breakfast"] = thursday_breakfast

        if params.thursday["lunch"] is not None:
            thursday_lunch = [
                MessMenuItem(id=item_id) for item_id in params.thursday["lunch"]
            ]

            for item in thursday_lunch:
                await item.sync_details(con)

            menu.thursday["lunch"] = thursday_lunch

        if params.thursday["snacks"] is not None:
            thursday_snacks = [
                MessMenuItem(id=item_id) for item_id in params.thursday["snacks"]
            ]

            for item in thursday_snacks:
                await item.sync_details(con)

            menu.thursday["snacks"] = thursday_snacks

        if params.thursday["dinner"] is not None:
            thursday_dinner = [
                MessMenuItem(id=item_id) for item_id in params.thursday["dinner"]
            ]

            for item in thursday_dinner:
                await item.sync_details(con)

            menu.thursday["dinner"] = thursday_dinner

    if params.friday is not None:
        if params.friday["breakfast"] is not None:
            friday_breakfast = [
                MessMenuItem(id=item_id) for item_id in params.friday["breakfast"]
            ]

            for item in friday_breakfast:
                await item.sync_details(con)

            menu.friday["breakfast"] = friday_breakfast

        if params.friday["lunch"] is not None:
            friday_lunch = [
                MessMenuItem(id=item_id) for item_id in params.friday["lunch"]
            ]

            for item in friday_lunch:
                await item.sync_details(con)

            menu.friday["lunch"] = friday_lunch

        if params.friday["snacks"] is not None:
            friday_snacks = [
                MessMenuItem(id=item_id) for item_id in params.friday["snacks"]
            ]

            for item in friday_snacks:
                await item.sync_details(con)

            menu.friday["snacks"] = friday_snacks

        if params.friday["dinner"] is not None:
            friday_dinner = [
                MessMenuItem(id=item_id) for item_id in params.friday["dinner"]
            ]

            for item in friday_dinner:
                await item.sync_details(con)

            menu.friday["dinner"] = friday_dinner

    if params.saturday is not None:
        if params.saturday["breakfast"] is not None:
            saturday_breakfast = [
                MessMenuItem(id=item_id) for item_id in params.saturday["breakfast"]
            ]

            for item in saturday_breakfast:
                await item.sync_details(con)

            menu.saturday["breakfast"] = saturday_breakfast

        if params.saturday["lunch"] is not None:
            saturday_lunch = [
                MessMenuItem(id=item_id) for item_id in params.saturday["lunch"]
            ]

            for item in saturday_lunch:
                await item.sync_details(con)

            menu.saturday["lunch"] = saturday_lunch

        if params.saturday["snacks"] is not None:
            saturday_snacks = [
                MessMenuItem(id=item_id) for item_id in params.saturday["snacks"]
            ]

            for item in saturday_snacks:
                await item.sync_details(con)

            menu.saturday["snacks"] = saturday_snacks

        if params.saturday["dinner"] is not None:
            saturday_dinner = [
                MessMenuItem(id=item_id) for item_id in params.saturday["dinner"]
            ]

            for item in saturday_dinner:
                await item.sync_details(con)

            menu.saturday["dinner"] = saturday_dinner

    if params.sunday is not None:
        if params.sunday["breakfast"] is not None:
            sunday_breakfast = [
                MessMenuItem(id=item_id) for item_id in params.sunday["breakfast"]
            ]

            for item in sunday_breakfast:
                await item.sync_details(con)

            menu.sunday["breakfast"] = sunday_breakfast

        if params.sunday["lunch"] is not None:
            sunday_lunch = [
                MessMenuItem(id=item_id) for item_id in params.sunday["lunch"]
            ]

            for item in sunday_lunch:
                await item.sync_details(con)

            menu.sunday["lunch"] = sunday_lunch

        if params.sunday["snacks"] is not None:
            sunday_snacks = [
                MessMenuItem(id=item_id) for item_id in params.sunday["snacks"]
            ]

            for item in sunday_snacks:
                await item.sync_details(con)

            menu.sunday["snacks"] = sunday_snacks

        if params.sunday["dinner"] is not None:
            sunday_dinner = [
                MessMenuItem(id=item_id) for item_id in params.sunday["dinner"]
            ]

            for item in sunday_dinner:
                await item.sync_details(con)

            menu.sunday["dinner"] = sunday_dinner

    await menu.update(con)

    disconnect(con)

    return {"menu": obj_to_json(menu)}


@router.delete(
    "/mess_menu/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete any Mess Menu by ID",
    tags=["[ADMIN] Mess"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": DeleteMessMenuResponseModel_ERR_404,
        }
    },
)
async def delete_mess_menu(id: int, api_key: APIKey = Depends(get_api_key)):
    con = connect()
    menu = MessMenu(id=id)
    await menu.sync_details(con)

    await menu.remove(con)

    disconnect(con)


@router.get(
    "/mess_menu_item",
    summary="Get Details of all Mess Menu Items",
    tags=["Mess"],
    response_model=GetAllMessMenuItemsDetails,
)
async def get_all_mess_menu_items_details():
    con = connect()
    cursor = con.cursor()

    cursor.execute("SELECT id FROM mess_menu_items")
    result = cursor.fetchall()
    ids = [row[0] for row in result]

    cursor.close()

    details = []
    for id in ids:
        item = MessMenuItem(id=id)
        await item.sync_details(con)

        details.append(obj_to_json(item))

    disconnect(con)

    return {"items": details}


@router.get(
    "/mess_menu_item/{id}",
    summary="Get Details of any Mess Menu Item by ID",
    tags=["Mess"],
    response_model=GetMessMenuItemDetailsResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": GetMessMenuItemDetailsResponseModel_ERR_404,
        }
    },
)
async def get_mess_menu_item_details(id: int):
    con = connect()

    item = MessMenuItem(id=id)
    await item.sync_details(con)

    disconnect(con)

    return {"item": obj_to_json(item)}


@router.post(
    "/mess_menu_item",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Mess Menu Item",
    tags=["[ADMIN] Mess"],
    response_model=CreateMessMenuItemResponseModel,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request Error",
            "model": CreateMessMenuItemResponseModel_ERR_400,
        }
    },
)
async def create_mess_menu_item(
    params: NewMessMenuItemBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()

    item = MessMenuItem(**params.model_dump())
    try:
        await item.sync_details(con)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mess menu item already exists",
        )
    except HTTPException as e:
        if e.status_code != status.HTTP_404_NOT_FOUND:
            disconnect(con)
            raise e

    await item.create(con)

    disconnect(con)

    return {"item": obj_to_json(item)}


@router.put(
    "/mess_menu_item/{id}",
    summary="Update Details of any Mess Menu Item by ID",
    tags=["[ADMIN] Mess"],
    response_model=UpdateMessMenuItemResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": UpdateMessMenuItemResponseModel_ERR_404,
        }
    },
)
async def update_mess_menu_item(
    id: int,
    params: UpdateMessMenuItemBodyParams,
    api_key: APIKey = Depends(get_api_key),
):
    con = connect()
    item = MessMenuItem(id=id)
    await item.sync_details(con)

    params_dict = params.model_dump()
    for key, value in params_dict.items():
        if value is not None:
            setattr(item, key, value)

    await item.update(con)

    disconnect(con)

    return {"item": obj_to_json(item)}


@router.delete(
    "/mess_menu_item/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete any Mess Menu Item by ID",
    tags=["[ADMIN] Mess"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": DeleteMessMenuItemResponseModel_ERR_404,
        }
    },
)
async def delete_mess_menu_item(id: int, api_key: APIKey = Depends(get_api_key)):
    con = connect()
    item = MessMenuItem(id=id)
    await item.sync_details(con)

    await item.remove(con)

    disconnect(con)
