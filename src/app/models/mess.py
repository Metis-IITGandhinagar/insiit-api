import psycopg2.extensions
from fastapi import HTTPException, status
from app.utils._db import json_to_sql
from app.models.globals import Location
from typing_extensions import TypedDict
from datetime import time
from typing import Optional


class MessMenuItem:
    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        description: str | None = None,
        rating: float | None = None,
        cal: int | None = None,
        image: str | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.description = description
        self.rating = rating
        self.cal = cal
        self.image = image

    async def sync_details(self, con: psycopg2.extensions.connection) -> None:
        cursor = con.cursor()

        if self.id is not None:
            cursor.execute(f"SELECT * FROM mess_menu_items WHERE id={self.id}")
        elif self.name is not None:
            cursor.execute("SELECT * FROM mess_menu_items WHERE name=%s", (self.name,))
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient data to fetch mess menu item details",
            )

        result = cursor.fetchone()
        cursor.close()

        try:
            self.id = result[0]
            self.name = result[1]
            self.description = result[2]
            self.rating = result[3]
            self.cal = result[4]
            self.image = result[5]
        except TypeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mess menu item not found",
            )

    async def create(self, con: psycopg2.extensions.connection) -> None:
        cursor = con.cursor()

        cursor.execute(
            "INSERT INTO mess_menu_items (name, description, rating, cal, image) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (self.name, self.description, self.rating, self.cal, self.image),
        )

        con.commit()

        self.id = cursor.fetchone()[0]
        cursor.close()

        await self.sync_details(con)

    async def update(self, con: psycopg2.extensions.connection) -> None:
        cursor = con.cursor()

        cursor.execute(
            "UPDATE mess_menu_items SET name=%s, description=%s, rating=%s, cal=%s, image=%s WHERE id=%s",
            (self.name, self.description, self.rating, self.cal, self.image, self.id),
        )
        con.commit()

        cursor.close()

        await self.sync_details(con)

    async def remove(self, con: psycopg2.extensions.connection) -> None:
        cursor = con.cursor()

        cursor.execute(f"DELETE FROM mess_menu_items WHERE id={self.id}")
        con.commit()

        cursor.close()


class DayMenu(TypedDict):
    breakfast: Optional[list[MessMenuItem] | list[int]]
    lunch: Optional[list[MessMenuItem] | list[int]]
    snacks: Optional[list[MessMenuItem] | list[int]]
    dinner: Optional[list[MessMenuItem] | list[int]]


