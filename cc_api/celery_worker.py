"""
    启动 Celery Worker 进程
        celery -A celery_worker.celery --loglevel=info worker
    启动 Celery Beat 进程，定时将任务发送到 Broker
        celery beat -A celery_worker.celery
"""
from cc_api.app import create_app
from cc_api.extensions import celery  # noaq

app = create_app()
