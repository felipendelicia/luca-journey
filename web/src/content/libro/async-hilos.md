---
title: "Asincronía: Dividir trabajo (hilos)"
order: 1105
---

> 🎯 **Meta:** conocer los **hilos** (`threading`) y cómo partir el trabajo en bloques para repartirlo.

---

`asyncio` brilla cuando el trabajo **espera** (red, disco). Pero si el trabajo es **cálculo puro**, se usan **hilos** (`threading`) o **procesos** (`multiprocessing`), que ejecutan en paralelo de verdad.

## Hilos con `threading`

```python
import threading

def trabajo(nombre):
    print("trabajando", nombre)

h1 = threading.Thread(target=trabajo, args=("A",))
h2 = threading.Thread(target=trabajo, args=("B",))
h1.start(); h2.start()     # arrancan en paralelo
h1.join(); h2.join()       # esperar a que terminen
```

## Partir en bloques contiguos

Para darle un pedazo a cada hilo, partís la lista en **bloques contiguos** lo más parejos posible:

```python
def dividir(items, n):
    k, m = divmod(len(items), n)
    return [items[i*k+min(i,m):(i+1)*k+min(i+1,m)] for i in range(n)]

print(dividir([1, 2, 3, 4, 5], 2))   # [[1, 2, 3], [4, 5]]
```

A diferencia del round-robin (que intercala), acá cada hilo recibe un tramo **seguido** — útil cuando el orden importa o los datos están cerca.

> ⚠️ Dato fino de Python: por el **GIL**, los hilos no aceleran cálculo puro (para eso van procesos). Pero sí ayudan cuando el trabajo espera I/O. Elegí la herramienta según el tipo de trabajo.

🕸️ La **Líder Opal** te espera para dividir en bloques.
