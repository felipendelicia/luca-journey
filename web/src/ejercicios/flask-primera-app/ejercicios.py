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
