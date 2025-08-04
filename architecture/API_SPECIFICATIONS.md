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

### 2. Analyze Satellite Image
```http
POST /analyze-image
Content-Type: multipart/form-data
X-API-Key: your-api-key
```

**Request Body (Form Data):**
```
image: [satellite_image.jpg] (file upload)
location_lat: 27.7172 (optional)
location_lng: 85.3240 (optional)
area_name: "Kathmandu Valley" (optional)
```

**Response (Success):**
```json
{
  "analysis_id": "uuid-12345",
  "landslide_detected": true,
  "confidence": 0.87,
  "risk_level": "high",
  "detections": [
    {
      "bbox": [120, 80, 340, 220],
      "confidence": 0.87,
      "class": "landslide",
      "area_affected": 48400
    }
  ],
  "processing_time_ms": 156,
  "timestamp": "2025-08-03T18:21:00Z"
}
```

**Response (Error):**
```json
{
  "error": "Invalid image format",
  "details": "Only JPEG, PNG formats supported",
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

### 4. Batch Image Analysis
```http
POST /batch-analyze
Content-Type: multipart/form-data
X-API-Key: your-api-key
```

**Request Body (Form Data):**
```
images: [image1.jpg, image2.jpg, image3.jpg] (multiple file uploads)
location_data: [{"lat": 27.7172, "lng": 85.3240}, {...}] (JSON array, optional)
```

**Response:**
```json
{
  "batch_id": "batch-12345",
  "total_images": 3,
  "results": [
    {
      "image_name": "image1.jpg",
      "landslide_detected": true,
      "confidence": 0.87,
      "risk_level": "high",
      "detections": [...]
    },
    {
      "image_name": "image2.jpg",
      "landslide_detected": false,
      "confidence": 0.12,
      "risk_level": "low",
      "detections": []
    }
  ],
  "processing_time_ms": 423,
  "timestamp": "2025-08-03T18:21:00Z",
  "model_version": "yolo-v8-landslide-v1.0"
}
```

### 5. Get Analysis History
```http
GET /analysis-history?limit=50&offset=0&risk_level=high
X-API-Key: your-api-key
```

**Query Parameters:**
- `limit` (optional): Number of analyses to return (default: 50, max: 100)
- `offset` (optional): Pagination offset (default: 0)
- `risk_level` (optional): Filter by risk level (low, medium, high, critical)
- `date_from` (optional): Filter from date (ISO 8601)
- `date_to` (optional): Filter to date (ISO 8601)

**Response:**
```json
{
  "analyses": [
    {
      "analysis_id": "uuid-12345",
      "landslide_detected": true,
      "confidence": 0.87,
      "risk_level": "high",
      "location": {
        "latitude": 27.7172,
        "longitude": 85.3240,
        "area_name": "Kathmandu Valley"
      },
      "detections_count": 2,
      "created_at": "2025-08-03T18:20:00Z"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

### 6. Get Model Information
```http
GET /model-info
X-API-Key: your-api-key
```

**Response:**
```json
{
  "model_name": "YOLOv8 Landslide Detector",
  "version": "v1.0.0",
  "accuracy": 0.89,
  "training_date": "2025-08-01T00:00:00Z",
  "classes": ["landslide"],
  "input_size": [640, 640],
  "supported_formats": ["jpg", "jpeg", "png", "tiff"],
  "max_image_size_mb": 10,
  "average_processing_time_ms": 150
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