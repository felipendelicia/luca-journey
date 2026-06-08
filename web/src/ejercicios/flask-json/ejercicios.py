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


# /tipos-json → ["fuego", "agua", "planta"]
@app.route("/tipos-json")
def tipos_json():
    # TU CÓDIGO ACÁ
    pass


# /info → {"region": "Kanto", "total": 151}
@app.route("/info")
def info():
    # TU CÓDIGO ACÁ
    pass


# /pikachu → {"nombre": "Pikachu", "tipo": "electrico", "nivel": 25}
@app.route("/pikachu")
def pikachu_info():
    # TU CÓDIGO ACÁ
    pass


# /numeros → [1, 2, 3, 4, 5]
@app.route("/numeros")
def numeros():
    # TU CÓDIGO ACÁ
    pass


# /vacio → {} (un objeto vacío)
@app.route("/vacio")
def vacio():
    # TU CÓDIGO ACÁ
    pass


# /lista-vacia → [] (una lista vacía)
@app.route("/lista-vacia")
def lista_vacia():
    # TU CÓDIGO ACÁ
    pass


# /booleano → {"activo": True}
@app.route("/booleano")
def booleano():
    # TU CÓDIGO ACÁ
    pass


# /anidado → {"pokemon": {"nombre": "Pikachu", "stats": {"hp": 35}}}
@app.route("/anidado")
def anidado():
    # TU CÓDIGO ACÁ
    pass


# /entrenador → {"nombre": "Ash", "medallas": 8}
@app.route("/entrenador")
def entrenador():
    # TU CÓDIGO ACÁ
    pass


# /tipos-conteo → {"agua": 32, "fuego": 12}
@app.route("/tipos-conteo")
def tipos_conteo():
    # TU CÓDIGO ACÁ
    pass


# /version-json → {"version": "1.0", "estable": True}
@app.route("/version-json")
def version_json():
    # TU CÓDIGO ACÁ
    pass


# /coordenadas → [10, 20]
@app.route("/coordenadas")
def coordenadas():
    # TU CÓDIGO ACÁ
    pass


# /mensaje → {"mensaje": "Hola"}
@app.route("/mensaje")
def mensaje():
    # TU CÓDIGO ACÁ
    pass


# /precios → {"pocion": 200, "revivir": 1500}
@app.route("/precios")
def precios():
    # TU CÓDIGO ACÁ
    pass


# /equipo-completo → [{"nombre": "Pikachu"}, {"nombre": "Onix"}]
@app.route("/equipo-completo")
def equipo_completo():
    # TU CÓDIGO ACÁ
    pass


# /estado-json → {"status": "ok", "codigo": 200}
@app.route("/estado-json")
def estado_json():
    # TU CÓDIGO ACÁ
    pass
