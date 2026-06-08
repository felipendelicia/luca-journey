"""🖥️ Soluciones — Ejecutar programas"""


def armar_comando(programa, opciones):
    cmd = [programa]
    for flag, valor in opciones.items():
        cmd.append(flag)
        cmd.append(str(valor))
    return cmd


def parsear_salida(texto):
    return [linea.strip() for linea in texto.splitlines() if linea.strip()]


def contar_lineas(texto):
    return len(parsear_salida(texto))


def estado(resultado):
    return "ok" if resultado["returncode"] == 0 else "error"


def comando_a_texto(comando):
    return " ".join(comando)


def texto_a_comando(texto):
    return texto.split()


def agregar_flag(comando, flag):
    return comando + [flag]


def tiene_flag(comando, flag):
    return flag in comando


def nombre_programa(comando):
    return comando[0]


def cantidad_argumentos(comando):
    return len(comando) - 1


def primera_linea(texto):
    for l in texto.split("\n"):
        if l.strip():
            return l.strip()
    return ""


def ultima_linea(texto):
    ult = ""
    for l in texto.split("\n"):
        if l.strip():
            ult = l.strip()
    return ult


def lineas_con(texto, palabra):
    return [l.strip() for l in texto.split("\n") if palabra in l]


def contar_lineas_con(texto, palabra):
    return sum(1 for l in texto.split("\n") if palabra in l)


def exitoso(resultado):
    return resultado["returncode"] == 0


def fallido(resultado):
    return resultado["returncode"] != 0


def combinar(programa, args):
    return [programa] + args


def ultima_columna(linea):
    return linea.split()[-1]


def tabla_a_filas(texto):
    return [l.split() for l in texto.split("\n") if l.strip()]


def quitar_vacias(lineas):
    return [l for l in lineas if l.strip()]
