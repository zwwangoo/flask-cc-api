from datetime import timedelta


class CeleryConfig(dict):

    CELERY_BROKER_URL = 'redis://localhost:16379/14'
    CELERY_IGNORE_RESULT = True

    CELERYBEAT_SCHEDULE = {
        'task_add': {
            'task': 'flask_cc_api.proj.tasks.add',
            'schedule': timedelta(seconds=30),
            'args': (1, 2),
        }
    }
