from flask_jwt_extended import jwt_required
from flask_restful import Resource

from ..extensions import cache, db
from ..models.user_info import UserInfo
from ..utils.auth_utils import get_user_id
from ..utils.cache_utils import cache_key
from ..utils.requests_utils import get_request_ip, obj_to_dict
from ..utils.response_utils import ok


class UserInfoHandler(Resource):

    @jwt_required
    @cache.cached(key_prefix=cache_key, timeout=60)
    def get(self):
        """
        获取用户信息
        ---
        tags:
          - user
        security:
          - Token: []
        responses:
          200:
            description: 获取用户信息
            schema:
              properties:
                data:
                  tpye: string
                msg:
                  type: string
                bool_status:
                  type: integer
              example: {bool_status: 1, msg: ok, data: {item: [UserInfo]}}
        """
        user_id = get_user_id()
        user = UserInfo.query.filter_by(id=user_id).first()
        user.login_ip = get_request_ip()
        result = obj_to_dict(user, ['user_name', 'created_at'])
        db.session.commit()
        return ok(data=result)
