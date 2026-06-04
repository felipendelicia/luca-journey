"""
pokedex_web.storage — Persistencia de la Pokédex en JSON.

Guarda una lista de Pokémon (diccionarios) en un archivo JSON. Cada Pokémon
tiene un id único autoincremental.
"""

import json
import os


def cargar(ruta):
    """Devuelve la lista de Pokémon guardada, o [] si el archivo no existe."""
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Archivo corrupto o ilegible: arrancamos vacío en vez de romper.
        return []


def guardar(ruta, pokemons):
    """Guarda la lista de Pokémon en el archivo JSON."""
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(pokemons, f, indent=2, ensure_ascii=False)


def proximo_id(pokemons):
    """Calcula el próximo id (el mayor existente + 1, o 1 si está vacía)."""
    if not pokemons:
        return 1
    return max(p["id"] for p in pokemons) + 1


def agregar(ruta, datos):
    """
    Agrega un Pokémon nuevo y devuelve el diccionario agregado (con su id).
    'datos' es un dict con al menos nombre, tipo y nivel.
    """
    pokemons = cargar(ruta)
    nuevo = {
        "id": proximo_id(pokemons),
        "nombre": datos.get("nombre", "").strip(),
        "tipo": datos.get("tipo", "").strip(),
        "nivel": int(datos.get("nivel", 1) or 1),
        "altura": datos.get("altura", ""),
        "peso": datos.get("peso", ""),
        "descripcion": datos.get("descripcion", ""),
    }
    pokemons.append(nuevo)
    guardar(ruta, pokemons)
    return nuevo


def buscar_por_id(ruta, pokemon_id):
    """Devuelve el Pokémon con ese id, o None si no existe."""
    for p in cargar(ruta):
        if p["id"] == pokemon_id:
            return p
    return None


def eliminar(ruta, pokemon_id):
    """Elimina el Pokémon con ese id. Devuelve True si lo borró."""
    pokemons = cargar(ruta)
    nuevos = [p for p in pokemons if p["id"] != pokemon_id]
    if len(nuevos) == len(pokemons):
        return False
    guardar(ruta, nuevos)
    return True
