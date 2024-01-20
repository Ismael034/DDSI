import json
import logging
import app.query.social as query
import app.database as database
from flask import request, jsonify, Blueprint, current_app

social = Blueprint('social', __name__)
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
        ccliente = record['ccliente']
        fecha_pedido = record['fecha_pedido']

        # Check values are valid
        if not isinstance(ccliente, int) or not isinstance(fecha_pedido, str):
            return jsonify({'error': 'invalid values'}), 400

        try:
            fecha_pedido = datetime.datetime.strptime(fecha_pedido, "%Y-%m-%d").date()            
        except Exception as e:
            current_app.logger.debug("Error parsing date: ", e)
            return jsonify({'error': 'invalid date'}), 400

        
        q.insert_pedido(ccliente, fecha_pedido)
        db.commit()
        
        result = jsonify({'message': 'pedido creado'})

        return result

    except Exception as ex:
        current_app.logger.debug("Error creating pedido: ", ex)
        return jsonify({'error': 'error creating pedido'})
        

@pedido.route('/pedido/<cpedido>/update', methods=['POST'])
def update_pedido(cpedido):
    try:
        record = json.loads(request.data)
        pedido = q.get_pedido_by_id(cpedido)
        
        if pedido is not None:
            result = q.update_pedido(cpedido, record['ccliente'], record['fecha_pedido'])
            return_value = q.get_pedido_by_id(pedido)
            return jsonify(return_value)
            
        else:
            return jsonify({'error': 'pedido does not exists'}), 400
    except Exception as ex:
        current_app.logger.debug("Error updating pedido: ", ex)
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
        logging.error("Error deleting pedido: ", ex)
        return jsonify({'error': 'error deleting pedido'})
