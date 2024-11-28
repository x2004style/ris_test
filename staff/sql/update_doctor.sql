UPDATE doctor
SET doc_surname = %s, doc_passport = %s, doc_address = %s, doc_birthday = %s,
doc_specialization = %s, doc_hire_date = %s, doc_fire_date = %s
WHERE doc_id = %s