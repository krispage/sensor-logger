from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from passlib.hash import sha256_crypt
from passlib import pwd
import MySQLdb.cursors
from database import mysql
import json

web_ui = Blueprint('ui', __name__, template_folder='templates', static_folder='static', static_url_path='/static/ui')


@web_ui.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))


@web_ui.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:
        if request.method == 'POST':
            if 'device_form' in request.form:
                #for later
                pass
            if 'api_key_form' in request.form:
                print("it's api key form")
                identifier = request.form['identifier']

                exists = None
                if not identifier:
                    flash('An identifier is required')
                else:
                    try:
                        secret_key = pwd.genword(entropy=56, charset='hex', length=32)
                        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        cursor.execute('SELECT id FROM api_keys WHERE api_key = %s', (identifier,))
                        exists = cursor.fetchone()
                        if exists:
                            msg = 'A key with that name already exists'
                        else:
                            cursor.execute('INSERT INTO api_keys (name, api_key) VALUES (%s, %s)',
                                           (identifier, secret_key))
                            mysql.connection.commit()
                    finally:
                        cursor.close()


            print(request.form)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT identifier as id FROM devices')
        devices = cursor.fetchall()
        last_data = {}
        for device in devices:
            cursor.execute('select time from data where device = %s group by time order by time desc limit 1',
                           (device['id'],))
            last_data[device['id']] = cursor.fetchone()

        cursor.execute('SELECT id, name, api_key FROM api_keys')
        api_keys = cursor.fetchall()

        return render_template('dashboard.html', devices=devices, api_keys=api_keys, last_data=last_data)

    return redirect(url_for('ui.login', r=url_for('ui.dashboard')))


@web_ui.route('/register_device', methods=['GET', 'POST'])
def register_device():
    if 'loggedin' not in session:
        return redirect(url_for('ui.login', r=url_for('ui.register_device')))

    msg = ''
    if request.method == 'POST':
        identifier = request.form['identifier']

        exists = None
        if not identifier:
            flash('An identifier is required')
        else:
            try:
                secret_key = pwd.genword(entropy=56, charset='hex', length=32)
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('SELECT identifier FROM devices WHERE identifier = %s', (identifier,))
                exists = cursor.fetchone()
                if exists:
                    msg = 'An device with that identifier already exists'
                else:
                    cursor.execute('INSERT INTO devices (identifier, secret_key) VALUES (%s, %s)',
                                   (identifier, secret_key))
                    mysql.connection.commit()
            finally:
                cursor.close()
            if not exists:
                return redirect(url_for('ui.device_details', device_id=identifier))
    return render_template('register_device.html', msg=msg)


@web_ui.route('/device/<device_id>')
def device_details(device_id):
    if 'loggedin' not in session:
        return redirect(url_for('ui.login', r=url_for('ui.device_details', device_id=device_id)))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT secret_key FROM devices where identifier = %s', (device_id,))
    secret_key = cursor.fetchone()
    if secret_key is None:
        return redirect(url_for('ui.dashboard'))
    cursor.execute(
        'SELECT device as id, time, data FROM data WHERE device = %s GROUP BY id, time, data ORDER BY time desc limit 5',
        (device_id,))
    device = cursor.fetchall()
    for d in device:
        d['data'] = json.loads(d['data'])

    return render_template('device_details.html', identifier=device_id, secret_key=secret_key, device=device)


@web_ui.route('/device/<device_id>/reset')
def device_reset_key(device_id):
    if 'loggedin' not in session:
        return redirect(url_for('ui.login', r=url_for('ui.device_reset_key', device_id=device_id)))

    try:
        secret_key = pwd.genword(entropy=56, charset='hex', length=32)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT identifier from devices where identifier = %s', (device_id,))
        exists = cursor.fetchone()
        if exists:
            cursor.execute('UPDATE devices set secret_key = %s WHERE identifier = %s', (secret_key, device_id))
            mysql.connection.commit()
    finally:
        cursor.close()

    return redirect(url_for('ui.device_details', device_id=device_id))


@web_ui.route('/device/<device_id>/delete')
def device_delete(device_id):
    if 'loggedin' not in session:
        return redirect(url_for('ui.login', r=url_for('ui.device_delete', device_id=device_id)))

    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id from devices where identifier = %s', (device_id,))
        exists = cursor.fetchone()
        if exists:
            cursor.execute('DELETE FROM data_fields WHERE device_id = %s', (exists['id'],))
            cursor.execute('DELETE FROM devices WHERE identifier = %s', (device_id,))
            mysql.connection.commit()
    finally:
        cursor.close()

    return redirect(url_for('ui.dashboard', device_id=device_id))


@web_ui.route('/login', methods=['GET', 'POST'])
def login(msg=''):
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id, username, password FROM users WHERE username = %s', (username,))

        account = cursor.fetchone()

        if account and sha256_crypt.verify(password, account['password']):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            dest_url = request.form['r']

            if not dest_url:
                dest_url = url_for('ui.dashboard')
            return redirect(dest_url)
        else:
            msg = 'Incorrect email/password!'

    dest_url = request.args.get('r')
    if not dest_url:
        dest_url = ""
    return render_template('login.html', msg=msg, redirect=dest_url)


@web_ui.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    session.pop('email', None)
    return redirect(url_for('ui.login'))
