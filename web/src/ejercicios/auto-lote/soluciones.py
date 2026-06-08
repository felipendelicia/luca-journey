"""🔁 Soluciones — Procesar carpetas en lote"""
from pathlib import Path


def solo_extension(archivos, ext):
    return [a for a in archivos if a.endswith(ext)]


def contar_por_extension(archivos):
    conteo = {}
    for a in archivos:
        ext = Path(a).suffix
        conteo[ext] = conteo.get(ext, 0) + 1
    return conteo


def renombrar_lote(archivos, viejo, nuevo):
    return [a.replace(viejo, nuevo) for a in archivos]


def mas_grande(archivos):
    if not archivos:
        return None
    return max(archivos, key=lambda par: par[1])[0]


def solo_imagenes(archivos):
    return [a for a in archivos if Path(a).suffix in (".png", ".jpg", ".gif")]


def nombres_sin_extension(archivos):
    return [Path(a).stem for a in archivos]


def agregar_prefijo(archivos, prefijo):
    return [prefijo + a for a in archivos]


def tamano_total(archivos):
    return sum(t for _, t in archivos)


def mas_chico(archivos):
    if not archivos:
        return None
    return min(archivos, key=lambda x: x[1])[0]


def ordenar_por_tamano(archivos):
    return [n for n, _ in sorted(archivos, key=lambda x: x[1], reverse=True)]


def filtrar_mayores_a(archivos, minimo):
    return [n for n, t in archivos if t > minimo]


def extensiones_unicas(archivos):
    return sorted(set(Path(a).suffix for a in archivos))


def contar(archivos):
    return len(archivos)


def quitar_duplicados(archivos):
    vistos = set()
    out = []
    for a in archivos:
        if a not in vistos:
            vistos.add(a)
            out.append(a)
    return out


def tienen_extension(archivos, ext):
    return all(a.endswith(ext) for a in archivos)


def cambiar_todas_extensiones(archivos, ext):
    return [Path(a).stem + ext for a in archivos]


def promedio_tamano(archivos):
    return sum(t for _, t in archivos) / len(archivos)


def nombres_largos(archivos, n):
    return [a for a in archivos if len(a) > n]


def agrupar_por_extension(archivos):
    d = {}
    for a in archivos:
        d.setdefault(Path(a).suffix, []).append(a)
    return d


def hay_extension(archivos, ext):
    return any(a.endswith(ext) for a in archivos)
