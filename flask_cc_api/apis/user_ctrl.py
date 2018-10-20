from flask_jwt_extended import jwt_required
from flask_restful import Resource

from ..extensions import db
from ..models.user_info import UserInfo
from ..utils.auth_utils import get_user_id
from ..utils.requests_utils import get_request_ip, obj_to_dict
from ..utils.response_utils import ok


class UserInfoHandler(Resource):

    @jwt_required
    def get(self):
        user_id = get_user_id()
        user = UserInfo.query.filter_by(id=user_id).first()
        user.login_ip = get_request_ip()
        result = obj_to_dict(user, ['user_name', 'created_at'])
        db.session.commit()
        return ok(data=result)
