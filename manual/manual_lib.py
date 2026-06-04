"""
manual_lib.py — Herramientas y estilos para construir el libro (manual.html / manual.pdf).

Acá viven los "ladrillos" del libro: funciones que devuelven HTML (párrafos, listas,
cajas de aviso, tablas y bloques de código con resaltado) y la hoja de estilos.
El contenido en sí está en manual_contenido.py.

Diseño: "Pokédex Codex". Papel crema cálido, tipografías distintivas (Bricolage
Grotesque + Hanken Grotesk + JetBrains Mono + Silkscreen), ventanas de código
oscuras y acentos de consola retro. La experiencia rica es para PANTALLA; al
imprimir (PDF) se vuelve un libro limpio y paginado.
"""

import html as _html
import re
import textwrap

from pygments import highlight
from pygments.lexers import PythonLexer, BashLexer
from pygments.formatters import HtmlFormatter


def _make_formatter():
    """Elige un tema oscuro de Pygments disponible para las ventanas de código."""
    for estilo in ("one-dark", "dracula", "material", "monokai", "native"):
        try:
            return HtmlFormatter(style=estilo, cssclass="highlight")
        except Exception:
            continue
    return HtmlFormatter(cssclass="highlight")


_FORMATTER = _make_formatter()
CODE_BG = _FORMATTER.style.background_color or "#1e2030"


def css_pygments():
    """CSS que pinta los tokens del código (tema oscuro)."""
    return _FORMATTER.get_style_defs(".highlight")


# ----------------------------------------------------------------------
#  Bloques de contenido (devuelven HTML)
# ----------------------------------------------------------------------
def code(src, lang="python"):
    """Bloque de código como una 'ventana' con barra y resaltado."""
    src = textwrap.dedent(src).strip("\n")
    lexer = BashLexer() if lang == "bash" else PythonLexer()
    cuerpo = highlight(src, lexer, _FORMATTER)
    etiqueta = "bash" if lang == "bash" else "python"
    return (
        '<figure class="code">'
        '<figcaption class="code-bar">'
        '<span class="dots"><i></i><i></i><i></i></span>'
        f'<span class="code-lang">{etiqueta}</span>'
        "</figcaption>"
        f"{cuerpo}</figure>"
    )


def inline(texto):
    """Código en línea: <code>...</code>."""
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
        f'<span class="et">{etiqueta}</span>'
        f'<span class="callout-body">{html_text}</span></div>'
    )


def tabla(headers, filas):
    """Tabla HTML a partir de encabezados y filas (listas de strings)."""
    th = "".join(f"<th>{h}</th>" for h in headers)
    cuerpo = ""
    for fila in filas:
        celdas = "".join(f"<td>{c}</td>" for c in fila)
        cuerpo += f"<tr>{celdas}</tr>"
    return (
        '<div class="tabla-wrap"><table>'
        f"<thead><tr>{th}</tr></thead><tbody>{cuerpo}</tbody>"
        "</table></div>"
    )


def capitulo(cid, titulo, *bloques):
    """Arma un capítulo: encabezado con número + sus bloques de contenido."""
    m = re.match(r"^\s*(\d+)\.\s*(.*)$", titulo)
    num, resto = (m.group(1), m.group(2)) if m else ("", titulo)
    h1 = (
        f'<h1 id="{cid}" class="cap">'
        f'<span class="cap-kicker">Capítulo</span>'
        f'<span class="cap-num">{num}</span>'
        f'<span class="cap-ttl">{resto}</span>'
        "</h1>"
    )
    return {
        "id": cid,
        "titulo": titulo,
        "num": num,
        "resto": resto,
        "html": h1 + "".join(bloques),
    }


