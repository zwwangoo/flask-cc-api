import click
from ..app import create_app
from flask.cli import FlaskGroup


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass
