"""
⚔️ combates/desafios.py — Los Combates de Gimnasio (desafíos integradores).

Cada función es un "jefe de gimnasio": un reto más difícil que combina varios temas.
Se desbloquean en la Liga cuando tenés la medalla del gimnasio.

Completá donde dice '# TU CÓDIGO ACÁ'. Probá tu trabajo retando al líder desde
'python aventura.py'. Las respuestas están en soluciones.py.
"""


# 🪨 ROCA — Devolvé {extension: cantidad} de una lista de nombres de archivo.
#    Sin punto -> cuenta como 'sin_extension'.
def organizar_por_extension(nombres):
    """Devolvé un diccionario {extension: cantidad}."""
    # TU CÓDIGO ACÁ
    pass


# 💧 CASCADA — Duelo por turnos: ataca A, después B... Devolvé 'a' o 'b' (quién gana).
def simular_duelo(hp_a, hp_b, dano_a, dano_b):
    """Devolvé 'a' o 'b' según quién deja al otro en 0 primero (empieza A)."""
    # TU CÓDIGO ACÁ
    pass


# ⚡ TRUENO — Aplicá 'funcion' a 'valor' n veces. aplicar_n_veces(doble, 1, 3) -> 8.
def aplicar_n_veces(funcion, valor, n):
    """Devolvé el resultado de aplicar 'funcion' n veces sobre 'valor'."""
    # TU CÓDIGO ACÁ
    pass


# 🌈 ARCOÍRIS — Parseá un texto 'nombre,tipo,nivel' (una línea por Pokémon).
#    Devolvé una lista de dicts. Ignorá líneas vacías. nivel como int.
def parsear_equipo(texto):
    """Devolvé una lista de dicts {nombre, tipo, nivel}."""
    # TU CÓDIGO ACÁ
    pass


# 💜 ALMA — Completá la clase Mochila (agregar, usar, cantidad).
class Mochila:
    """Guarda objetos con su cantidad."""

    def __init__(self):
        # TU CÓDIGO ACÁ (creá self.items como diccionario vacío)
        pass

    def agregar(self, item, cantidad=1):
        """Sumá 'cantidad' del item."""
        # TU CÓDIGO ACÁ
        pass

    def usar(self, item):
        """Restá 1 al item. Devolvé True si había, False si no."""
        # TU CÓDIGO ACÁ
        pass

    def cantidad(self, item):
        """Devolvé cuántos hay de 'item' (0 si no está)."""
        # TU CÓDIGO ACÁ
        pass


# 🔮 PANTANO — Devolvé {suma, promedio, maximo, minimo} de una lista de números.
#    Lista vacía: suma 0, promedio 0, maximo y minimo None.
def estadisticas(numeros):
    """Devolvé el diccionario de estadísticas."""
    # TU CÓDIGO ACÁ
    pass


# 🌋 VOLCÁN — De una lista de dicts {nombre, tipo}, devolvé los NOMBRES sin
#    tipos repetidos (el primero de cada tipo, en orden).
def equipo_sin_tipos_repetidos(pokemones):
    """Devolvé la lista de nombres sin tipos repetidos."""
    # TU CÓDIGO ACÁ
    pass


# 🌍 TIERRA — Capstone. 'capturados' (nombres) y 'batallas' ('gano'/'perdio').
#    Devolvé {total, victorias, porcentaje} (porcentaje entero de victorias).
def resumen_entrenador(capturados, batallas):
    """Devolvé {total, victorias, porcentaje}."""
    # TU CÓDIGO ACÁ
    pass
