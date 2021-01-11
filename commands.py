from flask import Blueprint
from flask.cli import with_appcontext
import click
import MySQLdb.cursors
from database import mysql
from passlib.hash import sha256_crypt
import re

cmd = Blueprint('cmd', __name__)


@cmd.cli.command('create_user')
@click.argument('name')
@click.argument('pwd')
@with_appcontext
def create_user(name, pwd):
    """Creates a user"""
    print("Create \nuser: {} \npass: {}".format(name, pwd))
    username = name
    password = sha256_crypt.encrypt(pwd)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    account = cursor.fetchone()
    if account:
        print('Account already exists!')
    elif not re.match(r'[A-Za-z0-9]+', username):
        print('Username must contain only characters and numbers!')
    elif not username or not password:
        print('Needs both username and password')
    else:
        cursor.execute('INSERT INTO users(username, password) VALUES (%s, %s)', (username, password))
        mysql.connection.commit()
        print('You have successfully registered account "{}"! Now log in'.format(username))


@cmd.cli.command('reset_password')
@click.argument('name')
@click.argument('pwd')
@with_appcontext
def reset_password(name, pwd):
    """Reset a user's password"""
    print("Create \nuser: {} \npass: {}".format(name, pwd))
    username = name
    password = sha256_crypt.encrypt(pwd)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT username FROM users where username = %s', (username,))
    account = cursor.fetchone()
    if account is None:
        print('Account doesn\'t exists!')
    elif not re.match(r'[A-Za-z0-9]+', username):
        print('Username must contain only characters and numbers!')
    else:
        cursor.execute('UPDATE users set password = %s where username = %s', (password, username))
        mysql.connection.commit()
        print('Password updated for "{}"'.format(username))


@cmd.cli.command('delete_user')
@click.argument('name')
@with_appcontext
def delete_user(name):
    """Delete a user"""
    print("Delete nuser: {}".format(name))
    username = name
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    account = cursor.fetchone()
    if account is None:
        print('Account doesn\'t exists!')
    else:
        cursor.execute('DELETE FROM users WHERE username = %s', (username,))
        mysql.connection.commit()
        print('"{}" deleted'.format(username))


cmd.cli.add_command(create_user)
cmd.cli.add_command(delete_user)
