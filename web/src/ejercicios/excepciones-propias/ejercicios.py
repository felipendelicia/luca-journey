"""✏️ Ejercicios — Excepciones personalizadas

Además de los errores de Python, podés crear los TUYOS heredando de Exception.
Le dan un nombre claro a los problemas de tu programa. ✅ Corregir al terminar.
"""


# Tu propia excepción
# Definí EquipoLlenoError: su mensaje por defecto debe ser "equipo lleno".
# Pista: en __init__, llamá a super().__init__("equipo lleno").
class EquipoLlenoError(Exception):
    def __init__(self):
        # TU CÓDIGO ACÁ
        pass


# Excepción con datos extra
# Definí EntrenadorError: además del mensaje, guardá un atributo 'codigo'.
# Pista: super().__init__(mensaje) y self.codigo = codigo.
class EntrenadorError(Exception):
    def __init__(self, mensaje, codigo):
        # TU CÓDIGO ACÁ
        pass


# Usar tu excepción
# Agregá un Pokémon al equipo. Si ya hay 6, lanzá EquipoLlenoError(). Sino agregalo y
# devolvé el equipo.
# Ejemplo:  agregar(["Pikachu"], "Eevee")  →  ["Pikachu", "Eevee"]
def agregar(equipo, pokemon):
    """Agregá el Pokémon, o lanzá EquipoLlenoError si ya hay 6."""
    # TU CÓDIGO ACÁ
    pass


# Lanzar con datos
# Lanzá un EntrenadorError con el mensaje "acceso denegado" y el 'codigo' recibido.
# Pista: raise EntrenadorError("acceso denegado", codigo).
def fallar(codigo):
    """Lanzá un EntrenadorError("acceso denegado", codigo)."""
    # TU CÓDIGO ACÁ
    pass
