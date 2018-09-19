from flask import Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required

from cc_api.utils.auth_utils import get_user_id
from cc_api.utils.requests_utils import get_argument, obj_to_dict, get_request_ip
from cc_api.utils.response_utils import ok

from cc_core.user_info import UserInfo


user_info_blueprint = Blueprint('user', __name__)
user_info_api = Api(user_info_blueprint, catch_all_404s=True)


class UserInfoHandler(Resource):

    @jwt_required
    def get(self):
        user_id = get_user_id()
        user = UserInfo.query.filter_by(id=user_id).first()
        result = obj_to_dict(user, ['user_name', 'created_at'])
        return ok(result)


user_info_api.add_resource(UserInfoHandler, '/information')
