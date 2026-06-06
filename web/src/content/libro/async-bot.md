---
title: "Asincronía: Descargador async"
order: 1107
---

> 🎯 **Meta:** juntar todo en un **descargador concurrente** que baja muchas cosas, rápido y con control.

---

Ya tenés las piezas: corrutinas, `await`, tareas, `gather`, colas, límites. Un descargador real las combina así:

1. **Preparar** la lista de descargas.
2. **Planificar** en lotes (para respetar el límite de concurrencia).
3. **Ejecutar** cada lote en paralelo con `gather`.
4. **Reportar** cuántas salieron bien.

## El esqueleto

```python
import asyncio

async def bajar(item):
    await asyncio.sleep(0.5)
    item["ok"] = True
    return item

def preparar(urls):
    return [{"url": u, "ok": False} for u in urls]

def por_lotes(items, tam):
    return [items[i:i+tam] for i in range(0, len(items), tam)]

async def descargar_todo(urls, limite):
    items = preparar(urls)
    for lote in por_lotes(items, limite):
        await asyncio.gather(*(bajar(it) for it in lote))   # el lote, en paralelo
    ok = sum(1 for it in items if it["ok"])
    return f"{ok}/{len(items)} descargadas."

print(asyncio.run(descargar_todo(["a", "b", "c", "d", "e"], 2)))
```

Fijate el patrón: **dentro** del lote, todo junto (`gather`); **entre** lotes, de a uno (respetando el límite). Rápido pero prolijo.

## Lo que aprendiste en Galar

Asincronía y concurrencia: hacer muchas cosas a la vez sin trabarte, repartir trabajo y controlar el caudal. Es lo que hace que las apps modernas sean rápidas.

## ✅ Comprobá lo que aprendiste

```quiz
P: En el descargador, DENTRO de un lote las descargas van…
+ todas juntas, con `gather`
- de a una, esperando cada una
- al azar
> Dentro del lote, en paralelo; entre lotes, de a uno (respetando el límite).
```

```quiz
P: ¿Por qué procesar por lotes en vez de todo junto?
+ respeta el límite de concurrencia y no satura
- queda más lindo
- usa menos código
> Rápido pero prolijo: el lote en paralelo, el límite respetado.
```

⚡ El **Líder Raihan** y el **Campeón Leon** te esperan para coronarte **Campeón de Galar**.
