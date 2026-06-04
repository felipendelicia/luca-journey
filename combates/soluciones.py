"""
✅ combates/soluciones.py — Soluciones de los Combates de Gimnasio.

Cada función es un desafío INTEGRADOR: combina varios temas de una fase del curso.
Son los "jefes de gimnasio". Mirá esto solo después de intentar en desafios.py.
"""


# 🪨 ROCA (Brock) — fase Linux: pensar en archivos y tipos.
def organizar_por_extension(nombres):
    """
    Recibe una lista de nombres de archivo y devuelve un diccionario
    {extension: cantidad}. Los archivos sin punto cuentan como 'sin_extension'.
    """
    conteo = {}
    for nombre in nombres:
        if "." in nombre:
            ext = nombre.rsplit(".", 1)[1]
        else:
            ext = "sin_extension"
        conteo[ext] = conteo.get(ext, 0) + 1
    return conteo


# 💧 CASCADA (Misty) — control de flujo: un duelo por turnos.
def simular_duelo(hp_a, hp_b, dano_a, dano_b):
    """
    Duelo por turnos: ataca A, después B, y así. Devuelve 'a' o 'b' según quién
    deja al otro en 0 primero.
    """
    while True:
        hp_b -= dano_a
        if hp_b <= 0:
            return "a"
        hp_a -= dano_b
        if hp_a <= 0:
            return "b"


# ⚡ TRUENO (Tnte. Surge) — funciones: aplicar una función varias veces.
def aplicar_n_veces(funcion, valor, n):
    """Aplica 'funcion' a 'valor' n veces. aplicar_n_veces(doble, 1, 3) -> 8."""
    for _ in range(n):
        valor = funcion(valor)
    return valor


# 🌈 ARCOÍRIS (Erika) — cadenas: parsear un equipo desde texto.
def parsear_equipo(texto):
    """
    Recibe un texto con líneas 'nombre,tipo,nivel' y devuelve una lista de
    diccionarios. Ignora líneas vacías. El nivel queda como int.
    """
    equipo = []
    for linea in texto.strip().splitlines():
        linea = linea.strip()
        if not linea:
            continue
        nombre, tipo, nivel = linea.split(",")
        equipo.append({"nombre": nombre, "tipo": tipo, "nivel": int(nivel)})
    return equipo


# 💜 ALMA (Koga) — POO: una clase Mochila.
class Mochila:
    """Guarda objetos con su cantidad."""

    def __init__(self):
        self.items = {}

    def agregar(self, item, cantidad=1):
        self.items[item] = self.items.get(item, 0) + cantidad

    def usar(self, item):
        """Usa un objeto (resta 1). Devuelve True si había, False si no."""
        if self.items.get(item, 0) <= 0:
            return False
        self.items[item] -= 1
        return True

    def cantidad(self, item):
        return self.items.get(item, 0)


# 🔮 PANTANO (Sabrina) — módulos/colecciones: estadísticas.
def estadisticas(numeros):
    """
    Devuelve {suma, promedio, maximo, minimo} de una lista de números.
    Si la lista está vacía: suma 0, promedio 0, maximo y minimo None.
    """
    if not numeros:
        return {"suma": 0, "promedio": 0, "maximo": None, "minimo": None}
    return {
        "suma": sum(numeros),
        "promedio": sum(numeros) / len(numeros),
        "maximo": max(numeros),
        "minimo": min(numeros),
    }


# 🌋 VOLCÁN (Blaine) — colecciones: equipo sin tipos repetidos.
def equipo_sin_tipos_repetidos(pokemones):
    """
    Recibe una lista de dicts {nombre, tipo} y devuelve los NOMBRES, quedándose
    solo con el primero de cada tipo (en orden).
    """
    vistos = set()
    resultado = []
    for p in pokemones:
        if p["tipo"] not in vistos:
            vistos.add(p["tipo"])
            resultado.append(p["nombre"])
    return resultado


# 🌍 TIERRA (Giovanni) — capstone: resumen del entrenador.
def resumen_entrenador(capturados, batallas):
    """
    'capturados': lista de nombres. 'batallas': lista de 'gano'/'perdio'.
    Devuelve {total, victorias, porcentaje} (porcentaje de victorias, entero).
    """
    total = len(capturados)
    victorias = batallas.count("gano")
    if len(batallas) == 0:
        porcentaje = 0
    else:
        porcentaje = round((victorias / len(batallas)) * 100)
    return {"total": total, "victorias": victorias, "porcentaje": porcentaje}
