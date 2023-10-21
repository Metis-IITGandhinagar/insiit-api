from fastapi import HTTPException, status
from typing import Optional, List
from datetime import time
import psycopg2
import psycopg2.extensions
import geopy.distance
from app.db import disconnect

class BusScheduleItem:
    def __init__(
        self,
        id: int | None = None,
        from_location: str | None = None,
        to_location: str | None = None,
        departure_time: time | None = None,
        via: List[str] | None = None,
        capacity: int | None = None,
    ):
        self.id = id
        self.from_location = from_location
        self.to_location = to_location
        self.departure_time = departure_time
        self.via = via
        self.capacity = capacity

    async def sync_details(self, con: psycopg2.extensions.connection):
        cursor = con.cursor()

        if self.id is not None:
            cursor.execute(f"SELECT * FROM bus_schedules WHERE id={self.id}")
        elif (self.from_location is not None) and (self.to_location is not None):
            cursor.execute(
                f"SELECT * FROM bus_schedules WHERE from_location=%s AND to_location=%s",
                (self.from_location, self.to_location),
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
            self.from_location = result[1]
            self.to_location = result[2]
            self.departure_time = result[3]
            self.via = result[4]
            self.capacity = result[5]
        except TypeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Bus schedule not found"
            )

    async def create(self, con: psycopg2.extensions.connection):
        cursor = con.cursor()

        cursor.execute(
            "INSERT INTO bus_schedules (from_location, to_location, departure_time, via, capacity) VALUES (%s, %s, %s, %s, %s) RETURNING id",
            (
                self.from_location,
                self.to_location,
                self.departure_time,
                self.via,
                self.capacity,
            ),
        )

        self.id = cursor.fetchone()[0]
        con.commit()
        await self.sync_details(con=con)
        return self.__dict__

    async def update(self, con: psycopg2.extensions.connection):
        cursor = con.cursor()

        cursor.execute(
            f"UPDATE bus_schedules SET from_location=%s, to_location=%s, departure_time=%s, via=%s, capacity=%s WHERE id={self.id}",
            (
                self.from_location,
                self.to_location,
                self.departure_time,
                self.via,
                self.capacity,
            ),
        )
        con.commit()
        cursor.close()
        return self.__dict__

    async def remove(self, con: psycopg2.extensions.connection):
        cursor = con.cursor()

        cursor.execute(f"DELETE FROM bus_schedules WHERE id={self.id}")
        con.commit()

class BusRoute:
    # Define the BusRoute class if necessary, similar to FoodOutlet

    async def searchBusSchedules(
        con: psycopg2.extensions.connection,
        from_location: Optional[str] = None,
        to_location: Optional[str] = None,
        departure_time: Optional[time] = None,
        capacity: Optional[int] = None,
        via: Optional[str] = None,
    ) -> List[BusScheduleItem]:
        cursor = con.cursor()

        cursor.execute(f"SELECT id FROM bus_schedules")
        result = cursor.fetchall()

        schedules: List[BusScheduleItem] = []

        for row in result:
            schedule = BusScheduleItem(id=row[0])
            schedules.append(schedule)

        cursor.close()

        for schedule in schedules:
            await schedule.sync_details(con=con)

        # Apply filtering based on parameters if needed

        return schedules
