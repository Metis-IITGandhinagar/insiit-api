from fastapi import APIRouter, HTTPException, status, Depends
from app.db import connect, disconnect
from app.models.bus import (
    create_bus_route,
    create_bus_schedule,
    create_bus_stop,
    create_bus_type,
    get_bus_route_by_id,
    get_bus_routes,
    get_bus_schedule_by_id,
    get_bus_schedules,
    get_bus_stop_by_id,
    get_bus_stops,
    get_bus_type_by_id,
    get_bus_types,
    remove_bus_route,
    remove_bus_schedule,
    update_bus_route,
    update_bus_schedule,
    update_bus_type,
)
from app.models.globals import Location
from app.utils.globals import obj_to_json
from fastapi.security.api_key import APIKey
from app.auth.key import get_api_key
from app.models.responses._bus import (
    GetAllBusTypesResponseModel,
    GetBusTypeResponseModel,
    GetBusTypeResponseModel_ERR_404,
    NewBusTypeResponseModel,
    NewBusTypeResponseModel_ERR_400,
    UpdateBusTypeResponseModel,
    UpdateBusTypeResponseModel_ERR_404,
    DeleteBusTypeResponseModel_ERR_404,
    GetAllBusStopsResponseModel,
    GetBusStopResponseModel,
    GetBusStopResponseModel_ERR_404,
    NewBusStopResponseModel,
    NewBusStopResponseModel_ERR_400,
    UpdateBusStopResponseModel,
    UpdateBusStopResponseModel_ERR_404,
    DeleteBusStopResponseModel_ERR_404,
    GetAllBusRoutesResponseModel,
    GetBusRouteResponseModel,
    GetBusRouteResponseModel_ERR_404,
    NewBusRouteResponseModel,
    NewBusRouteResponseModel_ERR_400,
    NewBusRouteResponseModel_ERR_404,
    UpdateBusRouteResponseModel,
    UpdateBusRouteResponseModel_ERR_404,
    DeleteBusRouteResponseModel_ERR_404,
    GetAllBusSchedulesResponseModel,
    GetBusScheduleResponseModel,
    GetBusScheduleResponseModel_ERR_404,
    NewBusScheduleResponseModel,
    NewBusScheduleResponseModel_ERR_404,
    NewBusScheduleResponseModel_ERR_400,
    UpdateBusScheduleResponseModel,
    UpdateBusScheduleResponseModel_ERR_404,
    UpdateBusScheduleResponseModel_ERR_400,
    DeleteBusScheduleResponseModel_ERR_404,
)
from app.models.requests._bus import (
    NewBusTypeBodyParams,
    UpdateBusTypeBodyParams,
    NewBusStopBodyParams,
    UpdateBusStopBodyParams,
    NewBusRouteBodyParams,
    UpdateBusRouteBodyParams,
    NewBusScheduleBodyParams,
    UpdateBusScheduleBodyParams,
)

router = APIRouter()


@router.get(
    "/bus_type",
    summary="Get Details of All Bus Types",
    tags=["bus"],
    response_model=GetAllBusTypesResponseModel,
)
async def get_all_bus_types():
    con = connect()

    bus_types = await get_bus_types(con)
    types_json = obj_to_json(bus_types)

    disconnect(con)

    return {"bus_types": types_json}


@router.get(
    "/bus_type/{id}",
    summary="Get Details of a Bus Type",
    tags=["bus"],
    response_model=GetBusTypeResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": GetBusTypeResponseModel_ERR_404,
        }
    },
)
async def get_bus_type(id: int):
    con = connect()

    bus_type = await get_bus_type_by_id(con, id)

    if bus_type is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bus Type Not Found"
        )

    type_json = obj_to_json(bus_type)

    disconnect(con)

    return {"type": type_json}


