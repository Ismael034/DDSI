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
            result = q.update_stock(record['producto'], record['cantidad'])
            return jsonify(result)
    except Exception as ex:
        print("Error updating pedido: ", ex)
        return jsonify({'error': 'error updating pedido'})
    

@pedido.route('/pedido/<cpedido>', methods=['UPDATE'])
def update_pedido_by_id(cpedido):
    try:
        record = json.loads(request.data)
        pedido = q.get_pedido_by_id(cpedido)
        
        if pedido is None:
            result = q.insert_pedido(record['producto'], record['cantidad'])
            return jsonify(result)
        else:
            result = q.update_stock(record['producto'], record['cantidad'])
            return jsonify(result)
    except Exception as ex:
        print("Error updating pedido: ", ex)
        return jsonify({'error': 'error updating pedido'})