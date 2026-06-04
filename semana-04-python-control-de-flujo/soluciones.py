"""
✅ Semana 04 — Soluciones: Control de Flujo

Comentadas línea por línea. Mirá después de intentar. 😉
"""


# 1)
def puede_evolucionar(nivel):
    """Devolvé True si nivel >= 25."""
    # La comparación >= ya devuelve True o False directamente.
    return nivel >= 25


# 2)
def estado_hp(hp):
    """Devolvé el estado según el hp."""
    # Revisamos de mayor a menor. Python entra en la primera condición verdadera.
    if hp > 70:
        return "sano"
    elif hp > 30:
        return "herido"
    elif hp > 0:
        return "grave"
    else:
        return "debilitado"


# 3)
def ventaja_tipo(atacante, defensor):
    """Devolvé True si el atacante es súper efectivo contra el defensor."""
    # Guardamos las reglas como pares (atacante, defensor) con ventaja.
    # (Las estructuras de datos las vemos a fondo en la semana 6; acá usamos lo justo.)
    if atacante == "fuego" and defensor == "planta":
        return True
    elif atacante == "agua" and defensor == "fuego":
        return True
    elif atacante == "planta" and defensor == "agua":
        return True
    elif atacante == "electrico" and defensor == "agua":
        return True
    else:
        return False


# 4)
def el_mas_fuerte(ataque_a, ataque_b):
    """Devolvé el mayor; si empatan, ataque_a."""
    # Si a es mayor o igual, gana a; si no, gana b.
    if ataque_a >= ataque_b:
        return ataque_a
    else:
        return ataque_b


# 5)
def clasificar_nivel(nivel):
    """Devolvé la categoría del Entrenador."""
    if nivel < 16:
        return "novato"
    elif nivel < 40:
        return "intermedio"
    else:
        return "experto"


# 6)
def necesita_curarse(hp):
    """Devolvé True si hp < 30."""
    return hp < 30


# 7)
def resultado_combate(mi_hp, rival_hp):
    """Compará los HP y devolvé el resultado."""
    if mi_hp > rival_hp:
        return "ganaste"
    elif mi_hp < rival_hp:
        return "perdiste"
    else:
        return "empate"


# 8)
def cuenta_regresiva(n):
    """Armá una cuenta regresiva como '3,2,1,Ya!'."""
    # Empezamos con un string vacío y le vamos pegando los números.
    resultado = ""
    # range(n, 0, -1) va de n hasta 1 (bajando de a 1).
    for numero in range(n, 0, -1):
        resultado = resultado + str(numero) + ","
    # Al final agregamos "Ya!".
    return resultado + "Ya!"


# 9)
def suma_1_a_n(n):
    """Sumá del 1 al n."""
    # Acumulador: arranca en 0 y va sumando.
    total = 0
    # range(1, n+1) genera del 1 al n (el +1 porque el final no se incluye).
    for numero in range(1, n + 1):
        total = total + numero
    return total


# 10)
def factorial(n):
    """Calculá n! con un bucle."""
    # El factorial arranca en 1 (factorial(0) = 1).
    resultado = 1
    for numero in range(1, n + 1):
        # En cada vuelta multiplicamos por el número actual.
        resultado = resultado * numero
    return resultado


# 11)
def contar_pares(n):
    """Contá los pares del 1 al n."""
    cantidad = 0
    for numero in range(1, n + 1):
        # Un número es par si el resto de dividir por 2 es 0.
        if numero % 2 == 0:
            cantidad = cantidad + 1
    return cantidad


# 12)
def cuantos_turnos(hp_rival, dano):
    """Contá turnos hasta debilitar al rival."""
    turnos = 0
    # Mientras el rival tenga HP, atacamos y contamos un turno.
    while hp_rival > 0:
        hp_rival = hp_rival - dano
        turnos = turnos + 1
    return turnos


# 13)
def potencia(base, exp):
    """Calculá base ** exp con un bucle."""
    # Cualquier número elevado a 0 es 1, así que arrancamos en 1.
    resultado = 1
    # Repetimos 'exp' veces, multiplicando por la base cada vez.
    for _ in range(exp):
        resultado = resultado * base
    return resultado


# 14)
def es_primo(n):
    """Devolvé True si n es primo."""
    # 0 y 1 no son primos por definición.
    if n < 2:
        return False
    # Probamos dividir por cada número del 2 al n-1.
    for divisor in range(2, n):
        if n % divisor == 0:
            # Si encontramos un divisor, no es primo: cortamos con return.
            return False
    # Si no encontramos ninguno, es primo.
    return True


# 15)
def primer_divisor(n):
    """Devolvé el menor divisor de n mayor que 1."""
    # Probamos del 2 hasta n. El primero que divida exacto es la respuesta.
    for divisor in range(2, n + 1):
        if n % divisor == 0:
            return divisor


# 16)
def contar_vocales(palabra):
    """Contá las vocales de la palabra."""
    cantidad = 0
    # Un string se puede recorrer letra por letra con un for.
    for letra in palabra:
        # 'in' chequea si la letra está dentro del texto de vocales.
        if letra in "aeiou":
            cantidad = cantidad + 1
    return cantidad


# 17)
def mayor_de_tres(a, b, c):
    """Devolvé el mayor de tres números."""
    # Empezamos asumiendo que a es el mayor y vamos comparando.
    mayor = a
    if b > mayor:
        mayor = b
    if c > mayor:
        mayor = c
    return mayor


# 18)
def signo(numero):
    """Devolvé el signo del número."""
    if numero > 0:
        return "positivo"
    elif numero < 0:
        return "negativo"
    else:
        return "cero"


# 19)
def esta_en_equipo(equipo, nombre):
    """Buscá un nombre en la lista equipo."""
    # Recorremos la lista. Si encontramos el nombre, devolvemos True y cortamos.
    for pokemon in equipo:
        if pokemon == nombre:
            return True
    # Si terminamos el bucle sin encontrarlo, no está.
    return False


# 20)
def contar_debilitados(equipo_hp):
    """Contá cuántos HP son <= 0."""
    cantidad = 0
    for hp in equipo_hp:
        if hp <= 0:
            cantidad = cantidad + 1
    return cantidad
