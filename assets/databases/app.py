from flask import Flask, request, jsonify
from flask import request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import time
from usuarios import Usuarios
from productos import Productos
from tiendas import Tiendas

app = Flask(__name__)
CORS(app)

# Usuarios
usuario = Usuarios(host="localhost", user="root", password="", database="ecommerce")

@app.route("/agregar-usuario", methods=["POST"])
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
    
@app.route("/iniciar-sesion", methods=["POST", "GET"])
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
    
# Productos
producto = Productos(host="localhost", user="root", password="", database="ecommerce")
ruta_destino = './static/imagenes/'

@app.route("/agregar-producto", methods=["POST"])
def agregar_producto():
    codigo = request.form["codigo"]
    nuevo_producto = request.form["producto"]
    precio = request.form["precio"]
    descripcion = request.form["descripcion"]
    categoria = request.form["categoria"]
    vendedor = request.form["vendedor"]
    imagen = request.files["imagen"]
    nombre_imagen = ""
    nombre_imagen = secure_filename(imagen.filename) 
    nombre_base, extension = os.path.splitext(nombre_imagen) 
    nombre_imagen = f"{nombre_base}_{int(time.time())}{extension}"
    nuevo_codigo = producto.agregar_producto(codigo, nuevo_producto, precio, descripcion, categoria, vendedor, nombre_imagen)

    if nuevo_codigo:
        path = os.path.join(ruta_destino, nombre_imagen)
        imagen.save(path)
        return jsonify({"mensaje": "Producto agregado"})
    else:
        return jsonify({"mensaje": "Producto ya existe"})

@app.route("/mostrar-productos", methods=["GET", "POST"])
def mostrar_productos():
    vendedor = request.form["vendedor"]
    productos = producto.mostrar_productos(vendedor)
    return jsonify(productos)

@app.route("/mostrar-all-productos", methods=["GET", "POST"])
def mostrar_all_productos():
    productos = producto.mostrar_all_productos()
    return jsonify(productos)

# Tiendas
# @app.route("/agregar-tienda", methods=["POST"])
# def agregar_tienda():
#     nomb

if __name__ == "__main__":
    app.run(debug=True)