---
title: "Python: Módulos y pip"
order: 95
---

> 🎯 **Meta:** usar código que ya escribieron otros. Vas a aprender a importar **módulos** de Python, instalar **librerías** con pip, y hasta consultar datos **reales de internet** con la PokéAPI.

---

## 🎮 Analogía: las MT (Máquinas Técnicas)

En los juegos Pokémon, las **MT** te enseñan ataques poderosos sin tener que entrenarlos desde cero. Las metés y listo, tu Pokémon ya sabe Rayo.

Los **módulos** y **librerías** son las MT del programador: código ya hecho que **importás** y usás. No reinventás la rueda: aprovechás el trabajo de millones de personas. 🧠

---

## 📦 import: traer un módulo

Un **módulo** es un archivo de Python lleno de funciones útiles. Python trae muchos "de fábrica" (la **librería estándar**). Para usarlos, los importás.

```python
import math

print(math.sqrt(16))    # 4.0  (raíz cuadrada)
print(math.pi)          # 3.141592653589793
print(math.ceil(4.2))   # 5    (redondea para arriba)
```

### Formas de importar

```python
import math                  # importás todo el módulo, usás math.algo
from math import sqrt        # importás solo sqrt, lo usás directo
from math import sqrt, pi    # varios
import math as m             # le ponés un apodo: m.sqrt(16)
```

---

## 🧰 Módulos estándar útiles

### `math` — matemática
```python
import math
math.sqrt(25)     # 5.0
math.ceil(4.1)    # 5
math.floor(4.9)   # 4
math.pow(2, 3)    # 8.0
```

### `random` — azar
```python
import random
random.randint(1, 6)               # número al azar entre 1 y 6 (dado)
random.choice(["Pikachu", "Onix"]) # elige uno al azar de la lista
random.shuffle(equipo)             # mezcla la lista (la modifica)
```

### `datetime` — fechas y horas
```python
from datetime import datetime, date
date.today()                  # la fecha de hoy
datetime.now()                # fecha y hora ahora
date.today().isoformat()      # "2024-06-04" (texto estándar)
datetime.now().year           # el año actual
```

### `os` y `sys` — sistema
```python
import os
os.path.exists("datos.txt")   # ¿existe el archivo? True/False
os.path.basename("/a/b/c.txt")# "c.txt" (solo el nombre)

import sys
sys.argv          # lista de argumentos pasados al programa
sys.exit()        # termina el programa
```

### `json` — guardar/cargar datos estructurados
```python
import json

datos = {"nombre": "Pikachu", "nivel": 25}

texto = json.dumps(datos)        # dict -> texto JSON
print(texto)                      # {"nombre": "Pikachu", "nivel": 25}

recuperado = json.loads(texto)   # texto JSON -> dict
print(recuperado["nombre"])      # Pikachu

# Guardar y cargar archivos JSON
with open("pokemon.json", "w") as f:
    json.dump(datos, f)
with open("pokemon.json", "r") as f:
    datos = json.load(f)
```

> 💡 JSON es **el formato** para guardar datos estructurados. Lo vas a usar en los proyectos finales. ¡Prestale atención!

---

## 🏗️ Crear tu propio módulo

Cualquier archivo `.py` tuyo es un módulo que podés importar desde otro archivo. ¡Así organizás proyectos grandes!

Archivo `pokeutils.py`:
```python
def formatear_nombre(nombre):
    return nombre.capitalize()

def es_legendario(nombre):
    return nombre.lower() in ["mewtwo", "mew", "articuno"]
```

Archivo `main.py` (en la misma carpeta):
```python
import pokeutils

print(pokeutils.formatear_nombre("pikachu"))   # Pikachu
print(pokeutils.es_legendario("Mewtwo"))       # True
```

> 💡 Acá tenés un `pokeutils.py` de ejemplo. Miralo: así se ven los módulos propios.

---

## 🛒 pip: instalar librerías externas

La librería estándar es enorme, pero a veces necesitás algo que no viene. **pip** es el instalador de paquetes de Python: tu PokéMart de librerías.

```bash
pip install requests       # instala la librería 'requests'
pip install flask          # instala Flask (para apps web)
pip list                   # muestra lo que tenés instalado
pip uninstall requests     # la desinstala
```

---

## 📦 venv: entornos virtuales

Un **entorno virtual (venv)** es una "cajita" aislada con sus propias librerías, separada del Python del sistema. Así cada proyecto tiene sus versiones sin pisarse.

```bash
python3 -m venv venv          # crea el entorno en la carpeta 'venv'
source venv/bin/activate      # lo activás (Linux/Mac)
pip install requests          # instala DENTRO del venv
deactivate                    # lo desactivás
```

> 💡 El `setup.sh` del curso hace esto por vos. Pero ahora entendés qué hace. 😎

---

## 📋 requirements.txt

Un archivo `requirements.txt` lista las librerías que tu proyecto necesita, para que cualquiera las instale de un saque:

```
requests>=2.31
flask>=3.0
```

Se instalan todas juntas con:
```bash
pip install -r requirements.txt
```

---

## 🌐 requests: consumir una API

Una **API** es un servicio en internet que te devuelve datos. La **PokéAPI** (https://pokeapi.co) tiene datos de TODOS los Pokémon, gratis.

La librería **requests** te deja pedir esos datos:

```python
import requests

# Pedimos los datos de Pikachu.
respuesta = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")

# .json() convierte la respuesta a un diccionario de Python.
datos = respuesta.json()

print(datos["name"])                    # pikachu
print(datos["height"])                  # altura
print(datos["weight"])                  # peso
print(datos["types"][0]["type"]["name"])# electric
```

> ⚠️ Para usar `requests` necesitás internet y tenerla instalada (`pip install requests`). Tené en cuenta el caso de "no hay internet" para que tu código no se rompa.

---

## 📝 Resumen

```python
# Importar módulos estándar
import math, random, json, os
from datetime import date

math.sqrt(16)               # 4.0
random.choice(["a", "b"])  # uno al azar
json.dumps({"x": 1})       # '{"x": 1}'
date.today().isoformat()    # fecha de hoy

# Módulo propio
import pokeutils
pokeutils.formatear_nombre("pikachu")

# Instalar librerías
# pip install requests
# pip install -r requirements.txt

# Consumir una API
import requests
datos = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu").json()
```

| Concepto | Para qué sirve |
|----------|----------------|
| `import` | Traer código de otros |
| `math/random/json/os/datetime` | Módulos estándar |
| módulo propio | Tu propio `.py` reutilizable |
| `pip` | Instalar librerías externas |
| `venv` | Entorno aislado por proyecto |
| `requirements.txt` | Lista de dependencias |
| `requests` | Pedir datos a una API |

---

## ➡️ ¿Y ahora qué?

Ahora **practicá**: andá a los [ejercicios de este tema](/ejercicios/modulos-y-pip) y resolvelos. Se corrigen al instante con tests reales en tu navegador. 💪

> ⚡ *"El mejor programador no es el que escribe más código, sino el que sabe reusar el de los demás."*
