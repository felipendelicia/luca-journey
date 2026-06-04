#!/usr/bin/env python3
"""
🔀 Simulador de Git — Semana de Descanso

Un simulador de Git con un repositorio VIRTUAL (en memoria). Practicá los
comandos de Git sin miedo a romper nada. Tiene 10 desafíos progresivos.

Cómo jugar:
    python interactivo.py

Comandos soportados (versiones simplificadas):
    git init, git status, git add <archivo>, git add ., git commit -m "msg",
    git log, git branch [nombre], git switch <rama>, git switch -c <rama>,
    git checkout <rama>, git merge <rama>, touch <archivo>, echo "x" > archivo,
    ls, help

La clase 'RepoVirtual' tiene toda la lógica (testeable). 'jugar()' es la interfaz.
"""

import shlex


class RepoVirtual:
    """Simula un repositorio Git en memoria."""

    def __init__(self):
        self.iniciado = False
        # Directorio de trabajo: archivo -> contenido.
        self.working = {}
        # Staging area: archivo -> contenido preparado.
        self.staging = {}
        # Lista global de commits: {"msg", "rama", "hash"}.
        self.commits = []
        # Árbol de archivos guardado por rama: rama -> {archivo: contenido}.
        self.branch_tree = {}
        # Rama actual.
        self.current_branch = None
        # Para que los desafíos sepan qué comando se corrió último.
        self.ultimo_comando = None
        self._contador_hash = 0

    # ------------------------------------------------------------------
    #  Comandos
    # ------------------------------------------------------------------
    def init(self):
        if self.iniciado:
            return "Ya existe un repositorio Git en esta carpeta."
        self.iniciado = True
        self.current_branch = "main"
        self.branch_tree["main"] = {}
        return "Repositorio Git inicializado (rama 'main')."

    def crear_archivo(self, nombre, contenido=""):
        self.working[nombre] = contenido
        return ""

    def ls(self):
        if not self.working:
            return "(carpeta vacía)"
        return "  ".join(sorted(self.working.keys()))

    def status(self):
        if not self.iniciado:
            return "fatal: no es un repositorio git (probá 'git init')."
        lineas = [f"En la rama {self.current_branch}"]
        tree = self.branch_tree[self.current_branch]

        staged = sorted(self.staging.keys())
        # "Untracked": en working, ni en staging ni guardado en la rama.
        untracked = sorted(
            f for f in self.working
            if f not in self.staging and f not in tree
        )
        # "Modificados": en working y en la rama, pero con distinto contenido y sin preparar.
        modificados = sorted(
            f for f in self.working
            if f in tree and f not in self.staging and self.working[f] != tree[f]
        )

        if staged:
            lineas.append("Cambios preparados para el commit:")
            for f in staged:
                lineas.append(f"    nuevo archivo: {f}")
        if modificados:
            lineas.append("Cambios no preparados:")
            for f in modificados:
                lineas.append(f"    modificado: {f}")
        if untracked:
            lineas.append("Archivos sin seguimiento (untracked):")
            for f in untracked:
                lineas.append(f"    {f}")
        if not staged and not modificados and not untracked:
            lineas.append("nada para commitear, el árbol de trabajo está limpio")
        return "\n".join(lineas)

    def add(self, objetivo):
        if not self.iniciado:
            return "fatal: no es un repositorio git."
        if objetivo == ".":
            # Prepara todos los archivos del working.
            for nombre, contenido in self.working.items():
                self.staging[nombre] = contenido
            return ""
        if objetivo not in self.working:
            return f"fatal: la ruta '{objetivo}' no coincide con ningún archivo."
        self.staging[objetivo] = self.working[objetivo]
        return ""

    def commit(self, mensaje):
        if not self.iniciado:
            return "fatal: no es un repositorio git."
        if not self.staging:
            return "nada para commitear (usá 'git add' primero)."
        if not mensaje:
            return "fatal: falta el mensaje del commit (usá -m \"mensaje\")."
        # Actualizamos el árbol de la rama con lo que está en staging.
        tree = dict(self.branch_tree[self.current_branch])
        tree.update(self.staging)
        self.branch_tree[self.current_branch] = tree
        # Creamos el commit con un "hash" cortito y falso.
        self._contador_hash += 1
        hash_corto = f"{self._contador_hash:07d}"
        self.commits.append({
            "msg": mensaje,
            "rama": self.current_branch,
            "hash": hash_corto,
        })
        cantidad = len(self.staging)
        self.staging = {}
        return f"[{self.current_branch} {hash_corto}] {mensaje}\n {cantidad} archivo(s) cambiado(s)"

    def log(self, oneline=False):
        if not self.iniciado:
            return "fatal: no es un repositorio git."
        if not self.commits:
            return "Todavía no hay commits."
        # Mostramos del más nuevo al más viejo.
        lineas = []
        for c in reversed(self.commits):
            if oneline:
                lineas.append(f"{c['hash']} {c['msg']}")
            else:
                lineas.append(f"commit {c['hash']} (rama: {c['rama']})")
                lineas.append(f"    {c['msg']}")
        return "\n".join(lineas)

    def branch(self, nombre=None):
        if not self.iniciado:
            return "fatal: no es un repositorio git."
        if nombre is None:
            # Lista las ramas; la actual con un *.
            lineas = []
            for r in sorted(self.branch_tree.keys()):
                marca = "* " if r == self.current_branch else "  "
                lineas.append(f"{marca}{r}")
            return "\n".join(lineas)
        if nombre in self.branch_tree:
            return f"fatal: la rama '{nombre}' ya existe."
        # La rama nueva arranca con una copia del árbol actual.
        self.branch_tree[nombre] = dict(self.branch_tree[self.current_branch])
        return ""

    def switch(self, nombre, crear=False):
        if not self.iniciado:
            return "fatal: no es un repositorio git."
        if crear:
            if nombre in self.branch_tree:
                return f"fatal: la rama '{nombre}' ya existe."
            self.branch_tree[nombre] = dict(self.branch_tree[self.current_branch])
        if nombre not in self.branch_tree:
            return f"fatal: la rama '{nombre}' no existe (creala con -c)."
        self.current_branch = nombre
        # Al cambiar de rama, el working refleja el árbol de esa rama.
        self.working = dict(self.branch_tree[nombre])
        self.staging = {}
        return f"Cambiado a la rama '{nombre}'"

    def merge(self, rama):
        if not self.iniciado:
            return "fatal: no es un repositorio git."
        if rama not in self.branch_tree:
            return f"fatal: la rama '{rama}' no existe."
        if rama == self.current_branch:
            return "No se puede fusionar una rama consigo misma."
        # Traemos los archivos de la otra rama a la actual.
        tree = dict(self.branch_tree[self.current_branch])
        tree.update(self.branch_tree[rama])
        self.branch_tree[self.current_branch] = tree
        self.working = dict(tree)
        return f"Fusionada la rama '{rama}' en '{self.current_branch}'."

    # ------------------------------------------------------------------
    #  Intérprete de líneas
    # ------------------------------------------------------------------
    def ejecutar(self, linea):
        """Recibe una línea de texto y la ejecuta; devuelve la salida."""
        linea = linea.strip()
        if not linea:
            return ""

        # Redirección con echo: echo "texto" > archivo
        if linea.startswith("echo") and ">" in linea:
            izquierda, _, derecha = linea.partition(">")
            archivo = derecha.strip()
            try:
                partes = shlex.split(izquierda)
            except ValueError:
                partes = izquierda.split()
            contenido = " ".join(partes[1:])
            self.ultimo_comando = "echo"
            return self.crear_archivo(archivo, contenido)

        try:
            tokens = shlex.split(linea)
        except ValueError:
            tokens = linea.split()

        comando = tokens[0]

        if comando == "ls":
            self.ultimo_comando = "ls"
            return self.ls()
        if comando == "touch":
            self.ultimo_comando = "touch"
            for nombre in tokens[1:]:
                self.crear_archivo(nombre)
            return ""
        if comando == "help":
            return AYUDA
        if comando != "git":
            return f"{comando}: comando no encontrado (probá 'help')."

        # A partir de acá, comandos de git.
        if len(tokens) < 2:
            return "uso: git <comando> (probá 'help')."
        sub = tokens[1]
        args = tokens[2:]
        self.ultimo_comando = sub

        if sub == "init":
            return self.init()
        if sub == "status":
            return self.status()
        if sub == "add":
            return self.add(args[0]) if args else "Nada especificado para 'git add'."
        if sub == "commit":
            mensaje = ""
            if "-m" in args:
                i = args.index("-m")
                if i + 1 < len(args):
                    mensaje = args[i + 1]
            return self.commit(mensaje)
        if sub == "log":
            return self.log(oneline=("--oneline" in args))
        if sub == "branch":
            nombre = next((a for a in args if not a.startswith("-")), None)
            return self.branch(nombre)
        if sub == "switch":
            crear = "-c" in args
            nombre = next((a for a in args if not a.startswith("-")), None)
            if nombre is None:
                return "uso: git switch <rama>."
            return self.switch(nombre, crear=crear)
        if sub == "checkout":
            crear = "-b" in args
            nombre = next((a for a in args if not a.startswith("-")), None)
            if nombre is None:
                return "uso: git checkout <rama>."
            return self.switch(nombre, crear=crear)
        if sub == "merge":
            return self.merge(args[0]) if args else "uso: git merge <rama>."

        return f"git: '{sub}' no es un comando válido (probá 'help')."


