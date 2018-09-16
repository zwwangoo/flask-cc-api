import click
from cc_api.app import create_app
from celery.bin.celery import CeleryCommand
from flask.cli import FlaskGroup, ScriptInfo, with_appcontext


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass
