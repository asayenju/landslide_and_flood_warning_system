# API Specifications
## Landslide Flood Warning System

### Base URL
```
Production: https://api.landslide-warning.com/v1
Development: http://localhost:8000/v1
```

### Authentication
All endpoints require an API key in the header:
```
X-API-Key: your-api-key-here
```

## Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-03T18:21:00Z",
  "version": "1.0.0",
  "services": {
    "database": "connected",
    "kafka": "connected",
    "redis": "connected"
  }
}
```

### 2. Submit Sensor Data
```http
POST /sensor-data
Content-Type: application/json
X-API-Key: your-api-key
```

**Request Body:**
```json
{
  "sensor_id": "SENSOR_001",
  "location": {
    "latitude": 27.7172,
    "longitude": 85.3240,
    "altitude": 1400
  },
  "measurements": {
    "rainfall": 25.5,
    "soil_moisture": 0.65,
    "ground_movement": 0.02,
    "water_level": 1.2,
    "temperature": 22.5,
    "humidity": 78.0
  },
  "timestamp": "2025-08-03T18:20:00Z"
}
```

**Response (Success):**
```json
{
  "message": "Sensor data received successfully",
  "data_id": "uuid-12345",
  "processed": true,
  "timestamp": "2025-08-03T18:21:00Z"
}
```

**Response (Error):**
```json
{
  "error": "Invalid sensor data",
  "details": "rainfall value must be between 0 and 1000",
  "timestamp": "2025-08-03T18:21:00Z"
}
```

### 3. Get Alerts
```http
GET /alerts?limit=50&offset=0&severity=high
X-API-Key: your-api-key
```

**Query Parameters:**
- `limit` (optional): Number of alerts to return (default: 50, max: 100)
- `offset` (optional): Pagination offset (default: 0)
- `severity` (optional): Filter by severity (low, medium, high, critical)
- `location` (optional): Filter by location radius "lat,lng,radius_km"

**Response:**
```json
{
  "alerts": [
    {
      "id": "alert-12345",
      "sensor_id": "SENSOR_001",
      "alert_type": "landslide",
      "severity": "high",
      "probability": 0.85,
      "location": {
        "latitude": 27.7172,
        "longitude": 85.3240,
        "area_name": "Kathmandu Valley"
      },
      "message": "High landslide risk detected",
      "created_at": "2025-08-03T18:20:00Z",
      "expires_at": "2025-08-03T20:20:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### 4. Get Predictions
```http
POST /predictions
Content-Type: application/json
X-API-Key: your-api-key
```

**Request Body:**
```json
{
  "sensor_data": {
    "sensor_id": "SENSOR_001",
    "measurements": {
      "rainfall": 25.5,
      "soil_moisture": 0.65,
      "ground_movement": 0.02,
      "water_level": 1.2
    }
  },
  "prediction_type": ["landslide", "flood"]
}
```

**Response:**
```json
{
  "predictions": {
    "landslide": {
      "probability": 0.75,
      "confidence": 0.92,
      "risk_level": "high"
    },
    "flood": {
      "probability": 0.45,
      "confidence": 0.88,
      "risk_level": "medium"
    }
  },
  "timestamp": "2025-08-03T18:21:00Z",
  "model_version": "v1.2.0"
}
```

### 5. Get Sensor Status
```http
GET /sensors/{sensor_id}/status
X-API-Key: your-api-key
```

**Response:**
```json
{
  "sensor_id": "SENSOR_001",
  "status": "active",
  "last_reading": "2025-08-03T18:20:00Z",
  "location": {
    "latitude": 27.7172,
    "longitude": 85.3240,
    "area_name": "Kathmandu Valley"
  },
  "health": {
    "battery_level": 85,
    "signal_strength": 92,
    "last_maintenance": "2025-08-01T10:00:00Z"
  }
}
```

### 6. Bulk Sensor Data
```http
POST /sensor-data/bulk
Content-Type: application/json
X-API-Key: your-api-key
```

**Request Body:**
```json
{
  "readings": [
    {
      "sensor_id": "SENSOR_001",
      "measurements": {...},
      "timestamp": "2025-08-03T18:20:00Z"
    },
    {
      "sensor_id": "SENSOR_002", 
      "measurements": {...},
      "timestamp": "2025-08-03T18:20:30Z"
    }
  ]
}
```

**Response:**
```json
{
  "processed": 2,
  "failed": 0,
  "results": [
    {
      "sensor_id": "SENSOR_001",
      "status": "success",
      "data_id": "uuid-12345"
    },
    {
      "sensor_id": "SENSOR_002",
      "status": "success", 
      "data_id": "uuid-12346"
    }
  ]
}
```

## Error Responses

### Standard Error Format
```json
{
  "error": "Error message",
  "error_code": "VALIDATION_ERROR",
  "details": "Specific details about the error",
  "timestamp": "2025-08-03T18:21:00Z",
  "request_id": "req-12345"
}
```

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (invalid API key)
- `403` - Forbidden (rate limit exceeded)
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error
- `503` - Service Unavailable

## Rate Limits

### Default Limits
- **Standard API Key**: 1000 requests/hour
- **Premium API Key**: 10000 requests/hour
- **Bulk endpoints**: 100 requests/hour

### Rate Limit Headers
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1691087400
```

## Data Validation Rules

### Sensor Data
- `sensor_id`: Required, 3-50 characters, alphanumeric + underscore
- `latitude`: Required, -90 to 90
- `longitude`: Required, -180 to 180
- `altitude`: Optional, -1000 to 10000 meters
- `rainfall`: 0 to 1000 mm
- `soil_moisture`: 0 to 1 (percentage as decimal)
- `ground_movement`: 0 to 100 mm
- `water_level`: 0 to 50 meters
- `temperature`: -50 to 60 degrees Celsius
- `humidity`: 0 to 100 percentage

### Timestamps
- ISO 8601 format: `2025-08-03T18:21:00Z`
- Must be within last 24 hours for real-time data
- Future timestamps rejected

## Webhook Support (Optional)

### Alert Webhooks
Register a webhook URL to receive real-time alerts:

```http
POST /webhooks
{
  "url": "https://your-app.com/webhook",
  "events": ["alert.created", "alert.updated"],
  "secret": "your-webhook-secret"
}
```

**Webhook Payload:**
```json
{
  "event": "alert.created",
  "data": {
    "alert": {...}
  },
  "timestamp": "2025-08-03T18:21:00Z"
}
```

## SDK Examples

### Python
```python
import requests

headers = {"X-API-Key": "your-api-key"}
data = {
    "sensor_id": "SENSOR_001",
    "measurements": {"rainfall": 25.5}
}

response = requests.post(
    "http://localhost:8000/v1/sensor-data",
    json=data,
    headers=headers
)
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/v1/sensor-data', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-api-key'
  },
  body: JSON.stringify({
    sensor_id: 'SENSOR_001',
    measurements: { rainfall: 25.5 }
  })
});
```

### cURL
```bash
curl -X POST http://localhost:8000/v1/sensor-data \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"sensor_id": "SENSOR_001", "measurements": {"rainfall": 25.5}}'