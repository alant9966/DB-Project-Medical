/**
 * Set up database tables (CREATE)
*/

-- Create the User table (for login management)
CREATE TABLE User (
    user_id INT AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(10) NOT NULL,
    PRIMARY KEY (user_id)
);

-- Create the Patient table
CREATE TABLE patient (
    patient_id INT AUTO_INCREMENT,
    user_id INT NULL UNIQUE,
    date_of_birth DATE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    weight_lb INT,
    height_in INT,
    age INT,
    address VARCHAR(100),
    PRIMARY KEY (patient_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Create the BloodTest table
CREATE TABLE bloodtest(
    bloodtest_id INT AUTO_INCREMENT,
    patient_id INT,
    time TIME, 
    result VARCHAR(500), 
    PRIMARY KEY (bloodtest_id),
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id)
);

-- Create the MedicalRecord table
CREATE TABLE medicalrecord (
    medicalrecord_id INT AUTO_INCREMENT,
    patient_id INT,
    diagnosis VARCHAR(500),
    result VARCHAR(500),
    PRIMARY KEY (medicalrecord_id),
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id)
);

-- Create the Insurance table
CREATE TABLE insurance (
    insurance_id INT AUTO_INCREMENT,
    patient_id INT,
    date_of_expiry DATE,
    company VARCHAR(500),
    PRIMARY KEY (insurance_id),
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id)
);

-- Create the Department table
CREATE TABLE department (
    department_id INT AUTO_INCREMENT,
    department_name VARCHAR(100),
    officelocation VARCHAR(150),
    PRIMARY KEY (department_id)
);

