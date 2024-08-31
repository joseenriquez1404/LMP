from flask import Blueprint, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

main = Blueprint('main', __name__)
mysql = MySQL()

@main.route('/')
def index():
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM eventos')
        eventos = cursor.fetchall()
        cursor.close()
        return render_template('index.html', eventos=eventos)
    except Exception as e:
        print(f"Error: {e}")
        return "Internal Server Error", 500


@main.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        try:
            titulo = request.form['titulo']
            descripcion = request.form['descripcion']
            fecha = request.form['fecha']

            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO eventos (titulo, descripcion, fecha) VALUES (%s, %s, %s)', 
                           (titulo, descripcion, fecha))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('main.index'))
        except Exception as e:
            print(f"Error: {e}")
            return "Internal Server Error", 500
    return render_template('agregar.html')
