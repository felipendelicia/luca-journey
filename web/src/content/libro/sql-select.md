---
title: "SQL: filtrar y ordenar"
order: 520
---

> 🎯 **Meta:** hacerle **preguntas** a la base: filtrar con `WHERE`, ordenar con `ORDER BY`, buscar texto con `LIKE` y cortar con `LIMIT`.

Tener los datos está bueno, pero la gracia es **consultarlos**: ¿quiénes superan el nivel 50? ¿los de tipo Fuego? ¿los 3 más fuertes?

## 🎯 WHERE: filtrar

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER, tipo TEXT)")
con.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", [
    ("Pikachu", 25, "Electrico"), ("Charizard", 90, "Fuego"),
    ("Bulbasaur", 12, "Planta"), ("Snorlax", 70, "Normal"),
])

for fila in con.execute("SELECT nombre FROM pokemon WHERE nivel >= ?", (50,)):
    print(fila[0])
```

> 💡 `WHERE` filtra filas por una condición. Y de nuevo: el valor va con `?` y una tupla `(50,)`.

```quiz
P: ¿Qué cláusula SQL filtra filas por una condición?
- ORDER BY
+ WHERE
- GROUP BY
> `WHERE` filtra qué filas entran al resultado. `ORDER BY` ordena el resultado y `GROUP BY` agrupa para calcular resúmenes.
```

## ↕️ ORDER BY: ordenar

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
con.executemany("INSERT INTO pokemon VALUES (?, ?)", [("Pikachu", 25), ("Charizard", 90), ("Bulbasaur", 12)])

# DESC = de mayor a menor (ASC sería al revés)
for nombre, nivel in con.execute("SELECT nombre, nivel FROM pokemon ORDER BY nivel DESC"):
    print(nombre, nivel)
```

## 🔤 LIKE: buscar texto

`LIKE` busca patrones. `%` significa "cualquier cosa".

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT)")
con.executemany("INSERT INTO pokemon VALUES (?)", [("Charizard",), ("Charmander",), ("Pikachu",)])

# nombres que empiezan con "Char"
for fila in con.execute("SELECT nombre FROM pokemon WHERE nombre LIKE ?", ("Char%",)):
    print(fila[0])
```

## ✂️ LIMIT: cortar

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
con.executemany("INSERT INTO pokemon VALUES (?, ?)", [("A", 10), ("B", 90), ("C", 50), ("D", 70)])

# los 2 de mayor nivel
for fila in con.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC LIMIT 2"):
    print(fila[0])
```

```quiz
P: ¿Qué hace `ORDER BY nivel DESC`?
- Ordena los Pokémon de nivel más bajo a más alto
- Ordena por nombre en vez de por nivel
+ Ordena de nivel más alto a más bajo
> `DESC` = descendente (mayor a menor). `ASC` sería ascendente (menor a mayor), que es el orden por defecto.
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `WHERE cond` | filtrar filas |
| `ORDER BY col DESC/ASC` | ordenar |
| `LIKE 'Char%'` | buscar por patrón de texto |
| `LIMIT n` | quedarte con n filas |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/sql-select). 💪

> ⚡ *"Una base sin consultas es una caja cerrada. WHERE es la llave."*
