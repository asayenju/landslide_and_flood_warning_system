# Simple Scalable FastAPI + Kafka Backend
## Single Developer - 1 Week Implementation

### Overview
A clean, scalable API that can handle high traffic with minimal complexity. Focus on core functionality that works reliably and can be easily deployed.

## Simplified Architecture

```mermaid
graph TB
    subgraph "Simple Stack"
        API[FastAPI App]
        KAFKA[Kafka]
        DB[PostgreSQL]
        REDIS[Redis Cache]
    end
    
    USERS[Users/Satellite] --> API
    API --> KAFKA
    API --> REDIS
    API --> DB
    KAFKA --> CONSUMER[Background Consumer]
    CONSUMER --> DB
```

## Core Components (Only What You Need)

### 1. FastAPI Application
- **Single service** with async endpoints
- **Connection pooling** for database
- **Basic caching** with Redis
- **Simple authentication** (API keys)

### 2. Kafka for Async Processing
- **Single Kafka instance** (can scale later)
- **2 topics**: `sensor.data` and `alerts`
- **Background consumer** for processing

### 3. PostgreSQL Database
- **Single instance** with proper indexing
- **Connection pooling** for performance
- **Simple schema** for sensor data and alerts

### 4. Redis Cache
- **Cache frequent queries**
- **Session storage**
- **Rate limiting data**

## 1-Week Implementation Plan

### Day 1: Core API Structure
```bash
# What you'll build:
- FastAPI app with async endpoints
- Database models and connections
- Basic CRUD operations
- Docker setup
```

### Day 2: Kafka Integration
```bash
# What you'll build:
- Kafka producer in API
- Background consumer service
- Message processing logic
- Error handling
```

### Day 3: Caching & Performance
```bash
# What you'll build:
- Redis integration
- Query caching
- Connection pooling
- Basic rate limiting
```

### Day 4: YOLO Satellite Image Analysis
```bash
# What you'll build:
- YOLOv8 model for landslide detection in satellite images
- Image preprocessing and inference pipeline
- Model serving in FastAPI with GPU support
- Result caching with Redis
```

### Day 5: Authentication & Deployment
```bash
# What you'll build:
- API key authentication
- Docker compose for local dev
- Cloud deployment (single instance)
- Basic testing
```

## File Structure
```
landside_flood_warning_system/
├── api/
│   ├── main.py              # FastAPI app
│   ├── models.py            # Database models
│   ├── database.py          # DB connection
│   ├── cache.py             # Redis operations
│   ├── kafka_client.py      # Kafka producer
│   ├── yolo_predictor.py    # YOLO model & image analysis
│   └── auth.py              # Simple authentication
├── consumer/
│   ├── main.py              # Kafka consumer
│   └── processors.py       # Message processing
├── yolo/
│   ├── models/              # YOLO model files (.pt)
│   ├── datasets/            # Training datasets
│   └── train.py             # YOLO training script
├── docker-compose.yml       # All services
└── requirements.txt         # Dependencies
```

## Key Features (Simple but Scalable)

### API Endpoints
```python
POST /api/v1/analyze-image   # Upload satellite image for analysis
GET  /api/v1/alerts          # Get landslide alerts
GET  /api/v1/health          # Health check
POST /api/v1/batch-analyze   # Batch image analysis (NEW)
GET  /api/v1/model-info      # Get YOLO model info (NEW)
```

### Performance Features
- **Async FastAPI** - Handle 1000+ concurrent requests
- **Connection pooling** - Efficient database usage
- **Redis caching** - Fast response times + ML prediction caching
- **Kafka async** - Non-blocking message processing
- **YOLO Model** - YOLOv8 for satellite image analysis (<200ms per image)

### Scalability Features
- **Horizontal scaling** - Add more API instances
- **Database indexing** - Fast queries
- **Caching strategy** - Reduce database load + cache image analysis results
- **Background processing** - Kafka consumers + async image processing
- **Model serving** - GPU-accelerated YOLO inference

## Simple Deployment Options

### Option 1: Single VPS (Cheapest)
```yaml
# $5-10/month VPS with Docker Compose
- 2GB RAM, 1 CPU
- All services on one machine
- Can handle 1000+ requests/minute
```

### Option 2: Cloud Free Tier
```yaml
# AWS/Azure/GCP free tier
- API: Container service
- Database: Managed PostgreSQL
- Cache: Managed Redis
- Kafka: Self-hosted or managed
```

### Option 3: Docker Swarm (Medium Scale)
```yaml
# 2-3 VPS instances
- Load balancer
- Multiple API instances
- Shared database and cache
```

## Technology Choices (Simple & Popular)

### Core Stack
- **FastAPI** - Fast, modern, easy to use
- **PostgreSQL** - Reliable, well-documented
- **Redis** - Simple caching solution
- **Kafka** - Industry standard messaging
- **Docker** - Easy deployment

### Libraries (Minimal Set)
```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
asyncpg==0.29.0
redis==5.0.1
kafka-python==2.0.2
pydantic==2.5.0
xgboost==2.0.3
scikit-learn==1.3.2
numpy==1.24.3
pandas==2.0.3
joblib==1.3.2
```

## Performance Targets (Realistic)

### Single Instance
- **1,000 concurrent requests** ✅
- **10,000 requests/minute** ✅
- **< 100ms response time** ✅
- **99% uptime** ✅

