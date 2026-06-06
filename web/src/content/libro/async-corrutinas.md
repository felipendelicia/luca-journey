---
title: "Asincronía: Corrutinas (async def)"
order: 1100
---

> 🎯 **Meta:** entender qué es una **corrutina** y por qué `async def` te deja hacer muchas cosas "a la vez" sin trabarte.

---

Imaginá que tenés que bajar 100 imágenes. Si las bajás una por una, esperás a que termine cada una antes de empezar la siguiente: lentísimo. La **asincronía** te deja arrancar todas y aprovechar el tiempo de espera. La pieza base es la **corrutina**.

## `async def`

Una corrutina es una función definida con `async def`. Lo raro: **llamarla NO la ejecuta**, te devuelve un objeto "corrutina" que correrá más tarde.

```python
import asyncio

async def descargar(url):
    print("bajando", url)
    return "datos"

c = descargar("/pokedex")   # NO imprime nada todavía: c es una corrutina
print(type(c))              # <class 'coroutine'>
```

Para que realmente corra, hace falta un **event loop** que la maneje (lo ves en los próximos capítulos con `await` y `asyncio.run`).

## Reconocer corrutinas

`asyncio.iscoroutinefunction(fn)` te dice si una función es `async`:

```python
import asyncio

async def baja(): ...
def suma(): ...

print(asyncio.iscoroutinefunction(baja))   # True
print(asyncio.iscoroutinefunction(suma))   # False
```

Esto importa porque las corrutinas se usan distinto que las funciones normales: a una corrutina la tenés que `await`-ear o pasársela al event loop; a una función normal la llamás y listo.

> 💡 Regla mental: **`async def`** = "esto puede pausarse para dejar correr otra cosa mientras espera". Ideal para lo que espera red, disco o tiempo.

🌀 El **Líder Milo** te espera para armar un registro de corrutinas.
