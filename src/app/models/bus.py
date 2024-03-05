from app.models.globals import Location
from datetime import datetime, time
from typing import Union, TypeVar, List
from psycopg2.extensions import connection


# bus types
BUS_56_SEATER = TypeVar("BUS_56_SEATER")
BUS_29_SEATER = TypeVar("BUS_29_SEATER")


class BusStop:
    def __init__(
        self,
        id: int,
        name: str,
        location: Union[Location, None] = None,
        landmark: Union[str, None] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.location = location
        self.landmark = landmark

    def __repr__(self) -> str:
        return f"BusStop(id={self.id}, name={self.name}, location={self.location}, landmark={self.landmark})"


async def get_bus_stops(con: connection) -> List[BusStop]:
    cursor = con.cursor()

    cursor.execute("SELECT * FROM bus_stops")
    result = cursor.fetchall()

    cursor.close()

    stops = [
        BusStop(
            id=stop[0],
            name=stop[1],
            location=(
                Location(stop[2], stop[3])
                if (stop[2] is not None) and (stop[3] is not None)
                else None
            ),
            landmark=stop[4],
        )
        for stop in result
    ]

    return stops


async def get_bus_stop_by_id(con: connection, id: int) -> Union[BusStop, None]:
    cursor = con.cursor()

    cursor.execute("SELECT * FROM bus_stops WHERE id=%s", (id,))
    result = cursor.fetchone()

    cursor.close()

    if result is None:
        return None

    stop = BusStop(
        id=result[0],
        name=result[1],
        location=(
            Location(result[2], result[3])
            if (result[2] is not None) and (result[3] is not None)
            else None
        ),
        landmark=result[4],
    )

    return stop


async def create_bus_stop(
    con: connection,
    name: str,
    location: Union[Location, None] = None,
    landmark: Union[str, None] = None,
) -> Union[BusStop, None]:
    cursor = con.cursor()

    cursor.execute("SELECT * FROM bus_stops WHERE name=%s", (name,))
    result = cursor.fetchone()
    if result is not None:
        cursor.close()
        return None

    cursor.execute(
        "INSERT INTO bus_stops (name, latitude, longitude, landmark) VALUES (%s, %s, %s, %s) RETURNING id",
        (
            name,
            location.latitude if location is not None else None,
            location.longitude if location is not None else None,
            landmark,
        ),
    )

    id: int = cursor.fetchone()[0]

    cursor.close()

    return BusStop(id, name, location, landmark)


async def update_bus_stop(con: connection, stop: BusStop) -> BusStop:
    cursor = con.cursor()

    cursor.execute(
        "UPDATE bus_stops SET name=%s, latitude=%s, longitude=%s, landmark=%s WHERE id=%s",
        (
            stop.name,
            stop.location.latitude if stop.location is not None else None,
            stop.location.longitude if stop.location is not None else None,
            stop.landmark,
            stop.id,
        ),
    )

    cursor.close()

    return stop


async def remove_bus_stop(con: connection, stop: BusStop) -> None:
    cursor = con.cursor()

    cursor.execute("DELETE FROM bus_stops WHERE id=%s", (stop.id,))

    cursor.close()


class BusRoute:
    def __init__(
        self,
        id: int,
        name: str,
        from_stop: BusStop,
        to_stop: BusStop,
        via_stops: List[BusStop],
    ) -> None:
        self.id = id
        self.name = name
        self.from_stop = from_stop
        self.to_stop = to_stop
        self.via_stops = via_stops


async def get_bus_routes(con: connection) -> List[BusRoute]:
    cursor = con.cursor()

    cursor.execute("SELECT * FROM bus_routes")
    result = cursor.fetchall()

    cursor.close()

    routes = [
        BusRoute(
            id=route[0],
            name=route[1],
            from_stop=await get_bus_stop_by_id(con, route[2]),
            to_stop=await get_bus_stop_by_id(con, route[3]),
            via_stops=[await get_bus_stop_by_id(con, stop_id) for stop_id in route[4]],
        )
        for route in result
    ]

    return routes


async def get_bus_route_by_id(con: connection, id: int) -> Union[BusRoute, None]:
    cursor = con.cursor()

    cursor.execute("SELECT * FROM bus_routes WHERE id=%s", (id,))
    result = cursor.fetchone()

    cursor.close()

    if result is None:
        return None

    route = BusRoute(
        id=result[0],
        name=result[1],
        from_stop=await get_bus_stop_by_id(con, result[2]),
        to_stop=await get_bus_stop_by_id(con, result[3]),
        via_stops=[await get_bus_stop_by_id(con, stop_id) for stop_id in result[4]],
    )

    return route


async def create_bus_route(
    con: connection,
    name: str,
    from_stop: BusStop,
    to_stop: BusStop,
    via_stops: List[BusStop],
) -> Union[BusRoute, None]:
    cursor = con.cursor()

    cursor.execute("SELECT * FROM bus_routes WHERE name=%s", (name,))
    result = cursor.fetchone()
    if result is not None:
        cursor.close()
        return None

    cursor.execute(
        "INSERT INTO bus_routes (name, from_stop, to_stop, via_stops) VALUES (%s, %s, %s, %s) RETURNING id",
        (name, from_stop.id, to_stop.id, [stop.id for stop in via_stops]),
    )

    id: int = cursor.fetchone()[0]

    cursor.close()

    return BusRoute(id, name, from_stop, to_stop, via_stops)


async def update_bus_route(con: connection, route: BusRoute) -> BusRoute:
    cursor = con.cursor()

    cursor.execute(
        "UPDATE bus_routes SET name=%s, from_stop=%s, to_stop=%s, via_stops=%s WHERE id=%s",
        (
            route.name,
            route.from_stop.id,
            route.to_stop.id,
            [stop.id for stop in route.via_stops],
            route.id,
        ),
    )

    cursor.close()

    return route


async def remove_bus_route(con: connection, route: BusRoute) -> None:
    cursor = con.cursor()

    cursor.execute("DELETE FROM bus_routes WHERE id=%s", (route.id,))

    cursor.close()


class BusScheduleItem:
    def __init__(
        self,
        id: int,
        start_time: time,
        route: BusRoute,
        bus_type: Union[BUS_56_SEATER, BUS_29_SEATER],
        end_time: Union[time, None] = None,
        via_stop_times: Union[List[Union[time, None]], None] = None,
    ) -> None:
        self.id = id
        self.start_time = start_time
        self.route = route
        self.bus_type = bus_type
        self.end_time = end_time
        self.via_stop_times = via_stop_times
