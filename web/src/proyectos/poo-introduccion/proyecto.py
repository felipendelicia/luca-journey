# Líder Sabrina — Pokémon en clases (solución de referencia).
# El preamble (DATA) está en meta.json y se antepone al corregir.

class Pokemon:
    def __init__(self, nombre, tipo, nivel):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel

    def presentar(self):
        return "Soy %s, de tipo %s. Nivel: %d." % (self.nombre, self.tipo, self.nivel)

    def subir_nivel(self, cantidad):
        self.nivel += cantidad


def desde_dict(data):
    return [Pokemon(d["nombre"], d["tipo"], d["nivel"]) for d in data]
