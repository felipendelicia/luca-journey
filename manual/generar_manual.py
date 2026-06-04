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


def generar_recursos():
    """Devuelve el HTML de la página de bibliografía (desde recursos.md)."""
    import markdown

    ruta_md = os.path.join(REPO, "recursos.md")
    with open(ruta_md, "r", encoding="utf-8") as f:
        md = f.read()
    cuerpo_md = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])
    cuerpo = f'<div class="wrap"><main class="book recursos">{cuerpo_md}</main></div>'
    return _pagina(
        "Bibliografía — Python con Pokémon", cuerpo,
        activo="Recursos", clase_body="pagina-recursos",
    )


# ----------------------------------------------------------------------
#  Sitio web: barra de navegación, Pyodide (Python en el navegador) y páginas
# ----------------------------------------------------------------------
DOCS = os.path.join(REPO, "docs")

# Pyodide corre Python real dentro del navegador (WebAssembly), sin instalar nada.
PYODIDE_TAG = '<script src="https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js"></script>'

# Links de navegación del sitio (Inicio, Libro, Playground, Recursos).
_NAV = [
    ("Inicio", "index.html"),
    ("Libro", "libro.html"),
    ("Playground", "playground.html"),
    ("Recursos", "recursos.html"),
]


def topbar(activo="", con_busqueda=False):
    """Barra superior compartida por todas las páginas del sitio."""
    enlaces = "".join(
        f'<a class="navlink{" activo" if texto == activo else ""}" href="{href}">{texto}</a>'
        for texto, href in _NAV
    )
    busqueda = (
        '<input class="search-box" type="search" placeholder="Buscar… (Enter)" aria-label="Buscar">'
        if con_busqueda else ""
    )
    return f"""<header class="topbar">
  <a class="brand-link" href="index.html"><span class="pb"></span><span class="brand">Pokédex <b>Codex</b></span></a>
  <div class="tools">{enlaces}{busqueda}<button class="theme-toggle" type="button" title="Tema claro/oscuro">🌙</button></div>
  <div class="progress"></div>
</header>"""


# Runner de Pyodide + botones "ejecutar" en el código del libro y en el playground.
RUN_JS = r"""
let _pyReady = null;
async function _getPy(estado){
  if(!_pyReady){
    if(estado){ estado.textContent = "⏳ Cargando Python en el navegador (la primera vez tarda ~10-20s)…"; }
    _pyReady = loadPyodide();
  }
  return _pyReady;
}
async function _correr(codigo, outEl, btn, estado){
  outEl.classList.add("show");
  outEl.innerHTML = '<span class="out-label">SALIDA</span>';
  if(btn){ btn.disabled = true; }
  try{
    const py = await _getPy(estado || outEl);
    if(estado){ estado.textContent = ""; }
    py.setStdout({ batched: (s) => { outEl.appendChild(document.createTextNode(s)); } });
    py.setStderr({ batched: (s) => { const e=document.createElement("span"); e.className="err"; e.textContent=s; outEl.appendChild(e); } });
    py.setStdin({ stdin: () => { const v = window.prompt("input():"); return v === null ? "" : v; } });
    await py.runPythonAsync(codigo);
  }catch(err){
    const e=document.createElement("span"); e.className="err";
    e.textContent = "\n" + (err && err.message ? err.message : err);
    outEl.appendChild(e);
  }finally{
    if(btn){ btn.disabled = false; }
  }
}
document.addEventListener("DOMContentLoaded", function(){
  document.querySelectorAll("figure.code").forEach(function(fig){
    const langEl = fig.querySelector(".code-lang");
    const lang = (langEl ? langEl.textContent : "").trim().toLowerCase();
    if(lang !== "python") return;
    const bar = fig.querySelector(".code-bar");
    const pre = fig.querySelector("pre");
    if(!bar || !pre) return;
    const out = document.createElement("div"); out.className = "code-out";
    fig.appendChild(out);
    const btn = document.createElement("button");
    btn.className = "run-btn"; btn.type = "button"; btn.textContent = "▶ ejecutar";
    btn.addEventListener("click", function(){ _correr(pre.innerText, out, btn); });
    bar.appendChild(btn);
  });
  const pgRun = document.getElementById("pg-run");
  if(pgRun){
    const code = document.getElementById("pg-code");
    const out = document.getElementById("pg-out");
    const estado = document.getElementById("pg-status");
    pgRun.addEventListener("click", function(){ _correr(code.value, out, pgRun, estado); });
    document.querySelectorAll(".pg-ej").forEach(function(b){
      b.addEventListener("click", function(){ code.value = b.getAttribute("data-code"); code.focus(); });
    });
  }
});
"""


