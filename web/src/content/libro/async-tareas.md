---
title: "Asincronía: Repartir tareas"
order: 1102
---

> 🎯 **Meta:** lanzar varias corrutinas **a la vez** con tareas, y entender cómo repartir trabajo parejo.

---

`await` de a una no acelera nada: esperás la primera, después la segunda… Lo potente es lanzar **muchas juntas**. Para eso existen las **tareas** (`asyncio.create_task`).

## Crear tareas

`asyncio.create_task(corrutina)` agenda la corrutina para que corra **ya**, en segundo plano, sin esperarla todavía:

```python
import asyncio

async def descargar(n):
    await asyncio.sleep(1)
    return n * 10

async def principal():
    t1 = asyncio.create_task(descargar(1))   # arrancan
    t2 = asyncio.create_task(descargar(2))   # las dos juntas
    a = await t1
    b = await t2
    print(a, b)   # 10 20  → tardó ~1s, no ~2s

asyncio.run(principal())
```

Como arrancaron juntas, el tiempo total es el de la más lenta, no la suma.

## Repartir el trabajo

Cuando tenés N tareas y K workers, conviene repartirlas **parejo** para que ninguno quede sobrecargado. El reparto **round-robin** da una a cada worker por turno:

```python
def repartir(tareas, n):
    buckets = [[] for _ in range(n)]
    for i, t in enumerate(tareas):
        buckets[i % n].append(t)   # el operador % cicla 0,1,...,n-1
    return buckets

print(repartir([1, 2, 3, 4, 5], 2))   # [[1, 3, 5], [2, 4]]
```

Un reparto está **equilibrado** si entre el worker más lleno y el más vacío hay como mucho 1 de diferencia.

🧵 El **Líder Kabu** te espera para balancear tareas.
