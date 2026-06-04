---
title: "SQL: actualizar y borrar"
order: 540
---

> 🎯 **Meta:** **cambiar** datos que ya existen (`UPDATE`) y **eliminarlos** (`DELETE`). Y la regla de oro: ¡nunca sin `WHERE`!

Los datos cambian: un Pokémon sube de nivel, otro hay que sacarlo. Para eso están `UPDATE` y `DELETE`.

## ✏️ UPDATE: cambiar datos

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
con.executemany("INSERT INTO pokemon VALUES (?, ?)", [("Pikachu", 25), ("Charizard", 90)])

# Pikachu evolucionó: sube a nivel 50
con.execute("UPDATE pokemon SET nivel = ? WHERE nombre = ?", (50, "Pikachu"))

print(con.execute("SELECT * FROM pokemon").fetchall())
```

> ⚠️ **El `WHERE` es clave.** Un `UPDATE` **sin** `WHERE` cambia **TODAS** las filas. Es como darle una Poción a todo el PC de Bill a la vez.

## ➕ Actualizar usando el valor actual

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
con.executemany("INSERT INTO pokemon VALUES (?, ?)", [("Pikachu", 25), ("Charizard", 90)])

# todos suben 5 niveles
con.execute("UPDATE pokemon SET nivel = nivel + 5")
print(con.execute("SELECT * FROM pokemon").fetchall())
```

## 🗑️ DELETE: borrar

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
con.executemany("INSERT INTO pokemon VALUES (?, ?)", [("Pikachu", 25), ("Caterpie", 5), ("Charizard", 90)])

# liberamos a Caterpie
con.execute("DELETE FROM pokemon WHERE nombre = ?", ("Caterpie",))
# y a todos los muy débiles
con.execute("DELETE FROM pokemon WHERE nivel < ?", (10,))

print([f[0] for f in con.execute("SELECT nombre FROM pokemon")])
```

> ⚠️ Igual que UPDATE: `DELETE` **sin** `WHERE` **vacía la tabla entera**. Siempre revisá el WHERE antes de ejecutar.

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `UPDATE t SET col = ? WHERE ...` | cambiar filas |
| `SET col = col + 1` | actualizar usando el valor actual |
| `DELETE FROM t WHERE ...` | borrar filas |
| sin `WHERE` | ⚠️ afecta TODA la tabla |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/sql-update-delete). 💪

> ⚡ *"Con gran poder viene un gran WHERE. No lo olvides nunca."*
