# Database Schema
## Landslide Flood Warning System

### Overview
Simple, scalable PostgreSQL schema optimized for high-throughput sensor data ingestion and fast alert queries.

## Tables

### 1. sensors
Stores sensor metadata and configuration.

```sql
CREATE TABLE sensors (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location_lat DECIMAL(10, 8) NOT NULL,
    location_lng DECIMAL(11, 8) NOT NULL,
    location_altitude INTEGER DEFAULT 0,
    area_name VARCHAR(100),
    sensor_type VARCHAR(50) NOT NULL DEFAULT 'multi',
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    battery_level INTEGER DEFAULT 100,
    signal_strength INTEGER DEFAULT 100,
    last_maintenance TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_sensors_location ON sensors (location_lat, location_lng);
CREATE INDEX idx_sensors_status ON sensors (status);
CREATE INDEX idx_sensors_area ON sensors (area_name);
```

### 2. sensor_readings
Stores all sensor measurements (time-series data).

```sql
CREATE TABLE sensor_readings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sensor_id VARCHAR(50) NOT NULL REFERENCES sensors(id),
    rainfall DECIMAL(6, 2),
    soil_moisture DECIMAL(4, 3),
    ground_movement DECIMAL(6, 3),
    water_level DECIMAL(6, 2),
    temperature DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    reading_timestamp TIMESTAMP NOT NULL,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE
);

-- Indexes for time-series queries
CREATE INDEX idx_readings_sensor_time ON sensor_readings (sensor_id, reading_timestamp DESC);
CREATE INDEX idx_readings_timestamp ON sensor_readings (reading_timestamp DESC);
CREATE INDEX idx_readings_processed ON sensor_readings (processed) WHERE processed = FALSE;

-- Partition by month for better performance (optional)
-- CREATE TABLE sensor_readings_2025_08 PARTITION OF sensor_readings
-- FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');
```

### 3. alerts
Stores generated alerts and predictions.

```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sensor_id VARCHAR(50) NOT NULL REFERENCES sensors(id),
    alert_type VARCHAR(20) NOT NULL, -- 'landslide', 'flood'
    severity VARCHAR(10) NOT NULL,   -- 'low', 'medium', 'high', 'critical'
    probability DECIMAL(4, 3) NOT NULL,
    confidence DECIMAL(4, 3),
    risk_level VARCHAR(10) NOT NULL,
    message TEXT,
    location_lat DECIMAL(10, 8) NOT NULL,
    location_lng DECIMAL(11, 8) NOT NULL,
    area_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_by VARCHAR(100),
    acknowledged_at TIMESTAMP
);

-- Indexes for alert queries
CREATE INDEX idx_alerts_sensor ON alerts (sensor_id);
CREATE INDEX idx_alerts_type_severity ON alerts (alert_type, severity);
CREATE INDEX idx_alerts_created ON alerts (created_at DESC);
CREATE INDEX idx_alerts_location ON alerts (location_lat, location_lng);
CREATE INDEX idx_alerts_active ON alerts (expires_at) WHERE expires_at > NOW();
```

### 4. api_keys
Stores API authentication keys.

```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    key_hash VARCHAR(64) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    tier VARCHAR(20) NOT NULL DEFAULT 'standard', -- 'standard', 'premium'
    rate_limit INTEGER NOT NULL DEFAULT 1000,
    is_active BOOLEAN DEFAULT TRUE,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP,
    expires_at TIMESTAMP
);

-- Indexes for authentication
CREATE INDEX idx_api_keys_hash ON api_keys (key_hash);
CREATE INDEX idx_api_keys_active ON api_keys (is_active) WHERE is_active = TRUE;
```

### 5. rate_limits
Tracks API usage for rate limiting.

```sql
CREATE TABLE rate_limits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_key_hash VARCHAR(64) NOT NULL,
    endpoint VARCHAR(100) NOT NULL,
    request_count INTEGER NOT NULL DEFAULT 1,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL
);

-- Indexes for rate limiting
CREATE INDEX idx_rate_limits_key_window ON rate_limits (api_key_hash, window_start, window_end);
CREATE INDEX idx_rate_limits_cleanup ON rate_limits (window_end);
```

### 6. system_metadata
Stores system configuration and metadata.

