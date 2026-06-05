# Líder Brawly — Tu primera API (solución de referencia).
from flask import Flask

def crear_app():
    app = Flask(__name__)

    @app.route("/")
    def inicio():
        return "¡Bienvenido, Entrenador!"

    @app.route("/ping")
    def ping():
        return "pong"

    @app.route("/version")
    def version():
        return "1.0"

    @app.route("/estado")
    def estado():
        return "online"

    return app
