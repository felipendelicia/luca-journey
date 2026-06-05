---
title: "Flask: tu primera app"
order: 310
---

> 🎯 **Meta:** crear tu **primera API con Flask**. Con pocas líneas vas a tener un servidor que responde pedidos.

**Flask** es una librería de Python para crear servidores web y APIs. Es chiquita y fácil: en 5 líneas tenés algo andando.

## 🧱 La estructura mínima

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "¡Hola, mundo Pokémon!"
```

Tres piezas:
- `app = Flask(__name__)` → crea la aplicación.
- `@app.route("/")` → dice **en qué dirección** responde la función (la ruta `/`).
- la función → devuelve la **respuesta**.

> 💡 `@app.route(...)` es un **decorador**: "engancha" la función de abajo a una URL. Cuando alguien pide esa URL, Flask llama a tu función.

```quiz
P: ¿Qué hace `@app.route("/ping")` en Flask?
- Crea una variable llamada `ping`.
- Instala la ruta en el servidor de producción.
+ Conecta la función que está abajo a la URL `/ping`: cuando alguien pide esa URL, Flask llama a esa función.
> `@app.route(...)` es un decorador. "Engancha" la función siguiente a la URL indicada. Sin él, Flask no sabe que esa función existe.
```

## 🧪 Probar sin servidor: test_client

Normalmente la app se prende con `app.run()` y queda escuchando. Pero para **probar** (¡y para correr acá en el navegador!) usamos el **cliente de pruebas**, que simula pedidos sin levantar un servidor real.

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "¡Bienvenido a la Pokédex API!"

@app.route("/ping")
def ping():
    return "pong"

# simulamos pedidos (en vez de app.run())
cliente = app.test_client()
print(cliente.get("/").get_data(as_text=True))
print(cliente.get("/ping").get_data(as_text=True))
print("status:", cliente.get("/ping").status_code)
```

> 💡 Tocá **▶ ejecutar**: corre Flask de verdad en tu navegador y ves las respuestas. La primera vez tarda un poco más porque instala Flask.

```quiz
P: ¿Para qué sirve `app.test_client()` en Flask?
- Para prender el servidor y escuchar pedidos reales.
- Para instalar Flask automáticamente.
+ Para simular pedidos HTTP sin levantar un servidor real, ideal para probar.
> `test_client()` simula un cliente que hace `GET`, `POST`, etc. contra tu app sin necesitar internet ni un puerto abierto. Perfecto para tests y para practicar en el navegador.
```

## 🛣️ Muchas rutas

Una app puede tener todas las rutas que quieras, cada una con su función.

```python
from flask import Flask
app = Flask(__name__)

@app.route("/hola")
def hola():
    return "Hola, Entrenador"

@app.route("/version")
def version():
    return "1.0"

c = app.test_client()
print(c.get("/hola").get_data(as_text=True))
print(c.get("/version").get_data(as_text=True))
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `from flask import Flask` | traer Flask |
| `app = Flask(__name__)` | crear la app |
| `@app.route("/ruta")` | conectar una función a una URL |
| `return "..."` | la respuesta |
| `app.test_client()` | simular pedidos para probar |
| `app.run()` | (en tu compu) prender el servidor real |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/flask-primera-app). 💪

> ⚡ *"Cinco líneas y ya tenés un servidor. Bienvenido al backend."*
