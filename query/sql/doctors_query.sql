SELECT p_doctor, doc_surname, COUNT(*) as pat_count
                FROM patient JOIN department ON patient.p_department = department.d_id
                JOIN doctor ON patient.p_doctor = doctor.doc_id
                WHERE d_name = $d_name AND YEAR(p_admission_date) = $p_admission_date
                GROUP BY p_doctor