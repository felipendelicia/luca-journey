#!/usr/bin/env python3
"""
🧠 Quiz de Linux — Semana 02

20 preguntas de opción múltiple sobre Linux (semanas 1 y 2). Por cada respuesta
te decimos si acertaste y por qué. Al final ves tu puntaje y un mensaje según
qué tan bien te fue.

Cómo jugar:
    python quiz.py

Los datos de las preguntas y la lógica de corrección están separados de la
interacción, así los tests pueden verificarlos sin teclado.
"""

# Cada pregunta es un dict con:
#   - "enunciado": la pregunta.
#   - "opciones":  lista de respuestas posibles.
#   - "correcta":  índice (0-based) de la opción correcta.
#   - "explicacion": por qué esa es la respuesta.
PREGUNTAS = [
    {
        "enunciado": "¿Qué comando muestra en qué carpeta estás parado?",
        "opciones": ["ls", "pwd", "cd", "whereami"],
        "correcta": 1,
        "explicacion": "pwd = 'print working directory'. Muestra tu ubicación actual.",
    },
    {
        "enunciado": "¿Qué hace el comando 'ls -a'?",
        "opciones": [
            "Borra todos los archivos",
            "Lista archivos incluyendo los ocultos",
            "Ordena los archivos alfabéticamente",
            "Lista solo carpetas",
        ],
        "correcta": 1,
        "explicacion": "El flag -a (all) muestra también los archivos ocultos (los que empiezan con punto).",
    },
    {
        "enunciado": "¿Cómo subís a la carpeta de arriba (el nivel anterior)?",
        "opciones": ["cd up", "cd ..", "cd /", "cd ~"],
        "correcta": 1,
        "explicacion": "'cd ..' sube un nivel. '..' representa la carpeta padre.",
    },
    {
        "enunciado": "¿Qué símbolo representa tu carpeta personal (home)?",
        "opciones": ["/", "*", "~", "@"],
        "correcta": 2,
        "explicacion": "El '~' (virgulilla) es un atajo para tu carpeta home.",
    },
    {
        "enunciado": "¿Qué flag necesita 'mkdir' para crear carpetas anidadas de una vez?",
        "opciones": ["-r", "-a", "-p", "-n"],
        "correcta": 2,
        "explicacion": "'mkdir -p ruta/larga/nueva' crea todas las carpetas intermedias que falten.",
    },
    {
        "enunciado": "En Linux, cuando borrás un archivo con 'rm'...",
        "opciones": [
            "Va a la papelera de reciclaje",
            "Se borra para siempre, no hay papelera",
            "Se mueve a /tmp",
            "Se puede recuperar con Ctrl+Z",
        ],
        "correcta": 1,
        "explicacion": "rm borra definitivamente. ¡No hay papelera! Siempre revisá antes de borrar.",
    },
    {
        "enunciado": "¿Qué hace 'cat archivo.txt'?",
        "opciones": [
            "Borra el archivo",
            "Muestra el contenido del archivo",
            "Copia el archivo",
            "Crea un archivo de gatos",
        ],
        "correcta": 1,
        "explicacion": "cat muestra el contenido de un archivo en pantalla.",
    },
    {
        "enunciado": "¿Cuál es la diferencia entre '>' y '>>'?",
        "opciones": [
            "Son exactamente iguales",
            "'>' reemplaza el archivo, '>>' agrega al final",
            "'>' agrega, '>>' reemplaza",
            "'>>' solo funciona con números",
        ],
        "correcta": 1,
        "explicacion": "'>' pisa el contenido; '>>' agrega al final sin borrar lo anterior.",
    },
    {
        "enunciado": "¿Qué hace un pipe '|' ?",
        "opciones": [
            "Conecta la salida de un comando con la entrada de otro",
            "Borra archivos",
            "Crea una variable",
            "Apaga la computadora",
        ],
        "correcta": 0,
        "explicacion": "El pipe encadena comandos: la salida de uno se vuelve la entrada del siguiente.",
    },
    {
        "enunciado": "¿Qué comando busca TEXTO dentro de archivos?",
        "opciones": ["find", "grep", "locate", "search"],
        "correcta": 1,
        "explicacion": "grep busca texto dentro de archivos o de lo que le llega por pipe.",
    },
    {
        "enunciado": "¿Qué comando busca ARCHIVOS por su nombre?",
        "opciones": ["grep", "cat", "find", "ls"],
        "correcta": 2,
        "explicacion": "find busca archivos por nombre, tipo, etc. Ej: find . -name '*.txt'",
    },
    {
        "enunciado": "¿Qué hace 'chmod +x script.sh'?",
        "opciones": [
            "Borra el script",
            "Le da permiso de ejecución",
            "Lo renombra",
            "Lo ejecuta",
        ],
        "correcta": 1,
        "explicacion": "+x agrega el permiso de ejecución, necesario para correr un script con ./",
    },
    {
        "enunciado": "¿Con qué empieza la primera línea de un script bash (el shebang)?",
        "opciones": ["//", "#!", "$$", "@@"],
        "correcta": 1,
        "explicacion": "El shebang '#!' (ej: #!/usr/bin/env bash) indica qué programa ejecuta el script.",
    },
    {
        "enunciado": "¿Cómo se accede al valor de una variable llamada NOMBRE en bash?",
        "opciones": ["NOMBRE", "$NOMBRE", "&NOMBRE", "*NOMBRE"],
        "correcta": 1,
        "explicacion": "Se usa el '$' adelante: $NOMBRE. Sin el $, es solo texto.",
    },
    {
        "enunciado": "Al crear una variable en bash, ¿cuál es la forma correcta?",
        "opciones": [
            'NOMBRE = "Ash"',
            'NOMBRE="Ash"',
            'NOMBRE := "Ash"',
            'var NOMBRE = "Ash"',
        ],
        "correcta": 1,
        "explicacion": "Sin espacios alrededor del '='. NOMBRE=\"Ash\" es correcto.",
    },
    {
        "enunciado": "¿Qué comando muestra los procesos en ejecución?",
        "opciones": ["ps", "ls", "top-secret", "proc"],
        "correcta": 0,
        "explicacion": "ps muestra procesos. 'ps aux' muestra todos los del sistema.",
    },
    {
        "enunciado": "¿Para qué sirve 'kill 1234'?",
        "opciones": [
            "Crea el proceso 1234",
            "Termina el proceso con PID 1234",
            "Lista el proceso 1234",
            "Reinicia la computadora",
        ],
        "correcta": 1,
        "explicacion": "kill envía una señal para terminar el proceso con ese PID.",
    },
    {
        "enunciado": "¿Qué hace 'sudo'?",
        "opciones": [
            "Ejecuta un comando como administrador (root)",
            "Apaga el sistema",
            "Sube un archivo a internet",
            "Borra el sistema",
        ],
        "correcta": 0,
        "explicacion": "sudo ejecuta un comando con permisos de root. Usalo con cuidado.",
    },
    {
        "enunciado": "En Ubuntu/Debian, ¿qué se usa para instalar programas?",
        "opciones": ["install", "apt", "get", "brew"],
        "correcta": 1,
        "explicacion": "apt es el gestor de paquetes. Ej: sudo apt install cowsay",
    },
    {
        "enunciado": "¿Para qué sirve SSH?",
        "opciones": [
            "Para editar archivos",
            "Para conectarte y controlar otra máquina de forma segura",
            "Para comprimir archivos",
            "Para ver imágenes",
        ],
        "correcta": 1,
        "explicacion": "SSH (Secure Shell) te da una terminal en otra computadora, de forma segura.",
    },
]


