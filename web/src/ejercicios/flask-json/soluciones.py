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


@app.route("/tipos-json")
def tipos_json():
    return jsonify(["fuego", "agua", "planta"])


@app.route("/info")
def info():
    return jsonify({"region": "Kanto", "total": 151})


@app.route("/pikachu")
def pikachu_info():
    return jsonify({"nombre": "Pikachu", "tipo": "electrico", "nivel": 25})


@app.route("/numeros")
def numeros():
    return jsonify([1, 2, 3, 4, 5])


@app.route("/vacio")
def vacio():
    return jsonify({})


@app.route("/lista-vacia")
def lista_vacia():
    return jsonify([])


@app.route("/booleano")
def booleano():
    return jsonify({"activo": True})


@app.route("/anidado")
def anidado():
    return jsonify({"pokemon": {"nombre": "Pikachu", "stats": {"hp": 35}}})


@app.route("/entrenador")
def entrenador():
    return jsonify({"nombre": "Ash", "medallas": 8})


@app.route("/tipos-conteo")
def tipos_conteo():
    return jsonify({"agua": 32, "fuego": 12})


@app.route("/version-json")
def version_json():
    return jsonify({"version": "1.0", "estable": True})


@app.route("/coordenadas")
def coordenadas():
    return jsonify([10, 20])


@app.route("/mensaje")
def mensaje():
    return jsonify({"mensaje": "Hola"})


@app.route("/precios")
def precios():
    return jsonify({"pocion": 200, "revivir": 1500})


@app.route("/equipo-completo")
def equipo_completo():
    return jsonify([{"nombre": "Pikachu"}, {"nombre": "Onix"}])


@app.route("/estado-json")
def estado_json():
    return jsonify({"status": "ok", "codigo": 200})
