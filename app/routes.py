from flask import Blueprint, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors

main = Blueprint('main', __name__)
mysql = MySQL()

@main.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM eventos')
    eventos = cursor.fetchall()
    cursor.close()
    return render_template('index.html', eventos=eventos)

@main.route('/event/<int:id>')
def event(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM eventos WHERE id = %s', (id,))
    evento = cursor.fetchone()
    cursor.close()
    if evento:
        return render_template('event.html', evento=evento)
    return 'Evento no encontrado', 404

@main.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO eventos (titulo, descripcion, fecha) VALUES (%s, %s, %s)', 
                       (titulo, descripcion, fecha))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('main.index'))
