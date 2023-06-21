from flask import Flask
from app.routes import celular, cliente, direccion_envio, pedido, index, auth

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = "mysecretkey"

app.register_blueprint(index)
app.register_blueprint(celular)
app.register_blueprint(cliente)
app.register_blueprint(direccion_envio)
app.register_blueprint(pedido)
app.register_blueprint(auth)


if __name__ == "__main__":
    app.run(port=3000, debug=True)