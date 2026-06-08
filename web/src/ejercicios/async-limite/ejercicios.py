"""🚦 Ejercicios — Límite de concurrencia

Lanzar 10.000 descargas a la vez tira todo abajo. Por eso se LIMITA cuántas corren
juntas (un "semáforo"): se procesan de a lotes. Acá manejás ese límite.
✅ Corregí cuando termines.
"""
import math


# Partir en lotes
# Partí `items` en lotes de hasta `tam` elementos cada uno (en orden).
# Ejemplo:  por_lotes([1, 2, 3, 4, 5], 2)  →  [[1, 2], [3, 4], [5]]
def por_lotes(items, tam):
    """Devolvé lotes de hasta tam elementos."""


# ¿Cuántos lotes?
# Devolvé cuántos lotes de tamaño `tam` hacen falta para `total` items (techo).
# Ejemplo:  cantidad_lotes(5, 2)  →  3
def cantidad_lotes(total, tam):
    """Devolvé el techo de total / tam."""


# ¿Cabe uno más?
# Devolvé True si todavía se puede lanzar otra tarea sin pasar el `maximo` de concurrentes.
# Ejemplo:  cabe(2, 3)  →  True   ·   cabe(3, 3)  →  False
def cabe(activos, maximo):
    """Devolvé True si activos es menor que maximo."""


# Limitar la tanda
# Devolvé como mucho los primeros `maximo` pedidos de la lista.
# Ejemplo:  limitar([1, 2, 3, 4], 2)  →  [1, 2]
def limitar(pedidos, maximo):
    """Devolvé los primeros maximo pedidos."""


# Lugares libres
# `activos` son las tareas corriendo ahora. Devolvé cuántos lugares quedan, dado un `maximo`.
# Ejemplo:  lugares_libres(["a"], 3)  →  2
def lugares_libres(activos, maximo):
    """Devolvé maximo - cantidad de activos."""
    # TU CÓDIGO ACÁ


# ¿Al límite?
# Devolvé True si la cantidad de activos llegó (o superó) el máximo.
def esta_al_limite(activos, maximo):
    """Devolvé True si se alcanzó el máximo."""
    # TU CÓDIGO ACÁ


# ¿Hay lugar?
# Devolvé True si todavía cabe una tarea más (activos < maximo).
def hay_lugar(activos, maximo):
    """Devolvé True si cabe una más."""
    # TU CÓDIGO ACÁ


# Agregar si cabe
# Agregá `item` a activos SOLO si no se alcanzó el máximo. Devolvé activos.
def agregar_si_cabe(activos, item, maximo):
    """Agregá item solo si hay lugar."""
    # TU CÓDIGO ACÁ


# Liberar
# Sacá la primera aparición de `item` de activos y devolvelo.
def liberar(activos, item):
    """Sacá item de activos."""
    # TU CÓDIGO ACÁ


# Tomar hasta el máximo
# Devolvé los primeros `maximo` pendientes (o menos).
# Ejemplo:  tomar_hasta(["a", "b", "c"], 2)  →  ["a", "b"]
def tomar_hasta(pendientes, maximo):
    """Devolvé los primeros maximo pendientes."""
    # TU CÓDIGO ACÁ


# El resto
# Devolvé los pendientes que quedan DESPUÉS de los primeros `maximo`.
# Ejemplo:  resto_despues_de(["a", "b", "c"], 2)  →  ["c"]
def resto_despues_de(pendientes, maximo):
    """Devolvé los pendientes después de maximo."""
    # TU CÓDIGO ACÁ


# Tamaño del último lote
# Si partís `total` items en lotes de `tam`, devolvé cuántos items tiene el ÚLTIMO lote.
# Ejemplo:  cantidad_ultimo_lote(10, 3)  →  1   ·   cantidad_ultimo_lote(9, 3)  →  3
def cantidad_ultimo_lote(total, tam):
    """Devolvé el tamaño del último lote."""
    # TU CÓDIGO ACÁ


# Procesar en lotes
# Aplicá `func` a cada item (procesando de a lotes de `tam`) y devolvé la lista de resultados.
# Ejemplo:  procesar_en_lotes([1, 2, 3], 2, lambda x: x*10)  →  [10, 20, 30]
def procesar_en_lotes(items, tam, func):
    """Devolvé func aplicada a cada item, en lotes."""
    # TU CÓDIGO ACÁ


# Rondas necesarias
# Devolvé cuántas rondas hacen falta para procesar `total` tareas de a `maximo` por vez.
# Ejemplo:  rondas_necesarias(10, 3)  →  4
def rondas_necesarias(total, maximo):
    """Devolvé cuántas rondas de maximo se necesitan."""
    # TU CÓDIGO ACÁ


# ¿Entra todo de una?
# Devolvé True si `total` tareas entran en una sola ronda (total <= maximo).
def cabe_todo(total, maximo):
    """Devolvé True si total entra en una ronda."""
    # TU CÓDIGO ACÁ


# Ocupación
# Devolvé qué fracción del máximo está ocupada (activos / maximo).
# Ejemplo:  ocupacion(["a", "b"], 4)  →  0.5
def ocupacion(activos, maximo):
    """Devolvé la fracción ocupada."""
    # TU CÓDIGO ACÁ


# Limitar la lista
# Devolvé como mucho los primeros `maximo` items.
def limitar_lista(items, maximo):
    """Devolvé los primeros maximo items."""
    # TU CÓDIGO ACÁ


# Los que sobran
# Devolvé los items que pasan del `maximo` (los que no entran).
def sobran(items, maximo):
    """Devolvé los items que pasan del máximo."""
    # TU CÓDIGO ACÁ


# ¿Puedo agregar n?
# Devolvé True si agregar `n` tareas a `activos` no pasa el `maximo`.
def puede_agregar_n(activos, n, maximo):
    """Devolvé True si len(activos) + n <= maximo."""
    # TU CÓDIGO ACÁ


# Cuántos esperan
# Si hay `total` tareas y el máximo en simultáneo es `maximo`, devolvé cuántas tienen que esperar.
# Ejemplo:  cuantos_esperan(10, 3)  →  7
def cuantos_esperan(total, maximo):
    """Devolvé cuántas tareas esperan (nunca negativo)."""
    # TU CÓDIGO ACÁ
