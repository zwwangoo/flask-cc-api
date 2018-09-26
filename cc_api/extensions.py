from celery import Celery
from flask_redis import FlaskRedis
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

redis_store = FlaskRedis()

celery = Celery('cc_api', include=['cc_api.proj.tasks'])

migrate = Migrate()

jwt_manager = JWTManager()
