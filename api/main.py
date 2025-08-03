from fastapi import FastAPI
from fastapi.requests import Request
from pydantic import BaseModel
from .database import store_sensor_data

app = FastAPI()

@app.post("/sensordata")
async def receive_sensor_data(request: Request):
    # Process and transform sensor data if necessary
    sensor_data = await request.json()
    
    # Store sensor data in the database
    store_sensor_data(sensor_data)
    
    return {"message": "Sensor data received"}