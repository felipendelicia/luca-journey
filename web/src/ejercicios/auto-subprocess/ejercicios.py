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


# Comando a texto
# Recibís un comando como lista y devolvé el texto con los elementos unidos por espacios.
# Ejemplo:  comando_a_texto(["git", "clone", "url"])  →  "git clone url"
def comando_a_texto(comando):
    """Devolvé el comando como un texto."""
    # TU CÓDIGO ACÁ


# Texto a comando
# Recibís un texto y devolvé la lista de sus palabras (el formato que pide subprocess).
# Ejemplo:  texto_a_comando("ls -la /home")  →  ["ls", "-la", "/home"]
def texto_a_comando(texto):
    """Devolvé el texto partido en palabras."""
    # TU CÓDIGO ACÁ


# Agregar una flag
# Devolvé una lista NUEVA con `flag` agregada al final del comando.
def agregar_flag(comando, flag):
    """Devolvé el comando con la flag al final."""
    # TU CÓDIGO ACÁ


# ¿Tiene la flag?
# Devolvé True si `flag` está en el comando.
def tiene_flag(comando, flag):
    """Devolvé True si la flag está en el comando."""
    # TU CÓDIGO ACÁ


# Nombre del programa
# Devolvé el primer elemento del comando (el programa).
def nombre_programa(comando):
    """Devolvé el programa (primer elemento)."""
    # TU CÓDIGO ACÁ


# Cantidad de argumentos
# Devolvé cuántos argumentos tiene el comando SIN contar el programa.
# Ejemplo:  cantidad_argumentos(["git", "clone", "url"])  →  2
def cantidad_argumentos(comando):
    """Devolvé la cantidad de argumentos (sin el programa)."""
    # TU CÓDIGO ACÁ


# Primera línea
# Devolvé la primera línea NO vacía del texto (sin espacios al borde), o "" si no hay.
def primera_linea(texto):
    """Devolvé la primera línea no vacía."""
    # TU CÓDIGO ACÁ


# Última línea
# Devolvé la última línea NO vacía (sin espacios al borde), o "" si no hay.
def ultima_linea(texto):
    """Devolvé la última línea no vacía."""
    # TU CÓDIGO ACÁ


# Líneas que contienen
# Devolvé las líneas (sin espacios al borde) que CONTIENEN `palabra`.
# Ejemplo:  lineas_con("ok: a\nerror: b\nok: c", "ok")  →  ["ok: a", "ok: c"]
def lineas_con(texto, palabra):
    """Devolvé las líneas que contienen palabra."""
    # TU CÓDIGO ACÁ


# Contar líneas que contienen
# Devolvé cuántas líneas contienen `palabra`.
def contar_lineas_con(texto, palabra):
    """Devolvé cuántas líneas contienen palabra."""
    # TU CÓDIGO ACÁ


# ¿Salió bien?
# `resultado` tiene la clave "returncode". Devolvé True si es 0.
def exitoso(resultado):
    """Devolvé True si returncode es 0."""
    # TU CÓDIGO ACÁ


# ¿Falló?
# Devolvé True si el "returncode" NO es 0.
def fallido(resultado):
    """Devolvé True si returncode no es 0."""
    # TU CÓDIGO ACÁ


# Combinar
# Devolvé una lista que empieza con `programa` seguido de todos los `args`.
# Ejemplo:  combinar("python", ["bot.py", "-v"])  →  ["python", "bot.py", "-v"]
def combinar(programa, args):
    """Devolvé [programa] + args."""
    # TU CÓDIGO ACÁ


# Última columna
# Una línea con columnas separadas por espacios. Devolvé la última columna.
# Ejemplo:  ultima_columna("pikachu 25 electrico")  →  "electrico"
def ultima_columna(linea):
    """Devolvé la última columna de la línea."""
    # TU CÓDIGO ACÁ


# Tabla a filas
# De un texto con varias líneas, devolvé una lista donde cada fila es la lista de columnas
# (separadas por espacios). Ignorá las líneas vacías.
# Ejemplo:  tabla_a_filas("a 1\nb 2")  →  [["a", "1"], ["b", "2"]]
def tabla_a_filas(texto):
    """Devolvé las filas como listas de columnas."""
    # TU CÓDIGO ACÁ


# Quitar líneas vacías
# Recibís una lista de líneas. Devolvé solo las que tienen algo (no vacías ni solo espacios).
def quitar_vacias(lineas):
    """Devolvé las líneas no vacías."""
    # TU CÓDIGO ACÁ
