"""✅ Soluciones — Flask: parámetros"""
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/pokemon/<int:n>")
def pokemon(n):
    return jsonify({"id": n})


@app.route("/saludo/<nombre>")
def saludo(nombre):
    return f"Hola, {nombre}"


@app.route("/buscar")
def buscar():
    tipo = request.args.get("tipo")
    return jsonify({"tipo": tipo})


@app.route("/doble/<int:n>")
def doble(n):
    return jsonify({"resultado": n * 2})