@router.post(
    "/bus_type",
    status_code=status.HTTP_201_CREATED,
    summary="Add a New Bus Type",
    tags=["[admin] bus"],
    response_model=NewBusTypeResponseModel,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request Error",
            "model": NewBusTypeResponseModel_ERR_400,
        }
    },
)
async def add_bus_type(
    params: NewBusTypeBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()

    bus_type = await create_bus_type(con, params.name)

    if bus_type is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bus Type Already Exists"
        )

    type_json = obj_to_json(bus_type)

    disconnect(con)

    return {"type": type_json}


@router.put(
    "/bus_type/{id}",
    summary="Update Details of a Bus Type by ID",
    tags=["[admin] bus"],
    response_model=UpdateBusTypeResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": UpdateBusTypeResponseModel_ERR_404,
        }
    },
)
async def modify_bus_type(
    id: int, params: UpdateBusTypeBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()

    bus_type = await get_bus_type_by_id(con, id)

    if bus_type is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bus Type Not Found"
        )

    bus_type.name = params.name
    new_type = update_bus_type(con, bus_type)

    type_json = obj_to_json(new_type)

    disconnect(con)

    return {"type": type_json}


@router.delete(
    "/bus_type/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Bus Type by ID",
    tags=["[admin] bus"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": DeleteBusTypeResponseModel_ERR_404,
        }
    },
)
async def remove_bus_type(id: int, api_key: APIKey = Depends(get_api_key)):
    con = connect()

    bus_type = await get_bus_type_by_id(con, id)

    if bus_type is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bus Type Not Found"
        )

    remove_bus_type(con, bus_type)

    disconnect(con)


@router.get(
    "/bus_stop",
    summary="Get Details of All Bus Stops",
    tags=["bus"],
    response_model=GetAllBusStopsResponseModel,
)
async def get_all_bus_stops():
    con = connect()

    bus_stops = await get_bus_stops(con)
    stops_json = obj_to_json(bus_stops)

    disconnect(con)

    return {"stops": stops_json}


@router.get(
    "/bus_stop/{id}",
    summary="Get Details of a Bus Stop",
    tags=["bus"],
    response_model=GetBusStopResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": GetBusStopResponseModel_ERR_404,
        }
    },
)
async def get_bus_stop(id: int):
    con = connect()

    bus_stop = await get_bus_stop_by_id(con, id)

    if bus_stop is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bus Stop Not Found"
        )

    stop_json = obj_to_json(bus_stop)

    disconnect(con)

    return {"stop": stop_json}


@router.post(
    "/bus_stop",
    status_code=status.HTTP_201_CREATED,
    summary="Add a New Bus Stop",
    tags=["[admin] bus"],
    response_model=NewBusStopResponseModel,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": NewBusStopResponseModel_ERR_400,
        }
    },
)
async def add_bus_stop(
    params: NewBusStopBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()

    stop = await create_bus_stop(
        con,
        params.name,
        (
            Location(params.location.latitude, params.location.longitude)
            if params.location is not None
            else None
        ),
        params.landmark,
    )

    if stop is None:
        disconnect(con)
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Bus Stop Already Exists"
        )

    stop_json = obj_to_json(stop)

    disconnect(con)

    return {"stop": stop_json}


@router.put(
    "/bus_stop/{id}",
    summary="Update Details of any Bus Stop by ID",
    tags=["[admin] bus"],
    response_model=UpdateBusStopResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": UpdateBusStopResponseModel_ERR_404,
        }
    },
)
async def update_bus_stop(
    id: int, params: UpdateBusStopBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()

    stop = await get_bus_stop_by_id(con, id)

    if stop is None:
        disconnect(con)
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Bus Stop Not Found")

    stop.name = params.name
    stop.location = (
        Location(params.location.latitude, params.location.longitude)
        if params.location is not None
        else None
    )
    stop.landmark = params.landmark

    new_stop = update_bus_stop(con, stop)

    stop_json = obj_to_json(new_stop)

    disconnect(con)

    return {"stop": stop_json}


@router.delete(
    "/bus_stop/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Bus Stop by ID",
    tags=["[admin] bus"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": DeleteBusStopResponseModel_ERR_404,
        }
    },
)
async def remove_bus_stop(id: int, api_key: APIKey = Depends(get_api_key)):
    con = connect()

    stop = await get_bus_stop_by_id(con, id)

    if stop is None:
        disconnect(con)
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Bus Stop Not Found")

    remove_bus_stop(con, stop)

    disconnect(con)


