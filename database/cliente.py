from inspect import _void
from connections.oracle_conn import conn_tienda

CONNECTION_ORACLE = conn_tienda

def select_all_clientes() -> list:
    clientes = []
    cur = CONNECTION_ORACLE.cursor()
    cur.execute("select * from tienda.cliente")
    while True:
        row = cur.fetchone()
        if row is None:
            break        
        clientes.append(row)
    cur.close()
    return clientes

def select_cliente_for_codi(codi: int)-> tuple:
    cliente = []
    cur = CONNECTION_ORACLE.cursor()
    for row in cur.execute("select * from tienda.cliente where codi_clie = :dept_id", [codi]):
        cliente.append(row)
        break
    cur.close()
    return cliente[0]

def select_cliente_codi_for_cedu_y_nomb(cedu: str, nomb:str)-> tuple:        
    cliente = []
    cur = CONNECTION_ORACLE.cursor()
    for row in cur.execute("select codi_clie from tienda.cliente where cedu_clie = :dept_cedu and nomb_clie = :dept_nomb", [cedu, nomb.capitalize()]):
        cliente.append(row)
        break
    cur.close()
    return cliente[0][0]

def insert_cliente(cedula: str, nomb: str, apell: str, dire: str, tele: str, email:str) -> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.insertar_cliente',[cedula, nomb, apell, dire, tele, email])
    cur.close()

def update_cliente(codi:int, cedula: str, nomb: str, apell: str, dire: str, tele: str, email:str) -> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.actualizar_cliente',[codi, cedula, nomb, apell, dire, tele, email])
    cur.close()

def delete_cliente(codi: int)-> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.eliminar_cliente',[codi])
    cur.close()