# ----------------------------------------------------------------------
#  Hoja de estilos del libro
# ----------------------------------------------------------------------
_VARS = """
:root{
  --paper:#f6efe1; --paper-2:#fffdf7; --card:#fffaf0;
  --ink:#211f2b; --ink-soft:#5a5667; --ink-mute:#8a8597;
  --red:#e3350d; --red-deep:#b21807; --red-ink:#7a1206;
  --yellow:#ffcb05; --yellow-deep:#e0a800;
  --teal:#0ea5a0; --teal-deep:#0b7c78;
  --blue:#2f5fd0;
  --line:#e7dcc4; --line-2:#efe6d2;
  --code-bg:%s;
  --shadow-sm:0 2px 6px rgba(40,30,10,.07);
  --shadow:0 14px 40px -18px rgba(60,40,10,.35);
  --shadow-lg:0 30px 70px -30px rgba(60,30,10,.5);
  --font-display:"Bricolage Grotesque","Hanken Grotesk",system-ui,sans-serif;
  --font-body:"Hanken Grotesk",system-ui,"Segoe UI",sans-serif;
  --font-mono:"JetBrains Mono",ui-monospace,"DejaVu Sans Mono",monospace;
  --font-pixel:"Silkscreen","JetBrains Mono",monospace;
  --maxw:1180px; --readw:720px;
}
""" % CODE_BG

