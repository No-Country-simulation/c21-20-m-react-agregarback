from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
CORS(app)

# Header
class Producto:
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
        
        # Categories table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            descripcion TEXT
            );''')

        # Products table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            id_producto INT AUTO_INCREMENT PRIMARY KEY,
            id_vendedor INT NOT NULL,
            titulo VARCHAR(255) NOT NULL,
            descripcion TEXT,
            precio DECIMAL(10,2) NOT NULL,
            categoria INT NOT NULL,
            creado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            modificado_el TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (id_vendedor) REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
            FOREIGN KEY (categoria) REFERENCES categorias(id_categoria)
            );''')

        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    ## Manejo de usuarios
    def agregar_usuario(self, username, email, contraseña, rol):
        self.cursor.execute(f"SELECT * FROM usuarios WHERE username = %s AND email = %s", (username, email))

        usuario_existente = self.cursor.fetchone()
        if usuario_existente:
            return False
        
        sql = "INSERT INTO usuarios (username, email, contraseña, rol) VALUES (%s, %s, %s, %s)"
        valores = (username, email, contraseña, rol)

        self.cursor.execute(sql, valores)
        self.conn.commit()
        return True
    
    def consultar_usuario(self, username, email):
        self.cursor.execute(f"SELECT * FROM usuarios WHERE username = %s AND email = %s", (username, email))
        return self.cursor.fetchone()
# End Header

# Body
producto = Producto(host='localhost', user='root', password='', database='ecommerce')

@app.route("/ecommerce", methods=["POST"])
def agregar_usuario():
    username = request.form["username"]
    email = request.form["email"]
    contraseña = request.form["contraseña"]
    rol = request.form["rol"]

    usuario = producto.consultar_usuario(username, email)
    if not usuario:
        if producto.agregar_usuario(username, email, contraseña, rol):
            return jsonify({"mensaje": "Usuario registrado"}), 201
    else:
        return jsonify({"mensaje": "El usuario ya existe"}), 400

if __name__ == "__main__":
    app.run(debug=True)
# End Body