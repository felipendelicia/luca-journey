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


CATALOGO = [{"id": 10, "nombre": "Mew"}, {"id": 11, "nombre": "Mewtwo"}, {"id": 12, "nombre": "Ditto"}]


@app.route("/catalogo")
def cat_listar():
    return jsonify(CATALOGO)


@app.route("/catalogo-cantidad")
def cat_cantidad():
    return jsonify({"cantidad": len(CATALOGO)})


@app.route("/catalogo-nombres")
def cat_nombres():
    return jsonify({"nombres": [p["nombre"] for p in CATALOGO]})


@app.route("/catalogo-ids")
def cat_ids():
    return jsonify({"ids": [p["id"] for p in CATALOGO]})


@app.route("/catalogo-id/<int:cid>")
def cat_obtener(cid):
    for p in CATALOGO:
        if p["id"] == cid:
            return jsonify(p)
    return jsonify({"error": "no existe"}), 404


@app.route("/catalogo-existe/<int:cid>")
def cat_existe(cid):
    return jsonify({"existe": any(p["id"] == cid for p in CATALOGO)})


@app.route("/catalogo-primero")
def cat_primero():
    return jsonify(CATALOGO[0])


@app.route("/catalogo-ultimo")
def cat_ultimo():
    return jsonify(CATALOGO[-1])


@app.route("/catalogo-buscar/<nombre>")
def cat_buscar(nombre):
    for p in CATALOGO:
        if p["nombre"] == nombre:
            return jsonify(p)
    return jsonify({"error": "no existe"}), 404


@app.route("/catalogo-ordenado")
def cat_ordenado():
    return jsonify(sorted([p["nombre"] for p in CATALOGO]))


@app.route("/catalogo-maxid")
def cat_maxid():
    return jsonify({"max": max(p["id"] for p in CATALOGO)})


@app.route("/catalogo-minid")
def cat_minid():
    return jsonify({"min": min(p["id"] for p in CATALOGO)})


@app.route("/catalogo-contar", methods=["POST"])
def cat_contar():
    return jsonify({"cantidad": len(request.json["ids"])})


@app.route("/catalogo-filtrar/<int:desde>")
def cat_filtrar(desde):
    return jsonify({"ids": [p["id"] for p in CATALOGO if p["id"] >= desde]})


@app.route("/catalogo-resumen")
def cat_resumen():
    return jsonify({"total": len(CATALOGO), "primero": CATALOGO[0]["nombre"]})


@app.route("/catalogo-vacio")
def cat_vacio():
    return jsonify({"vacio": len(CATALOGO) == 0})
