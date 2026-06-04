"""
agenda.batallas — Batalla e Historial.

Registra cada batalla con su resultado (ganó/perdió), contra quién y con qué
Pokémon se peleó.
"""

from datetime import date

# Resultados válidos.
GANO = "gano"
PERDIO = "perdio"


class Batalla:
    def __init__(self, rival, resultado, pokemon_usado, fecha=None):
        self.rival = rival
        # Normalizamos el resultado a 'gano' o 'perdio'.
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
        return cls(
            rival=datos["rival"],
            resultado=datos["resultado"],
            pokemon_usado=datos["pokemon_usado"],
            fecha=datos.get("fecha"),
        )

    def __repr__(self):
        return f"Batalla(rival={self.rival!r}, resultado={self.resultado!r})"


class Historial:
    def __init__(self):
        self.batallas = []

    def registrar(self, batalla):
        """Agrega una batalla al historial."""
        self.batallas.append(batalla)

    def total(self):
        return len(self.batallas)

    def victorias(self):
        return sum(1 for b in self.batallas if b.gano())

    def derrotas(self):
        return sum(1 for b in self.batallas if not b.gano())

    def to_list(self):
        return [b.to_dict() for b in self.batallas]
