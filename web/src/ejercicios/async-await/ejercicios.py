"""⏳ Ejercicios — await: dónde esperar

`await` se pone delante de las operaciones que ESPERAN (bajar algo, leer una API):
mientras esperan, el programa hace otra cosa. Acá decidís qué pasos lo necesitan.
Modelamos cada paso como un dict {"nombre", "espera": bool}. ✅ Corregí cuando termines.
"""


# ¿Este paso necesita await?
# Devolvé True si el paso es una operación que espera (su clave "espera" es True).
# Ejemplo:  necesita_await({"nombre": "bajar", "espera": True})  →  True
def necesita_await(paso):
    """Devolvé el valor de paso['espera']."""


# Pasos que llevan await
# `pasos` es una lista de esos dicts. Devolvé los NOMBRES de los que esperan.
# Ejemplo:  pasos_con_await([{"nombre":"bajar","espera":True},{"nombre":"sumar","espera":False}])
#               →  ["bajar"]
def pasos_con_await(pasos):
    """Devolvé los nombres de los pasos que esperan."""


# Agregar await a una línea
# Devolvé la línea con "await " adelante. Si YA empieza con "await ", devolvela igual.
# Ejemplo:  agregar_await("bajar(url)")        →  "await bajar(url)"
#           agregar_await("await bajar(url)")  →  "await bajar(url)"
def agregar_await(linea):
    """Devolvé la línea con 'await ' adelante (sin duplicar)."""


# Contar awaits
# Devolvé cuántas veces aparece "await " en un bloque de código (texto).
# Ejemplo:  contar_awaits("a = await f()\nb = await g()")  →  2
def contar_awaits(codigo):
    """Devolvé cuántos 'await ' hay en el código."""
