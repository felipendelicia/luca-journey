"""⚡ Soluciones — Descargador async"""


def preparar(urls):
    return [{"url": u, "ok": False} for u in urls]


def en_lotes(items, tam):
    return [items[i:i + tam] for i in range(0, len(items), tam)]


def marcar_ok(items):
    for it in items:
        it["ok"] = True
    return items


def resumen(items):
    hechas = sum(1 for it in items if it["ok"])
    return f"{len(items)} descargas, {hechas} ok."
