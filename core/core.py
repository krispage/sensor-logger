from flask import Blueprint, render_template, jsonify, request, redirect, url_for
import datetime
import MySQLdb.cursors
from database import mysql
import json
from auth import authenticate

core = Blueprint('core', __name__, template_folder='templates', static_folder='static', static_url_path='/static/core')


@core.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('ui.dashboard'))


@core.route('/version')
def version():
    return render_template('version.html')


@core.route('/auth', methods=['POST'])
def auth():
    success, msg = authenticate(request)
    if success:
        return jsonify(success="true"), 200
    else:
        return jsonify(msg), 400


@core.route('/data', methods=['POST'])
def data():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400

        success, msg = authenticate(request)

        if not success:
            return jsonify(msg), 400

        identifier = request.json.get('identifier', None)
        request_data = request.json['data']
        time = datetime.datetime.now()

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO data (device, time, data) VALUES (%s, %s, %s)',
                           (identifier, time, json.dumps(request_data)))
            mysql.connection.commit()
            for field in request_data:
                try:
                    cursor.execute('INSERT INTO data_fields(device_id, field) '
                                   'VALUES((SELECT id FROM devices WHERE identifier = %s),%s)', (identifier, field))
                    mysql.connection.commit()
                except:
                    pass

        finally:
            cursor.close()

        return jsonify(success="true"), 200


@core.route('/data/device/<device_id>', methods=['GET'])
def device_data(device_id):
    success, msg = authenticate(request, identifier=device_id)
    if not success:
        return jsonify(msg), 400

    from_time = None
    to_time = None

    if request.json is not None:
        from_time = datetime.datetime.strptime(request.json.get('from', None), '%Y-%m-%d %H:%M:%S')
        to_time = datetime.datetime.strptime(request.json.get('to', None), '%Y-%m-%d %H:%M:%S')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT device as id, time, data FROM data WHERE device = %s AND '
                   'time BETWEEN IFNULL(%s, "1900-01-01") AND IFNULL(%s, now()) '
                   'GROUP BY time ORDER BY time asc', (device_id, from_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                       to_time.strftime('%Y-%m-%d %H:%M:%S')))
    request_data = cursor.fetchall()

    return jsonify(request_data, 200)


