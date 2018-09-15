from flask import Blueprint, current_app
from flask_restful import Resource, Api

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, catch_all_404s=True)


class Index(Resource):

    def get(self):
        print(current_app.config)
        return 'ok'


api.add_resource(Index, '')
