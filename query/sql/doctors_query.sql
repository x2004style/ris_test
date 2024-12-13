SELECT doc_id, doc_surname, doc_specialization, doc_department
FROM doctor
LEFT JOIN patient
ON doctor.doc_id = patient.p_doctor
   AND YEAR(patient.p_admission_date) = $year
   AND MONTH(patient.p_admission_date) = $month
WHERE patient.p_id IS NULL AND doc_fire_date IS NULL;