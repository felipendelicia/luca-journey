---
title: "Asincronía: await — dónde esperar"
order: 1101
---

> 🎯 **Meta:** usar **`await`** para esperar una corrutina sin bloquear todo el programa.

---

`await` es la palabra mágica de la asincronía: pone tu corrutina "en pausa" esperando un resultado, pero mientras tanto el programa puede atender otras cosas.

## `await` dentro de `async def`

`await` solo se usa **adentro** de una función `async`. Espera a que la corrutina termine y te da su resultado:

```python
import asyncio

async def descargar(url):
    return f"datos de {url}"

async def principal():
    datos = await descargar("/pokedex")   # espera y guarda el resultado
    print(datos)

asyncio.run(principal())   # arranca el event loop y corre la corrutina
```

`asyncio.run(corrutina)` es el punto de entrada: prende el event loop, corre tu corrutina principal y lo apaga.

## ¿Dónde va el `await`?

`await` va delante de lo que **espera**: una descarga, una consulta a la base, un `asyncio.sleep`. NO lo pongas en cálculos normales (sumar, recorrer una lista) — eso no espera nada.

```python
async def tarea():
    datos = await bajar_pagina(url)   # ✅ espera I/O → await
    total = sum(datos)                # ❌ esto NO espera → sin await
    return total
```

> ⚠️ Si te olvidás el `await`, te queda el objeto corrutina sin ejecutar (y Python te avisa: *"coroutine was never awaited"*). Si lo ponés de más, sobre algo que no es corrutina, también falla.

⏳ La **Líder Nessa** te espera para marcar dónde van los awaits.
