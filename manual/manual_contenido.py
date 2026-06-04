"""
manual_contenido.py — El contenido del libro, capítulo por capítulo.

Cada capítulo se arma con las funciones de manual_lib (p, h2, code, caja, tabla...).
El contenido está escrito en HTML (no en Markdown), para tener control total del estilo.

Este libro cumple dos roles:
  1. Manual de cómo usar el proyecto/curso.
  2. Libro de Python para aprender el lenguaje desde cero.
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
    Por otro lado es un <strong>libro de Python</strong>: a partir del capítulo 1
    podés aprender el lenguaje desde cero, con ejemplos y ejercicios."""),
    p("""Todo está pensado para alguien que <strong>nunca programó</strong>. No hace
    falta saber nada de antes. Vamos con calma y con temática Pokémon. 🐍"""),

    h2("0.1. ¿Qué es este proyecto?", "que-es"),
    p("""Es un curso completo de <strong>Linux</strong> y <strong>Python</strong>,
    dividido en 12 semanas (más una semana de descanso de Git) y 4 proyectos finales.
    Cada concepto se explica con una analogía Pokémon, cada ejercicio usa Pokémon, y
    cada proyecto es algo que un Entrenador usaría de verdad."""),

    h2("0.2. Instalación", "instalacion"),
    p("Abrí una terminal dentro de la carpeta del proyecto y corré:"),
    code("bash setup.sh", lang="bash"),
    p("Eso crea un <em>entorno virtual</em> e instala lo necesario. Después, cada vez que trabajes, activalo:"),
    code("source venv/bin/activate", lang="bash"),
    caja("""Si <code>setup.sh</code> falla, abrilo: está comentado línea por línea.
    Las dos primeras semanas son de Linux y no necesitan Python para los ejercicios
    de terminal.""", "cuidado"),

    h2("0.3. La Liga Pokémon: jugá tu progreso", "liga"),
    p("""La mejor forma de hacer el curso. En vez de "hacer la tarea", subís de nivel.
    Abrila con:"""),
    code("python aventura.py", lang="bash"),
    p("Desde ese centro de mando podés:"),
    ul(
        "🎴 Ver tu <strong>Tarjeta de Entrenador</strong> (nivel, EXP, rango).",
        "🏋️ <strong>Entrenar</strong> una semana: corre <em>tus</em> ejercicios y te da EXP por cada test que pasás.",
        "🏅 Ganar las <strong>8 medallas de gimnasio</strong> y desbloquear logros.",
        "🔥 Mantener tu <strong>racha</strong> diaria y ver el mapa de la región.",
    ),
    p("Cuando consigas las 8 medallas, <strong>¡sos Campeón de Kanto!</strong> 🏆"),

    h2("0.4. El método: cómo trabajar cada semana", "metodo"),
    ol(
        "📖 <strong>Leé</strong> la teoría de la semana (también podés leer este libro).",
        "✏️ <strong>Resolvé</strong> los ejercicios (escribí tu código donde dice <code># TU CÓDIGO ACÁ</code>).",
        "🧪 <strong>Probá</strong> con los tests (ver capítulo 18).",
        "🎮 <strong>Jugá</strong> el <code>interactivo.py</code> de la semana.",
        "🏋️ <strong>Entrená</strong> esa semana en la Liga para ganar EXP.",
    ),
    caja("""<strong>Regla de oro:</strong> equivocarse es parte del juego. Escribí el
    código vos mismo, no copies y pegues: tipear te enseña.""", "tip"),
)


