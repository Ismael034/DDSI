import json
import logging
import app.query as query
import app.database as database
from flask import request, jsonify, Blueprint, current_app

stock = Blueprint('stock', __name__)
db = database.database()
q = query.query(db)


@stock.route('/stock/', methods=['GET'])
def query_stock():
    result = q.get_stock()
    return jsonify(result)

@stock.route('/stock/<cproducto>', methods=['GET'])
def query_stock_by_id(cproducto):
    if cproducto is None:
        result = q.get_stock()
        return jsonify(result)
    
    result = q.get_stock_by_id(cproducto)
    return jsonify(result)
    
@stock.route('/stock', methods=['POST'])
def insert_stock():
    try:
        record = json.loads(request.data)

        cantidad = record['cantidad']

        # Check values are valid
        if not isinstance(cantidad, int):
            return jsonify({'error': 'invalid values'}), 400
        
        q.insert_stock(cantidad)
        db.commit()

        result = jsonify({'message': 'stock creado'})
        return result
          
    except Exception as ex:
        logging.error("Error inserting stock: ", ex)
        return jsonify({'error': 'error updating stock'})


    
@stock.route('/stock/<cproducto>/update', methods=['POST'])
def update_stock_by_id(cproducto):
    try:
        record = json.loads(request.data)

        cantidad = record['cantidad']

        # Check values are valid
        if not isinstance(cantidad, int):
            return jsonify({'error': 'invalid values'}), 400

        stock = q.get_stock_by_id(cproducto)[1]
        logging.error(stock)
        
        if cantidad < 0:
            return jsonify({'error': 'invalid value cantidad'}), 400

        if stock - cantidad < 0:
            return jsonify({'error': 'cantidad to update is greater than stock'}), 400

        cantidad = stock - cantidad
        q.update_stock(cproducto, cantidad)

        new_stock = q.get_stock_by_id(cproducto)

        result = jsonify({'message': 'stock actualizado', 'stock': new_stock})
        return result

    except Exception as ex:
        logging.error("Error updating stock: ", ex)
        return jsonify({'error': 'error updating stock'})


    
@stock.route('/stock/<cproducto>/delete', methods=['POST'])
def delete_stock_by_id(cproducto):
    try:
        if cproducto is None:
            return jsonify({'error': 'invalid values'}), 400

        q.delete_stock(cproducto)
        db.commit()
        
        result = jsonify({'message': 'stock eliminado'})
        return result
    except Exception as ex:
        logging.error("Error deleting stock: ", ex)
        return jsonify({'error': 'error deleting stock'})