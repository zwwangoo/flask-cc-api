import time
from cc_api.extensions import celery


@celery.task(bind=True)
def add(self, a, b):
    try:
        c = a + b
        print('celery tasks……')
    except Exception as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)
    return a + b
