import json
import logging
import app.query.dev as query
import app.database as database
from flask import request, jsonify, Blueprint, current_app

creacion = Blueprint('dev', __name__)
db = database.database()
q = query.query(db)


@creacion.route('/creacion/', methods=['GET'])
def query_creacion():
    result = q.get_stock()
    return jsonify(result)

@creacion.route('/creacion/<Titulo_Creacion>', methods=['GET'])
def query_consulta_creacion(titulo_creacion):
 
    result = q.consulta_creacion(titulo_creacion)
    return jsonify(result)
    
@creacion.route('/creacion/<Tipo>', methods=['GET'])
def query_listar_creaciones(tipo):
 
    result = q.listar_creaciones(tipo)
    return jsonify(result)
        
@creacion.route('/creacion', methods=['POST'])
def query_subir_creacion():
    try:
        record = json.loads(request.data)

        titulo = record['Titulo_Creacion']
        tipo = record['Tipo']
        vid = record['Videojuego_Asociado']
        usu = record['#Nombre_Usuario']
        fecha = record['Fecha_Subida']
      
        q.subir_creacion(titulo, tipo, vid, usu, fecha)
        db.commit()

        result = jsonify({'message': 'creacion subida'})
        return result
          
    except Exception as ex:
        logging.error("Error subiendo creacion: ", ex)
        return jsonify({'error': 'error subiendo creacion'})

    
@stock.route('/creacion/<Titulo_Creacion>/delete', methods=['POST'])
def query_borrar_creacion(titulo_creacion):
    try:
        if titulo_creacion is None:
            return jsonify({'error': 'invalid values'}), 400

        q.borrar_creacion(titulo_creacion)
        db.commit()
        
        result = jsonify({'message': 'creacion eliminada'})
        return result
    except Exception as ex:
        logging.error("Error deleting creacion: ", ex)
        return jsonify({'error': 'error deleting creacion'})
