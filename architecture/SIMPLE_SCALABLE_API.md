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
    
    USERS[Users/Sensors] --> API
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

### Day 4: ML Model Integration
```bash
# What you'll build:
- Simple XGBoost models for landslide/flood prediction
- Feature engineering from sensor data
- Model serving in FastAPI
- Prediction caching with Redis
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
│   ├── ml_predictor.py      # ML models & predictions
│   └── auth.py              # Simple authentication
├── consumer/
│   ├── main.py              # Kafka consumer
│   └── processors.py       # Message processing
├── ml/
│   ├── models/              # Trained model files
│   └── train.py             # Model training script
├── docker-compose.yml       # All services
└── requirements.txt         # Dependencies
```

## Key Features (Simple but Scalable)

### API Endpoints
```python
POST /api/v1/sensor-data     # Receive sensor data
GET  /api/v1/alerts          # Get alerts
GET  /api/v1/health          # Health check
POST /api/v1/predictions     # Get ML predictions (NEW)
GET  /api/v1/model-info      # Get model version info (NEW)
```

### Performance Features
- **Async FastAPI** - Handle 1000+ concurrent requests
- **Connection pooling** - Efficient database usage
- **Redis caching** - Fast response times + ML prediction caching
- **Kafka async** - Non-blocking message processing
- **ML Models** - XGBoost for fast predictions (<50ms)

### Scalability Features
- **Horizontal scaling** - Add more API instances
- **Database indexing** - Fast queries
- **Caching strategy** - Reduce database load + cache ML predictions
- **Background processing** - Kafka consumers + async ML inference
- **Model serving** - In-memory models for fast predictions

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
❌ **Complex ML pipelines** - Simple XGBoost models only
❌ **Model versioning** - Basic file-based model storage

## Success Criteria

### Week 1 Goals
- [ ] API handles 1000+ concurrent requests
- [ ] Kafka processes messages reliably
- [ ] Database queries under 50ms
- [ ] Redis caching works
- [ ] ML models predict landslide/flood risk
- [ ] Docker deployment works
- [ ] Basic authentication implemented

### Ready for Production
- [ ] Environment variables configured
- [ ] Error handling implemented
- [ ] Basic logging added
- [ ] Health checks working
- [ ] ML models trained and loaded
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

## ML Model Integration (Simple Approach)

### Quick ML Setup
```python
# api/ml_predictor.py - Simple but effective
import xgboost as xgb
import joblib
import numpy as np

class SimpleMLPredictor:
    def __init__(self):
        self.landslide_model = joblib.load('ml/models/landslide.pkl')
        self.flood_model = joblib.load('ml/models/flood.pkl')
    
    def predict(self, sensor_data):
        # Simple feature extraction
        features = [
            sensor_data.rainfall,
            sensor_data.soil_moisture,
            sensor_data.ground_movement,
            sensor_data.water_level
        ]
        
        landslide_prob = self.landslide_model.predict_proba([features])[0][1]
        flood_prob = self.flood_model.predict_proba([features])[0][1]
        
        return {
            "landslide": {"probability": landslide_prob, "risk": self.get_risk(landslide_prob)},
            "flood": {"probability": flood_prob, "risk": self.get_risk(flood_prob)}
        }
    
    def get_risk(self, prob):
        if prob > 0.7: return "high"
        elif prob > 0.4: return "medium"
        else: return "low"
```

### Training Data (Start Simple)
```python
# ml/train.py - Generate synthetic data for initial model
import pandas as pd
import numpy as np
from xgboost import XGBClassifier

# Generate 10k samples of realistic sensor data
def create_training_data():
    data = []
    for i in range(10000):
        rainfall = np.random.exponential(10)
        soil_moisture = np.random.beta(2, 5)
        ground_movement = np.random.exponential(0.1)
        water_level = np.random.exponential(2)
        
        # Simple risk calculation
        landslide_risk = (rainfall > 50) * 0.4 + (soil_moisture > 0.8) * 0.3 + (ground_movement > 0.5) * 0.3
        landslide = 1 if landslide_risk > 0.6 else 0
        
        data.append([rainfall, soil_moisture, ground_movement, water_level, landslide])
    
    return pd.DataFrame(data, columns=['rainfall', 'soil_moisture', 'ground_movement', 'water_level', 'landslide'])

# Train and save model
df = create_training_data()
X = df[['rainfall', 'soil_moisture', 'ground_movement', 'water_level']]
y = df['landslide']

model = XGBClassifier(n_estimators=100, max_depth=6)
model.fit(X, y)
joblib.dump(model, 'ml/models/landslide.pkl')
```

## Next Steps

1. **Start with existing code** - Build on what you have
2. **Add simple ML models** - XGBoost with basic features
3. **Focus on core features** - Sensor data + ML predictions + alerts
4. **Test early and often** - Make sure predictions make sense
5. **Deploy simple first** - Single instance, then scale
6. **Collect real data** - Improve models over time

This approach gives you a production-ready, scalable API with ML capabilities without the complexity. You can always improve the models later as you collect more real data.