# ======================================================================
#  Capítulo 1 — Tu primer programa
# ======================================================================
cap1 = capitulo(
    "cap-1", "1. Tu primer programa en Python",
    p("""<strong>Python</strong> es un lenguaje de programación: la forma en que le
    damos órdenes a la computadora. Es famoso porque se lee casi como inglés y es
    ideal para aprender."""),
    caja("""Pensá en Python como el <strong>idioma de los Entrenadores</strong>. Vos
    escribís instrucciones (el código) y la computadora las obedece, como un Pokémon
    bien entrenado.""", "pokemon"),

    h2("1.1. print(): mostrar cosas en pantalla", "print"),
    p("La instrucción <code>print()</code> muestra texto en la pantalla. Es lo primero que hace todo programador:"),
    code('''
        print("¡Hola, mundo Pokémon!")
        print("Elegí a Pikachu como inicial")
    '''),
    p("Podés mostrar varias cosas separándolas con comas:"),
    code('print("Mi Pokémon es", "Charizard")   # Mi Pokémon es Charizard'),

    h2("1.2. El REPL: probar al instante", "repl"),
    p("""Si escribís <code>python3</code> en la terminal, se abre el <strong>REPL</strong>:
    un modo interactivo donde probás cosas y ves el resultado al toque. El símbolo
    <code>&gt;&gt;&gt;</code> es su prompt."""),
    code('''
        >>> 2 + 2
        4
        >>> print("Hola")
        Hola
    '''),
    p("Para salir del REPL escribís <code>exit()</code>. Para programas de verdad, escribís el código en un archivo <code>.py</code> y lo corrés con <code>python3 archivo.py</code>."),

    h2("1.3. Comentarios", "comentarios"),
    p("Un <strong>comentario</strong> es texto que Python ignora. Sirve para explicar tu código. Empieza con <code>#</code>:"),
    code('''
        # Esto es un comentario, Python no lo ejecuta.
        print("Hola")   # también se puede comentar al final de una línea
    '''),
    caja("Comentar bien tu código es de buen programador. Tu yo del futuro te lo agradece.", "tip"),
)


# ======================================================================
#  Capítulo 2 — Variables y tipos
# ======================================================================
cap2 = capitulo(
    "cap-2", "2. Variables y tipos de datos",
    h2("2.1. Variables", "variables"),
    p("""Una <strong>variable</strong> guarda un dato con un nombre, para usarlo después.
    Es como una <strong>Pokéball</strong>: adentro guardás algo y le ponés una etiqueta."""),
    code('''
        nombre = "Pikachu"      # guardamos un texto
        nivel = 25              # guardamos un número
        print(nombre)           # Pikachu
        print(nivel)            # 25
    '''),
    p("El nombre va a la izquierda del <code>=</code>, el valor a la derecha. Usá guiones bajos para separar palabras y no empieces con números:"),
    code('''
        pokemon_inicial = "Charmander"   # ✅ bien
        # 3pokemon = "no"                # ❌ mal: no puede empezar con número
    '''),

    h2("2.2. Los cuatro tipos básicos", "tipos"),
    tabla(
        ["Tipo", "Qué es", "Ejemplo"],
        [
            ["<code>int</code>", "Número entero", "<code>nivel = 25</code>"],
            ["<code>float</code>", "Número con decimales", "<code>peso = 6.0</code>"],
            ["<code>str</code>", "Texto (entre comillas)", '<code>nombre = "Pikachu"</code>'],
            ["<code>bool</code>", "Verdadero o falso", "<code>es_legendario = False</code>"],
        ],
    ),
    p("Para ver el tipo de un valor, usás <code>type()</code>:"),
    code('''
        print(type(25))         # <class 'int'>
        print(type("Pikachu"))  # <class 'str'>
        print(type(6.0))        # <class 'float'>
        print(type(True))       # <class 'bool'>
    '''),
    caja("""Los valores <code>bool</code> se escriben con mayúscula:
    <code>True</code> y <code>False</code>.""", "cuidado"),

    h2("2.3. f-strings: armar texto con variables", "fstrings"),
    p("Un <strong>f-string</strong> deja meter variables dentro de un texto poniendo una <code>f</code> antes de las comillas y las variables entre <code>{llaves}</code>:"),
    code('''
        nombre = "Pikachu"
        nivel = 25
        print(f"Mi {nombre} es nivel {nivel}")   # Mi Pikachu es nivel 25
    '''),
    caja("Los f-strings son la forma recomendada de armar texto. ¡Usalos siempre!", "clave"),
)


