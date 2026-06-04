#!/usr/bin/env python3
"""
generar_manual.py — Genera 'manual.html' y 'manual.pdf' (el libro del curso).

El manual es un LIBRO de Python con estilo (no se hace con Markdown, se arma con
HTML). El contenido está en 'manual_contenido.py' y los estilos/herramientas en
'manual_lib.py'.

Uso:
    python generar_manual.py

Produce:
    manual.html  -> el libro, abrible en cualquier navegador
    manual.pdf   -> el libro en PDF (vía WeasyPrint; si falta, usa Chrome o LibreOffice)

Requisitos de mantenimiento (no los necesita el alumno, solo quien regenera):
    pip install weasyprint pygments
(WeasyPrint hace el PDF; Pygments resalta el código.)

IMPORTANTE: cuando cambie el proyecto, actualizá 'manual_contenido.py' y volvé a
correr este script. (Ver CLAUDE.md.)
"""

import os
import re
import shutil
import subprocess
import sys

import manual_lib
import manual_contenido

RAIZ = os.path.dirname(os.path.abspath(__file__))            # carpeta manual/
REPO = os.path.dirname(RAIZ)                                 # raíz del repo
SALIDA_HTML = os.path.join(RAIZ, "manual.html")
SALIDA_PDF = os.path.join(RAIZ, "manual.pdf")
# Copia del libro para publicarlo con GitHub Pages (sirve docs/index.html).
SALIDA_DOCS = os.path.join(REPO, "docs", "index.html")

# Los emojis quedan lindos en el navegador (manual.html), pero WeasyPrint no tiene
# fuente de emoji a color y los dibuja como cuadritos. Por eso, SOLO para el PDF
# generado con WeasyPrint, los sacamos. (No tocamos las flechas → para no romper código.)
_EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF"   # pictogramas (🐍 🏆 🔥 🐧 ...)
    "\U00002600-\U000027BF"   # símbolos varios (⚡ ✅ ❌ ❤ ...)
    "\U00002B00-\U00002BFF"   # flechas/figuras decorativas
    "\U0001F1E6-\U0001F1FF"   # banderas
    "\U0000FE0F\U0000200D\U00002122\U00002139]"  # selector, ZWJ, ™, ℹ
)


def _quitar_emoji(texto):
    return _EMOJI.sub("", texto)


def _sin_tags(texto):
    """Saca etiquetas HTML para usar el texto en el índice."""
    return re.sub(r"<[^>]+>", "", texto).strip()


def renumerar(capitulos):
    """
    Asigna los números de capítulo y de sección SEGÚN EL ORDEN de la lista.
    Así, para reordenar el libro, basta con reordenar CAPITULOS: los números
    (1, 2, 3... y 3.1, 3.2...) se recalculan solos y nunca se desincronizan.
    """
    for i, cap in enumerate(capitulos):
        nuevo = str(i)
        # 1) Número del capítulo (en el badge cap-num del encabezado).
        cap["html"] = cap["html"].replace(
            f'<span class="cap-num">{cap["num"]}</span>',
            f'<span class="cap-num">{nuevo}</span>', 1,
        )
        cap["num"] = nuevo
        cap["titulo"] = f"{nuevo}. {cap['resto']}"

        # 2) Número de cada sección h2 (la forma i.j).
        contador = {"n": 0}

        def _renum_h2(m, n=nuevo, c=contador):
            c["n"] += 1
            texto = re.sub(r"^\s*\d+\.\d+\.\s*", "", m.group(2))
            return f'{m.group(1)}{n}.{c["n"]}. {texto}{m.group(3)}'

        cap["html"] = re.sub(
            r'(<h2 id="[^"]+"[^>]*>)(.*?)(</h2>)', _renum_h2, cap["html"], flags=re.S
        )
    return capitulos


def construir_toc(capitulos):
    """Arma el índice (TOC) con enlaces a cada capítulo y sus secciones."""
    items = []
    for cap in capitulos:
        # Buscamos las secciones <h2 id="..."> dentro del capítulo.
        subs = re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', cap["html"], re.S)
        sub_html = ""
        if subs:
            lis = "".join(
                f'<li><a href="#{sid}">{_sin_tags(titulo)}</a></li>'
                for sid, titulo in subs
            )
            sub_html = f"<ul>{lis}</ul>"
        items.append(
            f'<li><a href="#{cap["id"]}">{_sin_tags(cap["titulo"])}</a>{sub_html}</li>'
        )
    return (
        '<section class="toc">'
        '<h2 class="toc-t">Índice</h2>'
        f"<ul>{''.join(items)}</ul>"
        "</section>"
    )


