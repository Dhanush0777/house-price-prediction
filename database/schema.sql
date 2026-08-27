-- =======================================================
-- AI-Based House Price Prediction System
-- Database Schema Definition (MySQL 8.0+)
-- =======================================================

-- 1. Create Database if it does not exist
CREATE DATABASE IF NOT EXISTS house_price_prediction
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 2. Switch to Database
USE house_price_prediction;

-- 3. Create Predictions Table
CREATE TABLE IF NOT EXISTS predictions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    area DOUBLE NOT NULL,
    bedrooms INT NOT NULL,
    bathrooms INT NOT NULL,
    parking INT NOT NULL DEFAULT 0,
    property_age INT NOT NULL DEFAULT 0,
    floors INT NOT NULL DEFAULT 1,
    predicted_price DOUBLE NOT NULL,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_location (location),
    INDEX idx_prediction_date (prediction_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Sample Verification Record
INSERT INTO predictions (location, area, bedrooms, bathrooms, parking, property_age, floors, predicted_price, prediction_date)
VALUES ('Madhurawada', 1500.0, 3, 2, 1, 5, 2, 7344527.85, NOW());

-- 5. Query Verification
SELECT * FROM predictions ORDER BY prediction_date DESC;
