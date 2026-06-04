"""
pokedex_cli.cli — El bucle interactivo de la Pokédex de consola.
"""

import os

from . import pokeapi, favoritos, ui

# Archivo de favoritos, al lado del proyecto.
RUTA_FAVORITOS = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "favoritos.json"
)


def mostrar_pokemon(nombre, ruta_favoritos=RUTA_FAVORITOS):
    """
    Busca un Pokémon y devuelve su ficha como texto, o un mensaje de error.
    Función testeable (la parte de red está en pokeapi.consultar).
    """
    info = pokeapi.consultar(nombre)
    if info is None:
        return f"❌ No encontré a '{nombre}' (o no hay conexión)."
    favorito = favoritos.es_favorito(ruta_favoritos, info["nombre"])
    return ui.ficha(info, favorito=favorito)


def run():
    print("=" * 44)
    print("🔴⚪  POKÉDEX CLI")
    print("=" * 44)
    print("Comandos: <nombre> para buscar | fav <nombre> | favoritos | salir\n")

    while True:
        try:
            entrada = input("pokedex> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n¡Chau! 👋")
            return

        if not entrada:
            continue

        partes = entrada.split(maxsplit=1)
        comando = partes[0].lower()

        if comando == "salir":
            print("¡Hasta la próxima, Entrenador! 👋")
            return

        elif comando == "favoritos":
            lista = favoritos.cargar(RUTA_FAVORITOS)
            if not lista:
                print("  (no tenés favoritos todavía)")
            else:
                print("  ⭐ Tus favoritos:")
                for nombre in lista:
                    print(f"    - {nombre}")

        elif comando == "fav" and len(partes) > 1:
            ok, msg = favoritos.agregar(RUTA_FAVORITOS, partes[1])
            print("  " + msg)

        elif comando == "quitar" and len(partes) > 1:
            ok, msg = favoritos.quitar(RUTA_FAVORITOS, partes[1])
            print("  " + msg)

        else:
            # Cualquier otra cosa se interpreta como el nombre de un Pokémon.
            print("🔎 Buscando...")
            print(mostrar_pokemon(entrada))


if __name__ == "__main__":
    run()
