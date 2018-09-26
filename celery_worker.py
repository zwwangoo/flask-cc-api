"""
    启动 Celery Worker 进程
        celery -A celery_worker.celery --loglevel=info worker
    启动 Celery Beat 进程，定时将任务发送到 Broker
        celery beat -A celery_worker.celery -s ./cc_api/proj/schedule/beat

    一个终端启动
        celery -B -A celery_worker.celery worker --loglevel=info -s ./cc_api/proj/schedule/beat
"""
from cc_api.app import create_app
from cc_api.extensions import celery  # noqa

app = create_app()