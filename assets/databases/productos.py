import mysql.connector

class Productos:
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

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            codigo VARCHAR(255) NOT NULL PRIMARY KEY,
            producto VARCHAR(255) NOT NULL,
            precio VARCHAR(255) NOT NULL,
            descripcion VARCHAR(510) NOT NULL,
            categoria VARCHAR(255) NOT NULL,
            vendedor VARCHAR(255) NOT NULL,
            imagen VARCHAR(255) NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (vendedor) REFERENCES usuarios(username) ON DELETE CASCADE
        )''')
        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def mostrar_all_productos(self):
        self.cursor.execute(f"SELECT * FROM productos")
        respuesta = self.cursor.fetchall()
        return respuesta

    def consultar_producto(self, codigo):
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = '{codigo}'")
        return self.cursor.fetchone()

    def agregar_producto(self, codigo, producto, precio, descripcion, categoria, vendedor, imagen):
        self.consultar_producto(codigo)
        if self.consultar_producto(codigo):
            return False
        else:
            self.cursor.execute(f"INSERT INTO productos (codigo, producto, precio, descripcion, categoria, vendedor, imagen) VALUES ('{codigo}', '{producto}', '{precio}', '{descripcion}', '{categoria}', '{vendedor}', '{imagen}')")
            self.conn.commit()
            return True

    def mostrar_productos(self, vendedor):
        self.cursor.execute(f"SELECT * FROM productos WHERE vendedor = '{vendedor}'")
        return self.cursor.fetchall()

    def editar_producto(self, codigo, producto, precio, descripcion, categoria, imagen):
        sql = f"UPDATE productos SET producto = '{producto}', precio = '{precio}', descripcion = '{descripcion}', categoria = '{categoria}', imagen = '{imagen}' WHERE codigo = '{codigo}'"
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.rowcount > 0
    
    def borrar_producto(self, codigo):
        self.cursor.execute(f"DELETE FROM productos WHERE productos.codigo = '{codigo}'")
        self.conn.commit()
        return self.cursor.rowcount > 0