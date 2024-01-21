import json
import logging
import app.query.articulo as query
import app.database as database
from flask import Flask, request, jsonify, Blueprint

articulo_obtenido = Blueprint('articulo_obtenido', __name__)
db = database.database()
q = query.articulo(db)

@articulo_obtenido.route('/articulo_obtenido/<nombre_usuario>', methods=['GET'])
def query_articulos_by_nombre(nombre_usuario,n):
    #Pasar numero de consultas n
    n=4
    result = q.consultar_articulos(nombre_usuario,n)
    return jsonify(result)

@articulo_obtenido.route('/articulo_obtenido/<nombre_usuario>/<titulo>', methods=['GET'])
def query_articulos(nombre_usuario,titulo):
        
    record = json.loads(request.data)
    titulo = record['titulo']
    nombre_usuario = record['nombre_usuario']

    result = q.consultar_articulo_obtenido(nombre_usuario,titulo)
    return jsonify(result)

@articulo_obtenido.route('/articulo_obtenido/', methods=['POST'])
def insert_articulo_obtenido():
    try:
        record = json.loads(request.data)

        titulo = record['titulo']
        user = record['nombre_usuario']

        # Check values are valid
        if not isinstance(titulo, str) or not isinstance(user, str):
            return jsonify({'error': 'articulo invalid values'}), 400
        
        q.anadir_articulo_obtenido(user,titulo)

        return jsonify({'mensaje':'Articulo obtenido exitosamente'})
        
    except Exception as ex:
        logging.error("Error inserting Articulo obtenido: ", ex)
        return jsonify({'error': 'error inserting Articulo obtenido'})
    

@articulo_obtenido.route('/articulo_obtenido/delete', methods=['POST'])
def delete_articulo_obtenido():
    try:
        # Check if pedido exists
        record = json.loads(request.data)
        titulo = record['titulo']
        user = record['nombre_usuario']

        if user is None:
            return jsonify({'error':'invalid user'}), 400

        if titulo is None:
            return jsonify({'error': 'invalid titulo'}), 400

        articulo = q.consultar_articulo_obtenido(user,titulo)
        if articulo is None:
            return jsonify({'error': 'articulo obtenido does not exist'}), 400

        # Delete articulo
        q.eliminar_articulo_obtenido(user,titulo)
        result = jsonify({'message': 'Articulo_obtenido deleted'})
        return result

    except Exception as ex:
        logging.error("Error deleting articulo: ", ex)
        return jsonify({'error': 'error deleting articulo'})
