from database import mysql
import MySQLdb.cursors


def authenticate(request, identifier=None):
    if not request.is_json:
        return False, {"msg": "Missing JSON in request"}

    if identifier is None:
        identifier = request.json.get('identifier', None)
    secret_key = request.headers.get('Authorization', None)
    if not identifier:
        return False, {"msg": "Missing identifier parameter"}
    if not secret_key:
        return False, {"msg": "Missing Authorization parameter"}
    else:
        if not secret_key.startswith("Bearer "):
            return False, {"msg": "Authorization must contain Bearer "}
        secret_key = secret_key[7:]

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM devices WHERE identifier = %s and secret_key = %s', (identifier, secret_key))
    user = cursor.fetchone()
    if user is None:
        return False, {"msg": "Bad username or password"}

    return True, {"msg": "success"}
