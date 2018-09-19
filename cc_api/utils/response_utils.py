from flask import json, make_response


class JsonResult():
    def __init__(self, msg, bool_status, data, error_code):
        self._msg = msg
        self._bool_status = bool_status
        self._data = data
        self._error_code = error_code

    def get_dict(self):
        result = dict(bool_status=self._bool_status, data=self._data)
        if self._msg:
            result['msg'] = self._msg
        if self._error_code:
            result['error_code'] = self._error_code

        return result


def ok(data={}, msg='ok', data_encoder=True, content_type='application/json;charset=UTF-8'):
    result = JsonResult(msg, True, data, None)
    response = make_response(json.dumps(result.get_dict()))
    response.headers['Content-Type'] = 'application/json;charset=UTF-8'
    return response
