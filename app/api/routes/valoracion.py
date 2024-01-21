import json
import logging
import app.query.articulo as query
import app.database as database
import app.query.social as social
from flask import Flask, request, jsonify, Blueprint

valoracion = Blueprint('valoracion', __name__)
db = database.database()
q = query.articulo(db)
s = social.social(db)

@valoracion.route('/valoracion/<nombre_usuario>/<titulo>', methods=['GET'])
def query_articulos(nombre_usuario,titulo):
        
    record = json.loads(request.data)
    titulo = record['titulo']
    nombre_usuario = record['nombre_usuario']

    result = q.consultar_valoracion(nombre_usuario,titulo)
    return jsonify(result)

@valoracion.route('/valoracion/', methods=['POST'])
def insert_valoracion(user,titulo):
    try:
        record = json.loads(request.data)

        titulo = record['titulo']
        user = record['nombre_usuario']
        p = record['puntuacion']
        c = record['comentario']

        # Check values are valid
        if not isinstance(titulo, str) or not isinstance(user, str) or not isinstance(p,int) or not isinstance(c,str):
            return jsonify({'error': 'articulo invalid values'}), 400
        
        #comprobar que user exista
        if s.get_usuario_by_id(user) is None:
            return jsonify({'error': 'Usuario no encontrado para valoracion'}), 400
        
        if q.consultar_articulo(titulo) is None:
            return jsonify({'error': 'articulo no encontrado para valoracion'}), 400

        if q.consultar_articulo_obtenido(user,titulo) is None:
            return jsonify({'error': 'El usuario no puede comentar este artículo NO adquirido'}), 400

        q.comentar(user,titulo,p,c)

        return jsonify({'mensaje':f'Valoracion de {user} subida para {titulo}'})
        
    except Exception as ex:
        logging.error("Error inserting Valoracion: ", ex)
        return jsonify({'error': 'error inserting valoracion'})