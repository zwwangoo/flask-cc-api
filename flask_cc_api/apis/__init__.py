import os
from flask import current_app
from flask.signals import got_request_exception
from flask_restful import Api as BaseApi
from werkzeug.exceptions import HTTPException
from jwt.exceptions import PyJWTError, ExpiredSignatureError, InvalidSignatureError
from flask_jwt_extended.exceptions import (JWTExtendedException, NoAuthorizationError,
                                           RevokedTokenError, InvalidHeaderError)

from ..exceptions.service_exception import ServiceException
from ..exceptions.system_exception import SystemException
from ..utils.response_utils import error


class Api(BaseApi):

    def __init__(self, app=None, prefix='',
                 default_mediatype='application/json', decorators=None,
                 catch_all_404s=True, serve_challenge_on_401=False,
                 url_part_order='bae', errors=None):
        super().__init__(app, prefix,
                         default_mediatype, decorators,
                         catch_all_404s, serve_challenge_on_401,
                         url_part_order, errors)

    def handle_error(self, e):
        got_request_exception.send(current_app._get_current_object(), exception=e)

        code = 200
        result = None

        if isinstance(e, HTTPException):
            code = e.code
            result = error(msg=str(e),
                           error_code=100001, http_status_code=code)
        elif isinstance(e, ServiceException) or isinstance(e, SystemException):
            result = error(msg=str(e), error_code=e.error_code, http_status_code=code)
        elif issubclass(type(e), JWTExtendedException):
            code = 403
            if isinstance(e, NoAuthorizationError):
                result = error(msg=str(e), error_code=101001, http_status_code=code)
            elif isinstance(e, RevokedTokenError):
                result = error(msg=str(e), error_code=101002, http_status_code=code)
            elif isinstance(e, InvalidHeaderError):
                result = error(msg=str(e), error_code=101003, http_status_code=code)
        elif issubclass(type(e), PyJWTError):
            code = 403
            if isinstance(e, ExpiredSignatureError):
                result = error(msg=str(e), error_code=101004, http_status_code=code)
            elif isinstance(e, InvalidSignatureError):
                result = error(msg=str(e), error_code=101005, http_status_code=code)
        else:
            result = error(
                msg=str(e) if not os.environ.get('PRODUCTION_CONFIG') else 'No response',
                error_code=100002,
                http_status_code=code
            )

        return result
