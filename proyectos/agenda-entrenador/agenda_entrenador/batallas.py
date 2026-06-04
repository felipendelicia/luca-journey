"""agenda_entrenador.batallas — Batalla e Historial."""

from datetime import date

GANO = "gano"
PERDIO = "perdio"


class Batalla:
    def __init__(self, rival, resultado, pokemon_usado, fecha=None):
        self.rival = rival
        self.resultado = resultado
        self.pokemon_usado = pokemon_usado
        self.fecha = fecha or date.today().isoformat()

    def gano(self):
        return self.resultado == GANO

    def to_dict(self):
        return {
            "rival": self.rival,
            "resultado": self.resultado,
            "pokemon_usado": self.pokemon_usado,
            "fecha": self.fecha,
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(datos["rival"], datos["resultado"],
                   datos["pokemon_usado"], datos.get("fecha"))

    def __repr__(self):
        return f"Batalla({self.rival!r}, {self.resultado!r})"


class Historial:
    def __init__(self):
        self.batallas = []

    def registrar(self, batalla):
        self.batallas.append(batalla)

    def total(self):
        return len(self.batallas)

    def victorias(self):
        return sum(1 for b in self.batallas if b.gano())

    def derrotas(self):
        return sum(1 for b in self.batallas if not b.gano())

    def to_list(self):
        return [b.to_dict() for b in self.batallas]
