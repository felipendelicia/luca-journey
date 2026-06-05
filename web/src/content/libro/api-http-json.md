---
title: "APIs: HTTP y JSON"
order: 300
---

> 🎯 **Meta:** entrar a **Hoenn**, la región de las **APIs**. Vas a aprender qué es una API, cómo hablan los programas por internet (**HTTP**) y en qué idioma (**JSON**).

Bienvenido a **Hoenn**. 🛰️ Acá aprendés a construir **APIs**: la forma en que los programas se piden datos entre sí. La Pokédex de tu celular le pide datos a un servidor; ese servidor tiene una **API**.

## 🎮 Analogía: la API es el mostrador del Centro Pokémon

Vos (el **cliente**) vas al mostrador y pedís algo ("curá mis Pokémon"). La enfermera Joy (el **servidor**) lo hace y te responde. No entrás a la cocina: pedís por el **mostrador**, con reglas claras. Eso es una **API**: un mostrador de datos.

| Concepto | Qué es |
|----------|--------|
| **Cliente** | quien pide (tu app, el navegador) |
| **Servidor** | quien responde (la API) |
| **Request** | el pedido |
| **Response** | la respuesta |

## 🌐 HTTP: el idioma de los pedidos

Cada pedido usa un **método** y recibe un **código de estado**:

| Método | Para qué |
|--------|----------|
| **GET** | pedir/leer datos |
| **POST** | enviar/crear datos |
| **PUT** | actualizar |
| **DELETE** | borrar |

| Código | Significa |
|--------|-----------|
| **200** | OK ✅ |
| **201** | creado |
| **404** | no encontrado |
| **500** | error del servidor |

```quiz
P: Cuando tu app hace un pedido HTTP para **leer** datos de una API, ¿qué método usás?
- POST
- DELETE
+ GET
> `GET` es para leer/pedir datos. `POST` crea, `PUT` actualiza, `DELETE` borra. Pedir la info de un Pokémon es un `GET`.
```

## 📦 JSON: el idioma de los datos

Las APIs mandan datos en **JSON**: texto con la misma pinta que un diccionario de Python.

```python
import json

# de Python a JSON (texto)
pokemon = {"nombre": "Pikachu", "nivel": 25}
texto = json.dumps(pokemon)
print(texto)            # '{"nombre": "Pikachu", "nivel": 25}'
print(type(texto))      # <class 'str'>

# de JSON (texto) a Python
de_vuelta = json.loads(texto)
print(de_vuelta["nombre"])   # Pikachu
```

> 💡 `json.dumps` = **d**ump **s**tring (Python → texto JSON). `json.loads` = **load** **s**tring (texto JSON → Python). El JSON viaja como texto por la red.

```quiz
P: ¿Qué hace `json.loads('{"nombre": "Pikachu"}')`?
- Convierte un diccionario de Python a texto JSON.
- Guarda el JSON en un archivo.
+ Convierte el texto JSON a un diccionario de Python.
> `loads` = **load string**: recibe texto JSON y devuelve Python. Al revés, `dumps` convierte de Python a texto JSON.
```

## 🔎 Procesar una respuesta

Cuando una API te responde, recibís JSON y lo convertís a Python para usarlo.

```python
import json

respuesta = '{"results": [{"name": "bulbasaur"}, {"name": "ivysaur"}]}'
datos = json.loads(respuesta)
print("cantidad:", len(datos["results"]))
print("primero:", datos["results"][0]["name"])
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| API | mostrador de datos (cliente ↔ servidor) |
| HTTP | el protocolo: métodos (GET/POST/...) y códigos (200/404...) |
| `json.dumps(obj)` | Python → texto JSON |
| `json.loads(texto)` | texto JSON → Python |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/api-http-json). 💪

> ⚡ *"Toda app que conocés le habla a una API. Ahora vas a construir la tuya."*
