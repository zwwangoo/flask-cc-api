from celery import Celery
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

redis_store = FlaskRedis()

cors = CORS()

migrate = Migrate()

jwt_manager = JWTManager()

db = SQLAlchemy()

celery = Celery('flask_cc_api', include=['flask_cc_api.proj.tasks'])

cache = Cache()
