# Liga de Hoenn — API de Entrenadores (solución de referencia).
from flask import Flask, jsonify, request

def crear_app():
    app = Flask(__name__)
    entrenadores = []

    def _buscar(eid):
        for e in entrenadores:
            if e["id"] == eid:
                return e
        return None

    @app.route("/entrenadores", methods=["POST"])
    def registrar():
        nuevo = request.json
        nuevo["equipo"] = []
        entrenadores.append(nuevo)
        respuesta = {k: v for k, v in nuevo.items() if k != "equipo"}
        return jsonify(respuesta), 201

    @app.route("/entrenadores")
    def listar():
        return jsonify([{k: v for k, v in e.items() if k != "equipo"} for e in entrenadores])

    @app.route("/entrenadores/<int:eid>")
    def obtener(eid):
        e = _buscar(eid)
        if e is None:
            return jsonify({"error": "no existe"}), 404
        return jsonify({k: v for k, v in e.items() if k != "equipo"})

    @app.route("/entrenadores/<int:eid>", methods=["DELETE"])
    def borrar(eid):
        for i, e in enumerate(entrenadores):
            if e["id"] == eid:
                entrenadores.pop(i)
                return jsonify({"borrado": eid})
        return jsonify({"error": "no existe"}), 404

    @app.route("/entrenadores/region/<region>")
    def por_region(region):
        return jsonify([{k: v for k, v in e.items() if k != "equipo"} for e in entrenadores if e["region"] == region])

    @app.route("/entrenadores/<int:eid>/pokemon", methods=["POST"])
    def agregar_pokemon(eid):
        e = _buscar(eid)
        if e is None:
            return jsonify({"error": "no existe"}), 404
        poke = request.json
        e["equipo"].append(poke)
        return jsonify(poke), 201

    @app.route("/entrenadores/<int:eid>/pokemon")
    def equipo(eid):
        e = _buscar(eid)
        if e is None:
            return jsonify({"error": "no existe"}), 404
        return jsonify(e["equipo"])

    @app.route("/entrenadores/<int:eid>/nivel-total")
    def nivel_total(eid):
        e = _buscar(eid)
        if e is None:
            return jsonify({"error": "no existe"}), 404
        total = sum(p["nivel"] for p in e["equipo"])
        return jsonify({"nivel_total": total})

    return app
