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
        print(f"Error al obtener los eventos: {e}")
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
            print(f"Error al agregar el evento: {e}")
            return "Internal Server Error", 500
    return render_template('agregar.html')

@main.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_evento(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM eventos WHERE id = %s', (id,))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('main.index'))
    except Exception as e:
        print(f"Error al eliminar el evento: {e}")
        return "Internal Server Error", 500

@main.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        try:
            nuevo_titulo = request.form['titulo']
            nueva_descripcion = request.form['descripcion']
            nueva_fecha = request.form['fecha']

            cursor = mysql.connection.cursor()
            cursor.execute('''
                UPDATE eventos
                SET titulo = %s, descripcion = %s, fecha = %s
                WHERE id = %s
            ''', (nuevo_titulo, nueva_descripcion, nueva_fecha, id))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('main.index'))
        except Exception as e:
            print(f"Error al editar el evento: {e}")
            return "Internal Server Error", 500

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM eventos WHERE id = %s', (id,))
    evento = cursor.fetchone()
    cursor.close()

    if evento is None:
        return "Evento no encontrado", 404

    return render_template('editar.html', evento=evento)
