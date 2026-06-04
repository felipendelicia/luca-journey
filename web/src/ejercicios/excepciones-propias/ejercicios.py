"""
✏️ Ejercicios — Excepciones personalizadas

Además de los errores de Python, podés crear los TUYOS heredando de Exception.
Le dan un nombre claro a los problemas de tu programa.
"""


# 1) Definí EquipoLlenoError: su mensaje por defecto debe ser "equipo lleno".
class EquipoLlenoError(Exception):
    def __init__(self):
        # TU CÓDIGO ACÁ: llamá a super().__init__("equipo lleno")
        pass


# 2) Definí EntrenadorError: guardá un atributo 'codigo' además del mensaje.
class EntrenadorError(Exception):
    def __init__(self, mensaje, codigo):
        # TU CÓDIGO ACÁ: super().__init__(mensaje) y self.codigo = codigo
        pass


# 3) Agregá un Pokémon al equipo. Si ya hay 6, lanzá EquipoLlenoError().
def agregar(equipo, pokemon):
    """if len(equipo) >= 6: raise EquipoLlenoError(). Sino agregalo y devolvé el equipo."""
    # TU CÓDIGO ACÁ
    pass


# 4) Lanzá un EntrenadorError con el mensaje "acceso denegado" y el código recibido.
def fallar(codigo):
    """raise EntrenadorError("acceso denegado", codigo)."""
    # TU CÓDIGO ACÁ
    pass
