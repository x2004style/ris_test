from dataclasses import dataclass
from database.select import select_list


@dataclass
class PatientInfoResponse:
    result: tuple
    error_message: str
    status: bool


def model_route(db_config, user_input_data, sql_provider, query_id):
    if query_id == 1:
        error_message = ''
        if ('year' not in user_input_data) or ('month' not in user_input_data):
            print('user_input_data=', user_input_data)
            error_message = 'param_error'
            result = ()
            return PatientInfoResponse(result, error_message=error_message, status=False)

        _sql = sql_provider.get('doctors_query.sql', year= f"'{user_input_data['year']}'", month=user_input_data['month'])
        print('sql=', _sql)
        try:
            result, schema = select_list(db_config, _sql)
        except TypeError:
            error_message = 'type_error'
            return PatientInfoResponse((), error_message=error_message, status=False)
        else:
            return PatientInfoResponse(result=result, error_message=error_message, status=True)
    if query_id == 2:
        error_message = ''
        if 'p_id' not in user_input_data:
            print('user_input_data=', user_input_data)
            error_message = 'param_error'
            result = ()
            return PatientInfoResponse(result, error_message=error_message, status=False)

        _sql = sql_provider.get('patient_history_query.sql', p_id=user_input_data['p_id'])
        print('sql=', _sql)
        try:
            result, schema = select_list(db_config, _sql)
        except TypeError:
            error_message = 'type_error'
            return PatientInfoResponse((), error_message=error_message, status=False)
        else:
            return PatientInfoResponse(result=result, error_message=error_message, status=True)
    if query_id == 3:
        error_message = ''
        if 'd_id' not in user_input_data:
            print('user_input_data=', user_input_data)
            error_message = 'param_error'
            result = ()
            return PatientInfoResponse(result, error_message=error_message, status=False)

        _sql = sql_provider.get('patients_query.sql', d_id=user_input_data['d_id'])
        print('sql=', _sql)
        try:
            result, schema = select_list(db_config, _sql)
        except TypeError:
            error_message = 'type_error'
            return PatientInfoResponse((), error_message=error_message, status=False)
        else:
            return PatientInfoResponse(result=result, error_message=error_message, status=True)

