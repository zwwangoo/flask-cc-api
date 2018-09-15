from flask import Flask
from celery import Celery
from views.api import api_blueprint

from config.celery_config import CeleryConfig


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(CeleryConfig)
    app.config.from_pyfile('config.py')
    configure_blueprint(app)
    return app


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        include=['proj.tasks']
    )
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def configure_blueprint(app):
    app.register_blueprint(api_blueprint, url_prefix='/api')