_MAIN = r"""
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:var(--font-body); font-size:17px; line-height:1.68;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
}

/* ===== Tipografía base ===== */
h1,h2,h3{font-family:var(--font-display); font-weight:800; letter-spacing:-.02em; line-height:1.1;}
p{margin:.7em 0;}
strong{color:var(--red-ink); font-weight:700;}
a{color:var(--teal-deep); text-decoration:none;}

/* Código en línea */
p code,li code,td code,h2 code,h3 code,figcaption code{
  font-family:var(--font-mono); font-size:.82em; font-weight:500;
  background:#fff; color:var(--red-deep);
  border:1px solid var(--line); border-radius:6px; padding:.06em .4em;
}

/* ===== Encabezados de sección ===== */
h1.cap{
  display:grid; grid-template-columns:auto 1fr; grid-template-rows:auto auto;
  column-gap:18px; align-items:center; margin:0 0 .7em;
  padding-bottom:.5rem; border-bottom:3px solid var(--ink);
}
.cap-kicker{
  grid-column:2; grid-row:1; align-self:end;
  font-family:var(--font-pixel); font-size:10px; letter-spacing:.18em;
  text-transform:uppercase; color:var(--red); margin-bottom:2px;
}
.cap-num{
  grid-column:1; grid-row:1 / span 2; align-self:center;
  font-family:var(--font-pixel); font-size:24px; color:#fff;
  background:var(--red); width:62px; height:62px; border-radius:16px;
  display:flex; align-items:center; justify-content:center;
  box-shadow:0 0 0 4px var(--paper),0 0 0 6px var(--red), var(--shadow-sm);
}
.cap-ttl{grid-column:2; grid-row:2; font-size:2.05rem; color:var(--ink);}

h2{
  font-size:1.42rem; color:var(--red-deep); margin:2.2rem 0 .5rem;
  padding-left:.7rem; position:relative;
}
h2::before{
  content:""; position:absolute; left:0; top:.18em; bottom:.18em; width:5px;
  border-radius:3px; background:linear-gradient(var(--yellow),var(--red));
}
h3{font-size:1.12rem; color:var(--ink); margin:1.4rem 0 .35rem;}

ul,ol{margin:.6em 0; padding-left:1.3em;}
li{margin:.32em 0;}
li::marker{color:var(--red);}

/* ===== Ventanas de código ===== */
figure.code{
  margin:1.2em 0; border-radius:14px; overflow:hidden;
  background:var(--code-bg); box-shadow:var(--shadow);
  border:1px solid rgba(0,0,0,.25);
}
.code-bar{
  display:flex; align-items:center; gap:10px;
  padding:9px 14px; background:rgba(255,255,255,.05);
  border-bottom:1px solid rgba(255,255,255,.08);
}
.code-bar .dots{display:flex; gap:7px;}
.code-bar .dots i{width:11px; height:11px; border-radius:50%; display:block;}
.code-bar .dots i:nth-child(1){background:#ff5f56;}
.code-bar .dots i:nth-child(2){background:#ffbd2e;}
.code-bar .dots i:nth-child(3){background:#27c93f;}
.code-lang{
  margin-left:auto; font-family:var(--font-pixel); font-size:9px;
  letter-spacing:.12em; text-transform:uppercase; color:rgba(255,255,255,.55);
}
.highlight{margin:0; padding:16px 18px; overflow-x:auto; background:transparent !important;}
.highlight pre{
  margin:0; font-family:var(--font-mono); font-size:13.5px; line-height:1.6;
  white-space:pre-wrap; word-wrap:break-word; color:#e8eaf2;
}

/* ===== Cajas de aviso ===== */
.callout{
  position:relative; margin:1.2em 0; padding:14px 16px 14px 18px;
  border-radius:13px; background:var(--card); border:1px solid var(--line);
  border-left:5px solid var(--ink-mute); box-shadow:var(--shadow-sm);
  display:flex; flex-direction:column; gap:6px;
}
.callout .et{
  align-self:flex-start; font-family:var(--font-pixel); font-size:9px;
  letter-spacing:.1em; color:#fff; padding:4px 9px; border-radius:7px;
}
.callout-body{display:block;}
.callout p{margin:.2em 0;}
.nota{background:#eef5fd; border-color:#bcd8f5; border-left-color:var(--blue);}
.nota .et{background:var(--blue);}
.tip{background:#ecfaf1; border-color:#bce7cd; border-left-color:var(--teal-deep);}
.tip .et{background:var(--teal-deep);}
.cuidado{background:#fff6e2; border-color:#f3dca0; border-left-color:var(--yellow-deep);}
.cuidado .et{background:var(--yellow-deep);}
.clave{background:#fdeef6; border-color:#f3c6df; border-left-color:#c43d8b;}
.clave .et{background:#c43d8b;}
.pokemon{background:#feefe9; border-color:#f6c9b6; border-left-color:var(--red);}
.pokemon .et{background:var(--red);}

/* ===== Tablas ===== */
.tabla-wrap{margin:1.1em 0; overflow-x:auto; border-radius:12px; box-shadow:var(--shadow-sm);}
table{border-collapse:collapse; width:100%; background:var(--paper-2); font-size:.92rem;}
th,td{padding:9px 13px; text-align:left; border-bottom:1px solid var(--line);}
th{
  background:var(--ink); color:#fff; font-family:var(--font-display);
  font-weight:700; font-size:.82rem; letter-spacing:.02em; border-bottom:none;
}
tbody tr:last-child td{border-bottom:none;}
tbody tr:nth-child(even){background:#fbf5e9;}

/* ===== Índice (contenidos) ===== */
.toc{
  margin:0 0 2rem; padding:26px 28px; border-radius:18px;
  background:var(--paper-2); border:1px solid var(--line); box-shadow:var(--shadow-sm);
}
.toc h2.toc-t{
  font-family:var(--font-display); font-size:1.5rem; color:var(--ink);
  margin:0 0 .8rem; padding:0; }
.toc h2.toc-t::before{display:none;}
.toc ul{list-style:none; padding:0; margin:0;}
.toc > ul > li{margin:.5rem 0;}
.toc > ul > li > a{font-family:var(--font-display); font-weight:700; color:var(--ink); font-size:1.02rem;}
.toc ul ul{padding-left:1.1rem; margin:.2rem 0 .6rem; border-left:2px dotted var(--line);}
.toc ul ul li{margin:.18rem 0;}
.toc ul ul a{color:var(--ink-soft); font-size:.92rem;}
.toc a:hover{color:var(--red);}

.cierre{
  text-align:center; color:var(--ink-mute); font-style:italic; margin:3rem 0 1rem;
  font-size:.95rem;
}

/* =====================================================================
   PANTALLA — la experiencia rica de navegador
   ===================================================================== */
@media screen{
  body{padding-top:54px;}

  /* fondo con grilla de puntos + leve glow */
  .bg-grid{
    position:fixed; inset:0; z-index:-2; pointer-events:none;
    background:
      radial-gradient(1200px 600px at 80% -10%, rgba(227,53,13,.10), transparent 60%),
      radial-gradient(900px 500px at -10% 110%, rgba(14,165,160,.10), transparent 60%),
      radial-gradient(rgba(120,100,60,.16) 1px, transparent 1.4px);
    background-size:auto,auto,22px 22px;
  }

  /* barra superior fija con progreso de lectura */
  .topbar{
    position:fixed; top:0; left:0; right:0; z-index:50; height:54px;
    display:flex; align-items:center; gap:14px; padding:0 20px;
    background:rgba(246,239,225,.82); backdrop-filter:saturate(1.4) blur(10px);
    border-bottom:1px solid var(--line);
  }
  .topbar .pb{
    width:22px; height:22px; border-radius:50%; border:3px solid var(--ink);
    background:linear-gradient(to bottom,var(--red) 50%,#fff 50%); position:relative; flex:0 0 auto;
  }
  .topbar .pb::after{content:""; position:absolute; inset:8px; margin:auto; width:4px; height:4px; border-radius:50%; background:var(--ink); top:7px; left:7px;}
  .topbar .brand{font-family:var(--font-pixel); font-size:11px; letter-spacing:.14em; color:var(--ink); text-transform:uppercase;}
  .topbar .brand b{color:var(--red);}
  .topbar .meta{margin-left:auto; font-family:var(--font-pixel); font-size:9px; letter-spacing:.1em; color:var(--ink-mute);}
  .progress{
    position:absolute; left:0; bottom:-1px; height:3px; width:100%;
    background:linear-gradient(90deg,var(--red),var(--yellow),var(--teal));
    transform-origin:0 50%; transform:scaleX(0);
    animation:grow linear both; animation-timeline:scroll(root block);
  }
  @keyframes grow{to{transform:scaleX(1);}}

  /* layout con riel lateral */
  .wrap{max-width:var(--maxw); margin:0 auto; padding:34px 24px 80px;
        display:grid; grid-template-columns:248px minmax(0,1fr); gap:46px;}
  .rail{position:sticky; top:78px; align-self:start; height:max-content;}
  .rail .device{
    background:var(--ink); color:#fff; border-radius:18px; padding:16px;
    box-shadow:var(--shadow); margin-bottom:16px; position:relative; overflow:hidden;
  }
  .rail .device::before{content:""; position:absolute; inset:0;
    background:repeating-linear-gradient(transparent 0 3px, rgba(255,255,255,.025) 3px 4px);}
  .rail .lens{
    width:54px; height:54px; border-radius:50%;
    background:radial-gradient(circle at 32% 30%, #cdeafe 0 14%, #3aa0ee 38%, #1357a8 78%);
    border:4px solid #eaf4ff; box-shadow:0 0 0 3px var(--ink),0 6px 14px rgba(0,0,0,.4);
    position:relative;
  }
  .rail .leds{display:flex; gap:7px; margin-top:14px;}
  .rail .leds i{width:10px; height:10px; border-radius:50%;}
  .rail .leds i:nth-child(1){background:#ff5f56;}
  .rail .leds i:nth-child(2){background:var(--yellow);}
  .rail .leds i:nth-child(3){background:#27c93f;}
  .rail .dev-tt{font-family:var(--font-pixel); font-size:9px; letter-spacing:.12em; color:rgba(255,255,255,.6); margin-top:14px;}
  .rail nav{font-size:.86rem; max-height:60vh; overflow:auto; padding-right:4px;}
  .rail nav a{
    display:flex; gap:9px; align-items:center; padding:6px 8px; border-radius:9px;
    color:var(--ink-soft); margin:1px 0;
  }
  .rail nav a .rn{
    font-family:var(--font-pixel); font-size:9px; color:#fff; background:var(--ink-mute);
    width:22px; height:20px; border-radius:6px; display:flex; align-items:center; justify-content:center; flex:0 0 auto;
  }
  .rail nav a:hover{background:#fff; color:var(--ink); box-shadow:var(--shadow-sm);}
  .rail nav a:hover .rn{background:var(--red);}

  .book{min-width:0; max-width:var(--readw);}
  .book h1.cap{scroll-margin-top:74px;}
  .book h2{scroll-margin-top:70px;}

  /* el riel desaparece en pantallas chicas */
  @media (max-width:920px){
    .wrap{grid-template-columns:1fr; gap:0;}
    .rail{display:none;}
    .book{max-width:none;}
  }

  /* portada estilo consola Pokédex */
  .portada{
    position:relative; margin:0 0 2.4rem; padding:54px 40px 48px; overflow:hidden;
    border-radius:24px; color:#fff; text-align:center;
    background:
      radial-gradient(120% 120% at 50% -20%, #ff6a3d 0%, #e3350d 32%, #9d1505 72%, #5e0d04 100%);
    box-shadow:var(--shadow-lg);
  }
  .portada::after{content:""; position:absolute; inset:0; pointer-events:none;
    background:repeating-linear-gradient(transparent 0 3px, rgba(0,0,0,.05) 3px 4px);
    mix-blend-mode:overlay;}
  .portada .pokeball{
    width:108px; height:108px; border-radius:50%; margin:0 auto 22px;
    background:linear-gradient(to bottom,#fff 0 46%,var(--ink) 46% 54%,#fff 54%);
    border:7px solid var(--ink); position:relative;
    box-shadow:0 14px 30px rgba(0,0,0,.35);
  }
  .portada .pokeball::after{content:""; position:absolute; top:50%; left:50%;
    width:30px; height:30px; border-radius:50%; background:#fff; border:7px solid var(--ink);
    transform:translate(-50%,-50%);}
  .portada .kick{font-family:var(--font-pixel); font-size:11px; letter-spacing:.3em; color:var(--yellow); text-transform:uppercase;}
  .portada h1{
    font-size:clamp(2.4rem,6vw,4rem); margin:.3rem 0 .2rem; color:#fff;
    text-shadow:0 3px 0 rgba(0,0,0,.18); letter-spacing:-.03em;
  }
  .portada .sub{font-size:1.06rem; opacity:.95; margin:.25rem 0; max-width:560px; margin-inline:auto;}
  .portada .pie{margin-top:26px; font-family:var(--font-pixel); font-size:9px; letter-spacing:.14em; opacity:.8;}

  /* aparición escalonada al cargar */
  .reveal{opacity:0; transform:translateY(16px); animation:rise .8s cubic-bezier(.2,.75,.25,1) forwards;}
  .d1{animation-delay:.05s;} .d2{animation-delay:.14s;} .d3{animation-delay:.23s;}
  .d4{animation-delay:.32s;} .d5{animation-delay:.41s;}
  @keyframes rise{to{opacity:1; transform:none;}}

  figure.code:hover{transform:translateY(-2px); box-shadow:var(--shadow-lg); transition:transform .25s, box-shadow .25s;}
  .callout{transition:transform .2s;}
  .callout:hover{transform:translateX(2px);}
}

/* =====================================================================
   IMPRESIÓN — el libro limpio y paginado (WeasyPrint)
   ===================================================================== */
@media print{
  @page{
    size:A4; margin:2cm 1.7cm 1.8cm;
    @bottom-center{content:counter(page); color:#9aa0a6; font-size:9pt;}
    @top-right{content:"Python con Pokémon"; color:#c9ced4; font-size:8.5pt;}
  }
  @page:first{margin:0; @bottom-center{content:none;} @top-right{content:none;}}
  body{font-size:10.5pt; background:#fff; padding:0;}
  .bg-grid,.topbar,.rail{display:none !important;}
  .wrap{display:block; max-width:none; margin:0; padding:0;}
  .book{max-width:none;}
  p{text-align:justify;}

  .portada{
    height:100vh; color:#fff; text-align:center; padding-top:7cm; page-break-after:always;
    background:linear-gradient(160deg,#b5121b,#d62828 55%,#f25c54);
  }
  .portada .pokeball{width:120px; height:120px; border-radius:50%;
    border:8px solid #2a2a2a; margin:0 auto 1cm; background:linear-gradient(to bottom,#ee1515 50%,#fff 50%);}
  .portada .pokeball::after{display:none;}
  .portada h1{font-size:30pt; margin:.3cm 0;}
  .portada .kick{font-size:11pt; letter-spacing:.2em; color:#ffe; }
  .portada .sub{font-size:13pt;}

  .toc{page-break-after:always; box-shadow:none; border:none; padding:0;}
  h1.cap{page-break-before:always; display:block; border-bottom:3px solid #0b5fa5; color:#0b5fa5;}
  .cap-kicker{display:inline; font-family:inherit; color:#b21807; font-size:10pt; letter-spacing:.05em; margin-right:.4em;}
  .cap-num{display:inline; background:none; color:#0b5fa5; box-shadow:none; width:auto; height:auto; font-family:inherit; font-size:21pt;}
  .cap-num::after{content:". ";}
  .cap-ttl{display:inline; font-size:21pt; color:#0b5fa5;}
  h2{color:#11497e;} h2::before{background:#ffcb05;}
  figure.code,.callout,.tabla-wrap,table{box-shadow:none;}
  figure.code:hover{transform:none;}
}
"""

CSS = _VARS + _MAIN
