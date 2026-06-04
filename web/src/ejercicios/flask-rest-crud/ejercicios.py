"""✏️ Ejercicios — Flask: API REST (CRUD)

Una API REST maneja un recurso con varias operaciones: leer (GET), crear (POST) y
borrar (DELETE). Trabajás sobre la lista POKEDEX (en memoria). ✅ Corregir al terminar.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

POKEDEX = [
    {"id": 1, "nombre": "Bulbasaur"},
    {"id": 2, "nombre": "Charmander"},
    {"id": 3, "nombre": "Squirtle"},
]


# Listar todo (GET)
# En GET /pokedex devolvé TODA la lista. Pista: jsonify(POKEDEX).
@app.route("/pokedex")
def listar():
    # TU CÓDIGO ACÁ
    pass


# Obtener uno (GET por id)
# En GET /pokedex/<int:pid> devolvé el Pokémon con ese id. Si no existe,
# devolvé {"error": "no existe"} con estado 404.
# Ejemplo:  GET /pokedex/2  →  {"id": 2, "nombre": "Charmander"}
@app.route("/pokedex/<int:pid>")
def obtener(pid):
    # TU CÓDIGO ACÁ
    pass


# Crear (POST + 201)
# En POST /pokedex agregá a la lista el JSON recibido y devolvelo con estado 201.
# Ejemplo:  POST /pokedex con {"id": 4, "nombre": "Pikachu"}  →  ese mismo dict (estado 201)
@app.route("/pokedex", methods=["POST"])
def agregar():
    # TU CÓDIGO ACÁ
    pass


# Borrar (DELETE)
# En DELETE /pokedex/<int:pid> borrá ese Pokémon y devolvé {"borrado": pid}.
# Si no existe, devolvé {"error": "no existe"} con estado 404.
# Ejemplo:  DELETE /pokedex/1  →  {"borrado": 1}
@app.route("/pokedex/<int:pid>", methods=["DELETE"])
def borrar(pid):
    # TU CÓDIGO ACÁ
    pass
