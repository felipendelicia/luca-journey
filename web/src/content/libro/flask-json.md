---
title: "Flask: respuestas JSON"
order: 320
---

> 🎯 **Meta:** que tu API devuelva **JSON** (no texto suelto). Así otros programas pueden usar tus datos.

Una API de verdad no devuelve `"Pikachu"`: devuelve **datos estructurados** en JSON, como `{"nombre": "Pikachu", "nivel": 25}`. Para eso está **`jsonify`**.

## 📦 jsonify: convertir a respuesta JSON

`jsonify` toma un diccionario (o lista) de Python y arma la respuesta JSON con los headers correctos.

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/pokemon")
def pokemon():
    return jsonify({"nombre": "Pikachu", "nivel": 25})

c = app.test_client()
r = c.get("/pokemon")
print(r.get_json())            # {'nombre': 'Pikachu', 'nivel': 25}
print(r.headers["Content-Type"])   # application/json
```

> 💡 `r.get_json()` te devuelve la respuesta ya convertida a diccionario de Python. Es lo que usás para leer lo que mandó la API.

## 📋 Devolver listas

```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/equipo")
def equipo():
    return jsonify(["Pikachu", "Charizard", "Snorlax"])

c = app.test_client()
print(c.get("/equipo").get_json())
```

## 🗂️ Una mini Pokédex

Podés armar respuestas tan ricas como quieras: diccionarios con listas adentro, etc.

```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/pokedex")
def pokedex():
    return jsonify({
        "region": "Kanto",
        "pokemon": [
            {"nombre": "Bulbasaur", "tipo": "Planta"},
            {"nombre": "Charmander", "tipo": "Fuego"},
        ],
    })

c = app.test_client()
datos = c.get("/pokedex").get_json()
print(datos["region"])
print(datos["pokemon"][0]["nombre"])
```

> 💡 En Flask moderno también podés `return {"clave": valor}` (un dict) directo y lo convierte solo. Pero `jsonify` es lo clásico y deja todo explícito.

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `from flask import jsonify` | traer jsonify |
| `return jsonify({...})` | devolver un dict como JSON |
| `return jsonify([...])` | devolver una lista como JSON |
| `respuesta.get_json()` | leer el JSON de la respuesta (lado cliente) |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/flask-json). 💪

> ⚡ *"Texto suelto lo entiende un humano. JSON lo entiende el mundo entero."*
