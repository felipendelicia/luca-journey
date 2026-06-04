"""
manual_lib.py — Herramientas y estilos para construir el libro (manual.html / manual.pdf).

Acá viven los "ladrillos" con los que se arma el libro: funciones que devuelven
HTML (párrafos, listas, cajas de aviso, tablas y bloques de código con resaltado)
y la hoja de estilos. El contenido en sí está en manual_contenido.py.

El código se resalta con Pygments para que se vea como en un libro de verdad.
"""

import html as _html
import textwrap

from pygments import highlight
from pygments.lexers import PythonLexer, BashLexer
from pygments.formatters import HtmlFormatter

# Formateador de Pygments: estilo claro y legible, clase CSS 'highlight'.
_FORMATTER = HtmlFormatter(style="friendly", cssclass="highlight")


def css_pygments():
    """Devuelve el CSS que pinta los tokens del código."""
    return _FORMATTER.get_style_defs(".highlight")


# ----------------------------------------------------------------------
#  Bloques de contenido (devuelven HTML)
# ----------------------------------------------------------------------
def code(src, lang="python"):
    """Bloque de código con resaltado de sintaxis."""
    src = textwrap.dedent(src).strip("\n")
    lexer = BashLexer() if lang == "bash" else PythonLexer()
    return '<div class="codeblock">' + highlight(src, lexer, _FORMATTER) + "</div>"


def inline(texto):
    """Código en línea, dentro de un párrafo: <code>...</code>."""
    return f"<code>{_html.escape(texto)}</code>"


def h2(texto, sid):
    return f'<h2 id="{sid}">{texto}</h2>'


def h3(texto):
    return f"<h3>{texto}</h3>"


def p(html_text):
    return f"<p>{html_text}</p>"


