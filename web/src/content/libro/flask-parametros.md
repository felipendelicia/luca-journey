---
title: "Flask: parámetros"
order: 330
---

> 🎯 **Meta:** que tu API reciba **datos en la URL**: un id en el path (`/pokemon/25`) o filtros en la query (`/buscar?tipo=Fuego`).

Una API útil responde **distinto según lo que le pidas**. ¿El Pokémon número 25? ¿Los de tipo Fuego? Esos datos viajan en la **URL**.

## 🔢 Parámetros en el path

Ponés una parte **variable** de la URL entre `<...>`. Flask te la pasa como argumento a la función.

```python
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/pokemon/<int:n>")
def pokemon(n):
    return jsonify({"id": n, "nombre": f"Pokémon #{n}"})

c = app.test_client()
print(c.get("/pokemon/25").get_json())   # {'id': 25, 'nombre': 'Pokémon #25'}
print(c.get("/pokemon/1").get_json())
```

> 💡 `<int:n>` dice que `n` es un **número**. Sin `int:` llegaría como texto. También podés usar `<nombre>` para texto.

## 🔤 Parámetros de texto

```python
from flask import Flask
app = Flask(__name__)

@app.route("/saludo/<nombre>")
def saludo(nombre):
    return f"Hola, {nombre}"

c = app.test_client()
print(c.get("/saludo/Ash").get_data(as_text=True))   # Hola, Ash
```

## ❓ Query strings: filtros con ?

Lo que va después del `?` en la URL son **parámetros de consulta**. Se leen con `request.args`.

```python
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/buscar")
def buscar():
    tipo = request.args.get("tipo")          # de /buscar?tipo=Fuego
    return jsonify({"buscando": tipo})

c = app.test_client()
print(c.get("/buscar?tipo=Fuego").get_json())   # {'buscando': 'Fuego'}
```

> 💡 Path vs query: el **path** (`/pokemon/25`) identifica un recurso; la **query** (`?tipo=Fuego`) filtra o ajusta el pedido. Los dos llegan por la URL.

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `@app.route("/x/<int:n>")` | parte variable numérica del path |
| `@app.route("/x/<nombre>")` | parte variable de texto |
| la función recibe esos valores como **argumentos** | |
| `request.args.get("clave")` | leer un parámetro de la query (`?clave=...`) |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/flask-parametros). 💪

> ⚡ *"Una buena API responde la pregunta exacta que le hacés."*
