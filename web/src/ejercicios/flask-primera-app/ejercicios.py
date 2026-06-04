"""
✏️ Ejercicios — Flask: tu primera app

Creamos una app Flask y le agregamos rutas. Cada ruta devuelve texto.
La app ya está creada abajo; vos completá lo que devuelve cada ruta.
"""
from flask import Flask

app = Flask(__name__)


# 1) Devolvé el texto "¡Bienvenido a la Pokédex API!" en la ruta principal "/".
@app.route("/")
def inicio():
    # TU CÓDIGO ACÁ (return "...")
    pass


# 2) Devolvé "pong" en la ruta "/ping".
@app.route("/ping")
def ping():
    # TU CÓDIGO ACÁ
    pass


# 3) Devolvé "Hola, Entrenador" en la ruta "/hola".
@app.route("/hola")
def hola():
    # TU CÓDIGO ACÁ
    pass


# 4) Devolvé "1.0" en la ruta "/version".
@app.route("/version")
def version():
    # TU CÓDIGO ACÁ
    pass
