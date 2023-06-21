from email.charset import BASE64
from flask import Blueprint, request, render_template, redirect, url_for, flash
from database import select_all_celulares, select_celular_for_codi, insert_celular, update_celular, delete_celular
import pdfkit
from pathlib import Path
import os

BASE_DIR = Path(os.path.join(os.path.dirname(__file__))).parent.parent

celular = Blueprint('celular', __name__, url_prefix='/celular')

@celular.route('/', methods=['GET'])
def Index():
    data = select_all_celulares()    
    return render_template('/celular/index.html', celulares=data)

@celular.route('/insertar_celular', methods=['POST'])
def insertar_celular():
    marca = request.form['marca']
    modelo = request.form['modelo']        
    color = request.form['color']
    camara = request.form['camara']
    pantalla = request.form['pantalla']
    cpu = request.form['cpu']
    ram = request.form['ram']
    almacenamiento = request.form['almacenamiento']
    precio = request.form['precio'] 
    try:
        insert_celular(marca, modelo, color, camara, pantalla, cpu, ram, almacenamiento, precio)
        flash('Celular insertado con exito')
    except Exception as e:        
        print(e)
    return redirect(url_for('.Index'))

@celular.route('/actualizar_celular/<string:codi>', methods=['GET', 'POST'])
def actualizar_celular(codi):
    if( request.method == 'GET'):
        data = select_celular_for_codi(codi)
        return render_template('/celular/editar.html', celular=data)
    elif( request.method == 'POST'):
        marca = request.form['marca']
        modelo = request.form['modelo']        
        color = request.form['color']
        camara = request.form['camara']
        pantalla = request.form['pantalla']
        cpu = request.form['cpu']
        ram = request.form['ram']
        almacenamiento = request.form['almacenamiento']
        precio = request.form['precio']    
        try:    
            update_celular(codi, marca, modelo, color, camara, pantalla, cpu, ram, almacenamiento, precio)
            flash('Celular editado con exito')
        except Exception as e:
            print(e)
        return redirect(url_for('.Index'))

@celular.route('/eliminar_celular/<string:codi>', methods=['POST', 'GET'])
def eliminar_celular(codi:int):    
    try:
        delete_celular(codi)
        flash('Celular eliminado con exito')
    except Exception as e:
        print(e)
        flash('El Celular esta enlazado con un Pedido. Elimine el pedido primero.')
    return redirect(url_for('.Index'))
    
@celular.route('/reporte_celular', methods=['GET'])
def generar_reporte_cel():
    print(BASE_DIR / "reports")    
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url("http://127.0.0.1:3000/celular/", BASE_DIR / f"reports/celular/out.pdf", configuration=config)
    return redirect(url_for('.Index'))
