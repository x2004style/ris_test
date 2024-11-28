SELECT d_id, d_name, d_head_surname, SUM(r_bed_count)
                FROM department JOIN room ON department.d_id = room.r_department
                WHERE d_id = $d_id
                GROUP BY d_id, d_name, d_head_surname