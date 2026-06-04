"""✅ Soluciones — Flask: métodos y POST"""
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/eco", methods=["POST"])
def eco():
    return jsonify(request.json)


@app.route("/sumar", methods=["POST"])
def sumar():
    datos = request.json
    return jsonify({"suma": datos["a"] + datos["b"]})


@app.route("/crear", methods=["POST"])
def crear():
    nombre = request.json["nombre"]
    return jsonify({"creado": nombre}), 201
