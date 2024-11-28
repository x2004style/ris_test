SELECT *
FROM doctor d
WHERE d.doc_department = $department_id
ORDER BY d.doc_surname;