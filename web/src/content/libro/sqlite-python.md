---
title: "SQLite desde Python"
order: 560
---

> 🎯 **Meta:** manejar la base **desde Python** con el módulo `sqlite3`: conectarte, ejecutar, traer resultados y **guardar** los cambios.

Ya sabés SQL. Ahora lo juntamos con Python: el módulo **`sqlite3`** (que viene incluido con Python) te deja crear una base, ejecutar consultas y trabajar con los resultados en tu código.

## 🔌 Conectarse

```python
import sqlite3

# ":memory:" = una base temporal en RAM (perfecta para practicar).
# En un proyecto real pondrías un archivo: sqlite3.connect("pokedex.db")
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
print("Conectado ✅")
```

> 💡 `connect("archivo.db")` crea/abre un archivo de base de datos real, que **persiste** aunque cierres el programa. `:memory:` desaparece al terminar.

## 🏃 Ejecutar y traer resultados

`execute` corre la consulta. Para leer resultados: `fetchone()` (una fila) o `fetchall()` (todas).

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
con.executemany("INSERT INTO pokemon VALUES (?, ?)", [("Pikachu", 25), ("Charizard", 90)])

uno = con.execute("SELECT * FROM pokemon WHERE nombre = ?", ("Pikachu",)).fetchone()
print("uno:", uno)           # ('Pikachu', 25)  -> tupla, o None si no existe

todos = con.execute("SELECT nombre FROM pokemon").fetchall()
print("todos:", todos)       # [('Pikachu',), ('Charizard',)]
```

```quiz
P: ¿Cuál es la diferencia entre `sqlite3.connect(":memory:")` y `sqlite3.connect("pokedex.db")`?
- No hay diferencia, son equivalentes
- `:memory:` es más lento porque trabaja en disco
+ `:memory:` es temporal (desaparece al terminar); `pokedex.db` guarda en un archivo real
> `:memory:` crea la base de datos en la RAM — perfecta para practicar. Con un nombre de archivo, los datos **persisten** aunque el programa se cierre.
```

## 💾 Guardar: commit

Cuando **modificás** datos (INSERT/UPDATE/DELETE) en un archivo, hay que **confirmar** con `commit()` para que queden guardados.

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")

con.execute("INSERT INTO pokemon VALUES (?, ?)", ("Eevee", 15))
con.commit()     # ✅ guarda los cambios

print(con.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0])
```

> 💡 También existe el **cursor** (`cur = con.cursor()`), una forma más explícita de ejecutar y leer: `cur.execute(...)` y después `cur.fetchone()`. Para lo básico, usar `con.execute(...)` directo alcanza.

```quiz
P: Después de un `INSERT` en un archivo `.db`, ¿qué hay que hacer para que el dato quede guardado?
- Cerrar la conexión con `con.close()`
- Volver a abrir el archivo
+ Llamar a `con.commit()`
> Sin `commit()`, los cambios (INSERT/UPDATE/DELETE) quedan en una **transacción abierta** y se pierden al cerrar. `commit()` los confirma definitivamente.
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `sqlite3.connect(":memory:")` | base temporal en RAM |
| `connect("archivo.db")` | base en archivo (persistente) |
| `con.execute(sql, params)` | ejecutar una consulta |
| `.fetchone()` / `.fetchall()` | traer una fila / todas |
| `con.commit()` | guardar los cambios |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/sqlite-python). 💪

> ⚡ *"Python piensa, SQLite recuerda. Juntos, tu app no olvida nada."*
