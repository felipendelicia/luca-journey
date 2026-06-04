"""
✏️ Ejercicios — Proyecto: Pokédex API

Tu API REST completa de Pokémon. Junta todo Hoenn: rutas, JSON, parámetros,
POST y manejo de errores, sobre la lista POKEDEX.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

POKEDEX = [
    {"id": 1, "nombre": "Bulbasaur", "tipo": "Planta"},
    {"id": 2, "nombre": "Charmander", "tipo": "Fuego"},
    {"id": 3, "nombre": "Squirtle", "tipo": "Agua"},
    {"id": 4, "nombre": "Vulpix", "tipo": "Fuego"},
]


# 1) GET /pokedex -> devolvé toda la Pokédex.
@app.route("/pokedex")
def listar():
    # TU CÓDIGO ACÁ
    pass


# 2) GET /pokedex/<int:pid> -> devolvé ese Pokémon, o 404 si no existe.
@app.route("/pokedex/<int:pid>")
def obtener(pid):
    # TU CÓDIGO ACÁ
    pass


# 3) GET /buscar?tipo=Fuego -> devolvé la lista de Pokémon de ese tipo.
#    Pista: request.args.get("tipo").
@app.route("/buscar")
def buscar():
    # TU CÓDIGO ACÁ
    pass


# 4) POST /pokedex -> agregá el JSON recibido y devolvelo con estado 201.
@app.route("/pokedex", methods=["POST"])
def agregar():
    # TU CÓDIGO ACÁ
    pass
