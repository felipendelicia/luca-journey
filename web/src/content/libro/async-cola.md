---
title: "Asincronía: Cola productor/consumidor"
order: 1104
---

> 🎯 **Meta:** coordinar tareas con una **cola**: unos producen trabajo, otros lo consumen.

---

Un patrón clásico de concurrencia: los **productores** generan tareas y las ponen en una cola; los **consumidores** las sacan y las procesan. La cola desacopla a unos de otros — cada lado va a su ritmo.

## La cola es FIFO

FIFO = *first in, first out*: el primero que entra es el primero que sale (como una fila). En asyncio se usa `asyncio.Queue`; la idea, con una lista, es:

```python
cola = []
cola.append("tarea1")   # producir: al final
cola.append("tarea2")
primera = cola.pop(0)   # consumir: del principio  → "tarea1"
```

## Productor / consumidor

```python
import asyncio

async def productor(cola):
    for i in range(3):
        await cola.put(i)        # pone trabajo

async def consumidor(cola):
    while not cola.empty():
        item = await cola.get()  # saca y procesa
        print("procesando", item)

async def principal():
    cola = asyncio.Queue()
    await productor(cola)
    await consumidor(cola)

asyncio.run(principal())
```

Procesar la cola entera en orden FIFO es sacar del frente hasta vaciarla:

```python
def vaciar(cola):
    out = []
    while cola:
        out.append(cola.pop(0))
    return out
```

> 💡 Las colas evitan que el productor abrume al consumidor: si la cola se llena, el productor espera. Es la base de los sistemas de tareas (Celery, RabbitMQ…).

## ✅ Comprobá lo que aprendiste

```quiz
P: Una cola FIFO saca primero…
+ al que entró primero
- al último que entró
- al más grande
> First in, first out — como una fila.
```

```quiz
P: El patrón productor/consumidor con una cola sirve para…
+ que productores y consumidores avancen a su ritmo
- ordenar números
- acelerar cálculos puros
> La cola los desacopla: si se llena, el productor espera.
```

🎟️ El **Líder Allister** te espera con su cola fantasma.
