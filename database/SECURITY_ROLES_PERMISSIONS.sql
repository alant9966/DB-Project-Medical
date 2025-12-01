CREATE USER IF NOT EXISTS 'medical_app_user'@'localhost'
IDENTIFIED BY 'secure_app_password_2024';

-- Create a read-only reporting user (for analytics/reports)
-- This user can only SELECT data, no modifications
CREATE USER IF NOT EXISTS 'medical_readonly_user'@'localhost'
IDENTIFIED BY 'readonly_password_2024';

-- Create a backup user (for database backups)
-- This user can only read data for backup purposes
CREATE USER IF NOT EXISTS 'medical_backup_user'@'localhost'
IDENTIFIED BY 'backup_password_2024';


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
-- Patients/doctors can update their profiles, appointments can be modified
GRANT UPDATE ON medical_db.User TO 'medical_app_user'@'localhost';
GRANT UPDATE ON medical_db.patient TO 'medical_app_user'@'localhost';
GRANT UPDATE ON medical_db.doctor TO 'medical_app_user'@'localhost';
GRANT UPDATE ON medical_db.appointment TO 'medical_app_user'@'localhost';
GRANT UPDATE ON medical_db.insurance TO 'medical_app_user'@'localhost';
GRANT UPDATE ON medical_db.medicalrecord TO 'medical_app_user'@'localhost';

-- Grant DELETE permission (remove records)
-- Allows deletion of appointments and user accounts (CASCADE handles related records)
GRANT DELETE ON medical_db.appointment TO 'medical_app_user'@'localhost';
GRANT DELETE ON medical_db.User TO 'medical_app_user'@'localhost';


-- This user can ONLY read data (for reports, analytics)
-- NO INSERT, UPDATE, or DELETE permissions
GRANT SELECT ON medical_db.* TO 'medical_readonly_user'@'localhost';

-- Backup user needs SELECT, SHOW VIEW, LOCK TABLES, and RELOAD
GRANT SELECT, SHOW VIEW, LOCK TABLES ON medical_db.* TO 'medical_backup_user'@'localhost';
GRANT RELOAD ON *.* TO 'medical_backup_user'@'localhost';

-- Reload privilege tables to apply changes
FLUSH PRIVILEGES;