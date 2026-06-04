"""
✏️ Ejercicios — Flask: respuestas JSON

Las APIs devuelven JSON, no texto suelto. Usá jsonify(...) para que Flask
arme la respuesta JSON a partir de un dict o una lista.
"""
from flask import Flask, jsonify

app = Flask(__name__)


# 1) En "/pokemon", devolvé el JSON {"nombre": "Pikachu", "nivel": 25}.
@app.route("/pokemon")
def pokemon():
    # TU CÓDIGO ACÁ (return jsonify({...}))
    pass


# 2) En "/equipo", devolvé la lista JSON ["Pikachu", "Charizard", "Snorlax"].
@app.route("/equipo")
def equipo():
    # TU CÓDIGO ACÁ
    pass


# 3) En "/stats", devolvé {"ataque": 55, "defensa": 40, "velocidad": 90}.
@app.route("/stats")
def stats():
    # TU CÓDIGO ACÁ
    pass


# 4) En "/cantidad", devolvé {"total": 151}.
@app.route("/cantidad")
def cantidad():
    # TU CÓDIGO ACÁ
    pass