def ul(*items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def ol(*items):
    return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


_LABELS = {
    "nota": "NOTA",
    "tip": "TIP",
    "cuidado": "CUIDADO",
    "clave": "CONCEPTO CLAVE",
    "pokemon": "ANALOGÍA POKÉMON",
}


def caja(html_text, tipo="nota", titulo=None):
    """Caja de aviso destacada (nota, tip, cuidado, concepto clave, analogía)."""
    etiqueta = titulo or _LABELS.get(tipo, "NOTA")
    return (
        f'<div class="callout {tipo}">'
        f'<span class="et">{etiqueta}</span>{html_text}</div>'
    )


def tabla(headers, filas):
    """Tabla HTML a partir de encabezados y filas (listas de strings)."""
    th = "".join(f"<th>{h}</th>" for h in headers)
    cuerpo = ""
    for fila in filas:
        celdas = "".join(f"<td>{c}</td>" for c in fila)
        cuerpo += f"<tr>{celdas}</tr>"
    return f"<table><thead><tr>{th}</tr></thead><tbody>{cuerpo}</tbody></table>"


def capitulo(cid, titulo, *bloques):
    """Arma un capítulo: un <h1> con id + sus bloques de contenido."""
    cuerpo = "".join(bloques)
    return {
        "id": cid,
        "titulo": titulo,
        "html": f'<h1 id="{cid}" class="cap">{titulo}</h1>{cuerpo}',
    }


# ----------------------------------------------------------------------
#  Hoja de estilos del libro
# ----------------------------------------------------------------------
CSS = """
@page {
    size: A4;
    margin: 2cm 1.8cm 2cm 1.8cm;
    @bottom-center { content: counter(page); color: #9aa0a6; font-size: 9pt; }
    @top-right { content: "Python con Pokémon"; color: #c9ced4; font-size: 8.5pt; }
}
@page:first { margin: 0; @bottom-center { content: none; } @top-right { content: none; } }

* { box-sizing: border-box; }
body {
    font-family: 'DejaVu Sans', 'Liberation Sans', Arial, sans-serif;
    font-size: 10.5pt; color: #2d2d2d; line-height: 1.6; margin: 0;
}

/* Portada */
.portada {
    height: 100vh; background: linear-gradient(160deg, #b5121b 0%, #d62828 55%, #f25c54 100%);
    color: #fff; text-align: center; padding-top: 7cm;
    page-break-after: always;
}
.portada .pokeball {
    width: 120px; height: 120px; border-radius: 50%;
    border: 8px solid #2a2a2a; margin: 0 auto 1.2cm;
    background: linear-gradient(to bottom, #ee1515 50%, #ffffff 50%);
}
.portada h1 { font-size: 34pt; margin: .2cm 0; border: none; color: #fff; }
.portada .sub { font-size: 14pt; opacity: .95; }
.portada .pie { margin-top: 3cm; font-size: 10pt; opacity: .85; }

/* Títulos */
h1.cap {
    font-size: 21pt; color: #0b5fa5; border-bottom: 3px solid #0b5fa5;
    padding-bottom: .15em; margin: 0 0 .6em; page-break-before: always;
}
h2 { font-size: 14.5pt; color: #11497e; margin: 1.4em 0 .4em;
     border-left: 5px solid #ffcb05; padding-left: .4em; }
h3 { font-size: 11.8pt; color: #333; margin: 1em 0 .3em; }
p { margin: .55em 0; text-align: justify; }
ul, ol { margin: .5em 0 .5em 0; padding-left: 1.4em; }
li { margin: .25em 0; }
strong { color: #11497e; }

/* Código en línea */
p code, li code, td code {
    background: #eef1f4; color: #b5004a; padding: .05em .35em;
    border-radius: 3px; font-family: 'DejaVu Sans Mono', monospace; font-size: .88em;
}

/* Bloques de código */
.codeblock { margin: .8em 0; page-break-inside: avoid; }
.highlight {
    background: #f6f8fa; border: 1px solid #e1e4e8; border-left: 4px solid #0b5fa5;
    border-radius: 6px; padding: 9px 12px; overflow-x: auto;
}
.highlight pre {
    margin: 0; font-family: 'DejaVu Sans Mono', monospace; font-size: 9pt;
    line-height: 1.45; white-space: pre-wrap; word-wrap: break-word;
}

/* Cajas de aviso */
.callout {
    border-radius: 7px; padding: 9px 13px 9px 13px; margin: .9em 0;
    border-left: 5px solid #888; page-break-inside: avoid; font-size: 10pt;
}
.callout .et {
    display: inline-block; font-weight: bold; font-size: 8pt; letter-spacing: .04em;
    margin-right: .5em; padding: 1px 7px; border-radius: 10px; color: #fff;
    vertical-align: middle;
}
.nota { background: #eaf3fb; border-color: #2b78c4; }
.nota .et { background: #2b78c4; }
.tip { background: #eafaf0; border-color: #28a745; }
.tip .et { background: #28a745; }
.cuidado { background: #fff7e6; border-color: #e0a800; }
.cuidado .et { background: #d39e00; }
.clave { background: #f3eefb; border-color: #7d4bd1; }
.clave .et { background: #7d4bd1; }
.pokemon { background: #fdeef3; border-color: #e3508a; }
.pokemon .et { background: #e3508a; }

/* Tablas */
table { border-collapse: collapse; width: 100%; margin: .9em 0; page-break-inside: avoid; }
th, td { border: 1px solid #d0d7de; padding: 5px 9px; font-size: 9.5pt; text-align: left; }
th { background: #0b5fa5; color: #fff; }
tbody tr:nth-child(even) { background: #f6f8fa; }

/* Índice (TOC) */
.toc { page-break-after: always; }
.toc h1 { color: #0b5fa5; border-bottom: 3px solid #0b5fa5; font-size: 21pt;
          page-break-before: avoid; }
.toc ul { list-style: none; padding-left: 0; }
.toc > ul > li { margin: .35em 0; font-weight: bold; color: #11497e; }
.toc ul ul { padding-left: 1.3em; }
.toc ul ul li { font-weight: normal; color: #444; }
.toc a { color: inherit; text-decoration: none; }

/* Saludo / cierre */
.cierre { text-align: center; color: #777; margin-top: 2cm; font-style: italic; }
"""