# ======================================================================
#  Capítulo 3 — Operadores
# ======================================================================
cap3 = capitulo(
    "cap-3", "3. Operadores",
    h2("3.1. Operadores aritméticos", "aritmeticos"),
    tabla(
        ["Operador", "Hace", "Ejemplo", "Resultado"],
        [
            ["<code>+</code>", "Suma", "<code>10 + 5</code>", "15"],
            ["<code>-</code>", "Resta", "<code>10 - 5</code>", "5"],
            ["<code>*</code>", "Multiplicación", "<code>10 * 5</code>", "50"],
            ["<code>/</code>", "División (con decimales)", "<code>10 / 4</code>", "2.5"],
            ["<code>//</code>", "División entera", "<code>10 // 4</code>", "2"],
            ["<code>%</code>", "Resto (módulo)", "<code>10 % 4</code>", "2"],
            ["<code>**</code>", "Potencia", "<code>2 ** 3</code>", "8"],
        ],
    ),
    caja("""El operador <code>%</code> (módulo) es súper útil: un número es par si
    <code>numero % 2 == 0</code>.""", "tip"),

    h2("3.2. Operadores de comparación", "comparacion"),
    p("Devuelven <code>True</code> o <code>False</code>:"),
    tabla(
        ["Operador", "Significa"],
        [
            ["<code>==</code>", "igual a"],
            ["<code>!=</code>", "distinto de"],
            ["<code>&gt;</code> &nbsp; <code>&lt;</code>", "mayor / menor que"],
            ["<code>&gt;=</code> &nbsp; <code>&lt;=</code>", "mayor o igual / menor o igual"],
        ],
    ),
    caja("""<strong>¡Ojo!</strong> <code>=</code> asigna (guarda en una variable);
    <code>==</code> compara. No los confundas.""", "cuidado"),

    h2("3.3. Operadores lógicos", "logicos"),
    p("Combinan condiciones: <code>and</code> (ambas), <code>or</code> (al menos una), <code>not</code> (invierte)."),
    code('''
        nivel = 30
        tipo = "Fuego"
        if nivel >= 25 and tipo == "Fuego":
            print("¡Charmander evoluciona a Charmeleon!")
    '''),
)


# ======================================================================
#  Capítulo 4 — Strings
# ======================================================================
cap4 = capitulo(
    "cap-4", "4. Cadenas de texto (strings)",
    p("Un <strong>string</strong> es texto, siempre entre comillas. Tiene muchos <strong>métodos</strong> (acciones) para transformarlo. No cambian el original: devuelven uno nuevo."),
    code('''
        nombre = "  Pikachu  "
        print(nombre.upper())     # "  PIKACHU  "  (mayúsculas)
        print(nombre.lower())     # "  pikachu  "  (minúsculas)
        print(nombre.strip())     # "Pikachu"      (saca espacios de los bordes)
        print("pikachu".capitalize())   # "Pikachu"
        print("Pikachu".startswith("Pika"))  # True
        print(len("Pikachu"))     # 7  (longitud)
    '''),

    h2("4.1. split y join", "split-join"),
    p("<code>split</code> parte un texto en una lista; <code>join</code> une una lista en un texto. Son clave para los archivos CSV:"),
    code('''
        linea = "Pikachu,Electrico,25"
        partes = linea.split(",")     # ['Pikachu', 'Electrico', '25']

        datos = ["Charizard", "Fuego", "50"]
        linea = ",".join(datos)       # "Charizard,Fuego,50"
    '''),

    h2("4.2. Slicing: rebanar texto", "slicing"),
    p("El <strong>slicing</strong> saca una rebanada con <code>[inicio:fin]</code>. El <code>fin</code> NO se incluye:"),
    code('''
        texto = "Pikachu"
        #        0123456
        print(texto[0:4])    # "Pika"
        print(texto[4:])     # "chu"
        print(texto[-3:])    # "chu"  (los últimos 3)
        print(texto[::-1])   # "uhcakiP"  (al revés)
    '''),
)


# ======================================================================
#  Capítulo 5 — input
# ======================================================================
cap5 = capitulo(
    "cap-5", "5. Pedir datos: input()",
    p("<code>input()</code> pausa el programa y espera que el usuario escriba algo y apriete Enter:"),
    code('''
        nombre = input("¿Cómo se llama tu Pokémon? ")
        print(f"¡Hola, {nombre}!")
    '''),
    caja("""<strong>MUY IMPORTANTE:</strong> <code>input()</code> SIEMPRE devuelve
    texto (str), aunque el usuario escriba un número. Si querés un número, hay que
    convertirlo.""", "cuidado"),

    h2("5.1. Conversión de tipos", "conversion"),
    code('''
        nivel_texto = input("¿Nivel? ")   # esto es str, ej "25"
        nivel = int(nivel_texto)          # ahora es int: 25
        print(nivel + 5)                  # 30

        # Forma compacta, muy común:
        edad = int(input("¿Tu edad? "))
    '''),
    p("Funciones de conversión: <code>int(\"25\")</code>, <code>float(\"6.5\")</code>, <code>str(25)</code>."),
)


