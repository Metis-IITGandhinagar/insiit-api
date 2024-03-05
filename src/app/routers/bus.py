from fastapi import APIRouter, HTTPException, status, Depends
from app.db import connect, disconnect
from app.models.bus import (
    create_bus_route,
    create_bus_stop,
    get_bus_route_by_id,
    get_bus_routes,
    get_bus_stop_by_id,
    get_bus_stops,
    remove_bus_route,
    update_bus_route,
)
from app.models.globals import Location
from app.utils.globals import obj_to_json
from fastapi.security.api_key import APIKey
from app.auth.key import get_api_key
from app.models.responses._bus import (
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
)
from app.models.requests._bus import (
    NewBusStopBodyParams,
    UpdateBusStopBodyParams,
    NewBusRouteBodyParams,
    UpdateBusRouteBodyParams,
)

router = APIRouter()


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
