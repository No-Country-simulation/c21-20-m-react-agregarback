from flask import Flask, request, jsonify
from flask import request
from flask_cors import CORS
import mysql.connector
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
CORS(app)

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
            sql = "INSERT INTO usuarios (username, email, contraseña) VALUES (%s, %s, %s)"
            valores = (username, email, contraseña)
            self.cursor.execute(sql, valores)
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


usuario = Usuarios(host="localhost", user="root", password="", database="ecommerce")

@app.route("/ecommerce", methods=["POST"])
def agregar_usuario():
    username = request.form["username"]
    email = request.form["email"]
    contraseña = request.form["contraseña"]

    validar_usuario = usuario.agregar_usuario(username, email, contraseña)
    if validar_usuario == "usuario existente":
        return jsonify({"mensaje": "El usuario ya existe"})
    elif validar_usuario == "mail existente":
        return jsonify({"mensaje": "El email ya existe"})
    else:
        return jsonify({"mensaje": "Usuario registrado"})
    
@app.route("/usuarios", methods=["POST", "GET"])
def iniciar_sesion():
    _username = request.form["username"]
    _contraseña = request.form["contraseña"]
    login = usuario.iniciar_sesion(_username, _contraseña)
    if login == "usuario inexistente":
        return jsonify({"mensaje": "El usuario no está registrado"})
    elif login == "contraseña incorrecta":
        return jsonify({"mensaje":"La contraseña es incorrecta"})
    else:
        return jsonify({"mensaje": "Bienvenido"})
    
if __name__ == "__main__":
    app.run(debug=True)