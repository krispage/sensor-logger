from flask import Blueprint, request, jsonify
import json
import datetime
import MySQLdb.cursors
from database import mysql

from auth import authenticate_api_key

grafana = Blueprint('grafana', __name__)


# Grafana SimpleJSON
@grafana.route('/grafana/<device_id>', methods=['GET', 'POST'])
def test_connection(device_id):
    success, msg = authenticate_api_key(request)
    if not success:
        return jsonify(msg), 400

    return jsonify(success=True), 200


@grafana.route('/grafana/<device_id>/search', methods=['POST'])
def search(device_id):
    metrics = []
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT field FROM data_fields where device_id = '
                       '(SELECT id FROM devices where identifier = %s)', (device_id,))
        metrics_returned = cursor.fetchall()
        for metric in metrics_returned:
            metrics.append(metric.get('field'))
    finally:
        cursor.close()
    return jsonify(metrics), 200


@grafana.route('/grafana/<device_id>/query', methods=['POST'])
def query(device_id):
    success, msg = authenticate_api_key(request)
    if not success:
        return jsonify(msg), 400

    from_time = None
    to_time = None
    range = None
    if request.json is not None:
        range = request.json.get('range', None)
        if range is not None:
            from_time = datetime.datetime.strptime(range.get('from', None), '%Y-%m-%dT%H:%M:%S.%f%z')
            to_time = datetime.datetime.strptime(range.get('to', None), '%Y-%m-%dT%H:%M:%S.%f%z')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT time, data FROM data WHERE device = %s AND '
                   'time BETWEEN IFNULL(%s, "1900-01-01") AND IFNULL(%s, now()) '
                   'GROUP BY time ORDER BY time asc', (device_id, from_time.strftime('%Y-%m-%d %H:%M:%S'),
                                                       to_time.strftime('%Y-%m-%d %H:%M:%S')))
    response_data = cursor.fetchall()

    response = []

    for target in request.json.get('targets'):
        target_response = {}
        target_response['target'] = target.get('target')
        datapoints = []
        for point in response_data:
            data = json.loads(point.get('data'))
            if target.get('target') in data:
                if (data.get(target.get('target')) != ""):
                    datapoints.append([float(data.get(target.get('target'))), int(point.get('time').timestamp() * 1000)])

        target_response['datapoints'] = datapoints
        response.append(target_response)

    return jsonify(response)
