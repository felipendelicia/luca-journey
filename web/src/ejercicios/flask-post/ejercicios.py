"""✏️ Ejercicios — Flask: métodos y POST

Hasta ahora solo leíamos datos (GET). Con POST el cliente nos ENVÍA datos (en JSON),
que se leen con request.json. ✅ Corregir al terminar.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)


# Eco (POST)
# En "/eco" (POST), devolvé el mismo JSON que te mandaron. Pista: request.json.
# Ejemplo:  POST /eco con {"x": 1}  →  {"x": 1}
@app.route("/eco", methods=["POST"])
def eco():
    # TU CÓDIGO ACÁ  (return jsonify(request.json))
    pass


# Sumar (POST)
# En "/sumar" (POST) recibís {"a": .., "b": ..} y devolvés {"suma": a + b}.
# Ejemplo:  POST /sumar con {"a": 3, "b": 4}  →  {"suma": 7}
@app.route("/sumar", methods=["POST"])
def sumar():
    # TU CÓDIGO ACÁ
    pass


# Crear (POST + 201)
# En "/crear" (POST) recibís {"nombre": ..} y devolvés {"creado": <nombre>} con el
# código de estado 201 (creado). Pista: return jsonify(...), 201.
# Ejemplo:  POST /crear con {"nombre": "Mew"}  →  {"creado": "Mew"}  (estado 201)
@app.route("/crear", methods=["POST"])
def crear():
    # TU CÓDIGO ACÁ
    pass
