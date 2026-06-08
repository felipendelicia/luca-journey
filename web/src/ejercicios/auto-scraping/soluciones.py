"""🕸️ Soluciones — Scraping: extraer datos"""
import re


def extraer_numeros(texto):
    return [int(x) for x in re.findall(r"\d+", texto)]


def extraer_enlaces(html):
    return re.findall(r'href="([^"]+)"', html)


def entre_etiqueta(html, etiqueta):
    return re.findall(rf"<{etiqueta}>(.*?)</{etiqueta}>", html)


def sin_etiquetas(html):
    return re.sub(r"<[^>]+>", "", html).strip()


def extraer_emails(texto):
    return re.findall(r"[\w.]+@[\w.]+", texto)


def extraer_precios(texto):
    return [int(x) for x in re.findall(r"\$(\d+)", texto)]


def contar_etiquetas(html, etiqueta):
    return len(re.findall(r"<" + etiqueta + r"[ >]", html))


def primer_enlace(html):
    m = re.search(r'href="([^"]*)"', html)
    return m.group(1) if m else None


def tiene_etiqueta(html, etiqueta):
    return bool(re.search(r"<" + etiqueta + r"[ >]", html))


def contar_enlaces(html):
    return len(re.findall(r'href="[^"]*"', html))


def extraer_hashtags(texto):
    return re.findall(r"#(\w+)", texto)


def extraer_mayusculas(texto):
    return [p for p in texto.split() if p.isupper()]


def contar_palabras(texto):
    return len(texto.split())


def extraer_entre(texto, inicio, fin):
    out = []
    i = 0
    while True:
        a = texto.find(inicio, i)
        if a < 0:
            break
        a += len(inicio)
        b = texto.find(fin, a)
        if b < 0:
            break
        out.append(texto[a:b])
        i = b + len(fin)
    return out


def primer_numero(texto):
    m = re.search(r"\d+", texto)
    return int(m.group()) if m else None


def suma_numeros(texto):
    return sum(int(x) for x in re.findall(r"\d+", texto))


def quitar_espacios_extra(texto):
    return re.sub(r"\s+", " ", texto).strip()


def solo_letras(texto):
    return re.sub(r"[^a-zA-Z]", "", texto)


def ultimo_enlace(html):
    enlaces = re.findall(r'href="([^"]*)"', html)
    return enlaces[-1] if enlaces else None


def reemplazar_texto(texto, viejo, nuevo):
    return texto.replace(viejo, nuevo)
