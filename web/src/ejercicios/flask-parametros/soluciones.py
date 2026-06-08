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


@app.route("/triple/<int:n>")
def triple(n):
    return jsonify({"resultado": n * 3})


@app.route("/cuadrado/<int:n>")
def cuadrado(n):
    return jsonify({"resultado": n * n})


@app.route("/eco/<texto>")
def eco(texto):
    return jsonify({"texto": texto})


@app.route("/mayuscula/<texto>")
def mayuscula(texto):
    return texto.upper()


@app.route("/largo/<texto>")
def largo(texto):
    return jsonify({"largo": len(texto)})


@app.route("/suma/<int:a>/<int:b>")
def suma(a, b):
    return jsonify({"suma": a + b})


@app.route("/resta/<int:a>/<int:b>")
def resta(a, b):
    return jsonify({"resta": a - b})


@app.route("/es-par/<int:n>")
def es_par(n):
    return jsonify({"par": n % 2 == 0})


@app.route("/saludar")
def saludar():
    return jsonify({"saludo": "Hola " + request.args.get("nombre")})


@app.route("/nivel")
def nivel():
    return jsonify({"nivel": int(request.args.get("valor"))})


@app.route("/repetir/<texto>/<int:veces>")
def repetir(texto, veces):
    return jsonify({"resultado": texto * veces})


@app.route("/invertir/<texto>")
def invertir(texto):
    return texto[::-1]


@app.route("/rango/<int:n>")
def rango(n):
    return jsonify({"numeros": list(range(1, n + 1))})


@app.route("/multiplicar/<int:a>/<int:b>")
def multiplicar(a, b):
    return jsonify({"resultado": a * b})


@app.route("/inicial/<texto>")
def inicial(texto):
    return texto[0]


@app.route("/negativo/<int:n>")
def negativo(n):
    return jsonify({"resultado": -n})
