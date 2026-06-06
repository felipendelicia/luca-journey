---
title: "Algoritmos: Cola (queue)"
order: 1203
---

> 🎯 **Meta:** dominar la **cola** (FIFO), la estructura de los turnos y de recorrer "a lo ancho".

---

Una **cola** es como la fila del Centro Pokémon: el primero que llega es el primero que se atiende. **FIFO**: *first in, first out*.

## Operaciones

```python
cola = []
cola.append("a")    # encolar: al final
cola.append("b")
primero = cola.pop(0)   # atender: del frente  → "a"
```

> ⚠️ `pop(0)` sobre una lista grande es lento (mueve todos los elementos). Para colas de verdad se usa `collections.deque`, que saca del frente al instante:
> ```python
> from collections import deque
> cola = deque(["a", "b"])
> cola.popleft()   # "a", rapidísimo
> ```

## Pila vs cola

La diferencia es de dónde sacás:

| | Saca de… | Sirve para… |
|---|---|---|
| **Pila** (LIFO) | arriba (`pop()`) | deshacer, recursión |
| **Cola** (FIFO) | el frente (`pop(0)`) | turnos, BFS |

## ¿Para qué sirve?

- Sistemas de **turnos** y tareas (el que pidió primero se atiende primero).
- Recorrer un grafo **a lo ancho** (BFS): se visitan los nodos por cercanía usando una cola.

🚶 El **Líder Kofu** te espera con la fila de su restaurante.
