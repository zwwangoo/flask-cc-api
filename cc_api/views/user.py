from flask import Blueprint
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from . import Api
from ..utils.auth_utils import get_user_id
from ..utils.requests_utils import obj_to_dict, get_request_ip
from ..utils.response_utils import response

from cc_core.user_info import UserInfo
from cc_core.base import db


user_info_blueprint = Blueprint('user', __name__)
user_info_api = Api(user_info_blueprint, catch_all_404s=True)


class UserInfoHandler(Resource):

    @jwt_required
    def get(self):
        user_id = get_user_id()
        user = UserInfo.query.filter_by(id=user_id).first()
        user.ip = get_request_ip()
        db.session.commit()
        result = obj_to_dict(user, ['user_name', 'created_at'])
        return response(data=result)


user_info_api.add_resource(UserInfoHandler, '/information')
