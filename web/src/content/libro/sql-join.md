---
title: "SQL: relaciones y JOIN"
order: 550
---

> 🎯 **Meta:** combinar **varias tablas** relacionadas con `JOIN`. Así se organizan los datos de verdad: sin repetir información.

En una base bien hecha, los datos se reparten en **varias tablas** que se **relacionan**. Por ejemplo: una tabla de Pokémon y otra con la info de cada tipo. Para usarlas juntas, se hace un **JOIN**.

## 🧩 ¿Por qué separar en tablas?

Imaginá guardar la debilidad de cada tipo **en cada Pokémon**: repetirías "Fuego → débil a Agua" miles de veces. Mejor: una tabla `pokemon` y otra `tipos`, **relacionadas** por la columna `tipo`.

```
pokemon                 tipos
┌──────────┬───────┐    ┌───────┬───────────┐
│ nombre   │ tipo  │    │ tipo  │ debilidad │
├──────────┼───────┤    ├───────┼───────────┤
│ Charizard│ Fuego │◄──►│ Fuego │ Agua      │
│ Blastoise│ Agua  │◄──►│ Agua  │ Planta    │
└──────────┴───────┘    └───────┴───────────┘
```

## 🔗 JOIN: combinar tablas

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, tipo TEXT)")
con.execute("CREATE TABLE tipos (tipo TEXT, debilidad TEXT)")
con.executemany("INSERT INTO pokemon VALUES (?, ?)", [("Charizard", "Fuego"), ("Blastoise", "Agua")])
con.executemany("INSERT INTO tipos VALUES (?, ?)", [("Fuego", "Agua"), ("Agua", "Planta")])

sql = """
SELECT p.nombre, t.debilidad
FROM pokemon p
JOIN tipos t ON p.tipo = t.tipo
"""
for nombre, debilidad in con.execute(sql):
    print(nombre, "es débil a", debilidad)
```

> 💡 `JOIN tipos t ON p.tipo = t.tipo` une cada fila de `pokemon` con la de `tipos` que tenga **el mismo tipo**. Las letras `p` y `t` son **apodos** (alias) para escribir menos.

```quiz
P: En `JOIN tipos t ON p.tipo = t.tipo`, ¿para qué sirven las letras `p` y `t`?
- Son variables de Python que guardan los datos
+ Son alias (apodos) de las tablas para escribir menos
- Son los nombres de las columnas a combinar
> Los alias (`p` para `pokemon`, `t` para `tipos`) son apodos que se definen después del nombre de la tabla. Permiten escribir `p.nombre` en vez de `pokemon.nombre`.
```

## 🎯 JOIN + WHERE

Podés filtrar el resultado combinado como cualquier consulta:

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, tipo TEXT)")
con.execute("CREATE TABLE tipos (tipo TEXT, debilidad TEXT)")
con.executemany("INSERT INTO pokemon VALUES (?, ?)", [("Charizard", "Fuego"), ("Vulpix", "Fuego"), ("Blastoise", "Agua")])
con.executemany("INSERT INTO tipos VALUES (?, ?)", [("Fuego", "Agua"), ("Agua", "Planta")])

# ¿quiénes son débiles al Agua?
sql = "SELECT p.nombre FROM pokemon p JOIN tipos t ON p.tipo = t.tipo WHERE t.debilidad = ?"
print([f[0] for f in con.execute(sql, ("Agua",))])
```

```quiz
P: ¿Por qué se divide la información en varias tablas en lugar de poner todo en una?
- Porque SQLite no permite tablas con más de 3 columnas
- Para que las consultas sean más rápidas siempre
+ Para no repetir los mismos datos en cada fila
> La separación evita **redundancia**: si la debilidad del tipo Fuego cambia, la corregís en un solo lugar (tabla `tipos`), no en cada Pokémon de tipo Fuego.
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| varias tablas | no repetir datos |
| `JOIN t2 ON t1.col = t2.col` | combinar por una columna en común |
| alias (`p`, `t`) | apodos para las tablas |
| `JOIN ... WHERE` | filtrar el resultado combinado |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/sql-join). 💪

> ⚡ *"Los datos bien organizados viven en varias tablas. JOIN las hace una."*