-- Create the Doctor table
CREATE TABLE doctor (
    doctor_id INT AUTO_INCREMENT,
    user_id INT NULL UNIQUE,
    department_id INT,
    doctor_firstname VARCHAR(50),
    doctor_lastname VARCHAR(50),
    years_of_experience INT,
    doctor_address VARCHAR(150),
    PRIMARY KEY (doctor_id),
    FOREIGN KEY (department_id) REFERENCES department(department_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Create the Treatment table
CREATE TABLE treatment (
    treatment_name VARCHAR(50),
    duration_days INT,
    description VARCHAR(500),
    bill DECIMAL(19,4),
    PRIMARY KEY (treatment_name, duration_days)
);

-- Create the Prescription table
CREATE TABLE prescription (
    prescription_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    treatment_name VARCHAR(50) NOT NULL,
    duration_days INT NOT NULL,
    prescribed_on DATE NOT NULL,
    notes VARCHAR(255),
    paid BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (treatment_name, duration_days) REFERENCES treatment(treatment_name, duration_days)
);

-- Create the Room table
CREATE TABLE room (
    room_id INT,
    capacity INT,
    floor INT,
    PRIMARY KEY (room_id)
);

-- Create the Appointment table
CREATE TABLE appointment (
    appointment_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    room_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    description VARCHAR(255),
    duration_minutes INT NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id)
);

/**
 * Populate tables (INSERT INTO)
*/

-- Populate the Patient table
INSERT INTO patient (patient_id, date_of_birth, first_name, last_name, weight_lb, height_in, age, address)
VALUES
(1, '2000-10-23', 'Virgil', 'Adkins', 182, 68, 25, '4932 Lighthouse Drive, Springfield, MO 65804'),
(2, '1992-04-11', 'Winston', 'Cannon', 187, 72, 33, '2694 Romines Mill Road, Dallas, TX 75215'),
(3, '1991-12-13', 'Joanna Travis', 'Adkins', 170, 61, 33, '873 Smith Street, Cambridge, MA 02141'),
(4, '2003-07-22', 'Sam', 'Edwards', 168, 65, 22, '3377 Ford Street, Concord, CA 94520'),
(5, '1999-08-03', 'Columbus', 'Carr', 190, 70, 26, '4640 Rainbow Drive, Wooster, OH 44691'),
(6, '1989-07-21', 'Haley', 'Alvarez', 173, 70, 36, '1579 Hudson Street, Lyndhurst, NJ 07071'),
(7, '2012-02-01', 'Noel', 'Mcdonald', 177, 68, 13, '1904 Boggess Street, Wichita Falls, TX 76301'),
(8, '2001-10-05', 'Garland', 'Savage', 175, 74, 24, '4970 Hart Country Lane, Dalton, GA 30720'),
(9, '1992-11-11', 'Claudette', 'Mccormick', 162, 63, 32, '236 Stonepot Road, Rochelle Park, NJ 07662'),
(10, '1993-11-09', 'Shauna', 'Fletcher', 166, 64, 31, '4554 Stratford Drive, Honolulu, HI 96814');

-- Populate the BloodTest table
INSERT INTO bloodtest(bloodtest_id,patient_id,time,result)
VALUE
(1, 1, '08:30:00', 'Normal hemoglobin and glucose levels'),
(2, 2, '09:15:00', 'Slightly elevated cholesterol; HDL within range'),
(3, 3, '10:00:00', 'Low iron level; recommended dietary supplements'),
(4, 4, '11:20:00', 'White blood cell count elevated—possible infection'),
(5, 5, '13:45:00', 'All values within normal range'),
(6, 6, '14:10:00', 'High fasting glucose—monitor for diabetes'),
(7, 7, '15:30:00', 'Mild anemia detected'),
(8, 8, '16:00:00', 'Elevated liver enzymes—further testing recommended'),
(9, 9, '08:10:00', 'Vitamin D deficiency'),
(10, 10, '09:40:00', 'Normal profile; no abnormalities detected');

-- Populate the MedicalRecord table
INSERT INTO medicalrecord (medicalrecord_id, patient_id, diagnosis, result)
VALUES
(1, 1, 'Seasonal allergies', 'Prescribed Loratadine 10 mg daily'),
(2, 2, 'Hypertension', 'Continued Lisinopril 10 mg daily'),
(3, 3, 'Iron deficiency anemia', 'Started on iron supplements and dietary change'),
(4, 4, 'Upper respiratory infection', 'Prescribed Amoxicillin 500 mg for 10 days'),
(5, 5, 'Gastric reflux', 'Prescribed Omeprazole 20 mg once daily'),
(6, 6, 'Type 2 Diabetes', 'Initiated Metformin 500 mg twice daily'),
(7, 7, 'Mild asthma', 'Advised use of Albuterol HFA inhaler as needed'),
(8, 8, 'Hypothyroidism', 'Started Levothyroxine 50 mcg once daily'),
(9, 9, 'High cholesterol', 'Continued Atorvastatin 20 mg nightly'),
(10, 10, 'Sinus infection', 'Prescribed Azithromycin 250 mg course');

-- Populate the Insurance table
INSERT INTO insurance (insurance_id, patient_id, date_of_expiry, company)
VALUES
(1, 1, '2026-03-15', 'Blue Cross Blue Shield'),
(2, 2, '2025-12-31', 'UnitedHealthcare'),
(3, 3, '2027-01-01', 'Cigna Health'),
(4, 4, '2026-05-30', 'Aetna'),
(5, 5, '2025-09-20', 'Humana'),
(6, 6, '2026-07-10', 'Kaiser Permanente'),
(7, 7, '2027-02-18', 'Anthem Health'),
(8, 8, '2026-11-01', 'CVS Health'),
(9, 9, '2025-08-25', 'MetLife Health'),
(10, 10, '2026-12-12', 'Guardian Insurance');

-- Populate the Department table
INSERT INTO department (department_id, department_name, officelocation)
VALUES
(1, 'Emergency Medicine', 'Main Building - Ground Floor'),
(2, 'Cardiology', 'Building A - Room 201'),
(3, 'Neurology', 'Building B - Room 305'),
(4, 'Oncology', 'Building C - Room 410'),
(5, 'Pediatrics', 'Building D - Room 102'),
(6, 'Orthopedics', 'Building E - Room 220'),
(7, 'Radiology', 'Building F - Room 330'),
(8, 'Obstetrics and Gynecology', 'Building G - Room 115'),
(9, 'Anesthesiology', 'Building H - Room 250'),
(10, 'General Surgery', 'Building I - Room 340');

-- Populate the Doctor table
INSERT INTO doctor (doctor_id, department_id, doctor_firstname, doctor_lastname, years_of_experience, doctor_address)
VALUES
(1, 1, 'William', 'Johnson', 10, '4932 Lighthouse Drive, Springfield, MO 65804'),
(2, 2, 'Emily', 'Clark', 14, '2187 Maplewood Avenue, Austin, TX 73301'),
(3, 3, 'Daniel', 'Martinez', 9, '640 Pinecrest Road, Columbus, OH 43215'),
(4, 4, 'Sophia', 'Nguyen', 11, '327 Birchwood Lane, Seattle, WA 98101'),
(5, 5, 'Michael', 'Patel', 6, '142 Cedar Grove Drive, Orlando, FL 32801'),
(6, 6, 'Olivia', 'Brown', 8, '781 Elm Street, Denver, CO 80203'),
(7, 7, 'James', 'Chen', 13, '950 Willow Creek Road, Madison, WI 53703'),
(8, 8, 'Ava', 'Lopez', 7, '1120 Aspen Ridge Boulevard, Phoenix, AZ 85004'),
(9, 9, 'Ethan', 'Singh', 15, '475 Redwood Avenue, San Diego, CA 92103'),
(10, 10, 'Mia', 'Davis', 5, '623 Spruce Court, Nashville, TN 37201'),
(11, 1, 'Benjamin', 'Scott', 12, '350 Pine Hill Road, Raleigh, NC 27601'),
(12, 2, 'Grace', 'Lee', 17, '810 Forest Drive, Boston, MA 02108'),
(13, 3, 'Alexander', 'White', 4, '290 Riverbend Street, Atlanta, GA 30303'),
(14, 4, 'Natalie', 'Garcia', 9, '422 Maple Hollow Lane, Portland, OR 97205'),
(15, 5, 'Lucas', 'Miller', 20, '155 Cherry Blossom Road, Chicago, IL 60601');

-- Populate the Treatment table
INSERT INTO treatment (treatment_name, duration_days, description, bill)
VALUES
('Amoxicillin 500 mg', 10, '1 capsule by mouth, three times daily', 10.00),
('Lisinopril 10 mg 500 mg', 90, '1 tablet by mouth, once daily', 10.00),
('Atorvastatin 20 mg', 180, '1 tablet by mouth, once daily in the evening', 15.00),
('Metformin 500 mg', 180, '1 tablet by mouth, twice daily', 10.00),
('Albuterol HFA 90 mcg/actuation', 7, 'Inhale 2 puffs by mouth, every 4-6 hours as needed', 25.00),
('Levothyroxine 50 mcg', 150, '1 tablet by mouth, once daily at least an hour before eating', 10.00),
('Omeprazole 20 mg', 30, '1 capsule by mouth, once daily in the morning', 10.00),
('Ibuprofen 800 mg', 20, '1 tablet by mouth, every 8 hours as needed for pain', 10.00),
('Loratadine 10 mg', 30, '1 tablet by mouth, once daily as needed for allergy symptoms', 10.00),
('Azithromycin 250 mg', 6, '2 tablets by mouth on day 1, 1 tablet by mouth daily on days 2-5', 10.00);

-- Populate the Prescription table
INSERT INTO prescription (patient_id, treatment_name, duration_days, prescribed_on, notes)
VALUES
(1, 'Amoxicillin 500 mg', 10, '2025-11-03', 'Sinus infection'),
(2, 'Ibuprofen 800 mg', 20, '2025-11-03', 'Pain management'),
(3, 'Atorvastatin 20 mg', 180, '2025-11-04', 'Cholesterol control'),
(4, 'Loratadine 10 mg', 30, '2025-11-05', 'Allergy relief'),
(5, 'Metformin 500 mg', 180, '2025-11-05', 'Diabetes treatment'),
(6, 'Omeprazole 20 mg', 30, '2025-11-06', 'Acid reflux'),
(7, 'Albuterol HFA 90 mcg/actuation', 7, '2025-11-06', 'Asthma management'),
(8, 'Levothyroxine 50 mcg', 150, '2025-11-07', 'Thyroid disorder'),
(9, 'Azithromycin 250 mg', 6, '2025-11-08', 'Respiratory infection'),
(10, 'Lisinopril 10 mg 500 mg', 90, '2025-11-08', 'Blood pressure control');

-- Populate the Room table
INSERT INTO room (room_id, capacity, floor)
VALUES
(101, 4, 1),
(102, 4, 1),
(103, 3, 1),
(104, 3, 1),
(105, 5, 1),
(201, 3, 2),
(202, 3, 2),
(203, 4, 2),
(204, 4, 2),
(205, 5, 2),
(301, 8, 3),
(302, 10, 3),
(303, 10, 3),
(304, 12, 3),
(305, 8, 3);

-- Populate the Appointment table
INSERT INTO appointment (appointment_id, patient_id, doctor_id, room_id, appointment_date, appointment_time, description, duration_minutes)
VALUES
(1, 1, 2, 201, '2025-11-03', '09:00:00', 'Cardiology consult', 30),
(2, 2, 1, 101, '2025-11-03', '10:15:00', 'ER follow-up', 20),
(3, 3, 3, 305, '2025-11-04', '14:00:00', 'Neurology evaluation', 45),
(4, 4, 5, 105, '2025-11-05', '11:30:00', 'Pediatrics visit', 25),
(5, 5, 4, 305, '2025-11-05', '15:00:00', 'Oncology check', 40),
(6, 6, 6, 202, '2025-11-06', '13:00:00', 'Orthopedics consult', 30),
(7, 7, 7, 303, '2025-11-06', '09:45:00', 'Radiology reading', 15),
(8, 8, 8, 105, '2025-11-07', '16:00:00', 'OB/GYN routine exam', 30),
(9, 9, 9, 205, '2025-11-08', '08:30:00', 'Anesthesiology pre–op', 35),
(10, 10, 10, 304, '2025-11-08', '10:00:00', 'General surgery follow–up', 25);