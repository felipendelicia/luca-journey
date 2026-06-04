"""agenda_entrenador.pokemon — La clase Pokemon."""

from datetime import date


class Pokemon:
    def __init__(self, nombre, tipo, nivel, fecha_captura=None):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = int(nivel)
        self.fecha_captura = fecha_captura or date.today().isoformat()

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "nivel": self.nivel,
            "fecha_captura": self.fecha_captura,
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(datos["nombre"], datos["tipo"], datos["nivel"],
                   datos.get("fecha_captura"))

    def __eq__(self, otro):
        return isinstance(otro, Pokemon) and self.nombre == otro.nombre

    def __repr__(self):
        return f"Pokemon({self.nombre!r}, {self.tipo!r}, {self.nivel})"
