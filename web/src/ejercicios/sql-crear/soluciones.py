"""✅ Soluciones — SQL: crear e insertar"""
import sqlite3


def crear_tabla(conexion):
    conexion.execute("CREATE TABLE entrenadores (nombre TEXT, medallas INTEGER)")


def insertar(conexion, nombre, medallas):
    conexion.execute("INSERT INTO entrenadores VALUES (?, ?)", (nombre, medallas))


def insertar_varios(conexion, filas):
    conexion.executemany("INSERT INTO entrenadores VALUES (?, ?)", filas)


def crear_pokedex(conexion):
    conexion.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
    conexion.execute("INSERT INTO pokemon VALUES (?, ?)", ("Pikachu", 25))
