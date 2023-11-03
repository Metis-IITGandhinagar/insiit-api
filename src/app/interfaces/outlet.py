from typing import Optional, List
from app.interfaces.common import Location
from appTypes.outletTypes import FoodOutletMenu, FoodOutletDetails, FoodOutletDBValues
from datetime import time
from fastapi import HTTPException, status
import psycopg2
import psycopg2.extensions
import geopy.distance
from app.db import disconnect


class FoodOutletMenuItem:
    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        outlet_id: int | None = None,
        price: int | None = None,
        description: str | None = None,
        rating: float | None = None,
        size: str | None = None,
        cal: int | None = None,
        image: str | None = None,
    ):
        self.id = id
        self.name = name
        self.price = price
        self.outlet_id = outlet_id
        self.description = description
        self.rating = rating
        self.size = size
        self.cal = cal
        self.image = image

    async def sync_details(self, con: psycopg2.extensions.connection):
        cursor = con.cursor()

        if self.id is not None:
            cursor.execute(f"SELECT * FROM food_outlet_menu_items WHERE id={self.id}")
        elif (self.name is not None) and (self.outlet_id is not None):
            cursor.execute(
                f"SELECT * FROM food_outlet_menu_items WHERE name=%s AND food_outlet_id={self.outlet_id}",
                (self.name),
            )
        else:
            disconnect(con)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient data"
            )

        result = cursor.fetchone()
        cursor.close()

        try:
            self.id = result[0]
            self.name = result[1]
            self.price = result[2]
            self.description = result[3]
            self.rating = result[4]
            self.size = result[5]
            self.cal = result[6]
            self.image = result[7]
            self.outlet_id = result[8]
        except TypeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found"
            )

    async def create(self, con: psycopg2.extensions.connection):
        cursor = con.cursor()

        cursor.execute(
            "INSERT INTO food_outlet_menu_items (name, price, food_outlet_id, description, rating, size, cal, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (
                self.name,
                self.price,
                self.outlet_id,
                self.description,
                self.rating,
                self.size,
                self.cal,
                self.image,
            ),
        )

        self.id = cursor.fetchone()[0]
        con.commit()

        cursor.execute(f"SELECT menu FROM food_outlets WHERE id={self.outlet_id}")
        result = cursor.fetchone()
        menu = list(result[0])

        menu.append(self.id)

        cursor.execute(
            f"UPDATE food_outlets SET menu='[{', '.join([str(item_id) for item_id in menu])}]' WHERE id={self.outlet_id}"
        )
        con.commit()

        cursor.close()
        await self.sync_details(con=con)
        return self.__dict__

    async def update(self, con: psycopg2.extensions.connection):
        cursor = con.cursor()

        cursor.execute(
            f"UPDATE food_outlet_menu_items SET name=%s, price=%s, food_outlet_id=%s, description=%s, rating=%s, size=%s, cal=%s, image=%s WHERE id={self.id}",
            (
                self.name,
                self.price,
                self.outlet_id,
                self.description,
                self.rating,
                self.size,
                self.cal,
                self.image,
            ),
        )
        con.commit()
        cursor.close()
        return self.__dict__

    async def remove(self, con: psycopg2.extensions.connection):
        cursor = con.cursor()

        cursor.execute(f"SELECT menu FROM food_outlets WHERE id={self.outlet_id}")
        result = cursor.fetchone()
        menu = list(result[0])

        menu.remove(self.id)

        cursor.execute(
            f"UPDATE food_outlets SET menu='[{', '.join([str(id) for id in menu])}]' WHERE id={self.outlet_id}",
        )

        con.commit()

        cursor.execute(f"DELETE FROM food_outlet_menu_items WHERE id={self.id}")
        con.commit()
        cursor.close()


