import mysql.connector

class Tiendas:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database
            else:
                raise err

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tiendas (
            nombre VARCHAR(255) NOT NULL PRIMARY KEY,
            imagen VARCHAR(255) NOT NULL,
            vendedor VARCHAR(255) NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (vendedor) REFERENCES usuarios(username) ON DELETE CASCADE
        )''')
        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def consultar_tienda(self, nombre):
        self.cursor.execute(f"SELECT * FROM tiendas WHERE nombre = '{nombre}'")
        return self.cursor.fetchone()
    
    def agregar_tienda(self, nombre, imagen, vendedor):
        self.consultar_tienda(nombre)
        if self.consultar_tienda(nombre):
            return False
        else:
            self.cursor.execute(f"INSERT INTO tiendas (nombre, imagen, vendedor) VALUES ('{nombre}', '{imagen}', '{vendedor}')")
            self.conn.commit()
            return True
        
    def editar_tienda(self, nombre, imagen, vendedor):
        self.consultar_tienda(nombre)
        if self.consultar_tienda(nombre):
            return False
        else:
            self.cursor.execute(f"UPDATE tiendas SET nombre = '{nombre}', imagen = '{imagen}', vendedor = '{vendedor}' WHERE nombre = '{nombre}'")
            return True