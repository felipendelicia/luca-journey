"""✏️ Ejercicios — Flask: tu primera app

Creamos una app Flask y le agregamos rutas. Cada ruta es una función que devuelve
texto. La app ya está creada; completá lo que devuelve cada ruta. ✅ Corregir al terminar.
"""
from flask import Flask

app = Flask(__name__)


# Ruta principal "/"
# En la ruta "/", devolvé el texto: ¡Bienvenido a la Pokédex API!
# Ejemplo:  GET /  →  "¡Bienvenido a la Pokédex API!"
@app.route("/")
def inicio():
    # TU CÓDIGO ACÁ  (return "...")
    pass


# Ruta "/ping"
# En la ruta "/ping", devolvé el texto: pong
# Ejemplo:  GET /ping  →  "pong"
@app.route("/ping")
def ping():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/hola"
# En la ruta "/hola", devolvé el texto: Hola, Entrenador
# Ejemplo:  GET /hola  →  "Hola, Entrenador"
@app.route("/hola")
def hola():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/version"
# En la ruta "/version", devolvé el texto: 1.0
# Ejemplo:  GET /version  →  "1.0"
@app.route("/version")
def version():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/estado" → "activo"
@app.route("/estado")
def estado():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/autor" → "Profesor Oak"
@app.route("/autor")
def autor():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/region" → "Kanto"
@app.route("/region")
def region():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/total" → "151"
@app.route("/total")
def total():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/salud" → "OK"
@app.route("/salud")
def salud():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/creador" → "Ash Ketchum"
@app.route("/creador")
def creador():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/api" → "Pokedex API v1"
@app.route("/api")
def api():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/ayuda" → "Usa /pokemon"
@app.route("/ayuda")
def ayuda():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/tipos" → "fuego, agua, planta"
@app.route("/tipos")
def tipos():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/destacado" → "Pikachu"
@app.route("/destacado")
def destacado():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/contacto" → "oak@kanto.com"
@app.route("/contacto")
def contacto():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/horario" → "9 a 18"
@app.route("/horario")
def horario():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/reglas" → "Atrapalos a todos"
@app.route("/reglas")
def reglas():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/lema" → "Hazte con todos"
@app.route("/lema")
def lema():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/numero" → "25"
@app.route("/numero")
def numero():
    # TU CÓDIGO ACÁ
    pass


# Ruta "/servidor" → "online"
@app.route("/servidor")
def servidor():
    # TU CÓDIGO ACÁ
    pass