# ======================================================================
#  Capítulo 6 — Condicionales
# ======================================================================
cap6 = capitulo(
    "cap-6", "6. Condicionales: if / elif / else",
    p("<code>if</code> ejecuta un bloque solo si una condición es verdadera. <code>elif</code> agrega más condiciones, y <code>else</code> es el \"si no\"."),
    code('''
        hp = 40
        if hp > 70:
            print("Tu Pokémon está sano 💚")
        elif hp > 30:
            print("Tu Pokémon está cansado 💛")
        elif hp > 0:
            print("¡Está grave! ❤️")
        else:
            print("Se debilitó 💀")
    '''),
    caja("""<strong>La indentación importa.</strong> El código "adentro" del
    <code>if</code> va con 4 espacios de sangría. Python usa esa sangría para saber
    qué está adentro y qué afuera. No es decorativo: es obligatorio.""", "clave"),
    p("Python revisa las condiciones de arriba hacia abajo y entra en la <strong>primera</strong> verdadera; las demás las ignora."),
)


# ======================================================================
#  Capítulo 7 — Bucles
# ======================================================================
cap7 = capitulo(
    "cap-7", "7. Bucles: while y for",
    h2("7.1. while: repetir mientras...", "while"),
    p("<code>while</code> repite un bloque mientras una condición sea verdadera:"),
    code('''
        hp_rival = 100
        while hp_rival > 0:
            print(f"Atacás. HP del rival: {hp_rival}")
            hp_rival = hp_rival - 20

        print("¡Ganaste la batalla! 🏆")
    '''),
    caja("""¡Cuidado con los bucles infinitos! Si la condición nunca se vuelve falsa,
    el programa no termina nunca. Asegurate de que algo cambie adentro (acá, el HP baja).""", "cuidado"),

    h2("7.2. for y range()", "for"),
    p("<code>for</code> recorre una secuencia de valores. <code>range()</code> genera números, ideal para repetir N veces:"),
    code('''
        for i in range(5):           # 0, 1, 2, 3, 4
            print(f"Pokéball número {i + 1}")

        for nivel in range(1, 11):   # del 1 al 10 (el 11 NO se incluye)
            print(nivel)

        equipo = ["Pikachu", "Charizard"]
        for pokemon in equipo:       # recorre una lista
            print(f"Tengo a {pokemon}")
    '''),
    caja("Recordá: <code>range(5)</code> da <code>0, 1, 2, 3, 4</code> (empieza en 0, termina antes del 5).", "nota"),

    h2("7.3. break y continue", "break-continue"),
    p("<code>break</code> corta el bucle por completo; <code>continue</code> saltea el resto de esta vuelta y pasa a la siguiente:"),
    code('''
        for pokemon in equipo:
            if pokemon == "Mewtwo":
                print("¡Lo encontramos!")
                break          # salimos del for
    '''),
)


# ======================================================================
#  Capítulo 8 — Funciones
# ======================================================================
cap8 = capitulo(
    "cap-8", "8. Funciones",
    p("""Una <strong>función</strong> es un bloque de código con nombre que escribís
    una vez y usás muchas. Es como un ataque que tu Pokémon aprende una vez y usa mil veces."""),
    code('''
        def saludar(nombre):
            print(f"¡Hola, {nombre}!")

        saludar("Ash")      # ¡Hola, Ash!
        saludar("Misty")    # ¡Hola, Misty!
    '''),

    h2("8.1. return: devolver un resultado", "return"),
    p("<code>return</code> hace que la función devuelva un valor para usarlo después:"),
    code('''
        def calcular_dano(ataque, defensa):
            return ataque - defensa

        resultado = calcular_dano(50, 20)
        print(resultado)    # 30
    '''),
    caja("""<strong>print vs return:</strong> <code>print</code> solo MUESTRA;
    <code>return</code> DEVUELVE un valor que podés seguir usando. Si querés usar el
    resultado después, usá <code>return</code>.""", "clave"),

    h2("8.2. Valores por defecto", "defecto"),
    code('''
        def atacar(nombre, dano=10):     # dano vale 10 si no se especifica
            print(f"{nombre} hizo {dano} de daño")

        atacar("Pikachu")        # Pikachu hizo 10 de daño
        atacar("Charizard", 35)  # Charizard hizo 35 de daño
    '''),

    h2("8.3. Recursión", "recursion"),
    p("Una función puede llamarse a sí misma. Siempre necesita un <strong>caso base</strong> que la frene:"),
    code('''
        def factorial(n):
            if n <= 1:           # caso base
                return 1
            return n * factorial(n - 1)   # caso recursivo

        print(factorial(5))    # 120
    '''),
)


