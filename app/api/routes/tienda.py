import json
import logging
import app.query.tienda as query_tienda
import app.query.articulo as query_articulo

import app.database as database
from flask import Blueprint, jsonify, request

tienda = Blueprint('tienda', __name__)
db = database.database()
q = query_tienda.tienda(db)
q_articulo = query_articulo.articulo(db)

#Publicar videojuego
@tienda.route('/tienda/', methods=['POST'])
def insert_videojuego():
  titulo_videojuego = record['titulo_videojuego']
  precio = record['precio']
  version = record['version']
  nombre_usuario = record['nombre_usuario']
  descripcion_corta = record['descripcion_corta']
  descripcion_larga = record['descripcion_larga']
  genero = record['genero']
  icono = record['icono']
  tamaño = record['tamaño']
  ruta_ejecutable = record['ruta_ejecutable']
  especificaciones = record['especificaciones']
  
  result = q.insert_videojuego(titulo_videojuego, precio, version, nombre_usuario, genero)
  result2 = q_articulo.subir_articulo(titulo_videojuego, tamaño, descripcion_corta, descripcion_larga, genero, icono, ruta_ejecutable, especificaciones)
  return jsonify(result)


#Eliminar videojuego
@tienda.route('/tienda/<cvideojuego>', methods=['DELETE'])
def delete_videojuego(cvideojuego):
  result = q.delete_videojuego(cvideojuego)
  return jsonify(result)

#Actualizar version de un videojuego
@tienda.route('/tienda/update-version/<cvideojuego>', methods=['POST'])
def update_videojuego(cvideojuego):
  version = record['version']
  result = q.update_version_videojuego(cvideojuego, version)
  return jsonify(result)

#Obtener los videojuegos de un genero
@tienda.route("/tienda/<genero>", methods=['GET'])
def query_tienda(genero):
  result = q.get_videojuego_por_genero(genero)
  return jsonify(result)

#Comprar un videojuego
@tienda.route('/tienda/comprar/<cvideojuego>', methods=['POST'])
def comprar_videojuego(cvideojuego):
  nombre_usuario = record['nombre_usuario']
  result = q.comprar_videojuego(cvideojuego, nombre_usuario)
  result2 = q_articulo.anadir_articulo_obtenido(nombre_usuario, cvideojuego)
  return jsonify(result)

#Añadir saldo a un usuario
@tienda.route('/tienda/add-saldo/<cusuario>', methods=['POST'])
def add_saldo(cusuario):
  saldo = record['saldo']
  result = q.add_saldo(cusuario, saldo)
  return jsonify(result)