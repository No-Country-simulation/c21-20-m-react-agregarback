from flask import Flask, request, jsonify
from flask import request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import time
from usuarios import Usuarios
from productos import Productos

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
    imagen = request.form["imagen"]
    
    nuevo_codigo = producto.agregar_producto(codigo, nuevo_producto, precio, descripcion, categoria, vendedor, imagen)

    if nuevo_codigo:
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

@app.route("/mostrar-producto", methods=["GET", "POST"])
def mostrar_producto():
    codigo = request.form["codigo"]
    ver_producto = producto.consultar_producto(codigo)
    return jsonify(ver_producto)

@app.route("/editar-producto", methods=["PUT"])
def editar_producto():
    codigo = request.form["codigo"]
    product = request.form["producto"]
    precio = request.form["precio"]
    descripcion = request.form["descripcion"]
    categoria = request.form["categoria"]
    imagen = request.form["imagen"]

    editar_producto = producto.editar_producto(codigo, product, precio, descripcion, categoria, imagen)

    if editar_producto:
        return jsonify({"mensaje": "Producto modificado"}), 200
    else:
        return jsonify({"mensaje": "Producto no encontrado"}), 403
    
@app.route("/eliminar-producto", methods=["DELETE"])
def eliminar_producto():
    codigo = request.form["codigo"]
    borrar_producto = producto.borrar_producto(codigo)
    if borrar_producto:
        return jsonify({"mensaje": "Producto eliminado"}), 200
    else:
        return jsonify({"mensaje": "Error al eliminar el producto"}), 500


if __name__ == "__main__":
    app.run(debug=True)