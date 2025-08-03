import json
from fastapi.testclient import TestClient

client = TestClient(app)

def request_predictions(data):
    # Call the AI model with preprocessed sensor data
    predictions = {"landslide_probability": 0.7, "flood_probability": 0.4}
    return json.dumps(predictions)