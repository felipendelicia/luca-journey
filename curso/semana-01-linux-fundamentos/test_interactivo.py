"""
🧪 Tests del Simulador de Terminal Pokémon — Semana 01

Verifican que la TerminalVirtual responda bien a comandos conocidos.
Correlo con:
    pytest semana-01-linux-fundamentos/test_interactivo.py -v
"""

import importlib.util
import os

# Cargamos 'interactivo.py' que está al lado de este test. Usamos un nombre de
# módulo único ("semana01_interactivo") para que no choque con los interactivo.py
# de otras semanas cuando pytest corre todo el curso junto.
_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana01_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


interactivo = _cargar("interactivo")
TerminalVirtual = interactivo.TerminalVirtual
DESAFIOS = interactivo.DESAFIOS


# ----------------------------------------------------------------------
#  pwd y estado inicial
# ----------------------------------------------------------------------
def test_pwd_inicial():
    t = TerminalVirtual()
    assert t.ejecutar("pwd") == "/home/entrenador", (
        "Al arrancar, pwd debería devolver /home/entrenador"
    )


def test_ls_inicial_muestra_bienvenida():
    t = TerminalVirtual()
    salida = t.ejecutar("ls")
    assert "bienvenida.txt" in salida, (
        "El ls inicial debería incluir bienvenida.txt"
    )
    assert "mochila" in salida, "El ls inicial debería incluir la carpeta mochila"


# ----------------------------------------------------------------------
#  mkdir
# ----------------------------------------------------------------------
def test_mkdir_crea_carpeta():
    t = TerminalVirtual()
    t.ejecutar("mkdir pokecenter")
    assert "pokecenter" in t._carpeta_actual(), (
        "mkdir pokecenter debería crear la carpeta en la ubicación actual"
    )


def test_mkdir_carpeta_duplicada_avisa():
    t = TerminalVirtual()
    t.ejecutar("mkdir gimnasio")
    salida = t.ejecutar("mkdir gimnasio")
    assert "ya existe" in salida, (
        "Crear una carpeta que ya existe debería avisar 'ya existe'"
    )


def test_mkdir_varios_a_la_vez():
    t = TerminalVirtual()
    t.ejecutar("mkdir a b c")
    carpeta = t._carpeta_actual()
    assert "a" in carpeta and "b" in carpeta and "c" in carpeta, (
        "mkdir a b c debería crear las tres carpetas"
    )


# ----------------------------------------------------------------------
#  cd y navegación
# ----------------------------------------------------------------------
def test_cd_entra_a_carpeta():
    t = TerminalVirtual()
    t.ejecutar("mkdir pokecenter")
    t.ejecutar("cd pokecenter")
    assert t.pwd() == "/home/entrenador/pokecenter", (
        "cd pokecenter debería cambiar la ruta actual"
    )


def test_cd_punto_punto_sube():
    t = TerminalVirtual()
    t.ejecutar("cd mochila")
    t.ejecutar("cd ..")
    assert t.pwd() == "/home/entrenador", "cd .. debería subir un nivel"


def test_cd_tilde_va_al_home():
    t = TerminalVirtual()
    t.ejecutar("cd mochila")
    t.ejecutar("cd ~")
    assert t.pwd() == "/home/entrenador", "cd ~ debería volver al home"


def test_cd_carpeta_inexistente_da_error():
    t = TerminalVirtual()
    salida = t.ejecutar("cd noexiste")
    assert "no existe" in salida, "cd a carpeta inexistente debería dar error"


def test_cd_a_un_archivo_falla():
    t = TerminalVirtual()
    salida = t.ejecutar("cd bienvenida.txt")
    assert "no es una carpeta" in salida, (
        "cd a un archivo debería avisar que no es una carpeta"
    )


# ----------------------------------------------------------------------
#  touch, echo, cat
# ----------------------------------------------------------------------
def test_touch_crea_archivo_vacio():
    t = TerminalVirtual()
    t.ejecutar("touch pikachu.txt")
    assert t._carpeta_actual().get("pikachu.txt") == "", (
        "touch debería crear un archivo vacío (string vacío)"
    )


