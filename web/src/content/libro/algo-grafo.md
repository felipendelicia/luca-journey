---
title: "Algoritmos: Grafos"
order: 1205
---

> 🎯 **Meta:** representar **redes de conexiones** (mapas, amigos, rutas) y consultarlas.

---

Un **grafo** son **nodos** conectados por **aristas**. Modela todo lo que sea una red: el mapa de rutas entre ciudades, los amigos de una red social, las páginas enlazadas de internet.

## Representación: diccionario de adyacencia

La forma más práctica en Python: un diccionario donde cada nodo apunta a la lista de sus vecinos.

```python
grafo = {
    "Pueblo Paleta": ["Ciudad Verde"],
    "Ciudad Verde": ["Pueblo Paleta", "Ciudad Plateada"],
    "Ciudad Plateada": ["Ciudad Verde"],
}
```

## Consultas básicas

```python
def vecinos(grafo, nodo):
    return grafo.get(nodo, [])        # [] si el nodo no existe

def grado(grafo, nodo):
    return len(vecinos(grafo, nodo))  # cuántas conexiones tiene

def hay_arista(grafo, a, b):
    return b in vecinos(grafo, a)     # ¿a conecta con b?
```

`grafo.get(nodo, [])` es clave: si pedís un nodo que no está, devuelve lista vacía en vez de romper.

## ¿Para qué?

Sobre grafos corren los algoritmos más famosos: encontrar el **camino más corto** (GPS), detectar **comunidades** (redes sociales), ordenar **dependencias** (qué instalar primero). Recorrerlos usa pila (DFS) o cola (BFS) — por eso vinieron antes.

## ✅ Comprobá lo que aprendiste

```quiz
P: Un grafo como "diccionario de adyacencia" mapea…
+ cada nodo → la lista de sus vecinos
- cada nodo → un único valor
- números → nodos
> `{nodo: [vecinos]}` es la forma más práctica en Python.
```

```quiz
P: `grafo.get(nodo, [])` sirve para…
+ devolver `[]` si el nodo no existe (en vez de romper)
- agregar un nodo nuevo
- ordenar los nodos
> Evita el `KeyError` dando una lista vacía por defecto.
```

🕸️ La **Líder Ryme** te espera para tejer su red.
