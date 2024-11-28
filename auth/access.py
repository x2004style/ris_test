from flask import session, redirect, url_for, request, current_app, render_template
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('main_menu'))
    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            user_role = session.get('user_group')
            user_request = request.endpoint  # название blueprint + название обработчика
            print('request_endpoint=', user_request)
            user_bp = user_request.split('.')[0]
            access = current_app.config['db_access']
            print(user_role, user_bp, user_request, access)
            if (user_role in access and user_bp in access[user_role]) \
                    or (user_role in access and user_request in access[user_role]):
                return func(*args, **kwargs)
            else:
                return render_template('no_access.html')
        else:
            return render_template('not_authorized.html')
    return wrapper
