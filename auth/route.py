from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from database.select import select_dict
from database.sql_provider import SQLProvider
import os

blueprint_auth = Blueprint('auth_bp', __name__, template_folder='templates')

sql_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/')
def auth_index():
    return render_template('login.html')


@blueprint_auth.route('/login', methods=['POST'])
def auth_login():
    login = request.form.get('login')
    password = request.form.get('password')
    _sql = sql_provider.get('check_user.sql', login=login, password=password)
    result = select_dict(current_app.config['db_config'], _sql)
    if result:
        user_group = result[0]['user_group']  # Извлекаем 'user_group' из результата
        session['user_group'] = user_group
        session['user_login'] = login
        return redirect(url_for('main_menu'))
    else:
        return render_template('login_error.html')
