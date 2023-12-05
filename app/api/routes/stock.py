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
        stock = q.get_stock_by_id(record['producto'])
        
        if stock is None:
            result = q.insert_stock(record['producto'], record['cantidad'])
            return jsonify(result)
        else:
            result = q.update_stock(record['producto'], record['cantidad'])
            return jsonify(result)
    except Exception as ex:
        print("Error updating stock: ", ex)
        return jsonify({'error': 'error updating stock'})
    
@stock.route('/stock/<cproducto>', methods=['UPDATE'])
def update_stock_by_id(cproducto):
    try:
        record = json.loads(request.data)
        stock = q.get_stock_by_id(cproducto)
        
        if stock is None:
            result = q.insert_stock(record['producto'], record['cantidad'])
            return jsonify(result)
        else:
            result = q.update_stock(record['producto'], record['cantidad'])
            return jsonify(result)
    except Exception as ex:
        print("Error updating stock: ", ex)
        return jsonify({'error': 'error updating stock'})
    
@stock.route('/stock/<cproducto>', methods=['DELETE'])
def delete_stock_by_id(cproducto):
    try:
        result = q.delete_stock(cproducto)
        return jsonify(result)
    except Exception as ex:
        print("Error deleting stock: ", ex)
        return jsonify({'error': 'error deleting stock'})