# ======================================================================
#  Capítulo 9 — Listas y tuplas
# ======================================================================
cap9 = capitulo(
    "cap-9", "9. Listas y tuplas",
    p("Una <strong>lista</strong> es una colección ordenada y modificable. Se escribe entre corchetes. Es como tu equipo Pokémon:"),
    code('''
        equipo = ["Pikachu", "Charizard", "Snorlax"]
        print(equipo[0])    # Pikachu  (¡los índices empiezan en 0!)
        print(equipo[-1])   # Snorlax  (el último)

        equipo.append("Mewtwo")     # agrega al final
        equipo.remove("Charizard")  # borra por valor
        print(len(equipo))          # cantidad de elementos
        print("Pikachu" in equipo)  # ¿está? -> True
    '''),

    h2("9.1. Comprensiones de listas", "comprensiones"),
    p("Arman una lista nueva en una sola línea. Muy "+inline("pythónico")+":"),
    code('''
        niveles = [25, 50, 40, 15]
        dobles = [n * 2 for n in niveles]          # [50, 100, 80, 30]
        altos = [n for n in niveles if n >= 40]    # [50, 40]  (con filtro)
    '''),

    h2("9.2. Tuplas", "tuplas"),
    p("Una <strong>tupla</strong> es como una lista pero <strong>inmutable</strong> (no se puede cambiar). Se usa para datos fijos. Se escribe con paréntesis:"),
    code('''
        coordenada = (10, 20)
        print(coordenada[0])    # 10
        # coordenada[0] = 5     # ❌ ERROR: una tupla no se modifica
    '''),
)


# ======================================================================
#  Capítulo 10 — Diccionarios y conjuntos
# ======================================================================
cap10 = capitulo(
    "cap-10", "10. Diccionarios y conjuntos",
    p("Un <strong>diccionario</strong> guarda pares <strong>clave: valor</strong>. Es como una Pokédex: buscás por nombre y obtenés los datos:"),
    code('''
        pikachu = {
            "nombre": "Pikachu",
            "tipo": "Electrico",
            "nivel": 25,
        }
        print(pikachu["nombre"])        # Pikachu
        pikachu["nivel"] = 26           # cambiar un valor
        pikachu["ataque"] = 55          # agregar una clave nueva
        print(pikachu.get("defensa", 0))  # .get devuelve un default si no está
    '''),
    p("Para recorrerlo, usá <code>.items()</code>:"),
    code('''
        for clave, valor in pikachu.items():
            print(f"{clave}: {valor}")
    '''),

    h2("10.1. Conjuntos (sets)", "sets"),
    p("Un <strong>set</strong> guarda elementos únicos, sin repetidos. Ideal para sacar duplicados:"),
    code('''
        capturados = ["Pikachu", "Pidgey", "Pikachu", "Rattata"]
        unicos = set(capturados)
        print(len(unicos))    # 3 (sin contar el Pikachu repetido)
    '''),

    h2("10.2. Resumen de colecciones", "resumen-colecciones"),
    tabla(
        ["Colección", "Símbolo", "Característica"],
        [
            ["Lista", "<code>[ ]</code>", "Ordenada, modificable"],
            ["Tupla", "<code>( )</code>", "Ordenada, inmutable"],
            ["Set", "<code>{ }</code>", "Única, sin orden"],
            ["Diccionario", "<code>{clave: valor}</code>", "Pares clave-valor"],
        ],
    ),
)


