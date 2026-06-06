---
title: "Automatización: Tu primer bot"
order: 1007
---

> 🎯 **Meta:** **encadenar** todo lo aprendido en un bot que procesa datos de punta a punta.

---

Un "bot" no es magia: es un **pipeline**, una cadena de pasos donde la salida de uno alimenta al siguiente. Casi todas las automatizaciones siguen la misma receta de tres tiempos:

1. **Cargar** los datos (de un archivo, una API, el entorno).
2. **Transformar**: limpiar, filtrar, agrupar, calcular.
3. **Reportar**: guardar o mostrar el resultado.

## Cada paso, una función

La clave es que cada paso sea una **función chiquita** y testeable. Así el bot se lee como una historia:

```python
def normalizar(nombre):
    return nombre.strip().lower()

def filtrar_nivel(pokes, minimo):
    return [p for p in pokes if p["nivel"] >= minimo]

def agrupar_por_tipo(pokes):
    grupos = {}
    for p in pokes:
        grupos.setdefault(p["tipo"], []).append(p["nombre"])
    return grupos
```

`setdefault(clave, [])` es un viejo truco para agrupar: si la clave no existe, la crea con una lista vacía, y después agrega.

## El pipeline completo

```python
pokes = [
    {"nombre": "Squirtle", "tipo": "agua", "nivel": 16},
    {"nombre": "Charmander", "tipo": "fuego", "nivel": 9},
    {"nombre": "Psyduck", "tipo": "agua", "nivel": 20},
]

listos = filtrar_nivel(pokes, 15)      # cargar → filtrar
grupos = agrupar_por_tipo(listos)      # transformar
print(f"{len(listos)} Pokémon listos")  # reportar
print(grupos)                          # {"agua": ["Squirtle", "Psyduck"]}
```

Eso es un bot: funciones simples conectadas. Si cada una está bien testeada, el todo funciona.

## Lo que aprendiste en Alola

Argumentos, archivos, lotes, procesos, configuración, tiempo y scraping: todas las piezas de la automatización. Ahora las juntás.

🤖 El **Kahuna Hala** y el **Profesor Kukui** te esperan para coronarte **Campeón de Alola**. ¡A automatizar!
