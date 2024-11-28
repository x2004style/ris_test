import json
from flask import Flask, render_template, session
from query.route import blueprint_query
from auth.route import blueprint_auth
from report.route import blueprint_report
from staff.route import blueprint_staff

app = Flask(__name__)
with open('data/db_config_hospital.json') as f:
    app.config['db_config'] = json.load(f)
with open('data/db_access_hospital.json') as f:
    app.config['db_access'] = json.load(f)

app.secret_key = 'You will never guess'

app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_staff, url_prefix='/staff')

@app.route('/')
def main_menu():
    if 'user_group' in session:
        user_role = session.get('user_group')
        message = f'Вы авторизованы как {user_role}'
    else:
        message = 'Вам необходимо авторизоваться'
    return render_template('main_menu.html', message=message)

@app.route('/exit')
def exit_func():
    session.clear()
    return render_template('exit.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
