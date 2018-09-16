import os
from flask import Flask
from cc_api.extensions import celery
from cc_api.views.api import api_blueprint

from cc_api.config.celery_config import CeleryConfig
from cc_api.config.default_config import DefaultConfig

from cc_api.extensions import celery

_default_instance_path = '%(instance_path)s/instance' % \
                         {'instance_path': os.path.dirname(os.path.realpath(__file__))}

def create_app():
    app = Flask(__name__, instance_relative_config=True, instance_path=_default_instance_path)

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    configure_app(app)
    configure_blueprint(app)
    configure_celery(app, celery)
    return app

def configure_app(app):
    app.config.from_object(CeleryConfig)
    app.config.from_object(DefaultConfig)


def configure_celery(app, celery):
    app.config.update({"BROKER_URL": app.config["CELERY_BROKER_URL"]})
    celery.conf.update(app.config)

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask


def configure_blueprint(app):
    app.register_blueprint(api_blueprint, url_prefix='/api')
