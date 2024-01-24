import json
import logging
import app.query.tienda as query_tienda
import app.query.social as query_social
import app.query.articulo as query_articulo

import app.database as database
from flask import Blueprint, jsonify, request

tienda = Blueprint('tienda', __name__)
db = database.database()
q = query_tienda.tienda(db)
query_social = query_social.social(db)
q_articulo = query_articulo.articulo(db)

#Publicar videojuego
@tienda.route('/tienda/', methods=['POST'])
def insert_videojuego():
  record = json.loads(request.data)
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
  
  result2 = q_articulo.subir_articulo(titulo_videojuego, tamaño, descripcion_corta, descripcion_larga, genero, icono, ruta_ejecutable, especificaciones)
  if(result2 == False):
    return jsonify("El articulo ya existe", False)
  else:
    result = q.insert_videojuego(titulo_videojuego, precio, version, nombre_usuario, genero)
    return jsonify(result)


#Eliminar videojuego
@tienda.route('/tienda/', methods=['DELETE'])
def delete_videojuego():
  record = json.loads(request.data)
  cvideojuego = record['titulo']
  creador = record['creador']
  result = q.delete_videojuego(cvideojuego,creador)
  return jsonify(result)

#Actualizar version de un videojuego
@tienda.route('/tienda/update-version/<cvideojuego>', methods=['POST'])
def update_videojuego(cvideojuego):
  record = json.loads(request.data)
  version = record['version']
  result = q.update_version_videojuego(cvideojuego, version)
  return jsonify(result)

@tienda.route("/tienda/<genero>", methods=['GET'])
def query_tienda(genero):
    videojuegos = q.get_videojuego_por_genero(genero)

    # Crear un diccionario para mapear los videojuegos con sus artículos
    resultado_final = []
    for videojuego in videojuegos:
        # Suponiendo que cada videojuego tiene un identificador único
        nombre_videojuego = videojuego[0]
        articulo_correspondiente =  q_articulo.consultar_articulo(nombre_videojuego)
        
        videojuego_lista = list(videojuego)
        
        # Añadir el artículo al videojuego
        videojuego_lista.append(articulo_correspondiente[0][1])
        videojuego_lista.append(articulo_correspondiente[0][2])
        videojuego_lista.append(articulo_correspondiente[0][3])
        videojuego_lista.append(articulo_correspondiente[0][5])
        videojuego_lista.append(articulo_correspondiente[0][7])
        
            
        resultado_final.append(videojuego_lista)

    return jsonify(resultado_final)


#Comprar un videojuego
@tienda.route('/tienda/comprar/<cvideojuego>', methods=['POST'])
def comprar_videojuego(cvideojuego):
  record = json.loads(request.data)
  nombre_usuario = record['nombre_usuario']
  result = q.comprar_videojuego(cvideojuego, nombre_usuario)
  if(result[1] == True):
    q_articulo.anadir_articulo_obtenido(nombre_usuario, cvideojuego)
  return jsonify(result)

#Añadir saldo a un usuario
@tienda.route('/tienda/add-saldo/<cusuario>', methods=['POST'])
def add_saldo(cusuario):
  record = json.loads(request.data)
  saldo = record['saldo']
  result2 = query_social.update_saldo(cusuario, saldo)
  result = query_social.get_saldo_by_id(cusuario)
  return jsonify(result)