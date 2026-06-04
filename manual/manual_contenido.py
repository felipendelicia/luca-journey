"""
manual_contenido.py — El contenido del libro, capítulo por capítulo.

Cada capítulo se arma con las funciones de manual_lib (p, h2, h3, code, caja, tabla...).
El contenido está escrito en HTML (no en Markdown), para tener control total del estilo.

Este libro cumple dos roles:
  1. Manual de cómo usar el proyecto/curso.
  2. Libro que enseña Linux y Python desde cero, con explicaciones detalladas y ejemplos.
"""

from manual_lib import (
    capitulo, h2, h3, p, ul, ol, code, caja, tabla, inline,
)


# ======================================================================
#  Capítulo 0 — Cómo usar este libro y el curso
# ======================================================================
cap_intro = capitulo(
    "cap-intro", "0. Cómo usar este libro y el curso",
    p("""¡Bienvenido! Este libro tiene <strong>dos caras</strong>. Por un lado es el
    <strong>manual</strong> del proyecto: te explica cómo instalarlo y cómo avanzar.
    Por otro lado es un <strong>libro completo</strong> que te enseña Linux y Python
    desde cero, con explicaciones paso a paso y muchos ejemplos."""),
    p("""Está pensado para alguien que <strong>nunca programó</strong>. No hace falta
    saber nada de antes. Vamos con calma, con temática Pokémon, y cada concepto se
    explica primero en palabras simples y después con código que podés copiar y probar. 🐍"""),

    h2("0.1. ¿Qué es este proyecto?", "que-es"),
    p("""Es un curso completo de <strong>Linux</strong> y <strong>Python</strong>,
    dividido en 12 semanas (más una semana de descanso de Git) y 4 proyectos finales.
    Cada concepto se explica con una analogía Pokémon, cada ejercicio usa Pokémon, y
    cada proyecto es algo que un Entrenador usaría de verdad."""),
    p("""Este libro acompaña al curso: podés leerlo de principio a fin como un libro,
    o usarlo como referencia para buscar un tema puntual cuando lo necesites."""),

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
        "📖 <strong>Leé</strong> la teoría de la semana (o el capítulo de este libro).",
        "✏️ <strong>Resolvé</strong> los ejercicios (escribí tu código donde dice <code># TU CÓDIGO ACÁ</code>).",
        '🧪 <strong>Probá</strong> con los tests (ver el <a href="#cap-16">capítulo de tests</a>).',
        "🎮 <strong>Jugá</strong> el <code>interactivo.py</code> de la semana.",
        "🏋️ <strong>Entrená</strong> esa semana en la Liga para ganar EXP.",
    ),
    caja("""<strong>Regla de oro:</strong> equivocarse es parte del juego. Escribí el
    código vos mismo, no copies y pegues: tipear te enseña. Y cuando algo no funcione,
    leé el mensaje de error con calma: casi siempre te dice qué pasó.""", "tip"),
)


# ======================================================================
#  Capítulo 1 — Tu primer programa
# ======================================================================
cap1 = capitulo(
    "cap-1", "1. Tu primer programa en Python",
    p("""<strong>Python</strong> es un lenguaje de programación: la forma en que le
    damos órdenes a la computadora. Un programa es una <strong>lista de instrucciones</strong>
    que la computadora ejecuta una por una, de arriba hacia abajo, en orden."""),
    p("""Python es famoso porque se lee casi como inglés y es ideal para aprender. Lo
    usan para webs, videojuegos, inteligencia artificial, análisis de datos y mucho más."""),
    caja("""Pensá en Python como el <strong>idioma de los Entrenadores</strong>. Vos
    escribís instrucciones (el código) y la computadora las obedece, como un Pokémon
    bien entrenado obedece a su dueño. Cuanto más claras las órdenes, mejor responde.""", "pokemon"),

    h2("1.1. print(): mostrar cosas en pantalla", "print"),
    p("""La instrucción <code>print()</code> muestra texto en la pantalla. Es lo primero
    que hace todo programador. Lo que va entre las comillas se llama <strong>cadena de
    texto</strong> (o <em>string</em>):"""),
    code('''
        print("¡Hola, mundo Pokémon!")
        print("Elegí a Pikachu como inicial")
    '''),
    p("Cuando corrés ese programa, en la pantalla aparece:"),
    code('''
        ¡Hola, mundo Pokémon!
        Elegí a Pikachu como inicial
    ''', lang="bash"),
    h3("Imprimir varias cosas juntas"),
    p("""Podés pasarle a <code>print()</code> varias cosas separadas por comas. Las
    muestra en la misma línea, separadas por un espacio:"""),
    code('''
        print("Mi Pokémon es", "Charizard")   # Mi Pokémon es Charizard
        print("Nivel:", 50)                    # Nivel: 50
    '''),
    h3("Saltos de línea y separadores"),
    p("""Dentro de un texto, <code>\\n</code> es un <strong>salto de línea</strong> y
    <code>\\t</code> es una <strong>tabulación</strong> (un espacio grande). También
    podés cambiar el separador con <code>sep</code> y el final con <code>end</code>:"""),
    code('''
        print("Línea 1\\nLínea 2")        # imprime dos líneas
        print("Pika", "chu", sep="-")     # Pika-chu
        print("Hola", end=" ")            # no salta de línea al final
        print("mundo")                    # ...así "Hola mundo" queda junto
    '''),

    h2("1.2. El REPL: probar al instante", "repl"),
    p("""Si escribís <code>python3</code> en la terminal, se abre el <strong>REPL</strong>
    (modo interactivo): escribís una línea, apretás Enter, y ves el resultado al toque.
    Es ideal para experimentar sin crear un archivo. El símbolo <code>&gt;&gt;&gt;</code>
    es su <em>prompt</em> (te indica que espera tu instrucción):"""),
    code('''
        >>> 2 + 2
        4
        >>> "Pika" + "chu"
        'Pikachu'
        >>> print("Hola")
        Hola
    '''),
    p("""Para salir del REPL escribís <code>exit()</code> y Enter. Para programas de
    verdad (que se guardan y reusan), escribís el código en un archivo terminado en
    <code>.py</code> y lo corrés así:"""),
    code("python3 mi_programa.py", lang="bash"),
    caja("""En muchos sistemas el comando es <code>python3</code>; en otros,
    <code>python</code>. Si uno no funciona, probá el otro.""", "nota"),

    h2("1.3. Comentarios", "comentarios"),
    p("""Un <strong>comentario</strong> es texto que Python <strong>ignora</strong>
    por completo. Sirve para explicar tu código (a otros y a tu yo del futuro).
    Empieza con el símbolo <code>#</code>:"""),
    code('''
        # Esto es un comentario: Python no lo ejecuta.
        print("Hola")        # también se puede comentar al final de una línea

        # Los comentarios sirven para:
        # - explicar qué hace una parte del código
        # - dejar notas o recordatorios
        # - "apagar" temporalmente una línea sin borrarla
    '''),
    caja("""Comentar bien tu código es de buena programadora. Pero ojo: no comentes lo
    obvio (<code>x = x + 1  # suma 1 a x</code> no aporta). Comentá el <strong>porqué</strong>,
    no el qué.""", "tip"),

    h2("1.4. Cuando algo sale mal: los errores", "errores-intro"),
    p("""Equivocarse es normal y constante al programar. Si escribís algo que Python no
    entiende, te muestra un <strong>error</strong>. No te asustes: el error casi siempre
    te dice qué pasó y en qué línea. Por ejemplo, si te olvidás una comilla:"""),
    code('''
        print("Hola)
        # SyntaxError: unterminated string literal (detected at line 1)
    '''),
    p("""Leé la última línea del error: dice el <strong>tipo</strong> de error
    (<code>SyntaxError</code>) y una pista. Con el tiempo, leer errores se vuelve natural."""),
    caja("""<strong>Truco profesional:</strong> si no entendés un error, copiá el
    mensaje exacto y pegalo en un buscador. El 99% de las veces, alguien ya lo tuvo y
    está explicado. Esto es la mitad de programar.""", "tip"),
)


# ======================================================================
#  Capítulo 2 — Variables y tipos
# ======================================================================
cap2 = capitulo(
    "cap-2", "2. Variables y tipos de datos",
    h2("2.1. Variables", "variables"),
    p("""Una <strong>variable</strong> guarda un dato con un nombre, para poder usarlo
    después. Es como una <strong>Pokéball</strong>: adentro guardás algo y le ponés una
    etiqueta con un nombre. El símbolo <code>=</code> se llama <strong>asignación</strong>:
    "guardá lo de la derecha en el nombre de la izquierda"."""),
    code('''
        nombre = "Pikachu"      # guardamos un texto en la variable 'nombre'
        nivel = 25              # guardamos un número en la variable 'nivel'

        print(nombre)           # Pikachu
        print(nivel)            # 25
    '''),
    h3("Las variables se pueden cambiar"),
    p("""Podés cambiar el valor de una variable cuando quieras: el nuevo valor reemplaza
    al viejo. Por eso se llaman "variables" (varían):"""),
    code('''
        nivel = 25
        print(nivel)    # 25
        nivel = 26      # ahora vale otra cosa
        print(nivel)    # 26

        nivel = nivel + 1   # tomá el valor actual, sumale 1, y volvé a guardarlo
        print(nivel)        # 27
    '''),
    h3("Reglas para los nombres"),
    p("Los nombres de variables tienen algunas reglas y costumbres:"),
    ul(
        "Solo letras, números y guión bajo <code>_</code>. <strong>No</strong> pueden empezar con número.",
        "No llevan espacios: usá guión bajo para separar palabras (<code>pokemon_inicial</code>).",
        "Distinguen mayúsculas: <code>nivel</code> y <code>Nivel</code> son variables distintas.",
        "Elegí nombres que se entiendan: <code>nivel</code> es mejor que <code>n</code>.",
    ),
    code('''
        pokemon_inicial = "Charmander"   # ✅ bien
        hp_maximo = 100                  # ✅ bien
        # 3pokemon = "no"                # ❌ mal: no puede empezar con número
        # mi pokemon = "no"              # ❌ mal: no puede tener espacios
    '''),

    h2("2.2. Los cuatro tipos básicos", "tipos"),
    p("""Cada dato en Python tiene un <strong>tipo</strong>. El tipo define qué se puede
    hacer con ese dato. Los cuatro tipos que más vas a usar al empezar son:"""),
    tabla(
        ["Tipo", "Qué es", "Ejemplos"],
        [
            ["<code>int</code>", "Número entero (sin decimales)", "<code>25</code>, <code>0</code>, <code>-7</code>"],
            ["<code>float</code>", "Número con decimales", "<code>6.0</code>, <code>3.14</code>, <code>-0.5</code>"],
            ["<code>str</code>", "Texto, siempre entre comillas", '<code>"Pikachu"</code>, <code>"a"</code>, <code>""</code>'],
            ["<code>bool</code>", "Verdadero o falso", "<code>True</code>, <code>False</code>"],
        ],
    ),
    code('''
        nivel = 25            # int
        peso = 6.0            # float (¡el punto lo hace decimal!)
        nombre = "Pikachu"    # str (entre comillas)
        es_legendario = False # bool (con mayúscula: True o False)
    '''),
    p("Para ver el tipo de cualquier valor, usás la función <code>type()</code>:"),
    code('''
        print(type(25))         # <class 'int'>
        print(type(6.0))        # <class 'float'>
        print(type("Pikachu"))  # <class 'str'>
        print(type(True))       # <class 'bool'>
    '''),
    caja("""Cuidado con un error común: <code>"25"</code> (con comillas) es <strong>texto</strong>,
    no un número. <code>25 + 5</code> da <code>30</code>, pero <code>"25" + "5"</code> da
    <code>"255"</code> (pega los textos). El <a href="#cap-5">capítulo de input</a> explica cómo convertir entre tipos.""", "cuidado"),

    h2("2.3. f-strings: armar texto con variables", "fstrings"),
    p("""Muchas veces querés mezclar texto con el valor de tus variables. La forma más
    cómoda y moderna es el <strong>f-string</strong>: ponés una <code>f</code> antes de
    las comillas y metés las variables entre <code>{llaves}</code>:"""),
    code('''
        nombre = "Pikachu"
        nivel = 25
        print(f"Mi {nombre} es nivel {nivel}")   # Mi Pikachu es nivel 25
    '''),
    p("""Adentro de las llaves podés poner hasta operaciones; Python las calcula:"""),
    code('''
        hp = 100
        print(f"{nombre} tiene {hp} HP")              # Pikachu tiene 100 HP
        print(f"Al subir, será nivel {nivel + 1}")    # Al subir, será nivel 26
    '''),
    h3("Dar formato a los números"),
    p("""Para mostrar decimales con cierta cantidad de cifras, usás <code>:.2f</code>
    (dos decimales). Útil para porcentajes, precios, etc.:"""),
    code('''
        porcentaje = 2 / 3
        print(f"Victorias: {porcentaje:.2f}")   # Victorias: 0.67
    '''),
    caja("""Los f-strings son la forma recomendada de armar texto. Antes se usaban otras
    (con <code>+</code> o con <code>.format()</code>), pero el f-string es más claro y
    corto. ¡Usalo siempre!""", "clave"),
)


# ======================================================================
#  Capítulo 3 — Operadores
# ======================================================================
cap3 = capitulo(
    "cap-3", "3. Operadores",
    p("""Los <strong>operadores</strong> son símbolos que combinan o comparan valores.
    Ya usaste uno: el <code>=</code> de asignación. Ahora vemos los de matemática,
    comparación y lógica."""),

    h2("3.1. Operadores aritméticos", "aritmeticos"),
    p("Sirven para hacer cuentas:"),
    tabla(
        ["Operador", "Hace", "Ejemplo", "Resultado"],
        [
            ["<code>+</code>", "Suma", "<code>10 + 5</code>", "15"],
            ["<code>-</code>", "Resta", "<code>10 - 5</code>", "5"],
            ["<code>*</code>", "Multiplicación", "<code>10 * 5</code>", "50"],
            ["<code>/</code>", "División (da decimal)", "<code>10 / 4</code>", "2.5"],
            ["<code>//</code>", "División entera", "<code>10 // 4</code>", "2"],
            ["<code>%</code>", "Resto (módulo)", "<code>10 % 4</code>", "2"],
            ["<code>**</code>", "Potencia", "<code>2 ** 3</code>", "8"],
        ],
    ),
    h3("/ contra //"),
    p("""La división normal <code>/</code> siempre da un <code>float</code> (decimal),
    aunque dé exacto. La división entera <code>//</code> descarta los decimales:"""),
    code('''
        print(10 / 2)    # 5.0   (¡ojo, con punto: es float!)
        print(10 / 3)    # 3.3333333333333335
        print(10 // 3)   # 3     (entera: tira la parte decimal)
    '''),
    h3("El módulo % es más útil de lo que parece"),
    p("""El <strong>módulo</strong> da el <em>resto</em> de una división. Sirve, por
    ejemplo, para saber si un número es par (resto 0 al dividir por 2):"""),
    code('''
        print(10 % 3)    # 1   (10 = 3*3 + 1, sobra 1)
        print(8 % 2)     # 0   (8 es par: no sobra nada)
        print(7 % 2)     # 1   (7 es impar: sobra 1)
    '''),
    h3("El orden de las operaciones"),
    p("""Python respeta el orden matemático: primero <code>**</code>, después
    <code>*</code>, <code>/</code>, <code>//</code>, <code>%</code>, y al final
    <code>+</code> y <code>-</code>. Usá paréntesis para forzar el orden que querés:"""),
    code('''
        print(2 + 3 * 4)      # 14  (primero 3*4=12, después +2)
        print((2 + 3) * 4)    # 20  (los paréntesis van primero)
    '''),

    h2("3.2. Operadores de comparación", "comparacion"),
    p("""Comparan dos valores y devuelven un <strong>bool</strong>
    (<code>True</code> o <code>False</code>). Son la base de las decisiones (ver <a href="#cap-6">condicionales</a>):"""),
    tabla(
        ["Operador", "Significa", "Ejemplo", "Resultado"],
        [
            ["<code>==</code>", "igual a", "<code>25 == 25</code>", "True"],
            ["<code>!=</code>", "distinto de", "<code>25 != 30</code>", "True"],
            ["<code>&gt;</code>", "mayor que", "<code>30 &gt; 25</code>", "True"],
            ["<code>&lt;</code>", "menor que", "<code>30 &lt; 25</code>", "False"],
            ["<code>&gt;=</code>", "mayor o igual", "<code>25 &gt;= 25</code>", "True"],
            ["<code>&lt;=</code>", "menor o igual", "<code>20 &lt;= 25</code>", "True"],
        ],
    ),
    caja("""<strong>El error más común de principiante:</strong> confundir <code>=</code>
    con <code>==</code>. Un solo <code>=</code> <em>asigna</em> (guarda en una variable);
    el doble <code>==</code> <em>compara</em>. <code>nivel = 25</code> guarda; <code>nivel == 25</code>
    pregunta "¿son iguales?".""", "cuidado"),

    h2("3.3. Operadores lógicos: and, or, not", "logicos"),
    p("""Combinan condiciones. <code>and</code> es verdadero si <strong>ambas</strong>
    son verdaderas; <code>or</code> si <strong>al menos una</strong> lo es;
    <code>not</code> <strong>invierte</strong> (lo verdadero lo hace falso y viceversa)."""),
    tabla(
        ["Expresión", "Resultado"],
        [
            ["<code>True and True</code>", "True"],
            ["<code>True and False</code>", "False"],
            ["<code>True or False</code>", "True"],
            ["<code>False or False</code>", "False"],
            ["<code>not True</code>", "False"],
        ],
    ),
    code('''
        nivel = 30
        tipo = "Fuego"

        # Evoluciona si tiene nivel suficiente Y es de Fuego:
        print(nivel >= 25 and tipo == "Fuego")   # True

        # Es fuerte si es legendario O tiene nivel 100:
        es_legendario = False
        print(es_legendario or nivel == 100)      # False

        # Puede pelear si NO está debilitado:
        debilitado = False
        print(not debilitado)                     # True
    '''),

    h2("3.4. Operadores con texto", "operadores-texto"),
    p("""El <code>+</code> también funciona con strings: los <strong>pega</strong>
    (concatena). Y el <code>*</code> repite un texto:"""),
    code('''
        print("Pika" + "chu")     # Pikachu
        print("na" * 4)           # nananana
        print("=" * 20)           # ====================  (útil para separadores)
    '''),
)


