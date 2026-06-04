"""
✏️ Ejercicios — Flask: parámetros

Rutas que reciben datos: en el PATH (/pokemon/25) o en la QUERY (/buscar?tipo=Fuego).
"""
from flask import Flask, jsonify, request

app = Flask(__name__)


# 1) En "/pokemon/<int:n>", devolvé {"id": n} usando el número del path.
#    Pista: la función recibe n como parámetro.
@app.route("/pokemon/<int:n>")
def pokemon(n):
    # TU CÓDIGO ACÁ (return jsonify({"id": n}))
    pass


# 2) En "/saludo/<nombre>", devolvé el texto "Hola, <nombre>".
@app.route("/saludo/<nombre>")
def saludo(nombre):
    # TU CÓDIGO ACÁ
    pass


# 3) En "/buscar", leé el parámetro de query 'tipo' y devolvé {"tipo": <valor>}.
#    Pista: request.args.get("tipo").
@app.route("/buscar")
def buscar():
    # TU CÓDIGO ACÁ
    pass


# 4) En "/doble/<int:n>", devolvé {"resultado": n * 2}.
@app.route("/doble/<int:n>")
def doble(n):
    # TU CÓDIGO ACÁ
    pass
