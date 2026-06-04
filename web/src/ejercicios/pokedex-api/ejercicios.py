"""✏️ Ejercicios — Proyecto: Pokédex API

Tu API REST completa de Pokémon. Junta todo Hoenn: rutas, JSON, parámetros, POST y
manejo de errores, sobre la lista POKEDEX. ✅ Corregir al terminar.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

POKEDEX = [
    {"id": 1, "nombre": "Bulbasaur", "tipo": "Planta"},
    {"id": 2, "nombre": "Charmander", "tipo": "Fuego"},
    {"id": 3, "nombre": "Squirtle", "tipo": "Agua"},
    {"id": 4, "nombre": "Vulpix", "tipo": "Fuego"},
]


# Listar la Pokédex (GET)
# En GET /pokedex devolvé toda la Pokédex.
@app.route("/pokedex")
def listar():
    # TU CÓDIGO ACÁ
    pass


# Obtener uno (GET por id)
# En GET /pokedex/<int:pid> devolvé ese Pokémon, o {"error": ...} con 404 si no existe.
# Ejemplo:  GET /pokedex/2  →  {"id": 2, "nombre": "Charmander", "tipo": "Fuego"}
@app.route("/pokedex/<int:pid>")
def obtener(pid):
    # TU CÓDIGO ACÁ
    pass


# Buscar por tipo (query)
# En GET /buscar leé el query 'tipo' y devolvé la lista de Pokémon de ese tipo.
# Pista: request.args.get("tipo").
# Ejemplo:  GET /buscar?tipo=Fuego  →  [Charmander, Vulpix]
@app.route("/buscar")
def buscar():
    # TU CÓDIGO ACÁ
    pass


# Agregar (POST + 201)
# En POST /pokedex agregá el JSON recibido a la Pokédex y devolvelo con estado 201.
@app.route("/pokedex", methods=["POST"])
def agregar():
    # TU CÓDIGO ACÁ
    pass
