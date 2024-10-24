import mysql.connector

class Usuarios:
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

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            username VARCHAR(255) NOT NULL PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            contraseña VARCHAR(255) NOT NULL,
            creado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modificado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )''')
        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    def consultar_usuario(self, username):
        self.cursor.execute(f"SELECT * FROM usuarios WHERE username = '{username}'")
        return self.cursor.fetchone()

    def consultar_email(self, email):
        self.cursor.execute(f"SELECT * FROM usuarios WHERE email = '{email}'")
        return self.cursor.fetchone()

    def agregar_usuario(self, username, email, contraseña):
        self.consultar_usuario(username)
        self.consultar_email(email)
        if self.consultar_usuario(username):
            return "usuario existente"
        elif self.consultar_email(email):
            return "mail existente"
        else:
            sql = f"INSERT INTO usuarios (username, email, contraseña) VALUES ('{username}', '{email}', '{contraseña}')"
            self.cursor.execute(sql)
            self.conn.commit()
            return True
        
    def iniciar_sesion(self, username, contraseña):
        self.consultar_usuario(username)
        if self.consultar_usuario(username):
            self.cursor.execute(f"SELECT * FROM usuarios WHERE username = '{username}' AND contraseña = '{contraseña}'")
            validar_contraseña = self.cursor.fetchone()
            if validar_contraseña:
                return True
            else:
                return "contraseña incorrecta"
        else:
            return "usuario inexistente"