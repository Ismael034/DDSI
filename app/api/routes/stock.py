import json
import app.query as query
import app.database as database
from flask import Flask, request, jsonify, Blueprint

stock = Blueprint('stock', __name__)

db = database.database()
q = query.query(db)

@stock.route('/stock', methods=['GET'])
def query_records():
    name = request.args.get('producto')
    if name is None:
        result = q.get_stock()
        return jsonify(result)
    
    result = q.get_stock_by_id(name)
    return jsonify(result)
    


@stock.route('/stock', methods=['POST'])
def update_record():
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
    