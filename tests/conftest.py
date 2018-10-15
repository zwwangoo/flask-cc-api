import pytest

from flask_cc_api.app import create_app
from flask_cc_api.extensions import db as _db


class TestUser():

    @property
    def username(self):
        return 'admin'

    @property
    def password(self):
        return '123456'


@pytest.yield_fixture
def app():
    _app = create_app()
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.yield_fixture
def db(app):
    _db.app = app
    with app.app_context():
        _db.create_all()
    yield _db

    _db.session.close()
    _db.drop_all()
