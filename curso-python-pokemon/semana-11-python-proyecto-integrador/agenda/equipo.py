"""
agenda.equipo — La clase Equipo.

Maneja el equipo activo del Entrenador: como máximo 6 Pokémon, sin repetir nombres.
"""

from .pokemon import Pokemon

MAX_EQUIPO = 6


class Equipo:
    def __init__(self):
        # Lista de objetos Pokemon que forman el equipo activo.
        self.miembros = []

    def agregar(self, pokemon):
        """
        Agrega un Pokémon al equipo. Devuelve (ok, mensaje).
        Reglas: máximo 6 y sin nombres repetidos.
        """
        if len(self.miembros) >= MAX_EQUIPO:
            return False, f"El equipo está lleno (máximo {MAX_EQUIPO})."
        if self.esta(pokemon.nombre):
            return False, f"{pokemon.nombre} ya está en el equipo."
        self.miembros.append(pokemon)
        return True, f"{pokemon.nombre} se unió al equipo."

    def quitar(self, nombre):
        """Quita un Pokémon por nombre. Devuelve (ok, mensaje)."""
        encontrado = self.buscar(nombre)
        if encontrado is None:
            return False, f"{nombre} no está en el equipo."
        self.miembros.remove(encontrado)
        return True, f"{nombre} dejó el equipo."

    def buscar(self, nombre):
        """Devuelve el Pokémon del equipo con ese nombre, o None."""
        for p in self.miembros:
            if p.nombre.lower() == nombre.lower():
                return p
        return None

    def esta(self, nombre):
        """Devuelve True si hay un Pokémon con ese nombre en el equipo."""
        return self.buscar(nombre) is not None

    def lleno(self):
        return len(self.miembros) >= MAX_EQUIPO

    def cantidad(self):
        return len(self.miembros)

    def nombres(self):
        return [p.nombre for p in self.miembros]

    def to_list(self):
        """Lista de nombres del equipo (para guardar en JSON)."""
        return self.nombres()
