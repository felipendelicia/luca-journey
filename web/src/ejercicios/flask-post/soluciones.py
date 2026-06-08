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


@app.route("/multiplicar", methods=["POST"])
def multiplicar():
    d = request.json
    return jsonify({"producto": d["a"] * d["b"]})


@app.route("/restar", methods=["POST"])
def restar():
    d = request.json
    return jsonify({"resta": d["a"] - d["b"]})


@app.route("/saludar", methods=["POST"])
def saludar():
    return jsonify({"mensaje": "Hola " + request.json["nombre"]})


@app.route("/mayuscula", methods=["POST"])
def mayuscula():
    return jsonify({"texto": request.json["texto"].upper()})


@app.route("/largo", methods=["POST"])
def largo():
    return jsonify({"largo": len(request.json["texto"])})


@app.route("/promedio", methods=["POST"])
def promedio():
    n = request.json["numeros"]
    return jsonify({"promedio": sum(n) / len(n)})


@app.route("/maximo", methods=["POST"])
def maximo():
    return jsonify({"maximo": max(request.json["numeros"])})


@app.route("/contar", methods=["POST"])
def contar():
    return jsonify({"cantidad": len(request.json["items"])})


@app.route("/invertir", methods=["POST"])
def invertir():
    return jsonify({"resultado": request.json["texto"][::-1]})


@app.route("/sumar-lista", methods=["POST"])
def sumar_lista():
    return jsonify({"suma": sum(request.json["numeros"])})


@app.route("/validar", methods=["POST"])
def validar():
    nivel = request.json["nivel"]
    return jsonify({"valido": 1 <= nivel <= 100})


@app.route("/crear-pokemon", methods=["POST"])
def crear_pokemon():
    d = request.json
    return jsonify({"pokemon": {"nombre": d["nombre"], "tipo": d["tipo"]}}), 201


@app.route("/duplicar", methods=["POST"])
def duplicar():
    return jsonify({"resultado": request.json["valor"] * 2})


@app.route("/concatenar", methods=["POST"])
def concatenar():
    d = request.json
    return jsonify({"resultado": d["a"] + d["b"]})


@app.route("/es-mayor", methods=["POST"])
def es_mayor():
    d = request.json
    return jsonify({"mayor": d["a"] > d["b"]})


@app.route("/borrar", methods=["POST"])
def borrar():
    return jsonify({"borrado": request.json["id"]})


@app.route("/tipos-unicos", methods=["POST"])
def tipos_unicos():
    return jsonify({"tipos": sorted(set(request.json["tipos"]))})
