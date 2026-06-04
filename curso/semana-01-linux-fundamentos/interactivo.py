#!/usr/bin/env python3
"""
🐧 Simulador de Terminal Pokémon — Semana 01

Un "simulador" de terminal Linux con temática Pokémon. Tiene un árbol de
archivos VIRTUAL (en memoria), así que podés practicar comandos sin miedo a
romper tu computadora de verdad.

Te presenta 10 desafíos progresivos. En cada uno tenés que escribir el comando
correcto. El simulador te dice si lo hiciste bien o mal.

Cómo jugar:
    python interactivo.py

Comandos soportados (versiones simplificadas de los reales):
    pwd, ls, ls -a, cd, mkdir, touch, cat, echo "texto" > archivo, rm, rm -r, help

El código está separado en una clase 'TerminalVirtual' (la lógica) y la función
'jugar()' (la interacción). Así los tests pueden probar la lógica sin teclado.
"""

import shlex


# ======================================================================
#  LA TERMINAL VIRTUAL — toda la lógica vive acá adentro.
# ======================================================================
class TerminalVirtual:
    """
    Simula una terminal Linux con un sistema de archivos en memoria.

    El sistema de archivos se representa con diccionarios anidados:
      - Una carpeta es un dict: {nombre: contenido}
      - Un archivo es un string con su contenido.

    Ejemplo de árbol inicial:
      {
        "home": {
          "entrenador": {
            "bienvenida.txt": "Hola Entrenador!"
          }
        }
      }
    """

    def __init__(self):
        # El árbol arranca con una estructura temática Pokémon.
        self.raiz = {
            "home": {
                "entrenador": {
                    "bienvenida.txt": "Bienvenido al mundo Pokemon!",
                    "mochila": {
                        "pociones.txt": "5 pociones",
                        "pokeballs.txt": "10 pokeballs",
                    },
                }
            }
        }
        # La ruta actual se guarda como lista de carpetas desde la raíz.
        # Arrancamos en /home/entrenador (el "home" del usuario).
        self.ruta_actual = ["home", "entrenador"]

    # ------------------------------------------------------------------
    #  Helpers internos para movernos por el árbol.
    # ------------------------------------------------------------------
    def _carpeta_actual(self):
        """Devuelve el dict de la carpeta donde estamos parados."""
        nodo = self.raiz
        for parte in self.ruta_actual:
            nodo = nodo[parte]
        return nodo

    def _resolver(self, ruta):
        """
        Convierte una ruta (relativa o absoluta) en una lista de partes,
        resolviendo '.', '..' y '~'. Devuelve la lista o None si es inválida.
        """
        if ruta in ("~", ""):
            return ["home", "entrenador"]

        if ruta.startswith("/"):
            partes_base = []           # ruta absoluta: arranca desde la raíz
            resto = ruta.strip("/")
        elif ruta.startswith("~"):
            partes_base = ["home", "entrenador"]
            resto = ruta[1:].strip("/")
        else:
            partes_base = list(self.ruta_actual)  # ruta relativa
            resto = ruta.strip("/")

        partes = partes_base
        for parte in (resto.split("/") if resto else []):
            if parte in (".", ""):
                continue
            elif parte == "..":
                if partes:
                    partes = partes[:-1]
            else:
                partes = partes + [parte]
        return partes

    def _nodo_en(self, partes):
        """Devuelve el nodo (dict o str) en esa ruta, o None si no existe."""
        nodo = self.raiz
        for parte in partes:
            if isinstance(nodo, dict) and parte in nodo:
                nodo = nodo[parte]
            else:
                return None
        return nodo

    # ------------------------------------------------------------------
    #  Los comandos. Cada uno devuelve un string con la salida.
    # ------------------------------------------------------------------
    def pwd(self):
        """Devuelve la ruta absoluta actual."""
        return "/" + "/".join(self.ruta_actual)

    def ls(self, mostrar_ocultos=False):
        """Lista el contenido de la carpeta actual, ordenado."""
        carpeta = self._carpeta_actual()
        nombres = sorted(carpeta.keys())
        if not mostrar_ocultos:
            nombres = [n for n in nombres if not n.startswith(".")]
        return "  ".join(nombres)

    def cd(self, destino):
        """Cambia de carpeta. Devuelve "" si OK, o un mensaje de error."""
        partes = self._resolver(destino)
        nodo = self._nodo_en(partes)
        if nodo is None:
            return f"cd: no existe la carpeta '{destino}'"
        if not isinstance(nodo, dict):
            return f"cd: '{destino}' no es una carpeta"
        self.ruta_actual = partes
        return ""

    def mkdir(self, nombre):
        """Crea una carpeta en la ubicación actual."""
        if not nombre:
            return "mkdir: falta el nombre de la carpeta"
        carpeta = self._carpeta_actual()
        if nombre in carpeta:
            return f"mkdir: '{nombre}' ya existe"
        carpeta[nombre] = {}
        return ""

    def touch(self, nombre):
        """Crea un archivo vacío en la ubicación actual."""
        if not nombre:
            return "touch: falta el nombre del archivo"
        carpeta = self._carpeta_actual()
        if nombre not in carpeta:
            carpeta[nombre] = ""
        return ""

    def cat(self, nombre):
        """Muestra el contenido de un archivo."""
        carpeta = self._carpeta_actual()
        if nombre not in carpeta:
            return f"cat: '{nombre}' no existe"
        if isinstance(carpeta[nombre], dict):
            return f"cat: '{nombre}' es una carpeta"
        return carpeta[nombre]

    def echo(self, texto, archivo=None):
        """Imprime texto, o lo guarda en un archivo si se pasa 'archivo'."""
        if archivo is None:
            return texto
        carpeta = self._carpeta_actual()
        carpeta[archivo] = texto
        return ""

    def rm(self, nombre, recursivo=False):
        """Borra un archivo (o carpeta si recursivo=True)."""
        carpeta = self._carpeta_actual()
        if nombre not in carpeta:
            return f"rm: '{nombre}' no existe"
        if isinstance(carpeta[nombre], dict) and not recursivo:
            return f"rm: '{nombre}' es una carpeta (usá rm -r)"
        del carpeta[nombre]
        return ""

    # ------------------------------------------------------------------
    #  El intérprete: recibe una línea de texto y la ejecuta.
    # ------------------------------------------------------------------
    def ejecutar(self, linea):
        """
        Recibe una línea como la escribiría el usuario (ej: 'mkdir gimnasio')
        y devuelve la salida en texto. Es el corazón del simulador.
        """
        linea = linea.strip()
        if not linea:
            return ""

        # Caso especial: redirección con > (ej: echo "hola" > archivo.txt)
        if ">" in linea and linea.split()[0] == "echo":
            izquierda, _, derecha = linea.partition(">")
            archivo = derecha.strip()
            # Sacamos 'echo' y comillas del texto de la izquierda.
            try:
                partes_izq = shlex.split(izquierda)
            except ValueError:
                partes_izq = izquierda.split()
            texto = " ".join(partes_izq[1:])
            return self.echo(texto, archivo)

        try:
            partes = shlex.split(linea)
        except ValueError:
            partes = linea.split()

        comando = partes[0]
        args = partes[1:]

        if comando == "pwd":
            return self.pwd()
        elif comando == "ls":
            return self.ls(mostrar_ocultos=("-a" in args))
        elif comando == "cd":
            return self.cd(args[0] if args else "~")
        elif comando == "mkdir":
            # Soporta varios nombres: mkdir a b c
            nombres = [a for a in args if not a.startswith("-")]
            salidas = [self.mkdir(n) for n in nombres]
            return "\n".join(s for s in salidas if s)
        elif comando == "touch":
            nombres = [a for a in args if not a.startswith("-")]
            salidas = [self.touch(n) for n in nombres]
            return "\n".join(s for s in salidas if s)
        elif comando == "cat":
            return self.cat(args[0]) if args else "cat: falta el archivo"
        elif comando == "echo":
            return self.echo(" ".join(args))
        elif comando == "rm":
            recursivo = "-r" in args or "-rf" in args
            nombres = [a for a in args if not a.startswith("-")]
            salidas = [self.rm(n, recursivo) for n in nombres]
            return "\n".join(s for s in salidas if s)
        elif comando == "help":
            return AYUDA
        else:
            return f"{comando}: comando no encontrado (probá 'help')"


