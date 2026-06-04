"""✏️ Ejercicios — Funciones

Definir funciones, parámetros por defecto, recursión y lambdas. Algunos piden
REFACTORIZAR: meter código repetido en una función. ✅ Corregir cuando termines.
"""


# Calcular el daño
# Devolvé ataque menos defensa, pero nunca menos de 0.
# Ejemplo:  calcular_dano(80, 50)  →  30   ·   calcular_dano(20, 50)  →  0
def calcular_dano(ataque, defensa):
    """Devolvé ataque - defensa, con mínimo 0."""
    # TU CÓDIGO ACÁ
    pass


# Velocidad efectiva
# Devolvé la velocidad base más nivel × 2.
# Ejemplo:  velocidad_efectiva(60, 20)  →  100
def velocidad_efectiva(velocidad, nivel):
    """Devolvé velocidad + nivel * 2."""
    # TU CÓDIGO ACÁ
    pass


# Nivel por experiencia
# Cada 100 de experiencia equivale a 1 nivel (usá división entera //).
# Ejemplo:  nivel_por_experiencia(350)  →  3
def nivel_por_experiencia(exp):
    """Devolvé exp // 100."""
    # TU CÓDIGO ACÁ
    pass


# Experiencia para subir
# La experiencia necesaria para un nivel es el nivel al cubo (nivel ** 3).
# Ejemplo:  experiencia_para_nivel(5)  →  125
def experiencia_para_nivel(nivel):
    """Devolvé nivel ** 3."""
    # TU CÓDIGO ACÁ
    pass


# Saludo con ciudad por defecto
# Devolvé 'Hola <nombre> de <ciudad>'. 'ciudad' tiene valor por defecto "Pueblo Paleta".
# Ejemplo:  saludar_entrenador("Ash")  →  "Hola Ash de Pueblo Paleta"
#           saludar_entrenador("Brock", "Ciudad Plateada")  →  "Hola Brock de Ciudad Plateada"
def saludar_entrenador(nombre, ciudad="Pueblo Paleta"):
    """Devolvé 'Hola <nombre> de <ciudad>'."""
    # TU CÓDIGO ACÁ
    pass


# Aplicar poción
# Sumá 'cura' al hp, pero sin pasar de hp_max. 'cura' por defecto es 20.
# Ejemplo:  aplicar_pocion(90, 100)  →  100   ·   aplicar_pocion(50, 100, 30)  →  80
def aplicar_pocion(hp, hp_max, cura=20):
    """Devolvé el hp curado, sin superar hp_max."""
    # TU CÓDIGO ACÁ
    pass


# Promedio de tres
# Devolvé el promedio de los tres stats.
# Ejemplo:  promedio_tres(30, 60, 90)  →  60.0
def promedio_tres(a, b, c):
    """Devolvé el promedio de a, b y c."""
    # TU CÓDIGO ACÁ
    pass


# Total de stats
# Sumá hp, ataque, defensa y velocidad.
# Ejemplo:  total_stats(45, 49, 49, 45)  →  188
def total_stats(hp, ataque, defensa, velocidad):
    """Devolvé la suma de los cuatro stats."""
    # TU CÓDIGO ACÁ
    pass


# Clasificar el poder
# Según el total de stats:  total < 200 → "debil" ,  total < 400 → "promedio" ,
#                           si no      → "fuerte".
# Ejemplo:  clasificar_poder(188)  →  "debil"
def clasificar_poder(total):
    """Devolvé 'debil', 'promedio' o 'fuerte'."""
    # TU CÓDIGO ACÁ
    pass


# Refactor: daño con bonus
# Este cálculo estaba repetido por todos lados: (ataque - defensa) + bonus, con mínimo 0.
# Metelo en esta función, con 'bonus' por defecto en 0.
# Ejemplo:  calcular_dano_con_bonus(80, 50, 10)  →  40
def calcular_dano_con_bonus(ataque, defensa, bonus=0):
    """Devolvé (ataque - defensa) + bonus, con mínimo 0."""
    # TU CÓDIGO ACÁ
    pass


# Multiplicador de efectividad
# Devolvé 2.0 si es súper efectivo, 1.0 si no. 'es_super' por defecto es False.
# Ejemplo:  multiplicador_efectividad(True)  →  2.0
def multiplicador_efectividad(es_super=False):
    """Devolvé 2.0 si es_super es True, sino 1.0."""
    # TU CÓDIGO ACÁ
    pass


# Daño final (componer funciones)
# Reusá las funciones de arriba:  daño base = calcular_dano(ataque, defensa) ,
# daño final = daño base × multiplicador_efectividad(es_super). Devolvé un int.
# Ejemplo:  dano_final(80, 50, True)  →  60
def dano_final(ataque, defensa, es_super=False):
    """Combiná calcular_dano y multiplicador_efectividad. Devolvé un int."""
    # TU CÓDIGO ACÁ
    pass


# Factorial recursivo
# factorial(n) = n × factorial(n-1), con caso base factorial(0) = 1.
# Ejemplo:  factorial(5)  →  120
def factorial(n):
    """Devolvé n! usando recursión."""
    # TU CÓDIGO ACÁ
    pass


# Suma recursiva
# Sumá del 1 al n llamando a la función dentro de sí misma.
# Ejemplo:  suma_recursiva(3)  →  6   (3 + 2 + 1)
def suma_recursiva(n):
    """Devolvé 1 + 2 + ... + n usando recursión."""
    # TU CÓDIGO ACÁ
    pass


# Potencia recursiva
# base elevado a exp, con recursión. Caso base: exp 0 → 1.
# Ejemplo:  potencia_recursiva(2, 3)  →  8
def potencia_recursiva(base, exp):
    """Devolvé base ** exp usando recursión."""
    # TU CÓDIGO ACÁ
    pass


# Cuenta regresiva recursiva
# Igual que antes pero con recursión. Para n=3 → "3,2,1,Ya!".
# Ejemplo:  cuenta_regresiva_recursiva(3)  →  "3,2,1,Ya!"
def cuenta_regresiva_recursiva(n):
    """Devolvé la cuenta regresiva como string, usando recursión."""
    # TU CÓDIGO ACÁ
    pass


# ── Lambdas: funciones de una línea. Reemplazá None por una lambda. ──

# 'doble' devuelve el doble de un número.       Ej:  doble(5)  →  10
doble = None  # TU CÓDIGO ACÁ

# 'al_cuadrado' devuelve el número al cuadrado. Ej:  al_cuadrado(4)  →  16
al_cuadrado = None  # TU CÓDIGO ACÁ

# 'mayor' devuelve el más grande de dos números. Ej:  mayor(3, 8)  →  8
mayor = None  # TU CÓDIGO ACÁ

# 'es_par' devuelve True si el número es par.   Ej:  es_par(4)  →  True
es_par = None  # TU CÓDIGO ACÁ
