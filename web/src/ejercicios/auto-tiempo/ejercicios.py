"""⏰ Ejercicios — Fechas, esperas y agendado

Las automatizaciones viven del tiempo: "corré esto cada 6 horas", "solo días de
semana". El módulo datetime maneja fechas y diferencias. ✅ Corregí cuando termines.
"""
from datetime import date, datetime, timedelta


# Días entre dos fechas
# Recibís dos objetos date. Devolvé cuántos días hay de `d1` a `d2` (un entero).
# Ejemplo:  dias_entre(date(2024, 1, 1), date(2024, 1, 8))  →  7
def dias_entre(d1, d2):
    """Devolvé (d2 - d1) en días, como entero."""


# Formatear una fecha
# Recibís un date (o datetime) y devolvés el texto "AAAA-MM-DD".
# Ejemplo:  formatear(date(2024, 3, 9))  →  "2024-03-09"
def formatear(dt):
    """Devolvé la fecha como 'AAAA-MM-DD'."""


# ¿Es fin de semana?
# Recibís un date. Devolvé True si cae sábado o domingo. (weekday(): lunes=0 … domingo=6.)
# Ejemplo:  es_fin_de_semana(date(2024, 3, 9))  →  True  (es sábado)
def es_fin_de_semana(d):
    """Devolvé True si d es sábado o domingo."""


# ¿Toca correr la tarea?
# Recibís dos datetime (`ultima` corrida y `ahora`) y un número `cada_horas`. Devolvé
# True si pasaron AL MENOS `cada_horas` horas desde la última corrida.
# Ejemplo:  toca_correr(datetime(2024,1,1,0,0), datetime(2024,1,1,7,0), 6)  →  True
def toca_correr(ultima, ahora, cada_horas):
    """Devolvé True si pasaron cada_horas o más desde ultima."""


# Día de la semana
# Recibís un date. Devolvé el nombre del día en minúsculas: "lunes", …, "domingo".
# Ejemplo:  dia_de_semana(date(2024, 3, 9))  →  "sabado"
def dia_de_semana(d):
    """Devolvé el nombre del día."""
    # TU CÓDIGO ACÁ


# Sumar días
# Devolvé un date `n` días después de `d`.
# Ejemplo:  sumar_dias(date(2024, 1, 1), 7)  →  date(2024, 1, 8)
def sumar_dias(d, n):
    """Devolvé d más n días."""
    # TU CÓDIGO ACÁ


# Restar días
# Devolvé un date `n` días antes de `d`.
def restar_dias(d, n):
    """Devolvé d menos n días."""
    # TU CÓDIGO ACÁ


# ¿Está en el pasado?
# Devolvé True si `d` es anterior a `hoy`.
def es_pasado(d, hoy):
    """Devolvé True si d < hoy."""
    # TU CÓDIGO ACÁ


# Días hasta
# Devolvé cuántos días hay desde `d` hasta `objetivo` (entero, puede ser negativo).
def dias_hasta(d, objetivo):
    """Devolvé (objetivo - d) en días."""
    # TU CÓDIGO ACÁ


# ¿Mismo mes?
# Devolvé True si `a` y `b` son del mismo mes y año.
def mismo_mes(a, b):
    """Devolvé True si a y b son del mismo mes y año."""
    # TU CÓDIGO ACÁ


# Año
# Devolvé el año de `d`.
def anio_de(d):
    """Devolvé el año."""
    # TU CÓDIGO ACÁ


# Mes
# Devolvé el mes de `d` (1 a 12).
def mes_de(d):
    """Devolvé el mes."""
    # TU CÓDIGO ACÁ


# ¿Año bisiesto?
# Devolvé True si `anio` es bisiesto (divisible por 4, salvo fin de siglo no divisible por 400).
def es_bisiesto(anio):
    """Devolvé True si el año es bisiesto."""
    # TU CÓDIGO ACÁ


# La más reciente
# `fechas` es una lista de date. Devolvé la más reciente.
def mas_reciente(fechas):
    """Devolvé la fecha más reciente."""
    # TU CÓDIGO ACÁ


# La más antigua
# Devolvé la fecha más antigua.
def mas_antigua(fechas):
    """Devolvé la fecha más antigua."""
    # TU CÓDIGO ACÁ


# Ordenar fechas
# Devolvé las fechas ordenadas de la más antigua a la más reciente.
def ordenar_fechas(fechas):
    """Devolvé las fechas ordenadas."""
    # TU CÓDIGO ACÁ


# Cuántos fines de semana
# Devolvé cuántas de las fechas caen sábado o domingo.
def cuantos_fines_de_semana(fechas):
    """Devolvé cuántas fechas son fin de semana."""
    # TU CÓDIGO ACÁ


# Formatear hora
# Recibís un datetime. Devolvé la hora como "HH:MM".
# Ejemplo:  formatear_hora(datetime(2024, 1, 1, 14, 30))  →  "14:30"
def formatear_hora(dt):
    """Devolvé la hora como 'HH:MM'."""
    # TU CÓDIGO ACÁ


# Próximo lunes
# Devolvé el date del próximo lunes después de `d` (si `d` es lunes, el lunes siguiente).
def proximo_lunes(d):
    """Devolvé el próximo lunes después de d."""
    # TU CÓDIGO ACÁ


# Días laborales
# Devolvé cuántas de las fechas caen de lunes a viernes.
def cantidad_dias_laborales(fechas):
    """Devolvé cuántas fechas son días laborales."""
    # TU CÓDIGO ACÁ
