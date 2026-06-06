---
title: "Algoritmos: Analizá la Pokédex"
order: 1207
---

> 🎯 **Meta:** combinar **búsqueda, orden y conteo** en un análisis real de datos.

---

Llegaste al final de Paldea. Ahora juntás todo lo aprendido sobre una lista de Pokémon, donde cada uno es un diccionario:

```python
pokes = [
    {"nombre": "Squirtle", "tipo": "agua", "nivel": 16},
    {"nombre": "Charmander", "tipo": "fuego", "nivel": 9},
    {"nombre": "Gyarados", "tipo": "agua", "nivel": 30},
]
```

## Agrupar (diccionarios)

```python
def por_tipo(pokes):
    grupos = {}
    for p in pokes:
        grupos.setdefault(p["tipo"], []).append(p["nombre"])
    return grupos
# {"agua": ["Squirtle", "Gyarados"], "fuego": ["Charmander"]}
```

## Ordenar (con clave)

```python
def ordenar(pokes):
    return sorted(pokes, key=lambda p: p["nivel"], reverse=True)
```

`key=lambda p: p["nivel"]` le dice a `sorted` por qué campo ordenar; `reverse=True`, de mayor a menor.

## Encontrar el mejor

```python
def mas_fuerte(pokes):
    return max(pokes, key=lambda p: p["nivel"])["nombre"] if pokes else ""
```

El mismo patrón `key=...` sirve para `sorted`, `max` y `min`. Domínalo y resolvés media programación de datos.

## Lo que aprendiste en Paldea

Búsqueda, orden, pilas, colas, recursión, grafos y tablas hash: las **estructuras de datos y algoritmos** que son la base de toda la informática. Con esto pensás soluciones, no solo código.

🏆 La **Líder Grusha** y la **Campeona Geeta** te esperan para coronarte **Campeón de Paldea**.
