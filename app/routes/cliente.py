from flask import Blueprint, request, render_template, redirect, url_for, flash
from database import select_all_clientes, select_cliente_for_codi, insert_cliente, update_cliente, delete_cliente
import pdfkit
from pathlib import Path
import os

BASE_DIR = Path(os.path.join(os.path.dirname(__file__))).parent.parent

cliente = Blueprint('cliente', __name__, url_prefix='/cliente')

@cliente.route('/', methods=['GET'])
def Index():
    data = select_all_clientes()   
    return render_template('/cliente/index.html', clientes=data)

@cliente.route('/insertar_cliente', methods=['POST'])
def insertar_cliente():
    cedula = request.form['cedula']
    nombre = request.form['nombre']        
    apellido = request.form['apellido']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    email = request.form['email']    
    try:
        insert_cliente(cedula, nombre, apellido, direccion, telefono, email)
        flash('Cliente insertado con exito')
    except Exception as e:        
        flash('Error en el Pedido, vuelva a intentaro y revise los datos.')
        print(e)
    return redirect(url_for('.Index'))

@cliente.route('/actualizar_cliente/<string:codi>', methods=['GET', 'POST'])
def actualizar_cliente(codi):
    if( request.method == 'GET'):
        data = select_cliente_for_codi(codi)
        return render_template('/cliente/editar.html', cliente=data)
    elif( request.method == 'POST'):
        cedula = request.form['cedula']
        nombre = request.form['nombre']        
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        email = request.form['email']    
        try:    
            update_cliente(codi, cedula, nombre, apellido, direccion, telefono, email)
            flash('Cliente editado con exito')
        except Exception as e:
            print(e)
        return redirect(url_for('.Index'))

@cliente.route('/eliminar_cliente/<string:codi>', methods=['POST', 'GET'])
def eliminar_cliente(codi:int):    
    try:
        delete_cliente(codi)
        flash('Cliente eliminado con exito')
    except Exception as e:
        flash('El Cliente esta enlazado con un Pedido. Elimine el pedido primero.')
        print(e)
    return redirect(url_for('.Index'))
    
@cliente.route('/reporte_cliente', methods=['GET'])
def generar_reporte_cli():
    print(BASE_DIR / "reports")    
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url("http://127.0.0.1:3000/cliente/", BASE_DIR / f"reports/cliente/out.pdf", configuration=config)
    return redirect(url_for('.Index'))