# ======================================================================
#  Capítulo 4 — Strings
# ======================================================================
cap4 = capitulo(
    "cap-4", "4. Cadenas de texto (strings)",
    p("""Un <strong>string</strong> es texto, siempre entre comillas (simples
    <code>'...'</code> o dobles <code>"..."</code>, da igual). Es uno de los tipos que
    más vas a usar: nombres, mensajes, datos de archivos, todo es texto."""),
    code('''
        nombre = "Pikachu"
        frase = 'Yo elijo a Pikachu'
        vacio = ""                  # un string vacío (sin nada adentro)
    '''),

    h2("4.1. Largo, búsqueda e índices", "string-basico"),
    p("""Con <code>len()</code> sabés cuántos caracteres tiene. Con <code>in</code>
    preguntás si un texto está adentro de otro. Y con corchetes <code>[ ]</code> accedés
    a un carácter por su <strong>posición</strong> (que empieza en 0):"""),
    code('''
        nombre = "Pikachu"
        print(len(nombre))        # 7  (tiene 7 letras)
        print("ka" in nombre)     # True  (¿"ka" está adentro?)
        print(nombre[0])          # P    (el primer carácter, posición 0)
        print(nombre[1])          # i
        print(nombre[-1])         # u    (el último, contando desde atrás)
    '''),
    caja("""<strong>Los índices empiezan en 0</strong>, no en 1. Entonces, en
    <code>"Pikachu"</code>, la <code>P</code> está en la posición 0, la <code>i</code>
    en la 1, etc. Y <code>[-1]</code> es el último carácter. Esto vale también para
    listas (ver <a href="#cap-9">listas y tuplas</a>).""", "clave"),

    h2("4.2. Métodos de strings", "string-metodos"),
    p("""Un <strong>método</strong> es una acción que un dato sabe hacer. Se llama con
    un punto: <code>texto.metodo()</code>. Los strings tienen muchos. Importante: los
    métodos <strong>no cambian</strong> el original, devuelven uno <strong>nuevo</strong>:"""),
    code('''
        nombre = "  Pikachu  "
        print(nombre.upper())        # "  PIKACHU  "  (mayúsculas)
        print(nombre.lower())        # "  pikachu  "  (minúsculas)
        print(nombre.strip())        # "Pikachu"      (saca espacios de los bordes)
        print("pikachu".capitalize())     # "Pikachu"   (primera letra en mayúscula)
        print("Pikachu".replace("a", "@")) # "Pik@chu"  (reemplaza)
        print("Pikachu".startswith("Pika")) # True
        print("Pikachu".endswith("chu"))     # True
        print("Pikachu".count("a"))          # 1   (cuántas veces aparece "a")
    '''),
    tabla(
        ["Método", "Qué hace"],
        [
            ["<code>.upper()</code> / <code>.lower()</code>", "A mayúsculas / minúsculas"],
            ["<code>.strip()</code>", "Saca espacios de los bordes"],
            ["<code>.capitalize()</code>", "Primera letra en mayúscula"],
            ["<code>.replace(a, b)</code>", "Cambia todas las apariciones de a por b"],
            ["<code>.startswith(x)</code> / <code>.endswith(x)</code>", "¿Empieza / termina con x?"],
            ["<code>.count(x)</code>", "Cuántas veces aparece x"],
            ["<code>.split(sep)</code> / <code>sep.join(lista)</code>", "Separar / unir (abajo)"],
        ],
    ),

    h2("4.3. split y join", "split-join"),
    p("""<code>split</code> <strong>parte</strong> un texto en una lista usando un
    separador. <code>join</code> hace lo contrario: <strong>une</strong> una lista en
    un texto. Son clave para trabajar con archivos CSV (ver <a href="#cap-11">archivos</a>):"""),
    code('''
        linea = "Pikachu,Electrico,25"
        partes = linea.split(",")
        print(partes)     # ['Pikachu', 'Electrico', '25']

        datos = ["Charizard", "Fuego", "50"]
        linea = ",".join(datos)
        print(linea)      # "Charizard,Fuego,50"
    '''),

    h2("4.4. Slicing: rebanar texto", "slicing"),
    p("""El <strong>slicing</strong> saca una "rebanada" del texto con
    <code>[inicio:fin]</code>. Toma desde <code>inicio</code> hasta <code>fin</code>,
    pero <strong>sin incluir</strong> el <code>fin</code>:"""),
    code('''
        texto = "Pikachu"
        #        0123456    (posiciones)

        print(texto[0:4])    # "Pika"     (del 0 al 3)
        print(texto[4:])     # "chu"      (del 4 hasta el final)
        print(texto[:4])     # "Pika"     (del principio al 3)
        print(texto[-3:])    # "chu"      (los últimos 3)
        print(texto[::-1])   # "uhcakiP"  (todo, pero al revés)
    '''),
    caja("""<strong>Los strings son inmutables:</strong> no podés cambiar una letra con
    <code>texto[0] = "X"</code> (da error). Si querés un texto distinto, creás uno nuevo
    (por ejemplo con <code>.replace()</code>).""", "cuidado"),
)


# ======================================================================
#  Capítulo 5 — input
# ======================================================================
cap5 = capitulo(
    "cap-5", "5. Pedir datos al usuario: input()",
    p("""Hasta ahora tus programas mostraban cosas. Con <code>input()</code> tu programa
    puede <strong>pedirle datos a quien lo usa</strong>. Cuando Python llega a un
    <code>input()</code>, <strong>se detiene</strong> y espera que la persona escriba algo
    y apriete Enter. Lo que escribió queda guardado:"""),
    code('''
        nombre = input("¿Cómo se llama tu Pokémon? ")
        print(f"¡Hola, {nombre}!")
    '''),
    p("""Si la persona escribe <code>Pikachu</code> y aprieta Enter, el programa
    muestra <code>¡Hola, Pikachu!</code>. El texto que le pasás a <code>input()</code>
    es la <strong>pregunta</strong> que se ve en pantalla."""),

    h2("5.1. input() siempre devuelve texto", "input-texto"),
    caja("""<strong>¡MUY IMPORTANTE!</strong> <code>input()</code> SIEMPRE devuelve un
    <code>str</code> (texto), aunque la persona escriba un número. Por eso, si querés
    hacer cuentas, primero tenés que <strong>convertirlo</strong> a número.""", "cuidado"),
    p("Mirá qué pasa si no convertís:"),
    code('''
        edad = input("¿Tu edad? ")    # la persona escribe 10
        print(edad + 5)               # ❌ ERROR: no se puede sumar texto + número
    '''),

    h2("5.2. Conversión de tipos", "conversion"),
    p("""Para convertir entre tipos usás funciones con el nombre del tipo:
    <code>int()</code> (a entero), <code>float()</code> (a decimal) y <code>str()</code>
    (a texto):"""),
    code('''
        edad_texto = input("¿Tu edad? ")   # esto es str, ej "10"
        edad = int(edad_texto)             # ahora es int: 10
        print(edad + 5)                    # 15  ✅

        # Forma compacta, muy común: pedir y convertir en una sola línea
        nivel = int(input("¿Nivel de tu Pokémon? "))
        print(f"Cuando suba, será nivel {nivel + 1}")
    '''),
    tabla(
        ["Función", "Convierte a", "Ejemplo", "Resultado"],
        [
            ["<code>int(x)</code>", "entero", '<code>int("25")</code>', "25"],
            ["<code>float(x)</code>", "decimal", '<code>float("6.5")</code>', "6.5"],
            ["<code>str(x)</code>", "texto", "<code>str(25)</code>", '"25"'],
        ],
    ),
    h3("Un programa completo de ejemplo"),
    code('''
        print("=== Registro de Entrenador ===")
        nombre = input("Tu nombre: ")
        ciudad = input("Tu ciudad: ")
        edad = int(input("Tu edad: "))

        print(f"\\nEntrenador {nombre}, de {ciudad}.")
        print(f"En 5 años vas a tener {edad + 5} años.")
    '''),
    caja("""Si la persona escribe algo que no es un número (como "diez") y vos hacés
    <code>int(...)</code>, Python tira un <code>ValueError</code>. Más adelante, en el
    <a href="#cap-11">capítulo de archivos y errores</a>, vas a aprender a manejar ese
    error con <code>try</code>/<code>except</code>.""", "nota"),
)


# ======================================================================
#  Capítulo 6 — Condicionales
# ======================================================================
cap6 = capitulo(
    "cap-6", "6. Condicionales: if / elif / else",
    p("""Hasta ahora tus programas corrían en línea recta. Con los <strong>condicionales</strong>,
    tu programa puede <strong>tomar decisiones</strong>: hacer una cosa u otra según lo
    que pase. Es como en una batalla: <em>"si el rival es de Agua, uso un ataque Eléctrico"</em>."""),

    h2("6.1. if: hacer algo solo si...", "if"),
    p("""<code>if</code> (si, en inglés) ejecuta un bloque de código <strong>solo si</strong>
    una condición es verdadera. La condición es una comparación que da
    <code>True</code> o <code>False</code>:"""),
    code('''
        nivel = 30

        if nivel >= 25:
            print("¡Tu Pokémon puede evolucionar!")
    '''),
    caja("""<strong>La indentación (sangría) importa y es obligatoria.</strong> El código
    "adentro" del <code>if</code> va con <strong>4 espacios</strong> de sangría. Python
    usa esa sangría para saber qué está adentro y qué afuera del <code>if</code>. No es
    decoración: si te equivocás con la sangría, da error.""", "clave"),

    h2("6.2. else: el 'si no'", "else"),
    p("""<code>else</code> (si no) define qué hacer cuando la condición del <code>if</code>
    <strong>no</strong> se cumple:"""),
    code('''
        hp = 0

        if hp > 0:
            print("Tu Pokémon sigue en pie")
        else:
            print("Tu Pokémon se debilitó 💀")
    '''),

    h2("6.3. elif: más caminos", "elif"),
    p("""Con <code>elif</code> (else if, "si no, si...") agregás más condiciones.
    Python las revisa <strong>de arriba hacia abajo</strong> y entra en la
    <strong>primera</strong> que sea verdadera; el resto las ignora:"""),
    code('''
        hp = 40

        if hp > 70:
            print("Tu Pokémon está sano 💚")
        elif hp > 30:
            print("Tu Pokémon está cansado 💛")
        elif hp > 0:
            print("¡Tu Pokémon está grave! ❤️")
        else:
            print("Tu Pokémon se debilitó 💀")
    '''),
    p("""Como <code>hp</code> vale 40, no entra en el primer <code>if</code> (40 no es
    mayor a 70), pero sí en el primer <code>elif</code> (40 es mayor a 30), así que
    imprime "cansado" y se saltea los demás."""),

    h2("6.4. Combinar condiciones", "if-logicos"),
    p("""Podés usar <code>and</code>, <code>or</code> y <code>not</code> (ver <a href="#cap-3">operadores</a>)
    dentro de un <code>if</code> para decisiones más ricas:"""),
    code('''
        nivel = 30
        tipo = "Fuego"

        if nivel >= 25 and tipo == "Fuego":
            print("¡Charmeleon evoluciona a Charizard! 🔥")

        edad = 8
        if edad < 10 or edad > 60:
            print("Precio especial")
    '''),
    h3("Condicionales anidados"),
    p("Podés poner un <code>if</code> adentro de otro (anidado). Cada nivel suma 4 espacios más de sangría:"),
    code('''
        tiene_medalla = True
        nivel = 50

        if tiene_medalla:
            if nivel >= 40:
                print("Podés entrar a la Liga Pokémon")
            else:
                print("Tenés la medalla, pero te falta nivel")
        else:
            print("Primero conseguí una medalla")
    '''),
    caja("""Errores típicos: (1) usar <code>=</code> en vez de <code>==</code> en la
    condición; (2) olvidar los dos puntos <code>:</code> al final del <code>if</code>;
    (3) mezclar espacios y tabs en la sangría. Si algo no anda, revisá esas tres cosas.""", "cuidado"),
)


# ======================================================================
#  Capítulo 7 — Bucles
# ======================================================================
cap7 = capitulo(
    "cap-7", "7. Bucles: repetir cosas (while y for)",
    p("""Un <strong>bucle</strong> (o ciclo) repite un bloque de código varias veces.
    Sin bucles, para atacar 5 veces tendrías que escribir <code>print()</code> cinco
    veces. Con bucles, lo escribís una vez y le decís cuántas veces repetir."""),

    h2("7.1. while: repetir mientras...", "while"),
    p("""<code>while</code> (mientras) repite un bloque <strong>mientras</strong> una
    condición sea verdadera. Antes de cada vuelta revisa la condición; cuando se vuelve
    falsa, el bucle termina:"""),
    code('''
        hp_rival = 100

        while hp_rival > 0:
            print(f"Atacás. HP del rival: {hp_rival}")
            hp_rival = hp_rival - 20      # ¡importante! algo tiene que cambiar

        print("¡Ganaste la batalla! 🏆")
    '''),
    p("Eso imprime el HP bajando de 100 a 80, 60, 40, 20, y cuando llega a 0 corta y felicita."),
    caja("""<strong>¡Cuidado con los bucles infinitos!</strong> Si la condición nunca se
    vuelve falsa, el programa no termina nunca (se "cuelga"). Asegurate de que algo
    cambie adentro del <code>while</code> que, tarde o temprano, haga falsa la condición.
    Si quedás en un bucle infinito, cortalo con <strong>Ctrl + C</strong>.""", "cuidado"),
    h3("Acumuladores y contadores"),
    p("""Un patrón muy común: una variable que arranca en un valor y se va modificando
    en cada vuelta. Un <em>contador</em> cuenta; un <em>acumulador</em> suma:"""),
    code('''
        total = 0          # acumulador
        numero = 1
        while numero <= 5:
            total = total + numero    # le voy sumando
            numero = numero + 1
        print(total)       # 15  (1+2+3+4+5)
    '''),

    h2("7.2. for: recorrer una secuencia", "for"),
    p("""<code>for</code> (para cada) recorre los elementos de una secuencia, uno por
    uno. Es ideal cuando sabés sobre qué querés repetir (una lista, un texto, un rango
    de números):"""),
    code('''
        equipo = ["Pikachu", "Charizard", "Snorlax"]
        for pokemon in equipo:
            print(f"Tengo a {pokemon}")
        # Tengo a Pikachu
        # Tengo a Charizard
        # Tengo a Snorlax

        # También se puede recorrer un texto, letra por letra:
        for letra in "Pika":
            print(letra)     # P, i, k, a (cada una en su línea)
    '''),
    h3("range(): generar números"),
    p("""<code>range()</code> genera una secuencia de números, perfecta para repetir N
    veces. Ojo: el número final <strong>no</strong> se incluye:"""),
    code('''
        for i in range(5):           # 0, 1, 2, 3, 4
            print(f"Pokéball número {i + 1}")

        for nivel in range(1, 6):    # 1, 2, 3, 4, 5  (del 1 al 5)
            print(nivel)

        for n in range(0, 11, 2):    # 0, 2, 4, 6, 8, 10  (de 2 en 2)
            print(n)
    '''),
    tabla(
        ["Forma", "Genera"],
        [
            ["<code>range(5)</code>", "0, 1, 2, 3, 4"],
            ["<code>range(1, 6)</code>", "1, 2, 3, 4, 5"],
            ["<code>range(0, 11, 2)</code>", "0, 2, 4, 6, 8, 10"],
        ],
    ),

    h2("7.3. break y continue", "break-continue"),
    p("""Dos instrucciones para controlar el bucle desde adentro: <code>break</code>
    <strong>corta</strong> el bucle por completo; <code>continue</code> <strong>saltea</strong>
    el resto de la vuelta actual y pasa a la siguiente:"""),
    code('''
        equipo = ["Pikachu", "Mewtwo", "Snorlax"]

        # break: dejamos de buscar apenas encontramos a Mewtwo
        for pokemon in equipo:
            if pokemon == "Mewtwo":
                print("¡Encontramos a Mewtwo!")
                break
            print(f"{pokemon} no es Mewtwo, sigo buscando...")
    '''),
    code('''
        # continue: salteamos a los Pokémon debilitados
        equipo_hp = [100, 0, 50]
        for hp in equipo_hp:
            if hp == 0:
                continue          # saltea este y va al siguiente
            print(f"Este Pokémon tiene {hp} HP y puede pelear")
    '''),

    h2("7.4. Bucles anidados", "for-anidado"),
    p("""Podés poner un bucle adentro de otro. Por cada vuelta del de afuera, el de
    adentro hace todas sus vueltas. Útil para combinaciones, tablas, grillas:"""),
    code('''
        for entrenador in ["Ash", "Misty"]:
            for pokemon in ["Pikachu", "Staryu"]:
                print(f"{entrenador} podría usar a {pokemon}")
    '''),
)


# ======================================================================
#  Capítulo 8 — Funciones
# ======================================================================
cap8 = capitulo(
    "cap-8", "8. Funciones",
    p("""Una <strong>función</strong> es un bloque de código con nombre que escribís
    <strong>una vez</strong> y podés usar <strong>muchas veces</strong>. Sirve para no
    repetirte y para organizar tu programa en piezas con sentido."""),
    caja("""Es como un ataque que tu Pokémon <strong>aprende una vez</strong> y después
    usa mil veces. No reaprende "Impactrueno" en cada batalla: lo sabe, le pone un
    nombre, y lo invoca cuando quiere. ⚡""", "pokemon"),

    h2("8.1. Definir y llamar una función", "def"),
    p("""Se define con <code>def</code> (de <em>define</em>), un nombre, paréntesis y
    dos puntos. El cuerpo va indentado. <strong>Definir</strong> no la ejecuta; para
    ejecutarla hay que <strong>llamarla</strong> por su nombre con paréntesis:"""),
    code('''
        def saludar():                  # definición
            print("¡Hola, Entrenador!")

        saludar()    # llamada -> imprime el saludo
        saludar()    # la usamos de nuevo, gratis
    '''),

    h2("8.2. Parámetros: pasarle datos", "parametros"),
    p("""Un <strong>parámetro</strong> es un dato que la función recibe para trabajar.
    Va entre los paréntesis. Cuando llamás la función, le pasás el valor (el
    <strong>argumento</strong>):"""),
    code('''
        def saludar(nombre):
            print(f"¡Hola, {nombre}!")

        saludar("Ash")      # ¡Hola, Ash!
        saludar("Misty")    # ¡Hola, Misty!

        # Varios parámetros, separados por comas:
        def presentar(nombre, tipo):
            print(f"{nombre} es de tipo {tipo}")

        presentar("Pikachu", "Eléctrico")
    '''),

    h2("8.3. return: devolver un resultado", "return"),
    p("""<code>return</code> hace que la función <strong>devuelva</strong> un valor para
    usarlo después. Es la diferencia entre una función que solo "muestra" y una que
    "calcula y entrega":"""),
    code('''
        def calcular_dano(ataque, defensa):
            return ataque - defensa

        resultado = calcular_dano(50, 20)   # guardamos lo que devuelve
        print(resultado)                    # 30
        print(calcular_dano(80, 30))        # 50  (también se puede usar directo)
    '''),
    caja("""<strong>print vs return:</strong> <code>print</code> solo MUESTRA algo en
    pantalla; <code>return</code> DEVUELVE un valor que tu programa puede seguir usando
    (guardar, sumar, comparar...). Si querés <em>usar</em> el resultado después, usá
    <code>return</code>. Apenas Python ejecuta un <code>return</code>, sale de la función.""", "clave"),
    h3("Devolver varios valores"),
    p('Una función puede devolver más de un valor (en realidad devuelve una tupla, ver <a href="#cap-9">listas y tuplas</a>):'),
    code('''
        def stats(nivel):
            hp = nivel * 3
            ataque = nivel * 2
            return hp, ataque

        vida, ataque = stats(10)     # 30, 20
        print(vida, ataque)          # 30 20
    '''),

    h2("8.4. Valores por defecto", "defecto"),
    p("""Podés darle a un parámetro un valor por defecto, que se usa si al llamar no
    pasás ese dato:"""),
    code('''
        def atacar(nombre, dano=10):       # dano vale 10 si no se especifica
            print(f"{nombre} hizo {dano} de daño")

        atacar("Pikachu")          # Pikachu hizo 10 de daño  (usa el default)
        atacar("Charizard", 35)    # Charizard hizo 35 de daño (lo pisamos)
    '''),

    h2("8.5. Scope: dónde vive cada variable", "scope"),
    p("""El <strong>scope</strong> (alcance) es la zona donde una variable existe. Una
    variable creada <strong>adentro</strong> de una función solo existe ahí adentro
    (es <em>local</em>). Afuera no se la ve:"""),
    code('''
        def entrenar():
            secreto = "técnica oculta"    # variable LOCAL
            print(secreto)

        entrenar()
        # print(secreto)   # ❌ ERROR: 'secreto' no existe afuera de la función
    '''),

    h2("8.6. Funciones lambda", "lambda"),
    p("""Una <strong>lambda</strong> es una función chiquita de una sola línea, sin
    nombre. Útil para cosas simples. Su forma es <code>lambda parámetros: expresión</code>:"""),
    code('''
        doble = lambda x: x * 2
        print(doble(5))      # 10

        sumar = lambda a, b: a + b
        print(sumar(3, 4))   # 7
    '''),

    h2("8.7. Recursión", "recursion"),
    p("""La <strong>recursión</strong> es cuando una función se llama a sí misma para
    resolver un problema más chico. Siempre necesita un <strong>caso base</strong>: una
    condición que la frene (si no, se llama infinitamente y revienta):"""),
    code('''
        def factorial(n):
            if n <= 1:                    # caso base: frena acá
                return 1
            return n * factorial(n - 1)   # caso recursivo: se llama con n-1

        print(factorial(5))    # 120  (5*4*3*2*1)
    '''),
    p("""Es como muñecas rusas: cada <code>factorial</code> abre otra más chica, hasta
    llegar a la más chiquita (el caso base), y ahí se arma el resultado para arriba."""),
)


# ======================================================================
#  Capítulo 9 — Listas y tuplas
# ======================================================================
cap9 = capitulo(
    "cap-9", "9. Listas y tuplas",
    p("""Hasta ahora cada variable guardaba <strong>un</strong> dato. Una <strong>lista</strong>
    guarda <strong>muchos</strong> datos juntos, en orden, bajo un solo nombre. Es como
    tu equipo Pokémon. Se escribe entre corchetes <code>[ ]</code>, con los elementos
    separados por comas:"""),
    code('''
        equipo = ["Pikachu", "Charizard", "Snorlax"]
        niveles = [25, 50, 40]
        vacia = []                     # una lista vacía
        mezcla = ["Pikachu", 25, True] # puede tener tipos distintos
    '''),

    h2("9.1. Acceder y modificar", "lista-acceso"),
    p("Cada elemento tiene una <strong>posición (índice)</strong>, que empieza en 0:"),
    code('''
        equipo = ["Pikachu", "Charizard", "Snorlax"]
        print(equipo[0])    # Pikachu   (el primero)
        print(equipo[1])    # Charizard
        print(equipo[-1])   # Snorlax   (el último)

        equipo[0] = "Raichu"   # cambiar un elemento (Pikachu evolucionó)
        print(equipo)          # ['Raichu', 'Charizard', 'Snorlax']

        print(len(equipo))         # 3   (cuántos hay)
        print("Snorlax" in equipo) # True  (¿está?)
    '''),

    h2("9.2. Métodos de listas", "lista-metodos"),
    p("Las listas tienen métodos para agregar, quitar, ordenar, etc.:"),
    code('''
        equipo = ["Pikachu", "Charizard"]

        equipo.append("Snorlax")     # agrega al final
        equipo.insert(0, "Mewtwo")   # inserta en la posición 0
        equipo.remove("Charizard")   # borra por valor
        ultimo = equipo.pop()        # saca y devuelve el último
        equipo.sort()                # ordena (alfabético o numérico)
        equipo.reverse()             # da vuelta el orden
    '''),
    tabla(
        ["Método / función", "Qué hace"],
        [
            ["<code>.append(x)</code>", "Agrega x al final"],
            ["<code>.insert(i, x)</code>", "Inserta x en la posición i"],
            ["<code>.remove(x)</code>", "Borra la primera aparición de x"],
            ["<code>.pop()</code>", "Saca y devuelve el último"],
            ["<code>.sort()</code> / <code>.reverse()</code>", "Ordena / invierte"],
            ["<code>len(lista)</code>", "Cantidad de elementos"],
            ["<code>x in lista</code>", "¿x está en la lista?"],
        ],
    ),
    p('Y por supuesto, recorrés una lista con un <code>for</code> (ver <a href="#cap-7">bucles</a>):'),
    code('''
        niveles = [25, 50, 40]
        total = 0
        for n in niveles:
            total = total + n
        print(f"Nivel total del equipo: {total}")   # 115
    '''),

    h2("9.3. enumerate y zip", "enumerate-zip"),
    p("""<code>enumerate</code> te da la posición <strong>y</strong> el valor a la vez.
    <code>zip</code> recorre dos listas en paralelo:"""),
    code('''
        equipo = ["Pikachu", "Charizard"]
        for i, pokemon in enumerate(equipo, start=1):
            print(f"{i}. {pokemon}")
        # 1. Pikachu
        # 2. Charizard

        nombres = ["Pikachu", "Charizard"]
        niveles = [25, 50]
        for nombre, nivel in zip(nombres, niveles):
            print(f"{nombre} es nivel {nivel}")
    '''),

    h2("9.4. Comprensiones de listas", "comprensiones"),
    p("""Una <strong>comprensión</strong> crea una lista nueva a partir de otra, en una
    sola línea. Es muy "pythónico" y, una vez que te acostumbrás, súper cómodo:"""),
    code('''
        niveles = [25, 50, 40, 15]

        # Forma larga (con for):
        dobles = []
        for n in niveles:
            dobles.append(n * 2)

        # La misma cosa, en una línea (comprensión):
        dobles = [n * 2 for n in niveles]      # [50, 100, 80, 30]

        # Con condición (filtrar): solo los niveles altos
        altos = [n for n in niveles if n >= 40]  # [50, 40]
    '''),
    p("La estructura es: <code>[expresión for elemento in coleccion if condición]</code>."),

    h2("9.5. Tuplas", "tuplas"),
    p("""Una <strong>tupla</strong> es como una lista, pero <strong>inmutable</strong>:
    una vez creada, no se puede cambiar. Se escribe con paréntesis <code>( )</code>.
    Se usa para datos que no deberían cambiar (como una coordenada):"""),
    code('''
        coordenada = (10, 20)
        print(coordenada[0])    # 10
        # coordenada[0] = 5     # ❌ ERROR: una tupla no se puede modificar

        # Desempaquetado: asignar varios a la vez
        x, y = coordenada
        print(x, y)             # 10 20
    '''),
    caja("""¿Lista o tupla? Usá <strong>lista</strong> cuando los datos van a cambiar
    (tu equipo, que evoluciona). Usá <strong>tupla</strong> cuando son fijos (las
    coordenadas de un punto, los días de la semana).""", "nota"),
)


# ======================================================================
#  Capítulo 10 — Diccionarios y conjuntos
# ======================================================================
cap10 = capitulo(
    "cap-10", "10. Diccionarios y conjuntos",
    h2("10.1. Diccionarios: pares clave → valor", "dict"),
    p("""Un <strong>diccionario</strong> guarda pares de <strong>clave: valor</strong>.
    En vez de acceder por posición (como las listas), accedés por una <strong>clave</strong>
    con sentido. Es como una Pokédex de verdad: buscás por nombre y obtenés los datos.
    Se escribe con llaves <code>{ }</code>:"""),
    code('''
        pikachu = {
            "nombre": "Pikachu",
            "tipo": "Electrico",
            "nivel": 25,
            "hp": 100,
        }

        print(pikachu["nombre"])    # Pikachu  (accedo por la clave)
        print(pikachu["nivel"])     # 25
    '''),
    h3("Modificar, agregar y acceso seguro"),
    code('''
        pikachu["nivel"] = 26           # cambiar un valor existente
        pikachu["ataque"] = 55          # agregar una clave nueva

        # .get() devuelve un valor por defecto si la clave NO existe (no rompe):
        print(pikachu.get("defensa", 0))   # 0  (no existe "defensa", devuelve 0)
        print("nivel" in pikachu)          # True  (¿existe esa clave?)
    '''),
    h3("Recorrer un diccionario"),
    p("Con <code>.items()</code> obtenés la clave y el valor de cada par:"),
    code('''
        for clave, valor in pikachu.items():
            print(f"{clave}: {valor}")
        # nombre: Pikachu
        # tipo: Electrico
        # nivel: 26
        # ...
    '''),
    p("""Los diccionarios se pueden anidar (un dict adentro de otro) para datos más
    complejos. Por ejemplo, una Pokédex es un dict de Pokémon, donde cada Pokémon es
    a su vez un dict:"""),
    code('''
        pokedex = {
            "pikachu": {"tipo": "Electrico", "nivel": 25},
            "charizard": {"tipo": "Fuego", "nivel": 50},
        }
        print(pokedex["charizard"]["tipo"])   # Fuego
    '''),

    h2("10.2. Conjuntos (sets)", "sets"),
    p("""Un <strong>set</strong> (conjunto) guarda elementos <strong>únicos</strong>:
    sin repetidos y sin un orden definido. Se escribe con llaves <code>{ }</code> (pero
    sin pares clave:valor). Es ideal para sacar duplicados:"""),
    code('''
        tipos = {"Fuego", "Agua", "Fuego", "Planta"}
        print(tipos)            # {'Fuego', 'Agua', 'Planta'}  (el Fuego repetido desaparece)

        capturados = ["Pikachu", "Pidgey", "Pikachu", "Rattata"]
        unicos = set(capturados)
        print(len(unicos))      # 3  (sin contar el Pikachu repetido)

        tipos.add("Electrico")  # agregar
        print("Agua" in tipos)  # True
    '''),

    h2("10.3. Resumen de colecciones", "resumen-colecciones"),
    p("Ya viste las cuatro colecciones principales de Python. Cuándo usar cada una:"),
    tabla(
        ["Colección", "Símbolo", "Característica", "Cuándo usarla"],
        [
            ["Lista", "<code>[ ]</code>", "Ordenada, modificable", "Una serie de cosas que cambia"],
            ["Tupla", "<code>( )</code>", "Ordenada, inmutable", "Datos fijos que no cambian"],
            ["Set", "<code>{ }</code>", "Única, sin orden", "Elementos sin repetir"],
            ["Diccionario", "<code>{c: v}</code>", "Pares clave-valor", "Buscar datos por nombre/clave"],
        ],
    ),
)


