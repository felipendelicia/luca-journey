---
title: "Asincronía: Límite de concurrencia"
order: 1106
---

> 🎯 **Meta:** controlar **cuántas** tareas corren a la vez para no saturar la red ni el servidor.

---

Lanzar 10.000 descargas juntas suena genial… hasta que tu red colapsa o el servidor te bloquea. La solución: **limitar la concurrencia**, procesando de a tandas.

## Semáforo

Un **semáforo** (`asyncio.Semaphore`) permite que como mucho N tareas pasen a la vez; las demás esperan su turno:

```python
import asyncio

sem = asyncio.Semaphore(3)   # máximo 3 a la vez

async def bajar(url):
    async with sem:          # pide un cupo; si no hay, espera
        await asyncio.sleep(1)
        return url
```

## Procesar por lotes

La idea más simple: partir en **lotes** de tamaño fijo y procesar lote por lote.

```python
def por_lotes(items, tam):
    return [items[i:i+tam] for i in range(0, len(items), tam)]

print(por_lotes([1, 2, 3, 4, 5], 2))   # [[1, 2], [3, 4], [5]]
```

Y la lógica del "cupo": ¿cabe una más?

```python
def cabe(activos, maximo):
    return activos < maximo

print(cabe(2, 3))   # True   (hay lugar)
print(cabe(3, 3))   # False  (lleno)
```

> 💡 Límite de concurrencia = respeto. No abuses de las APIs ajenas; un buen bot va de a poco.

🚦 La **Líder Melony** te espera para controlar la concurrencia.
