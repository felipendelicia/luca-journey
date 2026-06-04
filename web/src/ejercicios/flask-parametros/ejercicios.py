"""✏️ Ejercicios — Flask: parámetros

Rutas que reciben datos: en el PATH (/pokemon/25) o en la QUERY (/buscar?tipo=Fuego).
✅ Corregir al terminar.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)


# Número en el path
# En "/pokemon/<int:n>", devolvé {"id": n} usando el número del path.
# La función recibe n como parámetro.
# Ejemplo:  GET /pokemon/25  →  {"id": 25}
@app.route("/pokemon/<int:n>")
def pokemon(n):
    # TU CÓDIGO ACÁ
    pass


# Texto en el path
# En "/saludo/<nombre>", devolvé el texto "Hola, <nombre>".
# Ejemplo:  GET /saludo/Ash  →  "Hola, Ash"
@app.route("/saludo/<nombre>")
def saludo(nombre):
    # TU CÓDIGO ACÁ
    pass


# Parámetro de query
# En "/buscar", leé el parámetro de query 'tipo' y devolvé {"tipo": <valor>}.
# Pista: request.args.get("tipo").
# Ejemplo:  GET /buscar?tipo=Fuego  →  {"tipo": "Fuego"}
@app.route("/buscar")
def buscar():
    # TU CÓDIGO ACÁ
    pass


# Calcular con el path
# En "/doble/<int:n>", devolvé {"resultado": n * 2}.
# Ejemplo:  GET /doble/21  →  {"resultado": 42}
@app.route("/doble/<int:n>")
def doble(n):
    # TU CÓDIGO ACÁ
    pass
