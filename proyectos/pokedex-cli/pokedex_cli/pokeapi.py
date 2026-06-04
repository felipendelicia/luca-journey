"""
pokedex_cli.pokeapi — Cliente de la PokéAPI.

Separamos la descarga (consultar, usa internet) del parseo (parsear, función
pura y testeable).
"""

URL_BASE = "https://pokeapi.co/api/v2/pokemon/"


def parsear(datos):
    """Convierte el JSON crudo de la PokéAPI en un diccionario limpio."""
    tipos = [t["type"]["name"] for t in datos.get("types", [])]

    stats = {}
    for s in datos.get("stats", []):
        stats[s["stat"]["name"]] = s["base_stat"]

    return {
        "id": datos.get("id", 0),
        "nombre": datos.get("name", "?"),
        "altura_m": datos.get("height", 0) / 10,
        "peso_kg": datos.get("weight", 0) / 10,
        "tipos": tipos,
        "tipo_principal": tipos[0] if tipos else "normal",
        "stats": stats,
    }


def consultar(nombre):
    """
    Descarga datos de un Pokémon. Devuelve el dict parseado o None si falla.
    """
    try:
        import requests
    except ImportError:
        return None

    try:
        respuesta = requests.get(URL_BASE + nombre.strip().lower(), timeout=10)
    except Exception:
        return None

    if respuesta.status_code != 200:
        return None
    return parsear(respuesta.json())