def corregir(pregunta, indice_respuesta):
    """
    Devuelve (es_correcta, explicacion).
    'indice_respuesta' es 0-based.
    """
    es_correcta = indice_respuesta == pregunta["correcta"]
    return es_correcta, pregunta["explicacion"]


def mensaje_final(puntaje, total):
    """Devuelve un mensaje motivador según el puntaje."""
    porcentaje = (puntaje / total) * 100 if total else 0
    if porcentaje == 100:
        return "🏆 ¡PERFECTO! Sos un Maestro de Linux. ¡Increíble!"
    elif porcentaje >= 80:
        return "🥇 ¡Muy bien! Dominás Linux casi por completo."
    elif porcentaje >= 60:
        return "🥈 ¡Bien! Vas por buen camino. Repasá lo que fallaste."
    elif porcentaje >= 40:
        return "🥉 Aprobado, pero conviene repasar la teoría de nuevo."
    else:
        return "📚 Tranqui, esto recién empieza. Releé teoria.md y volvé a intentar."


def jugar():
    print("=" * 60)
    print("🧠  QUIZ DE LINUX — Semana 02")
    print("=" * 60)
    print(f"Son {len(PREGUNTAS)} preguntas. Respondé con el número de la opción.\n")

    puntaje = 0
    for numero, pregunta in enumerate(PREGUNTAS, start=1):
        print(f"\n❓ Pregunta {numero}/{len(PREGUNTAS)}: {pregunta['enunciado']}")
        for i, opcion in enumerate(pregunta["opciones"], start=1):
            print(f"   {i}) {opcion}")

        # Pedimos una respuesta válida.
        while True:
            try:
                respuesta = input("   Tu respuesta (número) > ")
            except (EOFError, KeyboardInterrupt):
                print("\n¡Chau! 👋")
                return
            if respuesta.strip().isdigit():
                idx = int(respuesta) - 1
                if 0 <= idx < len(pregunta["opciones"]):
                    break
            print("   ⚠️ Escribí el número de una opción válida.")

        es_correcta, explicacion = corregir(pregunta, idx)
        if es_correcta:
            print("   ✅ ¡Correcto!")
            puntaje += 1
        else:
            correcta_texto = pregunta["opciones"][pregunta["correcta"]]
            print(f"   ❌ Incorrecto. La respuesta era: {correcta_texto}")
        print(f"   💡 {explicacion}")

    print("\n" + "=" * 60)
    print(f"🎯 Puntaje final: {puntaje}/{len(PREGUNTAS)}")
    print(mensaje_final(puntaje, len(PREGUNTAS)))
    print("=" * 60)


if __name__ == "__main__":
    jugar()
