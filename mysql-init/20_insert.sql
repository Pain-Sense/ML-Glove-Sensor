USE sql_data;
-- Insert patients
INSERT INTO patient (name, age, gender) VALUES
('Alice Smith', 30, 'Female'),
('Bob Johnson', 40, 'Male'),
('Alice Johnson', 20, 'Female');

-- Insert 5 experiments, linked to these patients
INSERT INTO experiment (patient_id, name, description, start_date, end_date) VALUES
(1, 'Stress Test', 'Measuring response to stress', '2025-04-01', '2025-04-30'),
(2, 'Sleep Study', 'Monitoring sleep patterns', '2025-05-01', '2025-05-15'),
(2, 'Cardio Response', 'Cardiac monitoring during activity', '2025-06-01', '2025-06-15'),
(1, 'Biofeedback', 'Tracking physiological signals for training', '2025-07-01', '2025-07-10'),
(3, 'NeuroSensor', 'Brain activity signal collection', '2025-08-01', '2025-08-20');