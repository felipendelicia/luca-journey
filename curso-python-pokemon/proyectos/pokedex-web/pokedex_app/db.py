"""
pokedex_app.db — Persistencia en SQLite.

Cada función abre su propia conexión (simple y seguro para una app chica).
Las filas se devuelven como diccionarios para que las plantillas las usen cómodo.
"""

import sqlite3


def _conectar(ruta):
    """Abre una conexión y configura que las filas se lean como diccionarios."""
    conexion = sqlite3.connect(ruta)
    conexion.row_factory = sqlite3.Row  # permite acceder por nombre de columna
    return conexion


def init_db(ruta):
    """Crea la tabla 'pokemon' si todavía no existe."""
    with _conectar(ruta) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS pokemon (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT,
                nivel INTEGER DEFAULT 1,
                altura TEXT,
                peso TEXT,
                descripcion TEXT
            )
            """
        )


def _fila_a_dict(fila):
    """Convierte una fila de SQLite en un diccionario normal."""
    return dict(fila) if fila is not None else None


def listar(ruta):
    """Devuelve todos los Pokémon, ordenados por id."""
    with _conectar(ruta) as con:
        filas = con.execute("SELECT * FROM pokemon ORDER BY id").fetchall()
    return [dict(f) for f in filas]


def buscar(ruta, texto):
    """Devuelve los Pokémon cuyo nombre o tipo contienen 'texto'."""
    patron = f"%{texto}%"
    with _conectar(ruta) as con:
        filas = con.execute(
            "SELECT * FROM pokemon WHERE nombre LIKE ? OR tipo LIKE ? ORDER BY id",
            (patron, patron),
        ).fetchall()
    return [dict(f) for f in filas]


def obtener(ruta, pokemon_id):
    """Devuelve un Pokémon por id, o None."""
    with _conectar(ruta) as con:
        fila = con.execute(
            "SELECT * FROM pokemon WHERE id = ?", (pokemon_id,)
        ).fetchone()
    return _fila_a_dict(fila)


def agregar(ruta, datos):
    """Inserta un Pokémon y devuelve su id nuevo."""
    with _conectar(ruta) as con:
        cursor = con.execute(
            """
            INSERT INTO pokemon (nombre, tipo, nivel, altura, peso, descripcion)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                datos.get("nombre", ""),
                datos.get("tipo", ""),
                int(datos.get("nivel", 1) or 1),
                datos.get("altura", ""),
                datos.get("peso", ""),
                datos.get("descripcion", ""),
            ),
        )
        return cursor.lastrowid


def actualizar(ruta, pokemon_id, datos):
    """Actualiza un Pokémon existente. Devuelve True si cambió algo."""
    with _conectar(ruta) as con:
        cursor = con.execute(
            """
            UPDATE pokemon
            SET nombre = ?, tipo = ?, nivel = ?, altura = ?, peso = ?, descripcion = ?
            WHERE id = ?
            """,
            (
                datos.get("nombre", ""),
                datos.get("tipo", ""),
                int(datos.get("nivel", 1) or 1),
                datos.get("altura", ""),
                datos.get("peso", ""),
                datos.get("descripcion", ""),
                pokemon_id,
            ),
        )
        return cursor.rowcount > 0


def eliminar(ruta, pokemon_id):
    """Elimina un Pokémon por id. Devuelve True si lo borró."""
    with _conectar(ruta) as con:
        cursor = con.execute("DELETE FROM pokemon WHERE id = ?", (pokemon_id,))
        return cursor.rowcount > 0
