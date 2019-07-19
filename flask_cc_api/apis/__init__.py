import os
from flask import current_app
from flask.signals import got_request_exception
from flask_restful import Api as BaseApi
from werkzeug.exceptions import HTTPException
from jwt.exceptions import PyJWTError, ExpiredSignatureError, InvalidSignatureError
from flask_jwt_extended.exceptions import (
    JWTExtendedException, NoAuthorizationError,
    RevokedTokenError, InvalidHeaderError,
)

from ..exceptions.service_exception import ServiceException
from ..exceptions.system_exception import SystemException
from ..utils.response_utils import error


class Api(BaseApi):

    def __init__(
        self, app=None, prefix='',
        default_mediatype='application/json', decorators=None,
        catch_all_404s=True, serve_challenge_on_401=False,
        url_part_order='bae', errors=None,
    ):
        super().__init__(
            app, prefix,
            default_mediatype, decorators,
            catch_all_404s, serve_challenge_on_401,
            url_part_order, errors,
        )

    def handle_error(self, e):
        got_request_exception.send(current_app._get_current_object(), exception=e)

        if isinstance(e, HTTPException):
            code = e.code
            ext = e
        elif isinstance(e, ServiceException) or isinstance(e, SystemException):
            code = 200
            ext = e
        elif issubclass(type(e), (PyJWTError, JWTExtendedException)):
            code = 403
            if isinstance(e, NoAuthorizationError):
                ext = SystemException(102004)
            elif isinstance(e, InvalidHeaderError):
                ext = SystemException(102005)
            elif isinstance(e, (RevokedTokenError, ExpiredSignatureError)):
                ext = SystemException(102008)
            elif isinstance(e, InvalidSignatureError):
                ext = SystemException(102009)
            else:
                ext = SystemException(102010)
        else:
            code = 502
            ext = e if os.environ.get('FLASK_ENV') != 'production' \
                else SystemException(101002)

        if hasattr(ext, 'error_code'):
            error_code = ext.error_code
        else:
            error_code = 101002

        return error(msg=str(ext), error_code=error_code, http_status_code=code)
