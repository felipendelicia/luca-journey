"""
✏️ Semana 05 — Ejercicios: Funciones

Completá cada función donde dice '# TU CÓDIGO ACÁ'.
Algunos ejercicios te piden REFACTORIZAR: tomar código repetido y meterlo
en una función para no repetirte.

Para probar tu trabajo: en test_ejercicios.py cambiá _cargar("soluciones")
por _cargar("ejercicios"). Respuestas completas en soluciones.py.
"""


# 1) Calculá el daño: ataque menos defensa. Nunca menos de 0.
def calcular_dano(ataque, defensa):
    """Devolvé ataque - defensa, con mínimo 0."""
    # TU CÓDIGO ACÁ
    pass


# 2) Velocidad efectiva = velocidad base + (nivel * 2).
def velocidad_efectiva(velocidad, nivel):
    """Devolvé velocidad + nivel * 2."""
    # TU CÓDIGO ACÁ
    pass


# 3) Nivel a partir de la experiencia: cada 100 de exp = 1 nivel (división entera).
def nivel_por_experiencia(exp):
    """Devolvé exp // 100."""
    # TU CÓDIGO ACÁ
    pass


# 4) Experiencia necesaria para un nivel = nivel al cubo (nivel ** 3).
def experiencia_para_nivel(nivel):
    """Devolvé nivel ** 3."""
    # TU CÓDIGO ACÁ
    pass


# 5) Saludá al entrenador. La ciudad tiene un valor por DEFECTO: "Pueblo Paleta".
#    saludar_entrenador("Ash") -> "Hola Ash de Pueblo Paleta"
#    saludar_entrenador("Brock", "Ciudad Plateada") -> "Hola Brock de Ciudad Plateada"
def saludar_entrenador(nombre, ciudad="Pueblo Paleta"):
    """Devolvé 'Hola <nombre> de <ciudad>' usando el valor por defecto."""
    # TU CÓDIGO ACÁ
    pass


# 6) Aplicá una poción: sumá 'cura' al hp, sin pasar de hp_max. cura por defecto = 20.
def aplicar_pocion(hp, hp_max, cura=20):
    """Devolvé el hp curado, sin superar hp_max."""
    # TU CÓDIGO ACÁ
    pass


# 7) Promedio de tres stats.
def promedio_tres(a, b, c):
    """Devolvé el promedio de a, b y c."""
    # TU CÓDIGO ACÁ
    pass


# 8) Total de stats: sumá hp, ataque, defensa y velocidad.
def total_stats(hp, ataque, defensa, velocidad):
    """Devolvé la suma de los cuatro stats."""
    # TU CÓDIGO ACÁ
    pass


# 9) Clasificá el poder según el total de stats:
#    total < 200 -> "debil" ; total < 400 -> "promedio" ; si no -> "fuerte"
def clasificar_poder(total):
    """Devolvé 'debil', 'promedio' o 'fuerte'."""
    # TU CÓDIGO ACÁ
    pass


# 10) REFACTOR. Este código estaba repetido en muchos lados:
#         resultado = (ataque - defensa) + bonus
#         if resultado < 0: resultado = 0
#     Convertilo en una función con 'bonus' por defecto en 0.
def calcular_dano_con_bonus(ataque, defensa, bonus=0):
    """Devolvé (ataque - defensa) + bonus, con mínimo 0."""
    # TU CÓDIGO ACÁ
    pass


# 11) Multiplicador de efectividad: 2.0 si es súper efectivo, 1.0 si no.
#     Usá un parámetro 'es_super' con valor por defecto False.
def multiplicador_efectividad(es_super=False):
    """Devolvé 2.0 si es_super es True, sino 1.0."""
    # TU CÓDIGO ACÁ
    pass


# 12) REFACTOR / COMPOSICIÓN. Calculá el daño final REUSANDO otras funciones:
#     daño base = calcular_dano(ataque, defensa)
#     daño final = daño base * multiplicador_efectividad(es_super)
#     Devolvé el resultado como entero (int).
def dano_final(ataque, defensa, es_super=False):
    """Combiná calcular_dano y multiplicador_efectividad. Devolvé un int."""
    # TU CÓDIGO ACÁ
    pass


# 13) Factorial RECURSIVO. factorial(n) = n * factorial(n-1), con caso base factorial(0)=1.
def factorial(n):
    """Devolvé n! usando recursión (la función se llama a sí misma)."""
    # TU CÓDIGO ACÁ
    pass


# 14) Suma RECURSIVA del 1 al n. suma_recursiva(3) = 3 + 2 + 1 = 6.
def suma_recursiva(n):
    """Devolvé 1 + 2 + ... + n usando recursión."""
    # TU CÓDIGO ACÁ
    pass


# 15) Potencia RECURSIVA. potencia(2, 3) = 8. Caso base: exp 0 -> 1.
def potencia_recursiva(base, exp):
    """Devolvé base ** exp usando recursión."""
    # TU CÓDIGO ACÁ
    pass


# 16) Cuenta regresiva RECURSIVA. Para n=3 -> "3,2,1,Ya!".
def cuenta_regresiva_recursiva(n):
    """Devolvé la cuenta regresiva como string, usando recursión."""
    # TU CÓDIGO ACÁ
    pass


# ----------------------------------------------------------------------
# Ejercicios 17 a 20: definí estas LAMBDAS (funciones de una línea).
# Asignales una lambda a cada variable.
# ----------------------------------------------------------------------

# 17) 'doble' debe devolver el doble de un número. Ej: doble(5) -> 10.
doble = None  # TU CÓDIGO ACÁ (reemplazá None por una lambda)

# 18) 'al_cuadrado' debe devolver el número al cuadrado. Ej: al_cuadrado(4) -> 16.
al_cuadrado = None  # TU CÓDIGO ACÁ

# 19) 'mayor' debe devolver el más grande de dos números. Ej: mayor(3, 8) -> 8.
mayor = None  # TU CÓDIGO ACÁ

# 20) 'es_par' debe devolver True si el número es par. Ej: es_par(4) -> True.
es_par = None  # TU CÓDIGO ACÁ
