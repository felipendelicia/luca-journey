"""✅ Soluciones — Flask: API REST (CRUD)"""
from flask import Flask, jsonify, request

app = Flask(__name__)

POKEDEX = [
    {"id": 1, "nombre": "Bulbasaur"},
    {"id": 2, "nombre": "Charmander"},
    {"id": 3, "nombre": "Squirtle"},
]


@app.route("/pokedex")
def listar():
    return jsonify(POKEDEX)


@app.route("/pokedex/<int:pid>")
def obtener(pid):
    for p in POKEDEX:
        if p["id"] == pid:
            return jsonify(p)
    return jsonify({"error": "no existe"}), 404


@app.route("/pokedex", methods=["POST"])
def agregar():
    nuevo = request.json
    POKEDEX.append(nuevo)
    return jsonify(nuevo), 201


@app.route("/pokedex/<int:pid>", methods=["DELETE"])
def borrar(pid):
    for p in POKEDEX:
        if p["id"] == pid:
            POKEDEX.remove(p)
            return jsonify({"borrado": pid})
    return jsonify({"error": "no existe"}), 404
