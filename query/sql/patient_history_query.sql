SELECT mr_id, mr_date, mr_observations, mr_patient_department, mr_doctor
FROM medical_record mr
JOIN disease_history dh ON mr.mr_disease_history = dh.dh_id
WHERE dh.dh_patient = $p_id;