```sql
CREATE TABLE system_metadata (
    key VARCHAR(50) PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default values
INSERT INTO system_metadata (key, value, description) VALUES
('api_version', '1.0.0', 'Current API version'),
('ml_model_version', 'v1.2.0', 'Current ML model version'),
('alert_retention_days', '30', 'Days to keep alerts'),
('reading_retention_days', '365', 'Days to keep sensor readings');
```

## Views for Common Queries

### Latest Sensor Readings
```sql
CREATE VIEW latest_sensor_readings AS
SELECT DISTINCT ON (sensor_id) 
    sensor_id,
    rainfall,
    soil_moisture,
    ground_movement,
    water_level,
    temperature,
    humidity,
    reading_timestamp,
    received_at
FROM sensor_readings
ORDER BY sensor_id, reading_timestamp DESC;
```

### Active Alerts
```sql
CREATE VIEW active_alerts AS
SELECT 
    a.*,
    s.name as sensor_name,
    s.area_name
FROM alerts a
JOIN sensors s ON a.sensor_id = s.id
WHERE a.expires_at > NOW() 
   OR a.expires_at IS NULL
ORDER BY a.created_at DESC;
```

### Sensor Health Status
```sql
CREATE VIEW sensor_health AS
SELECT 
    s.id,
    s.name,
    s.status,
    s.battery_level,
    s.signal_strength,
    s.last_maintenance,
    lr.reading_timestamp as last_reading,
    CASE 
        WHEN lr.reading_timestamp > NOW() - INTERVAL '1 hour' THEN 'online'
        WHEN lr.reading_timestamp > NOW() - INTERVAL '24 hours' THEN 'delayed'
        ELSE 'offline'
    END as connectivity_status
FROM sensors s
LEFT JOIN latest_sensor_readings lr ON s.id = lr.sensor_id;
```

## Database Configuration

### Connection Settings
```sql
-- Optimize for high-throughput writes
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;
```

### Maintenance Tasks
```sql
-- Auto-vacuum settings for high-write tables
ALTER TABLE sensor_readings SET (
    autovacuum_vacuum_scale_factor = 0.1,
    autovacuum_analyze_scale_factor = 0.05
);

-- Cleanup old data (run daily)
DELETE FROM rate_limits WHERE window_end < NOW() - INTERVAL '1 day';
DELETE FROM sensor_readings WHERE reading_timestamp < NOW() - INTERVAL '365 days';
DELETE FROM alerts WHERE expires_at < NOW() - INTERVAL '30 days';
```

## Sample Data

### Insert Sample Sensors
```sql
INSERT INTO sensors (id, name, location_lat, location_lng, area_name) VALUES
('SENSOR_001', 'Kathmandu Valley Sensor 1', 27.7172, 85.3240, 'Kathmandu Valley'),
('SENSOR_002', 'Pokhara Lake Sensor', 28.2096, 83.9856, 'Pokhara Valley'),
('SENSOR_003', 'Chitwan Flood Sensor', 27.5291, 84.3542, 'Chitwan District');
```

### Insert Sample API Key
```sql
-- API key: test-key-12345 (hashed)
INSERT INTO api_keys (key_hash, name, tier, rate_limit) VALUES
('a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'Test API Key', 'standard', 1000);
```

## Migration Scripts

### Initial Setup
```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create all tables in order
\i create_sensors.sql
\i create_sensor_readings.sql
\i create_alerts.sql
\i create_api_keys.sql
\i create_rate_limits.sql
\i create_system_metadata.sql

-- Create views
\i create_views.sql

-- Insert default data
\i insert_defaults.sql
```

### Performance Monitoring Queries
```sql
-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check index usage
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Check slow queries
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

## Backup Strategy

### Daily Backup
```bash
# Full database backup
pg_dump -h localhost -U postgres landslide_flood_db > backup_$(date +%Y%m%d).sql

# Compressed backup
pg_dump -h localhost -U postgres landslide_flood_db | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Point-in-Time Recovery
```sql
-- Enable WAL archiving
ALTER SYSTEM SET archive_mode = 'on';
ALTER SYSTEM SET archive_command = 'cp %p /var/lib/postgresql/archive/%f';
```

This schema is designed for:
- **High-throughput writes** (sensor data ingestion)
- **Fast alert queries** (proper indexing)
- **Scalable growth** (partitioning ready)
- **Simple maintenance** (automated cleanup)
- **Performance monitoring** (built-in queries)