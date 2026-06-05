# Líder Norman — Recibir datos con POST (solución de referencia).
from flask import Flask, jsonify, request

def crear_app():
    app = Flask(__name__)

    @app.route("/eco", methods=["POST"])
    def eco():
        return jsonify(request.json)

    @app.route("/registrar", methods=["POST"])
    def registrar():
        datos = request.json
        return jsonify({"registrado": datos["nombre"], "nivel": datos["nivel"]}), 201

    @app.route("/sumar-niveles", methods=["POST"])
    def sumar_niveles():
        total = sum(request.json["niveles"])
        return jsonify({"total": total})

    @app.route("/tipo-fuerte", methods=["POST"])
    def tipo_fuerte():
        equipo = request.json["equipo"]
        mas_fuerte = max(equipo, key=lambda p: p["nivel"])
        return jsonify({"mas_fuerte": mas_fuerte["nombre"]})

    return app
