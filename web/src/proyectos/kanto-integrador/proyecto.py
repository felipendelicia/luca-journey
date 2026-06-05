# Integrador de Kanto — La Liga Pokémon (solución de referencia).
# El preamble (ENTRENADORES) está en meta.json y se antepone al corregir.

def clasificados(entrenadores, minimo):
    filtrados = [e for e in entrenadores if e["insignias"] >= minimo]
    return sorted(filtrados, key=lambda e: e["insignias"], reverse=True)


def nivel_promedio(entrenador):
    niveles = [p["nivel"] for p in entrenador["pokemones"]]
    return sum(niveles) / len(niveles)


def nivel_maximo(entrenador):
    return max(p["nivel"] for p in entrenador["pokemones"])


class Entrenador:
    def __init__(self, datos):
        self.nombre = datos["nombre"]
        self.insignias = datos["insignias"]
        self.pokemones = datos["pokemones"]

    def es_finalista(self):
        return self.insignias == 8

    def __str__(self):
        return "%s [%d insignias]" % (self.nombre, self.insignias)


def ranking(entrenadores):
    objetos = [Entrenador(e) for e in entrenadores]
    finalistas = [e for e in objetos if e.es_finalista()]
    return sorted(finalistas, key=lambda e: nivel_maximo({"pokemones": e.pokemones}), reverse=True)


def campeon(entrenadores):
    rank = ranking(entrenadores)
    if not rank:
        return None
    return rank[0].nombre
