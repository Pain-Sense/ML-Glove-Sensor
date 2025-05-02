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