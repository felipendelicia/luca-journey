"""⚡ Ejercicios — Descargador async

Juntás todo: preparás un montón de descargas, las procesás por lotes (para no saturar)
y reportás. ✅ Corregí cuando termines.
"""


# Preparar las descargas
# Dada una lista de URLs, devolvé una lista de dicts {"url": u, "ok": False} (todavía
# ninguna está hecha).
# Ejemplo:  preparar(["a", "b"])  →  [{"url": "a", "ok": False}, {"url": "b", "ok": False}]
def preparar(urls):
    """Devolvé la lista de descargas pendientes."""


# Procesar en lotes
# Partí `items` en lotes de hasta `tam` (para respetar el límite de concurrencia).
# Ejemplo:  en_lotes([1, 2, 3], 2)  →  [[1, 2], [3]]
def en_lotes(items, tam):
    """Devolvé lotes de hasta tam elementos."""


# Marcar como hechas
# Recorré las descargas y poné "ok" en True en todas. Devolvé la lista.
# Ejemplo:  marcar_ok([{"url": "a", "ok": False}])  →  [{"url": "a", "ok": True}]
def marcar_ok(items):
    """Poné ok=True en cada item y devolvé la lista."""


# Resumen final
# Devolvé un texto con el formato EXACTO:
#   "<total> descargas, <hechas> ok."
# donde hechas = cuántas tienen "ok" en True.
# Ejemplo:  resumen([{"ok": True}, {"ok": False}])  →  "2 descargas, 1 ok."
def resumen(items):
    """Devolvé el resumen de descargas."""


# Cantidad
# Devolvé cuántas URLs hay en la lista.
def cantidad(urls):
    """Devolvé cuántas URLs hay."""
    # TU CÓDIGO ACÁ


# Quitar duplicadas
# Devolvé las URLs sin repetir, en orden de aparición.
def quitar_duplicados(urls):
    """Devolvé las URLs sin repetir."""
    # TU CÓDIGO ACÁ


# Solo HTTPS
# Devolvé solo las URLs que empiezan con "https://".
def solo_https(urls):
    """Devolvé las URLs https."""
    # TU CÓDIGO ACÁ


# Agregar protocolo
# Si la URL no empieza con "http://" ni "https://", agregale "https://" adelante. Si ya tiene,
# dejala igual.  Ejemplo:  agregar_protocolo("pokeapi.co")  →  "https://pokeapi.co"
def agregar_protocolo(url):
    """Asegurá que la URL tenga protocolo."""
    # TU CÓDIGO ACÁ


# Contar OK
# `items` es una lista de dicts {"url": ..., "ok": True/False}. Devolvé cuántos tienen ok=True.
def contar_ok(items):
    """Devolvé cuántos items están ok."""
    # TU CÓDIGO ACÁ


# Contar fallidos
# Devolvé cuántos items tienen ok=False.
def contar_fallidos(items):
    """Devolvé cuántos items fallaron."""
    # TU CÓDIGO ACÁ


# URLs que fallaron
# Devolvé las "url" de los items con ok=False.
def urls_fallidas(items):
    """Devolvé las urls de los items fallidos."""
    # TU CÓDIGO ACÁ


# Tasa de éxito
# Devolvé la fracción de items ok (cantidad ok / total).
def tasa_exito(items):
    """Devolvé la fracción de items ok."""
    # TU CÓDIGO ACÁ


# ¿Todos OK?
# Devolvé True si TODOS los items tienen ok=True.
def todos_ok(items):
    """Devolvé True si todos están ok."""
    # TU CÓDIGO ACÁ


# Primer fallo
# Devolvé el primer item (dict) con ok=False, o None si no hay ninguno.
def primer_fallo(items):
    """Devolvé el primer item fallido, o None."""
    # TU CÓDIGO ACÁ


# Marcar todos OK
# Poné ok=True en todos los items y devolvelos.
def marcar_todos_ok(items):
    """Poné ok=True en todos."""
    # TU CÓDIGO ACÁ


# Resumen del estado
# Devolvé un dict {"ok": cantidad_ok, "error": cantidad_fallidos}.
def resumen_estado(items):
    """Devolvé {"ok": n, "error": m}."""
    # TU CÓDIGO ACÁ


# Marcar error por URL
# Poné ok=False en el item cuya "url" sea `url`. Devolvé los items.
def marcar_error(items, url):
    """Marcá como fallido el item con esa url."""
    # TU CÓDIGO ACÁ


# Ordenar por URL
# Devolvé los items ordenados alfabéticamente por su "url".
def ordenar_por_url(items):
    """Devolvé los items ordenados por url."""
    # TU CÓDIGO ACÁ


# Agregar si es nueva
# Agregá `url` a la lista solo si no estaba. Devolvé la lista.
def agregar_si_nueva(urls, url):
    """Agregá url si no estaba."""
    # TU CÓDIGO ACÁ


# Con índice
# Devolvé una lista de tuplas (índice, url).
# Ejemplo:  con_indice(["a", "b"])  →  [(0, "a"), (1, "b")]
def con_indice(urls):
    """Devolvé pares (índice, url)."""
    # TU CÓDIGO ACÁ
