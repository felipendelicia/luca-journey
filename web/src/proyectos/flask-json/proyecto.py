# Líder Wattson — Rutas con JSON (solución de referencia).
from flask import Flask, jsonify

def crear_app():
    app = Flask(__name__)

    @app.route("/pokemon")
    def pokemon():
        return jsonify({"nombre": "Voltorb", "tipo": "eléctrico", "nivel": 20})

    @app.route("/equipo")
    def equipo():
        return jsonify(["Voltorb", "Electrode", "Magneton"])

    @app.route("/stats")
    def stats():
        return jsonify({"ataque": 55, "defensa": 40, "velocidad": 90})

    @app.route("/info")
    def info():
        return jsonify({"region": "Hoenn", "gimnasio": 3, "tipo": "eléctrico"})

    return app
