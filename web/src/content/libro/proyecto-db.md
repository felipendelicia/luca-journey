---
title: "Proyecto: Pokédex en SQLite"
order: 570
---

> 🎯 **Meta:** juntar **todo Sinnoh** en una **Pokédex con base de datos**: crear, cargar, consultar, agrupar — desde Python. Tu primera app con datos que **perduran**.

Llegaste al final de Sinnoh. 🔵 Ahora armás una **Pokédex completa** guardada en SQLite, juntando todo lo que aprendiste.

## 🏗️ La Pokédex completa

```python
import sqlite3


def crear_pokedex():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE pokemon (nombre TEXT, tipo TEXT, nivel INTEGER)")
    return con


def agregar(con, nombre, tipo, nivel):
    con.execute("INSERT INTO pokemon VALUES (?, ?, ?)", (nombre, tipo, nivel))
    con.commit()


def listar(con):
    return [f[0] for f in con.execute("SELECT nombre FROM pokemon ORDER BY nombre")]


def el_mas_fuerte(con):
    return con.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC LIMIT 1").fetchone()[0]


def por_tipo(con):
    return dict(con.execute("SELECT tipo, COUNT(*) FROM pokemon GROUP BY tipo"))
```

## ▶️ Usándola

```python
import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pokemon (nombre TEXT, tipo TEXT, nivel INTEGER)")

# cargamos el equipo
equipo = [("Pikachu", "Electrico", 25), ("Charizard", "Fuego", 90),
          ("Vulpix", "Fuego", 18), ("Snorlax", "Normal", 70)]
con.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", equipo)
con.commit()

# consultas
print("Todos:", [f[0] for f in con.execute("SELECT nombre FROM pokemon ORDER BY nombre")])
print("El más fuerte:", con.execute("SELECT nombre FROM pokemon ORDER BY nivel DESC LIMIT 1").fetchone()[0])
print("Por tipo:", dict(con.execute("SELECT tipo, COUNT(*) FROM pokemon GROUP BY tipo")))
```

## 🗺️ Lo que aprendiste en Sinnoh

1. **SELECT** — leer datos de una tabla.
2. **CREATE / INSERT** — crear tablas y cargarlas.
3. **WHERE / ORDER BY / LIKE / LIMIT** — filtrar y ordenar.
4. **COUNT / AVG / GROUP BY** — resumir y agrupar.
5. **UPDATE / DELETE** — cambiar y borrar (¡con WHERE!).
6. **JOIN** — combinar varias tablas.
7. **sqlite3** — todo eso desde Python, con `commit` para guardar.

Con esto manejás **datos que perduran**: la base de toda app seria (redes sociales, juegos, bancos) guarda su info así. 🚀

## ➡️ ¿Y ahora qué?

Cerrá Sinnoh con los [ejercicios de este tema](/ejercicios/proyecto-db). Al completarlos ganás la medalla **Faro** y sos **Campeón de Sinnoh**. 🔦🏆

> ⚡ *"Una app sin base de datos olvida todo al cerrar. Con una, recuerda para siempre."*
