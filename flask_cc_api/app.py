import os
from flask import Flask, got_request_exception
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import PyJWTError

from werkzeug.exceptions import HTTPException

from .extensions import (
    celery,
    redis_store,
    db,
    cors
)

from .apis import urls
from .config.celery_config import CeleryConfig
from .config.default_config import DefaultConfig
from .logger.logger import logger

from .exceptions.system_exception import SystemException
from .exceptions.service_exception import ServiceException

from .extensions import celery, migrate, jwt_manager  # noqa

_default_instance_path = '%(instance_path)s/instance' % \
                         {'instance_path': os.path.dirname(os.path.realpath(__file__))}


def log_exception(sender, exception, **extra):
    if (isinstance(exception, ServiceException) or isinstance(exception, SystemException)) \
            and exception.error_code not in (100000, 100001, 300000, 900001) \
            or isinstance(exception, HTTPException) \
            or issubclass(type(exception), PyJWTError) \
            or issubclass(type(exception), JWTExtendedException):
        logger.console(exception)
        return
    logger.exception(exception)


def create_app():
    app = Flask(__name__, instance_relative_config=True, instance_path=_default_instance_path)

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    configure_app(app)
    configure_blueprint(app)
    configure_celery(app, celery)
    configure_extensions(app)
    configure_logging(app)
    return app


def configure_app(app):
    app.config.from_object(CeleryConfig)
    app.config.from_object(DefaultConfig)
    app.config.from_pyfile('dev.py')


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


def configure_extensions(app):

    # redis
    redis_store.init_app(app)

    # jwt
    jwt_manager.init_app(app)

    # cors
    cors.init_app(app,
                  origins=['*'],
                  methods=['POST', 'GET', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
                  allow_headers=['Authorization', 'Content-Type'])
    # db
    db.init_app(app)

    # migrate
    migrate.init_app(app, db)


def configure_logging(app):

    got_request_exception.connect(log_exception, app)


def configure_blueprint(app):
    urls.register_blueprint(app)
