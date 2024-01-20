import json
import logging
import app.query.articulo as query
import app.database as database
from flask import Flask, request, jsonify, Blueprint

detalle_pedido = Blueprint('detalle_pedido', __name__)
db = database.database()
q = query.articulo(db)


@detalle_pedido.route('/detalle_pedido/', methods=['GET'])
def query_detalle_pedido():
    result = q.get_detalle_pedido()
    return jsonify(result)

@detalle_pedido.route('/detalle_pedido/<cpedido>/<cproducto>', methods=['GET'])
def query_detalle_pedido_by_id(cpedido, cproducto):    
    result = q.get_detalle_pedido_by_id(cpedido, cproducto)
    return jsonify(result)
    

@detalle_pedido.route('/detalle_pedido/', methods=['POST'])
def insert_detalle_pedido():
    try:
        record = json.loads(request.data)

        cproducto = record['cproducto']

        cpedido = record['cpedido']
        cantidad = record['cantidad']

        # Check values are valid
        if not isinstance(cpedido, int) or not isinstance(cproducto, int) or not isinstance(cantidad, int):
            return jsonify({'error': 'invalid values'}), 400

        # Check if pedido exists
        pedido = q.get_pedido_by_id(cpedido)
        if pedido is None:
            return jsonify({'error': 'pedido does not exist'}), 400

        # Check if producto exists
        stock = q.get_stock_by_id(cproducto)[1]
        if stock is None:
            return jsonify({'error': 'producto does not exist'}), 400

        # Check if stock is in stock
        if cantidad < 0:
            return jsonify({'error': 'invalid value cantidad'}), 400

        if stock - cantidad < 0:
            return jsonify({'error': 'cantidad to update is greater than stock'}), 400

        # Check if producto is already in pedido
        detalle_pedido = q.get_detalle_pedido_by_id(cproducto, cpedido)
        if detalle_pedido is not None:
            return jsonify({'error': 'producto already in pedido'}), 400

        # Insert detalle pedido and update stock
        q.insert_detalle_pedido(cpedido, cproducto, cantidad)
        q.update_stock(cproducto, cantidad)

        result = q.get_detalle_pedido_by_id(cpedido, cproducto)
        return jsonify(result)

    except Exception as ex:
        logging.error("Error insering detalle pedido: ", ex)
        return jsonify({'error': 'error inserting detalle pedido'})


@detalle_pedido.route('/detalle_pedido/delete', methods=['POST'])
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
