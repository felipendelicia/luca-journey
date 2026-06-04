---
title: "Proyecto: Pokédex API"
order: 370
---

> 🎯 **Meta:** juntar **todo Hoenn** en una **API REST completa** de Pokémon: listar, buscar, obtener por id y crear. Tu primer backend de verdad.

Llegaste al final de Hoenn. 🌧️ Ahora armás una **Pokédex API** que junta todo: rutas, JSON, parámetros de path y query, POST y manejo de errores.

## 🏗️ La app completa

```python
from flask import Flask, jsonify, request
app = Flask(__name__)

POKEDEX = [
    {"id": 1, "nombre": "Bulbasaur", "tipo": "Planta"},
    {"id": 2, "nombre": "Charmander", "tipo": "Fuego"},
    {"id": 3, "nombre": "Squirtle", "tipo": "Agua"},
    {"id": 4, "nombre": "Vulpix", "tipo": "Fuego"},
]

@app.route("/pokedex")
def listar():
    return jsonify(POKEDEX)

@app.route("/pokedex/<int:pid>")
def obtener(pid):
    for p in POKEDEX:
        if p["id"] == pid:
            return jsonify(p)
    return jsonify({"error": "no existe"}), 404

@app.route("/buscar")
def buscar():
    tipo = request.args.get("tipo")
    return jsonify([p for p in POKEDEX if p["tipo"] == tipo])

@app.route("/pokedex", methods=["POST"])
def agregar():
    nuevo = request.json
    POKEDEX.append(nuevo)
    return jsonify(nuevo), 201
```

## ▶️ Probándola

```python
from flask import Flask, jsonify, request
app = Flask(__name__)
POKEDEX = [
    {"id": 1, "nombre": "Bulbasaur", "tipo": "Planta"},
    {"id": 2, "nombre": "Charmander", "tipo": "Fuego"},
    {"id": 4, "nombre": "Vulpix", "tipo": "Fuego"},
]

@app.route("/pokedex")
def listar():
    return jsonify(POKEDEX)

@app.route("/buscar")
def buscar():
    tipo = request.args.get("tipo")
    return jsonify([p for p in POKEDEX if p["tipo"] == tipo])

c = app.test_client()
print("todos:", [p["nombre"] for p in c.get("/pokedex").get_json()])
print("fuego:", [p["nombre"] for p in c.get("/buscar?tipo=Fuego").get_json()])
```

## 🗺️ Lo que aprendiste en Hoenn

1. **HTTP + JSON**: cómo hablan los programas.
2. **Flask**: crear una app y rutas.
3. **JSON responses**: devolver datos con `jsonify`.
4. **Parámetros**: path (`/pokedex/<id>`) y query (`?tipo=`).
5. **POST**: recibir datos y responder `201`.
6. **CRUD + errores**: el patrón REST y el `404`.
7. **Consumir**: procesar respuestas de otras APIs.

Con esto ya entendés cómo funciona el **backend** de casi cualquier app moderna. 🚀

## ➡️ ¿Y ahora qué?

Cerrá Hoenn con los [ejercicios de este tema](/ejercicios/pokedex-api). Al completarlos ganás la medalla **Lluvia** y sos **Campeón de Hoenn**. 🌧️🏆

> ⚡ *"Construiste una API. Ahora el mundo puede pedirle datos a tu código."*