AYUDA = """Comandos disponibles:
  git init                      inicia el repositorio
  git status                    muestra el estado
  git add <archivo> | git add . prepara cambios
  git commit -m "mensaje"       guarda la partida
  git log [--oneline]           muestra la historia
  git branch [nombre]           lista o crea ramas
  git switch <rama> [-c]        cambia de rama (-c la crea)
  git checkout <rama> [-b]      igual que switch
  git merge <rama>              fusiona una rama
  touch <archivo>               crea un archivo vacío
  echo "texto" > <archivo>      crea un archivo con contenido
  ls                            lista archivos
  help                          muestra esta ayuda"""


# ======================================================================
#  Desafíos
# ======================================================================
DESAFIOS = [
    {
        "consigna": "Iniciá un repositorio Git.",
        "pista": "git init",
        "check": lambda r, s: r.iniciado,
    },
    {
        "consigna": "Creá un archivo llamado 'equipo.txt'.",
        "pista": 'touch equipo.txt   (o: echo "Pikachu" > equipo.txt)',
        "check": lambda r, s: "equipo.txt" in r.working,
    },
    {
        "consigna": "Prepará 'equipo.txt' para el commit (staging).",
        "pista": "git add equipo.txt",
        "check": lambda r, s: "equipo.txt" in r.staging,
    },
    {
        "consigna": "Hacé tu primer commit con un mensaje.",
        "pista": 'git commit -m "Mi primer commit"',
        "check": lambda r, s: len(r.commits) == 1,
    },
    {
        "consigna": "Mirá el estado del repo (debería estar limpio).",
        "pista": "git status",
        "check": lambda r, s: r.ultimo_comando == "status" and "limpio" in s,
    },
    {
        "consigna": "Hacé un SEGUNDO commit (creá otro archivo, add y commit).",
        "pista": 'touch pokedex.txt → git add . → git commit -m "..."',
        "check": lambda r, s: len(r.commits) >= 2,
    },
    {
        "consigna": "Mostrá la historia de commits.",
        "pista": "git log   (o git log --oneline)",
        "check": lambda r, s: r.ultimo_comando == "log",
    },
    {
        "consigna": "Creá una rama llamada 'nueva-aventura'.",
        "pista": "git branch nueva-aventura",
        "check": lambda r, s: "nueva-aventura" in r.branch_tree,
    },
    {
        "consigna": "Cambiate a la rama 'nueva-aventura' y commiteá un 'secreto.txt' ahí.",
        "pista": "git switch nueva-aventura → touch secreto.txt → git add . → git commit -m \"...\"",
        "check": lambda r, s: "secreto.txt" in r.branch_tree.get("nueva-aventura", {}),
    },
    {
        "consigna": "Volvé a 'main' y fusioná 'nueva-aventura' (así llega secreto.txt).",
        "pista": "git switch main → git merge nueva-aventura",
        "check": lambda r, s: "secreto.txt" in r.branch_tree.get("main", {}),
    },
]


