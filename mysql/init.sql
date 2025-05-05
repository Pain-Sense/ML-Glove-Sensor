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

INSERT INTO patients (name, age, gender, health_condition) VALUES
  ('John Doe', '42', 'male', 'Chronic Pain'),
  ('Jane Smith', '35', 'female', 'Neuropathy');

INSERT INTO devices (name, type, status) VALUES
  ('ECG Sensor #001', 'ECG', 'available'),
  ('ECG Sensor #002', 'ECG', 'available'),
  ('ECG Sensor #003', 'ECG', 'available'),
  ('ECG Sensor #004', 'ECG', 'available'),
  ('ECG Sensor #005', 'ECG', 'available'),
  ('ECG Sensor #006', 'ECG', 'available'),
  ('ECG Sensor #007', 'ECG', 'available'),
  ('ECG Sensor #008', 'ECG', 'available'),
  ('ECG Sensor #009', 'ECG', 'available'),
  ('ECG Sensor #010', 'ECG', 'available');
  