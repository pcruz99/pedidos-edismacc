from inspect import _void
from connections.oracle_conn import conn_tienda

CONNECTION_ORACLE = conn_tienda

def select_all_direccion_envio() -> list:
    direcciones_envio = []
    cur = CONNECTION_ORACLE.cursor()
    cur.execute("select * from tienda.direccion_envio")
    while True:
        row = cur.fetchone()
        if row is None:
            break        
        direcciones_envio.append(row)
    cur.close()
    return direcciones_envio

def select_direccion_envio_for_codi(codi: int)-> tuple:
    direccion_envio = []
    cur = CONNECTION_ORACLE.cursor()
    for row in cur.execute(f"select * from tienda.direccion_envio where codi_dien = '{codi}'"):
        direccion_envio.append(row)
        break
    cur.close()
    return direccion_envio[0]

def select_direccion_envio_codi_for_clpr_y_refe(callpr:str, refe:str)-> tuple:
    direccion_envio = []
    cur = CONNECTION_ORACLE.cursor()
    for row in cur.execute("select codi_dien from tienda.direccion_envio where capr_dien = :dept_capr and refe_dien = :dept_refe", [callpr ,refe]):
        direccion_envio.append(row)
        break
    cur.close()
    return direccion_envio[0][0]

def insert_direccion_envio(calle_prin:str, calle_secu:str, nume_depa:int, refere:str, ciudad:str, provi:str, codi_post:str) -> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.insertar_direccion_envio',[calle_prin, calle_secu, nume_depa, refere, ciudad, provi, codi_post])
    cur.close()

def update_direccion_envio(codi:int, calle_prin:str, calle_secu:str, nume_depa:int, refere:str, ciudad:str, provi:str, codi_post:str) -> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.actualizar_direccion_envio',[codi, calle_prin, calle_secu, nume_depa, refere, ciudad, provi, codi_post])
    cur.close()

def delete_direccion_envio(codi: int)-> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.eliminar_direccion_envio',[codi])
    cur.close()
