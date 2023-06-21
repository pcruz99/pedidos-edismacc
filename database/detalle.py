from inspect import _void
from connections.oracle_conn import conn_tienda, conn_caja1

CONNECTION_ORACLE = conn_tienda

def select_all_detalles() -> list:
    detalles = []
    cur = CONNECTION_ORACLE.cursor()
    cur.execute("select * from tienda.detalle")
    while True:
        row = cur.fetchone()
        if row is None:
            break        
        detalles.append(row)
    cur.close()
    return detalles

def select_detalle_for_codi(codi: int)-> tuple:
    detalle = []
    cur = CONNECTION_ORACLE.cursor()
    for row in cur.execute(f"select * from tienda.detalle where fk_codi_pedi = '{codi}'"):
        detalle.append(row)
        break
    cur.close()
    return detalle[0]

def insert_detalle(cantidad:int, fk_coid_celu:int, fk_codi_pedi:int) -> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.insertar_detalle',[cantidad, fk_coid_celu, fk_codi_pedi])
    cur.close()

def update_detalle(codi:int, cantidad:int, fk_coid_celu:int, fk_codi_pedi:int) -> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.actualizar_detalle',[codi, cantidad, fk_coid_celu, fk_codi_pedi])
    cur.close()

def delete_detalle(codi: int)-> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.eliminar_detalle',[codi])
    cur.close()