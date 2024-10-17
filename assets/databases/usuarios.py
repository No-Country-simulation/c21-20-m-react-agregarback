from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
CORS(app)

# Header
class Usuarios:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err: 
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
                self.conn.database = database
            else:
                raise err
            
        # Create tables
        # Users Table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            contraseña VARCHAR(255) NOT NULL,
            rol ENUM('comprador', 'vendedor') NOT NULL,
            creado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modificado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            );''')

        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    ## Manejo de usuarios
    def agregar_usuario(self, username, email, contraseña, rol):
        # Verificamos si ya existe un usuario con el mismo turno
        self.cursor.execute(f"SELECT * FROM usuarios WHERE username = %s AND email = %s", (username, email))

        usuario_existente = self.cursor.fetchone()
        if usuario_existente:
            return False
        sql = "INSERT INTO usuarios (username, email, contraseña, rol) VALUES (%s, %s, %s, %s)"
        valores = (username, email, contraseña, rol)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True
    
    def leer_usuario(self):
        self.cursor.execute("SELECT * FROM usuarios")
        usuario = self.cursor.fetchall()
        return usuario
# End Header

# Body
usuario = Usuarios(host='localhost', user='root', password='', database='ecommerce')

@app.route("/ecommerce", methods=["POST"])
def agregar_usuario():
    username = request.form["username"]
    email = request.form["email"]
    contraseña = request.form["contraseña"]
    rol = request.form["rol"]

    if usuario.agregar_usuario(username, email, contraseña, rol):
        return jsonify({"mensaje": "Usuario registrado"}), 201
    else:
        return jsonify({"mensaje": "El usuario ya existe"}), 400

@app.route("/ecommerce", methods=["GET"])
def leer_usuario():
    usuarios = usuario.leer_usuario()
    return jsonify(usuarios)

# End Body
if __name__ == "__main__":
    app.run(debug=True)