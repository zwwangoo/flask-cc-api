from flask.cli import FlaskGroup, click

from ..app import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass
