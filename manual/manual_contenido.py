"""
manual_contenido.py — El contenido del libro, capítulo por capítulo.

La mayoría de los capítulos se GENERAN automáticamente desde los archivos
'teoria.md' del curso (carpeta curso/): así el libro contiene TODO el contenido
de las teorías y se mantiene sincronizado con ellas. Para cambiar la teoría de un
tema, se edita su teoria.md y se regenera el libro (python generar_manual.py).

Solo unos pocos capítulos están escritos a mano acá: la introducción (cómo usar
el libro y el curso), el mapa de temas y la página de ayuda/glosario.
"""

from manual_lib import (
    capitulo, h2, p, ul, ol, code, caja, tabla, inline, desde_teoria,
)


# ======================================================================
#  Capítulo 0 — Cómo usar este libro y el curso (escrito a mano)
# ======================================================================
cap_intro = capitulo(
    "cap-intro", "0. Cómo usar este libro y el curso",
    p("""¡Bienvenido! Este libro tiene <strong>dos caras</strong>. Por un lado es el
    <strong>manual</strong> del proyecto: te explica cómo instalarlo y cómo avanzar.
    Por otro lado es un <strong>libro completo</strong> que te enseña Linux y Python
    desde cero: contiene <strong>toda la teoría del curso</strong>, con explicaciones
    paso a paso, analogías Pokémon y muchos ejemplos."""),
    p("""Está pensado para alguien que <strong>nunca programó</strong>. No hace falta
    saber nada de antes. 🐍"""),

    h2("0.1. ¿Qué es este proyecto?", "que-es"),
    p("""Es un curso completo de <strong>Linux</strong> y <strong>Python</strong>,
    dividido en 12 semanas (más una semana de descanso de Git) y 4 proyectos finales.
    Cada concepto se explica con una analogía Pokémon, cada ejercicio usa Pokémon, y
    cada proyecto es algo que un Entrenador usaría de verdad."""),
    p("""Los capítulos de teoría de este libro son exactamente las lecciones del curso:
    podés leer el libro de principio a fin, o usar cada semana del curso por separado."""),

    h2("0.2. Instalación", "instalacion"),
    p("Abrí una terminal dentro de la carpeta del proyecto y corré:"),
    code("bash setup.sh", lang="bash"),
    p("""Eso crea un <em>entorno virtual</em> (una cajita aislada para las librerías
    del curso) e instala lo necesario. Después, cada vez que vayas a trabajar, lo activás:"""),
    code("source venv/bin/activate", lang="bash"),
    caja("""Si <code>setup.sh</code> falla, abrilo con un editor: está comentado línea
    por línea. Las dos primeras semanas son de Linux y no necesitan Python para los
    ejercicios de terminal.""", "cuidado"),

    h2("0.3. La Liga Pokémon: jugá tu progreso", "liga"),
    p("""La mejor forma de hacer el curso. En vez de "hacer la tarea", subís de nivel.
    Hay un único programa que es tu centro de mando:"""),
    code("python aventura.py", lang="bash"),
    p("Desde ese único archivo podés:"),
    ul(
        "🎮 <strong>Elegir un capítulo para jugar</strong>: lanza el juego interactivo de esa semana. Si tenés progreso, <strong>continuás donde lo dejaste</strong>; si ya lo completaste, te ofrece <strong>reintentarlo</strong>.",
        "🏋️ <strong>Entrenar</strong> una semana: corre <em>tus</em> ejercicios y te da EXP por cada test que pasás. Si algo falla, te dice <strong>qué ejercicio</strong> y una pista.",
        "⚔️ <strong>Combates de gimnasio</strong>: con una medalla en mano, retás al líder con un desafío integrador más difícil.",
        "🎴 Ver tu <strong>Tarjeta de Entrenador</strong>, 🏅 las <strong>8 medallas</strong>, ✨ los <strong>logros</strong> y 🗺️ el mapa.",
        "🔥 Mantener tu <strong>racha</strong> diaria.",
    ),
    p("Cuando consigas las 8 medallas (y venzas a los 8 líderes), <strong>¡sos Campeón de Kanto!</strong> 🏆"),

    h2("0.4. El método: cómo trabajar cada semana", "metodo"),
    ol(
        "📖 <strong>Leé</strong> la teoría del tema (este libro la tiene completa).",
        "✏️ <strong>Resolvé</strong> los ejercicios (escribí tu código donde dice <code># TU CÓDIGO ACÁ</code>).",
        '🧪 <strong>Probá</strong> con los tests (ver el <a href="#cap-ayuda">capítulo de ayuda</a>).',
        "🎮 <strong>Jugá</strong> el <code>interactivo.py</code> de la semana.",
        "🏋️ <strong>Entrená</strong> esa semana en la Liga para ganar EXP.",
    ),
    caja("""<strong>Regla de oro:</strong> equivocarse es parte del juego. Escribí el
    código vos mismo, no copies y pegues: tipear te enseña.""", "tip"),
)


# ======================================================================
#  Capítulos de TEORÍA — generados desde los teoria.md del curso
# ======================================================================
# Linux primero, después Python (en el orden del curso). El lang_default es
# 'bash' para las semanas de terminal y de Git, y 'python' para el resto.
cap_linux1 = desde_teoria("cap-linux1", "curso/semana-01-linux-fundamentos/teoria.md", lang_default="bash")
cap_linux2 = desde_teoria("cap-linux2", "curso/semana-02-linux-intermedio/teoria.md", lang_default="bash")
cap_py_intro = desde_teoria("cap-py-intro", "curso/semana-03-python-introduccion/teoria.md")
cap_flujo = desde_teoria("cap-flujo", "curso/semana-04-python-control-de-flujo/teoria.md")
cap_func = desde_teoria("cap-func", "curso/semana-05-python-funciones/teoria.md")
cap_colecciones = desde_teoria("cap-colecciones", "curso/semana-06-python-listas-y-colecciones/teoria.md")
cap_archivos = desde_teoria("cap-archivos", "curso/semana-07-python-cadenas-y-archivos/teoria.md")
cap_git = desde_teoria("cap-git", "curso/semana-git-control-de-versiones/teoria.md", lang_default="bash")
cap_poo1 = desde_teoria("cap-poo1", "curso/semana-08-python-poo-introduccion/teoria.md")
cap_poo2 = desde_teoria("cap-poo2", "curso/semana-09-python-poo-avanzado/teoria.md")
cap_modulos = desde_teoria("cap-modulos", "curso/semana-10-python-modulos-y-pip/teoria.md")


# ======================================================================
#  Capítulo Mapa de temas (escrito a mano)
# ======================================================================
cap_mapa = capitulo(
    "cap-mapa", "Mapa de temas del curso",
    p("Un vistazo a <strong>todo el recorrido</strong>, semana por semana. Cada semana tiene su teoría (en este libro), ejercicios, soluciones, tests y un programa interactivo."),

    h2("Fase 1 — Linux 🐧", "fase-linux"),
    tabla(
        ["Semana", "Temas"],
        [
            ["01 — Fundamentos", "Terminal, navegación, <code>ls cd pwd mkdir rm cp mv cat echo</code>, rutas, permisos"],
            ["02 — Intermedio", "<code>nano</code>, variables, scripts bash, <code>&gt; &gt;&gt; |</code>, <code>grep find ps kill chmod apt</code>, SSH"],
        ],
    ),

    h2("Fase 2 — Python básico 🐍", "fase-py-basico"),
    tabla(
        ["Semana", "Temas"],
        [
            ["03 — Introducción", "Variables, tipos, <code>print</code>, <code>input</code>, f-strings"],
            ["04 — Control de flujo", "<code>if/elif/else</code>, comparadores, lógicos, <code>while/for/range</code>, <code>break/continue</code>"],
            ["05 — Funciones", "<code>def</code>, parámetros, <code>return</code>, scope, <code>lambda</code>, recursión"],
            ["06 — Listas y colecciones", "Listas, tuplas, sets, diccionarios, comprensiones, <code>enumerate</code>, <code>zip</code>"],
            ["07 — Cadenas y archivos", "Métodos de string, slicing, <code>open</code>, CSV, <code>try/except</code>"],
        ],
    ),

    h2("Descanso — Git 🔀", "fase-git"),
    p("<strong>Git: Control de Versiones</strong> — <code>init</code>, <code>add</code>, <code>commit</code>, <code>log</code>, ramas (<code>branch/switch/merge</code>), GitHub, <code>push/pull/clone</code>, <code>.gitignore</code>. Pensada para hacerse después de la semana 7."),

    h2("Fase 3 — Python avanzado 🧬", "fase-py-avanzado"),
    tabla(
        ["Semana", "Temas"],
        [
            ["08 — POO introducción", "Clases, <code>__init__</code>, atributos, métodos, <code>self</code>, <code>__str__</code>, <code>__repr__</code>"],
            ["09 — POO avanzado", "Herencia, <code>super()</code>, polimorfismo, <code>@property</code>, clases abstractas (<code>abc</code>)"],
            ["10 — Módulos y pip", "<code>import</code>, módulos estándar, módulos propios, <code>pip</code>, <code>venv</code>, <code>requests</code>"],
        ],
    ),

    h2("Fase 4 — Proyectos 🏆", "fase-proyectos"),
    ul(
        "<strong>Semana 11 — Agenda del Entrenador:</strong> app de consola modular con persistencia en JSON.",
        "<strong>Semana 12 — Pokédex Web:</strong> web con Flask + PokéAPI.",
        "<strong>proyectos/pokedex-cli:</strong> Pokédex de consola con sprites ASCII y favoritos.",
        "<strong>proyectos/batalla-pokemon:</strong> simulador con tipos, PP y estados alterados.",
        "<strong>proyectos/agenda-entrenador</strong> y <strong>proyectos/pokedex-web:</strong> versiones pulidas.",
    ),
)