class MessMenu:
    def __init__(
        self,
        id: int | None = None,
        month: int | None = None,
        year: int | None = None,
        monday: DayMenu | None = None,
        tuesday: DayMenu | None = None,
        wednesday: DayMenu | None = None,
        thursday: DayMenu | None = None,
        friday: DayMenu | None = None,
        saturday: DayMenu | None = None,
        sunday: DayMenu | None = None,
    ) -> None:
        self.id = id
        self.month = month
        self.year = year
        self.monday = monday
        self.tuesday = tuesday
        self.wednesday = wednesday
        self.thursday = thursday
        self.friday = friday
        self.saturday = saturday
        self.sunday = sunday

    async def sync_details(self, con: psycopg2.extensions.connection) -> None:
        cursor = con.cursor()

        if self.id is not None:
            cursor.execute(f"SELECT * FROM mess_menus WHERE id={self.id}")
        elif self.month is not None and self.year is not None:
            cursor.execute(
                "SELECT * FROM mess_menus WHERE month=%s AND year=%s",
                (self.month, self.year),
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient data to fetch mess menu details",
            )

        result = cursor.fetchone()
        cursor.close()

        try:
            self.id = result[0]
            self.month = result[1]
            self.year = result[2]

            monday_breakfast: list[int] | None = result[3]
            monday_lunch: list[int] | None = result[4]
            monday_snacks: list[int] | None = result[5]
            monday_dinner: list[int] | None = result[6]

            self.monday = {
                "breakfast": [MessMenuItem(id=item_id) for item_id in monday_breakfast]
                if monday_breakfast is not None
                else None,
                "lunch": [MessMenuItem(id=item_id) for item_id in monday_lunch]
                if monday_lunch is not None
                else None,
                "snacks": [MessMenuItem(id=item_id) for item_id in monday_snacks]
                if monday_snacks is not None
                else None,
                "dinner": [MessMenuItem(id=item_id) for item_id in monday_dinner]
                if monday_dinner is not None
                else None,
            }

            tuesday_breakfast: list[int] | None = result[7]
            tuesday_lunch: list[int] | None = result[8]
            tuesday_snacks: list[int] | None = result[9]
            tuesday_dinner: list[int] | None = result[10]

            self.tuesday = {
                "breakfast": [MessMenuItem(id=item_id) for item_id in tuesday_breakfast]
                if tuesday_breakfast is not None
                else None,
                "lunch": [MessMenuItem(id=item_id) for item_id in tuesday_lunch]
                if tuesday_lunch is not None
                else None,
                "snacks": [MessMenuItem(id=item_id) for item_id in tuesday_snacks]
                if tuesday_snacks is not None
                else None,
                "dinner": [MessMenuItem(id=item_id) for item_id in tuesday_dinner]
                if tuesday_dinner is not None
                else None,
            }

            wednesday_breakfast: list[int] | None = result[11]
            wednesday_lunch: list[int] | None = result[12]
            wednesday_snacks: list[int] | None = result[13]
            wednesday_dinner: list[int] | None = result[14]

            self.wednesday = {
                "breakfast": [
                    MessMenuItem(id=item_id) for item_id in wednesday_breakfast
                ]
                if wednesday_breakfast is not None
                else None,
                "lunch": [MessMenuItem(id=item_id) for item_id in wednesday_lunch]
                if wednesday_lunch is not None
                else None,
                "snacks": [MessMenuItem(id=item_id) for item_id in wednesday_snacks]
                if wednesday_snacks is not None
                else None,
                "dinner": [MessMenuItem(id=item_id) for item_id in wednesday_dinner]
                if wednesday_dinner is not None
                else None,
            }

            thursday_breakfast: list[int] | None = result[15]
            thursday_lunch: list[int] | None = result[16]
            thursday_snacks: list[int] | None = result[17]
            thursday_dinner: list[int] | None = result[18]

            self.thursday = {
                "breakfast": [
                    MessMenuItem(id=item_id) for item_id in thursday_breakfast
                ]
                if thursday_breakfast is not None
                else None,
                "lunch": [MessMenuItem(id=item_id) for item_id in thursday_lunch]
                if thursday_lunch is not None
                else None,
                "snacks": [MessMenuItem(id=item_id) for item_id in thursday_snacks]
                if thursday_snacks is not None
                else None,
                "dinner": [MessMenuItem(id=item_id) for item_id in thursday_dinner]
                if thursday_dinner is not None
                else None,
            }

            friday_breakfast: list[int] | None = result[19]
            friday_lunch: list[int] | None = result[20]
            friday_snacks: list[int] | None = result[21]
            friday_dinner: list[int] | None = result[22]

            self.friday = {
                "breakfast": [MessMenuItem(id=item_id) for item_id in friday_breakfast]
                if friday_breakfast is not None
                else None,
                "lunch": [MessMenuItem(id=item_id) for item_id in friday_lunch]
                if friday_lunch is not None
                else None,
                "snacks": [MessMenuItem(id=item_id) for item_id in friday_snacks]
                if friday_snacks is not None
                else None,
                "dinner": [MessMenuItem(id=item_id) for item_id in friday_dinner]
                if friday_dinner is not None
                else None,
            }

            saturday_breakfast: list[int] | None = result[23]
            saturday_lunch: list[int] | None = result[24]
            saturday_snacks: list[int] | None = result[25]
            saturday_dinner: list[int] | None = result[26]

            self.saturday = {
                "breakfast": [
                    MessMenuItem(id=item_id) for item_id in saturday_breakfast
                ]
                if saturday_breakfast is not None
                else None,
                "lunch": [MessMenuItem(id=item_id) for item_id in saturday_lunch]
                if saturday_lunch is not None
                else None,
                "snacks": [MessMenuItem(id=item_id) for item_id in saturday_snacks]
                if saturday_snacks is not None
                else None,
                "dinner": [MessMenuItem(id=item_id) for item_id in saturday_dinner]
                if saturday_dinner is not None
                else None,
            }

            sunday_breakfast: list[int] | None = result[27]
            sunday_lunch: list[int] | None = result[28]
            sunday_snacks: list[int] | None = result[29]
            sunday_dinner: list[int] | None = result[30]

            self.sunday = {
                "breakfast": [MessMenuItem(id=item_id) for item_id in sunday_breakfast]
                if sunday_breakfast is not None
                else None,
                "lunch": [MessMenuItem(id=item_id) for item_id in sunday_lunch]
                if sunday_lunch is not None
                else None,
                "snacks": [MessMenuItem(id=item_id) for item_id in sunday_snacks]
                if sunday_snacks is not None
                else None,
                "dinner": [MessMenuItem(id=item_id) for item_id in sunday_dinner]
                if sunday_dinner is not None
                else None,
            }

            if self.monday["breakfast"] is not None:
                for item in self.monday["breakfast"]:
                    await item.sync_details(con)

            if self.monday["lunch"] is not None:
                for item in self.monday["lunch"]:
                    await item.sync_details(con)

            if self.monday["snacks"] is not None:
                for item in self.monday["snacks"]:
                    await item.sync_details(con)

            if self.monday["dinner"] is not None:
                for item in self.monday["dinner"]:
                    await item.sync_details(con)

            if self.tuesday["breakfast"] is not None:
                for item in self.tuesday["breakfast"]:
                    await item.sync_details(con)

            if self.tuesday["lunch"] is not None:
                for item in self.tuesday["lunch"]:
                    await item.sync_details(con)

            if self.tuesday["snacks"] is not None:
                for item in self.tuesday["snacks"]:
                    await item.sync_details(con)

            if self.tuesday["dinner"] is not None:
                for item in self.tuesday["dinner"]:
                    await item.sync_details(con)

            if self.wednesday["breakfast"] is not None:
                for item in self.wednesday["breakfast"]:
                    await item.sync_details(con)

            if self.wednesday["lunch"] is not None:
                for item in self.wednesday["lunch"]:
                    await item.sync_details(con)

            if self.wednesday["snacks"] is not None:
                for item in self.wednesday["snacks"]:
                    await item.sync_details(con)

            if self.wednesday["dinner"] is not None:
                for item in self.wednesday["dinner"]:
                    await item.sync_details(con)

            if self.thursday["breakfast"] is not None:
                for item in self.thursday["breakfast"]:
                    await item.sync_details(con)

            if self.thursday["lunch"] is not None:
                for item in self.thursday["lunch"]:
                    await item.sync_details(con)

            if self.thursday["snacks"] is not None:
                for item in self.thursday["snacks"]:
                    await item.sync_details(con)

            if self.thursday["dinner"] is not None:
                for item in self.thursday["dinner"]:
                    await item.sync_details(con)

            if self.friday["breakfast"] is not None:
                for item in self.friday["breakfast"]:
                    await item.sync_details(con)

            if self.friday["lunch"] is not None:
                for item in self.friday["lunch"]:
                    await item.sync_details(con)

            if self.friday["snacks"] is not None:
                for item in self.friday["snacks"]:
                    await item.sync_details(con)

            if self.friday["dinner"] is not None:
                for item in self.friday["dinner"]:
                    await item.sync_details(con)

            if self.saturday["breakfast"] is not None:
                for item in self.saturday["breakfast"]:
                    await item.sync_details(con)

            if self.saturday["lunch"] is not None:
                for item in self.saturday["lunch"]:
                    await item.sync_details(con)

            if self.saturday["snacks"] is not None:
                for item in self.saturday["snacks"]:
                    await item.sync_details(con)

            if self.saturday["dinner"] is not None:
                for item in self.saturday["dinner"]:
                    await item.sync_details(con)

            if self.sunday["breakfast"] is not None:
                for item in self.sunday["breakfast"]:
                    await item.sync_details(con)

            if self.sunday["lunch"] is not None:
                for item in self.sunday["lunch"]:
                    await item.sync_details(con)

            if self.sunday["snacks"] is not None:
                for item in self.sunday["snacks"]:
                    await item.sync_details(con)

            if self.sunday["dinner"] is not None:
                for item in self.sunday["dinner"]:
                    await item.sync_details(con)
        except TypeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mess menu not found",
            )

    async def create(self, con: psycopg2.extensions.connection) -> None:
        cursor = con.cursor()

        cursor.execute(
            f"""INSERT INTO mess_menus (month, year, monday_breakfast, monday_lunch, monday_snacks, monday_dinner, tuesday_breakfast, tuesday_lunch, tuesday_snacks, tuesday_dinner, wednesday_breakfast, wednesday_lunch, wednesday_snacks, wednesday_dinner, thursday_breakfast, thursday_lunch, thursday_snacks, thursday_dinner, friday_breakfast, friday_lunch, friday_snacks, friday_dinner, saturday_breakfast, saturday_lunch, saturday_snacks, saturday_dinner, sunday_breakfast, sunday_lunch, sunday_snacks, sunday_dinner) VALUES (%s, %s, '{[item.id for item in self.monday["breakfast"]] if self.monday is not None and self.monday["breakfast"] is not None else []}', '{[item.id for item in self.monday["lunch"]] if self.monday is not None and self.monday["lunch"] is not None else []}', '{[item.id for item in self.monday["snacks"]] if self.monday is not None and self.monday["snacks"] is not None else []}', '{[item.id for item in self.monday["dinner"]] if self.monday is not None and self.monday["dinner"] is not None else []}', '{[item.id for item in self.tuesday["breakfast"]] if self.tuesday is not None and self.tuesday["breakfast"] is not None else []}', '{[item.id for item in self.tuesday["lunch"]] if self.tuesday is not None and self.tuesday["lunch"] is not None else []}', '{[item.id for item in self.tuesday["snacks"]] if self.tuesday is not None and self.tuesday["snacks"] is not None else []}', '{[item.id for item in self.tuesday["dinner"]] if self.tuesday is not None and self.tuesday["dinner"] is not None else []}', '{[item.id for item in self.wednesday["breakfast"]] if self.wednesday is not None and self.wednesday["breakfast"] is not None else []}', '{[item.id for item in self.wednesday["lunch"]] if self.wednesday is not None and self.wednesday["lunch"] is not None else []}', '{[item.id for item in self.wednesday["snacks"]] if self.wednesday is not None and self.wednesday["snacks"] is not None else []}', '{[item.id for item in self.wednesday["dinner"]] if self.wednesday is not None and self.wednesday["dinner"] is not None else []}', '{[item.id for item in self.thursday["breakfast"]] if self.thursday is not None and self.thursday["breakfast"] is not None else []}', '{[item.id for item in self.thursday["lunch"]] if self.thursday is not None and self.thursday["lunch"] is not None else []}', '{[item.id for item in self.thursday["sncaks"]] if self.thursday is not None and self.thursday["sncaks"] is not None else []}', '{[item.id for item in self.thursday["dinner"]] if self.thursday is not None and self.thursday["dinner"] is not None else []}', '{[item.id for item in self.friday["breakfast"]] if self.friday is not None and self.friday["breakfast"] is not None else []}', '{[item.id for item in self.friday["lunch"]] if self.friday is not None and self.friday["lunch"] is not None else []}', '{[item.id for item in self.friday["snacks"]] if self.friday is not None and self.friday["snacks"] is not None else []}', '{[item.id for item in self.friday["dinner"]] if self.friday is not None and self.friday["dinner"] is not None else []}', '{[item.id for item in self.saturday["breakfast"]] if self.saturday is not None and self.saturday["breakfast"] is not None else []}', '{[item.id for item in self.saturday["lunch"]] if self.saturday is not None and self.saturday["lunch"] is not None else []}', '{[item.id for item in self.saturday["snacks"]] if self.saturday is not None and self.saturday["snacks"] is not None else []}', '{[item.id for item in self.saturday["dinner"]] if self.saturday is not None and self.saturday["dinner"] is not None else []}', '{[item.id for item in self.sunday["breakfast"]] if self.sunday is not None and self.sunday["breakfast"] is not None else []}', '{[item.id for item in self.sunday["lunch"]] if self.sunday is not None and self.sunday["lunch"] is not None else []}', '{[item.id for item in self.sunday["snacks"]] if self.sunday is not None and self.sunday["snacks"] is not None else []}', '{[item.id for item in self.sunday["dinner"]] if self.sunday is not None and self.sunday["dinner"] is not None else []}') RETURNING id""",
            (self.month, self.year),
        )

        con.commit()

        self.id = cursor.fetchone()[0]
        cursor.close()

        await self.sync_details(con)

    async def update(self, con: psycopg2.extensions.connection) -> None:
        cursor = con.cursor()

        cursor.execute(
            f"""UPDATE mess_menus SET monday_breakfast='{[item.id for item in self.monday["breakfast"]] if self.monday is not None and self.monday["breakfast"] is not None else []}', monday_lunch='{[item.id for item in self.monday["lunch"]] if self.monday is not None and self.monday["lunch"] is not None else []}', monday_snacks='{[item.id for item in self.monday["snacks"]] if self.monday is not None and self.monday["snacks"] is not None else []}', monday_dinner='{[item.id for item in self.monday["dinner"]] if self.monday is not None and self.monday["dinner"] is not None else []}', tuesday_breakfast='{[item.id for item in self.tuesday["breakfast"]] if self.tuesday is not None and self.tuesday["breakfast"] is not None else []}', tuesday_lunch='{[item.id for item in self.tuesday["lunch"]] if self.tuesday is not None and self.tuesday["lunch"] is not None else []}', tuesday_snacks='{[item.id for item in self.tuesday["snacks"]] if self.tuesday is not None and self.tuesday["snacks"] is not None else []}', tuesday_dinner='{[item.id for item in self.tuesday["dinner"]] if self.tuesday is not None and self.tuesday["dinner"] is not None else []}', wednesday_breakfast='{[item.id for item in self.wednesday["breakfast"]] if self.wednesday is not None and self.wednesday["breakfast"] is not None else []}', wednesday_lunch='{[item.id for item in self.wednesday["lunch"]] if self.wednesday is not None and self.wednesday["lunch"] is not None else []}', wednesday_snacks='{[item.id for item in self.wednesday["snacks"]] if self.wednesday is not None and self.wednesday["snacks"] is not None else []}', wednesday_dinner='{[item.id for item in self.wednesday["dinner"]] if self.wednesday is not None and self.wednesday["dinner"] is not None else []}', thursday_breakfast='{[item.id for item in self.thursday["breakfast"]] if self.thursday is not None and self.thursday["breakfast"] is not None else []}', thursday_lunch='{[item.id for item in self.thursday["lunch"]] if self.thursday is not None and self.thursday["lunch"] is not None else []}', thursday_snacks='{[item.id for item in self.thursday["snacks"]] if self.thursday is not None and self.thursday["snacks"] is not None else []}', thursday_dinner='{[item.id for item in self.thursday["dinner"]] if self.thursday is not None and self.thursday["dinner"] is not None else []}', friday_breakfast='{[item.id for item in self.friday["breakfast"]] if self.friday is not None and self.friday["breakfast"] is not None else []}', friday_lunch='{[item.id for item in self.friday["lunch"]] if self.friday is not None and self.friday["lunch"] is not None else []}', friday_snacks='{[item.id for item in self.friday["snacks"]] if self.friday is not None and self.friday["snacks"] is not None else []}', friday_dinner='{[item.id for item in self.friday["dinner"]] if self.friday is not None and self.friday["dinner"] is not None else []}', saturday_breakfast='{[item.id for item in self.saturday["breakfast"]] if self.saturday is not None and self.saturday["breakfast"] is not None else []}', saturday_lunch='{[item.id for item in self.saturday["lunch"]] if self.saturday is not None and self.saturday["lunch"] is not None else []}', saturday_snacks='{[item.id for item in self.saturday["snacks"]] if self.saturday is not None and self.saturday["snacks"] is not None else []}', saturday_dinner='{[item.id for item in self.saturday["dinner"]] if self.saturday is not None and self.saturday["dinner"] is not None else []}', sunday_breakfast='{[item.id for item in self.sunday["breakfast"]] if self.sunday is not None and self.sunday["breakfast"] is not None else []}', sunday_lunch='{[item.id for item in self.sunday["lunch"]] if self.sunday is not None and self.sunday["lunch"] is not None else []}', sunday_snacks='{[item.id for item in self.sunday["snacks"]] if self.sunday is not None and self.sunday["snacks"] is not None else []}', sunday_dinner='{[item.id for item in self.sunday["dinner"]] if self.sunday is not None and self.sunday["dinner"] is not None else []}' WHERE id={self.id}""",
        )

        con.commit()

        cursor.close()

        await self.sync_details(con)

    async def remove(self, con: psycopg2.extensions.connection) -> None:
        cursor = con.cursor()

        cursor.execute(f"DELETE FROM mess_menus WHERE id={self.id}")
        con.commit()

        cursor.close()


