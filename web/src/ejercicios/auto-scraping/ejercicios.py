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


# Extraer emails
# Devolvé una lista con los emails que aparezcan en el texto (algo con forma usuario@dominio).
# Ejemplo:  extraer_emails("escribi a ash@kanto.com")  →  ["ash@kanto.com"]
def extraer_emails(texto):
    """Devolvé los emails del texto."""
    # TU CÓDIGO ACÁ


# Extraer precios
# Devolvé los números que vienen después de un "$", como enteros.
# Ejemplo:  extraer_precios("Poción $200, Revivir $1500")  →  [200, 1500]
def extraer_precios(texto):
    """Devolvé los precios (números tras $) como int."""
    # TU CÓDIGO ACÁ


# Contar etiquetas
# Devolvé cuántas etiquetas de apertura `<etiqueta ...>` hay en el HTML.
# Ejemplo:  contar_etiquetas("<li>a</li><li>b</li>", "li")  →  2
def contar_etiquetas(html, etiqueta):
    """Devolvé cuántas etiquetas de apertura hay."""
    # TU CÓDIGO ACÁ


# Primer enlace
# Devolvé la URL del primer href="...", o None si no hay.
def primer_enlace(html):
    """Devolvé el primer href, o None."""
    # TU CÓDIGO ACÁ


# ¿Tiene esa etiqueta?
# Devolvé True si el HTML tiene al menos una etiqueta `<etiqueta ...>`.
def tiene_etiqueta(html, etiqueta):
    """Devolvé True si aparece esa etiqueta."""
    # TU CÓDIGO ACÁ


# Contar enlaces
# Devolvé cuántos href="..." hay en el HTML.
def contar_enlaces(html):
    """Devolvé cuántos enlaces hay."""
    # TU CÓDIGO ACÁ


# Extraer hashtags
# Devolvé las palabras que vienen después de un "#" (sin el #).
# Ejemplo:  extraer_hashtags("hoy #kanto y #pokemon")  →  ["kanto", "pokemon"]
def extraer_hashtags(texto):
    """Devolvé los hashtags (sin el #)."""
    # TU CÓDIGO ACÁ


# Palabras en mayúscula
# Devolvé las palabras que están TODAS en mayúsculas.
# Ejemplo:  extraer_mayusculas("el TEAM ROCKET ataca")  →  ["TEAM", "ROCKET"]
def extraer_mayusculas(texto):
    """Devolvé las palabras todas en mayúsculas."""
    # TU CÓDIGO ACÁ


# Contar palabras
# Devolvé cuántas palabras hay (separadas por espacios).
def contar_palabras(texto):
    """Devolvé la cantidad de palabras."""
    # TU CÓDIGO ACÁ


# Extraer entre marcadores
# Devolvé los textos que están entre `inicio` y `fin` (puede haber varios).
# Ejemplo:  extraer_entre("[a] y [b]", "[", "]")  →  ["a", "b"]
def extraer_entre(texto, inicio, fin):
    """Devolvé los textos entre inicio y fin."""
    # TU CÓDIGO ACÁ


# Primer número
# Devolvé el primer número entero del texto, o None si no hay.
def primer_numero(texto):
    """Devolvé el primer entero, o None."""
    # TU CÓDIGO ACÁ


# Suma de números
# Devolvé la suma de todos los enteros que aparezcan en el texto.
# Ejemplo:  suma_numeros("3 pokemon y 2 pociones")  →  5
def suma_numeros(texto):
    """Devolvé la suma de los números del texto."""
    # TU CÓDIGO ACÁ


# Quitar espacios extra
# Devolvé el texto con cada secuencia de espacios convertida en uno solo, y sin espacios al borde.
# Ejemplo:  quitar_espacios_extra("  hola   mundo  ")  →  "hola mundo"
def quitar_espacios_extra(texto):
    """Devolvé el texto con espacios normalizados."""
    # TU CÓDIGO ACÁ


# Solo letras
# Devolvé el texto dejando únicamente las letras (sin números, espacios ni símbolos).
# Ejemplo:  solo_letras("Pika-2!")  →  "Pika"
def solo_letras(texto):
    """Devolvé solo las letras del texto."""
    # TU CÓDIGO ACÁ


# Último enlace
# Devolvé la URL del último href="...", o None si no hay.
def ultimo_enlace(html):
    """Devolvé el último href, o None."""
    # TU CÓDIGO ACÁ


# Reemplazar texto
# Devolvé el texto con cada aparición de `viejo` cambiada por `nuevo`.
def reemplazar_texto(texto, viejo, nuevo):
    """Devolvé el texto con viejo cambiado por nuevo."""
    # TU CÓDIGO ACÁ
