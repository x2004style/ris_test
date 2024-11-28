SELECT
    patient.p_id, patient.p_birthday, patient.p_passport,
    patient.p_address, patient.p_admission_date, patient.p_room
FROM
    patient
JOIN
    department ON patient.p_department = department.d_id
WHERE
    department.d_id = $d_id;
