# Líder Flannery — Rutas con parámetros (solución de referencia).
# El preamble (POKEDEX) está en meta.json y se antepone al corregir.
from flask import Flask, jsonify, request

def crear_app():
    app = Flask(__name__)

    @app.route("/saludo/<nombre>")
    def saludo(nombre):
        return "Hola, %s!" % nombre

    @app.route("/pokemon/<int:pid>")
    def pokemon_id(pid):
        poke = POKEDEX.get(pid)
        if poke is None:
            return jsonify({"error": "no encontrado"}), 404
        return jsonify(poke)

    @app.route("/buscar")
    def buscar():
        tipo = request.args.get("tipo", "")
        nombres = [p["nombre"] for p in POKEDEX.values() if p["tipo"] == tipo]
        return jsonify(nombres)

    @app.route("/nivel/<int:base>/<int:bonus>")
    def nivel(base, bonus):
        return jsonify({"nivel_final": base + bonus})

    return app
