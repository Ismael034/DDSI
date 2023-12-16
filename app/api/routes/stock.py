import json
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
        print("Error creating stock: ", ex)
        return jsonify({'error': 'error updating stock'})


    
@stock.route('/stock/<cproducto>/update', methods=['POST'])
def update_stock_by_id(cproducto):
    try:

        cantidad = record['cantidad']

        # Check values are valid
        if not isinstance(cproducto, int) or not isinstance(cantidad, int):
            return jsonify({'error': 'invalid values'}), 400

        record = json.loads(request.data)
        stock = q.get_stock_by_id(cproducto)
        
        if cantidad < 0 or stock['cantidad'] - cantidad < 0:
            return jsonify({'error': 'invalid value cantidad'}), 400

        cantidad = stock['cantidad'] - cantidad
        q.update_stock(cproducto, cantidad)
        db.commit()

        result = jsonify({'message': 'stock actualizado'})
        return result

    except Exception as ex:
        print("Error updating stock: ", ex)
        return jsonify({'error': 'error updating stock'})


    
@stock.route('/stock/<cproducto>/delete', methods=['POST'])
def delete_stock_by_id(cproducto):
    try:
        if not isinstance(cproducto, int):
            return jsonify({'error': 'invalid values'}), 400

        q.delete_stock(cproducto)
        db.commit()
        
        result = jsonify({'message': 'stock eliminado'})
        return result
    except Exception as ex:
        print("Error deleting stock: ", ex)
        return jsonify({'error': 'error deleting stock'})