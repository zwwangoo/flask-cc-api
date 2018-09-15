import time
from wsgi import celery


@celery.task(bind=True)
def add(self, a, b):
    try:
        c = a + b
    except Exception as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)
    return a + b
