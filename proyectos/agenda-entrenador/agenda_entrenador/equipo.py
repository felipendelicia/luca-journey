"""agenda_entrenador.equipo — La clase Equipo (máximo 6 activos)."""

MAX_EQUIPO = 6


class Equipo:
    def __init__(self):
        self.miembros = []

    def agregar(self, pokemon):
        if len(self.miembros) >= MAX_EQUIPO:
            return False, f"El equipo está lleno (máximo {MAX_EQUIPO})."
        if self.esta(pokemon.nombre):
            return False, f"{pokemon.nombre} ya está en el equipo."
        self.miembros.append(pokemon)
        return True, f"{pokemon.nombre} se unió al equipo."

    def quitar(self, nombre):
        encontrado = self.buscar(nombre)
        if encontrado is None:
            return False, f"{nombre} no está en el equipo."
        self.miembros.remove(encontrado)
        return True, f"{nombre} dejó el equipo."

    def buscar(self, nombre):
        for p in self.miembros:
            if p.nombre.lower() == nombre.lower():
                return p
        return None

    def esta(self, nombre):
        return self.buscar(nombre) is not None

    def lleno(self):
        return len(self.miembros) >= MAX_EQUIPO

    def cantidad(self):
        return len(self.miembros)

    def nombres(self):
        return [p.nombre for p in self.miembros]

    def to_list(self):
        return self.nombres()
