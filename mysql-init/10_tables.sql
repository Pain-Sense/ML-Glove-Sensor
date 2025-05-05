USE sql_data;

DROP TABLE IF EXISTS experiments;
DROP TABLE IF EXISTS devices;
DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  age VARCHAR(10),
  gender VARCHAR(10),
  health_condition VARCHAR(255)
);

CREATE TABLE devices (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  type VARCHAR(100),
  status VARCHAR(50)
);

CREATE TABLE experiments (
  id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  notes TEXT,
  patient_id BIGINT,
  device_id BIGINT,
  CONSTRAINT fk_experiment_patient FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
  CONSTRAINT fk_experiment_device FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE SET NULL
);
