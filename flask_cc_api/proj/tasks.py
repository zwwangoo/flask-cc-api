import time

from ..extensions import celery


@celery.task(bind=True)
def add(self, a, b):
    try:
        c = a + b
        time.sleep(10)
        print('celery tasks……')
    except Exception as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)
    return c


@celery.task(bind=True)
def sum(self, a, b):
    c = a * b
    time.sleep(12)
    print('sum')
    return c
