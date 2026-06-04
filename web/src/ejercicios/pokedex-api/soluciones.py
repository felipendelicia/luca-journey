"""✅ Soluciones — Proyecto: Pokédex API"""
from flask import Flask, jsonify, request

app = Flask(__name__)

POKEDEX = [
    {"id": 1, "nombre": "Bulbasaur", "tipo": "Planta"},
    {"id": 2, "nombre": "Charmander", "tipo": "Fuego"},
    {"id": 3, "nombre": "Squirtle", "tipo": "Agua"},
    {"id": 4, "nombre": "Vulpix", "tipo": "Fuego"},
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


@app.route("/buscar")
def buscar():
    tipo = request.args.get("tipo")
    return jsonify([p for p in POKEDEX if p["tipo"] == tipo])


@app.route("/pokedex", methods=["POST"])
def agregar():
    nuevo = request.json
    POKEDEX.append(nuevo)
    return jsonify(nuevo), 201
