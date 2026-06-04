"""pokedex_app.pokeapi — Integración con la PokéAPI (igual que en la semana 12)."""

URL_BASE = "https://pokeapi.co/api/v2/pokemon/"


def parsear(datos):
    tipos = [t["type"]["name"] for t in datos.get("types", [])]
    return {
        "nombre": datos.get("name", "").capitalize(),
        "altura": datos.get("height", 0) / 10,
        "peso": datos.get("weight", 0) / 10,
        "tipo": tipos[0] if tipos else "",
        "descripcion": f"Pokémon de tipo {', '.join(tipos)}." if tipos else "",
    }


def consultar(nombre):
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
