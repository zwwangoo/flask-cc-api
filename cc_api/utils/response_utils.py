import time
from flask import json, make_response


def response(code=1, **args):
    if code == 1:
        if not args or 'data' not in args:
            args['data'] = {}
        args['bool_status'] = True
    else:
        args['bool_status'] = False
        args['error_msg'] = 'Login error'
        args['error_code'] = code
    args['response_time'] = int(time.time())
    response = make_response(json.dumps(args))
    response.headers['Content-Type'] = 'application/json;charset=UTF-8'
    return response
