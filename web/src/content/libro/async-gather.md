---
title: "Asincronía: Juntar resultados (gather)"
order: 1103
---

> 🎯 **Meta:** lanzar muchas corrutinas juntas y recoger **todos** los resultados con `asyncio.gather`.

---

Crear tareas a mano y esperarlas una por una es tedioso. **`asyncio.gather`** lo hace en una línea: lanza todas, espera a que terminen, y te devuelve la lista de resultados **en el mismo orden** en que las pasaste.

## `gather`

```python
import asyncio

async def bajar(n):
    await asyncio.sleep(1)
    return n * 10

async def principal():
    resultados = await asyncio.gather(bajar(1), bajar(2), bajar(3))
    print(resultados)   # [10, 20, 30]  → ¡en orden!  (tardó ~1s)

asyncio.run(principal())
```

El orden de los resultados coincide con el de las corrutinas, **aunque terminen en otro orden**. Eso te deja emparejarlos con sus nombres por posición:

```python
nombres = ["pikachu", "onix", "snorlax"]
valores = [100, 80, 160]
ficha = {n: v for n, v in zip(nombres, valores)}
```

## Cuando algo falla

Si una tarea devuelve `None` (o usás `return_exceptions=True`), conviene revisar qué salió bien:

```python
resultados = [100, None, 160]
ok = [r for r in resultados if r is not None]   # [100, 160]
fallaron = resultados.count(None)               # 1
```

> 💡 `gather` es la herramienta más usada de asyncio: "hacé todo esto junto y traeme los resultados".

🪢 La **Líder Bea** te espera para recolectar resultados.
