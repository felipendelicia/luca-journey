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