@router.get(
    "/bus_route",
    summary="Get Details of All Bus Routes",
    tags=["bus"],
    response_model=GetAllBusRoutesResponseModel,
)
async def get_all_bus_routes():
    con = connect()

    routes = await get_bus_routes(con)
    routes_json = obj_to_json(routes)

    disconnect(con)

    return {"routes": routes_json}


@router.get(
    "/bus_route/{id}",
    summary="Get Details of a Bus Route",
    tags=["bus"],
    response_model=GetBusRouteResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": GetBusRouteResponseModel_ERR_404,
        }
    },
)
async def get_bus_route(id: int):
    con = connect()

    route = await get_bus_route_by_id(con, id)

    if route is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bus Route Not Found"
        )

    route_json = obj_to_json(route)

    disconnect(con)

    return {"route": route_json}


@router.post(
    "/bus_route",
    status_code=status.HTTP_201_CREATED,
    summary="Add a New Bus Route",
    tags=["[admin] bus"],
    response_model=NewBusRouteResponseModel,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request Error",
            "model": NewBusRouteResponseModel_ERR_400,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": NewBusRouteResponseModel_ERR_404,
        },
    },
)
async def new_bus_route(
    params: NewBusRouteBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()

    from_stop = await get_bus_stop_by_id(con, params.from_stop_id)
    if from_stop is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="FROM Bus Stop Not Found"
        )

    to_stop = await get_bus_stop_by_id(con, params.to_stop_id)
    if to_stop is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TO Bus Stop Not Found"
        )

    via_stops = []
    for stop_id in params.via_stops:
        stop = await get_bus_stop_by_id(con, stop_id)
        if stop is None:
            disconnect(con)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="VIA Bus Stop Not Found"
            )
        via_stops.append(stop)

    route = await create_bus_route(con, params.name, from_stop, to_stop, via_stops)
    if route is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bus Route Already Exists"
        )

    route_json = obj_to_json(route)

    return {"route": route_json}


@router.put(
    "/bus_route/{id}",
    summary="Update Details of a Bus Route by ID",
    tags=["[admin] bus"],
    response_model=UpdateBusRouteResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": UpdateBusRouteResponseModel_ERR_404,
        }
    },
)
async def modify_bus_route(
    id: int, params: UpdateBusRouteBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()

    route = await get_bus_route_by_id(con, id)
    if route is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bus Route Not Found"
        )

    if params.from_stop_id is not None:
        from_stop = await get_bus_stop_by_id(con, params.from_stop_id)
        if from_stop is None:
            disconnect(con)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="FROM Bus Stop Not Found"
            )
        route.from_stop = from_stop

    if params.to_stop_id is not None:
        to_stop = await get_bus_stop_by_id(con, params.to_stop_id)
        if to_stop is None:
            disconnect(con)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="TO Bus Stop Not Found"
            )
        route.to_stop = to_stop

    if params.via_stops is not None:
        via_stops = []
        for stop_id in params.via_stops:
            stop = await get_bus_stop_by_id(con, stop_id)
            if stop is None:
                disconnect(con)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="VIA Bus Stop Not Found",
                )
            via_stops.append(stop)
        route.via_stops = via_stops

    route = await update_bus_route(con, route)
    route_json = obj_to_json(route)

    return {"route": route_json}


@router.delete(
    "/bus_route/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Bus Route by ID",
    tags=["[admin] bus"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": DeleteBusRouteResponseModel_ERR_404,
        }
    },
)
async def delete_bus_route(id: int, api_key: APIKey = Depends(get_api_key)):
    con = connect()

    route = await get_bus_route_by_id(con, id)
    if route is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bus Route Not Found"
        )

    remove_bus_route(con, route)

    disconnect(con)