class FoodOutlet:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        location: Optional[Location] = None,
        landmark: Optional[str] = None,
        open_time: Optional[time] = None,
        close_time: Optional[time] = None,
        rating: Optional[float] = None,
        menu: Optional[List[FoodOutletMenuItem]] = None,
        image: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.location = location
        self.landmark = landmark
        self.open_time = open_time
        self.close_time = close_time
        self.rating = rating
        self.menu = menu
        self.image = image

    async def sync_details(self, con: psycopg2.extensions.connection):
        cursor = con.cursor()

        if self.id is not None:
            cursor.execute(f"SELECT * FROM food_outlets WHERE id={self.id}")
        elif self.name is not None:
            cursor.execute(f"SELECT * FROM food_outlets WHERE name='{self.name}'")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient data"
            )

        result = cursor.fetchone()

        try:
            self.id = result[0]
            self.name = result[1]
            self.location = (
                Location(
                    latitude=result[2]["latitude"], longitude=result[2]["longitude"]
                )
                if result[2] is not None
                else None
            )
            self.landmark = result[3]
            self.open_time = result[4]
            self.close_time = result[5]
            self.rating = result[6]

            menu_ids = result[7] if result[7] is not None else []
            menu = []
            for i in range(len(menu_ids)):
                item = FoodOutletMenuItem(id=menu_ids[i])
                await item.sync_details(con=con)
                menu.append(item)
            self.menu = menu if len(menu) > 0 else None

            self.image = result[8]
        except TypeError as e:
            # print(e)
            # print("disconnected here")
            disconnect(con)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Food outlet not found"
            )

    async def create(self, con: psycopg2.extensions.connection) -> FoodOutletDetails:
        cursor = con.cursor()

        location_value = (
            str(
                {
                    "latitude": self.location.latitude,
                    "longitude": self.location.longitude,
                }
            )
            if self.location is not None
            else None
        )

        menu_value = [item.id for item in self.menu] if self.menu is not None else None

        cursor.execute(
            f"INSERT INTO food_outlets(name, location, landmark, open_time, close_time, rating, menu, image) VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
            (
                self.name,
                location_value,
                self.landmark,
                self.open_time,
                self.close_time,
                self.rating,
                menu_value,
                self.image,
            ),
        )

        self.id = cursor.fetchone()[0]
        con.commit()
        await self.sync_details(con)
        return self.__dict__

    async def update(self, con: psycopg2.extensions.connection) -> FoodOutletDetails:
        cursor = con.cursor()

        location_value = (
            str(
                {
                    "latitude": self.location.latitude,
                    "longitude": self.location.longitude,
                }
            )
            if self.location is not None
            else None
        )

        menu_value = [item.id for item in self.menu] if self.menu is not None else None

        cursor.execute(
            f"UPDATE food_outlets SET name=%s, location=%s, landmark=%s, open_time=%s, close_time=%s, rating=%s, menu=%s, image=%s WHERE id={self.id}",
            (
                self.name,
                location_value,
                self.landmark,
                self.open_time,
                self.close_time,
                self.rating,
                menu_value,
                self.image,
            ),
        )
        con.commit()
        return self.__dict__

    async def remove(self, con: psycopg2.extensions.connection):
        cursor = con.cursor()

        cursor.execute(f"DELETE FROM food_outlets WHERE id={self.id}")
        con.commit()


async def searchOutlets(
    con: psycopg2.extensions.connection,
    nameFilter: Optional[str] = None,
    locationFilter: Optional[Location] = None,
    landmarkFilter: Optional[str] = None,
    timeFilter: Optional[time] = None,
    ratingFilter: Optional[float] = None,
    itemFilter: Optional[str] = None,
) -> List[FoodOutletDetails]:
    cursor = con.cursor()

    cursor.execute(f"SELECT id FROM food_outlets")
    result = cursor.fetchall()

    outlets: List[FoodOutlet] = []

    for row in result:
        outlet = FoodOutlet(id=row[0])
        outlets.append(outlet)

    cursor.close()

    for outlet in outlets:
        await outlet.sync_details(con=con)
        if outlet.menu is not None:
            for item in outlet.menu:
                await item.sync_details(con=con)

    outlets = list(
        filter(
            lambda outlet: True
            if nameFilter is None
            else (True if outlet.name.find(nameFilter) != -1 else False),
            outlets,
        )
    )

    outlets = list(
        filter(
            lambda outlet: True
            if locationFilter is None
            else (
                True
                if geopy.distance.geodesic(
                    (
                        float(locationFilter["latitude"]),
                        float(locationFilter["longitude"]),
                    ),
                    (float(outlet.location.latitude), float(outlet.location.longitude)),
                ).km
                <= 1
                else False
            ),
            outlets,
        )
    )

    outlets = list(
        filter(
            lambda outlet: True
            if landmarkFilter is None
            else (
                False
                if outlet.landmark is None
                else (True if outlet.landmark.find(landmarkFilter) != -1 else False)
            ),
            outlets,
        )
    )

    outlets = list(
        filter(
            lambda outlet: True
            if timeFilter is None
            else (
                False
                if outlet.open_time is None or outlet.close_time is None
                else (
                    True
                    if (outlet.open_time <= timeFilter)
                    and (outlet.close_time > timeFilter)
                    else False
                )
            ),
            outlets,
        )
    )

    outlets = list(
        filter(
            lambda outlet: True
            if ratingFilter is None
            else (
                False
                if outlet.rating is None
                else (True if outlet.rating >= ratingFilter else False)
            ),
            outlets,
        )
    )

    outlets = list(
        filter(
            lambda outlet: True
            if itemFilter is None
            else (
                False
                if outlet.menu is None
                else (
                    True
                    if [-1 for _ in range(len(outlet.menu))]
                    != [item.name.find(itemFilter) for item in outlet.menu]
                    else False
                )
            ),
            outlets,
        )
    )

    return outlets
