from flask import g, request
from flask_restful import reqparse
from werkzeug import datastructures

from ..exceptions.system_error import SystemError
from ..exceptions.system_exception import SystemException
from ..exceptions.service_error import ServiceError
from ..exceptions.service_exception import ServiceException


def _get_request():
    if 'req' not in g:
        g.req = reqparse.RequestParser()
    print(request.__dict__)
    return g.req


def get_argument(
    key, *, default=None, type=str, location=None,
    help=None, required=False, action='store'
):
    '''
    :param default: The value produced if the argument is absent from the
        request.
    :param type: The type to which the request argument should be
        converted. If a type raises an exception, the message in the
        error will be returned in the response. Defaults to :class:`unicode`
        in python2 and :class:`str` in python3.
    :param action: The basic type of action to be taken when this argument
        is encountered in the request. Valid options are "store" and "append".
    :param location: The attributes of the :class:`flask.Request` object
        to source the arguments from (ex: headers, args, etc.), can be an
        iterator. The last item listed takes precedence in the result set.
    :param help: A brief description of the argument, returned in the
        response when the argument is invalid. May optionally contain
        an "{error_msg}" interpolation token, which will be replaced with
        the text of the error raised by the type converter.
    '''
    cur_type = type  # 保存参数初始时的状态
    type = str if type == int else cur_type  # 当类型为int时，先转换成str的获取形式

    kwargs = dict(default=default, type=type, action=action)
    if location:
        kwargs['location'] = location
    if type == 'file':
        kwargs['type'] = datastructures.FileStorage
        kwargs['location'] = location if location else 'files'

    parser = _get_request()
    parser.add_argument(key, **kwargs)
    args = parser.parse_args()

    if cur_type == int and args[key]:  # 将str的结果转换成int
        try:
            args[key] = cur_type(args[key])
            type = cur_type
        except:
            raise ServiceException(ServiceError.INVALID_VALUE, key)

    if required and action == 'store' and \
       (args[key] is None or type == str and args[key].strip() == '' and key != '_id'):
        raise SystemException(SystemError.MISSING_REQUIRED_PARAMETER, help if help else key)

    return args[key]


def get_request_ip():
    if request.remote_addr == '127.0.0.1':
        return '127.0.0.1'
    ip_list = request.headers['X-Forwarded-For']
    ip = ip_list.split(',')[0]
    return ip
