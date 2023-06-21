import cx_Oracle

userpwd_tienda = "tienda" # Obtain password string from a user prompt or environment variable
userpwd_caja1 = "caja1" # Obtain password string from a user prompt or environment variable
userpwd_caja2 = "caja2" # Obtain password string from a user prompt or environment variable

conn_tienda = cx_Oracle.connect(user="tienda", password=userpwd_tienda,
                                                        dsn="DESKTOP-J8NS19L",
                                                        encoding="UTF-8")

conn_caja1 = cx_Oracle.connect(user="caja1", password=userpwd_caja1,
                                                    dsn="DESKTOP-J8NS19L",
                                                    encoding="UTF-8")

conn_caja2 = cx_Oracle.connect(user="caja2", password=userpwd_caja2,
                                                    dsn="DESKTOP-J8NS19L",
                                                    encoding="UTF-8")

class Connection:        
    @staticmethod
    def getConn(username:str):            
        conns = {"tienda": conn_tienda, "caja1": conn_caja1, "caja2": conn_caja2}
        return conns[username]

    
