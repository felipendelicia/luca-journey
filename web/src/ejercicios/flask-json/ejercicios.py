"""✏️ Ejercicios — Flask: respuestas JSON

Las APIs devuelven JSON, no texto suelto. Usá jsonify(...) para que Flask arme la
respuesta JSON a partir de un dict o una lista. ✅ Corregir al terminar.
"""
from flask import Flask, jsonify

app = Flask(__name__)


# /pokemon → un objeto JSON
# En "/pokemon", devolvé el JSON {"nombre": "Pikachu", "nivel": 25}. Pista: return jsonify({...}).
@app.route("/pokemon")
def pokemon():
    # TU CÓDIGO ACÁ
    pass


# /equipo → una lista JSON
# En "/equipo", devolvé la lista JSON ["Pikachu", "Charizard", "Snorlax"].
@app.route("/equipo")
def equipo():
    # TU CÓDIGO ACÁ
    pass


# /stats → stats en JSON
# En "/stats", devolvé {"ataque": 55, "defensa": 40, "velocidad": 90}.
@app.route("/stats")
def stats():
    # TU CÓDIGO ACÁ
    pass


# /cantidad → un total
# En "/cantidad", devolvé {"total": 151}.
@app.route("/cantidad")
def cantidad():
    # TU CÓDIGO ACÁ
    pass
