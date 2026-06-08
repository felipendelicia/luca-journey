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


EQUIPO = [
    {"id": 1, "nombre": "Pikachu", "tipo": "Electrico"},
    {"id": 2, "nombre": "Onix", "tipo": "Roca"},
    {"id": 3, "nombre": "Staryu", "tipo": "Agua"},
    {"id": 4, "nombre": "Gengar", "tipo": "Fantasma"},
]


@app.route("/equipo")
def equipo_listar():
    return jsonify(EQUIPO)


@app.route("/equipo-cantidad")
def equipo_cantidad():
    return jsonify({"cantidad": len(EQUIPO)})


@app.route("/equipo-nombres")
def equipo_nombres():
    return jsonify({"nombres": [p["nombre"] for p in EQUIPO]})


@app.route("/equipo-tipos")
def equipo_tipos():
    return jsonify({"tipos": sorted(set(p["tipo"] for p in EQUIPO))})


@app.route("/equipo-de-tipo/<tipo>")
def equipo_de_tipo(tipo):
    return jsonify([p for p in EQUIPO if p["tipo"] == tipo])


@app.route("/equipo-id/<int:eid>")
def equipo_obtener(eid):
    for p in EQUIPO:
        if p["id"] == eid:
            return jsonify(p)
    return jsonify({"error": "no existe"}), 404


@app.route("/equipo-contar-tipo/<tipo>")
def equipo_contar_tipo(tipo):
    return jsonify({"cantidad": sum(1 for p in EQUIPO if p["tipo"] == tipo)})


@app.route("/equipo-primero")
def equipo_primero():
    return jsonify(EQUIPO[0])


@app.route("/equipo-ultimo")
def equipo_ultimo():
    return jsonify(EQUIPO[-1])


@app.route("/equipo-existe/<nombre>")
def equipo_existe(nombre):
    return jsonify({"existe": any(p["nombre"] == nombre for p in EQUIPO)})


@app.route("/equipo-ordenado")
def equipo_ordenado():
    return jsonify(sorted(p["nombre"] for p in EQUIPO))


@app.route("/equipo-filtrar", methods=["POST"])
def equipo_filtrar():
    tipo = request.json["tipo"]
    return jsonify([p for p in EQUIPO if p["tipo"] == tipo])


@app.route("/equipo-resumen")
def equipo_resumen():
    return jsonify({"total": len(EQUIPO), "tipos": len(set(p["tipo"] for p in EQUIPO))})


@app.route("/equipo-ids")
def equipo_ids():
    return jsonify({"ids": [p["id"] for p in EQUIPO]})


@app.route("/equipo-buscar/<nombre>")
def equipo_buscar(nombre):
    for p in EQUIPO:
        if p["nombre"] == nombre:
            return jsonify(p)
    return jsonify({"error": "no existe"}), 404


@app.route("/equipo-tiene-tipo/<tipo>")
def equipo_tiene_tipo(tipo):
    return jsonify({"hay": any(p["tipo"] == tipo for p in EQUIPO)})
