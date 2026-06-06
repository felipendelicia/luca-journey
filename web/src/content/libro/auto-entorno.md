---
title: "Automatización: Variables de entorno y config"
order: 1004
---

> 🎯 **Meta:** sacar contraseñas, claves y rutas FUERA del código, leyéndolas del **entorno** o de un archivo de config.

---

Regla de oro de la automatización: **nunca escribas una contraseña o una API key en el código**. Si lo hacés, se filtra al subirlo a Git. En cambio, los datos sensibles viven en el **entorno** o en un archivo de configuración.

## Variables de entorno

El sistema operativo guarda variables que tu programa puede leer con `os.environ`:

```python
import os

# .get(clave, defecto): devuelve el valor, o el defecto si no existe
api_key = os.environ.get("POKE_API_KEY", "sin-clave")
debug = os.environ.get("DEBUG", "0")
print(api_key, debug)
```

En la terminal las definís antes de correr el script:

```bash
POKE_API_KEY=abc123 DEBUG=1 python bot.py
```

> ⚠️ Todo lo que sale del entorno es **texto**. `"1"`, no `1`; `"true"`, no `True`. Si querés un número o un booleano, lo convertís vos.

## El archivo `.env`

Para no tipear las variables cada vez, se usa un archivo `.env` (que **no** se sube a Git):

```text
# config del bot
POKE_API_KEY=abc123
DEBUG=1
NIVEL=info
```

Parsearlo es leer líneas `CLAVE=valor`, ignorando vacías y comentarios:

```python
config = {}
for linea in texto.splitlines():
    linea = linea.strip()
    if not linea or linea.startswith("#"):
        continue
    clave, valor = linea.split("=", 1)   # partir en el PRIMER =
    config[clave.strip()] = valor.strip()
print(config)   # {"POKE_API_KEY": "abc123", "DEBUG": "1", "NIVEL": "info"}
```

## Valores por defecto

Una config robusta siempre tiene defectos, y lo que el usuario define los pisa:

```python
defectos = {"DEBUG": "0", "NIVEL": "info"}
final = {**defectos, **config}   # config gana donde coincida
```

🔑 El **Capitán Sophocles** te espera para armar un cargador de configuración.