### With Scaling (2-3 instances)
- **5,000 concurrent requests** ✅
- **50,000 requests/minute** ✅
- **< 50ms response time** ✅
- **99.9% uptime** ✅

## What We're NOT Building (Keep It Simple)

❌ **Complex microservices** - Single API service
❌ **Advanced monitoring** - Basic health checks only
❌ **Service mesh** - Direct service communication
❌ **Advanced security** - API keys are enough
❌ **Complex CI/CD** - Simple deployment scripts
❌ **Multiple databases** - PostgreSQL handles everything
❌ **Advanced caching** - Redis with simple TTL
❌ **Complex ML pipelines** - Simple YOLO inference only
❌ **Model versioning** - Basic file-based model storage

## Success Criteria

### Week 1 Goals
- [ ] API handles 1000+ concurrent requests
- [ ] Kafka processes messages reliably
- [ ] Database queries under 50ms
- [ ] Redis caching works
- [ ] YOLO model detects landslides in satellite images
- [ ] Docker deployment works
- [ ] Basic authentication implemented

### Ready for Production
- [ ] Environment variables configured
- [ ] Error handling implemented
- [ ] Basic logging added
- [ ] Health checks working
- [ ] YOLO model trained and loaded
- [ ] Database migrations ready
- [ ] Documentation written

## Cost Estimate

### Development (Free)
- Local development with Docker Compose
- Free tier cloud services for testing

### Production (Low Cost)
- **VPS Option**: $5-20/month
- **Cloud Option**: $10-50/month (within free tiers initially)
- **Scaling**: Add instances as needed

## YOLO Satellite Image Analysis (Simple Approach)

### Quick YOLO Setup
```python
# api/yolo_predictor.py - YOLO for landslide detection
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image

class YOLOLandslideDetector:
    def __init__(self):
        # Load pre-trained YOLO model (fine-tuned for landslides)
        self.model = YOLO('yolo/models/landslide_yolo.pt')
        
    def analyze_image(self, image_path_or_bytes):
        # Load and preprocess image
        if isinstance(image_path_or_bytes, bytes):
            image = Image.open(io.BytesIO(image_path_or_bytes))
        else:
            image = Image.open(image_path_or_bytes)
        
        # Run YOLO inference
        results = self.model(image)
        
        # Process results
        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    detection = {
                        "bbox": box.xyxy[0].tolist(),  # [x1, y1, x2, y2]
                        "confidence": float(box.conf[0]),
                        "class": "landslide",
                        "area_affected": self.calculate_area(box.xyxy[0])
                    }
                    detections.append(detection)
        
        return {
            "landslide_detected": len(detections) > 0,
            "confidence": max([d["confidence"] for d in detections]) if detections else 0,
            "detections": detections,
            "risk_level": self.get_risk_level(detections)
        }
    
    def get_risk_level(self, detections):
        if not detections:
            return "low"
        
        max_confidence = max([d["confidence"] for d in detections])
        total_area = sum([d["area_affected"] for d in detections])
        
        if max_confidence > 0.8 and total_area > 1000:
            return "critical"
        elif max_confidence > 0.6:
            return "high"
        elif max_confidence > 0.4:
            return "medium"
        else:
            return "low"
    
    def calculate_area(self, bbox):
        # Calculate area of bounding box
        x1, y1, x2, y2 = bbox
        return (x2 - x1) * (y2 - y1)
```

### Training Data (Use Existing Datasets)
```python
# yolo/train.py - Train YOLO on landslide dataset
from ultralytics import YOLO
import os

def train_landslide_yolo():
    # Use existing landslide datasets:
    # 1. Landslide4Sense dataset
    # 2. NASA Landslide Inventory
    # 3. Custom satellite imagery with annotations
    
    # Load base YOLOv8 model
    model = YOLO('yolov8n.pt')  # nano version for speed
    
    # Train on landslide dataset
    results = model.train(
        data='datasets/landslide_dataset.yaml',  # Dataset config
        epochs=100,
        imgsz=640,
        batch=16,
        device='cuda' if torch.cuda.is_available() else 'cpu'
    )
    
    # Save trained model
    model.save('yolo/models/landslide_yolo.pt')
    
    return results

# Dataset structure (YOLO format):
# datasets/
# ├── landslide_dataset.yaml
# ├── train/
# │   ├── images/
# │   └── labels/
# └── val/
#     ├── images/
#     └── labels/
```

### Available Datasets
```python
# Good landslide datasets for YOLO training:

# 1. Landslide4Sense (Recommended)
# - 3,799 image patches
# - Sentinel-2 satellite imagery
# - Pre-labeled landslide areas
# - Download: https://www.iarai.ac.at/landslide4sense/

# 2. NASA Global Landslide Catalog
# - Historical landslide events with coordinates
# - Can be used to find satellite imagery
# - Download: https://data.nasa.gov/

# 3. Custom Dataset Creation
def create_custom_dataset():
    # Use Google Earth Engine or Planet API
    # to get satellite imagery of known landslide areas
    # Then annotate using tools like LabelImg
    pass
```

## Next Steps

1. **Start with existing code** - Build on what you have
2. **Add simple ML models** - XGBoost with basic features
3. **Focus on core features** - Sensor data + ML predictions + alerts
4. **Test early and often** - Make sure predictions make sense
5. **Deploy simple first** - Single instance, then scale
6. **Collect real data** - Improve models over time

This approach gives you a production-ready, scalable API with ML capabilities without the complexity. You can always improve the models later as you collect more real data.