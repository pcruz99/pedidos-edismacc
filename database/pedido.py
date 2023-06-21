from inspect import _void
from connections.oracle_conn import conn_tienda

CONNECTION_ORACLE = conn_tienda

def select_all_pedidos() -> list:
    
    pedidos = []
    cur = CONNECTION_ORACLE.cursor()
    cur.execute("select * from tienda.pedido_detail order by codi_pedi asc")
    while True:
        row = cur.fetchone()
        if row is None:
            break        
        pedidos.append(row)
    cur.close()    
    return pedidos

def select_pedido_for_codi(codi: int)-> tuple:
    pedido = []
    cur = CONNECTION_ORACLE.cursor()
    for row in cur.execute(f"select * from tienda.pedido where codi_pedi = '{codi}'"):
        pedido.append(row)
        break
    cur.close()
    return pedido[0]

def select_pedido_codi_for_clie_y_dien(codi_clie: int, codi_dien: int)-> tuple:
    pedido = []
    cur = CONNECTION_ORACLE.cursor()
    for row in cur.execute("select codi_pedi from tienda.pedido where fk_codi_clie = :dept_clie and fk_codi_dien = :dept_dien", [codi_clie, codi_dien]):
        pedido.append(row)
        break
    cur.close()
    return pedido[0][0]

def select_detalle_for_codi_pedi(codi: int)-> tuple:
    data = []
    cur = CONNECTION_ORACLE.cursor()
    for row in cur.execute(f"select * from tienda.pedido_detail_get_celulares where codi_pedi = '{codi}'"):
        data.append(row)
    cur.close()
    return data

def insert_pedido(fecha:str, tota:float, obser:str, fk_coid_clie:int, fk_codi_dien:int) -> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.insertar_pedido',[fecha, tota, obser, fk_coid_clie, fk_codi_dien])
    cur.close()

def update_pedido(codi:int, fecha:str, tota:float, obser:str, fk_codi_clie:int, fk_codi_dien:int) -> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.actualizar_pedido',[codi, fecha, tota, obser, fk_codi_clie, fk_codi_dien])
    cur.close()

def delete_pedido(codi: int)-> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.eliminar_pedido',[codi])
    cur.close()

def calcular_subtotal_producto(cantidad:int, precio_unitario:float):
    cur = CONNECTION_ORACLE.cursor()    
    subtotal = cur.callfunc('tienda.calcular_subtotal_producto', float, [cantidad, precio_unitario])
    cur.close()
    return subtotal

def calcular_iva(total:float, porcentaje:int):
    cur = CONNECTION_ORACLE.cursor()    
    iva = cur.callfunc('tienda.calcular_iva', float, [total, porcentaje])
    cur.close()
    return iva