def _pagina(titulo, cuerpo, activo="", clase_body="", scripts="", con_busqueda=False):
    """Arma una página HTML del sitio con la barra, los estilos y los scripts comunes."""
    estilos = manual_lib.CSS + "\n" + manual_lib.css_pygments()
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
{FUENTES}
<style>{estilos}</style>
</head>
<body class="{clase_body}">
<div class="bg-grid" aria-hidden="true"></div>
{topbar(activo, con_busqueda)}
{cuerpo}
{JS}
{scripts}
</body>
</html>"""


def construir_landing():
    """La página de inicio del sitio."""
    tarjetas = [
        ("📖", "El libro", "Aprendé Linux y Python desde cero, con toda la teoría del curso.", "libro.html"),
        ("🎮", "Playground", "Escribí y ejecutá Python en el navegador, sin instalar nada.", "playground.html"),
        ("📚", "Bibliografía", "Libros, cursos (¡CS50!) y recursos recomendados.", "recursos.html"),
        ("🗺️", "Roadmap", "El mapa completo del viaje, semana por semana.", "roadmap.html"),
        ("💻", "Proyectos", "Los 4 proyectos finales para coronar el curso.", "proyectos.html"),
        ("🏆", "El repositorio", "Código, ejercicios y la Liga Pokémon en GitHub.", "https://github.com/felipendelicia/luca-journey"),
    ]
    cards = "".join(
        f'<a class="card" href="{href}"><div class="ico">{ico}</div><h3>{t}</h3><p>{d}</p></a>'
        for ico, t, d, href in tarjetas
    )
    cuerpo = f"""<div class="wrap"><main class="landing">
  <section class="hero-home">
    <p class="kick">El curso completo, online</p>
    <h1>Python con Pokémon</h1>
    <p>Aprendé a programar desde cero — Linux, Python y mucha aventura — y convertite en Campeón de Kanto. 🏆</p>
    <div class="cta">
      <a class="btn-grande" href="libro.html">📖 Empezar a leer</a>
      <a class="btn-grande sec" href="playground.html">🎮 Probar Python ya</a>
    </div>
  </section>
  <div class="cards">{cards}</div>
</main></div>"""
    return _pagina("Python con Pokémon — Inicio", cuerpo, activo="Inicio", clase_body="pagina-landing")


def construir_playground():
    """El playground: editor de Python que corre en el navegador (Pyodide)."""
    inicial = (
        'print("¡Hola, mundo Pokémon!")\n\n'
        'nombre = "Pikachu"\n'
        'nivel = 25\n'
        'print(f"Mi {nombre} es nivel {nivel}")\n\n'
        'for i in range(1, 4):\n'
        '    print(f"Pokéball número {i}")\n'
    )
    ejemplos = [
        ("Saludo", 'nombre = input("¿Tu nombre? ")\nprint(f"¡Hola, {nombre}!")'),
        ("Bucle", 'for n in range(1, 11):\n    print(n, "x 7 =", n * 7)'),
        ("Función", 'def dano(ataque, defensa):\n    return max(ataque - defensa, 1)\n\nprint(dano(50, 20))'),
        ("Lista", 'equipo = ["Pikachu", "Charizard", "Snorlax"]\nfor p in equipo:\n    print("Tengo a", p)'),
    ]
    import html as _h
    botones = "".join(
        f'<button class="pg-ej" type="button" data-code="{_h.escape(cod).replace(chr(10), "&#10;")}">{nom}</button>'
        for nom, cod in ejemplos
    )
    cuerpo = f"""<div class="wrap"><main class="pg book">
  <h1 class="cap"><span class="cap-kicker">Probá</span><span class="cap-num">🎮</span><span class="cap-ttl">Playground de Python</span></h1>
  <p>Escribí código Python y tocá <strong>Ejecutar</strong>. Corre de verdad en tu navegador (no se instala nada).
  La primera ejecución descarga Python (~10-20s); después es instantáneo.</p>
  <div class="pg-ejemplos">{botones}</div>
  <div class="pg-panel">
    <div class="pg-bar"><span class="dots"><i></i><i></i><i></i></span><span class="lbl">python</span>
      <button class="pg-run" id="pg-run" type="button">▶ Ejecutar</button></div>
    <textarea class="pg-code" id="pg-code" spellcheck="false">{_h.escape(inicial)}</textarea>
    <div class="pg-out" id="pg-out"><span class="out-label">SALIDA</span></div>
  </div>
  <p class="pg-status" id="pg-status"></p>
  <p style="color:var(--ink-mute);font-size:.9rem">💡 Si tu código usa <code>input()</code>, te va a aparecer una ventanita para escribir la respuesta.</p>
