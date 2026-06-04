"""✅ Soluciones — Flask: tu primera app"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def inicio():
    return "¡Bienvenido a la Pokédex API!"


@app.route("/ping")
def ping():
    return "pong"


@app.route("/hola")
def hola():
    return "Hola, Entrenador"


@app.route("/version")
def version():
    return "1.0"
