from celery import Celery

celery = Celery('cc_api', include=['proj.tasks'])
