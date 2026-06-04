"""
✏️ Ejercicios — Flask: métodos y POST

Hasta ahora solo leímos datos (GET). Con POST el cliente nos ENVÍA datos
(en JSON). Se leen con request.json.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)


# 1) En "/eco" (POST), devolvé el mismo JSON que te mandaron.
#    Pista: request.json tiene los datos recibidos.
@app.route("/eco", methods=["POST"])
def eco():
    # TU CÓDIGO ACÁ (return jsonify(request.json))
    pass


# 2) En "/sumar" (POST), recibís {"a": .., "b": ..} y devolvés {"suma": a+b}.
@app.route("/sumar", methods=["POST"])
def sumar():
    # TU CÓDIGO ACÁ
    pass


# 3) En "/crear" (POST), recibís {"nombre": ..} y devolvés {"creado": <nombre>}
#    con el código de estado 201 (creado). Pista: return jsonify(...), 201
@app.route("/crear", methods=["POST"])
def crear():
    # TU CÓDIGO ACÁ
    pass
