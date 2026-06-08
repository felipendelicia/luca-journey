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


def cantidad(urls):
    return len(urls)


def quitar_duplicados(urls):
    vistos = set()
    out = []
    for u in urls:
        if u not in vistos:
            vistos.add(u)
            out.append(u)
    return out


def solo_https(urls):
    return [u for u in urls if u.startswith("https://")]


def agregar_protocolo(url):
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return "https://" + url


def contar_ok(items):
    return sum(1 for it in items if it["ok"])


def contar_fallidos(items):
    return sum(1 for it in items if not it["ok"])


def urls_fallidas(items):
    return [it["url"] for it in items if not it["ok"]]


def tasa_exito(items):
    return contar_ok(items) / len(items)


def todos_ok(items):
    return all(it["ok"] for it in items)


def primer_fallo(items):
    for it in items:
        if not it["ok"]:
            return it
    return None


def marcar_todos_ok(items):
    for it in items:
        it["ok"] = True
    return items


def resumen_estado(items):
    return {"ok": contar_ok(items), "error": contar_fallidos(items)}


def marcar_error(items, url):
    for it in items:
        if it["url"] == url:
            it["ok"] = False
    return items


def ordenar_por_url(items):
    return sorted(items, key=lambda it: it["url"])


def agregar_si_nueva(urls, url):
    if url not in urls:
        urls.append(url)
    return urls


def con_indice(urls):
    return [(i, u) for i, u in enumerate(urls)]