# ======================================================================
#  Capítulo 11 — Archivos y errores
# ======================================================================
cap11 = capitulo(
    "cap-11", "11. Archivos y manejo de errores",
    p("Para que tus datos sobrevivan al cerrar el programa, los guardás en <strong>archivos</strong>. La forma recomendada es con <code>with</code>, que cierra el archivo solo:"),
    code('''
        # Escribir (¡el modo "w" pisa lo que había!)
        with open("equipo.txt", "w", encoding="utf-8") as archivo:
            archivo.write("Pikachu\\n")     # \\n = salto de línea
            archivo.write("Charizard\\n")

        # Leer línea por línea
        with open("equipo.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                print(linea.strip())   # strip saca el \\n del final
    '''),
    caja("""Modos de <code>open()</code>: <code>"r"</code> leer, <code>"w"</code>
    escribir (reemplaza), <code>"a"</code> agregar al final.""", "nota"),

    h2("11.1. try / except", "try-except"),
    p("Un error puede romper tu programa. Con <code>try</code>/<code>except</code> lo atrapás y seguís adelante:"),
    code('''
        try:
            numero = int(input("Nivel: "))
            print(f"El nivel es {numero}")
        except ValueError:
            print("Eso no es un número válido")
    '''),
    caja("""Atrapá errores específicos (como <code>ValueError</code> o
    <code>FileNotFoundError</code>), no un <code>except:</code> pelado.""", "tip"),
)


# ======================================================================
#  Capítulo 12 — POO
# ======================================================================
cap12 = capitulo(
    "cap-12", "12. Programación orientada a objetos (POO)",
    p("""La POO te deja crear tus propios "moldes". Una <strong>clase</strong> es el
    molde (la especie Pikachu); un <strong>objeto</strong> es un individuo hecho con
    ese molde (tu Pikachu concreto)."""),
    code('''
        class Pokemon:
            def __init__(self, nombre, tipo, nivel):
                # self es el propio objeto. Guardamos sus datos (atributos).
                self.nombre = nombre
                self.tipo = tipo
                self.nivel = nivel
                self.hp = 100

            def atacar(self):                 # un método (una acción)
                return f"{self.nombre} ataca con tipo {self.tipo}!"

            def __str__(self):                # texto lindo para print()
                return f"{self.nombre} (Nivel {self.nivel})"

        pikachu = Pokemon("Pikachu", "Electrico", 25)
        print(pikachu.atacar())   # Pikachu ataca con tipo Electrico!
        print(pikachu)            # Pikachu (Nivel 25)
    '''),
    caja("""<code>__init__</code> es el <strong>constructor</strong>: se ejecuta
    automáticamente al crear el objeto. <code>self</code> es el propio objeto y va
    como primer parámetro de los métodos (pero no lo pasás al llamarlos).""", "clave"),
)


# ======================================================================
#  Capítulo 13 — POO avanzado
# ======================================================================
cap13 = capitulo(
    "cap-13", "13. POO avanzado: herencia y polimorfismo",
    p("La <strong>herencia</strong> deja que una clase hija reciba todo lo de una clase padre, y agregue o cambie lo suyo:"),
    code('''
        class Pokemon:
            def __init__(self, nombre):
                self.nombre = nombre
            def atacar(self):
                return f"{self.nombre} usa un ataque normal"

        class PokemonFuego(Pokemon):       # hereda de Pokemon
            def atacar(self):              # SOBRESCRIBE el método (polimorfismo)
                return f"{self.nombre} usa Lanzallamas! 🔥"

        equipo = [PokemonFuego("Charizard"), Pokemon("Rattata")]
        for p in equipo:
            print(p.atacar())   # cada uno responde a su manera
    '''),
    caja("""<strong>Polimorfismo</strong> = "muchas formas": el mismo método
    (<code>atacar</code>) se comporta distinto según la clase. Así evitás llenar el
    código de <code>if tipo == ...</code>.""", "clave"),
    p("También existen <code>super()</code> (llamar al padre), <code>@property</code> (usar un método como atributo) y las clases abstractas con el módulo <code>abc</code>. Lo ves en detalle en la semana 9 del curso."),
)


# ======================================================================
#  Capítulo 14 — Módulos y pip
# ======================================================================
cap14 = capitulo(
    "cap-14", "14. Módulos, pip y entornos virtuales",
    p("Un <strong>módulo</strong> es código ya hecho que importás. Python trae muchos de fábrica (la librería estándar):"),
    code('''
        import math
        import random

        print(math.sqrt(16))                 # 4.0
        print(random.choice(["Pikachu", "Onix"]))  # uno al azar
    '''),
    p("También podés crear tus propios módulos (cualquier archivo <code>.py</code>) e importarlos, e instalar librerías externas con <strong>pip</strong>:"),
    code("pip install requests", lang="bash"),
    caja("""Un <strong>entorno virtual</strong> (<code>venv</code>) es una cajita
    aislada con las librerías de tu proyecto, separada del Python del sistema. El
    <code>setup.sh</code> del curso lo crea por vos.""", "nota"),
    p("Y con <code>requests</code> podés traer datos reales de internet, como de la PokéAPI:"),
    code('''
        import requests
        datos = requests.get("https://pokeapi.co/api/v2/pokemon/pikachu").json()
        print(datos["name"])    # pikachu
    '''),
)


