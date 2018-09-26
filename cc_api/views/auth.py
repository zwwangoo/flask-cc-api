from flask import Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required

from cc_api.utils.requests_utils import get_argument
from cc_api.utils.response_utils import response
from cc_core.user_info import UserInfo
from cc_api.utils.auth_utils import verify_hash, get_user_id

auth_blueprint = Blueprint('auth', __name__)
auth_api = Api(auth_blueprint, catch_all_404s=True)


class UserLoginHandler(Resource):

    def post(self):
        user_name = get_argument('user_name', required=True)
        user_password = get_argument('user_password', required=True)

        user = UserInfo.query.filter_by(user_name=user_name).first()

        if user and verify_hash(user_password, user.password):
            access_token = create_access_token(identity=user.id)
            refrech_token = create_refresh_token(identity=user.id)
            result = {'access_token': access_token, 'refrech_token': refrech_token}
            return response(data=result)
        else:
            return response(code=100001)


class UserTokenRefrech(Resource):

    @jwt_refresh_token_required
    def get(self):
        user_id = get_user_id()
        user = UserInfo.query.filter_by(id=user_id).first()
        if user:
            access_token = create_access_token(identity=user.id)
            result = {'access_token': access_token}
            return response(data=result)
        else:
            return response(code=100002)


auth_api.add_resource(UserLoginHandler, '/login')
auth_api.add_resource(UserTokenRefrech, '/token/refrech')
