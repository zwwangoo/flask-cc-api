import click
from app import create_app
from celery.bin.celery import CeleryCommand
from flask.cli import FlaskGroup, ScriptInfo, with_appcontext
from extensions import celery


@click.group(cli=FlaskGroup, create_app=create_app)
def cli():
    pass


@click.group(cli=FlaskGroup, create_app=create_app)
@with_appcontext
def start_celery(ctx):
    """Preconfigured wrapper around the 'celery' command."""
    CeleryCommand(celery).execute_from_commandline(
        ["celery"] + ctx.args
    )
