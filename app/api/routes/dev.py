import json
import logging
import app.query.dev as query_dev
import app.query.articulo as query_articulo

import app.database as database
from flask import request, jsonify, Blueprint, current_app

dev = Blueprint('dev', __name__)
db = database.database()

q_dev = query_dev.dev(db)
q_articulo = query_articulo.articulo(db)

@dev.route('/creacion/<titulo_creacion>', methods=['GET'])
def query_consulta_creacion(titulo_creacion):
 
    result = q_dev.consulta_creacion(titulo_creacion)
    return jsonify(result)
    
@dev.route('/creacion/tipo/<tipo>', methods=['GET'])
def query_listar_creaciones(tipo):
 
    result = q_dev.listar_creaciones(tipo)
    return jsonify(result)
        
@dev.route('/creacion', methods=['POST'])
def query_subir_creacion():
    try:
        record = json.loads(request.data)

        titulo = record['titulo_creacion']
        tipo = record['tipo']
        usu = record['nombre_usuario']
        fecha = record['fecha_subida']
        
        descripcion_corta = record['descripcion_corta']
        descripcion_larga = record['descripcion_larga']
        genero = record['genero']
        icono = record['icono']
        tamano = record['tamano']
        ruta_ejecutable = record['ruta_ejecutable']
        especificaciones = record['especificaciones']
      
        q_articulo.subir_articulo(titulo, tamano, descripcion_corta, descripcion_larga, genero, icono, ruta_ejecutable, especificaciones)
        q_dev.subir_creacion(titulo, tipo, usu, fecha)
        db.commit()

        result = jsonify({'message': 'creacion subida'})
        return result
          
    except Exception as ex:
        logging.error("Error subiendo creacion: ", ex)
        return jsonify({'error': 'error subiendo creacion'})

    
@dev.route('/creacion/delete', methods=['POST'])
def query_borrar_creacion():
    try:
        record = json.loads(request.data)
	
        titulo = record['titulo_creacion']
        usu = record['nombre_usuario']
        
        q_dev.borrar_creacion(titulo, usu)
        db.commit()
        
        result = jsonify({'message': 'creacion eliminada'})
        return result
    except Exception as ex:
        logging.error("Error deleting creacion: ", ex)
        return jsonify({'error': 'error deleting creacion'})
        
@dev.route('/creacion/<titulo_creacion>/activar', methods=['POST'])
def query_activar_mod(titulo_creacion):
    try:        
        q_dev.activar_mod(titulo_creacion)
        db.commit()
        
        result = jsonify({'message': 'mod activado'})
        return result
    except Exception as ex:
        logging.error("Error activating mod: ", ex)
        return jsonify({'error': 'error activating mod'})       
