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


# Error de HP
# Definí una excepción propia HPInvalidoError (hereda de Exception, cuerpo `pass`).
class HPInvalidoError(Exception):
    """Error: HP fuera de rango."""
    # TU CÓDIGO ACÁ
    pass


# Error de nivel
# Definí NivelInvalidoError (hereda de Exception).
class NivelInvalidoError(Exception):
    """Error: nivel fuera de rango."""
    # TU CÓDIGO ACÁ
    pass


# Error de saldo
# Definí SaldoInsuficienteError (hereda de Exception).
class SaldoInsuficienteError(Exception):
    """Error: no alcanza el saldo."""
    # TU CÓDIGO ACÁ
    pass


# Error de Pokémon no encontrado
# Definí PokemonNoEncontradoError (hereda de Exception).
class PokemonNoEncontradoError(Exception):
    """Error: ese Pokémon no está."""
    # TU CÓDIGO ACÁ
    pass


# Validar HP (con tu excepción)
# Si hp no está entre 0 y 100, lanzá HPInvalidoError; sino devolvé hp.
def validar_hp(hp):
    """Lanzá HPInvalidoError si hp está fuera de 0..100."""
    # TU CÓDIGO ACÁ
    pass


# Validar nivel (con tu excepción)
# Si nivel no está entre 1 y 100, lanzá NivelInvalidoError; sino devolvelo.
def validar_nivel(nivel):
    """Lanzá NivelInvalidoError si nivel está fuera de 1..100."""
    # TU CÓDIGO ACÁ
    pass


# Retirar (con tu excepción)
# Si monto > saldo, lanzá SaldoInsuficienteError; sino devolvé saldo - monto.
def retirar(saldo, monto):
    """Lanzá SaldoInsuficienteError si monto > saldo."""
    # TU CÓDIGO ACÁ
    pass


# Buscar Pokémon (con tu excepción)
# Si `nombre` no está en el dict `pokedex`, lanzá PokemonNoEncontradoError; sino devolvé su valor.
def buscar_pokemon(pokedex, nombre):
    """Lanzá PokemonNoEncontradoError si no está; sino devolvé pokedex[nombre]."""
    # TU CÓDIGO ACÁ
    pass


# Excepción con dato
# Definí RangoError que en __init__ reciba `valor`, lo guarde en self.valor y llame a
# super().__init__ con un mensaje que incluya ese valor.
class RangoError(Exception):
    """Error con el valor que falló (self.valor)."""
    # TU CÓDIGO ACÁ
    pass


# Validar en rango (con RangoError)
# Si n no está entre lo y hi, lanzá RangoError(n); sino devolvé n.
def validar_en_rango(n, lo, hi):
    """Lanzá RangoError(n) si n está fuera de [lo, hi]."""
    # TU CÓDIGO ACÁ
    pass


# Nombre del error
# Llamá a func(x). Si tira un error, devolvé el NOMBRE de la clase del error (type(e).__name__);
# si no tira nada, devolvé None.
# Ejemplo:  nombre_del_error(int, "pika")  →  "ValueError"
def nombre_del_error(func, x):
    """Devolvé el nombre de la clase del error que tira func(x), o None."""
    # TU CÓDIGO ACÁ
    pass


# Mensaje del error
# Devolvé el texto del error (convertirlo a string).
# Ejemplo:  mensaje_de(ValueError("mal"))  →  "mal"
def mensaje_de(error):
    """Devolvé el mensaje del error como string."""
    # TU CÓDIGO ACÁ
    pass


# ¿Es de esa clase?
# Devolvé True si `error` es una instancia de `clase`.
# Ejemplo:  es_instancia(ValueError("x"), ValueError)  →  True
def es_instancia(error, clase):
    """Devolvé True si error es instancia de clase."""
    # TU CÓDIGO ACÁ
    pass


# ¿Lanza ese error?
# Devolvé True si func(x) lanza un error de la clase `clase`; False si lanza otro o ninguno.
# Ejemplo:  lanza_ese_error(int, "pika", ValueError)  →  True
def lanza_ese_error(func, x, clase):
    """Devolvé True si func(x) lanza un error de tipo clase."""
    # TU CÓDIGO ACÁ
    pass


# Colección vacía
# Definí ColeccionVaciaError (hereda de Exception).
class ColeccionVaciaError(Exception):
    """Error: la colección está vacía."""
    # TU CÓDIGO ACÁ
    pass


# Sacar uno
# Si la colección está vacía, lanzá ColeccionVaciaError; sino sacá y devolvé el último elemento.
def sacar_uno(coleccion):
    """Lanzá ColeccionVaciaError si está vacía; sino devolvé el último."""
    # TU CÓDIGO ACÁ
    pass
