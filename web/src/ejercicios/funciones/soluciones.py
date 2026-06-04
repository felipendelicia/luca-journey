"""
✅ Semana 05 — Soluciones: Funciones

Comentadas línea por línea.
"""


# 1)
def calcular_dano(ataque, defensa):
    """Devolvé ataque - defensa, con mínimo 0."""
    # Calculamos la resta.
    dano = ataque - defensa
    # Si quedó negativo, lo dejamos en 0 (no existe daño negativo).
    if dano < 0:
        dano = 0
    return dano


# 2)
def velocidad_efectiva(velocidad, nivel):
    """Velocidad + nivel * 2."""
    # El nivel suma 2 puntos de velocidad por cada nivel.
    return velocidad + nivel * 2


# 3)
def nivel_por_experiencia(exp):
    """exp // 100."""
    # // es la división entera: descarta los decimales.
    return exp // 100


# 4)
def experiencia_para_nivel(nivel):
    """nivel ** 3."""
    # ** es la potencia. nivel al cubo.
    return nivel ** 3


# 5)
def saludar_entrenador(nombre, ciudad="Pueblo Paleta"):
    """'Hola <nombre> de <ciudad>'."""
    # Si no pasan 'ciudad', se usa el valor por defecto.
    return f"Hola {nombre} de {ciudad}"


# 6)
def aplicar_pocion(hp, hp_max, cura=20):
    """Cura sin superar hp_max."""
    # Sumamos la cura.
    nuevo = hp + cura
    # Si pasamos el máximo, lo limitamos al máximo.
    if nuevo > hp_max:
        nuevo = hp_max
    return nuevo


# 7)
def promedio_tres(a, b, c):
    """Promedio de tres números."""
    return (a + b + c) / 3


# 8)
def total_stats(hp, ataque, defensa, velocidad):
    """Suma de los cuatro stats."""
    return hp + ataque + defensa + velocidad


# 9)
def clasificar_poder(total):
    """Clasificá el poder."""
    if total < 200:
        return "debil"
    elif total < 400:
        return "promedio"
    else:
        return "fuerte"


# 10) REFACTOR
def calcular_dano_con_bonus(ataque, defensa, bonus=0):
    """(ataque - defensa) + bonus, mínimo 0."""
    # Antes este cálculo estaba copiado en muchos lados; ahora vive acá.
    resultado = (ataque - defensa) + bonus
    if resultado < 0:
        resultado = 0
    return resultado


# 11)
def multiplicador_efectividad(es_super=False):
    """2.0 si es súper efectivo, 1.0 si no."""
    if es_super:
        return 2.0
    else:
        return 1.0


# 12) COMPOSICIÓN: reusamos funciones que ya escribimos.
def dano_final(ataque, defensa, es_super=False):
    """Combiná calcular_dano y el multiplicador."""
    # Reusamos calcular_dano para el daño base.
    base = calcular_dano(ataque, defensa)
    # Reusamos el multiplicador según la efectividad.
    multiplicador = multiplicador_efectividad(es_super)
    # int() descarta los decimales del resultado.
    return int(base * multiplicador)


# 13) Recursión
def factorial(n):
    """Factorial recursivo."""
    # Caso base: frena la recursión.
    if n <= 1:
        return 1
    # Caso recursivo: la función se llama con un número más chico.
    return n * factorial(n - 1)


# 14) Recursión
def suma_recursiva(n):
    """Suma 1..n recursivamente."""
    # Caso base.
    if n <= 0:
        return 0
    # Sumamos n y delegamos el resto a la misma función.
    return n + suma_recursiva(n - 1)


# 15) Recursión
def potencia_recursiva(base, exp):
    """base ** exp recursivo."""
    # Caso base: cualquier número elevado a 0 es 1.
    if exp == 0:
        return 1
    # Multiplicamos la base por la potencia con un exponente menos.
    return base * potencia_recursiva(base, exp - 1)


# 16) Recursión
def cuenta_regresiva_recursiva(n):
    """Cuenta regresiva como string, recursiva."""
    # Caso base: cuando llegamos a 0, ponemos el final.
    if n == 0:
        return "Ya!"
    # Caso recursivo: el número actual + la cuenta del resto.
    return str(n) + "," + cuenta_regresiva_recursiva(n - 1)


# ----------------------------------------------------------------------
# 17 a 20) Lambdas
# ----------------------------------------------------------------------

# 'lambda x: x * 2' es una función sin nombre que recibe x y devuelve x*2.
doble = lambda x: x * 2

al_cuadrado = lambda x: x ** 2

# Si a es mayor que b devuelve a, sino b (expresión condicional en una línea).
mayor = lambda a, b: a if a > b else b

es_par = lambda x: x % 2 == 0
