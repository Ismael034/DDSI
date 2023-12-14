import json
from flask import request, jsonify, Blueprint
import app.query as query
import app.database as database

pedido = Blueprint('pedido', __name__)
db = database.database()
q = query.query(db)


@pedido.route('/pedido/', methods=['GET'])
def query_pedido():
    result = q.get_pedido()
    return jsonify(result)


@pedido.route('/pedido/<cpedido>', methods=['GET'])
def query_pedido_by_id(cpedido):
    result = q.get_pedido_by_id(cpedido)
    return jsonify(result)


@pedido.route('/pedido/', methods=['POST'])
def create_pedido():
    try:
        record = json.loads(request.data)
        pedido = q.get_pedido_by_id(record['cpedido'])
        
        if pedido is None:
            result = q.insert_pedido(record['producto'], record['cantidad'])
            return jsonify(result)
        else:
            return jsonify({'error': 'pedido already exists'}), 400
    except Exception as ex:
        print("Error updating pedido: ", ex)
        return jsonify({'error': 'error updating pedido'})

@pedido.route('/pedido/<cpedido>/update', methods=['POST'])
def update_pedido():
    try:
        record = json.loads(request.data)
        pedido = q.get_pedido_by_id(record['cpedido'])
        
        if pedido is None:
            result = q.insert_pedido(record['producto'], record['cantidad'])
            return jsonify(result)
        else:
            return jsonify({'error': 'pedido already exists'}), 400
    except Exception as ex:
        print("Error updating pedido: ", ex)
        return jsonify({'error': 'error updating pedido'})

@pedido.route('/pedido/<cpedido>/delete', methods=['POST'])
def delete_pedido_by_id(cpedido):
    try:
        pedido = q.get_pedido_by_id(cpedido)
        if pedido is not None:
            q.delete_pedido(cpedido)
            
            # Delete detalle pedido
            detalle_pedido = q.get_detalle_pedido_by_id(cpedido)
            if detalle_pedido is not None:
                q.delete_detalle_pedido(cpedido)

            return jsonify({'message': 'pedido deleted'})
        else:
            return jsonify({'error': 'pedido does not exist'}), 400
    except Exception as ex:
        print("Error deleting pedido: ", ex)
        return jsonify({'error': 'error deleting pedido'})