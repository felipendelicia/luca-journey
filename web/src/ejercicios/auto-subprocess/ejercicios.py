"""🖥️ Ejercicios — Ejecutar programas

Una automatización a menudo LLAMA a otros programas (con subprocess.run) y lee su
salida. En el navegador no podemos lanzar procesos reales, así que practicás las dos
mitades que SÍ son lógica pura: armar el comando y procesar su salida.
✅ Corregí cuando termines.
"""


# Armar el comando
# subprocess.run recibe el comando como una LISTA: [programa, arg1, arg2, ...].
# Escribí armar_comando(programa, opciones) donde `opciones` es un dict {flag: valor}.
# Devolvé la lista [programa, flag1, valor1, flag2, valor2, ...] (cada valor como texto).
# Ejemplo:  armar_comando("git", {"--depth": 1})  →  ["git", "--depth", "1"]
def armar_comando(programa, opciones):
    """Devolvé la lista de comando para subprocess."""


# Parsear la salida
# La salida de un programa viene como un texto con varias líneas. Devolvé una lista
# con cada línea SIN espacios al borde, descartando las líneas vacías.
# Ejemplo:  parsear_salida("uno\n\n  dos  \n")  →  ["uno", "dos"]
def parsear_salida(texto):
    """Devolvé las líneas no vacías, sin espacios al borde."""


# Contar líneas
# Devolvé cuántas líneas NO vacías tiene el texto.
# Ejemplo:  contar_lineas("a\n\nb\n")  →  2
def contar_lineas(texto):
    """Devolvé la cantidad de líneas no vacías."""


# Estado del proceso
# subprocess devuelve un returncode: 0 significa que salió bien. `resultado` es un dict
# con la clave "returncode". Devolvé "ok" si es 0, o "error" en cualquier otro caso.
# Ejemplo:  estado({"returncode": 0})  →  "ok"   ·   estado({"returncode": 1})  →  "error"
def estado(resultado):
    """Devolvé 'ok' si returncode es 0, si no 'error'."""
