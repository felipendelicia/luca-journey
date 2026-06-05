# Líder Wallace — Mini Pokédex API (solución de referencia).
# El preamble (POKEDEX) está en meta.json y se antepone al corregir.
from flask import Flask, jsonify, request

def crear_app():
    app = Flask(__name__)

    @app.route("/pokemon")
    def listar():
        return jsonify(POKEDEX)

    @app.route("/pokemon/<int:pid>")
    def obtener(pid):
        for p in POKEDEX:
            if p["id"] == pid:
                return jsonify(p)
        return jsonify({"error": "no encontrado"}), 404

    @app.route("/pokemon/tipo/<tipo>")
    def por_tipo(tipo):
        return jsonify([p for p in POKEDEX if p["tipo"] == tipo])

    @app.route("/buscar")
    def buscar():
        nombre = request.args.get("nombre", "").lower()
        return jsonify([p for p in POKEDEX if nombre in p["nombre"].lower()])

    @app.route("/stats")
    def stats():
        total = len(POKEDEX)
        nivel_promedio = sum(p["nivel"] for p in POKEDEX) / total if total else 0
        tipos_vistos = []
        for p in POKEDEX:
            if p["tipo"] not in tipos_vistos:
                tipos_vistos.append(p["tipo"])
        return jsonify({"total": total, "nivel_promedio": nivel_promedio, "tipos": tipos_vistos})

    return app