</main></div>"""
    return _pagina(
        "Playground — Python con Pokémon", cuerpo, activo="Playground",
        clase_body="pagina-recursos",
        scripts=PYODIDE_TAG + '\n<script src="pyodide-run.js"></script>',
    )


def construir_proyectos():
    """Página con los 4 proyectos finales."""
    base = "https://github.com/felipendelicia/luca-journey/tree/main/proyectos"
    proys = [
        ("🔴", "pokedex-cli", "Pokédex de consola que consume la PokéAPI, muestra stats y sprites en ASCII, y guarda favoritos.", f"{base}/pokedex-cli"),
        ("⚔️", "batalla-pokemon", "Simulador de batalla por turnos con tipos, movimientos, PP, estados alterados y dos modos (vs CPU y vs jugador).", f"{base}/batalla-pokemon"),
        ("📒", "agenda-entrenador", "Agenda modular del Entrenador: capturas, equipo, batallas y estadísticas, con persistencia en JSON.", f"{base}/agenda-entrenador"),
        ("🌐", "pokedex-web", "Pokédex web con Flask + SQLite + PokéAPI, con buscador y edición.", f"{base}/pokedex-web"),
    ]
    cards = "".join(
        f'<a class="card" href="{href}"><div class="ico">{ico}</div><h3>{t}</h3><p>{d}</p></a>'
        for ico, t, d, href in proys
    )
    cuerpo = f"""<div class="wrap"><main class="book recursos">
  <h1>💻 Proyectos finales</h1>
  <p>Cuatro aplicaciones completas para coronar el curso. Cada una tiene su propio README con instrucciones. El código está en GitHub:</p>
  <div class="cards">{cards}</div>
</main></div>"""
    return _pagina("Proyectos — Python con Pokémon", cuerpo, activo="", clase_body="pagina-recursos")


def pagina_desde_md(titulo, ruta_md, activo="", h1=None):
    """Convierte un .md del repo en una página del sitio (estilo libro)."""
    import markdown as _md
    ruta = os.path.join(REPO, ruta_md)
    with open(ruta, "r", encoding="utf-8") as f:
        md = f.read()
    cuerpo_md = _md.markdown(md, extensions=["tables", "fenced_code"])
    cuerpo = f'<div class="wrap"><main class="book recursos">{cuerpo_md}</main></div>'
    return _pagina(titulo, cuerpo, activo=activo, clase_body="pagina-recursos")


def construir_html():
    """Arma el libro completo (manual.html / libro.html)."""
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
{topbar(activo="Libro", con_busqueda=True)}
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
{PYODIDE_TAG}
<script src="pyodide-run.js"></script>
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


def _escribir(nombre, html):
    destino = os.path.join(DOCS, nombre)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ {destino}")


def generar():
    html = construir_html()
    os.makedirs(DOCS, exist_ok=True)

    # 1) El libro: copia local (para el PDF) y en el sitio (docs/libro.html).
    with open(SALIDA_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ HTML generado: {SALIDA_HTML}")
    _escribir("libro.html", html)

    # 2) El resto del sitio.
    print("➤ Generando el sitio web...")
    _escribir("index.html", construir_landing())
    _escribir("playground.html", construir_playground())
    _escribir("proyectos.html", construir_proyectos())
    _escribir("pyodide-run.js", RUN_JS)
    try:
        _escribir("recursos.html", generar_recursos())
    except Exception as e:
        print(f"  (recursos: {e})")
    try:
        _escribir("roadmap.html", pagina_desde_md(
            "Roadmap — Python con Pokémon", "ROADMAP.md", activo=""))
    except Exception as e:
        print(f"  (roadmap: {e})")

    # 3) Generamos el PDF con el mejor motor disponible.
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
