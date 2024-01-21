import json
import logging
import app.query.articulo as query
import app.database as database
from flask import Flask, request, jsonify, Blueprint

articulo = Blueprint('articulo', __name__)
db = database.database()
q = query.articulo(db)


@articulo.route('/articulo/<titulo>', methods=['GET'])
def query_articulo(titulo):
    result = q.consultar_articulo(titulo)
    return jsonify(result)

@articulo.route('/articulo/', methods=['POST'])
def insert_articulo():
    try:
        record = json.loads(request.data)

        titulo = record['titulo']

        tamano = record['tamaño']
        desc = record['descripcion_corta']
        desl = record['descripcion_larga']
        genero = record['genero']
        icono = record['icono']
        eje = record['ejecutable']
        esp = record['especificaciones']

        # Check values are valid
        if not isinstance(titulo, str) or not isinstance(tamano, str) or not isinstance(desc, str) or not isinstance(desl,str) or not isinstance(genero,str) or not isinstance(icono,str) or not isinstance(eje,str) or not isinstance(esp,str):
            return jsonify({'error': 'articulo invalid values'}), 400
        
        articulo = q.consultar_articulo(titulo)
        if articulo is None:
            return jsonify({'error': 'articulo does not exist'}), 400
        
        q.subir_articulo(titulo,tamano,desc,desl,genero,icono,eje,esp)
        
        return jsonify({'mensaje':'Articulo subido exitosamente'})
        
    except Exception as ex:
        logging.error("Error inserting Articulo: ", ex)
        return jsonify({'error': 'error inserting Articulo'})
    

@articulo.route('/articulo/delete', methods=['POST'])
def delete_articulo():
    try:
        # Check if pedido exists
        record = json.loads(request.data)
        titulo = record['titulo']

        if titulo is None:
            return jsonify({'error': 'invalid titulo'}), 400

        articulo = q.consultar_articulo(titulo)
        if articulo is None:
            return jsonify({'error': 'articulo does not exist'}), 400

        # Delete articulo
        q.eliminar_articulo(titulo)
        result = jsonify({'message': 'Articulo deleted'})
        return result

    except Exception as ex:
        logging.error("Error deleting articulo: ", ex)
        return jsonify({'error': 'error deleting articulo'})