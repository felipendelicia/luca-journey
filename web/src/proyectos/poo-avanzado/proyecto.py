# Líder Blaine — Pokémon evolucionados (solución de referencia).
# El preamble (clase base Pokemon) está en meta.json y se antepone al corregir.

class PokemonFuego(Pokemon):
    def __init__(self, nombre, nivel, temperatura):
        super().__init__(nombre, "fuego", nivel)
        self.temperatura = temperatura

    def __str__(self):
        return "%s (Nv.%d) — 🔥 %d°C" % (self.nombre, self.nivel, self.temperatura)

    def evolucionar(self, nuevo_nombre):
        self.nombre = nuevo_nombre
        self.nivel += 10
        self.temperatura += 200
        return self


def equipo_fuego(datos):
    return [PokemonFuego(d["nombre"], d["nivel"], d["temperatura"]) for d in datos]


def mas_caliente(equipo):
    return max(equipo, key=lambda p: p.temperatura)