class Timings(TypedDict):
    start: time
    end: time


class MessTimings(TypedDict):
    breakfast: Timings
    lunch: Timings
    snacks: Timings
    dinner: Timings


class Mess:
    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        location: Location | None = None,
        landmark: str | None = None,
        timings: MessTimings | None = None,
        rating: float | None = None,
        menu: MessMenu | None = None,
        image: str | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.location = location
        self.landmark = landmark
        self.timings = timings
        self.rating = rating
        self.menu = menu
        self.image = image

    async def sync_details(self, con: psycopg2.extensions.connection) -> None:
        cursor = con.cursor()

        if self.id is not None:
            cursor.execute(f"SELECT * FROM messes WHERE id={self.id}")
        elif self.name is not None:
            cursor.execute("SELECT * FROM messes WHERE name=%s", (self.name,))
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient data to fetch mess details",
            )

        result = cursor.fetchone()
        cursor.close()

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

            timings = result[4]

            self.timings = (
                {
                    "breakfast": {
                        "start": timings["breakfast"]["start"],
                        "end": timings["breakfast"]["end"],
                    },
                    "lunch": {
                        "start": timings["lunch"]["start"],
                        "end": timings["lunch"]["end"],
                    },
                    "snacks": {
                        "start": timings["snacks"]["start"],
                        "end": timings["snacks"]["end"],
                    },
                    "dinner": {
                        "start": timings["dinner"]["start"],
                        "end": timings["dinner"]["end"],
                    },
                }
                if timings is not None
                else None
            )

            self.rating = result[5]

            self.menu = MessMenu(id=result[6]) if result[6] is not None else None
            if self.menu is not None:
                await self.menu.sync_details(con)

            self.image = result[7]

        except TypeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mess not found",
            )

    async def create(self, con: psycopg2.extensions.connection) -> None:
        cursor = con.cursor()

        cursor.execute(
            f"INSERT INTO messes (name, location, landmark, timings, rating, image) VALUES (%s, {json_to_sql({'latitude': self.location.latitude, 'longitude': self.location.longitude}) if self.location is not None else 'NULL'}, %s, {json_to_sql({'breakfast': {'start': self.timings['breakfast']['start'], 'end': self.timings['breakfast']['end']}, 'lunch': {'start': self.timings['lunch']['start'], 'end': self.timings['lunch']['end']}, 'snacks': {'start': self.timings['snacks']['start'],'end': self.timings['snacks']['end']}, 'dinner': {'start': self.timings['dinner']['start'], 'end': self.timings['dinner']['end']}}) if self.timings is not None else 'NULL'}, %s, %s) RETURNING id",
            (
                self.name,
                self.landmark,
                self.rating,
                self.image,
            ),
        )

        con.commit()

        self.id = cursor.fetchone()[0]
        cursor.close()

        self.sync_details(con)

    async def update(self, con: psycopg2.extensions.connection) -> None:
        cursor = con.cursor()

        cursor.execute(
            f"UPDATE messes SET name=%s, location={json_to_sql({'latitude': self.location.latitude, 'longitude': self.location.longitude}) if self.location is not None else 'NULL'}, landmark=%s, timings={json_to_sql({'breakfast': {'start': self.timings['breakfast']['start'], 'end': self.timings['breakfast']['end']}, 'lunch': {'start': self.timings['lunch']['start'], 'end': self.timings['lunch']['end']}, 'snacks': {'start': self.timings['snacks']['start'], 'end': self.timings['snacks']['end']}, 'dinner': {'start': self.timings['dinner']['start'], 'end': self.timings['dinner']['end']}}) if self.timings is not None else 'NULL'}, rating=%s, menu_id=%s, image=%s WHERE id=%s",
            (
                self.name,
                self.landmark,
                self.rating,
                (self.menu.id if self.menu is not None else None),
                self.image,
                self.id,
            ),
        )

        con.commit()
        cursor.close()

        self.sync_details(con)

    async def remove(self, con: psycopg2.extensions.connection) -> None:
        cursor = con.cursor()

        cursor.execute(f"DELETE FROM messes WHERE id={self.id}")
        con.commit()

        cursor.close()
