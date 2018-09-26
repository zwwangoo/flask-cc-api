from celery import Celery
from flask_redis import FlaskRedis

redis_store = FlaskRedis()

celery = Celery('cc_api', include=['cc_api.proj.tasks'])
