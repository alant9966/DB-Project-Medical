-- Security setup for AWS RDS database

-- Create the application user (for Flask app connections)
-- Can read/write data but cannot modify schema
CREATE USER IF NOT EXISTS 'medical_app_user'@'%'
IDENTIFIED BY 'aws.cs3083!user';

-- Create a read-only reporting user (for analytics/reports)
-- Can only SELECT data (no modifications)
CREATE USER IF NOT EXISTS 'medical_readonly_user'@'%'
IDENTIFIED BY 'aws.cs3083!readonly';

-- Create a backup user (for database backups)
-- Can only read data
CREATE USER IF NOT EXISTS 'medical_backup_user'@'%'
IDENTIFIED BY 'aws.cs3083!backup';


-- Grant SELECT permission (read data)
GRANT SELECT ON medical_db.User TO 'medical_app_user'@'%';
GRANT SELECT ON medical_db.patient TO 'medical_app_user'@'%';
GRANT SELECT ON medical_db.doctor TO 'medical_app_user'@'%';
GRANT SELECT ON medical_db.department TO 'medical_app_user'@'%';
GRANT SELECT ON medical_db.appointment TO 'medical_app_user'@'%';
GRANT SELECT ON medical_db.treatment TO 'medical_app_user'@'%';
GRANT SELECT ON medical_db.prescription TO 'medical_app_user'@'%';
GRANT SELECT ON medical_db.bloodtest TO 'medical_app_user'@'%';
GRANT SELECT ON medical_db.medicalrecord TO 'medical_app_user'@'%';
GRANT SELECT ON medical_db.insurance TO 'medical_app_user'@'%';
GRANT SELECT ON medical_db.room TO 'medical_app_user'@'%';

-- Grant INSERT permission (create new records)
-- Users need to register, create appointments, etc.
GRANT INSERT ON medical_db.User TO 'medical_app_user'@'%';
GRANT INSERT ON medical_db.patient TO 'medical_app_user'@'%';
GRANT INSERT ON medical_db.doctor TO 'medical_app_user'@'%';
GRANT INSERT ON medical_db.appointment TO 'medical_app_user'@'%';
GRANT INSERT ON medical_db.prescription TO 'medical_app_user'@'%';
GRANT INSERT ON medical_db.insurance TO 'medical_app_user'@'%';
GRANT INSERT ON medical_db.medicalrecord TO 'medical_app_user'@'%';

-- Grant UPDATE permission (modify existing records)
-- Patients/doctors can update their profiles and modify appointments
GRANT UPDATE ON medical_db.User TO 'medical_app_user'@'%';
GRANT UPDATE ON medical_db.patient TO 'medical_app_user'@'%';
GRANT UPDATE ON medical_db.doctor TO 'medical_app_user'@'%';
GRANT UPDATE ON medical_db.appointment TO 'medical_app_user'@'%';
GRANT UPDATE ON medical_db.insurance TO 'medical_app_user'@'%';
GRANT UPDATE ON medical_db.medicalrecord TO 'medical_app_user'@'%';
GRANT UPDATE ON medical_db.prescription TO 'medical_app_user'@'%';

-- Grant DELETE permission (remove records)
-- Allows deletion of appointments and user accounts
GRANT DELETE ON medical_db.appointment TO 'medical_app_user'@'%';
GRANT DELETE ON medical_db.User TO 'medical_app_user'@'%';

-- Grant EXECUTE permission (call stored procedures)
GRANT EXECUTE ON PROCEDURE medical_db.search_appointment TO 'medical_app_user'@'%';
GRANT EXECUTE ON PROCEDURE medical_db.get_patient_appointments_by_date TO 'medical_app_user'@'%';


-- Read-only user can only read data (for reports and analytics)
GRANT SELECT ON medical_db.* TO 'medical_readonly_user'@'%';

-- Backup user needs SELECT, SHOW VIEW, LOCK TABLES
GRANT SELECT, SHOW VIEW, LOCK TABLES ON medical_db.* TO 'medical_backup_user'@'%';

-- Reload privilege tables to apply changes
FLUSH PRIVILEGES;

