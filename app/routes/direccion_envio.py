from flask import Blueprint, request, render_template, redirect, url_for, flash
from database import (
    direccion_envio,
    select_all_direccion_envio,
    select_direccion_envio_for_codi,
    insert_direccion_envio,
    update_direccion_envio,
    delete_direccion_envio
)
import pdfkit
from pathlib import Path
import os

BASE_DIR = Path(os.path.join(os.path.dirname(__file__))).parent.parent

direccion_envio = Blueprint('direccion_envio', __name__, url_prefix='/direccion_envio')

@direccion_envio.route('/', methods=['GET'])
def Index():
    data = select_all_direccion_envio()   
    return render_template('/direccion_envio/index.html', direcciones_envio=data)

@direccion_envio.route('/insertar_direccion_envio', methods=['POST'])
def insertar_direccion_envio():
    calle_pri = request.form['calle_pri']
    calle_sec = request.form['calle_sec']        
    nume_depa = request.form['nume_depa']
    referencia = request.form['referencia']
    ciudad = request.form['ciudad']
    provincia = request.form['provincia']
    codi_postal = request.form['codi_postal']    
    try:
        insert_direccion_envio(calle_pri, calle_sec, nume_depa, referencia, ciudad, provincia, codi_postal)
        flash('Direccion de Envio insertado con exito')
    except Exception as e:                
        print(e)
    return redirect(url_for('.Index'))

@direccion_envio.route('/actualizar_direccion_envio/<string:codi>', methods=['GET', 'POST'])
def actualizar_direccion_envio(codi):
    if( request.method == 'GET'):
        data = select_direccion_envio_for_codi(codi)
        return render_template('/direccion_envio/editar.html', direccion_envio=data)
    elif( request.method == 'POST'):
        calle_pri = request.form['calle_pri']
        calle_sec = request.form['calle_sec']        
        nume_depa = request.form['nume_depa']
        referencia = request.form['referencia']
        ciudad = request.form['ciudad']
        provincia = request.form['provincia']
        codi_postal = request.form['codi_postal']           
        try:    
            update_direccion_envio(codi, calle_pri, calle_sec, nume_depa, referencia, ciudad, provincia, codi_postal)
            flash('Direccion de Envio editado con exito')
        except Exception as e:
            print(e)
        return redirect(url_for('.Index'))

@direccion_envio.route('/eliminar_direccion_envio/<string:codi>', methods=['POST', 'GET'])
def eliminar_direccion_envio(codi:int):    
    try:
        delete_direccion_envio(codi)
        flash('Direccion de Envio eliminado con exito')
    except Exception as e:
        flash('La Direccion de Envio esta enlazado con un Pedido. Elimine el pedido primero.')
        print(e)
    return redirect(url_for('.Index'))

@direccion_envio.route('/reporte_direccion_envio', methods=['GET'])
def generar_reporte_die():
    print(BASE_DIR / "reports")    
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url("http://127.0.0.1:3000/direccion_envio/", BASE_DIR / f"reports/direccion_envio/out.pdf", configuration=config)
    return redirect(url_for('.Index'))
