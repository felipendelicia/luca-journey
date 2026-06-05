---
title: "Flask: API REST (CRUD)"
order: 350
---

> 🎯 **Meta:** construir una **API REST** completa: las 4 operaciones (**CRUD**) sobre un recurso. Es el patrón que usan casi todas las APIs del mundo.

**CRUD** = **C**reate, **R**ead, **U**pdate, **D**elete. Una API REST le da a cada operación un método HTTP y una ruta. Vamos a manejar una Pokédex en memoria.

## 🗺️ El mapa REST

| Operación | Método | Ruta | Qué hace |
|-----------|--------|------|----------|
| Listar | GET | `/pokedex` | todos |
| Obtener | GET | `/pokedex/<id>` | uno |
| Crear | POST | `/pokedex` | agregar |
| Borrar | DELETE | `/pokedex/<id>` | eliminar |

> 💡 Fijate el patrón: la **misma ruta** (`/pokedex`) hace cosas distintas según el **método**. Eso es REST.

```quiz
P: En una API REST, ¿qué método HTTP y ruta se usan para **obtener un Pokémon específico** por su id?
- POST `/pokedex`
- DELETE `/pokedex/<id>`
+ GET `/pokedex/<id>`
> GET es para leer; la ruta con `<id>` identifica el recurso específico. POST crea, DELETE borra; la ruta sin id (`/pokedex`) opera sobre la colección completa.
```

## 📖 Read: listar y obtener

```python
from flask import Flask, jsonify
app = Flask(__name__)

POKEDEX = [
    {"id": 1, "nombre": "Bulbasaur"},
    {"id": 2, "nombre": "Charmander"},
]

@app.route("/pokedex")
def listar():
    return jsonify(POKEDEX)

@app.route("/pokedex/<int:pid>")
def obtener(pid):
    for p in POKEDEX:
        if p["id"] == pid:
            return jsonify(p)
    return jsonify({"error": "no existe"}), 404   # 👈 not found

c = app.test_client()
print(c.get("/pokedex").get_json())
print(c.get("/pokedex/2").get_json())
print("inexistente:", c.get("/pokedex/99").status_code)   # 404
```

> 💡 Cuando el recurso **no existe**, se responde **404**. Manejar el error es parte de hacer una buena API.

```quiz
P: ¿Qué código de estado devuelve la ruta cuando el Pokémon buscado **no existe**?
- `200`
- `201`
+ `404`
> `404` significa "Not Found": el recurso pedido no existe. Es importante manejarlo explícitamente (`return jsonify(...), 404`) para que el cliente entienda qué pasó.
```

## ➕ Create y 🗑️ Delete

```python
from flask import Flask, jsonify, request
app = Flask(__name__)
POKEDEX = [{"id": 1, "nombre": "Bulbasaur"}]

@app.route("/pokedex", methods=["POST"])
def agregar():
    nuevo = request.json
    POKEDEX.append(nuevo)
    return jsonify(nuevo), 201

@app.route("/pokedex/<int:pid>", methods=["DELETE"])
def borrar(pid):
    for p in POKEDEX:
        if p["id"] == pid:
            POKEDEX.remove(p)
            return jsonify({"borrado": pid})
    return jsonify({"error": "no existe"}), 404

c = app.test_client()
print(c.post("/pokedex", json={"id": 2, "nombre": "Pikachu"}).status_code)  # 201
print(c.delete("/pokedex/1").get_json())     # {'borrado': 1}
print([p["nombre"] for p in POKEDEX])        # ['Pikachu']
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| GET `/recurso` | listar todos |
| GET `/recurso/<id>` | obtener uno (o 404) |
| POST `/recurso` | crear (201) |
| DELETE `/recurso/<id>` | borrar (o 404) |
| `return ..., 404` | avisar que no existe |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/flask-rest-crud). 💪

> ⚡ *"CRUD es el alfabeto de las APIs. Sabiéndolo, leés cualquier backend."*
