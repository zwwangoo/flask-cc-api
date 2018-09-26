from flask import request
from flask_restful import reqparse
from enum import Enum
from datetime import datetime
from werkzeug import datastructures


def get_argument(key, *, default=None, type=str, location=None, help=None, required=False):
    kwargs = dict(default=default, type=type)
    if location:
        kwargs['location'] = location
    if type == 'file':
        kwargs['type'] = datastructures.FileStorage
        kwargs['location'] = location if location else 'files'

    parser = reqparse.RequestParser()
    parser.add_argument(key, **kwargs)
    args = parser.parse_args()

    return args[key]


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


def get_request_ip():
    if request.remote_addr == '127.0.0.1':
        return '127.0.0.1'
    ip_list = request.headers['X-Forwarded-For']
    ip = ip_list.split(',')[0]
    return ip
