USE sql_data;

INSERT INTO patients (name, age, gender, health_condition) VALUES
  ('John Doe', '42', 'male', 'Chronic Pain'),
  ('Jane Smith', '35', 'female', 'Neuropathy');

INSERT INTO devices (name, type, status) VALUES
  ('ECG Sensor #001', 'ECG', 'available'),
  ('ECG Sensor #002', 'ECG', 'in_use'),
  ('ECG Sensor #003', 'ECG', 'maintenance'),
  ('ECG Sensor #004', 'ECG', 'available'),
  ('ECG Sensor #005', 'ECG', 'available'),
  ('ECG Sensor #006', 'ECG', 'available'),
  ('ECG Sensor #007', 'ECG', 'available'),
  ('ECG Sensor #008', 'ECG', 'available'),
  ('ECG Sensor #009', 'ECG', 'available'),
  ('ECG Sensor #010', 'ECG', 'available');
  

INSERT INTO experiments (name, notes, patient_id, device_id) VALUES
  ('Baseline ECG', 'Resting state capture.', 1, 1),
  ('Pain Response Study', 'ECG during stimulus.', 2, 2);