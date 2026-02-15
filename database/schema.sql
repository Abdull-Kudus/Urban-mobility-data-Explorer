-- Urban Mobility Data Explorer — MySQL Schema

CREATE DATABASE IF NOT EXISTS urban_mobility;
USE urban_mobility;

CREATE TABLE IF NOT EXISTS boroughs (
    borough_id   INT          NOT NULL AUTO_INCREMENT,
    borough_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (borough_id),
    UNIQUE KEY uq_borough_name (borough_name)
);

CREATE TABLE IF NOT EXISTS service_zones (
    zone_type_id INT         NOT NULL AUTO_INCREMENT,
    zone_type    VARCHAR(50) NOT NULL,
    PRIMARY KEY (zone_type_id),
    UNIQUE KEY uq_zone_type (zone_type)
);

CREATE TABLE IF NOT EXISTS taxi_zones (
    location_id  INT          NOT NULL,
    zone_name    VARCHAR(200) NOT NULL,
    borough_id   INT          NOT NULL,
    zone_type_id INT          NOT NULL,
    PRIMARY KEY (location_id),
    CONSTRAINT fk_zone_borough
        FOREIGN KEY (borough_id)   REFERENCES boroughs(borough_id),
    CONSTRAINT fk_zone_type
        FOREIGN KEY (zone_type_id) REFERENCES service_zones(zone_type_id)
);

CREATE TABLE IF NOT EXISTS rate_codes (
    ratecode_id          INT         NOT NULL,
    ratecode_description VARCHAR(100) NOT NULL,
    PRIMARY KEY (ratecode_id)
);

CREATE TABLE IF NOT EXISTS vendors (
    vendor_id   INT         NOT NULL,
    vendor_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (vendor_id)
);

CREATE TABLE IF NOT EXISTS payment_types (
    payment_type_id   INT         NOT NULL,
    payment_type_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (payment_type_id)
);

CREATE TABLE IF NOT EXISTS trips (
    trip_id              BIGINT         NOT NULL AUTO_INCREMENT,

    vendor_id            INT            NOT NULL,
    ratecode_id          INT            NOT NULL,
    payment_type_id      INT            NOT NULL,

    pickup_location_id   INT            NOT NULL,
    dropoff_location_id  INT            NOT NULL,

    pickup_datetime      DATETIME       NOT NULL,
    dropoff_datetime     DATETIME       NOT NULL,

    passenger_count      TINYINT        NOT NULL DEFAULT 1,
    trip_distance        DECIMAL(8, 2)  NOT NULL DEFAULT 0.00,
    store_and_fwd_flag   CHAR(1)        NOT NULL DEFAULT 'N',

    fare_amount          DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    extra                DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    mta_tax              DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    tip_amount           DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    tolls_amount         DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    improvement_surcharge DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    congestion_surcharge DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    total_amount         DECIMAL(10, 2) NOT NULL DEFAULT 0.00,

    trip_duration_minutes DECIMAL(8, 2)  DEFAULT NULL,
    fare_per_mile        DECIMAL(10, 4)  DEFAULT NULL,
    pickup_hour          TINYINT         DEFAULT NULL,
    is_weekend           TINYINT(1)      DEFAULT NULL,
    avg_speed_mph        DECIMAL(10, 4)  DEFAULT NULL,

    PRIMARY KEY (trip_id),

    -- Foreign key constraints
    CONSTRAINT fk_trip_vendor
        FOREIGN KEY (vendor_id)          REFERENCES vendors(vendor_id),
    CONSTRAINT fk_trip_ratecode
        FOREIGN KEY (ratecode_id)        REFERENCES rate_codes(ratecode_id),
    CONSTRAINT fk_trip_payment
        FOREIGN KEY (payment_type_id)    REFERENCES payment_types(payment_type_id),
    CONSTRAINT fk_trip_pickup_zone
        FOREIGN KEY (pickup_location_id) REFERENCES taxi_zones(location_id),
    CONSTRAINT fk_trip_dropoff_zone
        FOREIGN KEY (dropoff_location_id) REFERENCES taxi_zones(location_id)
);

-- INDEXES
CREATE INDEX idx_trips_pickup_datetime  ON trips (pickup_datetime);
CREATE INDEX idx_trips_dropoff_datetime ON trips (dropoff_datetime);
CREATE INDEX idx_trips_pickup_hour      ON trips (pickup_hour);

CREATE INDEX idx_trips_pickup_location  ON trips (pickup_location_id);
CREATE INDEX idx_trips_dropoff_location ON trips (dropoff_location_id);

CREATE INDEX idx_trips_fare_amount      ON trips (fare_amount);
CREATE INDEX idx_trips_trip_distance    ON trips (trip_distance);

CREATE INDEX idx_trips_zone_hour        ON trips (pickup_location_id, pickup_hour);
CREATE INDEX idx_trips_is_weekend       ON trips (is_weekend);