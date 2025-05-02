-- Drop existing tables if they exist
DROP TABLE IF EXISTS experiment;
DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS patient;

-- Patient Table
CREATE TABLE patient (
  id CHAR(36) NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  age VARCHAR(10),
  gender VARCHAR(10),
  condition VARCHAR(255)
);

-- Device Table
CREATE TABLE device (
  id CHAR(36) NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  type VARCHAR(100),
  status VARCHAR(50)
);

-- Experiment Table
CREATE TABLE experiment (
  id CHAR(36) NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  notes TEXT,
  patient_id CHAR(36),
  device_id CHAR(36),
  CONSTRAINT fk_experiment_patient FOREIGN KEY (patient_id) REFERENCES patient(id) ON DELETE CASCADE,
  CONSTRAINT fk_experiment_device FOREIGN KEY (device_id) REFERENCES device(id) ON DELETE SET NULL
);

-- Patients
INSERT INTO patient (id, name, age, gender, condition) VALUES
  ('11111111-1111-1111-1111-111111111111', 'John Doe', '42', 'male', 'Chronic Pain'),
  ('22222222-2222-2222-2222-222222222222', 'Jane Smith', '35', 'female', 'Neuropathy');

-- Devices
INSERT INTO device (id, name, type, status) VALUES
  ('aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'ECG Sensor #001', 'ECG', 'available'),
  ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'ECG Sensor #002', 'ECG', 'in_use');
    ('aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'ECG Sensor #003', 'ECG', 'maintenance'),;

-- Experiments
INSERT INTO experiment (id, name, notes, patient_id, device_id) VALUES
  ('eeeeeee1-eeee-eeee-eeee-eeeeeeeeeeee', 'Baseline ECG', 'Resting state capture.', '11111111-1111-1111-1111-111111111111', 'aaaaaaa1-aaaa-aaaa-aaaa-aaaaaaaaaaaa'),
  ('eeeeeee2-eeee-eeee-eeee-eeeeeeeeeeee', 'Pain Response Study', 'ECG during stimulus.', '22222222-2222-2222-2222-222222222222', 'aaaaaaa2-aaaa-aaaa-aaaa-aaaaaaaaaaaa');
