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


# Equipo FIJO para estos ejercicios (no lo modifiques):
EQUIPO = [
    {"id": 1, "nombre": "Pikachu", "tipo": "Electrico"},
    {"id": 2, "nombre": "Onix", "tipo": "Roca"},
    {"id": 3, "nombre": "Staryu", "tipo": "Agua"},
    {"id": 4, "nombre": "Gengar", "tipo": "Fantasma"},
]


# GET /equipo → toda la lista EQUIPO
@app.route("/equipo")
def equipo_listar():
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-cantidad → {"cantidad": cuántos hay}
@app.route("/equipo-cantidad")
def equipo_cantidad():
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-nombres → {"nombres": [lista de nombres]}
@app.route("/equipo-nombres")
def equipo_nombres():
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-tipos → {"tipos": lista ORDENADA de tipos distintos}
@app.route("/equipo-tipos")
def equipo_tipos():
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-de-tipo/<tipo> → lista de Pokémon de ese tipo
@app.route("/equipo-de-tipo/<tipo>")
def equipo_de_tipo(tipo):
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-id/<int:eid> → el Pokémon con ese id, o {"error": ...} con 404
@app.route("/equipo-id/<int:eid>")
def equipo_obtener(eid):
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-contar-tipo/<tipo> → {"cantidad": cuántos son de ese tipo}
@app.route("/equipo-contar-tipo/<tipo>")
def equipo_contar_tipo(tipo):
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-primero → el primer Pokémon
@app.route("/equipo-primero")
def equipo_primero():
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-ultimo → el último Pokémon
@app.route("/equipo-ultimo")
def equipo_ultimo():
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-existe/<nombre> → {"existe": True/False}
@app.route("/equipo-existe/<nombre>")
def equipo_existe(nombre):
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-ordenado → la lista de NOMBRES ordenada alfabéticamente
@app.route("/equipo-ordenado")
def equipo_ordenado():
    # TU CÓDIGO ACÁ
    pass


# POST /equipo-filtrar recibe {"tipo": ..} → lista de Pokémon de ese tipo
@app.route("/equipo-filtrar", methods=["POST"])
def equipo_filtrar():
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-resumen → {"total": cantidad, "tipos": cantidad de tipos distintos}
@app.route("/equipo-resumen")
def equipo_resumen():
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-ids → {"ids": [lista de ids]}
@app.route("/equipo-ids")
def equipo_ids():
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-buscar/<nombre> → el Pokémon con ese nombre, o {"error": ...} con 404
@app.route("/equipo-buscar/<nombre>")
def equipo_buscar(nombre):
    # TU CÓDIGO ACÁ
    pass


# GET /equipo-tiene-tipo/<tipo> → {"hay": True/False si hay alguno de ese tipo}
@app.route("/equipo-tiene-tipo/<tipo>")
def equipo_tiene_tipo(tipo):
    # TU CÓDIGO ACÁ
    pass
