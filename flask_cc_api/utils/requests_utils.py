from flask import g, request
from flask_restful import reqparse
from werkzeug import datastructures

from ..exceptions.system_error import SystemError
from ..exceptions.system_exception import SystemException


def _get_request():
    if 'req' not in g:
        g.req = reqparse.RequestParser()
    return g.req


def get_argument(key, *, default=None, type=str, location=None, help=None, required=False):
    kwargs = dict(default=default, type=type)
    if location:
        kwargs['location'] = location
    if type == 'file':
        kwargs['type'] = datastructures.FileStorage
        kwargs['location'] = location if location else 'files'

    parser = _get_request()
    parser.add_argument(key, **kwargs)
    args = parser.parse_args()

    if required and (args[key] is None or type == str and args[key].strip() == '' and key != '_id'):
        raise SystemException(SystemError.MISSING_REQUIRED_PARAMETER, help if help else key)

    return args[key]


def get_request_ip():
    if request.remote_addr == '127.0.0.1':
        return '127.0.0.1'
    ip_list = request.headers['X-Forwarded-For']
    ip = ip_list.split(',')[0]
    return ip
