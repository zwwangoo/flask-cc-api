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
        """用户登录
        ---
        tags:
          - auth
        summary: 管理员登录接口
        parameters:
          - name: body
            in: body
            required: true
            description: '用户通过账号密码进行登录'
            properties:
              user_name:
                type: string
                description: '账号'
                example: 'admin'
              user_password:
                type: string
                description: '密码'
                example: '123456'
        responses:
          200:
            description: 登录成功之后返回token值
            properties:
              data:
                properties:
                  access_token:
                    type: string
                    description: 'token值'
                  refresh_token:
                    type: string
                    description: '刷新token值'
              msg:
                type: string
              bool_status:
                type: integer
              response_time:
                type: integer
        """
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
        """刷新Token
        ---
        tags:
          - auth
        security:
          - Token: []
        responses:
          200:
            description: 登录成功之后返回token值
            schema:
              properties:
                data:
                  properties:
                    access_token:
                      type: string
                msg:
                  type: string
                bool_status:
                  type: integer
                response_time:
                  type: integer

              example: {bool_status: 1, msg: ok, data: {access_token: xxx}}
        """
        user_id = get_user_id()
        user = UserInfo.query.filter_by(id=user_id).first()
        if user:
            access_token = create_access_token(identity=user.id)
            result = {'access_token': access_token}
            return ok(data=result)
        else:
            raise ServiceException(ServiceError.NO_AUTH)
