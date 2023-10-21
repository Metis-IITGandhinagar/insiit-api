from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define data models
class BusSchedule(BaseModel):
    from_location: str
    to_location: str
    departure_time: str
    via: List[str]
    capacity: int

# Simulated database
bus_schedule_db = []

# Endpoint to add a new bus schedule
@app.post("/bus-schedule/", response_model=BusSchedule)
def create_bus_schedule(schedule: BusSchedule):
    bus_schedule_db.append(schedule)
    return schedule

# Endpoint to retrieve all bus schedules
@app.get("/bus-schedule/", response_model=List[BusSchedule])
def get_all_bus_schedules():
    return bus_schedule_db

# Endpoint to retrieve bus schedules by departure and destination locations
@app.get("/bus-schedule/search/")
def search_bus_schedules(from_location: str, to_location: str):
    matching_schedules = [
        schedule
        for schedule in bus_schedule_db
        if schedule.from_location == from_location and schedule.to_location == to_location
    ]
    if matching_schedules:
        return matching_schedules
    raise HTTPException(status_code=404, detail="Bus schedules not found")

# Endpoint to update an existing bus schedule by index
@app.put("/bus-schedule/{index}", response_model=BusSchedule)
def update_bus_schedule(index: int, schedule: BusSchedule):
    if 0 <= index < len(bus_schedule_db):
        bus_schedule_db[index] = schedule
        return schedule
    raise HTTPException(status_code=404, detail="Bus schedule not found")

# Endpoint to delete a bus schedule by index
@app.delete("/bus-schedule/{index}", response_model=BusSchedule)
def delete_bus_schedule(index: int):
    if 0 <= index < len(bus_schedule_db):
        deleted_schedule = bus_schedule_db.pop(index)
        return deleted_schedule
    raise HTTPException(status_code=404, detail="Bus schedule not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
