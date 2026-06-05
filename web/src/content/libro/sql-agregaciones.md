---
title: "SQL: agregaciones y GROUP BY"
order: 530
---

> 🎯 **Meta:** sacar **resúmenes** de la base: contar, promediar, sumar, y agrupar con `GROUP BY` (ej: cuántos Pokémon de cada tipo).

A veces no querés las filas una por una, sino un **número que las resuma**: el promedio de niveles, el máximo, cuántos hay de cada tipo. Para eso están las **funciones de agregación**.

## 📊 Funciones de agregación

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
con.executemany("INSERT INTO pokemon VALUES (?, ?)", [("Pikachu", 20), ("Charizard", 90), ("Bulbasaur", 10)])

print("cantidad:", con.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0])
print("promedio:", con.execute("SELECT AVG(nivel) FROM pokemon").fetchone()[0])
print("máximo:", con.execute("SELECT MAX(nivel) FROM pokemon").fetchone()[0])
print("suma:", con.execute("SELECT SUM(nivel) FROM pokemon").fetchone()[0])
```

> 💡 `COUNT`, `AVG`, `MAX`, `MIN`, `SUM` toman toda la columna y devuelven **un** valor. Por eso usás `.fetchone()[0]`.

```quiz
P: ¿Qué función SQL devuelve el promedio de una columna numérica?
- `SUM(col)`
+ `AVG(col)`
- `COUNT(col)`
> `AVG` (average) calcula el promedio. `SUM` suma todos los valores y `COUNT` cuenta cuántos hay.
```

## 🧮 GROUP BY: resumir por grupo

`GROUP BY` arma grupos y calcula la agregación **por cada grupo**. Es lo más potente de SQL.

```python
import sqlite3
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER, tipo TEXT)")
con.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", [
    ("Pikachu", 20, "Electrico"), ("Raichu", 40, "Electrico"),
    ("Charizard", 90, "Fuego"), ("Bulbasaur", 10, "Planta"),
])

# cuántos hay de cada tipo
for tipo, cantidad in con.execute("SELECT tipo, COUNT(*) FROM pokemon GROUP BY tipo"):
    print(tipo, "->", cantidad)

print("---")
# nivel promedio por tipo
for tipo, prom in con.execute("SELECT tipo, AVG(nivel) FROM pokemon GROUP BY tipo"):
    print(tipo, "promedio", prom)
```

> 💡 El patrón: `SELECT columna_grupo, AGREGACIÓN FROM tabla GROUP BY columna_grupo`. Pensalo como "por cada tipo, contame/promediame...".

```quiz
P: ¿Qué hace `SELECT tipo, COUNT(*) FROM pokemon GROUP BY tipo`?
- Filtra solo los Pokémon de un tipo específico
- Cuenta el total de Pokémon sin importar el tipo
+ Muestra cuántos Pokémon hay de cada tipo
> `GROUP BY tipo` forma un grupo por cada tipo distinto, y `COUNT(*)` cuenta las filas de cada grupo por separado.
```

## 📝 Resumen

| Cosa | Para qué |
|------|----------|
| `COUNT(*)` | contar filas |
| `AVG(col)` | promedio |
| `MAX/MIN(col)` | máximo / mínimo |
| `SUM(col)` | suma |
| `GROUP BY col` | agrupar y resumir por grupo |

## ➡️ ¿Y ahora qué?

Practicá con los [ejercicios de este tema](/ejercicios/sql-agregaciones). 💪

> ⚡ *"Mil filas, una pregunta, una respuesta. Eso es GROUP BY."*