AYUDA = """Comandos disponibles:
  pwd                       muestra la carpeta actual
  ls [-a]                   lista archivos (con -a muestra ocultos)
  cd <carpeta>              cambia de carpeta (.. sube, ~ va al home)
  mkdir <nombre>            crea una carpeta
  touch <archivo>           crea un archivo vacio
  cat <archivo>             muestra el contenido de un archivo
  echo "texto" > <archivo>  escribe texto en un archivo
  rm [-r] <nombre>          borra un archivo (o carpeta con -r)
  help                      muestra esta ayuda"""


# ======================================================================
#  LOS DESAFÍOS — cada uno tiene una consigna y una forma de verificar.
# ======================================================================
# Cada desafío es un dict con:
#   - "consigna": qué tiene que lograr el jugador.
#   - "pista":    una ayuda.
#   - "check":    función(terminal) -> bool, devuelve True si está cumplido.
DESAFIOS = [
    {
        "consigna": "Mostrá en qué carpeta estás parado.",
        "pista": "El comando que imprime tu ubicación actual.",
        "check": lambda t, ultima_salida: ultima_salida == "/home/entrenador",
    },
    {
        "consigna": "Listá el contenido de la carpeta actual.",
        "pista": "El comando para 'ver alrededor'.",
        "check": lambda t, s: "bienvenida.txt" in s,
    },
    {
        "consigna": "Creá una carpeta llamada 'pokecenter'.",
        "pista": "mkdir <nombre>",
        "check": lambda t, s: "pokecenter" in t._carpeta_actual(),
    },
    {
        "consigna": "Entrá a la carpeta 'pokecenter'.",
        "pista": "cd <carpeta>",
        "check": lambda t, s: t.ruta_actual[-1] == "pokecenter",
    },
    {
        "consigna": "Creá un archivo vacío llamado 'pikachu.txt'.",
        "pista": "touch <archivo>",
        "check": lambda t, s: "pikachu.txt" in t._carpeta_actual(),
    },
    {
        "consigna": "Escribí 'Tipo Electrico' dentro de 'pikachu.txt'.",
        "pista": 'echo "texto" > archivo',
        "check": lambda t, s: t._carpeta_actual().get("pikachu.txt") == "Tipo Electrico",
    },
    {
        "consigna": "Mostrá el contenido de 'pikachu.txt'.",
        "pista": "cat <archivo>",
        "check": lambda t, s: s == "Tipo Electrico",
    },
    {
        "consigna": "Creá una carpeta 'gimnasio' y entrá en ella.",
        "pista": "Primero mkdir, después cd.",
        "check": lambda t, s: t.ruta_actual[-1] == "gimnasio",
    },
    {
        "consigna": "Volvé a la carpeta de arriba (pokecenter).",
        "pista": "cd ..",
        "check": lambda t, s: t.ruta_actual[-1] == "pokecenter",
    },
    {
        "consigna": "Borrá el archivo 'pikachu.txt'.",
        "pista": "rm <archivo>",
        "check": lambda t, s: "pikachu.txt" not in t._carpeta_actual(),
    },
]


