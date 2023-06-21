from inspect import _void
from connections.oracle_conn import conn_tienda

CONNECTION_ORACLE = conn_tienda

def select_all_celulares() -> list:    
    celulares = []
    cur = CONNECTION_ORACLE.cursor()
    cur.execute("select * from tienda.celular")
    while True:
        row = cur.fetchone()
        if row is None:
            break        
        celulares.append(row)
    cur.close()
    return celulares

def select_celular_for_codi(codi: int)-> tuple:
    celular = []
    cur = CONNECTION_ORACLE.cursor()
    for row in cur.execute(f"select * from tienda.celular where codi_celu = '{codi}'"):
        celular.append(row)
        break
    cur.close()
    return celular[0]

def insert_celular(marc: str, modelo: str, color: str, camara: str, pantalla: str, proce: str, ram: int, almace: int, precio: float) -> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.insertar_celular',[marc, modelo, color, camara, pantalla, proce, ram, almace, precio])
    cur.close()

def update_celular(codi:int, marc: str, modelo: str, color: str, camara: str, pantalla: str, proce: str, ram: int, almace: int, precio: float) -> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.actualizar_celular',[codi, marc, modelo, color, camara, pantalla, proce, ram, almace, precio])
    cur.close()

def delete_celular(codi: int)-> _void:
    cur = CONNECTION_ORACLE.cursor()    
    cur.callproc('tienda.eliminar_celular',[codi])
    cur.close()

# insertar_celular('Samsung', 's21+', 'Negro', '64mpx', 'AMOLED', 'Qualcom', 8, 128, 600.4)
# print(select_all_celulares())
# print(select_celular_for_codi(2))