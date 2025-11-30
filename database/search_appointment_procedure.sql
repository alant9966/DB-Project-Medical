DELIMITER $$

DROP PROCEDURE IF EXISTS search_appointment$$

CREATE PROCEDURE search_appointment(
    IN p_patient_id INT,
    IN p_start_date DATE,
    IN p_end_date DATE,
    IN p_query VARCHAR(100)
)
BEGIN
    SELECT a.appointment_id,
           CONCAT(d.doctor_firstname, ' ', d.doctor_lastname) AS doctor_name,
           a.room_id,
           a.appointment_date,
           a.appointment_time,
           a.duration_minutes,
           a.description,
           d.doctor_firstname,
           d.doctor_lastname
    FROM appointment a 
    INNER JOIN doctor d ON a.doctor_id = d.doctor_id 
    WHERE a.patient_id = p_patient_id
        AND a.appointment_date >= p_start_date
        AND a.appointment_date <= p_end_date
        AND (
            CONCAT(d.doctor_firstname, ' ', d.doctor_lastname) LIKE CONCAT('%', p_query, '%')
            OR CAST(a.room_id AS CHAR) LIKE CONCAT('%', p_query, '%')
            OR CAST(a.appointment_date AS CHAR) LIKE CONCAT('%', p_query, '%')
            OR CAST(a.appointment_time AS CHAR) LIKE CONCAT('%', p_query, '%')
            OR CAST(a.duration_minutes AS CHAR) LIKE CONCAT('%', p_query, '%')
            OR a.description LIKE CONCAT('%', p_query, '%')
        )
    ORDER BY a.appointment_date ASC, a.appointment_time ASC;
END$$

DELIMITER ;
