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

@articulo.route('/articulo/<titulo>/<cproducto>', methods=['GET'])
def query_detalle_pedido_by_id(cpedido, cproducto):    
    result = q.get_detalle_pedido_by_id(cpedido, cproducto)
    return jsonify(result)
    

@articulo.route('/articulo/', methods=['POST'])
def insert_articulo():
    try:
        record = json.loads(request.data)

        titulo = record['titulo']

        tamano = record['tamaño']
        descripcion_corta = record['descripcion_corta']
        descripcion_larga = record['descripcion_larga']
        genero = record['genero']
        icono = record['icono']
        est = record['estadisticas']
        eje = record['ejecutable']
        esp = record['especificaciones']

        # Check values are valid
        if not isinstance(titulo, str) or not isinstance(tamano, str) or not isinstance(descripcion_corta, str)\
            or not isinstance(descripcion_larga,str) or not isinstance(genero,str):
            return jsonify({'error': 'invalid values'}), 400

        # Check if pedido exists
        pedido = q.consultar_articulo(titulo)
        if pedido is None:
            return jsonify({'error': 'articulo does not exist'}), 400

        # Check if producto exists
        stock = q.get_stock_by_id(cproducto)[1]
        if stock is None:
            return jsonify({'error': 'producto does not exist'}), 400

        result = q.get_detalle_pedido_by_id(cpedido, cproducto)
        return jsonify(result)

    except Exception as ex:
        logging.error("Error insering detalle pedido: ", ex)
        return jsonify({'error': 'error inserting detalle pedido'})


@articulo.route('/detalle_pedido/delete', methods=['POST'])
def delete_detalle_pedido():
    try:
        # Check if pedido exists
        record = json.loads(request.data)
        cproducto = record['cproducto']
        cpedido = record['cpedido']

        if cpedido is None or cproducto is None:
            return jsonify({'error': 'invalid values'}), 400

        pedido = q.get_pedido_by_id(cpedido)
        if pedido is None:
            return jsonify({'error': 'pedido does not exist'}), 400
        
        # Check if producto exists
        stock = q.get_stock_by_id(cproducto)[1]
        if stock is None:
            return jsonify({'error': 'producto does not exist'}), 400

        # Check if producto is in pedido
        detalle_pedido = q.get_detalle_pedido_by_id(cpedido, cproducto)
        if detalle_pedido is None:
            return jsonify({'error': 'producto is not in pedido'}), 400

        # Delete detalle pedido
        q.delete_detalle_pedido(cpedido, cproducto)

        result = jsonify({'message': 'detalle pedido deleted'})
        return result

    except Exception as ex:
        logging.error("Error deleting detalle pedido: ", ex)
        return jsonify({'error': 'error deleting detalle pedido'})
