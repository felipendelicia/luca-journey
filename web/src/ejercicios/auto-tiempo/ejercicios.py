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
