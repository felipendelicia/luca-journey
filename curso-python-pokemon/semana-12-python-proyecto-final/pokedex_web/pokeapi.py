"""
pokedex_web.pokeapi — Integración con la PokéAPI.

Consulta datos reales de un Pokémon para autocompletar el formulario.
Importa 'requests' de forma perezosa para que el módulo se pueda importar
aunque requests no esté instalada.
"""

URL_BASE = "https://pokeapi.co/api/v2/pokemon/"


def parsear(datos):
    """Convierte el JSON crudo de la PokéAPI en un dict simple para el formulario."""
    tipos = [t["type"]["name"] for t in datos.get("types", [])]
    return {
        "nombre": datos.get("name", "").capitalize(),
        # La API da altura en decímetros y peso en hectogramos.
        "altura": datos.get("height", 0) / 10,
        "peso": datos.get("weight", 0) / 10,
        "tipo": tipos[0] if tipos else "",
        "descripcion": f"Pokémon de tipo {', '.join(tipos)}." if tipos else "",
    }


def consultar(nombre):
    """
    Descarga datos de un Pokémon de la PokéAPI.
    Devuelve el dict parseado, o None si falla (sin internet, no existe, etc.).
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