def construir_rail(capitulos):
    """El riel lateral de navegación (estilo aparato Pokédex). Solo se ve en pantalla."""
    enlaces = "".join(
        f'<a href="#{c["id"]}"><span class="rn">{c["num"] or "&bull;"}</span>'
        f'<span>{_sin_tags(c["resto"])}</span></a>'
        for c in capitulos
    )
    return (
        '<aside class="rail">'
        '<div class="device">'
        '<div class="lens"></div>'
        '<div class="leds"><i></i><i></i><i></i></div>'
        '<div class="dev-tt">Pokédex &middot; Codex</div>'
        "</div>"
        f"<nav>{enlaces}</nav>"
        "</aside>"
    )


def construir_portada():
    """La portada/hero del libro."""
    return (
        '<section class="portada">'
        '<div class="pokeball reveal d1"></div>'
        '<p class="kick reveal d2">El libro del curso</p>'
        '<h1 class="reveal d2">Python con Pokémon</h1>'
        '<p class="sub reveal d3">Aprendé a programar desde cero, paso a paso, '
        "con Linux, Python y mucha aventura.</p>"
        '<p class="sub reveal d4">Y convertite en Campeón de Kanto 🏆</p>'
        '<p class="pie reveal d5">Manual + libro de Python &middot; generar_manual.py</p>'
        "</section>"
    )


# Tipografías distintivas (se cargan en el navegador; en el PDF hay buenos respaldos).
FUENTES = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&"
    "family=Hanken+Grotesk:wght@400;500;600;700;800&"
    "family=JetBrains+Mono:wght@400;500;700&"
    "family=Silkscreen:wght@400;700&display=swap\">"
)


# JavaScript del libro (solo afecta al navegador; el PDF lo ignora):
# modo oscuro con memoria, botón "copiar" en cada bloque de código y buscador.
JS = """<script>
(function(){
  var body = document.body;
  if (localStorage.getItem('tema') === 'dark') body.classList.add('dark');

  var toggle = document.querySelector('.theme-toggle');
  if (toggle) {
    var refrescar = function(){ toggle.textContent = body.classList.contains('dark') ? '\\u2600\\uFE0F' : '\\uD83C\\uDF19'; };
    refrescar();
    toggle.addEventListener('click', function(){
      body.classList.toggle('dark');
      localStorage.setItem('tema', body.classList.contains('dark') ? 'dark' : 'claro');
      refrescar();
    });
  }

  document.querySelectorAll('figure.code').forEach(function(fig){
    var bar = fig.querySelector('.code-bar');
    var pre = fig.querySelector('pre');
    if (!bar || !pre) return;
    var btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.type = 'button';
    btn.textContent = 'copiar';
    btn.addEventListener('click', function(){
      navigator.clipboard.writeText(pre.innerText).then(function(){
        btn.textContent = 'copiado!';
        btn.classList.add('ok');
        setTimeout(function(){ btn.textContent = 'copiar'; btn.classList.remove('ok'); }, 1500);
      });
    });
    bar.appendChild(btn);
  });

  var search = document.querySelector('.search-box');
  if (search) {
    var heads = Array.prototype.slice.call(document.querySelectorAll('h1.cap, h2'));
    search.addEventListener('keydown', function(e){
      if (e.key !== 'Enter') return;
      var q = search.value.trim().toLowerCase();
      if (!q) return;
      var hit = heads.find(function(h){ return h.textContent.toLowerCase().indexOf(q) >= 0; });
      if (hit) hit.scrollIntoView({behavior:'smooth', block:'start'});
    });
  }
})();
</script>"""


# CSS extra para la subpágina de bibliografía (recursos.html).
RECURSOS_CSS = """
@media screen{
  .tools .navlink, .tools .volver{
    font-family:var(--font-display); font-weight:700; font-size:.86rem; color:var(--ink);
    text-decoration:none; padding:6px 12px; border:1px solid var(--line);
    border-radius:999px; background:var(--paper-2);
  }
  .tools .navlink:hover, .tools .volver:hover{ border-color:var(--red); color:var(--red); }
}
.recursos{ max-width:var(--readw); }
.recursos h1{
  font-family:var(--font-display); font-weight:800; color:var(--red-deep);
  border-bottom:3px solid var(--red); padding-bottom:.2em; font-size:2rem; letter-spacing:-.02em;
}
.recursos h3{ color:var(--teal-deep); }
.recursos a{ word-break:break-word; }
.recursos hr{ border:none; border-top:1px solid var(--line); margin:1.6rem 0; }
.recursos ul{ padding-left:1.2em; }
.recursos li{ margin:.5em 0; }
"""


def generar_recursos():
    """Genera docs/recursos.html (la subpágina de bibliografía) desde recursos.md."""
    import markdown

    ruta_md = os.path.join(REPO, "recursos.md")
    if not os.path.exists(ruta_md):
        return
    with open(ruta_md, "r", encoding="utf-8") as f:
        md = f.read()
    cuerpo = markdown.markdown(
        md, extensions=["tables", "fenced_code", "sane_lists"]
    )
    estilos = manual_lib.CSS + "\n" + manual_lib.css_pygments() + RECURSOS_CSS
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bibliografía recomendada — Python con Pokémon</title>
{FUENTES}
<style>{estilos}</style>
</head>
<body>
<div class="bg-grid" aria-hidden="true"></div>
<header class="topbar">
  <span class="pb"></span>
  <span class="brand">Pokédex <b>Codex</b></span>
  <div class="tools">
    <a class="volver" href="index.html">← Volver al libro</a>
    <button class="theme-toggle" type="button" title="Cambiar tema claro/oscuro">🌙</button>
  </div>
