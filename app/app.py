from flask import Flask
import logging

from app.api.config import Config
from app.api.routes.detalle_pedido import detalle_pedido
from app.api.routes.pedido import pedido
from app.api.routes.stock import stock
from app.database import database
from app.query import query
from app.api.helpers import helpers

app = Flask(__name__)
app.config.from_object(Config)

db = database()
q = query(db)

app.register_blueprint(detalle_pedido)
app.register_blueprint(pedido)
app.register_blueprint(stock)

# Check if tables are generated
helpers.check_init_tables(q, db)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

def run():
    app.run(debug=True, host='0.0.0.0', port=5000)