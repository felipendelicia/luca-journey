"""✅ Soluciones — Flask: respuestas JSON"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/pokemon")
def pokemon():
    return jsonify({"nombre": "Pikachu", "nivel": 25})


@app.route("/equipo")
def equipo():
    return jsonify(["Pikachu", "Charizard", "Snorlax"])


@app.route("/stats")
def stats():
    return jsonify({"ataque": 55, "defensa": 40, "velocidad": 90})


@app.route("/cantidad")
def cantidad():
    return jsonify({"total": 151})
