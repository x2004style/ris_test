from flask import Blueprint, render_template, request, current_app, redirect, url_for
from database.sql_provider import SQLProvider
from database.select import select_dict
from database.DBcm import DBContextManager
from access import group_required
import os

blueprint_staff = Blueprint('staff_bp', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_staff.route('/departments')
@group_required
def department_list():
    sql = provider.get('departments_list.sql')
    try:
        departments = select_dict(current_app.config['db_config'], sql)
    except Exception:
        return render_template('error.html', error_message="Ошибка при загрузке данных отделений.")
    return render_template('departments_list.html', departments=departments)


@blueprint_staff.route('/departments/<int:department_id>/doctors')
@group_required
def doctors_by_department(department_id):
    sql = provider.get('doctors_by_department.sql', department_id=department_id)
    try:
        doctors = select_dict(current_app.config['db_config'], sql)
    except Exception:
        return render_template('error.html', error_message="Ошибка при загрузке данных о врачах.")
    return render_template('doctors_list.html', doctors=doctors, department_id=department_id)


@blueprint_staff.route('/departments/<int:department_id>/add_doctor', methods=['GET', 'POST'])
@group_required
def add_doctor(department_id):
    if request.method == 'POST':
        try:
            doc_surname = request.form['doc_surname']
            doc_passport = request.form['doc_passport']
            doc_address = request.form['doc_address']
            doc_birthday = request.form['doc_birthday']
            doc_specialization = request.form['doc_specialization']
            doc_hire_date = request.form['doc_hire_date']
            sql = provider.get('insert_doctor.sql')
            with DBContextManager(current_app.config['db_config']) as cursor:
                cursor.execute(sql, (doc_surname, doc_passport, doc_address, doc_birthday,
                                     doc_specialization, doc_hire_date, department_id))
            return redirect(url_for('staff_bp.doctors_by_department', department_id=department_id))
        except Exception:
            return render_template('error.html', error_message="Ошибка при добавлении врача.")
    return render_template('add_doctor.html', department_id=department_id)


@blueprint_staff.route('/departments/<int:department_id>/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
@group_required
def edit_doctor(department_id, doctor_id):
    sql = provider.get('doctor_info.sql', doc_id=doctor_id)
    print(sql)
    try:
        doctors = select_dict(current_app.config['db_config'], sql)
        if not doctors:
            return render_template('error.html', error_message=f"Врач с ID {doctor_id} не найден.")
        doctor = doctors[0]
    except Exception:
        return render_template('error.html', error_message="Ошибка при загрузке данных врача.")

    if request.method == 'POST':
        try:
            doc_surname = request.form['doc_surname']
            doc_passport = request.form['doc_passport']
            doc_address = request.form['doc_address']
            doc_birthday = request.form['doc_birthday']
            doc_specialization = request.form['doc_specialization']
            doc_hire_date = request.form['doc_hire_date']
            doc_fire_date = request.form.get('doc_fire_date')
            sql_update = provider.get('update_doctor.sql')
            with DBContextManager(current_app.config['db_config']) as cursor:
                cursor.execute(sql_update, (doc_surname, doc_passport, doc_address, doc_birthday,
                                            doc_specialization, doc_hire_date, doc_fire_date, doctor_id))
            return redirect(url_for('staff_bp.doctors_by_department', department_id=department_id))
        except Exception:
            return render_template('error.html', error_message="Ошибка при обновлении данных врача.")

    return render_template('edit_doctor.html', doctor=doctor, department_id=department_id)


@blueprint_staff.route('/departments/<int:department_id>/delete_doctor/<int:doctor_id>')
@group_required
def delete_doctor(department_id, doctor_id):
    sql = provider.get('delete_doctor.sql', doc_id=doctor_id)
    try:
        with DBContextManager(current_app.config['db_config']) as cursor:
            cursor.execute(sql)
        return redirect(url_for('staff_bp.doctors_by_department', department_id=department_id))
    except Exception:
        return render_template('error.html', error_message="Ошибка при удалении врача.")
