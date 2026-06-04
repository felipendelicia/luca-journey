"""
agenda.pokemon — La clase Pokemon.

Representa un Pokémon capturado, con nombre, tipo, nivel y fecha de captura.
Sabe convertirse a/desde diccionario (para guardarlo en JSON).
"""

from datetime import date


class Pokemon:
    def __init__(self, nombre, tipo, nivel, fecha_captura=None):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = int(nivel)
        # Si no nos dan fecha, usamos la de hoy en formato ISO (AAAA-MM-DD).
        self.fecha_captura = fecha_captura or date.today().isoformat()

    def to_dict(self):
        """Convierte el Pokémon a un diccionario simple (para JSON)."""
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "nivel": self.nivel,
            "fecha_captura": self.fecha_captura,
        }

    @classmethod
    def from_dict(cls, datos):
        """Crea un Pokemon a partir de un diccionario (al cargar de JSON)."""
        return cls(
            nombre=datos["nombre"],
            tipo=datos["tipo"],
            nivel=datos["nivel"],
            fecha_captura=datos.get("fecha_captura"),
        )

    def __eq__(self, otro):
        # Dos Pokémon se consideran iguales si tienen el mismo nombre.
        return isinstance(otro, Pokemon) and self.nombre == otro.nombre

    def __repr__(self):
        return f"Pokemon({self.nombre!r}, {self.tipo!r}, {self.nivel})"

    def __str__(self):
        return f"{self.nombre} ({self.tipo}) Nv{self.nivel} — capturado {self.fecha_captura}"
