"""
pokedex_cli.ascii_art — Sprites en ASCII según el tipo del Pokémon.

No son sprites reales (eso requeriría imágenes), pero le dan onda a la Pokédex.
Cada tipo tiene su dibujito; si el tipo no está, usamos uno genérico.
"""

# Un sprite ASCII por tipo. Simples a propósito, para que entren en la consola.
SPRITES = {
    "fire": r"""
      (    )
     (      )
      )    (
    .-~~~~~~-.
   (  ^    ^  )
    \   __   /
     '-.__.-'
    """,
    "water": r"""
      .-~~~-.
    .'  o o  '.
   (    \_/    )
    '.  ___  .'
      '-...-'
     ~ ~ ~ ~ ~
    """,
    "grass": r"""
       _\|/_
      (  o o )
     (   \_/  )
      \  ___ /
       \/   \/
      \ |   | /
    """,
    "electric": r"""
       \   /
      __\_/__
     ( o   o )
      \  ^  /
       \___/
      zZ  zZ
    """,
    "psychic": r"""
      .-~*~-.
     ( o   o )
     (  .v.  )
      \ '-' /
       '~*~'
    """,
    "rock": r"""
     __________
    /  o    o  \
   |   ______   |
   |  /      \  |
    \________ _/
    """,
}

GENERICO = r"""
      .-""-.
     / o  o \
    |   __   |
     \  --  /
      '-..-'
"""


def sprite(tipo):
    """Devuelve el sprite ASCII correspondiente al tipo (o uno genérico)."""
    return SPRITES.get(tipo.lower(), GENERICO)