# ======================================================================
#  Capítulo 11 — Archivos y errores
# ======================================================================
cap11 = capitulo(
    "cap-11", "11. Archivos y manejo de errores",
    p("""Hasta ahora, cuando cerrabas tu programa, todos los datos se perdían. Para que
    <strong>sobrevivan</strong>, los guardás en <strong>archivos</strong> del disco.
    Así tu programa tiene "memoria" permanente."""),

    h2("11.1. Abrir archivos con with", "with"),
    p("""La forma recomendada de trabajar con archivos es <code>with open(...)</code>,
    que se encarga de cerrar el archivo solo, aunque haya un error. <code>open()</code>
    recibe el nombre y el <strong>modo</strong>:"""),
    tabla(
        ["Modo", "Significa"],
        [
            ['<code>"r"</code>', "leer (read) — el archivo debe existir"],
            ['<code>"w"</code>', "escribir (write) — crea o REEMPLAZA todo"],
            ['<code>"a"</code>', "agregar (append) — escribe al final"],
        ],
    ),
    code('''
        # Escribir (¡el modo "w" pisa lo que había!)
        with open("equipo.txt", "w", encoding="utf-8") as archivo:
            archivo.write("Pikachu\\n")     # \\n = salto de línea
            archivo.write("Charizard\\n")
        # Al salir del 'with', el archivo se cierra solo.

        # Leer todo el contenido de una:
        with open("equipo.txt", "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            print(contenido)

        # Leer línea por línea (lo más común):
        with open("equipo.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                print(linea.strip())   # strip() saca el \\n del final
    '''),
    caja("""El <code>encoding="utf-8"</code> evita problemas con tildes y la ñ.
    Acostumbrate a ponerlo siempre que abras un archivo de texto.""", "nota"),

    h2("11.2. CSV: datos en filas y columnas", "csv"),
    p("""Un <strong>CSV</strong> (valores separados por comas) es un archivo donde cada
    línea es una fila y los datos van separados por comas. Es como una mini planilla.
    Lo podés manejar con <code>split</code>/<code>join</code> (ver <a href="#cap-4">cadenas</a>)
    o con el módulo <code>csv</code>:"""),
    code('''
        import csv

        # Escribir un CSV:
        with open("pokedex.csv", "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["nombre", "tipo", "nivel"])   # encabezado
            escritor.writerow(["Pikachu", "Electrico", 25])
            escritor.writerow(["Charizard", "Fuego", 50])

        # Leer un CSV:
        with open("pokedex.csv", "r", encoding="utf-8") as f:
            lector = csv.reader(f)
            for fila in lector:
                print(fila)    # cada fila es una lista: ['Pikachu', 'Electrico', '25']
    '''),

    h2("11.3. try / except: manejar errores", "try-except"),
    p("""Algunas cosas pueden fallar: abrir un archivo que no existe, convertir "abc" a
    número, dividir por cero. Sin protección, el programa se cae. Con
    <code>try</code>/<code>except</code> <strong>atrapás</strong> el error y seguís:"""),
    code('''
        try:
            # Código que PODRÍA fallar
            numero = int(input("Nivel: "))
            print(f"El nivel es {numero}")
        except ValueError:
            # Esto corre SOLO si hubo un ValueError
            print("Eso no es un número válido")
    '''),
    h3("Atrapar errores al abrir archivos"),
    code('''
        try:
            with open("noexiste.txt", "r") as f:
                contenido = f.read()
        except FileNotFoundError:
            print("El archivo no existe, arranco vacío")
            contenido = ""
    '''),
    tabla(
        ["Error común", "Cuándo pasa"],
        [
            ["<code>ValueError</code>", 'Conversión inválida (<code>int("abc")</code>)'],
            ["<code>FileNotFoundError</code>", "Abrir un archivo que no existe"],
            ["<code>KeyError</code>", "Pedir una clave que no está en un diccionario"],
            ["<code>ZeroDivisionError</code>", "Dividir por cero"],
            ["<code>IndexError</code>", "Pedir una posición que no existe en una lista"],
        ],
    ),
    caja("""Atrapá errores <strong>específicos</strong> (como <code>ValueError</code>),
    no un <code>except:</code> pelado que atrapa todo. Así sabés exactamente qué estás
    manejando y no te ocultás bugs sin querer.""", "tip"),
)


# ======================================================================
#  Capítulo 12 — POO
# ======================================================================
cap12 = capitulo(
    "cap-12", "12. Programación orientada a objetos (POO)",
    p("""La <strong>POO</strong> es una forma de organizar tu código creando tus propios
    "moldes". Una <strong>clase</strong> es el molde (la especie "Pikachu", el plano).
    Un <strong>objeto</strong> (o instancia) es un individuo hecho con ese molde (tu
    Pikachu concreto, distinto del Pikachu de Ash)."""),
    caja("""Mismo molde, datos distintos: la clase <code>Pokemon</code> define que todo
    Pokémon tiene nombre, nivel y HP, y que puede atacar. Pero <em>tu</em> Pikachu y el
    Pikachu de Ash son objetos distintos, con sus propios valores.""", "pokemon"),

    h2("12.1. Definir una clase", "clase"),
    p("""Se define con <code>class</code> y, por convención, el nombre empieza con
    <strong>mayúscula</strong>. El método especial <code>__init__</code> es el
    <strong>constructor</strong>: se ejecuta automáticamente al crear el objeto y le da
    sus datos iniciales. <code>self</code> es "el propio objeto":"""),
    code('''
        class Pokemon:
            def __init__(self, nombre, tipo, nivel):
                # 'self' es este objeto. Guardamos sus datos (atributos).
                self.nombre = nombre
                self.tipo = tipo
                self.nivel = nivel
                self.hp = 100

        # Crear objetos (instancias) con el molde:
        pikachu = Pokemon("Pikachu", "Electrico", 25)
        charizard = Pokemon("Charizard", "Fuego", 50)

        print(pikachu.nombre)     # Pikachu   (accedo a un atributo con punto)
        print(charizard.nivel)    # 50
    '''),
    caja("""<code>self</code> siempre es el <strong>primer parámetro</strong> de los
    métodos, pero <strong>no lo pasás</strong> al llamarlos: Python lo manda solo.
    <code>self.nombre = nombre</code> significa "guardá este nombre adentro mío".""", "clave"),

    h2("12.2. Métodos: las acciones del objeto", "metodos"),
    p("""Un <strong>método</strong> es una función definida dentro de la clase. Son las
    acciones que el objeto puede hacer. Siempre reciben <code>self</code> primero, y
    así pueden usar y modificar los atributos del objeto:"""),
    code('''
        class Pokemon:
            def __init__(self, nombre, tipo):
                self.nombre = nombre
                self.tipo = tipo
                self.hp = 100

            def atacar(self):
                return f"{self.nombre} ataca con un golpe de tipo {self.tipo}!"

            def recibir_dano(self, cantidad):
                self.hp = self.hp - cantidad
                if self.hp < 0:
                    self.hp = 0

        pikachu = Pokemon("Pikachu", "Electrico")
        print(pikachu.atacar())     # Pikachu ataca con un golpe de tipo Electrico!
        pikachu.recibir_dano(30)
        print(pikachu.hp)           # 70
    '''),

    h2("12.3. __str__: cómo se muestra el objeto", "str"),
    p("""Si hacés <code>print(pikachu)</code> sin más, Python muestra algo feo como
    <code>&lt;__main__.Pokemon object at 0x...&gt;</code>. El método especial
    <code>__str__</code> define un texto lindo:"""),
    code('''
        class Pokemon:
            def __init__(self, nombre, nivel):
                self.nombre = nombre
                self.nivel = nivel

            def __str__(self):
                return f"{self.nombre} (Nivel {self.nivel})"

        pikachu = Pokemon("Pikachu", 25)
        print(pikachu)    # Pikachu (Nivel 25)  ← ¡mucho mejor!
    '''),
    caja("""También existe <code>__repr__</code>, parecido pero pensado para el
    programador (lo ves en el REPL y cuando un objeto está dentro de una lista). Regla:
    <code>__str__</code> para el usuario (lindo), <code>__repr__</code> para vos (preciso).""", "nota"),

    h2("12.4. Encapsulamiento básico", "encapsulamiento"),
    p("""<strong>Encapsular</strong> es proteger los datos internos. Por convención, un
    atributo que no debería tocarse desde afuera se nombra con un <strong>guión bajo</strong>
    adelante (<code>_hp</code>), y se cambia solo a través de métodos que pueden validar:"""),
    code('''
        class Pokemon:
            def __init__(self, nombre):
                self.nombre = nombre
                self._hp = 100        # "interno": no lo toques directo

            def curar(self, cantidad):
                self._hp = self._hp + cantidad
                if self._hp > 100:    # el método valida que no pase de 100
                    self._hp = 100
    '''),
)


# ======================================================================
#  Capítulo 13 — POO avanzado
# ======================================================================
cap13 = capitulo(
    "cap-13", "13. POO avanzado: herencia y polimorfismo",
    h2("13.1. Herencia", "herencia"),
    p("""La <strong>herencia</strong> deja que una clase "hija" reciba todo lo de una
    clase "padre", y le agregue o cambie lo suyo. Así escribís lo común una vez. La hija
    se define poniendo el padre entre paréntesis:"""),
    code('''
        class Pokemon:                    # clase PADRE
            def __init__(self, nombre, nivel):
                self.nombre = nombre
                self.nivel = nivel
            def atacar(self):
                return f"{self.nombre} ataca!"

        class PokemonFuego(Pokemon):      # HIJA: hereda de Pokemon
            def lanzallamas(self):
                return f"{self.nombre} usa Lanzallamas! 🔥"

        charizard = PokemonFuego("Charizard", 50)
        print(charizard.atacar())       # heredado de Pokemon
        print(charizard.lanzallamas())  # propio de PokemonFuego
    '''),
    h3("super(): llamar al padre"),
    p("Cuando la hija define su propio <code>__init__</code>, usa <code>super()</code> para no repetir el del padre:"),
    code('''
        class PokemonFuego(Pokemon):
            def __init__(self, nombre, nivel):
                super().__init__(nombre, nivel)   # ejecuta el __init__ del padre
                self.tipo = "Fuego"               # y agrega lo propio
    '''),

    h2("13.2. Polimorfismo", "polimorfismo"),
    p("""<strong>Polimorfismo</strong> ("muchas formas") significa que el mismo método se
    comporta distinto según la clase. Todos los Pokémon tienen <code>atacar()</code>,
    pero cada tipo lo <strong>sobrescribe</strong> a su manera:"""),
    code('''
        class Pokemon:
            def __init__(self, nombre):
                self.nombre = nombre
            def atacar(self):
                return f"{self.nombre} usa un ataque normal"

        class PokemonFuego(Pokemon):
            def atacar(self):       # SOBRESCRIBE el método del padre
                return f"{self.nombre} usa Lanzallamas! 🔥"

        class PokemonAgua(Pokemon):
            def atacar(self):
                return f"{self.nombre} usa Pistola Agua! 💧"

        equipo = [PokemonFuego("Charizard"), PokemonAgua("Blastoise")]
        for p in equipo:
            print(p.atacar())   # cada uno responde a su manera
    '''),
    caja("""El poder del polimorfismo: tratás a todos como "Pokémon" y cada uno hace lo
    suyo, sin tener que escribir <code>if tipo == "fuego" ... elif tipo == "agua" ...</code>
    por todos lados. El código queda mucho más limpio.""", "clave"),

    h2("13.3. property, métodos de clase y abstractas", "property-abc"),
    p("""Hay más herramientas avanzadas que vas a ver en la semana 9 del curso:"""),
    ul(
        "<code>@property</code> — deja usar un método como si fuera un atributo (sin paréntesis), ideal para calcular o validar valores.",
        "<code>@staticmethod</code> y <code>@classmethod</code> — funciones dentro de la clase con usos especiales.",
        "Clases abstractas (módulo <code>abc</code>) — un \"contrato\" que obliga a las hijas a implementar ciertos métodos.",
    ),
    code('''
        class Pokemon:
            def __init__(self, hp):
                self._hp = hp

            @property
            def hp(self):           # se accede como pokemon.hp (sin paréntesis)
                return self._hp

            @hp.setter
            def hp(self, valor):    # se ejecuta al hacer pokemon.hp = algo
                self._hp = max(0, valor)   # nunca negativo

        p = Pokemon(100)
        p.hp = -50          # el setter lo corrige
        print(p.hp)         # 0
    '''),
)


