from flask import Blueprint
from flask_restful import Resource, Api

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, catch_all_404s=True)


class Index(Resource):

    def get(self):
        # 10 秒后执行该函数
        sum.apply_async((2, 2), countdown=10)
        return 'ok'


api.add_resource(Index, '/')
