---
title: "Automatización: Scripts y argumentos"
order: 1000
---

> 🎯 **Meta:** convertir tu código en un **script** que se ejecuta desde la terminal y recibe **argumentos**, el primer paso de toda automatización.

---

Hasta ahora corriste código en el editor. Pero una **automatización** vive en un archivo `.py` que ejecutás desde la terminal, muchas veces sin tocar nada:

```bash
python bot.py --nivel 30 --shiny
```

Esos `--nivel 30 --shiny` son **argumentos**. Tu programa los lee y se comporta distinto según lo que le pasen. Es lo que hace que un mismo script sirva para mil situaciones.

## `sys.argv`: los argumentos crudos

Python te da los argumentos en `sys.argv`, una **lista de textos**. El truco que confunde a todos: **el primero (`sys.argv[0]`) es el nombre del script**, no un argumento de verdad.

```python
import sys
print("script:", sys.argv[0])
print("argumentos:", sys.argv[1:])
print("cantidad real:", len(sys.argv) - 1)
```

Como es una lista común, podés preguntar cosas a mano:

```python
argv = ["bot.py", "--nivel", "30", "--shiny"]
print("--shiny" in argv)              # True  → ¿está la bandera?
i = argv.index("--nivel")             # posición de la opción
print(argv[i + 1])                    # "30"  → el valor que viene justo después
```

> ⚠️ Ojo: todo en `sys.argv` es **texto**. Si querés un número, convertilo con `int(...)`.

## `argparse`: la forma profesional

Leer a mano funciona, pero se vuelve un lío con muchas opciones. El módulo **`argparse`** (de la librería estándar) lo hace por vos: define las opciones, valida tipos y hasta arma el `--help`.

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nivel", type=int, default=1)      # número, por defecto 1
parser.add_argument("--nombre", default="Pikachu")        # texto
parser.add_argument("--shiny", action="store_true")       # bandera: True si está

args = parser.parse_args(["--nivel", "30", "--shiny"])
print(args.nivel, args.nombre, args.shiny)   # 30 Pikachu True
print(vars(args))    # {'nivel': 30, 'nombre': 'Pikachu', 'shiny': True}
```

Tres cosas clave:

- `type=int` convierte solo: `args.nivel` ya es un entero.
- `default=...` es el valor si la opción no aparece.
- `action="store_true"` hace una **bandera**: `True` si está, `False` si no.
- `vars(args)` convierte el resultado en un **diccionario** común.

> 💡 En un script real usarías `parser.parse_args()` **sin argumentos**, y `argparse` lee de `sys.argv` solo. Acá le pasamos la lista a mano para poder probarlo.

Con esto ya podés escribir scripts que se configuran desde afuera. En los ejercicios vas a leer argumentos a mano y con `argparse`. ⚡ El **Líder Ilima** te espera en el gimnasio.