# ======================================================================
#  Capítulo 14 — Módulos y pip
# ======================================================================
cap14 = capitulo(
    "cap-14", "14. Módulos, pip y entornos virtuales",
    p("""Un <strong>módulo</strong> es un archivo lleno de código útil que podés
    <strong>importar</strong> y usar. Python trae muchísimos "de fábrica" (la librería
    estándar). No reinventes la rueda: aprovechá el trabajo de millones de personas."""),

    h2("14.1. import y la librería estándar", "import"),
    p("Para usar un módulo, lo importás. Después accedés a sus funciones con un punto:"),
    code('''
        import math
        import random
        from datetime import date

        print(math.sqrt(16))                 # 4.0   (raíz cuadrada)
        print(math.ceil(4.2))                # 5     (redondea para arriba)
        print(random.randint(1, 6))          # un número al azar entre 1 y 6 (dado)
        print(random.choice(["Pikachu", "Onix"]))  # uno al azar de la lista
        print(date.today())                  # la fecha de hoy
    '''),
    tabla(
        ["Módulo", "Sirve para"],
        [
            ["<code>math</code>", "Matemática (raíz, redondeo, pi...)"],
            ["<code>random</code>", "Azar (números al azar, elegir, mezclar)"],
            ["<code>datetime</code>", "Fechas y horas"],
            ["<code>os</code> / <code>sys</code>", "Interactuar con el sistema"],
            ["<code>json</code>", "Guardar/cargar datos estructurados"],
        ],
    ),

    h2("14.2. json: guardar datos estructurados", "json"),
    p("""<strong>JSON</strong> es <em>el</em> formato para guardar datos (diccionarios,
    listas) en un archivo. Lo vas a usar en los proyectos finales:"""),
    code('''
        import json

        datos = {"nombre": "Pikachu", "nivel": 25}

        # Guardar en un archivo:
        with open("pokemon.json", "w") as f:
            json.dump(datos, f)

        # Cargar de un archivo:
        with open("pokemon.json", "r") as f:
            datos = json.load(f)
        print(datos["nombre"])    # Pikachu
    '''),

    h2("14.3. Tus propios módulos", "modulo-propio"),
    p("""Cualquier archivo <code>.py</code> tuyo es un módulo que podés importar desde
    otro. Así organizás proyectos grandes. Si tenés <code>pokeutils.py</code> con una
    función <code>formatear_nombre</code>, desde otro archivo hacés:"""),
    code('''
        import pokeutils
        print(pokeutils.formatear_nombre("pikachu"))   # Pikachu
    '''),

    h2("14.4. pip y entornos virtuales", "pip-venv"),
    p("""La librería estándar es enorme, pero a veces necesitás algo externo.
    <strong>pip</strong> es el instalador de paquetes de Python (tu PokéMart de
    librerías):"""),
    code('''
        pip install requests           # instala una librería
        pip install -r requirements.txt  # instala todas las de una lista
    ''', lang="bash"),
    caja("""Un <strong>entorno virtual</strong> (<code>venv</code>) es una cajita aislada
    con las librerías de tu proyecto, separada del Python del sistema. Así cada proyecto
    tiene sus versiones sin pisarse. El <code>setup.sh</code> del curso lo crea por vos.""", "nota"),

    h2("14.5. requests: traer datos de internet", "requests"),
    p("""Con la librería <code>requests</code> tu programa puede pedir datos a un servicio
    de internet (una <strong>API</strong>). La <strong>PokéAPI</strong> tiene datos de
    todos los Pokémon, gratis:"""),
    code('''
        import requests

        respuesta = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu")
        datos = respuesta.json()      # convierte la respuesta a un diccionario

        print(datos["name"])                       # pikachu
        print(datos["height"])                     # altura
        print(datos["types"][0]["type"]["name"])   # electric
    '''),
    caja("""Para usar <code>requests</code> necesitás internet y tenerla instalada
    (<code>pip install requests</code>). En la semana 10 del curso construís una Pokédex
    online que muestra datos reales con esto.""", "nota"),
)


# ======================================================================
#  Capítulo 15 — Linux: la terminal
# ======================================================================
cap_linux1 = capitulo(
    "cap-linux1", "15. Linux: la terminal",
    p("""Esta parte cubre <strong>Linux</strong>, que en el curso ves en las semanas
    1 y 2 (antes de Python). La <strong>terminal</strong> es una ventana donde escribís
    comandos de texto y la computadora te responde. Al principio asusta, pero es la
    herramienta más poderosa que vas a tener."""),
    caja("""Pensá en la terminal como la <strong>Pokédex de tu sistema</strong>: una
    herramienta de texto donde cada comando es un "ataque". Aprender los comandos es
    como aprender los movimientos de tu Pokémon.""", "pokemon"),
    p("""Cuando abrís la terminal, ves un <em>prompt</em> tipo
    <code>felipe@maquina:~$</code>. El <code>~</code> significa "tu carpeta personal"
    (tu <em>home</em>) y el <code>$</code> dice "estoy listo, escribí tu comando"."""),

    h2("15.1. Moverte por las carpetas", "linux-mover"),
    p("""Todo en Linux está organizado en <strong>carpetas</strong> (directorios), una
    dentro de otra, formando un árbol. Estos tres comandos te dejan ubicarte y viajar:"""),
    code('''
        pwd            # ¿dónde estoy? muestra la ruta de la carpeta actual
        ls             # ver qué hay acá (archivos y carpetas)
        ls -l          # en formato largo: permisos, tamaño, fecha
        ls -a          # incluye archivos ocultos (empiezan con un punto)
        cd pokecenter  # entrar a la carpeta pokecenter
        cd ..          # subir un nivel (a la carpeta de arriba)
        cd ~           # ir a tu carpeta personal (home)
        cd /           # ir a la raíz de todo
    ''', lang="bash"),
    p("""Las opciones como <code>-l</code> o <code>-a</code> se llaman <strong>flags</strong>:
    modifican lo que hace el comando. Es como un objeto que potencia el ataque."""),

    h2("15.2. Crear, copiar y borrar", "linux-crear"),
    code('''
        mkdir pokecenter        # crear una carpeta (make directory)
        mkdir -p a/b/c          # crear carpetas anidadas de una (-p)
        touch pikachu.txt       # crear un archivo vacío
        echo "Electrico" > pikachu.txt   # escribir texto DENTRO de un archivo
        cat pikachu.txt         # mostrar el contenido de un archivo
        cp pikachu.txt copia.txt   # copiar un archivo
        cp -r carpeta copia        # copiar una carpeta entera (-r = recursivo)
        mv pikachu.txt raichu.txt  # renombrar (o mover a otra carpeta)
        rm pikachu.txt          # borrar un archivo
        rm -r carpeta           # borrar una carpeta y todo lo de adentro
    ''', lang="bash"),
    caja("""En Linux <strong>no hay papelera de reciclaje</strong>: lo que borrás con
    <code>rm</code>, se va para siempre. Revisá siempre antes de borrar. Y
    <strong>nunca, jamás</strong> corras <code>rm -rf /</code>: intenta borrar todo el
    sistema.""", "cuidado"),

    h2("15.3. Rutas absolutas y relativas", "linux-rutas"),
    p("""Una <strong>ruta</strong> es la dirección de un archivo o carpeta. Una ruta
    <strong>absoluta</strong> empieza en la raíz <code>/</code> y vale desde cualquier
    lado (como una dirección completa). Una <strong>relativa</strong> parte de donde
    estás parado:"""),
    code('''
        cd /home/ash/pokecenter   # ruta ABSOLUTA (empieza con /)
        cd pokecenter/gimnasio    # ruta RELATIVA (desde donde estás)
    ''', lang="bash"),
    ul(
        "<code>.</code> &rarr; la carpeta actual (acá mismo)",
        "<code>..</code> &rarr; la carpeta de arriba",
        "<code>~</code> &rarr; tu home",
        "<code>/</code> &rarr; la raíz de todo",
    ),

    h2("15.4. Permisos básicos", "linux-permisos"),
    p("""Cada archivo tiene <strong>permisos</strong> que dicen quién puede leerlo,
    escribirlo o ejecutarlo. Al correr <code>ls -l</code> ves algo como
    <code>-rwxr-xr--</code>. Esa columna se lee así:"""),
    ul(
        "<code>r</code> = leer, <code>w</code> = escribir, <code>x</code> = ejecutar.",
        "Se agrupan de a 3, para tres grupos: el <strong>dueño</strong>, el <strong>grupo</strong> y los <strong>otros</strong>.",
    ),
    p("En la próxima parte vas a aprender a cambiar estos permisos con <code>chmod</code>."),

    h2("15.5. Resumen", "linux-resumen-1"),
    tabla(
        ["Comando", "Qué hace"],
        [
            ["<code>pwd</code>", "Dice en qué carpeta estás"],
            ["<code>ls</code>", "Lista archivos y carpetas"],
            ["<code>cd</code>", "Cambia de carpeta"],
            ["<code>mkdir</code>", "Crea una carpeta"],
            ["<code>touch</code> / <code>echo</code>", "Crea / escribe archivos"],
            ["<code>cat</code>", "Muestra un archivo"],
            ["<code>cp</code> / <code>mv</code>", "Copia / mueve o renombra"],
            ["<code>rm</code>", "Borra (¡sin papelera!)"],
        ],
    ),
)


