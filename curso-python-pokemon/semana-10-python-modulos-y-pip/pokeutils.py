"""
🧰 pokeutils.py — Tu primer MÓDULO PROPIO (mini proyecto de la semana 10)

Un módulo es simplemente un archivo .py con funciones reutilizables. Este junta
utilidades Pokémon que podés importar desde otros programas así:

    import pokeutils
    print(pokeutils.formatear_nombre("pikachu"))   # Pikachu

Probalo importándolo desde ejercicios.py o desde el REPL.
"""

# Lista de algunos Pokémon legendarios conocidos (en minúscula).
LEGENDARIOS = [
    "mewtwo", "mew", "articuno", "zapdos", "moltres",
    "lugia", "ho-oh", "rayquaza", "dialga", "palkia",
]

# Multiplicadores de daño básicos entre tipos.
VENTAJAS = {
    "fuego": "planta",
    "agua": "fuego",
    "planta": "agua",
    "electrico": "agua",
}


def formatear_nombre(nombre):
    """Devuelve el nombre con la primera letra en mayúscula. 'pikachu' -> 'Pikachu'."""
    return nombre.strip().capitalize()


def es_legendario(nombre):
    """Devuelve True si el Pokémon está en la lista de legendarios."""
    return nombre.strip().lower() in LEGENDARIOS


def tiene_ventaja(tipo_atacante, tipo_defensor):
    """Devuelve True si el tipo atacante tiene ventaja sobre el defensor."""
    return VENTAJAS.get(tipo_atacante.lower()) == tipo_defensor.lower()


def slug(nombre):
    """
    Convierte un nombre a 'slug' para la PokéAPI:
    minúsculas y espacios convertidos en guiones. 'Mr Mime' -> 'mr-mime'.
    """
    return nombre.strip().lower().replace(" ", "-")


def resumen(nombre, tipo, nivel):
    """Devuelve una línea resumen de un Pokémon."""
    estrella = " ⭐" if es_legendario(nombre) else ""
    return f"{formatear_nombre(nombre)} | Tipo: {tipo} | Nv {nivel}{estrella}"


# Si el módulo se ejecuta directamente (en vez de importarse), mostramos una demo.
if __name__ == "__main__":
    print("Demo de pokeutils:")
    print(resumen("pikachu", "Electrico", 25))
    print(resumen("mewtwo", "Psiquico", 70))
    print("¿Fuego le gana a Planta?", tiene_ventaja("fuego", "planta"))
