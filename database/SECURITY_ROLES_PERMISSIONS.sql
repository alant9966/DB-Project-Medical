CREATE USER IF NOT EXISTS 'medical_app_user'@'localhost'
IDENTIFIED BY 'aws.cs3083!user';

-- Create a read-only reporting user (for analytics/reports)
-- Can only SELECT data (no modifications)
CREATE USER IF NOT EXISTS 'medical_readonly_user'@'localhost'
IDENTIFIED BY 'aws.cs3083!readonly';

-- Create a backup user (for database backups)
-- Can only read data
CREATE USER IF NOT EXISTS 'medical_backup_user'@'localhost'
IDENTIFIED BY 'aws.cs3083!backup';


-- Grant SELECT permission (read data)
GRANT SELECT ON medical_db.User TO 'medical_app_user'@'localhost';
GRANT SELECT ON medical_db.patient TO 'medical_app_user'@'localhost';
GRANT SELECT ON medical_db.doctor TO 'medical_app_user'@'localhost';
GRANT SELECT ON medical_db.department TO 'medical_app_user'@'localhost';
GRANT SELECT ON medical_db.appointment TO 'medical_app_user'@'localhost';
GRANT SELECT ON medical_db.treatment TO 'medical_app_user'@'localhost';
GRANT SELECT ON medical_db.prescription TO 'medical_app_user'@'localhost';
GRANT SELECT ON medical_db.bloodtest TO 'medical_app_user'@'localhost';
GRANT SELECT ON medical_db.medicalrecord TO 'medical_app_user'@'localhost';
GRANT SELECT ON medical_db.insurance TO 'medical_app_user'@'localhost';
GRANT SELECT ON medical_db.room TO 'medical_app_user'@'localhost';

-- Grant INSERT permission (create new records)
-- Users need to register, create appointments, etc.
GRANT INSERT ON medical_db.User TO 'medical_app_user'@'localhost';
GRANT INSERT ON medical_db.patient TO 'medical_app_user'@'localhost';
GRANT INSERT ON medical_db.doctor TO 'medical_app_user'@'localhost';
GRANT INSERT ON medical_db.appointment TO 'medical_app_user'@'localhost';
GRANT INSERT ON medical_db.prescription TO 'medical_app_user'@'localhost';
GRANT INSERT ON medical_db.insurance TO 'medical_app_user'@'localhost';

-- Grant UPDATE permission (modify existing records)
-- Patients/doctors can update their profiles and modify appointments
GRANT UPDATE ON medical_db.User TO 'medical_app_user'@'localhost';
GRANT UPDATE ON medical_db.patient TO 'medical_app_user'@'localhost';
GRANT UPDATE ON medical_db.doctor TO 'medical_app_user'@'localhost';
GRANT UPDATE ON medical_db.appointment TO 'medical_app_user'@'localhost';
GRANT UPDATE ON medical_db.insurance TO 'medical_app_user'@'localhost';
GRANT UPDATE ON medical_db.medicalrecord TO 'medical_app_user'@'localhost';
GRANT UPDATE ON medical_db.prescription TO 'medical_app_user'@'localhost';

-- Grant DELETE permission (remove records)
-- Allows deletion of appointments and user accounts
GRANT DELETE ON medical_db.appointment TO 'medical_app_user'@'localhost';
GRANT DELETE ON medical_db.User TO 'medical_app_user'@'localhost';

-- Grant EXECUTE permission (call stored procedures)
GRANT EXECUTE ON PROCEDURE medical_db.search_appointment TO 'medical_app_user'@'localhost';
GRANT EXECUTE ON PROCEDURE medical_db.get_patient_appointments_by_date TO 'medical_app_user'@'localhost';


-- Read-only user can only read data (for reports and analytics)
GRANT SELECT ON medical_db.* TO 'medical_readonly_user'@'localhost';

-- Backup user needs SELECT, SHOW VIEW, LOCK TABLES, and RELOAD
GRANT SELECT, SHOW VIEW, LOCK TABLES ON medical_db.* TO 'medical_backup_user'@'localhost';
GRANT RELOAD ON *.* TO 'medical_backup_user'@'localhost';

-- Reload privilege tables to apply changes
FLUSH PRIVILEGES;