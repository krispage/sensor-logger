from flask import Flask
from dotenv import load_dotenv
import os
from core.core import core
from ui.ui import web_ui
from commands import cmd
from database import mysql

app = Flask(__name__)
app.secret_key = os.getenv('APP_KEY')

load_dotenv()
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql.init_app(app)

app.register_blueprint(core)
app.register_blueprint(web_ui)
app.register_blueprint(cmd)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
