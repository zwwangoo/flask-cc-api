from celery import Celery

celery = Celery('cc_api', include=['cc_api.proj.tasks'])
