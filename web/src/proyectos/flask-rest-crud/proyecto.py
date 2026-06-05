# Líder Winona — API REST CRUD (solución de referencia).
from flask import Flask, jsonify, request

def crear_app():
    app = Flask(__name__)
    pokemon_lista = []

    @app.route("/pokemon")
    def listar():
        return jsonify(pokemon_lista)

    @app.route("/pokemon/<int:pid>")
    def obtener(pid):
        for p in pokemon_lista:
            if p["id"] == pid:
                return jsonify(p)
        return jsonify({"error": "no existe"}), 404

    @app.route("/pokemon", methods=["POST"])
    def crear():
        nuevo = request.json
        pokemon_lista.append(nuevo)
        return jsonify(nuevo), 201

    @app.route("/pokemon/<int:pid>", methods=["DELETE"])
    def borrar(pid):
        for i, p in enumerate(pokemon_lista):
            if p["id"] == pid:
                pokemon_lista.pop(i)
                return jsonify({"borrado": pid})
        return jsonify({"error": "no existe"}), 404

    @app.route("/pokemon/<int:pid>", methods=["PUT"])
    def actualizar(pid):
        for i, p in enumerate(pokemon_lista):
            if p["id"] == pid:
                pokemon_lista[i] = request.json
                return jsonify(pokemon_lista[i])
        return jsonify({"error": "no existe"}), 404

    return app
