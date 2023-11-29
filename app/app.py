from flask import Flask
from app.api.config import Config
from app.api.routes.detalle_pedido import detalle_pedido
from app.api.routes.pedido import pedido
from app.api.routes.stock import stock


app = Flask(__name__)
app.config.from_object(Config)


app.register_blueprint(detalle_pedido)
app.register_blueprint(pedido)
app.register_blueprint(stock)

def run():
    app.run(debug=True)