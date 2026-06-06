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
