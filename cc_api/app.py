import os
from flask import Flask, got_request_exception
from flask_migrate import Migrate

from cc_core.base import db

from .extensions import celery, redis_store

from .views.api import api_blueprint
from .views.auth import auth_blueprint
from .views.user import user_info_blueprint

from .config.celery_config import CeleryConfig
from .config.default_config import DefaultConfig
from .logger.logger import logger

from .extensions import celery, migrate, jwt_manager  # noqa

_default_instance_path = '%(instance_path)s/instance' % \
                         {'instance_path': os.path.dirname(os.path.realpath(__file__))}


def create_app():
    app = Flask(__name__, instance_relative_config=True, instance_path=_default_instance_path)

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    configure_app(app)
    configure_blueprint(app)
    configure_celery(app, celery)
    configure_database(app, db)
    configure_extensions(app)
    configure_logging(app)
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


def configure_database(app, db):
    db.init_app(app)
    Migrate(app, db)


def configure_extensions(app):

    redis_store.init_app(app)

    jwt_manager.init_app(app)


def configure_logging(app):

    def log_exception(sender, exception, **extra):
        logger.exception(exception)

    got_request_exception.connect(log_exception, app)


def configure_blueprint(app):
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(user_info_blueprint, url_prefix='/auth')
