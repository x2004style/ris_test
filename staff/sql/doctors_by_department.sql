SELECT *
FROM doctor d
WHERE d.doc_department = $department_id AND d.doc_fire_date IS NULL
ORDER BY d.doc_surname;