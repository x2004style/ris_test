from flask import render_template, Blueprint, request, current_app
from database.sql_provider import SQLProvider
import os
from .model_route import model_route
from access import group_required

blueprint_query = Blueprint('query_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_query.route('/')
@group_required
def query_menu():
    queries = [
        {'id': 1, 'name': 'Сведения о врачах, которые не назначались лечащими врачами'},
        {'id': 2, 'name': 'Записи в истории болезни пациента'},
        {'id': 3, 'name': 'Сведения о текущих пациентах'}
    ]
    return render_template('query_menu.html', queries=queries)



@blueprint_query.route('/<int:query_id>', methods=['GET'])
@group_required
def query_handler(query_id):
    if query_id == 1:
        return render_template('input_doctor.html')
    elif query_id == 2:
        return render_template('input_patient_history.html')
    elif query_id == 3:
        return render_template('input_patient.html')


@blueprint_query.route('/<int:query_id>', methods=['POST'])
@group_required
def query_result_handler(query_id):
    user_data = request.form
    print('user_data = ', user_data)
    res_info = model_route(current_app.config['db_config'], user_data, provider, query_id)
    if res_info.status and res_info.result != ():
        print('res_info.result=', res_info.result)
        prod_title = 'Результаты из БД'
        if query_id == 1:
            return render_template('dynamic1.html', prod_title=prod_title, doctors=res_info.result)
        if query_id == 2:
            return render_template('dynamic2.html', prod_title=prod_title, history=res_info.result)
        if query_id == 3:
            return render_template('dynamic3.html', prod_title=prod_title, patients=res_info.result)
    elif res_info.error_message == 'type_error':
        return render_template('query_error.html', query_id=query_id)
    else:
        return render_template('query_blank.html', query_id=query_id)
