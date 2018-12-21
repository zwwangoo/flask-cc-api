import time
from datetime import datetime
from enum import Enum

from flask import json, make_response


def response(data=None, error_code=None, msg='', http_status_code=200):
    args = {}
    if error_code is not None:
        args['error_code'] = error_code
        args['bool_status'] = False
    else:
        args['bool_status'] = True

    if data:
        args['data'] = data

    args['msg'] = msg
    args['response_time'] = int(time.time())
    response = make_response(json.dumps(args), http_status_code)
    response.headers['Content-Type'] = 'application/json;charset=UTF-8'
    return response


def error(msg='error', error_code=None, http_status_code=200):
    return response(error_code=error_code, msg=msg, http_status_code=http_status_code)


def ok(data=None, msg='ok', http_status_code=200):
    return response(data=data, msg=msg, http_status_code=http_status_code)


def obj_to_dict(obj, keys=None, *, display=True, format_time='%Y-%m-%d %H:%M:%S'):
    dict_result = {}
    obj_values = obj.__dict__

    for key in obj_values:
        if key == '_sa_instance_state':
            continue
        key_value = obj_values.get(key)
        if display and key in keys \
                or not display and key not in keys:
            if isinstance(key_value, datetime):
                dict_result[key] = datetime.strftime(key_value, format_time)
            elif isinstance(key_value, Enum):
                dict_result[key] = key_value.value
            else:
                dict_result[key] = key_value
    return dict_result
