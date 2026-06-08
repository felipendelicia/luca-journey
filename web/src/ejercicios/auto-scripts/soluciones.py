"""⚙️ Soluciones — Scripts y argumentos"""
import argparse


def contar_argumentos(argv):
    return len(argv) - 1


def flag_presente(argv, flag):
    return flag in argv


def valor_de(argv, flag, defecto=None):
    if flag in argv:
        i = argv.index(flag)
        if i + 1 < len(argv):
            return argv[i + 1]
    return defecto


def parsear(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--nivel", type=int, default=1)
    parser.add_argument("--nombre", default="Pikachu")
    parser.add_argument("--shiny", action="store_true")
    return vars(parser.parse_args(argv))


def primer_argumento(argv):
    return argv[0] if argv else None


def ultimo_argumento(argv):
    return argv[-1] if argv else None


def es_flag(arg):
    return arg.startswith("-")


def solo_flags(argv):
    return [a for a in argv if a.startswith("-")]


def sin_flags(argv):
    return [a for a in argv if not a.startswith("-")]


def cantidad_flags(argv):
    return sum(1 for a in argv if a.startswith("-"))


def contar_posicionales(argv):
    return sum(1 for a in argv if not a.startswith("-"))


def posicion_de(argv, arg):
    for i, a in enumerate(argv):
        if a == arg:
            return i
    return -1


def tiene_todas_las_flags(argv, flags):
    return all(f in argv for f in flags)


def quitar_flag(argv, flag):
    return [a for a in argv if a != flag]


def agregar_flag(argv, flag):
    if flag not in argv:
        argv.append(flag)
    return argv


def normalizar_flag(flag):
    return flag.lstrip("-")


def valor_con_igual(argv, clave):
    for a in argv:
        if a.startswith(clave + "="):
            return a[len(clave) + 1:]
    return None


def juntar_argumentos(argv):
    return " ".join(argv)


def reemplazar_flag(argv, viejo, nuevo):
    return [nuevo if a == viejo else a for a in argv]


def hay_flag_repetida(argv):
    flags = [a for a in argv if a.startswith("-")]
    return len(flags) != len(set(flags))
