"""
liga.datos — El "mapa" del curso: las semanas, sus carpetas y los gimnasios.

Acá vive toda la configuración del juego. Si agregás contenido al curso, lo
sumás a estas listas.
"""

# Cada semana del curso como una "ruta" del mapa.
#   id        -> número de semana
#   dir       -> carpeta de la semana
#   nombre    -> título
#   emoji     -> ícono
#   objetivo  -> si es "ejercicios", la Liga evalúa el archivo ejercicios.py del
#                alumno (poniendo CURSO_MODULO=ejercicios). Si es None, corre los
#                tests que ya vienen hechos (semanas de Linux y proyectos).
#   archivo   -> qué test correr (None = toda la carpeta)
SEMANAS = [
    {"id": 1,  "dir": "curso/semana-01-linux-fundamentos",        "nombre": "Linux: Fundamentos",     "emoji": "🐧", "objetivo": None,         "archivo": None},
    {"id": 2,  "dir": "curso/semana-02-linux-intermedio",         "nombre": "Linux: Intermedio",      "emoji": "🐧", "objetivo": None,         "archivo": None},
    {"id": 3,  "dir": "curso/semana-03-python-introduccion",      "nombre": "Python: Introducción",   "emoji": "⚡", "objetivo": "ejercicios", "archivo": "test_ejercicios.py"},
    {"id": 4,  "dir": "curso/semana-04-python-control-de-flujo",  "nombre": "Control de Flujo",       "emoji": "⚡", "objetivo": "ejercicios", "archivo": "test_ejercicios.py"},
    {"id": 5,  "dir": "curso/semana-05-python-funciones",         "nombre": "Funciones",              "emoji": "⚡", "objetivo": "ejercicios", "archivo": "test_ejercicios.py"},
    {"id": 6,  "dir": "curso/semana-06-python-listas-y-colecciones", "nombre": "Listas y Colecciones", "emoji": "⚡", "objetivo": "ejercicios", "archivo": "test_ejercicios.py"},
    {"id": 7,  "dir": "curso/semana-07-python-cadenas-y-archivos","nombre": "Cadenas y Archivos",     "emoji": "⚡", "objetivo": "ejercicios", "archivo": "test_ejercicios.py"},
    {"id": 8,  "dir": "curso/semana-08-python-poo-introduccion",  "nombre": "POO: Introducción",      "emoji": "🔥", "objetivo": "ejercicios", "archivo": "test_ejercicios.py"},
    {"id": 9,  "dir": "curso/semana-09-python-poo-avanzado",      "nombre": "POO: Avanzado",          "emoji": "🔥", "objetivo": "ejercicios", "archivo": "test_ejercicios.py"},
    {"id": 10, "dir": "curso/semana-10-python-modulos-y-pip",     "nombre": "Módulos y pip",          "emoji": "🔥", "objetivo": "ejercicios", "archivo": "test_ejercicios.py"},
    {"id": 11, "dir": "curso/semana-11-python-proyecto-integrador","nombre": "Proyecto: Agenda",      "emoji": "🛠️", "objetivo": None,         "archivo": None},
    {"id": 12, "dir": "curso/semana-12-python-proyecto-final",    "nombre": "Proyecto: Pokédex Web",  "emoji": "🌐", "objetivo": None,         "archivo": None},
]

# Las 8 medallas de gimnasio de Kanto. Cada una se gana al completar sus semanas.
GIMNASIOS = [
    {"id": "roca",     "nombre": "Medalla Roca",     "lider": "Brock",        "emoji": "🪨", "ciudad": "Ciudad Plateada", "requiere": [1, 2]},
    {"id": "cascada",  "nombre": "Medalla Cascada",  "lider": "Misty",        "emoji": "💧", "ciudad": "Ciudad Celeste",  "requiere": [3, 4]},
    {"id": "trueno",   "nombre": "Medalla Trueno",   "lider": "Tnte. Surge",  "emoji": "⚡", "ciudad": "Ciudad Carmín",   "requiere": [5, 6]},
    {"id": "arcoiris", "nombre": "Medalla Arcoíris", "lider": "Erika",        "emoji": "🌈", "ciudad": "Ciudad Azulona",  "requiere": [7]},
    {"id": "alma",     "nombre": "Medalla Alma",     "lider": "Koga",         "emoji": "💜", "ciudad": "Ciudad Fucsia",   "requiere": [8, 9]},
    {"id": "pantano",  "nombre": "Medalla Pantano",  "lider": "Sabrina",      "emoji": "🔮", "ciudad": "Ciudad Azafrán",  "requiere": [10]},
    {"id": "volcan",   "nombre": "Medalla Volcán",   "lider": "Blaine",       "emoji": "🌋", "ciudad": "Isla Canela",     "requiere": [11]},
    {"id": "tierra",   "nombre": "Medalla Tierra",   "lider": "Giovanni",     "emoji": "🌍", "ciudad": "Ciudad Verde",    "requiere": [12]},
]

# Misiones BONUS: no forman parte de la escalera de gimnasios, pero dan EXP y un
# logro especial. La semana de Git es un descanso entre las clases de Python.
BONUS = [
    {"id": "git", "dir": "curso/semana-git-control-de-versiones", "nombre": "Git: Control de Versiones", "emoji": "🔀", "objetivo": None, "archivo": None},
]

# Cuánta EXP da cada test que pasás.
EXP_POR_TEST = 10
# Bonus por completar una semana al 100%.
BONUS_SEMANA_COMPLETA = 50


def semana_por_id(semana_id):
    """Devuelve el dict de la semana con ese id, o None."""
    for s in SEMANAS:
        if s["id"] == semana_id:
            return s
    return None


def bonus_por_id(bonus_id):
    """Devuelve el dict de la misión bonus con ese id, o None."""
    for b in BONUS:
        if b["id"] == bonus_id:
            return b
    return None
