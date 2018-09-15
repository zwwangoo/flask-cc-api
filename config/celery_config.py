from datetime import timedelta


class CeleryConfig(dict):

    CELERY_BROKER_URL = 'redis://localhost:16379/4'

    CELERYBEAT_SCHEDULE = {
        'task_add': {
            'task': 'proj.tasks.add',
            'schedule': timedelta(seconds=30),
            'args': (1, 2),
        }
    }

