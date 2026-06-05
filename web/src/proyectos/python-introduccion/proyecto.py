# Líder Brock — Pokédex de consola (solución de referencia).
# El preamble (POKEDEX) está en meta.json y se antepone al corregir.

def buscar(nombre):
    return POKEDEX.get(nombre.lower())

def mostrar(poke):
    if poke is None:
        return "No encontrado."
    return "Tipo: %s · Nivel: %d" % (poke["tipo"], poke["nivel"])

def responder(nombre):
    return mostrar(buscar(nombre))

def pokedex(consultas):
    return [responder(n) for n in consultas]
