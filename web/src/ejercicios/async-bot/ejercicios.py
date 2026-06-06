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
