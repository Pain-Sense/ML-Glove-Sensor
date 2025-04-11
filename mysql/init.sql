CREATE DATABASE IF NOT EXISTS sql_data;
USE sql_data;

CREATE TABLE patient (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  age INT,
  gender VARCHAR(10)
);

CREATE TABLE experiment (
  id INT AUTO_INCREMENT PRIMARY KEY,
  patient_id INT,
  name VARCHAR(100),
  description TEXT,
  start_date DATE,
  end_date DATE,
  FOREIGN KEY (patient_id) REFERENCES patient(id)
);

-- Insert patients
INSERT INTO patient (name, age, gender) VALUES
('Alice Smith', 30, 'Female'),
('Bob Johnson', 40, 'Male'),
('Alice Johnson', 20, 'Female');

-- Insert experiments
INSERT INTO experiment (patient_id, name, description, start_date, end_date) VALUES
(1, 'Stress Test', 'Measuring response to stress', '2025-04-01', '2025-04-30'),
(2, 'Sleep Study', 'Monitoring sleep patterns', '2025-05-01', '2025-05-15'),
(2, 'Cardio Response', 'Cardiac monitoring during activity', '2025-06-01', '2025-06-15'),
(1, 'Biofeedback', 'Tracking physiological signals for training', '2025-07-01', '2025-07-10'),
(3, 'NeuroSensor', 'Brain activity signal collection', '2025-08-01', '2025-08-20');
