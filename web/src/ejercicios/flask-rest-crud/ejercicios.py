"""
✏️ Ejercicios — Flask: API REST (CRUD)

Una API REST maneja un recurso con 4 operaciones: leer (GET), crear (POST),
y borrar (DELETE). Trabajamos sobre la lista POKEDEX (en memoria).
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

POKEDEX = [
    {"id": 1, "nombre": "Bulbasaur"},
    {"id": 2, "nombre": "Charmander"},
    {"id": 3, "nombre": "Squirtle"},
]


# 1) GET /pokedex -> devolvé TODA la lista (jsonify(POKEDEX)).
@app.route("/pokedex")
def listar():
    # TU CÓDIGO ACÁ
    pass


# 2) GET /pokedex/<int:pid> -> devolvé el Pokémon con ese id.
#    Si no existe, devolvé {"error": "no existe"} con estado 404.
@app.route("/pokedex/<int:pid>")
def obtener(pid):
    # TU CÓDIGO ACÁ
    pass


# 3) POST /pokedex -> agregá a la lista el JSON recibido y devolvelo con estado 201.
@app.route("/pokedex", methods=["POST"])
def agregar():
    # TU CÓDIGO ACÁ
    pass


# 4) DELETE /pokedex/<int:pid> -> borrá ese Pokémon y devolvé {"borrado": pid}.
#    Si no existe, devolvé {"error": "no existe"} con estado 404.
@app.route("/pokedex/<int:pid>", methods=["DELETE"])
def borrar(pid):
    # TU CÓDIGO ACÁ
    pass
