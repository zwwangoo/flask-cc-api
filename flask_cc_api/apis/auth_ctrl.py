from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_refresh_token_required)
from flask_restful import Resource

from ..exceptions.service_error import ServiceError
from ..exceptions.service_exception import ServiceException
from ..models.user_info import UserInfo
from ..utils.auth_utils import get_user_id, verify_hash
from ..utils.requests_utils import get_argument
from ..utils.response_utils import ok


class UserLoginHandler(Resource):

    def post(self):
        user_name = get_argument('user_name', required=True)
        user_password = get_argument('user_password', required=True)

        user = UserInfo.query.filter_by(user_name=user_name).first()

        if user and verify_hash(user_password, user.password):
            access_token = create_access_token(identity=user.id)
            refrech_token = create_refresh_token(identity=user.id)
            result = {'access_token': access_token, 'refrech_token': refrech_token}
            return ok(result)
        else:
            raise ServiceException(ServiceError.NO_AUTH)


class UserTokenRefrech(Resource):

    @jwt_refresh_token_required
    def post(self):
        user_id = get_user_id()
        user = UserInfo.query.filter_by(id=user_id).first()
        if user:
            access_token = create_access_token(identity=user.id)
            result = {'access_token': access_token}
            return ok(data=result)
        else:
            raise ServiceException(ServiceError.NO_AUTH)
