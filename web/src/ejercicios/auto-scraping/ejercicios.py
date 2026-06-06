"""🕸️ Ejercicios — Scraping: extraer datos

Scraping = bajar una página y SACARLE los datos. Bajar la página necesita internet
(eso se hace con requests, afuera del navegador); lo que practicás acá es la parte
testeable: EXTRAER datos de un texto/HTML con expresiones regulares. ✅ Corregí al terminar.
"""
import re


# Extraer números
# Devolvé una lista con TODOS los números enteros que aparezcan en el texto, como int.
# Ejemplo:  extraer_numeros("Pikachu nivel 30, HP 100")  →  [30, 100]
def extraer_numeros(texto):
    """Devolvé los enteros del texto, como lista de int."""


# Extraer enlaces
# De un HTML, devolvé la lista de URLs que están en los href="...".
# Ejemplo:  extraer_enlaces('<a href="/kanto">K</a><a href="/johto">J</a>')
#               →  ["/kanto", "/johto"]
def extraer_enlaces(html):
    """Devolvé las URLs de los href del HTML."""


# Contenido entre etiquetas
# Devolvé la lista de textos que están entre <etiqueta>...</etiqueta>.
# Ejemplo:  entre_etiqueta("<li>Bulbasaur</li><li>Charmander</li>", "li")
#               →  ["Bulbasaur", "Charmander"]
def entre_etiqueta(html, etiqueta):
    """Devolvé el contenido entre <etiqueta>…</etiqueta>."""


# Sacar las etiquetas
# Devolvé el texto sin ninguna etiqueta HTML (<...>), y sin espacios al borde.
# Ejemplo:  sin_etiquetas("<b>Hola</b> mundo")  →  "Hola mundo"
def sin_etiquetas(html):
    """Devolvé el texto sin etiquetas HTML."""
