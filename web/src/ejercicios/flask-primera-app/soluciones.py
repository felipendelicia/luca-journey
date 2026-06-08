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


@app.route("/estado")
def estado():
    return "activo"


@app.route("/autor")
def autor():
    return "Profesor Oak"


@app.route("/region")
def region():
    return "Kanto"


@app.route("/total")
def total():
    return "151"


@app.route("/salud")
def salud():
    return "OK"


@app.route("/creador")
def creador():
    return "Ash Ketchum"


@app.route("/api")
def api():
    return "Pokedex API v1"


@app.route("/ayuda")
def ayuda():
    return "Usa /pokemon"


@app.route("/tipos")
def tipos():
    return "fuego, agua, planta"


@app.route("/destacado")
def destacado():
    return "Pikachu"


@app.route("/contacto")
def contacto():
    return "oak@kanto.com"


@app.route("/horario")
def horario():
    return "9 a 18"


@app.route("/reglas")
def reglas():
    return "Atrapalos a todos"


@app.route("/lema")
def lema():
    return "Hazte con todos"


@app.route("/numero")
def numero():
    return "25"


@app.route("/servidor")
def servidor():
    return "online"
