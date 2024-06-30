-- init.sql
CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    pressure REAL NOT NULL,
    air_quality REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