# ======================================================================
#  LA INTERACCIÓN — el bucle de juego con el usuario.
# ======================================================================
def jugar():
    """Corre el simulador interactivo en la terminal."""
    print("=" * 60)
    print("🐧  SIMULADOR DE TERMINAL POKÉMON — Semana 01")
    print("=" * 60)
    print("Resolvé los 10 desafíos escribiendo comandos.")
    print("Escribí 'help' para ver los comandos, 'pista' para una ayuda,")
    print("o 'salir' para terminar.\n")

    terminal = TerminalVirtual()
    indice = 0

    while indice < len(DESAFIOS):
        desafio = DESAFIOS[indice]
        print(f"\n🎯 Desafío {indice + 1}/{len(DESAFIOS)}: {desafio['consigna']}")

        # Prompt falso al estilo Linux.
        prompt = f"entrenador@pokemon:{terminal.pwd()}$ "
        try:
            linea = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print("\n¡Hasta la próxima, Entrenador! 👋")
            return

        if linea.strip() == "salir":
            print("¡Hasta la próxima, Entrenador! 👋")
            return
        if linea.strip() == "pista":
            print(f"💡 Pista: {desafio['pista']}")
            continue

        # Ejecutamos el comando y mostramos su salida.
        salida = terminal.ejecutar(linea)
        if salida:
            print(salida)

        # Verificamos si el desafío quedó cumplido.
        if desafio["check"](terminal, salida):
            print("✅ ¡Correcto! Pasás al siguiente desafío.")
            indice += 1
        # Si no se cumplió, el jugador sigue intentando el mismo desafío.

    print("\n" + "=" * 60)
    print("🏆 ¡FELICITACIONES! Completaste los 10 desafíos.")
    print("Ya sabés moverte por una terminal Linux. ¡Sos un crack!")
    print("=" * 60)


if __name__ == "__main__":
    jugar()