# ======================================================================
#  Capítulo de ayuda: tests, FAQ y glosario (escrito a mano)
# ======================================================================
cap_ayuda = capitulo(
    "cap-ayuda", "Ayuda: tests, preguntas frecuentes y glosario",
    h2("Cómo correr los tests", "tests"),
    p("Los <strong>tests</strong> te dicen si tus ejercicios están bien. Usamos <strong>pytest</strong>:"),
    code('''
        pytest                                        # todos los tests
        pytest curso/semana-04-python-control-de-flujo/   # una semana
        pytest curso/semana-05-python-funciones/test_ejercicios.py -v   # con detalle
    ''', lang="bash"),
    caja("""🟢 Verde = aprobado. 🔴 Rojo = revisá tu solución. Por defecto los tests
    prueban las soluciones; la Liga los corre contra TU <code>ejercicios.py</code> para
    darte EXP y decirte qué ejercicio falta.""", "nota"),

    h2("Preguntas frecuentes", "faq"),
    p("<strong>¿Por dónde empiezo?</strong> Por la Liga: <code>python aventura.py</code>. Después seguí la semana 01."),
    p("<strong>Me sale \"command not found: python\".</strong> Probá con <code>python3</code>."),
    p("<strong>Los tests me dan rojo. ¿Está mal?</strong> Significa que tu solución todavía no es correcta. Leé el error (está en español), corregí y volvé a probar. Es parte normal del aprendizaje."),
    p("<strong>¿Puedo ver las soluciones?</strong> Sí, están en <code>soluciones.py</code>. Pero intentá primero vos: mirar sin intentar es como usar un truco, ganás pero no aprendés."),
    p("<strong>¿Necesito internet?</strong> Solo para algunas partes (la semana 10, la Pokédex online y el autocompletado web). El resto funciona sin conexión."),

    h2("Glosario", "glosario"),
    tabla(
        ["Palabra", "Qué significa"],
        [
            ["Terminal / consola", "La ventana donde escribís comandos de texto."],
            ["Variable", 'Una "caja con nombre" donde guardás un dato.'],
            ["Tipo", "La clase de dato: int, float, str, bool..."],
            ["Función", "Un bloque de código con nombre que podés reusar."],
            ["Parámetro / argumento", "El dato que recibe / le pasás a una función."],
            ["Bucle", "Una estructura que repite código (while, for)."],
            ["Lista / diccionario", "Colecciones que guardan muchos datos."],
            ["Clase / objeto", "El molde / un individuo hecho con ese molde (POO)."],
            ["Test", "Un programa que revisa si tu código funciona bien."],
            ["EXP", "Puntos de experiencia que ganás en la Liga al pasar tests."],
            ["Commit", "Un punto de guardado de tu código en Git."],
            ["venv", "Entorno virtual: cajita aislada con las librerías del curso."],
        ],
    ),
)


# Lista final de capítulos, EN ORDEN DE LECTURA (la numeración es automática).
CAPITULOS = [
    cap_intro,
    cap_linux1, cap_linux2,                 # Linux (la base)
    cap_py_intro, cap_flujo, cap_func,      # Python básico
    cap_colecciones, cap_archivos,
    cap_git,                                # descanso: Git
    cap_poo1, cap_poo2, cap_modulos,        # Python avanzado
    cap_mapa, cap_ayuda,                    # mapa + ayuda
]
