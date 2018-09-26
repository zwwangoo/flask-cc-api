import time
from flask import json, make_response


def response(data=None, error_code=None, msg='', http_status_code=200):
    args = {}
    if error_code:
        args['error_code'] = error_code
        args['bool_status'] = False
    else:
        args['bool_status'] = True

    if data:
        args['data'] = data

    args['msg'] = msg
    args['response_time'] = int(time.time())
    response = make_response(json.dumps(args))
    response.headers['Content-Type'] = 'application/json;charset=UTF-8'
    return response


def error(msg='error', error_code=None, http_status_code=200):
    return response(error_code=error_code, msg=msg, http_status_code=http_status_code)


def ok(data=None, msg='ok', http_status_code=200):
    return response(data=data, msg=msg, http_status_code=http_status_code)
