"""
pokedex_cli.ui — Formato de la ficha en consola.
"""

from . import ascii_art


def barra_stat(valor, largo=20, maximo=160):
    """Barra visual para un stat (los stats base llegan hasta ~160)."""
    llenos = int((valor / maximo) * largo)
    llenos = max(0, min(largo, llenos))
    return "█" * llenos + "░" * (largo - llenos)


def ficha(info, favorito=False):
    """
    Arma la ficha completa (sprite + datos + stats) a partir del dict parseado.
    'favorito' agrega una estrellita si el Pokémon está guardado.
    """
    estrella = " ⭐" if favorito else ""
    lineas = [ascii_art.sprite(info["tipo_principal"])]
    lineas.append("=" * 44)
    lineas.append(f"  #{info['id']:03d}  {info['nombre'].upper()}{estrella}")
    lineas.append("=" * 44)
    lineas.append(f"  Tipos:  {', '.join(info['tipos']) or '?'}")
    lineas.append(f"  Altura: {info['altura_m']} m   Peso: {info['peso_kg']} kg")
    lineas.append("  --- Stats base ---")
    for nombre_stat, valor in info["stats"].items():
        lineas.append(f"  {nombre_stat:<16} {barra_stat(valor)} {valor}")
    lineas.append("=" * 44)
    return "\n".join(lineas)
