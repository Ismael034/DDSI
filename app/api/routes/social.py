import json
import logging
import app.query.social as query
import app.database as database
from flask import request, jsonify, Blueprint, current_app

social = Blueprint('social', __name__)
db = database.database()
q = query.social(db)



@social.route('/user/<username>', methods=['GET'])
def query_usuario_by_id(username):
    result = q.get_usuario_by_id(username)
    return jsonify(result)


@social.route('/user/', methods=['POST'])
def create_usuario():
    try:
        record = json.loads(request.data)
        nombre_usuario = record['nombre_usuario']
        nombre = record['nombre']
        password = record['password']
        saldo = 0
        articulos_adquiridos = ''

        # Check values are valid
        if not isinstance(nombre_usuario, str) or not isinstance(nombre, str) or not isinstance(password, str):
            return jsonify({'error': 'invalid values'}), 400

        q.insert_usuario(nombre_usuario, nombre, password, saldo, articulos_adquiridos)
        return jsonify({'message': 'usuario creado'})

    except Exception as ex:
        current_app.logger.debug("Error al crear usuario: ", ex)
        return jsonify({'error': 'error al crear usuario'})
        

@social.route('/user/<usuario>/update', methods=['POST'])
def update_usuario(usuario):
    try:
        record = json.loads(request.data)
        nombre = record['nombre']
        password = record['password']
        articulos_adquiridos = record['articulos_adquiridos']

        # Check values are valid
        if not isinstance(nombre, str) or not isinstance(password, str) or not isinstance(articulos_adquiridos, str):
            return jsonify({'error': 'invalid values'}), 400
    
    except Exception as ex:
        current_app.logger.debug("Error al actualizar usuario: ", ex)
        return jsonify({'error': 'error al actualizar usuario'})

@social.route('/user/<cpedido>/delete', methods=['POST'])
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