def jugar():
    print("=" * 60)
    print("🔀  SIMULADOR DE GIT — Semana de Descanso")
    print("=" * 60)
    print("Resolvé los 10 desafíos. 'help' para comandos, 'pista' para ayuda,")
    print("'salir' para terminar.\n")

    repo = RepoVirtual()
    indice = 0

    while indice < len(DESAFIOS):
        desafio = DESAFIOS[indice]
        print(f"\n🎯 Desafío {indice + 1}/{len(DESAFIOS)}: {desafio['consigna']}")
        rama = repo.current_branch or "—"
        try:
            linea = input(f"entrenador@git ({rama})$ ")
        except (EOFError, KeyboardInterrupt):
            print("\n¡Hasta la próxima! 👋")
            return

        if linea.strip() == "salir":
            print("¡Hasta la próxima! 👋")
            return
        if linea.strip() == "pista":
            print(f"💡 Pista: {desafio['pista']}")
            continue

        salida = repo.ejecutar(linea)
        if salida:
            print(salida)

        if desafio["check"](repo, salida):
            print("✅ ¡Correcto! Siguiente desafío.")
            indice += 1

    print("\n" + "=" * 60)
    print("🏆 ¡COMPLETASTE EL SIMULADOR DE GIT! Ya sabés guardar tu partida. 💾")
    print("=" * 60)


if __name__ == "__main__":
    jugar()
