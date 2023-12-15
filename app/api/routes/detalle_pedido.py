import json
import app.query as query
import app.database as database
from flask import Flask, request, jsonify, Blueprint

detalle_pedido = Blueprint('detalle_pedido', __name__)
db = database.database()
q = query.query(db)


@detalle_pedido.route('/detalle_pedido/', methods=['GET'])
def query_detalle_pedido():
    result = q.get_detalle_pedido()
    return jsonify(result)

@detalle_pedido.route('/detalle_pedido/<cpedido>', methods=['GET'])
def query_detalle_pedido_by_id(cpedido):    
    result = q.get_detalle_pedido_by_id(cpedido)
    return jsonify(result)
    

@detalle_pedido.route('/detalle_pedido/<cpedido>', methods=['POST'])
def insert_detalle_pedido(cpedido):
    try:
        record = json.loads(request.data)

        cproducto = record['cproducto']
        cantidad = record['cantidad']

        # Check values are valid
        if not isinstance(cpedido, int) or not isinstance(cproducto, int) or not isinstance(cantidad, int):
            return jsonify({'error': 'invalid values'}), 400

        # Check if pedido exists
        pedido = q.get_pedido_by_id(cpedido)
        if pedido is None:
            return jsonify({'error': 'pedido does not exist'}), 400

        # Check if producto exists
        producto = q.get_producto_by_id(cproducto)
        if producto is None:
            return jsonify({'error': 'producto does not exist'}), 400

        # Check if producto is in stock
        if producto['stock'] < cantidad:
            return jsonify({'error': 'not enough stock'}), 400

        # Check if producto is already in pedido
        detalle_pedido = q.get_detalle_pedido_by_id(cpedido)
        if detalle_pedido is not None:
            return jsonify({'error': 'producto already in pedido'}), 400

        # Insert detalle pedido and update stock
        q.insert_detalle_pedido(cpedido, cproducto, cantidad)
        q.update_stock(cproducto, cantidad)

        result = q.get_detalle_pedido_by_id(cpedido)
        return jsonify(result)

    except Exception as ex:
        print("Error insering detalle pedido: ", ex)
        return jsonify({'error': 'error inserting detalle pedido'})


@detalle_pedido.route('/detalle_pedido/<cpedido>/delete', methods=['POST'])
def delete_detalle_pedido(cpedido):
    try:
        # Check if pedido exists
        pedido = q.get_pedido_by_id(cpedido)
        if pedido is None:
            return jsonify({'error': 'pedido does not exist'}), 400

        q.delete_detalle_pedido(cpedido);
        return jsonify({'success': 'detalle pedido deleted'})


    except Exception as ex:
        print("Error deleting detalle pedido: ", ex)
        return jsonify({'error': 'error deleting detalle pedido'})