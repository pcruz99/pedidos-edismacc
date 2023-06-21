from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from database import select_user
from connections.oracle_conn import Connection

auth = Blueprint('auth', __name__, url_prefix='/auth')

conn = None

@auth.route('/login', methods=('GET', 'POST'))
def login():
    global conn
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']              

        error = None
        try:
            user = select_user(username)                 
        except Exception as e:  
            user = None          
            print(e)

        if user is None:
            error = 'Nombre de Usuario Incorrecto.'
        elif (user[2] != password):
            error = 'Contraseña Incorrecta.'
        if error is None:
            session.clear()
            session['username'] = user[1]
            conn = Connection.getConn(username)
            print(conn)
            return redirect(url_for('pedido.insertar_pedido'))
        flash(error)

    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))