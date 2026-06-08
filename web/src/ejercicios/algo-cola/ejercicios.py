"""🚶 Ejercicios — Cola (queue)

Una cola es FIFO: el primero que llega es el primero que se atiende (como la fila del
Centro Pokémon). Se usa para turnos y para recorrer "a lo ancho" (BFS).
✅ Corregí cuando termines.
"""


# Encolar
# Agregá `x` al FINAL de la fila (una lista) y devolvé la cola.
# Ejemplo:  encolar([1, 2], 3)  →  [1, 2, 3]
def encolar(cola, x):
    """Agregá x al final y devolvé la cola."""


# Atender (FIFO)
# Sacá y devolvé el PRIMERO de la fila (el que llegó antes). Si está vacía, devolvé None.
# Ejemplo:  atender([1, 2, 3])  →  1  (la cola queda [2, 3])
def atender(cola):
    """Sacá y devolvé el primero, o None si está vacía."""


# Cuántos esperan
# Devolvé cuántos hay en la fila.
# Ejemplo:  en_espera([1, 2, 3])  →  3
def en_espera(cola):
    """Devolvé la cantidad en la cola."""


# Orden de atención
# Devolvé una lista con los elementos en el orden en que se van a atender (sin modificar
# la cola). Ejemplo:  orden_de_atencion([1, 2, 3])  →  [1, 2, 3]
def orden_de_atencion(cola):
    """Devolvé los elementos en orden FIFO (lista nueva)."""


# ¿Cola vacía?
# Devolvé True si la cola no tiene a nadie.  Ejemplo:  esta_vacia([])  →  True
def esta_vacia(cola):
    """Devolvé True si la cola está vacía."""
    # TU CÓDIGO ACÁ


# Tamaño
# Devolvé cuántos están esperando.  Ejemplo:  tamano(["A", "B"])  →  2
def tamano(cola):
    """Devolvé la cantidad en la cola."""
    # TU CÓDIGO ACÁ


# El próximo
# Devolvé al PRÓXIMO en ser atendido (el de adelante) SIN sacarlo. Si está vacía, None.
# Ejemplo:  proximo(["Ash", "Misty"])  →  "Ash"   ·   proximo([])  →  None
def proximo(cola):
    """Devolvé el de adelante, o None."""
    # TU CÓDIGO ACÁ


# Encolar varios
# Agregá todos los `elementos` al final de la cola, en orden, y devolvé la cola.
# Ejemplo:  encolar_varios(["A"], ["B", "C"])  →  ["A", "B", "C"]
def encolar_varios(cola, elementos):
    """Encolá todos los elementos y devolvé la cola."""
    # TU CÓDIGO ACÁ


# Atender a todos
# Atendé a todos en orden (FIFO) y devolvé la lista en el orden en que fueron atendidos.
# Ejemplo:  atender_a_todos(["A", "B", "C"])  →  ["A", "B", "C"]
def atender_a_todos(cola):
    """Devolvé a todos en el orden de atención."""
    # TU CÓDIGO ACÁ


# Atender a N
# Atendé a los primeros `n` (o menos si no alcanzan) y devolvé a quiénes atendiste.
# Ejemplo:  atender_n(["A", "B", "C"], 2)  →  ["A", "B"]
def atender_n(cola, n):
    """Devolvé los primeros n atendidos."""
    # TU CÓDIGO ACÁ


# Simular una cola
# `operaciones`: "enqueue N" agrega N al final, "dequeue" atiende al de adelante (si hay).
# Devolvé la cola final.  Ejemplo:  simular_cola(["enqueue 1", "enqueue 2", "dequeue"])  →  [2]
def simular_cola(operaciones):
    """Aplicá las operaciones y devolvé la cola final."""
    # TU CÓDIGO ACÁ


# El juego de la papa caliente (Josephus)
# Todos en ronda. Se cuenta de a `k`: el que queda en `k` sale. Se repite hasta que queda
# UNO. Devolvé el nombre del que sobrevive. (Pensalo moviendo al frente al final, k-1 veces,
# y sacando al k-ésimo.)
# Ejemplo:  josephus(["A", "B", "C", "D"], 2)  →  "A"
def josephus(nombres, k):
    """Devolvé el sobreviviente del juego de la papa caliente."""
    # TU CÓDIGO ACÁ


# Invertir la cola
# Devolvé una cola NUEVA con el orden invertido (ayudate con una pila).
# Ejemplo:  invertir_cola(["A", "B", "C"])  →  ["C", "B", "A"]
def invertir_cola(cola):
    """Devolvé la cola invertida."""
    # TU CÓDIGO ACÁ


# Intercalar dos colas
# Devolvé una cola que alterne: primero de `a`, primero de `b`, segundo de `a`, … hasta
# agotar ambas.  Ejemplo:  intercalar(["A", "C"], ["B", "D", "E"])  →  ["A", "B", "C", "D", "E"]
def intercalar(a, b):
    """Devolvé las dos colas intercaladas."""
    # TU CÓDIGO ACÁ


# Posición en la fila
# Devolvé en qué puesto está `x` (el primero es 1). Si no está, devolvé -1.
# Ejemplo:  posicion_en_fila(["A", "B", "C"], "C")  →  3
def posicion_en_fila(cola, x):
    """Devolvé el puesto de x (desde 1), o -1."""
    # TU CÓDIGO ACÁ


# Mover al final
# Mové la primera aparición de `x` al final de la cola y devolvé la cola.
# Ejemplo:  mover_al_final(["A", "B", "C"], "A")  →  ["B", "C", "A"]
def mover_al_final(cola, x):
    """Mové x al final de la cola."""
    # TU CÓDIGO ACÁ


# ¿Está en la cola?
# Devolvé True si `x` está esperando.  Ejemplo:  hay_en_cola(["A", "B"], "B")  →  True
def hay_en_cola(cola, x):
    """Devolvé True si x está en la cola."""
    # TU CÓDIGO ACÁ


# Duplicar cada uno
# Devolvé una cola donde cada elemento aparece dos veces seguidas.
# Ejemplo:  duplicar_cada(["A", "B"])  →  ["A", "A", "B", "B"]
def duplicar_cada(cola):
    """Devolvé cada elemento repetido dos veces."""
    # TU CÓDIGO ACÁ


# Atender hasta encontrar
# Atendé desde adelante hasta encontrar a `x` (incluido). Devolvé a quiénes atendiste.
# Ejemplo:  atender_hasta(["A", "B", "C"], "B")  →  ["A", "B"]
def atender_hasta(cola, x):
    """Devolvé los atendidos hasta x (inclusive)."""
    # TU CÓDIGO ACÁ


# Rotar la cola
# Mové los primeros `n` al final, conservando el orden. Devolvé la cola.
# Ejemplo:  rotar(["A", "B", "C", "D"], 2)  →  ["C", "D", "A", "B"]
def rotar(cola, n):
    """Mové los primeros n al final."""
    # TU CÓDIGO ACÁ
