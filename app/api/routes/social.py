import json
import logging
import app.query.social as query
import app.database as database
from flask import request, jsonify, Blueprint, current_app

social = Blueprint('social', __name__)
db = database.database()
q = query.social(db)



@social.route('/user/<username>', methods=['GET'])
def query_perfil_by_id(username):
    perfil = q.get_perfil_by_id(username)
    if perfil is None:
        return jsonify({'error': 'perfil not found'}), 404
    
    return jsonify(perfil)

@social.route('/user/', methods=['POST'])
def create_usuario():
    try:
        record = json.loads(request.data)
        nombre_usuario = record['nombre_usuario']
        nombre = record['nombre']
        email = record['email']
        password = record['password']
        saldo = 0
        articulos_adquiridos = ''

        usuario = q.get_usuario_by_id(nombre_usuario)
        if usuario is not None:
            return jsonify({'error': 'usuario already exists'}), 400
        # Check values are valid
        if not isinstance(nombre_usuario, str) or not isinstance(nombre, str) or not isinstance(password, str):
            return jsonify({'error': 'invalid values'}), 400

        q.insert_usuario(nombre_usuario, nombre, email, password, saldo, articulos_adquiridos)
        #q.insert_perfil(nombre_usuario, '', '', '', '')
        return jsonify({'message': 'usuario creado'})

    except Exception as ex:
        current_app.logger.debug("Error al crear usuario: ", ex)
        return jsonify({'error': 'error al crear usuario'})
        
@social.route('/user/login', methods=['POST'])
def iniciar_sesion():
    try:
        record = json.loads(request.data)
        nombre_usuario = record['nombre_usuario']
        password = record['password']

        usuario = q.get_usuario_by_id(nombre_usuario)
        if usuario is None:
            return jsonify({'error': 'usuario not found'}), 404

        if usuario[4] != password:
            return jsonify({'error': 'invalid password'}), 400

        return jsonify({'message': 'sesion iniciada'})

    except Exception as ex:
        current_app.logger.debug("Error al iniciar sesion: ", ex)
        return jsonify({'error': 'error al iniciar sesion'})
    

@social.route('/user/<usuario>/update_articulo', methods=['POST'])
def update_articulos_adquiridos(usuario):
    try:
        record = json.loads(request.data)
        articulos_adquiridos = record['articulos_adquiridos']

        # Check values are valid
        if not isinstance(articulos_adquiridos, str):
            return jsonify({'error': 'invalid values'}), 400

        q.update_articulos_adquiridos(usuario, articulos_adquiridos)
        return jsonify({'message': 'usuario actualizado'})

    except Exception as ex:
        current_app.logger.debug("Error al actualizar articulos adquiridos: ", ex)
        return jsonify({'error': 'error al actualizar articulos adquiridos'})

@social.route('/user/<usuario>/update', methods=['POST'])
def update_perfil(usuario):
    try:
        record = json.loads(request.data)
        fotografia = record['fotografia']
        biografia = record['biografia']
        logros = record['logros']

        # Check values are valid
        if not isinstance(fotografia, str) or not isinstance(biografia, str) or not isinstance(logros, str):
            return jsonify({'error': 'invalid values'}), 400

        q.update_perfil(usuario, fotografia, biografia, logros)
        return jsonify({'message': 'perfil actualizado'})

    except Exception as ex:
        current_app.logger.debug("Error al actualizar usuario: ", ex)
        return jsonify({'error': 'error al actualizar usuario'})


@social.route('/user/<usuario>/delete', methods=['POST'])
def delete_usuario_by_id(usuario):
    try:
        usuario = q.get_usuario_by_id(usuario)[0]
        if usuario is not None:
            q.delete_perfil(usuario)
            q.delete_usuario(usuario)
            
            return jsonify({'message': 'usuario borrado'})
        else:
            return jsonify({'error': 'el usuario no existe'}), 400
    except Exception as ex:
        logging.error(f"Error borrando usuario: {ex}")
        return jsonify({'error': 'error borrando usuario'})


@social.route('/user/<usuario>/amigos', methods=['GET'])
def query_amigos_by_id(usuario):
    amigos = q.get_amistad_by_id(usuario)
    return jsonify(amigos)

@social.route('/user/<usuario>/amigos/accept', methods=['POST'])
def accept_amigo(usuario):
    try:
        record = json.loads(request.data)
        amigo = record['amigo']

        # Check values are valid
        if not isinstance(amigo, str):
            return jsonify({'error': 'invalid values'}), 400

        amistad = q.get_amistad_by_id(usuario)
        if amistad is None:
            return jsonify({'error': 'amistad no existe'}), 400

        q.accept_amistad(usuario, amigo)
        return jsonify({'message': 'amigo aceptado'})

    except Exception as ex:
        current_app.logger.debug("Error al aceptar amigo: ", ex)
        return jsonify({'error': 'error al aceptar amigo'})


@social.route('/user/<usuario>/amigos/add', methods=['POST'])
def add_amigo(usuario):
    try:
        record = json.loads(request.data)
        amigo = record['amigo']

        # Check values are valid
        if not isinstance(amigo, str):
            return jsonify({'error': 'invalid values'}), 400

        amigo = q.get_usuario_by_id(amigo)[0]

        if amigo is None:
            return jsonify({'error': 'amigo no existe'}), 400

        q.insert_amistad(usuario, amigo)
        return jsonify({'message': 'solicitud enviada'})

    except Exception as ex:
        current_app.logger.debug("Error al agregar amigo: ", ex)
        return jsonify({'error': 'error al agregar amigo'})

@social.route('/user/<usuario>/amigos/delete', methods=['POST'])
def delete_amigo(usuario):
    try:
        record = json.loads(request.data)
        amigo = record['amigo']

        # Check values are valid
        if not isinstance(amigo, str):
            return jsonify({'error': 'invalid values'}), 400

        amigo = q.get_usuario_by_id(amigo)[0]

        if amigo is None:
            return jsonify({'error': 'amigo no existe'}), 400

        q.delete_amistad(usuario, amigo)
        return jsonify({'message': 'amigo borrado'})

    except Exception as ex:
        current_app.logger.debug("Error al borrar amigo: ", ex)
        return jsonify({'error': 'error al borrar amigo'})

