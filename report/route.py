from flask import Blueprint, render_template, request, current_app
from database.select import call_proc, select_dict
from course_work.auth.access import group_required

blueprint_report = Blueprint('report_bp', __name__, template_folder='templates')

report_list = [
    {'rep_id': '1', 'proc_name': 'doctor_report'},
    {'rep_id': '2', 'proc_name': 'discharge_report'}
]


@blueprint_report.route('/', methods=['GET'])
@group_required
def report_menu():
    return render_template('report_menu.html')


@blueprint_report.route('/create', methods=['GET', 'POST'])
@group_required
def create_report():
    if request.method == 'POST':
        report_choice = request.form.get('report_choice')
        month_choice = request.form.get('month_choice')
        year_choice = request.form.get('year_choice')
        proc_name = ''
        for report in report_list:
            if report['rep_id'] == report_choice:
                proc_name = report['proc_name']
                break
        res = call_proc(current_app.config['db_config'], proc_name, month_choice, year_choice)
        error_code = res[0][0]
        if error_code == 1:
            return render_template('report_already_exists.html')
        if error_code == 2:
            return render_template('report_error.html')
        return render_template('report_success.html', report_choice=proc_name, month_choice=month_choice, year_choice=year_choice)
    return render_template('create_report.html')


@blueprint_report.route('/view', methods=['GET', 'POST'])
@group_required
def view_report():
    if request.method == 'POST':
        report_choice = request.form.get('report_choice')
        month_choice = request.form.get('month_choice')
        year_choice = request.form.get('year_choice')
        proc_name = ''
        for report in report_list:
            if report['rep_id'] == report_choice:
                proc_name = report['proc_name']
                break
        _sql = f"SELECT * FROM {proc_name} WHERE r_month = {month_choice} AND r_year = {year_choice}"
        report_data = select_dict(current_app.config['db_config'], _sql)
        if report_data:
            if report_choice == '1':
                result_message = f"Отчет о работе врачей за период {month_choice}-{year_choice}"
                return render_template('doctor_report_results.html', doctors=report_data, result_message=result_message)
            if report_choice == '2':
                result_message = f"Отчет о работе отделений за период {month_choice}-{year_choice}"
                return render_template('discharge_report_results.html', departments=report_data, result_message=result_message)
        result_message = "Отчет за указанный период не найден."
        return render_template('no_report_found.html', result_message=result_message)
    return render_template('view_report.html')