# ======================================================================
#  Capítulo 16 — Linux: comandos intermedios
# ======================================================================
cap_linux2 = capitulo(
    "cap-linux2", "16. Linux: comandos intermedios",
    p("""Ahora que te movés por la terminal, sumamos superpoderes: editar archivos,
    encadenar comandos, buscar, manejar procesos y automatizar con scripts."""),

    h2("16.1. Editar con nano", "linux-nano"),
    p("""<code>nano</code> es un editor de texto simple que vive dentro de la terminal.
    Abajo te muestra los atajos (el <code>^</code> significa la tecla Ctrl):"""),
    code("nano notas.txt   # Ctrl+O para guardar, Ctrl+X para salir", lang="bash"),

    h2("16.2. Variables, redirección y pipes", "linux-pipes"),
    p("""Una <strong>variable de entorno</strong> guarda un dato con un nombre. La
    <strong>redirección</strong> manda la salida de un comando a un archivo, y un
    <strong>pipe</strong> (<code>|</code>) conecta la salida de un comando con otro:"""),
    code('''
        echo $HOME                     # muestra el valor de una variable

        echo "Pikachu" > equipo.txt    # > CREA o REEMPLAZA el archivo
        echo "Charizard" >> equipo.txt # >> AGREGA al final (no borra)

        cat equipo.txt | sort          # | conecta cat con sort (ordena)
        ls | wc -l                     # cuenta cuántos archivos hay
    ''', lang="bash"),
    caja("""Ojo: <code>&gt;</code> pisa todo lo que había en el archivo;
    <code>&gt;&gt;</code> agrega al final. Confundirlos borra datos.""", "cuidado"),

    h2("16.3. Buscar: grep y find", "linux-buscar"),
    p("""<code>grep</code> busca <strong>texto dentro</strong> de archivos.
    <code>find</code> busca <strong>los archivos en sí</strong> por su nombre:"""),
    code('''
        grep "Fuego" pokedex.txt    # muestra las líneas que contienen "Fuego"
        grep -i "fuego" pokedex.txt # -i ignora mayúsculas/minúsculas
        find . -name "*.txt"        # busca todos los .txt desde la carpeta actual
    ''', lang="bash"),

    h2("16.4. Procesos y permisos", "linux-procesos"),
    p("""Un <strong>proceso</strong> es un programa corriendo. <code>chmod</code> cambia
    los permisos de un archivo (lo más común: dar permiso de ejecución con
    <code>+x</code>):"""),
    code('''
        ps aux              # lista todos los procesos en ejecución
        ps aux | grep python   # filtra los de python
        kill 1234           # cierra el proceso con ese número (PID)
        chmod +x script.sh  # da permiso de EJECUCIÓN al archivo
        chmod 755 script.sh # forma numérica (rwx para el dueño, r-x para el resto)
    ''', lang="bash"),

    h2("16.5. Tu primer script bash", "linux-scripts"),
    p("""Un <strong>script</strong> es un archivo de texto con una lista de comandos que
    se ejecutan en orden. Es tu máquina automática. La primera línea (el "shebang") dice
    que es un script bash:"""),
    code('''
        #!/usr/bin/env bash
        # Este script saluda y registra un Pokémon capturado.
        echo "¡Hola, Entrenador!"
        echo "Capturaste a: $1"          # $1 es el primer argumento
        echo "$1" >> capturados.txt      # lo guarda en un archivo
    ''', lang="bash"),
    p("Para correrlo, le das permiso de ejecución y lo ejecutás con <code>./</code>:"),
    code('''
        chmod +x capturar.sh
        ./capturar.sh Snorlax    # imprime y registra a Snorlax
    ''', lang="bash"),

    h2("16.6. Instalar programas y SSH", "linux-apt-ssh"),
    p("""En Ubuntu/Debian, <code>apt</code> instala programas. <code>ssh</code> te deja
    controlar otra computadora por la terminal, de forma segura:"""),
    code('''
        sudo apt update             # actualiza la lista de programas
        sudo apt install cowsay     # instala un programa
        ssh entrenador@192.168.1.50 # te conectás a otra máquina
    ''', lang="bash"),
    caja("""<code>sudo</code> ejecuta un comando como administrador (root). Es poderoso:
    no corras con <code>sudo</code> cosas que no entendés.""", "nota"),

    h2("16.7. Resumen", "linux-resumen-2"),
    tabla(
        ["Comando", "Qué hace"],
        [
            ["<code>nano</code>", "Edita un archivo de texto"],
            ["<code>&gt;</code> / <code>&gt;&gt;</code>", "Redirige (reemplaza / agrega)"],
            ["<code>|</code>", "Conecta la salida de un comando con otro"],
            ["<code>grep</code> / <code>find</code>", "Busca texto / archivos"],
            ["<code>ps</code> / <code>kill</code>", "Ver / cerrar procesos"],
            ["<code>chmod</code>", "Cambia permisos"],
            ["<code>apt</code> / <code>ssh</code>", "Instala programas / conecta a otra máquina"],
        ],
    ),
)


# ======================================================================
#  Capítulo 17 — Mapa del curso (índice de temas)
# ======================================================================
cap15 = capitulo(
    "cap-15", "17. Mapa de temas del curso",
    p("Estos son <strong>todos los temas</strong> del curso, semana por semana. Cada semana tiene su teoría, ejercicios, soluciones, tests y un programa interactivo."),

    h2("17.1. Fase 1 — Linux 🐧", "fase-linux"),
    tabla(
        ["Semana", "Temas"],
        [
            ["01 — Fundamentos", "Terminal, navegación, <code>ls cd pwd mkdir rm cp mv cat echo</code>, rutas, permisos"],
            ["02 — Intermedio", "<code>nano</code>, variables, scripts bash, <code>&gt; &gt;&gt; |</code>, <code>grep find ps kill chmod apt</code>, SSH"],
        ],
    ),

    h2("17.2. Fase 2 — Python básico 🐍", "fase-py-basico"),
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

    h2("17.3. Descanso — Git 🔀", "fase-git"),
    p("<strong>Git: Control de Versiones</strong> — <code>init</code>, <code>add</code>, <code>commit</code>, <code>log</code>, ramas (<code>branch/switch/merge</code>), GitHub, <code>push/pull/clone</code>, <code>.gitignore</code>. Pensada para hacerse después de la semana 7."),

    h2("17.4. Fase 3 — Python avanzado 🧬", "fase-py-avanzado"),
    tabla(
        ["Semana", "Temas"],
        [
            ["08 — POO introducción", "Clases, <code>__init__</code>, atributos, métodos, <code>self</code>, <code>__str__</code>, <code>__repr__</code>"],
            ["09 — POO avanzado", "Herencia, <code>super()</code>, polimorfismo, <code>@property</code>, clases abstractas (<code>abc</code>)"],
            ["10 — Módulos y pip", "<code>import</code>, módulos estándar, módulos propios, <code>pip</code>, <code>venv</code>, <code>requests</code>"],
        ],
    ),

    h2("17.5. Fase 4 — Proyectos 🏆", "fase-proyectos"),
    ul(
        "<strong>Semana 11 — Agenda del Entrenador:</strong> app de consola modular con persistencia en JSON.",
        "<strong>Semana 12 — Pokédex Web:</strong> web con Flask + PokéAPI.",
        "<strong>proyectos/pokedex-cli:</strong> Pokédex de consola con sprites ASCII y favoritos.",
        "<strong>proyectos/batalla-pokemon:</strong> simulador con tipos, PP y estados alterados.",
        "<strong>proyectos/agenda-entrenador</strong> y <strong>proyectos/pokedex-web:</strong> versiones pulidas.",
    ),
)


# ======================================================================
#  Capítulo 18 — Tests, FAQ y glosario
# ======================================================================
cap16 = capitulo(
    "cap-16", "18. Tests, preguntas frecuentes y glosario",
    h2("18.1. Cómo correr los tests", "tests"),
    p("Los <strong>tests</strong> te dicen si tus ejercicios están bien. Usamos <strong>pytest</strong>:"),
    code('''
        pytest                                   # todos los tests
        pytest semana-04-python-control-de-flujo/   # una semana
        pytest semana-05-python-funciones/test_ejercicios.py -v   # con detalle
    ''', lang="bash"),
    caja("""🟢 Verde = aprobado. 🔴 Rojo = revisá tu solución. Por defecto los tests
    prueban las soluciones; la Liga los corre contra TU <code>ejercicios.py</code> para
    darte EXP y decirte qué ejercicio falta.""", "nota"),

    h2("18.2. Preguntas frecuentes", "faq"),
    p("<strong>¿Por dónde empiezo?</strong> Por la Liga: <code>python aventura.py</code>. Después seguí la semana 01."),
    p("<strong>Me sale \"command not found: python\".</strong> Probá con <code>python3</code>."),
    p("<strong>Los tests me dan rojo. ¿Está mal?</strong> Significa que tu solución todavía no es correcta. Leé el error (está en español), corregí y volvé a probar. Es parte normal del aprendizaje."),
    p("<strong>¿Puedo ver las soluciones?</strong> Sí, están en <code>soluciones.py</code>. Pero intentá primero vos: mirar sin intentar es como usar un truco, ganás pero no aprendés."),
    p("<strong>¿Necesito internet?</strong> Solo para algunas partes (la semana 10, la Pokédex online y el autocompletado web). El resto funciona sin conexión."),

    h2("18.3. Glosario", "glosario"),
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


# Lista final de capítulos, EN ORDEN DE LECTURA.
# Los números de capítulo y de sección los asigna automáticamente el generador
# (generar_manual.renumerar), según esta posición. Para reordenar el libro,
# cambiá el orden de esta lista: los números se recalculan solos.
# Linux va primero (es la base), después Python, y al final el mapa y la ayuda.
CAPITULOS = [
    cap_intro,                       # 0 — cómo usar el libro
    cap_linux1, cap_linux2,          # Linux (la base)
    cap1, cap2, cap3, cap4, cap5,    # Python básico
    cap6, cap7, cap8, cap9, cap10, cap11,
    cap12, cap13, cap14,             # Python avanzado
    cap15, cap16,                    # mapa del curso + tests/FAQ
]
