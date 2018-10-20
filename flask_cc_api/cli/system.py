from flask.cli import click, with_appcontext

from ..extensions import db
from ..models.user_info import UserInfo
from ..utils.auth_utils import generate_hash
from .main import cli


def get_prompt(tip, data_type, default=None, hide_input=False):
    data = click.prompt(tip, type=data_type, default=default, hide_input=hide_input)
    if not data:
        get_prompt(tip, data_type, default)

    return data


def get_password():
    password = get_prompt('Passowrd (Characters <= 32)', data_type=str, hide_input=True)
    confirm = get_prompt('Repeat passowrd (Characters <= 32)', data_type=str, hide_input=True)
    if password != confirm:
        click.echo('Passwords does not match')
        get_password()
    else:
        return password


@cli.command('new_user')
@with_appcontext
def new_user():
    ''' new user '''
    click.echo('Create an user follow these steps\n')

    user_name = get_prompt('Username (Characters <= 32)', str, 'user')
    password = get_password().encode()

    user_info = UserInfo.query.filter(UserInfo.user_name == user_name).first()

    if user_info:
        click.echo('\nCreate failed')
        click.echo('User already exists')
    else:
        user = UserInfo()
        user.user_name = user_name
        user.password = generate_hash(password)
        db.session.add(user)
        db.session.commit()
        click.echo('\nCreate user successfully')
