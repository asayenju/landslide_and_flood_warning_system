from fastapi import FastAPI
from fastapi.requests import Request
from pydantic import BaseModel

app = FastAPI()
@app.get("/")
def read_root():
    return {"Good Morning": "World"}


@app.post("/sensordata")
async def receive_sensor_data(request: Request):
    # Process and transform sensor data if necessary
    sensor_data = await request.json()
    
    return {"message": "Sensor data received: " + str(sensor_data)}