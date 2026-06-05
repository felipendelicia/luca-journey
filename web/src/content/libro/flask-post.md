---
title: "Flask: métodos y POST"
order: 340
---

> 🎯 **Meta:** que tu API **reciba datos** del cliente con **POST**. Hasta ahora solo entregabas; ahora también recibís.

`GET` sirve para **leer**. Pero cuando el cliente quiere **enviar** algo (crear un Pokémon, mandar un formulario), usa **`POST`**, con los datos en el **cuerpo** del pedido (en JSON).

## 📨 Aceptar POST

Por defecto una ruta solo acepta GET. Para aceptar POST lo decís con `methods`.

```python
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/eco", methods=["POST"])
def eco():
    datos = request.json       # lo que mandó el cliente (un dict)
    return jsonify(datos)      # se lo devolvemos igual

c = app.test_client()
r = c.post("/eco", json={"nombre": "Mew", "nivel": 70})
print(r.get_json())            # {'nombre': 'Mew', 'nivel': 70}
```

> 💡 `request.json` te da el cuerpo del pedido ya convertido a diccionario. En el cliente, `c.post(url, json={...})` manda ese cuerpo.

```quiz
P: ¿Cómo se lee el cuerpo JSON que mandó el cliente en una ruta POST de Flask?
- `request.args.get("datos")`
- `request.body`
+ `request.json`
> `request.json` parsea automáticamente el cuerpo JSON del pedido y te da un diccionario. `request.args` es para la query string (lo del `?`).
```

## ➕ Usar los datos recibidos

```python
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/sumar", methods=["POST"])
def sumar():
    d = request.json
    return jsonify({"suma": d["a"] + d["b"]})

c = app.test_client()
print(c.post("/sumar", json={"a": 25, "b": 17}).get_json())   # {'suma': 42}
```

```quiz
P: ¿Qué código de estado HTTP se usa por convención cuando una API **crea** un recurso nuevo?
- `200`
- `404`
+ `201`
> `200` significa "OK" (pedido procesado). `201` significa "Creado": se usa cuando el resultado del POST fue crear algo nuevo. `404` es "no encontrado".
```

## 🏷️ Devolver un código de estado

Cuando **creás** algo, la convención es responder **201** (creado). Devolvés una tupla `(respuesta, código)`.

```python
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/crear", methods=["POST"])
def crear():
    nombre = request.json["nombre"]
    return jsonify({"creado": nombre}), 201   # 👈 el 201

c = app.test_client()
r = c.post("/crear", json={"nombre": "Pikachu"})
print(r.status_code)     # 201
print(r.get_json())      # {'creado': 'Pikachu'}
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `@app.route("/x", methods=["POST"])` | aceptar POST en esa ruta |
| `request.json` | leer el cuerpo JSON del pedido |
| `return jsonify(...), 201` | responder con un código de estado |
| `c.post(url, json={...})` | (cliente) mandar datos por POST |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/flask-post). 💪

> ⚡ *"GET pregunta, POST entrega. Con los dos, tu API conversa."*