# ======================================================================
#  Capítulo 15 — Mapa del curso (índice de temas)
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
#  Capítulo 16 — Tests, FAQ y glosario
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
    darte EXP.""", "nota"),

    h2("18.2. Preguntas frecuentes", "faq"),
    p("<strong>¿Por dónde empiezo?</strong> Por la Liga: <code>python aventura.py</code>. Después seguí la semana 01."),
    p("<strong>Me sale \"command not found: python\".</strong> Probá con <code>python3</code>."),
    p("<strong>Los tests me dan rojo. ¿Está mal?</strong> Significa que tu solución todavía no es correcta. Leé el error (está en español), corregí y volvé a probar. Es normal."),
    p("<strong>¿Puedo ver las soluciones?</strong> Sí, pero intentá primero vos. Mirar sin intentar es como usar un truco: ganás pero no aprendés."),

    h2("18.3. Glosario", "glosario"),
    tabla(
        ["Palabra", "Qué significa"],
        [
            ["Terminal", "La ventana donde escribís comandos de texto."],
            ["Variable", 'Una "caja con nombre" donde guardás un dato.'],
            ["Función", "Un bloque de código con nombre que podés reusar."],
            ["Test", "Un programa que revisa si tu código funciona bien."],
            ["EXP", "Puntos de experiencia que ganás en la Liga al pasar tests."],
            ["Commit", "Un punto de guardado de tu código en Git."],
            ["venv", "Entorno virtual: cajita aislada con las librerías del curso."],
        ],
    ),
)


# ======================================================================
#  Capítulo 15 — Linux: la terminal (semana 1 del curso)
# ======================================================================
cap_linux1 = capitulo(
    "cap-linux1", "15. Linux: la terminal",
    p("""Esta parte cubre <strong>Linux</strong>, que en el curso ves en las semanas
    1 y 2 (antes de Python). La <strong>terminal</strong> es una ventana donde
    escribís comandos de texto y la computadora te responde."""),
    caja("""Pensá en la terminal como la <strong>Pokédex de tu sistema</strong>: una
    herramienta de texto, al principio rara, pero la más poderosa que vas a tener.
    Cada comando es un "ataque".""", "pokemon"),

    h2("15.1. Moverte por las carpetas", "linux-mover"),
    p("Tres comandos para ubicarte y viajar entre carpetas:"),
    code('''
        pwd            # ¿dónde estoy? muestra la carpeta actual
        ls             # ver qué hay acá (archivos y carpetas)
        ls -l          # en formato largo (permisos, tamaño, fecha)
        ls -a          # incluye archivos ocultos (empiezan con .)
        cd pokecenter  # entrar a una carpeta
        cd ..          # subir un nivel
        cd ~           # ir a tu carpeta personal (home)
    ''', lang="bash"),

    h2("15.2. Crear, copiar y borrar", "linux-crear"),
    code('''
        mkdir pokecenter        # crear una carpeta
        mkdir -p a/b/c          # crear carpetas anidadas de una
        touch pikachu.txt       # crear un archivo vacío
        echo "Electrico" > pikachu.txt   # escribir texto en un archivo
        cat pikachu.txt         # mostrar el contenido de un archivo
        cp pikachu.txt copia.txt   # copiar un archivo
        cp -r carpeta copia        # copiar una carpeta entera
        mv pikachu.txt raichu.txt  # renombrar (o mover)
        rm pikachu.txt          # borrar un archivo
        rm -r carpeta           # borrar una carpeta y todo lo de adentro
    ''', lang="bash"),
    caja("""En Linux <strong>no hay papelera de reciclaje</strong>: lo que borrás con
    <code>rm</code>, se va para siempre. Revisá siempre antes de borrar.""", "cuidado"),

    h2("15.3. Rutas absolutas y relativas", "linux-rutas"),
    p("""Una <strong>ruta absoluta</strong> empieza en la raíz <code>/</code> y vale
    desde cualquier lado. Una <strong>ruta relativa</strong> parte de donde estás parado."""),
    code('''
        cd /home/ash/pokecenter   # ruta absoluta (empieza con /)
        cd pokecenter/gimnasio    # ruta relativa (desde acá)
    ''', lang="bash"),
    ul(
        "<code>.</code> &rarr; la carpeta actual",
        "<code>..</code> &rarr; la carpeta de arriba",
        "<code>~</code> &rarr; tu home",
        "<code>/</code> &rarr; la raíz de todo",
    ),

    h2("15.4. Permisos básicos", "linux-permisos"),
    p("Cada archivo tiene permisos. Al correr <code>ls -l</code> ves algo como <code>-rwxr-xr--</code>:"),
    ul(
        "<code>r</code> = leer, <code>w</code> = escribir, <code>x</code> = ejecutar.",
        "Se agrupan de a 3: <strong>dueño</strong>, <strong>grupo</strong> y <strong>otros</strong>.",
    ),
    p("En la próxima parte vas a aprender a cambiarlos con <code>chmod</code>."),

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
#  Capítulo 16 — Linux: comandos intermedios (semana 2 del curso)
# ======================================================================
cap_linux2 = capitulo(
    "cap-linux2", "16. Linux: comandos intermedios",
    p("Ahora que te movés por la terminal, sumamos superpoderes: editar archivos, encadenar comandos, buscar, y automatizar con scripts."),

    h2("16.1. Editar con nano", "linux-nano"),
    p("<code>nano</code> es un editor de texto simple dentro de la terminal:"),
    code("nano notas.txt   # Ctrl+O para guardar, Ctrl+X para salir", lang="bash"),

    h2("16.2. Redirección y pipes", "linux-pipes"),
    p("Podés mandar la salida de un comando a un archivo, o encadenar comandos:"),
    code('''
        echo "Pikachu" > equipo.txt    # > CREA o REEMPLAZA el archivo
        echo "Charizard" >> equipo.txt # >> AGREGA al final
        cat equipo.txt | sort          # | (pipe) conecta dos comandos
        ls | wc -l                     # cuenta cuántos archivos hay
    ''', lang="bash"),
    caja("Ojo: <code>&gt;</code> pisa todo lo que había; <code>&gt;&gt;</code> agrega. No los confundas.", "cuidado"),

    h2("16.3. Buscar: grep y find", "linux-buscar"),
    code('''
        grep "Fuego" pokedex.txt    # busca TEXTO dentro de un archivo
        grep -i "fuego" pokedex.txt # -i ignora mayúsculas/minúsculas
        find . -name "*.txt"        # busca ARCHIVOS por nombre
    ''', lang="bash"),

    h2("16.4. Procesos y permisos", "linux-procesos"),
    code('''
        ps aux              # lista los procesos en ejecución
        ps aux | grep python   # filtra los de python
        kill 1234           # cierra el proceso con ese número (PID)
        chmod +x script.sh  # da permiso de EJECUCIÓN
        chmod 755 script.sh # forma numérica (rwx r-x r-x)
    ''', lang="bash"),

    h2("16.5. Tu primer script bash", "linux-scripts"),
    p("Un <strong>script</strong> es un archivo con una lista de comandos. Es tu máquina automática:"),
    code('''
        #!/usr/bin/env bash
        # La primera línea (shebang) dice que esto es un script bash.
        echo "¡Hola, Entrenador!"
        echo "Capturaste a: $1"   # $1 es el primer argumento
    ''', lang="bash"),
    p("Para correrlo, le das permiso y lo ejecutás:"),
    code('''
        chmod +x saludo.sh
        ./saludo.sh Snorlax    # ./ = "ejecutá este archivo de acá"
    ''', lang="bash"),

    h2("16.6. Instalar programas y SSH", "linux-apt-ssh"),
    code('''
        sudo apt update             # actualiza la lista de programas
        sudo apt install cowsay     # instala un programa
        ssh entrenador@192.168.1.50 # te conectás a otra máquina
    ''', lang="bash"),
    caja("""<code>sudo</code> ejecuta un comando como administrador (root). Es
    poderoso: no corras con <code>sudo</code> cosas que no entendés.""", "nota"),

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


# Lista final de capítulos, en orden.
CAPITULOS = [
    cap_intro, cap1, cap2, cap3, cap4, cap5, cap6, cap7, cap8,
    cap9, cap10, cap11, cap12, cap13, cap14,
    cap_linux1, cap_linux2,
    cap15, cap16,
]
