"""✏️ Ejercicios — Flask: parámetros

Rutas que reciben datos: en el PATH (/pokemon/25) o en la QUERY (/buscar?tipo=Fuego).
✅ Corregir al terminar.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)


# Número en el path
# En "/pokemon/<int:n>", devolvé {"id": n} usando el número del path.
# La función recibe n como parámetro.
# Ejemplo:  GET /pokemon/25  →  {"id": 25}
@app.route("/pokemon/<int:n>")
def pokemon(n):
    # TU CÓDIGO ACÁ
    pass


# Texto en el path
# En "/saludo/<nombre>", devolvé el texto "Hola, <nombre>".
# Ejemplo:  GET /saludo/Ash  →  "Hola, Ash"
@app.route("/saludo/<nombre>")
def saludo(nombre):
    # TU CÓDIGO ACÁ
    pass


# Parámetro de query
# En "/buscar", leé el parámetro de query 'tipo' y devolvé {"tipo": <valor>}.
# Pista: request.args.get("tipo").
# Ejemplo:  GET /buscar?tipo=Fuego  →  {"tipo": "Fuego"}
@app.route("/buscar")
def buscar():
    # TU CÓDIGO ACÁ
    pass


# Calcular con el path
# En "/doble/<int:n>", devolvé {"resultado": n * 2}.
# Ejemplo:  GET /doble/21  →  {"resultado": 42}
@app.route("/doble/<int:n>")
def doble(n):
    # TU CÓDIGO ACÁ
    pass


# /triple/<int:n> → {"resultado": n * 3}
@app.route("/triple/<int:n>")
def triple(n):
    # TU CÓDIGO ACÁ
    pass


# /cuadrado/<int:n> → {"resultado": n * n}
@app.route("/cuadrado/<int:n>")
def cuadrado(n):
    # TU CÓDIGO ACÁ
    pass


# /eco/<texto> → {"texto": texto}
@app.route("/eco/<texto>")
def eco(texto):
    # TU CÓDIGO ACÁ
    pass


# /mayuscula/<texto> → el texto en MAYÚSCULAS (como texto, no JSON)
@app.route("/mayuscula/<texto>")
def mayuscula(texto):
    # TU CÓDIGO ACÁ
    pass


# /largo/<texto> → {"largo": cantidad de caracteres}
@app.route("/largo/<texto>")
def largo(texto):
    # TU CÓDIGO ACÁ
    pass


# /suma/<int:a>/<int:b> → {"suma": a + b}
@app.route("/suma/<int:a>/<int:b>")
def suma(a, b):
    # TU CÓDIGO ACÁ
    pass


# /resta/<int:a>/<int:b> → {"resta": a - b}
@app.route("/resta/<int:a>/<int:b>")
def resta(a, b):
    # TU CÓDIGO ACÁ
    pass


# /es-par/<int:n> → {"par": True/False según si n es par}
@app.route("/es-par/<int:n>")
def es_par(n):
    # TU CÓDIGO ACÁ
    pass


# /saludar → leé la query 'nombre' y devolvé {"saludo": "Hola <nombre>"}.
# Ejemplo:  GET /saludar?nombre=Ash  →  {"saludo": "Hola Ash"}
@app.route("/saludar")
def saludar():
    # TU CÓDIGO ACÁ
    pass


# /nivel → leé la query 'valor', convertila a int y devolvé {"nivel": valor}.
# Ejemplo:  GET /nivel?valor=25  →  {"nivel": 25}
@app.route("/nivel")
def nivel():
    # TU CÓDIGO ACÁ
    pass


# /repetir/<texto>/<int:veces> → {"resultado": texto repetido 'veces' veces}
# Ejemplo:  GET /repetir/ab/3  →  {"resultado": "ababab"}
@app.route("/repetir/<texto>/<int:veces>")
def repetir(texto, veces):
    # TU CÓDIGO ACÁ
    pass


# /invertir/<texto> → el texto al revés (como texto)
@app.route("/invertir/<texto>")
def invertir(texto):
    # TU CÓDIGO ACÁ
    pass


# /rango/<int:n> → {"numeros": [1, 2, ..., n]}
@app.route("/rango/<int:n>")
def rango(n):
    # TU CÓDIGO ACÁ
    pass


# /multiplicar/<int:a>/<int:b> → {"resultado": a * b}
@app.route("/multiplicar/<int:a>/<int:b>")
def multiplicar(a, b):
    # TU CÓDIGO ACÁ
    pass


# /inicial/<texto> → la primera letra del texto (como texto)
@app.route("/inicial/<texto>")
def inicial(texto):
    # TU CÓDIGO ACÁ
    pass


# /negativo/<int:n> → {"resultado": -n}
@app.route("/negativo/<int:n>")
def negativo(n):
    # TU CÓDIGO ACÁ
    pass