def test_echo_redirige_a_archivo():
    t = TerminalVirtual()
    t.ejecutar('echo "Tipo Electrico" > pikachu.txt')
    assert t._carpeta_actual().get("pikachu.txt") == "Tipo Electrico", (
        "echo ... > archivo debería guardar el texto en el archivo"
    )


def test_echo_sin_redireccion_imprime():
    t = TerminalVirtual()
    salida = t.ejecutar("echo hola entrenador")
    assert salida == "hola entrenador", (
        "echo sin > debería imprimir el texto tal cual"
    )


def test_cat_muestra_contenido():
    t = TerminalVirtual()
    t.ejecutar('echo "Rayos!" > nota.txt')
    salida = t.ejecutar("cat nota.txt")
    assert salida == "Rayos!", "cat debería mostrar el contenido del archivo"


def test_cat_archivo_inexistente():
    t = TerminalVirtual()
    salida = t.ejecutar("cat fantasma.txt")
    assert "no existe" in salida, "cat de un archivo inexistente debería avisar"


# ----------------------------------------------------------------------
#  rm
# ----------------------------------------------------------------------
def test_rm_borra_archivo():
    t = TerminalVirtual()
    t.ejecutar("touch borrame.txt")
    t.ejecutar("rm borrame.txt")
    assert "borrame.txt" not in t._carpeta_actual(), (
        "rm debería borrar el archivo"
    )


def test_rm_carpeta_sin_flag_falla():
    t = TerminalVirtual()
    t.ejecutar("mkdir carpeta")
    salida = t.ejecutar("rm carpeta")
    assert "usá rm -r" in salida, (
        "rm de una carpeta sin -r debería pedir el flag -r"
    )


def test_rm_carpeta_con_flag_recursivo():
    t = TerminalVirtual()
    t.ejecutar("mkdir carpeta")
    t.ejecutar("rm -r carpeta")
    assert "carpeta" not in t._carpeta_actual(), (
        "rm -r debería borrar la carpeta entera"
    )


# ----------------------------------------------------------------------
#  comando desconocido
# ----------------------------------------------------------------------
def test_comando_desconocido():
    t = TerminalVirtual()
    salida = t.ejecutar("evolucionar pikachu")
    assert "comando no encontrado" in salida, (
        "Un comando inexistente debería avisar 'comando no encontrado'"
    )


# ----------------------------------------------------------------------
#  Los desafíos: simulamos resolverlos y verificamos los checks.
# ----------------------------------------------------------------------
def test_hay_al_menos_10_desafios():
    assert len(DESAFIOS) >= 10, "Debe haber al menos 10 desafíos"


def test_recorrido_completo_de_desafios():
    """
    Simula a un jugador que resuelve TODOS los desafíos en orden,
    y verifica que cada check dé True en el momento correcto.
    """
    t = TerminalVirtual()
    soluciones = [
        "pwd",
        "ls",
        "mkdir pokecenter",
        "cd pokecenter",
        "touch pikachu.txt",
        'echo "Tipo Electrico" > pikachu.txt',
        "cat pikachu.txt",
        "mkdir gimnasio",  # parte 1 del desafío 8
        "cd gimnasio",     # parte 2 del desafío 8
        "cd ..",
        "rm pikachu.txt",
    ]
    # El desafío 8 requiere dos comandos; los ejecutamos juntos.
    indice_desafio = 0
    i = 0
    while i < len(soluciones) and indice_desafio < len(DESAFIOS):
        salida = t.ejecutar(soluciones[i])
        check = DESAFIOS[indice_desafio]["check"]
        if check(t, salida):
            indice_desafio += 1
        i += 1
    assert indice_desafio == len(DESAFIOS), (
        f"Se completaron {indice_desafio} de {len(DESAFIOS)} desafíos; "
        "el recorrido debería completarlos todos"
    )
