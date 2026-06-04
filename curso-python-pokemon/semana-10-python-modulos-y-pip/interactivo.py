#!/usr/bin/env python3
"""
🌐 Pokédex Online — Semana 10

Usa la librería 'requests' para consultar la PokéAPI (https://pokeapi.co) y
mostrar datos REALES de cualquier Pokémon que ingreses.

Cómo jugar:
    pip install requests       (o: bash ../setup.sh)
    python interactivo.py

La función que parsea los datos (parsear_datos) es pura y testeable: no toca la
red. La función que descarga (consultar_pokeapi) importa requests de forma
"perezosa" para que el módulo se pueda importar aunque requests no esté instalada.
"""

URL_BASE = "https://pokeapi.co/api/v2/pokemon/"


def parsear_datos(datos):
    """
    Recibe el diccionario JSON crudo de la PokéAPI y devuelve un diccionario
    limpio y ordenado con lo que nos interesa. No usa internet.
    """
    # Los tipos vienen como una lista de dicts anidados; extraemos los nombres.
    tipos = [t["type"]["name"] for t in datos.get("types", [])]

    # Las estadísticas también vienen anidadas; armamos un dict simple.
    stats = {}
    for s in datos.get("stats", []):
        nombre_stat = s["stat"]["name"]
        stats[nombre_stat] = s["base_stat"]

    return {
        "nombre": datos.get("name", "?"),
        # La PokéAPI da altura en decímetros y peso en hectogramos; convertimos.
        "altura_m": datos.get("height", 0) / 10,
        "peso_kg": datos.get("weight", 0) / 10,
        "tipos": tipos,
        "stats": stats,
        "numero": datos.get("id", 0),
    }


def consultar_pokeapi(nombre):
    """
    Descarga los datos de un Pokémon de la PokéAPI.
    Devuelve el diccionario parseado, o None si falla (sin internet, no existe, etc.).
    """
    # Importamos requests acá adentro: si no está instalada, avisamos sin romper todo.
    try:
        import requests
    except ImportError:
        print("⚠️ Falta la librería 'requests'. Instalala con: pip install requests")
        return None

    url = URL_BASE + nombre.strip().lower()
    try:
        respuesta = requests.get(url, timeout=10)
    except Exception as error:
        print(f"⚠️ No se pudo conectar a la PokéAPI: {error}")
        return None

    if respuesta.status_code != 200:
        # 404 = no existe ese Pokémon.
        return None

    return parsear_datos(respuesta.json())


def formatear_ficha(info):
    """Arma una ficha de texto a partir del diccionario parseado."""
    tipos = ", ".join(info["tipos"]) if info["tipos"] else "?"
    lineas = [
        "=" * 40,
        f"  #{info['numero']:03d}  {info['nombre'].upper()}",
        "=" * 40,
        f"  Altura: {info['altura_m']} m",
        f"  Peso:   {info['peso_kg']} kg",
        f"  Tipos:  {tipos}",
        "  --- Estadísticas base ---",
    ]
    for nombre_stat, valor in info["stats"].items():
        lineas.append(f"  {nombre_stat:<16} {valor}")
    lineas.append("=" * 40)
    return "\n".join(lineas)


def jugar():
    print("=" * 50)
    print("🌐  POKÉDEX ONLINE — Semana 10")
    print("=" * 50)
    print("Consultá datos reales de la PokéAPI. Escribí 'salir' para terminar.\n")

    while True:
        try:
            nombre = input("Nombre del Pokémon (ej: pikachu) > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n¡Chau! 👋")
            return

        if nombre.lower() == "salir":
            print("¡Hasta la próxima, Entrenador! 👋")
            return
        if not nombre:
            continue

        print("🔎 Buscando...")
        info = consultar_pokeapi(nombre)
        if info is None:
            print(f"❌ No encontré a '{nombre}' (o no hay conexión). Probá otro.\n")
        else:
            print(formatear_ficha(info))
            print()


if __name__ == "__main__":
    jugar()
