from datetime import datetime
from time import sleep
from flask import Blueprint, request, render_template, redirect, url_for, flash
from database import (
    select_all_celulares,
    select_all_pedidos,
    select_pedido_for_codi,
    select_detalle_for_codi_pedi,
    update_pedido,
    update_detalle,
    delete_detalle,
    delete_pedido,
    select_cliente_codi_for_cedu_y_nomb,
    select_direccion_envio_codi_for_clpr_y_refe,
    select_pedido_codi_for_clie_y_dien,
    insert_cliente,
    insert_direccion_envio,
    insert_pedido,
    insert_detalle,
    calcular_subtotal_producto,
    calcular_iva,
)
import pdfkit
from pathlib import Path
import os

BASE_DIR = Path(os.path.join(os.path.dirname(__file__))).parent.parent

pedido = Blueprint("pedido", __name__, url_prefix="/pedido")


@pedido.route("/", methods=["GET"])
def Index():
    data = select_all_pedidos()
    return render_template("/pedido/index.html", pedidos=data)


@pedido.route("/insertar_pedido", methods=["GET", "POST"])
def insertar_pedido():
    data = select_all_celulares()

    if request.method == "GET":
        return render_template("/pedido/ingresar.html", celulares=data)
    elif request.method == "POST":
        # Datos del cliente
        cedula = request.form["cedula"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        # Datos de la direccion de envio
        calle_pri = request.form["calle_pri"]
        calle_sec = request.form["calle_sec"]
        nume_depa = request.form["nume_depa"]
        referencia = request.form["referencia"]
        ciudad = request.form["ciudad"]
        provincia = request.form["provincia"]
        codi_postal = request.form["codi_postal"]
        # Datos del Pedido
        total_pedi = 0
        subtotal_por_produ = []
        cantidadTemp = {}
        fecha_pedi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        selected_celu = request.form.getlist("celulares")
        observa = request.form["observa"]
        # Celulares selccionados y cantidad
        for celu in selected_celu:
            comodin = f"celular_{celu}"
            cantidad = request.form[comodin]
            cantidadTemp[celu] = cantidad
            for c in data:
                if c[0] == int(celu):
                    total_pedi = (c[9] * int(cantidad)) + total_pedi
                    subtotal_por_produ.append(
                        calcular_subtotal_producto(int(cantidad), c[9])
                    )
                    break
        try:
            iva = calcular_iva(total_pedi, 12)
            #===========================================================
            insert_cliente(cedula, nombre, apellido, direccion, telefono, email)
            insert_direccion_envio(
                calle_pri,
                calle_sec,
                nume_depa,
                referencia,
                ciudad,
                provincia,
                codi_postal,
            )
            codi_clie = select_cliente_codi_for_cedu_y_nomb(cedula, nombre)            
            codi_dien = select_direccion_envio_codi_for_clpr_y_refe(
                calle_pri, referencia
            )            
            insert_pedido(fecha_pedi, total_pedi, observa, codi_clie, codi_dien)            
            codi_pedi = select_pedido_codi_for_clie_y_dien(codi_clie, codi_dien)                                    
            sleep(0.5)
            for celu, canti in cantidadTemp.items():
                insert_detalle(canti, celu, codi_pedi)
            #===========================================================

            flash("Pedido realizado con exito")
            flash(f"El valor a pagar es de ${total_pedi}")
        except Exception as e:
            print(e)
        return render_template(
            "/pedido/resumen.html",
            subtotales=subtotal_por_produ,
            total=total_pedi,
            iva=iva,
        )

@pedido.route("/actualizar_pedido/<string:codi>", methods=["GET", "POST"])
def actualizar_pedido(codi):
    if request.method == "GET":
        data1 = select_pedido_for_codi(codi)
        data2 = select_detalle_for_codi_pedi(codi)
        return render_template("/pedido/editar.html", pedido=data1, detalle=data2)
    elif request.method == "POST":
        codes = select_detalle_for_codi_pedi(codi)
        fecha_pedido = request.form["fecha_pedido"]
        observ = request.form["observ"]
        total_pedido = 0
        for code in codes:
            comodin = f"celular_{code[6]}"
            cantidad = request.form[comodin]
            total_pedido = total_pedido + (int(cantidad) * code[5])
            try:
                update_detalle(code[1], cantidad, code[6], code[0])
            except Exception as e:
                print(e)
        try:
            update_pedido(
                codi, fecha_pedido, total_pedido, observ, codes[0][7], codes[0][8]
            )
            flash("Pedido editado con exito")
        except Exception as e:
            print(e)
        return redirect(url_for(".Index"))


@pedido.route("/eliminar_pedido/<string:codi>", methods=["POST", "GET"])
def eliminar_pedido(codi: int):
    codes = select_detalle_for_codi_pedi(codi)
    try:
        for code in codes:
            delete_detalle(code[1])
        delete_pedido(codi)
        flash("Pedido eliminado con exito")
    except Exception as e:
        print(e)
    return redirect(url_for(".Index"))


@pedido.route("/eliminar_detalle/<string:codi>", methods=["POST", "GET"])
def eliminar_detalle(codi: int):
    try:
        delete_detalle(codi)
        flash("Celular eliminado con exito")
    except Exception as e:
        print(e)
    return redirect(url_for(".Index"))

@pedido.route('/reporte_pedido', methods=['GET'])
def generar_reporte_ped():
    print(BASE_DIR / "reports")    
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_url("http://127.0.0.1:3000/pedido/", BASE_DIR / f"reports/pedido/out.pdf", configuration=config)
    return redirect(url_for('.Index'))