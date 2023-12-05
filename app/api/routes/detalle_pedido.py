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

@detalle_pedido.route('/detalle_pedido/', methods=['POST'])
def insert_detalle_pedido():
    try:
        record = json.loads(request.data)
        detalle_pedido = q.get_detalle_pedido_by_id(record['cpedido'])
        
        if detalle_pedido is None:
            result = q.insert_detalle_pedido(record['cpedido'], record['cproducto'], record['cantidad'])
            return jsonify(result)
        else:
            result = q.update_detalle_pedido(record['cpedido'], record['cproducto'], record['cantidad'])
            return jsonify(result)
    except Exception as ex:
        print("Error insering detalle pedido: ", ex)
        return jsonify({'error': 'error inserting detalle pedido'})