"""
pokedex_cli.favoritos — Guardado local de Pokémon favoritos en JSON.
"""

import json
import os


def cargar(ruta):
    """Devuelve la lista de nombres favoritos, o [] si no hay archivo."""
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def guardar(ruta, favoritos):
    """Guarda la lista de favoritos."""
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(favoritos, f, indent=2, ensure_ascii=False)


def agregar(ruta, nombre):
    """
    Agrega un favorito (en minúscula, sin repetir). Devuelve (ok, mensaje).
    """
    nombre = nombre.strip().lower()
    favoritos = cargar(ruta)
    if nombre in favoritos:
        return False, f"{nombre} ya estaba en favoritos."
    favoritos.append(nombre)
    guardar(ruta, favoritos)
    return True, f"⭐ {nombre} agregado a favoritos."


def quitar(ruta, nombre):
    """Quita un favorito. Devuelve (ok, mensaje)."""
    nombre = nombre.strip().lower()
    favoritos = cargar(ruta)
    if nombre not in favoritos:
        return False, f"{nombre} no estaba en favoritos."
    favoritos.remove(nombre)
    guardar(ruta, favoritos)
    return True, f"{nombre} quitado de favoritos."


def es_favorito(ruta, nombre):
    """Devuelve True si el nombre está en favoritos."""
    return nombre.strip().lower() in cargar(ruta)