@router.get(
    "/bus_schedule",
    summary="Get Details of All Bus Schedules",
    tags=["bus"],
    response_model=GetAllBusSchedulesResponseModel,
)
async def get_all_bus_schedules():
    con = connect()

    schedules = await get_bus_schedules(con)
    schedules_json = obj_to_json(schedules)

    disconnect(con)

    return {"schedules": schedules_json}


@router.get(
    "/bus_schedule/{id}",
    summary="Get Details of a Bus Schedule",
    tags=["bus"],
    response_model=GetBusScheduleResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": GetBusScheduleResponseModel_ERR_404,
        }
    },
)
async def get_bus_schedule(id: int):
    con = connect()

    schedule = await get_bus_schedule_by_id(con, id)
    if schedule is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bus Schedule Not Found"
        )

    schedule_json = obj_to_json(schedule)

    disconnect(con)

    return {"schedule": schedule_json}


@router.post(
    "/bus_schedule",
    status_code=status.HTTP_201_CREATED,
    summary="Add a New Bus Schedule",
    tags=["[admin] bus"],
    response_model=NewBusScheduleResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": NewBusScheduleResponseModel_ERR_404,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request Error",
            "model": NewBusScheduleResponseModel_ERR_400,
        },
    },
)
async def new_bus_schedule(
    params: NewBusScheduleBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()

    route = await get_bus_route_by_id(con, params.route_id)
    if route is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bus Route Not Found"
        )

    bus_type = await get_bus_type_by_id(con, params.bus_type_id)
    if bus_type is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bus Type Not Found"
        )

    try:
        schedule = await create_bus_schedule(
            con,
            route,
            bus_type,
            params.start_time,
            params.end_time,
            params.via_stops_times,
        )
    except ValueError:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Time Format",
        )

    if schedule is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bus Schedule Already Exists",
        )

    disconnect(con)

    schedule_json = obj_to_json(schedule)

    return {"schedule": schedule_json}


@router.put(
    "/bus_schedule/{id}",
    summary="Update Details of a Bus Schedule by ID",
    tags=["[admin] bus"],
    response_model=UpdateBusScheduleResponseModel,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": UpdateBusScheduleResponseModel_ERR_404,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request Error",
            "model": UpdateBusScheduleResponseModel_ERR_400,
        },
    },
)
async def modify_bus_schedule(
    id: int, params: UpdateBusScheduleBodyParams, api_key: APIKey = Depends(get_api_key)
):
    con = connect()

    schedule = await get_bus_schedule_by_id(con, id)
    if schedule is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bus Schedule Not Found"
        )

    if params.route_id is not None:
        route = await get_bus_route_by_id(con, params.route_id)
        if route is None:
            disconnect(con)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Bus Route Not Found"
            )
        schedule.route = route

    if params.bus_type_id is not None:
        bus_type = await get_bus_type_by_id(con, params.bus_type_id)
        if bus_type is None:
            disconnect(con)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Bus Type Not Found"
            )
        schedule.bus_type = bus_type

    if params.start_time is not None:
        schedule.start_time = params.start_time

    if params.end_time is not None:
        schedule.end_time = params.end_time

    if params.via_stops_times is not None:
        schedule.via_stop_times = params.via_stops_times

    try:
        schedule = await update_bus_schedule(con, schedule)
    except ValueError:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Time Format",
        )

    schedule_json = obj_to_json(schedule)

    disconnect(con)

    return {"schedule": schedule_json}


@router.delete(
    "/bus_schedule/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Bus Schedule by ID",
    tags=["[admin] bus"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found Error",
            "model": DeleteBusScheduleResponseModel_ERR_404,
        }
    },
)
async def delete_bus_schedule(id: int, api_key: APIKey = Depends(get_api_key)):
    con = connect()

    schedule = await get_bus_schedule_by_id(con, id)
    if schedule is None:
        disconnect(con)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Bus Schedule Not Found"
        )

    remove_bus_schedule(con, schedule)

    disconnect(con)
