from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'agenda'

    mysql.init_app(app)

    from .routes import main
    app.register_blueprint(main, url_prefix='/')

    return app
