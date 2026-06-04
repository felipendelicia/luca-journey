---
title: "Consumir una API"
order: 360
---

> 🎯 **Meta:** estar del **otro lado** del mostrador: ser el **cliente** que le pide datos a una API (como la PokéAPI) y procesa la respuesta.

Hasta ahora **construiste** APIs. Ahora vas a **usar** una. Tu programa hace un pedido a una API externa y trabaja con el JSON que recibe.

## 🌐 Cómo se pide (concepto)

En una compu normal, para pedirle datos a una API se usa la librería **`requests`**:

```python
# (así se ve en tu compu; necesita internet y la librería requests)
import requests

respuesta = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")
datos = respuesta.json()      # convierte el JSON a diccionario
print(datos["name"])          # pikachu
```

> ⚠️ Hacer pedidos de red **de verdad** desde el navegador tiene límites (CORS, permisos). Por eso acá practicamos la parte clave y siempre necesaria: **procesar la respuesta** que te da la API. El pedido lo simulamos con el JSON ya recibido.

## 🔎 Procesar la respuesta

Lo que recibís es JSON (texto). Lo convertís a Python y extraés lo que necesitás.

```python
import json

# así viene la respuesta de la API (texto JSON)
respuesta = '{"name": "charizard", "tipos": ["fuego", "volador"], "nivel": 90}'

datos = json.loads(respuesta)
print("nombre:", datos["name"])
print("tipos:", datos["tipos"])
print("primer tipo:", datos["tipos"][0])
```

## 📋 Recorrer listas de resultados

Muchas APIs devuelven `{"results": [...]}`. Recorrés esa lista.

```python
import json

respuesta = '{"results": [{"name": "bulbasaur"}, {"name": "ivysaur"}, {"name": "venusaur"}]}'
datos = json.loads(respuesta)

print("cantidad:", len(datos["results"]))
for p in datos["results"]:
    print("-", p["name"])
```

## ⚠️ Manejar errores

No siempre sale bien. Revisás el **código de estado** antes de confiar en los datos.

```python
import json

def procesar(status, texto):
    if status == 200:
        return json.loads(texto)
    return None     # algo falló (404, 500, ...)

print(procesar(200, '{"ok": 1}'))   # {'ok': 1}
print(procesar(404, 'Not Found'))   # None
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `requests.get(url)` | (en tu compu) pedir datos a una API |
| `respuesta.json()` | convertir la respuesta a diccionario |
| `json.loads(texto)` | procesar JSON recibido |
| revisar `status` | manejar errores antes de usar los datos |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/consumir-api). 💪

> ⚡ *"Saber pedir y saber procesar: con eso, todas las APIs del mundo son tuyas."*
