DROP DATABASE IF EXISTS garmin_api_state_db;

CREATE DATABASE garmin_api_state_db;

USE garmin_api_state_db;

DROP TABLE IF EXISTS state;

CREATE TABLE state (
  id INT AUTO_INCREMENT PRIMARY KEY,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  healthy BOOL
);

INSERT INTO state (healthy) VALUES (1);