---
title: "SQL: crear e insertar"
order: 510
---

> 🎯 **Meta:** crear tus propias **tablas** (CREATE TABLE) y cargarles datos (INSERT). Sin esto, no hay nada que consultar.

Antes de leer datos, hay que **tenerlos**. Se crea una **tabla** definiendo sus columnas, y después se **insertan** filas.

## 🏗️ CREATE TABLE

Definís el nombre de la tabla y sus columnas con su **tipo** (`TEXT` para texto, `INTEGER` para números enteros, `REAL` para decimales).

```python
import sqlite3
con = sqlite3.connect(":memory:")

con.execute("CREATE TABLE entrenadores (nombre TEXT, medallas INTEGER)")
print("Tabla creada ✅")
```

## ➕ INSERT: agregar filas

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE entrenadores (nombre TEXT, medallas INTEGER)")

con.execute("INSERT INTO entrenadores VALUES (?, ?)", ("Ash", 8))
con.execute("INSERT INTO entrenadores VALUES (?, ?)", ("Misty", 3))

for fila in con.execute("SELECT * FROM entrenadores"):
    print(fila)
```

> ⚠️ **Siempre usá `?`** para los valores (no los pegues con f-strings). Es más seguro: evita el famoso "SQL injection". SQLite reemplaza cada `?` por el valor de la tupla.

```quiz
P: ¿Por qué se usa `?` en lugar de poner el valor directo en el SQL?
- Porque SQLite no acepta strings en el INSERT
- Porque los `?` hacen la consulta más rápida
+ Para evitar SQL injection y que SQLite maneje el tipo correctamente
> Pegar valores con f-strings abre la puerta al SQL injection. Los `?` son **parámetros seguros**: SQLite reemplaza cada `?` con el valor correspondiente de la tupla.
```

## 📦 Insertar muchos de una: executemany

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")

equipo = [("Pikachu", 25), ("Charizard", 90), ("Snorlax", 70)]
con.executemany("INSERT INTO pokemon VALUES (?, ?)", equipo)

print("Cargados:", con.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0])
```

> 💡 `executemany` corre el mismo INSERT para cada tupla de la lista. Ideal para cargar muchos datos juntos.

```quiz
P: ¿Qué tipo de columna usarías para guardar el nombre de un Pokémon?
+ `TEXT`
- `INTEGER`
- `REAL`
> `TEXT` es para cadenas de texto. `INTEGER` es para números enteros y `REAL` para decimales.
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `CREATE TABLE t (col TIPO, ...)` | crear una tabla |
| `TEXT`, `INTEGER`, `REAL` | tipos de columna |
| `INSERT INTO t VALUES (?, ?)` | agregar una fila (con parámetros) |
| `executemany(sql, lista)` | insertar muchas filas |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/sql-crear). 💪

> ⚡ *"Primero construís la PC de Bill; después la llenás de Pokémon."*
