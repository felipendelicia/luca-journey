---
title: "SQL: leer datos"
order: 500
---

> 🎯 **Meta:** entrar a **Sinnoh**, la región de las **bases de datos**. Vas a aprender **SQL**, el idioma para guardar y consultar montones de datos de forma ordenada.

Bienvenido a **Sinnoh**. 🗄️ Hasta ahora guardaste datos en listas, archivos o JSON. Pero cuando son **muchos** y querés buscarlos rápido, se usa una **base de datos**. Y a las bases se les habla en **SQL**.

## 🎮 Analogía: la base de datos es la PC de Bill

La **PC de Bill** guarda todos tus Pokémon ordenados en cajas, y podés buscar al instante "todos los de tipo Fuego". Una **base de datos** es eso: guarda **tablas** (filas y columnas, como un Excel) y te deja **consultarlas** con SQL.

| Concepto | Qué es |
|----------|--------|
| **Tabla** | una planilla (ej: `pokemon`) |
| **Columna** | un campo (ej: `nombre`, `nivel`) |
| **Fila** | un registro (un Pokémon) |
| **SQL** | el idioma para crear/leer/cambiar datos |
| **SQLite** | una base chiquita que usamos (viene con Python) |

## 🔎 SELECT: leer datos

La consulta más usada: `SELECT columnas FROM tabla`. Tocá **▶ ejecutar**:

```python
import sqlite3

# armamos una base de ejemplo (esto lo vemos en detalle más adelante)
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER, tipo TEXT)")
con.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", [
    ("Pikachu", 25, "Electrico"),
    ("Charizard", 90, "Fuego"),
    ("Bulbasaur", 12, "Planta"),
])

# leemos TODOS los nombres
for fila in con.execute("SELECT nombre FROM pokemon"):
    print(fila[0])
```

> 💡 `con.execute("SELECT ...")` devuelve las filas. Cada fila es una **tupla** (por eso `fila[0]` es la primera columna). La primera vez tarda un poco porque carga SQLite.

## 🧮 Contar: COUNT

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
con.executemany("INSERT INTO pokemon VALUES (?, ?)", [("Pikachu", 25), ("Charizard", 90)])

cantidad = con.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]
print("Hay", cantidad, "Pokémon")
```

> 💡 `COUNT(*)` cuenta las filas. `.fetchone()` trae **una** fila de resultado; `[0]` es su primer (y único) valor.

```quiz
P: ¿Qué hace `SELECT COUNT(*) FROM pokemon`?
- Devuelve la primera fila de la tabla
- Devuelve el nombre de todas las columnas
+ Cuenta cuántas filas hay en la tabla
> `COUNT(*)` cuenta filas y devuelve un único número. Para traer datos usarías `SELECT *` (sin `COUNT`).
```

## 🏛️ Elegir columnas

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER, tipo TEXT)")
con.execute("INSERT INTO pokemon VALUES ('Snorlax', 70, 'Normal')")

for nombre, nivel in con.execute("SELECT nombre, nivel FROM pokemon"):
    print(nombre, "es nivel", nivel)
```

```quiz
P: ¿Qué devuelve `con.execute("SELECT nombre FROM pokemon")` al iterar?
- Una lista de strings con los nombres
- Una sola string con todos los nombres unidos
+ Tuplas de un elemento, ej: `('Pikachu',)`
> `execute` devuelve filas como **tuplas**. Por eso necesitás `fila[0]` para sacar el primer (y único) valor de cada fila.
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `SELECT col FROM tabla` | leer una columna |
| `SELECT *` | leer todas las columnas |
| `SELECT COUNT(*)` | contar filas |
| `con.execute(sql)` | correr una consulta (devuelve filas) |
| `.fetchone()` / `.fetchall()` | traer una fila / todas |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/sql-intro). 💪

> ⚡ *"Los datos guardados sin orden son ruido. En una base, son poder."*