</header>
<div class="wrap">
<main class="book recursos">
{cuerpo}
</main>
</div>
{JS}
</body>
</html>"""
    destino = os.path.join(REPO, "docs", "recursos.html")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Subpágina de bibliografía: {destino}")


def construir_html():
    """Arma el documento HTML completo (standalone)."""
    # Numeramos los capítulos/secciones según el orden de la lista (Linux primero).
    capitulos = renumerar(manual_contenido.CAPITULOS)
    cuerpo = "".join(cap["html"] for cap in capitulos)
    estilos = manual_lib.CSS + "\n" + manual_lib.css_pygments()
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Python con Pokémon — El libro del curso</title>
{FUENTES}
<style>{estilos}</style>
</head>
<body>
<div class="bg-grid" aria-hidden="true"></div>
<header class="topbar">
  <span class="pb"></span>
  <span class="brand">Pokédex <b>Codex</b></span>
  <div class="tools">
    <a class="navlink" href="recursos.html">📚 Bibliografía</a>
    <input class="search-box" type="search" placeholder="Buscar tema… (Enter)" aria-label="Buscar">
    <button class="theme-toggle" type="button" title="Cambiar tema claro/oscuro">🌙</button>
  </div>
  <div class="progress"></div>
</header>
<div class="wrap">
{construir_rail(capitulos)}
<main class="book">
{construir_portada()}
{construir_toc(capitulos)}
{cuerpo}
<p class="cierre">⚡ "El mejor momento para empezar a programar fue ayer.
El segundo mejor momento es ahora." ⚡<br>¡A atraparlos a todos!</p>
</main>
</div>
{JS}
</body>
</html>"""


# ----------------------------------------------------------------------
#  Generación del PDF (varios motores, por orden de preferencia)
# ----------------------------------------------------------------------
def pdf_con_weasyprint(html):
    try:
        from weasyprint import HTML
    except ImportError:
        return False
    # WeasyPrint no renderiza emoji a color: los quitamos solo para el PDF.
    HTML(string=_quitar_emoji(html), base_url=RAIZ).write_pdf(SALIDA_PDF)
    return True


def pdf_con_chrome(ruta_html):
    chrome = None
    for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if shutil.which(c):
            chrome = c
            break
    if chrome is None:
        return False
    comando = [
        chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
        "--no-pdf-header-footer", "--virtual-time-budget=8000",
        f"--print-to-pdf={SALIDA_PDF}", "file://" + ruta_html,
    ]
    r = subprocess.run(comando, capture_output=True, text=True)
    return r.returncode == 0 and os.path.exists(SALIDA_PDF)


def pdf_con_soffice(ruta_html):
    soffice = shutil.which("libreoffice") or shutil.which("soffice")
    if soffice is None:
        return False
    r = subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf", "--outdir", RAIZ, ruta_html],
        capture_output=True, text=True,
    )
    return r.returncode == 0 and os.path.exists(SALIDA_PDF)


def generar():
    html = construir_html()

    # 1) Escribimos el libro en HTML (siempre, es abrible en el navegador).
    with open(SALIDA_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ HTML generado: {SALIDA_HTML}")

    # 1b) Copia para GitHub Pages (docs/index.html en la raíz del repo).
    os.makedirs(os.path.dirname(SALIDA_DOCS), exist_ok=True)
    with open(SALIDA_DOCS, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Copia para GitHub Pages: {SALIDA_DOCS}")

    # 1c) Subpágina de bibliografía (docs/recursos.html) desde recursos.md.
    try:
        generar_recursos()
    except Exception as e:
        print(f"  (no se pudo generar la subpágina de recursos: {e})")

    # 2) Generamos el PDF con el mejor motor disponible.
    print("➤ Generando PDF...")
    if pdf_con_weasyprint(html):
        print(f"✓ PDF generado con WeasyPrint: {SALIDA_PDF}")
        return 0
    print("  (WeasyPrint no disponible, probando Chrome...)")
    if pdf_con_chrome(SALIDA_HTML):
        print(f"✓ PDF generado con Chrome: {SALIDA_PDF}")
        return 0
    print("  (Chrome no disponible, probando LibreOffice...)")
    if pdf_con_soffice(SALIDA_HTML):
        print(f"✓ PDF generado con LibreOffice: {SALIDA_PDF}")
        return 0

    print("✗ No se pudo generar el PDF (instalá weasyprint: pip install weasyprint).")
    print(f"  De todos modos, podés abrir el libro en el navegador: {SALIDA_HTML}")
    return 1


if __name__ == "__main__":
    sys.exit(generar())
