from connections.oracle_conn import conn_tienda

CONNECTION_ORACLE = conn_tienda

def select_user(username:str) -> tuple:
    usuario = []
    cur = CONNECTION_ORACLE.cursor()    
    for row in cur.execute(f"select * from tienda.auth where username=:dept_username", [username]):
        usuario.append(row)        
        break
    cur.close()
    return usuario[0]
    