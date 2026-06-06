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
