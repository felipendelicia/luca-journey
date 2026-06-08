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


# Para estos ejercicios usá este catálogo FIJO (no lo modifiques):
CATALOGO = [{"id": 10, "nombre": "Mew"}, {"id": 11, "nombre": "Mewtwo"}, {"id": 12, "nombre": "Ditto"}]


# GET /catalogo → toda la lista CATALOGO
@app.route("/catalogo")
def cat_listar():
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-cantidad → {"cantidad": cuántos hay en CATALOGO}
@app.route("/catalogo-cantidad")
def cat_cantidad():
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-nombres → {"nombres": [lista de nombres]}
@app.route("/catalogo-nombres")
def cat_nombres():
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-ids → {"ids": [lista de ids]}
@app.route("/catalogo-ids")
def cat_ids():
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-id/<int:cid> → el item con ese id, o {"error": "no existe"} con 404
@app.route("/catalogo-id/<int:cid>")
def cat_obtener(cid):
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-existe/<int:cid> → {"existe": True/False}
@app.route("/catalogo-existe/<int:cid>")
def cat_existe(cid):
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-primero → el primer item
@app.route("/catalogo-primero")
def cat_primero():
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-ultimo → el último item
@app.route("/catalogo-ultimo")
def cat_ultimo():
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-buscar/<nombre> → el item con ese nombre, o {"error": "no existe"} con 404
@app.route("/catalogo-buscar/<nombre>")
def cat_buscar(nombre):
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-ordenado → la lista de NOMBRES ordenada alfabéticamente
@app.route("/catalogo-ordenado")
def cat_ordenado():
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-maxid → {"max": id más grande}
@app.route("/catalogo-maxid")
def cat_maxid():
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-minid → {"min": id más chico}
@app.route("/catalogo-minid")
def cat_minid():
    # TU CÓDIGO ACÁ
    pass


# POST /catalogo-contar recibe {"ids": [...]} → {"cantidad": cuántos ids mandaron}
@app.route("/catalogo-contar", methods=["POST"])
def cat_contar():
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-filtrar/<int:desde> → {"ids": ids mayores o iguales a 'desde'}
@app.route("/catalogo-filtrar/<int:desde>")
def cat_filtrar(desde):
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-resumen → {"total": cantidad, "primero": nombre del primero}
@app.route("/catalogo-resumen")
def cat_resumen():
    # TU CÓDIGO ACÁ
    pass


# GET /catalogo-vacio → {"vacio": True/False según si CATALOGO está vacío}
@app.route("/catalogo-vacio")
def cat_vacio():
    # TU CÓDIGO ACÁ
    pass
