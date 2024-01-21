from flask import Flask
import logging

from app.api.config import Config

from app.api.routes.articulo import articulo
from app.api.routes.valoracion import valoracion
from app.api.routes.tienda import tienda
from app.api.routes.social import social
from app.api.routes.dev import dev
from app.api.routes.articulo_obtenido import articulo_obtenido

from app.database import database
from app.api.helpers import helpers

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(articulo)
app.register_blueprint(articulo_obtenido)
app.register_blueprint(tienda)
app.register_blueprint(social)
app.register_blueprint(dev)
app.register_blueprint(valoracion)

gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)


helpers.check_init_tables()

def run():
    app.run(debug=True, host='0.0.0.0', port=5000)
