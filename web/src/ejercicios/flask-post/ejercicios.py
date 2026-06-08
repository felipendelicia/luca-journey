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


# /multiplicar (POST) recibe {"a":..,"b":..} → {"producto": a*b}
@app.route("/multiplicar", methods=["POST"])
def multiplicar():
    # TU CÓDIGO ACÁ
    pass


# /restar (POST) recibe {"a":..,"b":..} → {"resta": a-b}
@app.route("/restar", methods=["POST"])
def restar():
    # TU CÓDIGO ACÁ
    pass


# /saludar (POST) recibe {"nombre":..} → {"mensaje": "Hola <nombre>"}
@app.route("/saludar", methods=["POST"])
def saludar():
    # TU CÓDIGO ACÁ
    pass


# /mayuscula (POST) recibe {"texto":..} → {"texto": <texto en MAYÚSCULAS>}
@app.route("/mayuscula", methods=["POST"])
def mayuscula():
    # TU CÓDIGO ACÁ
    pass


# /largo (POST) recibe {"texto":..} → {"largo": cantidad de caracteres}
@app.route("/largo", methods=["POST"])
def largo():
    # TU CÓDIGO ACÁ
    pass


# /promedio (POST) recibe {"numeros":[...]} → {"promedio": el promedio}
@app.route("/promedio", methods=["POST"])
def promedio():
    # TU CÓDIGO ACÁ
    pass


# /maximo (POST) recibe {"numeros":[...]} → {"maximo": el mayor}
@app.route("/maximo", methods=["POST"])
def maximo():
    # TU CÓDIGO ACÁ
    pass


# /contar (POST) recibe {"items":[...]} → {"cantidad": cuántos hay}
@app.route("/contar", methods=["POST"])
def contar():
    # TU CÓDIGO ACÁ
    pass


# /invertir (POST) recibe {"texto":..} → {"resultado": <texto al revés>}
@app.route("/invertir", methods=["POST"])
def invertir():
    # TU CÓDIGO ACÁ
    pass


# /sumar-lista (POST) recibe {"numeros":[...]} → {"suma": la suma}
@app.route("/sumar-lista", methods=["POST"])
def sumar_lista():
    # TU CÓDIGO ACÁ
    pass


# /validar (POST) recibe {"nivel":..} → {"valido": True si nivel está entre 1 y 100}
@app.route("/validar", methods=["POST"])
def validar():
    # TU CÓDIGO ACÁ
    pass


# /crear-pokemon (POST) recibe {"nombre":..,"tipo":..} → {"pokemon": {"nombre":..,"tipo":..}}
# con código 201.
@app.route("/crear-pokemon", methods=["POST"])
def crear_pokemon():
    # TU CÓDIGO ACÁ
    pass


# /duplicar (POST) recibe {"valor":..} → {"resultado": valor*2}
@app.route("/duplicar", methods=["POST"])
def duplicar():
    # TU CÓDIGO ACÁ
    pass


# /concatenar (POST) recibe {"a":..,"b":..} (textos) → {"resultado": a+b}
@app.route("/concatenar", methods=["POST"])
def concatenar():
    # TU CÓDIGO ACÁ
    pass


# /es-mayor (POST) recibe {"a":..,"b":..} → {"mayor": True si a > b}
@app.route("/es-mayor", methods=["POST"])
def es_mayor():
    # TU CÓDIGO ACÁ
    pass


# /borrar (POST) recibe {"id":..} → {"borrado": id}
@app.route("/borrar", methods=["POST"])
def borrar():
    # TU CÓDIGO ACÁ
    pass


# /tipos-unicos (POST) recibe {"tipos":[...]} → {"tipos": lista ORDENADA sin repetir}
@app.route("/tipos-unicos", methods=["POST"])
def tipos_unicos():
    # TU CÓDIGO ACÁ
    pass
