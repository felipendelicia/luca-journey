"""
✏️ Semana 04 — Ejercicios: Control de Flujo

Completá cada función donde dice '# TU CÓDIGO ACÁ'.

Para probar TU trabajo: en test_ejercicios.py cambiá _cargar("soluciones")
por _cargar("ejercicios"). Las respuestas completas están en soluciones.py.
"""


# 1) Devolvé True si el Pokémon puede evolucionar (nivel 25 o más).
def puede_evolucionar(nivel):
    """Devolvé True si nivel >= 25, sino False."""
    # TU CÓDIGO ACÁ
    pass


# 2) Devolvé el estado según el HP:
#    hp > 70  -> "sano"
#    hp > 30  -> "herido"
#    hp > 0   -> "grave"
#    si no    -> "debilitado"
def estado_hp(hp):
    """Devolvé 'sano', 'herido', 'grave' o 'debilitado' según el hp."""
    # TU CÓDIGO ACÁ
    pass


# 3) Ventaja de tipo. Devolvé True si 'atacante' es súper efectivo contra 'defensor'.
#    Reglas: fuego>planta, agua>fuego, planta>agua, electrico>agua.
def ventaja_tipo(atacante, defensor):
    """Devolvé True si el atacante tiene ventaja sobre el defensor."""
    # TU CÓDIGO ACÁ
    pass


# 4) Devolvé el ataque más fuerte (el número mayor). Si son iguales, devolvé el primero.
def el_mas_fuerte(ataque_a, ataque_b):
    """Devolvé el mayor de los dos; si empatan, devolvé ataque_a."""
    # TU CÓDIGO ACÁ
    pass


# 5) Clasificá al Entrenador por nivel:
#    nivel < 16   -> "novato"
#    nivel < 40   -> "intermedio"
#    si no        -> "experto"
def clasificar_nivel(nivel):
    """Devolvé 'novato', 'intermedio' o 'experto'."""
    # TU CÓDIGO ACÁ
    pass


# 6) Devolvé True si el Pokémon necesita curarse (hp menor a 30).
def necesita_curarse(hp):
    """Devolvé True si hp < 30."""
    # TU CÓDIGO ACÁ
    pass


# 7) Resultado del combate comparando HP:
#    mi_hp > rival_hp -> "ganaste"
#    mi_hp < rival_hp -> "perdiste"
#    iguales          -> "empate"
def resultado_combate(mi_hp, rival_hp):
    """Devolvé 'ganaste', 'perdiste' o 'empate'."""
    # TU CÓDIGO ACÁ
    pass


# 8) Cuenta regresiva. Para n=3 devolvé el string "3,2,1,Ya!".
#    Usá un for o un while para armarlo.
def cuenta_regresiva(n):
    """Devolvé una cuenta regresiva como '3,2,1,Ya!'."""
    # TU CÓDIGO ACÁ
    pass


# 9) Sumá todos los números del 1 al n (inclusive) usando un bucle.
def suma_1_a_n(n):
    """Devolvé 1 + 2 + ... + n."""
    # TU CÓDIGO ACÁ
    pass


# 10) Calculá el factorial de n (n! = n * (n-1) * ... * 1). factorial(0) = 1.
def factorial(n):
    """Devolvé el factorial de n usando un bucle."""
    # TU CÓDIGO ACÁ
    pass


# 11) Contá cuántos números pares hay del 1 al n (inclusive).
def contar_pares(n):
    """Devolvé la cantidad de números pares entre 1 y n."""
    # TU CÓDIGO ACÁ
    pass


# 12) ¿Cuántos turnos hacen falta para debilitar al rival?
#     Cada turno le bajás 'dano' al 'hp_rival'. Contá los turnos hasta hp <= 0.
#     Ej: hp_rival=100, dano=30 -> 4 turnos (30,60,90,120).
def cuantos_turnos(hp_rival, dano):
    """Devolvé cuántos turnos de 'dano' hacen falta para que hp_rival llegue a 0."""
    # TU CÓDIGO ACÁ
    pass


# 13) Calculá base elevado a exp (potencia) usando un bucle, sin usar **.
def potencia(base, exp):
    """Devolvé base ** exp pero calculado con un bucle."""
    # TU CÓDIGO ACÁ
    pass


# 14) Devolvé True si n es primo (solo divisible por 1 y por sí mismo).
#     Recordá: 0 y 1 NO son primos.
def es_primo(n):
    """Devolvé True si n es primo, False si no."""
    # TU CÓDIGO ACÁ
    pass


# 15) Devolvé el menor divisor de n que sea mayor que 1.
#     Ej: primer_divisor(15) -> 3 ; primer_divisor(7) -> 7.
def primer_divisor(n):
    """Devolvé el divisor más chico de n mayor que 1."""
    # TU CÓDIGO ACÁ
    pass


# 16) Contá cuántas vocales (a, e, i, o, u) tiene una palabra.
def contar_vocales(palabra):
    """Devolvé la cantidad de vocales en la palabra (en minúsculas)."""
    # TU CÓDIGO ACÁ
    pass


# 17) Devolvé el mayor de tres números.
def mayor_de_tres(a, b, c):
    """Devolvé el más grande de a, b y c."""
    # TU CÓDIGO ACÁ
    pass


# 18) Devolvé "positivo", "negativo" o "cero" según el número.
def signo(numero):
    """Devolvé 'positivo', 'negativo' o 'cero'."""
    # TU CÓDIGO ACÁ
    pass


# 19) Buscá un Pokémon en el equipo (una lista de nombres).
#     Devolvé True si está, False si no. Usá un for con break.
def esta_en_equipo(equipo, nombre):
    """Devolvé True si 'nombre' está en la lista 'equipo'."""
    # TU CÓDIGO ACÁ
    pass


# 20) Contá cuántos Pokémon del equipo están debilitados.
#     'equipo_hp' es una lista de números (el HP de cada Pokémon).
#     Un Pokémon está debilitado si su HP es 0 o menos.
def contar_debilitados(equipo_hp):
    """Devolvé cuántos valores de la lista son <= 0."""
    # TU CÓDIGO ACÁ
    pass
