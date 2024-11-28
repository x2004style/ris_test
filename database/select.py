from database.DBcm import DBContextManager

def select_list(db_config: dict, _sql):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            cursor.execute(_sql)
            print('cursor.description', cursor.description)
            result = cursor.fetchall()
            print(cursor.description)
            schema = [item[0] for item in cursor.description]
            return result, schema

def select_dict(db_config: dict, _sql: str):
    result, schema = select_list(db_config, _sql)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    print(result_dict)
    return result_dict

def call_proc(db_config: dict, proc_name: str, *args):
    res = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        param_list = []
        for arg in args:
            param_list.append(arg)
        cursor.callproc(proc_name, param_list)
        res = cursor.fetchall()
        print(res)
    return res
