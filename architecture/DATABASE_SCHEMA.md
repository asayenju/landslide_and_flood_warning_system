# Database Schema
## Landslide Flood Warning System

### Overview
Simple, scalable PostgreSQL schema optimized for high-throughput sensor data ingestion and fast alert queries.

## Tables

### 1. image_analyses
Stores satellite image analysis results.

```sql
CREATE TABLE image_analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    image_filename VARCHAR(255) NOT NULL,
    image_path VARCHAR(500),
    image_size_bytes INTEGER,
    location_lat DECIMAL(10, 8),
    location_lng DECIMAL(11, 8),
    area_name VARCHAR(100),
    landslide_detected BOOLEAN NOT NULL DEFAULT FALSE,
    confidence DECIMAL(4, 3) NOT NULL,
    risk_level VARCHAR(10) NOT NULL, -- 'low', 'medium', 'high', 'critical'
    detections_count INTEGER DEFAULT 0,
    processing_time_ms INTEGER,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_analyses_location ON image_analyses (location_lat, location_lng);
CREATE INDEX idx_analyses_detected ON image_analyses (landslide_detected);
CREATE INDEX idx_analyses_risk ON image_analyses (risk_level);
CREATE INDEX idx_analyses_created ON image_analyses (created_at DESC);
CREATE INDEX idx_analyses_confidence ON image_analyses (confidence DESC);
```

### 2. landslide_detections
Stores individual landslide detections within images.

```sql
CREATE TABLE landslide_detections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID NOT NULL REFERENCES image_analyses(id) ON DELETE CASCADE,
    bbox_x1 INTEGER NOT NULL,
    bbox_y1 INTEGER NOT NULL,
    bbox_x2 INTEGER NOT NULL,
    bbox_y2 INTEGER NOT NULL,
    confidence DECIMAL(4, 3) NOT NULL,
    area_affected INTEGER, -- calculated area in pixels
    class_name VARCHAR(50) DEFAULT 'landslide',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for detection queries
CREATE INDEX idx_detections_analysis ON landslide_detections (analysis_id);
CREATE INDEX idx_detections_confidence ON landslide_detections (confidence DESC);
CREATE INDEX idx_detections_area ON landslide_detections (area_affected DESC);
```

### 3. alerts
Stores generated alerts from image analysis.

```sql
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID REFERENCES image_analyses(id),
    alert_type VARCHAR(20) NOT NULL DEFAULT 'landslide',
    severity VARCHAR(10) NOT NULL,   -- 'low', 'medium', 'high', 'critical'
    confidence DECIMAL(4, 3) NOT NULL,
    risk_level VARCHAR(10) NOT NULL,
    message TEXT,
    location_lat DECIMAL(10, 8),
    location_lng DECIMAL(11, 8),
    area_name VARCHAR(100),
    detections_count INTEGER DEFAULT 0,
    total_area_affected INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    acknowledged BOOLEAN DEFAULT FALSE,
    acknowledged_by VARCHAR(100),
    acknowledged_at TIMESTAMP
);

-- Indexes for alert queries
CREATE INDEX idx_alerts_analysis ON alerts (analysis_id);
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

### 5. batch_analyses
Stores batch image analysis jobs.

```sql
CREATE TABLE batch_analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    batch_name VARCHAR(255),
    total_images INTEGER NOT NULL,
    processed_images INTEGER DEFAULT 0,
    failed_images INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'processing', -- 'processing', 'completed', 'failed'
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    processing_time_ms INTEGER,
    created_by VARCHAR(100)
);

-- Indexes for batch queries
CREATE INDEX idx_batch_status ON batch_analyses (status);
CREATE INDEX idx_batch_created ON batch_analyses (started_at DESC);
```

### 6. rate_limits
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

### 7. system_metadata
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
('yolo_model_version', 'v1.0.0', 'Current YOLO model version'),
('alert_retention_days', '30', 'Days to keep alerts'),
('analysis_retention_days', '365', 'Days to keep image analyses'),
('max_image_size_mb', '10', 'Maximum image upload size'),
('supported_formats', 'jpg,jpeg,png,tiff', 'Supported image formats');
```

## Views for Common Queries

### Recent High-Risk Analyses
```sql
CREATE VIEW recent_high_risk_analyses AS
SELECT
    ia.*,
    COUNT(ld.id) as detection_count,
    SUM(ld.area_affected) as total_area_affected
FROM image_analyses ia
LEFT JOIN landslide_detections ld ON ia.id = ld.analysis_id
WHERE ia.risk_level IN ('high', 'critical')
  AND ia.created_at > NOW() - INTERVAL '7 days'
GROUP BY ia.id
ORDER BY ia.created_at DESC;
```

### Active Alerts
```sql
CREATE VIEW active_alerts AS
SELECT
    a.*,
    ia.image_filename,
    ia.area_name
FROM alerts a
JOIN image_analyses ia ON a.analysis_id = ia.id
WHERE a.expires_at > NOW()
   OR a.expires_at IS NULL
ORDER BY a.created_at DESC;
```

### Analysis Summary Stats
```sql
CREATE VIEW analysis_summary_stats AS
SELECT
    DATE(created_at) as analysis_date,
    COUNT(*) as total_analyses,
    COUNT(*) FILTER (WHERE landslide_detected = true) as landslides_detected,
    AVG(confidence) as avg_confidence,
    COUNT(*) FILTER (WHERE risk_level = 'high') as high_risk_count,
    COUNT(*) FILTER (WHERE risk_level = 'critical') as critical_risk_count
FROM image_analyses
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY DATE(created_at)
ORDER BY analysis_date DESC;
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
ALTER TABLE image_analyses SET (
    autovacuum_vacuum_scale_factor = 0.1,
    autovacuum_analyze_scale_factor = 0.05
);

-- Cleanup old data (run daily)
DELETE FROM rate_limits WHERE window_end < NOW() - INTERVAL '1 day';
DELETE FROM image_analyses WHERE created_at < NOW() - INTERVAL '365 days';
DELETE FROM alerts WHERE expires_at < NOW() - INTERVAL '30 days';
DELETE FROM batch_analyses WHERE completed_at < NOW() - INTERVAL '90 days';
```

## Sample Data

### Insert Sample Data
```sql
-- Sample image analysis
INSERT INTO image_analyses (
    image_filename, location_lat, location_lng, area_name,
    landslide_detected, confidence, risk_level, detections_count,
    processing_time_ms, model_version
) VALUES
('kathmandu_satellite_001.jpg', 27.7172, 85.3240, 'Kathmandu Valley',
 true, 0.87, 'high', 2, 156, 'yolo-v8-landslide-v1.0'),
('pokhara_satellite_002.jpg', 28.2096, 83.9856, 'Pokhara Valley',
 false, 0.12, 'low', 0, 143, 'yolo-v8-landslide-v1.0');
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
\i create_image_analyses.sql
\i create_landslide_detections.sql
\i create_alerts.sql
\i create_api_keys.sql
\i create_batch_analyses.sql
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